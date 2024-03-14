import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from openai import OpenAI
import json

def read_file(filename):
    with open(filename, 'r') as f:
        text = f.read().strip()
    return text

client = OpenAI(api_key=read_file("./OPENAI_KEY"))

global ai_model
ai_model = "gpt-3.5-turbo"

# Create lists to keep track of GUI elements
textboxes = []
output_textboxes = []
labels = []
buttons = [] # Button Index: 0 Reset, 1 Submit, 2 Add Line, 3 Model


def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def add_textbox():
    new_row_idx = len(textboxes) + 1
    label = ttk.Label(canvas_frame, text=f"Line {new_row_idx}")
    label.grid(row=new_row_idx, column=0, padx=5, pady=5)
    labels.append(label)
    textbox = tk.Text(canvas_frame, height=3, width=30)
    textbox.grid(row=new_row_idx, column=1, padx=5, pady=5)
    textboxes.append(textbox)

# Translates text blocks and renders output text boxes
def submit():
    base_prompt = read_file('./BASE_PROMPT')
    text_lines = []
    for index, textbox in enumerate(textboxes):
        text_lines.append(f"{index + 1}. {{ {textbox.get('1.0', tk.END)} }}\n")

    response = client.chat.completions.create(
    model=ai_model,
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": "".join(text_lines)}
    ]
    )

    # Parse response JSON and render output to adjacent text boxes
    translated_data = json.loads(response.choices[0].message.content)
    for key, value in translated_data.items():
        output_textbox = ttk.Text(canvas_frame, height=3, width=30)
        output_textbox.insert(tk.END, value)
        output_textbox.grid(row=int(key), column=2, padx=5, pady=5)
        output_textboxes.append(output_textbox)
    
# Resets text inputs and text boxes
def reset():
    for box in textboxes:
        box.destroy()
    for box in output_textboxes:
        box.destroy()
    for l in labels:
        l.destroy()
    output_textboxes.clear()
    textboxes.clear()
    add_textbox()

# Toggle between GPT 3.5 Turbo and 4 Turbo
def switch_model():
    global ai_model
    m_button = buttons[3]
    m_button.destroy()
    if ai_model == "gpt-3.5-turbo":
        ai_model = "gpt-4-turbo-preview"
        m_button = ttk.Button(canvas_frame, text="Switch to GPT 3.5 Turbo", command=switch_model, bootstyle=SECONDARY)
        m_button.grid(row=0, column=3, padx=5, pady=5)
    else:
        ai_model = "gpt-3.5-turbo"
        m_button = ttk.Button(canvas_frame, text="Switch to GPT 4 Turbo", command=switch_model, bootstyle=SECONDARY)
        m_button.grid(row=0, column=3, padx=5, pady=5)
    buttons[3] = m_button

# Create the main window
root = ttk.Window()
root.title("Open AI Block Translator")
root.minsize(640, 480)

# Create a Canvas widget with a vertical scrollbar
canvas = ttk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame to contain the widgets inside the canvas
canvas_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=canvas_frame, anchor='nw')

# Configure canvas scrollregion
canvas_frame.bind("<Configure>", on_canvas_configure)

# Bind mousewheel event to canvas for scrolling
canvas.bind("<MouseWheel>", on_mousewheel)

# Create a button to reset input
reset_button = ttk.Button(canvas_frame, text="Reset", command=reset, bootstyle=DANGER)
reset_button.grid(row=0, column=0, padx=5, pady=5)
buttons.append(reset_button)

# Create a button to submit the input
submit_button = ttk.Button(canvas_frame, text="Submit", command=submit, bootstyle=PRIMARY)
submit_button.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
buttons.append(submit_button)

# Create a label for the initial textbox
initial_label = ttk.Label(canvas_frame, text="Line 1")
initial_label.grid(row=1, column=0, padx=5, pady=5)

# Create a textbox for user input
initial_textbox = ttk.Text(canvas_frame, height=3, width=30)
initial_textbox.grid(row=1, column=1, padx=5, pady=5)
textboxes.append(initial_textbox)

# Create a button to add more textboxes
add_button = ttk.Button(canvas_frame, text="Add Line", command=add_textbox, bootstyle=SUCCESS)
add_button.grid(row=0, column=2, padx=5, pady=5)
buttons.append(add_button)

# Create a button to toggle between GPT 3.5 Turbo and GPT 4 Turbo
model_button = ttk.Button(canvas_frame, text="Switch to GPT 4 Turbo", command=switch_model, bootstyle=SECONDARY)
model_button.grid(row=0, column=3, padx=5, pady=5)
buttons.append(model_button)

# Run the application
root.mainloop()
