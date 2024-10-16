import gradio as gr

# theme = gr.themes.Default()
theme = gr.Theme.from_hub("Medguy/randomtheme")

theme.set(
    input_border_width="10px",
)
