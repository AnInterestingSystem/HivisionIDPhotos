import gradio as gr

# theme = gr.themes.Default()
theme = gr.Theme.from_hub("Medguy/randomtheme")

theme.set(
    #overall
    input_border_width="1px",

    #labels
    block_title_text_color="#374151",
    block_title_background_fill='none',
    link_text_color_active="#81c8e0",

    #images
    block_label_text_color="#374151",
    block_label_background_fill="#f0fbfe",

    #checkbox
    checkbox_label_background_fill_selected="#f0fbfe",
    checkbox_label_text_color_selected="#374151",
    checkbox_background_color_selected="#CEE9F2",
    checkbox_border_color_selected="#ADD8E6",

    #button
    button_primary_background_fill="#81c8e0",
    button_primary_background_fill_hover="#1677ff",

    #input
    input_border_color_focus="#f0fbfe",
    input_background_fill_focus="#81c8e0",
)
