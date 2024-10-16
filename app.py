import argparse
import os

import gradio as gr

from ui .processor import IDPhotoProcessor
from ui.theme import theme
from ui.ui import create_ui

LANGUAGE = ["zh", "en", "ko", "ja"]

root_dir = os.path.dirname(os.path.abspath(__file__))
demo = gr.Blocks(title="HivisionIDPhotos", css_paths=[os.path.join(root_dir, "ui/assets/styles.css")], theme=theme)
processor = IDPhotoProcessor()
create_ui(demo, processor, root_dir, LANGUAGE)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--port", type=int, default=7860, help="The port number of the server")
    argument_parser.add_argument("--host", type=str, default="0.0.0.0", help="The host of the server")
    argument_parser.add_argument("--root_path", type=str, default=None, help="The root path of the server, default is None (='/'), e.g. '/myapp'")
    args = argument_parser.parse_args()

    # 如果RUN_MODE是Beast，打印已开启野兽模式
    if os.getenv("RUN_MODE") == "beast":
        print("[Beast mode activated.] 已开启野兽模式。")

    demo.launch(server_name=args.host, server_port=args.port, root_path=args.root_path, show_api=False)
