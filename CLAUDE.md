# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

HivisionIDPhotos is a Python service that generates ID/passport photos from a portrait photo: background removal (matting), face detection/alignment, cropping to a target size, background color/gradient rendering, layout sheet generation (for printing), watermarking, and beautification (whitening/skin smoothing/thin-face). It ships two entry points that both sit on top of the same `hivision` core library:

- **`app.py`** — Gradio web UI (multi-language: zh/en/ko/ja) mounted onto a FastAPI app. This is the interactive demo/product.
- **`deploy_api.py`** — a standalone FastAPI REST API (`/idphoto`, `/human_matting`, `/add_background`, `/generate_layout_photos`, `/watermark`, `/set_kb`, `/idphoto_crop`) for headless/backend integration. It does not depend on the `ui` package.

## Commands

There is no lint/test tooling configured in this repo (no pytest, no ruff/flake8 config, no CI). Development is run-and-manually-verify.

This project uses **uv** for the virtual environment and dependency management (Python >= 3.14 per `pyproject.toml`). Dependencies live in `pyproject.toml`/`uv.lock` (`requirements.txt` has been removed) — use `uv add`/`uv remove` rather than editing `pyproject.toml`'s `dependencies` array by hand, so `uv.lock` stays in sync.

```bash
# create the venv and install/sync dependencies from pyproject.toml/uv.lock
uv sync

# add/remove a dependency (updates pyproject.toml + uv.lock)
uv add <package>
uv remove <package>

# run the Gradio web UI (default port 7860)
uv run app.py --port 7860 --host 0.0.0.0

# run the standalone REST API (default port 8080)
uv run deploy_api.py

# build & push the Docker image (Aliyun registry — requires push access)
./build.bash
```

Set `RUN_MODE=beast` to keep ONNX model sessions resident in memory across requests instead of reloading them each call (see "Model loading" below) — useful for perf testing, heavier on memory.

## Core architecture: `hivision/creator`

Everything funnels through `IDCreator` (`hivision/creator/__init__.py`), a callable class that runs a fixed pipeline over a mutable `Context` (`hivision/creator/context.py`):

1. Resize input to max side 2000px → `ctx.origin_image` / `ctx.processing_image`
2. **Matting** — `self.matting_handler(ctx)` (skipped if `crop_only`)
3. **Beauty** — `self.beauty_handler(ctx)` (whitening/brightness/contrast/sharpen/saturation, always runs)
4. If `change_bg_only`: return early with the matted image as the result
5. **Face detection** — `self.detection_handler(ctx)`, raises `FaceError` unless exactly one face is found
6. **Face alignment** (optional) — re-rotates and re-runs detection if `face_alignment=True` and roll angle > 2°
7. **Adjustment** (`photo_adjuster.py`) — crops/positions the head per `head_measure_ratio` / `head_height_ratio` / `head_top_range`, producing standard + HD outputs plus clothing/typography params

`matting_handler` and `detection_handler` are swappable strategy functions, not hardcoded — always call `choose_handler(creator)` (`hivision/creator/choose_handler.py`) after constructing `IDCreator()` to wire in the production handlers (RetinaFace detection + RMBG matting). Both `app.py`'s processor and `deploy_api.py` do this. `IDCreator` also exposes `before_all` / `after_matting` / `after_detect` / `after_all` callback hooks on the Context for extension points.

`Params` and `Result` (both in `context.py`) are the frozen input/output value objects — `Params` is read-only (name-mangled private attrs + properties), `Result` unpacks via `__iter__` in a fixed order: `standard, hd, matting, clothing_params, typography_params, face`.

### Alternative matting/detection backends

`human_matting.py` and `face_detector.py` each define multiple interchangeable implementations (e.g. `extract_human_rmbg`, `extract_human_mnn_modnet`, `extract_human_birefnet_lite` for matting; `detect_face_retinaface`, `detect_face_mtcnn`, `detect_face_face_plusplus` for detection). Only one pair is wired up by default via `choose_handler`; swapping backends means assigning a different function to `creator.matting_handler` / `creator.detection_handler`.

### Model loading

ONNX sessions (`hivision/creator/human_matting.py`, `face_detector.py`, `retinaface/inference.py`) are lazily loaded into module-level globals on first use and picks CUDA if `onnxruntime.get_device() == "GPU"` else falls back to CPU. Unless `RUN_MODE=beast` is set, sessions are dropped back to `None` after each call (trading latency for memory). Model weight files live under `hivision/creator/weights/` and `hivision/creator/retinaface/weights/` — not all of them are checked into this checkout; missing-weight paths print a warning and return `None` rather than raising.

## `ui/` package (Gradio app only)

- `ui/ui.py` — builds the Gradio Blocks layout (inputs/outputs/event wiring).
- `ui/processor.py` — `IDPhotoProcessor.process(...)`, the single entry point the Gradio submit button calls. Internally it: builds an `idphoto_json` config dict from the raw Gradio component values, resolves size/color modes (including custom px/mm size and RGB/hex color), invokes `IDCreator`, renders the background, applies watermark, generates layout + template previews, and writes output files sized to a target KB/DPI.
- `ui/locales.py` — all UI strings and per-language option lists (`LOCALES[section][language]`); size/color mode dispatch in `processor.py` is done by comparing against `LOCALES[...][language]["choices"]` indices, so changing the order of `choices` for a locale changes control flow — keep en/zh/ko/ja choice lists in the same order.
- `ui/request.py` — task/quota bookkeeping (`create_task`, `save_task_result`, `save_failed_task`) around each generation request.
- `ui/config.py` — loads size/color preset CSVs from `ui/assets/*.csv` into the structures `locales.py`/`processor.py` expect.

## `hivision/plugin`

Optional post-processing plugins invoked from the core pipeline or from `ui/processor.py`, independent of the matting/detection strategy pattern above:
- `plugin/beauty/` — whitening, skin smoothing, thin-face (`handler.py` exposes `beauty_face`, always called by `IDCreator` regardless of strength settings — strength 0 is a no-op).
- `plugin/watermark.py` — text watermarking on the final image.
- `plugin/template/template_calculator.py` — composites the HD result into preset template photos.

## Conventions

- Source comments and docstrings in `hivision/` are written in Chinese; keep this consistent when editing that package.
- Images are moved around as raw `numpy.ndarray` (BGR or BGRA depending on stage) rather than PIL objects almost everywhere except at ONNX pre/post-processing boundaries — check `image2bgr` / `cv2.split`/`cv2.merge` usage patterns in the surrounding function before changing channel order.
