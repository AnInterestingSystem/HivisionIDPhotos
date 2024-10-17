import io
import logging
import os

import gradio as gr
import requests
from PIL import Image
from numpy import ndarray

chatbot_backend_base_url = "http://localhost:8080/api"
if os.environ.get("ENV") == "prod":
    chatbot_backend_base_url = "https://app.iknow.plus/api"


def create_task(request: gr.Request, input_image: ndarray) -> int | None:
    user_agent = request.request.headers.get("user-agent")
    is_mini_program = False
    if "miniProgram" in user_agent or "MicroMessenger" in user_agent:
        is_mini_program = True

    headers = {}
    token = request.request.query_params.get("token")
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    elif not is_mini_program:
        return None

    pil_image = Image.fromarray(input_image)
    image_bytes_io = io.BytesIO()
    pil_image.save(image_bytes_io, format="PNG")
    image_bytes = image_bytes_io.getvalue()

    params = {
        "isMiniProgram": is_mini_program
    }
    files = {
        "inputImage": ("input-image.png", image_bytes, "image/png")
    }
    response = requests.post(f"{chatbot_backend_base_url}/idPhoto/createTask", headers=headers, params=params, files=files)
    if response.status_code != 200:
        logging.error(f"Failed to create task. Response status code: {response.status_code}")
        return None

    status_response = response.json()
    if status_response.get("status") != "SUCCESS":
        logging.error(f"Failed to create task. Reason: {status_response.get('reason')}")
        return None

    return status_response["payload"]

# def save_task_result(request: gr.Request) -> None:
#
