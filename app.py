import argparse
import os

import gradio as gr
import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse

from ui.processor import IDPhotoProcessor
from ui.theme import theme
from ui.ui import create_ui

LANGUAGE = ["zh", "en", "ko", "ja"]

root_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()


@app.get("/AXanVx083s.txt")
async def get_text_file():
    return FileResponse(os.path.join(root_dir, "ui/assets/AXanVx083s.txt"))


blocks = gr.Blocks(title="iKnow", css_paths=[os.path.join(root_dir, "ui/assets/styles.css")], theme=theme, delete_cache=(86400, 86400))
processor = IDPhotoProcessor()
create_ui(blocks, processor, root_dir, LANGUAGE)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--port", type=int, default=7860, help="The port number of the server")
    argument_parser.add_argument("--host", type=str, default="0.0.0.0", help="The host of the server")
    args = argument_parser.parse_args()

    # 如果RUN_MODE是Beast，打印已开启野兽模式
    if os.getenv("RUN_MODE") == "beast":
        print("[Beast mode activated.] 已开启野兽模式。")

    # blocks.launch(server_name=args.host, server_port=args.port, favicon_path=os.path.join(root_dir, "ui/assets/favicon.ico"), show_api=False, max_file_size="10mb")
    app = gr.mount_gradio_app(app, blocks, path="/", favicon_path=os.path.join(root_dir, "ui/assets/favicon.ico"), max_file_size="10mb")
    uvicorn.run(app, host=args.host, port=args.port)
