import io
import logging
import os

import gradio as gr
import requests
from PIL import Image
from numpy import ndarray

INPUT_IMAGE_MAX_SIZE = 10_000_000

chatbot_backend_base_url = "http://localhost:8080/api"
if os.environ.get("ENV") == "prod":
    chatbot_backend_base_url = "https://app.iknow.plus/api"


def create_task(request: gr.Request, input_image: ndarray) -> int:
    user_agent = request.request.headers.get("user-agent")
    is_mini_program = False
    if "miniProgram" in user_agent or "MicroMessenger" in user_agent:
        is_mini_program = True

    headers = {}
    token = request.request.query_params.get("token")
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    elif not is_mini_program:
        return -1

    pil_image = Image.fromarray(input_image)
    image_bytes_io = io.BytesIO()
    image_bytes: bytes = b''
    for quality in range(95, 5, -10):
        pil_image.save(image_bytes_io, format="JPEG", optimize=True, quality=75)
        image_bytes = image_bytes_io.getvalue()
        if len(image_bytes) <= INPUT_IMAGE_MAX_SIZE:
            break
    if len(image_bytes) == 0 or len(image_bytes) >= INPUT_IMAGE_MAX_SIZE:
        return -2

    params = {
        "type": "ID",
        "isMiniProgram": is_mini_program
    }
    files = {
        "inputImage": ("input-image.jpg", image_bytes, "image/jpeg")
    }
    response = requests.post(f"{chatbot_backend_base_url}/photoEdit/createTask", headers=headers, params=params, files=files)
    if response.status_code != 200:
        logging.error(f"Failed to create task. Response status code: {response.status_code}")
        return -3

    status_response = response.json()
    if status_response.get("status") != "SUCCESS":
        logging.error(f"Failed to create task. Reason: {status_response.get('reason')}")
        return -3

    return status_response["payload"]


def save_failed_task(request: gr.Request, task_id: int) -> None:
    user_agent = request.request.headers.get("user-agent")
    is_mini_program = False
    if "miniProgram" in user_agent or "MicroMessenger" in user_agent:
        is_mini_program = True

    headers = {}
    token = request.request.query_params.get("token")
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    elif not is_mini_program:
        return

    params = {
        "id": task_id,
        "status": "FAILED",
        "isMiniProgram": is_mini_program
    }
    response = requests.post(f"{chatbot_backend_base_url}/photoEdit/saveTask", headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"Failed to save task. Response status code: {response.status_code}")
        return

    status_response = response.json()
    if status_response.get("status") != "SUCCESS":
        logging.error(f"Failed to save task. Reason: {status_response.get('reason')}")
        return


def save_task_result(
    request: gr.Request,
    task_id: int,
    jpeg_format_option: bool,
    img_output_standard: str,
    img_output_standard_hd: str,
    img_output_standard_png: ndarray,
    img_output_standard_hd_png: ndarray,
    img_output_layout: str,
    img_output_templates: list[ndarray],
) -> None:
    user_agent = request.request.headers.get("user-agent")
    is_mini_program = False
    if "miniProgram" in user_agent or "MicroMessenger" in user_agent:
        is_mini_program = True

    headers = {}
    token = request.request.query_params.get("token")
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    elif not is_mini_program:
        return

    params = {
        "id": task_id,
        "status": "SUCCEEDED",
        "isMiniProgram": is_mini_program
    }
    with (open(img_output_standard, "rb") as standard_file,
          # open(img_output_standard_hd, "rb") as hd_file,
          open(img_output_layout, "rb") as layout_file):
        # matting_standard_pil_image = Image.fromarray(img_output_standard_png)
        # matting_standard_image_bytes_io = io.BytesIO()
        # matting_standard_pil_image.save(matting_standard_image_bytes_io, format="PNG")
        # matting_standard_image_bytes = matting_standard_image_bytes_io.getvalue()
        #
        # matting_hd_pil_image = Image.fromarray(img_output_standard_hd_png)
        # matting_hd_image_bytes_io = io.BytesIO()
        # matting_hd_pil_image.save(matting_hd_image_bytes_io, format="PNG")
        # matting_hd_image_bytes = matting_hd_image_bytes_io.getvalue()

        extension_name = "jpeg" if jpeg_format_option else "png"
        files = {
            "standard-file": (f"standard-file.{extension_name}", standard_file, f"image/{extension_name}"),
            # "hd-file": (f"hd-file.{extension_name}", hd_file, f"image/{extension_name}"),
            "layout-file": (f"layout-file.{extension_name}", layout_file, f"image/{extension_name}"),
            # "matting-standard-file": ("matting-standard-file.png", matting_standard_image_bytes, "image/png"),
            # "matting-hd-file": ("matting-hd-file.png", matting_hd_image_bytes, "image/png"),
        }

        # for i in range(len(img_output_templates)):
        #     template_pil_image = Image.fromarray(img_output_templates[0])
        #     template_image_bytes_io = io.BytesIO()
        #     template_pil_image.save(template_image_bytes_io, format="PNG")
        #     template_image_bytes = template_image_bytes_io.getvalue()
        #     files[f"template-file-{i}"] = (f"template-file-{i}.png", template_image_bytes, "image/png")

        response = requests.post(f"{chatbot_backend_base_url}/photoEdit/saveTask", headers=headers, params=params, files=files)
        if response.status_code != 200:
            logging.error(f"Failed to save task. Response status code: {response.status_code}")
            return

        status_response = response.json()
        if status_response.get("status") != "SUCCESS":
            logging.error(f"Failed to save task. Reason: {status_response.get('reason')}")
            return
