import argparse
import os

from demo.processor import IDPhotoProcessor
from demo.ui import create_ui

root_dir = os.path.dirname(os.path.abspath(__file__))

LANGUAGE = ["zh", "en", "ko", "ja"]

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--port", type=int, default=7860, help="The port number of the server")
    argument_parser.add_argument("--host", type=str, default="0.0.0.0", help="The host of the server")
    argument_parser.add_argument("--root_path", type=str, default=None, help="The root path of the server, default is None (='/'), e.g. '/myapp'")
    args = argument_parser.parse_args()

    processor = IDPhotoProcessor()

    demo = create_ui(processor, root_dir, LANGUAGE)

    # 如果RUN_MODE是Beast，打印已开启野兽模式
    if os.getenv("RUN_MODE") == "beast":
        print("[Beast mode activated.] 已开启野兽模式。")

    demo.launch(server_name=args.host, server_port=args.port, root_path=args.root_path, show_api=False)
