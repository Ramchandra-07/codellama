import requests
import json
import gradio as gr

# API URL and headers
url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}

# Conversation history
history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model": "codeguru",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        data = response.json()
        actual_response = data.get('response', 'No response found.')
        return actual_response
    else:
        return f"Error: {response.status_code} - {response.text}"

def clear_history():
    """Clear the conversation history."""
    history.clear()
    return "History cleared! Start a new prompt."

# Improved Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as interface:
    gr.Markdown(
        "<h1 style='text-align: center; color: #ff6600;'>🚀 Interactive AI Code Assistant</h1>"
        "<p style='text-align: center;'>Enter your prompt and get AI-generated responses instantly!</p>"
    )

    with gr.Row():
        with gr.Column(scale=1):
            prompt_input = gr.Textbox(
                lines=4,
                placeholder="Enter your prompt here...",
                label="Prompt",
                elem_id="prompt-box"
            )

            with gr.Row():
                submit_btn = gr.Button("Submit", variant="primary")
                clear_btn = gr.Button("Clear History", variant="secondary")

        with gr.Column(scale=2):
            response_output = gr.Textbox(
                lines=18,  # Larger response window
                interactive=True,
                label="AI Response",
                placeholder="Response will appear here...",
                elem_id="response-box"
            )

    # Event bindings
    submit_btn.click(fn=generate_response, inputs=prompt_input, outputs=response_output)
    clear_btn.click(fn=clear_history, outputs=response_output)

interface.launch()
