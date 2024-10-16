import gradio as gr


def check_auth(request: gr.Request) -> bool:
    user_agent = request.request.headers.get("user-agent")
    if "miniProgram" in user_agent or "MicroMessenger" in user_agent:
        return True

    return False
