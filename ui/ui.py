import os
import pathlib

import gradio as gr
from gradio import Blocks

from .locales import LOCALES
from .processor import IDPhotoProcessor

"""
只裁切模式:
1. 如果重新上传了照片，然后点击按钮，第一次会调用不裁切的模式，第二次会调用裁切的模式
"""


def load_description(fp):
    """
    加载title.md文件作为Demo的顶部栏
    """
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def create_ui(demo: Blocks, processor: IDPhotoProcessor, root_dir: str, language: list):
    # 加载环境变量DEFAULT_LANG, 如果有且在language中，则将DEFAULT_LANG设置为环境变量
    if "DEFAULT_LANG" in os.environ and os.environ["DEFAULT_LANG"] in language:
        default_lang = os.environ["DEFAULT_LANG"]
    else:
        default_lang = language[0]

    with demo:
        gr.HTML(load_description(os.path.join(root_dir, "ui/assets/title.md")))
        with gr.Row():
            # ------------------------ 左半边 UI ------------------------
            with gr.Column(elem_classes=["left-container"]):
                img_input = gr.Image(height=400)

                with gr.Row():
                    # 语言选择器
                    language_options = gr.Dropdown(choices=language, label="语种", value=default_lang)

                # TAB1 - 关键参数 ------------------------------------------------
                with gr.Tab(LOCALES["key_param"][default_lang]["label"]) as key_parameter_tab:
                    # 尺寸模式
                    with gr.Row():
                        mode_options = gr.Radio(choices=LOCALES["size_mode"][default_lang]["choices"], label=LOCALES["size_mode"][default_lang]["label"], value=LOCALES["size_mode"][default_lang]["choices"][0], min_width=520)

                    # 尺寸列表
                    with gr.Row(visible=True) as size_list_row:
                        size_list_options = gr.Dropdown(choices=LOCALES["size_list"][default_lang]["choices"], label=LOCALES["size_list"][default_lang]["label"], value=LOCALES["size_list"][default_lang]["choices"][0], elem_id="size_list")
                    # 自定义尺寸px
                    with gr.Row(visible=False) as custom_size_px:
                        custom_size_height_px = gr.Number(value=413, label=LOCALES["custom_size_px"][default_lang]["height"], interactive=True)
                        custom_size_width_px = gr.Number(value=295, label=LOCALES["custom_size_px"][default_lang]["width"], interactive=True)
                    # 自定义尺寸mm
                    with gr.Row(visible=False) as custom_size_mm:
                        custom_size_height_mm = gr.Number(value=35, label=LOCALES["custom_size_mm"][default_lang]["height"], interactive=True)
                        custom_size_width_mm = gr.Number(value=25, label=LOCALES["custom_size_mm"][default_lang]["width"], interactive=True)

                    # 背景颜色
                    color_options = gr.Radio(choices=LOCALES["bg_color"][default_lang]["choices"], label=LOCALES["bg_color"][default_lang]["label"], value=LOCALES["bg_color"][default_lang]["choices"][0])

                    # 自定义颜色RGB
                    with gr.Row(visible=False) as custom_color_rgb:
                        custom_color_r = gr.Number(value=0, label="R", minimum=0, maximum=255, interactive=True)
                        custom_color_g = gr.Number(value=0, label="G", minimum=0, maximum=255, interactive=True)
                        custom_color_b = gr.Number(value=0, label="B", minimum=0, maximum=255, interactive=True)

                    # 自定义颜色HEX
                    with gr.Row(visible=False) as custom_color_hex:
                        custom_color_hex_value = gr.Text(value="000000", label="Hex", interactive=True)

                    # 渲染模式
                    render_options = gr.Radio(choices=LOCALES["render_mode"][default_lang]["choices"], label=LOCALES["render_mode"][default_lang]["label"], value=LOCALES["render_mode"][default_lang]["choices"][0])

                    with gr.Row():
                        # 插件模式
                        plugin_options = gr.CheckboxGroup(label=LOCALES["plugin"][default_lang]["label"], choices=LOCALES["plugin"][default_lang]["choices"], interactive=True, value=LOCALES["plugin"][default_lang]["value"])

                # TAB2 - 高级参数 ------------------------------------------------
                with gr.Tab(LOCALES["advance_param"][default_lang]["label"]) as advance_parameter_tab:
                    head_measure_ratio_option = gr.Slider(minimum=0.1, maximum=0.5, value=0.2, step=0.01, label=LOCALES["head_measure_ratio"][default_lang]["label"], interactive=True)
                    top_distance_option = gr.Slider(minimum=0.02, maximum=0.5, value=0.12, step=0.01, label=LOCALES["top_distance"][default_lang]["label"], interactive=True)

                    image_kb_options = gr.Radio(choices=LOCALES["image_kb"][default_lang]["choices"], label=LOCALES["image_kb"][default_lang]["label"], value=LOCALES["image_kb"][default_lang]["choices"][0])

                    custom_image_kb_size = gr.Slider(minimum=10, maximum=1000, value=50, label=LOCALES["image_kb_size"][default_lang]["label"], interactive=True, visible=False)

                    image_dpi_options = gr.Radio(choices=LOCALES["image_dpi"][default_lang]["choices"], label=LOCALES["image_dpi"][default_lang]["label"], value=LOCALES["image_dpi"][default_lang]["choices"][0])
                    custom_image_dpi_size = gr.Slider(minimum=72, maximum=600, value=300, label=LOCALES["image_dpi_size"][default_lang]["label"], interactive=True, visible=False)

                # TAB3 - 美颜 ------------------------------------------------
                with gr.Tab(LOCALES["beauty_tab"][default_lang]["label"]) as beauty_parameter_tab:
                    # 美白组件
                    whitening_option = gr.Slider(label=LOCALES["whitening_strength"][default_lang]["label"], minimum=0, maximum=15, value=2, step=1, interactive=True)

                    with gr.Row():
                        # 亮度组件
                        brightness_option = gr.Slider(label=LOCALES["brightness_strength"][default_lang]["label"], minimum=-5, maximum=25, value=0, step=1, interactive=True)
                        # 对比度组件
                        contrast_option = gr.Slider(label=LOCALES["contrast_strength"][default_lang]["label"], minimum=-10, maximum=50, value=0, step=1, interactive=True)
                        # 饱和度组件
                        saturation_option = gr.Slider(label=LOCALES["saturation_strength"][default_lang]["label"], minimum=-10, maximum=50, value=0, step=1, interactive=True)

                    # 锐化组件
                    sharpen_option = gr.Slider(label=LOCALES["sharpen_strength"][default_lang]["label"], minimum=0, maximum=5, value=0, step=1, interactive=True)

                # TAB4 - 水印 ------------------------------------------------
                with gr.Tab(LOCALES["watermark_tab"][default_lang]["label"]) as watermark_parameter_tab:
                    watermark_options = gr.Radio(choices=LOCALES["watermark_switch"][default_lang]["choices"], label=LOCALES["watermark_switch"][default_lang]["label"], value=LOCALES["watermark_switch"][default_lang]["choices"][0])

                    with gr.Row():
                        watermark_text_options = gr.Text(
                            max_length=20,
                            label=LOCALES["watermark_text"][default_lang]["label"],
                            value=LOCALES["watermark_text"][default_lang]["value"],
                            placeholder=LOCALES["watermark_text"][default_lang]["placeholder"],
                            interactive=False,
                        )
                        watermark_text_color = gr.ColorPicker(label=LOCALES["watermark_color"][default_lang]["label"], interactive=False, value="#FFFFFF")

                    watermark_text_size = gr.Slider(minimum=10, maximum=100, value=20, label=LOCALES["watermark_size"][default_lang]["label"], interactive=False, step=1)

                    watermark_text_opacity = gr.Slider(minimum=0, maximum=1, value=0.15, label=LOCALES["watermark_opacity"][default_lang]["label"], interactive=False, step=0.01)

                    watermark_text_angle = gr.Slider(minimum=0, maximum=360, value=30, label=LOCALES["watermark_angle"][default_lang]["label"], interactive=False, step=1)

                    watermark_text_space = gr.Slider(minimum=10, maximum=200, value=25, label=LOCALES["watermark_space"][default_lang]["label"], interactive=False, step=1)

                    def update_watermark_text_visibility(choice, language):
                        return [gr.update(interactive=(choice == LOCALES["watermark_switch"][language]["choices"][1]))] * 6

                    watermark_options.change(
                        fn=update_watermark_text_visibility,
                        inputs=[
                            watermark_options,
                            language_options,
                        ],
                        outputs=[
                            watermark_text_options,
                            watermark_text_color,
                            watermark_text_size,
                            watermark_text_opacity,
                            watermark_text_angle,
                            watermark_text_space,
                        ],
                    )

                img_but = gr.Button(LOCALES["button"][default_lang]["label"], elem_id="btn", variant="primary")

                gr.Examples(inputs=[img_input], examples=[[path.as_posix()] for path in sorted(pathlib.Path(os.path.join(root_dir, "ui/images")).rglob("*.jpg"))])

            # ---------------- 右半边 UI ----------------
            with gr.Column(elem_classes=["right-container"]):
                notification = gr.Text(label=LOCALES["notification"][default_lang]["label"], visible=False)
                with gr.Row(elem_classes=["right-row-container"]):
                    # 标准照
                    img_output_standard = gr.Image(label=LOCALES["standard_photo"][default_lang]["label"], height=350, format="png")
                    # 高清照
                    img_output_standard_hd = gr.Image(label=LOCALES["hd_photo"][default_lang]["label"], height=350, format="png")
                # 排版照
                img_output_layout = gr.Image(label=LOCALES["layout_photo"][default_lang]["label"], height=350, format="png", elem_classes=["right-row-container"])
                # 模版照片
                with gr.Accordion(LOCALES["template_photo"][default_lang]["label"], open=True, elem_classes=["label-wrap"]) as template_image_accordion:
                    img_output_template = gr.Gallery(label=LOCALES["template_photo"][default_lang]["label"], height=350, format="png")
                # 抠图图像
                with gr.Accordion(LOCALES["matting_image"][default_lang]["label"], open=True) as matting_image_accordion:
                    with gr.Row():
                        img_output_standard_png = gr.Image(label=LOCALES["standard_photo_png"][default_lang]["label"], height=350, format="png", elem_id="standard_photo_png")
                        img_output_standard_hd_png = gr.Image(label=LOCALES["hd_photo_png"][default_lang]["label"], height=350, format="png", elem_id="hd_photo_png")

            # ---------------- 多语言切换函数 ----------------
            def change_language(language):
                return {
                    size_list_options: gr.update(label=LOCALES["size_list"][language]["label"], choices=LOCALES["size_list"][language]["choices"], value=LOCALES["size_list"][language]["choices"][0]),
                    mode_options: gr.update(label=LOCALES["size_mode"][language]["label"], choices=LOCALES["size_mode"][language]["choices"], value=LOCALES["size_mode"][language]["choices"][0]),
                    color_options: gr.update(label=LOCALES["bg_color"][language]["label"], choices=LOCALES["bg_color"][language]["choices"], value=LOCALES["bg_color"][language]["choices"][0]),
                    img_but: gr.update(value=LOCALES["button"][language]["label"]),
                    render_options: gr.update(label=LOCALES["render_mode"][language]["label"], choices=LOCALES["render_mode"][language]["choices"], value=LOCALES["render_mode"][language]["choices"][0]),
                    image_kb_options: gr.update(label=LOCALES["image_kb_size"][language]["label"], choices=LOCALES["image_kb"][language]["choices"], value=LOCALES["image_kb"][language]["choices"][0]),
                    custom_image_kb_size: gr.update(label=LOCALES["image_kb"][language]["label"]),
                    notification: gr.update(label=LOCALES["notification"][language]["label"]),
                    img_output_standard: gr.update(label=LOCALES["standard_photo"][language]["label"]),
                    img_output_standard_hd: gr.update(label=LOCALES["hd_photo"][language]["label"]),
                    img_output_standard_png: gr.update(label=LOCALES["standard_photo_png"][language]["label"]),
                    img_output_standard_hd_png: gr.update(label=LOCALES["hd_photo_png"][language]["label"]),
                    img_output_layout: gr.update(label=LOCALES["layout_photo"][language]["label"]),
                    head_measure_ratio_option: gr.update(label=LOCALES["head_measure_ratio"][language]["label"]),
                    top_distance_option: gr.update(label=LOCALES["top_distance"][language]["label"]),
                    key_parameter_tab: gr.update(label=LOCALES["key_param"][language]["label"]),
                    advance_parameter_tab: gr.update(label=LOCALES["advance_param"][language]["label"]),
                    watermark_parameter_tab: gr.update(label=LOCALES["watermark_tab"][language]["label"]),
                    watermark_text_options: gr.update(label=LOCALES["watermark_text"][language]["label"], placeholder=LOCALES["watermark_text"][language]["placeholder"]),
                    watermark_text_color: gr.update(label=LOCALES["watermark_color"][language]["label"]),
                    watermark_text_size: gr.update(label=LOCALES["watermark_size"][language]["label"]),
                    watermark_text_opacity: gr.update(label=LOCALES["watermark_opacity"][language]["label"]),
                    watermark_text_angle: gr.update(label=LOCALES["watermark_angle"][language]["label"]),
                    watermark_text_space: gr.update(label=LOCALES["watermark_space"][language]["label"]),
                    watermark_options: gr.update(label=LOCALES["watermark_switch"][language]["label"], choices=LOCALES["watermark_switch"][language]["choices"], value=LOCALES["watermark_switch"][language]["choices"][0]),
                    matting_image_accordion: gr.update(label=LOCALES["matting_image"][language]["label"]),
                    beauty_parameter_tab: gr.update(label=LOCALES["beauty_tab"][language]["label"]),
                    whitening_option: gr.update(label=LOCALES["whitening_strength"][language]["label"]),
                    image_dpi_options: gr.update(label=LOCALES["image_dpi"][language]["label"], choices=LOCALES["image_dpi"][language]["choices"], value=LOCALES["image_dpi"][language]["choices"][0]),
                    custom_image_dpi_size: gr.update(label=LOCALES["image_dpi"][language]["label"]),
                    brightness_option: gr.update(label=LOCALES["brightness_strength"][language]["label"]),
                    contrast_option: gr.update(label=LOCALES["contrast_strength"][language]["label"]),
                    sharpen_option: gr.update(label=LOCALES["sharpen_strength"][language]["label"]),
                    saturation_option: gr.update(label=LOCALES["saturation_strength"][language]["label"]),
                    custom_size_width_px: gr.update(label=LOCALES["custom_size_px"][language]["width"]),
                    custom_size_height_px: gr.update(label=LOCALES["custom_size_px"][language]["height"]),
                    custom_size_width_mm: gr.update(label=LOCALES["custom_size_mm"][language]["width"]),
                    custom_size_height_mm: gr.update(label=LOCALES["custom_size_mm"][language]["height"]),
                    img_output_template: gr.update(label=LOCALES["template_photo"][language]["label"]),
                    template_image_accordion: gr.update(label=LOCALES["template_photo"][language]["label"]),
                    plugin_options: gr.update(label=LOCALES["plugin"][language]["label"], choices=LOCALES["plugin"][language]["choices"], value=LOCALES["plugin"][language]["choices"][0]),
                }

            def change_visibility(option, lang, locales_key, custom_component):
                return {
                    custom_component: gr.update(visible=option == LOCALES[locales_key][lang]["choices"][-1])
                }

            def change_color(colors, lang):
                return {
                    custom_color_rgb: gr.update(visible=colors == LOCALES["bg_color"][lang]["choices"][-2]),
                    custom_color_hex: gr.update(visible=colors == LOCALES["bg_color"][lang]["choices"][-1]),
                }

            def change_size_mode(size_option_item, lang):
                choices = LOCALES["size_mode"][lang]["choices"]
                # 如果选择自定义尺寸mm
                if size_option_item == choices[3]:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=True),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=True),
                    }
                # 如果选择自定义尺寸px
                elif size_option_item == choices[2]:
                    return {
                        custom_size_px: gr.update(visible=True),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=True),
                    }
                # 如果选择只换底，则隐藏所有尺寸组件
                elif size_option_item == choices[1]:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=False),
                    }
                # 如果选择预设尺寸，则隐藏自定义尺寸组件
                else:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=True),
                        plugin_options: gr.update(interactive=True),
                    }

            def change_image_kb(image_kb_option, lang):
                return change_visibility(image_kb_option, lang, "image_kb", custom_image_kb_size)

            def change_image_dpi(image_dpi_option, lang):
                return change_visibility(image_dpi_option, lang, "image_dpi", custom_image_dpi_size)

            # ---------------- 绑定事件 ----------------
            # 语言切换
            language_options.input(
                change_language,
                inputs=[
                    language_options
                ],
                outputs=[
                    size_list_options,
                    mode_options,
                    color_options,
                    img_but,
                    render_options,
                    image_kb_options,
                    custom_image_kb_size,
                    notification,
                    img_output_standard,
                    img_output_standard_hd,
                    img_output_standard_png,
                    img_output_standard_hd_png,
                    img_output_layout,
                    head_measure_ratio_option,
                    top_distance_option,
                    key_parameter_tab,
                    advance_parameter_tab,
                    watermark_parameter_tab,
                    watermark_text_options,
                    watermark_text_color,
                    watermark_text_size,
                    watermark_text_opacity,
                    watermark_text_angle,
                    watermark_text_space,
                    watermark_options,
                    matting_image_accordion,
                    beauty_parameter_tab,
                    whitening_option,
                    image_dpi_options,
                    custom_image_dpi_size,
                    brightness_option,
                    contrast_option,
                    sharpen_option,
                    saturation_option,
                    plugin_options,
                    custom_size_width_px,
                    custom_size_height_px,
                    custom_size_width_mm,
                    custom_size_height_mm,
                    img_output_template,
                    template_image_accordion,
                ],
            )

            # ---------------- 设置隐藏/显示交互效果 ----------------
            # 尺寸模式
            mode_options.input(change_size_mode, inputs=[mode_options, language_options], outputs=[custom_size_px, custom_size_mm, size_list_row, plugin_options])

            # 颜色
            color_options.input(change_color, inputs=[color_options, language_options], outputs=[custom_color_rgb, custom_color_hex])

            # 图片kb
            image_kb_options.input(change_image_kb, inputs=[image_kb_options, language_options], outputs=[custom_image_kb_size])

            # 图片dpi
            image_dpi_options.input(change_image_dpi, inputs=[image_dpi_options, language_options], outputs=[custom_image_dpi_size])

            img_but.click(
                processor.process,
                inputs=[
                    img_input,
                    mode_options,
                    size_list_options,
                    color_options,
                    render_options,
                    image_kb_options,
                    custom_color_r,
                    custom_color_g,
                    custom_color_b,
                    custom_color_hex_value,
                    custom_size_height_px,
                    custom_size_width_px,
                    custom_size_height_mm,
                    custom_size_width_mm,
                    custom_image_kb_size,
                    language_options,
                    watermark_options,
                    watermark_text_options,
                    watermark_text_color,
                    watermark_text_size,
                    watermark_text_opacity,
                    watermark_text_angle,
                    watermark_text_space,
                    head_measure_ratio_option,
                    top_distance_option,
                    whitening_option,
                    image_dpi_options,
                    custom_image_dpi_size,
                    brightness_option,
                    contrast_option,
                    sharpen_option,
                    saturation_option,
                    plugin_options,
                ],
                outputs=[
                    img_output_standard,
                    img_output_standard_hd,
                    img_output_standard_png,
                    img_output_standard_hd_png,
                    img_output_layout,
                    img_output_template,
                    template_image_accordion,
                    notification,
                ],
            )
