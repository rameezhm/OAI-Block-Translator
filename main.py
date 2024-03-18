import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from openai import OpenAI
import json

def read_file(filename):
    with open(filename, 'r') as f:
        text = f.read().strip()
    return text

config_json = json.loads(read_file("./config.json"))
client = OpenAI(api_key=config_json["OPENAI_KEY"])

global ai_model
ai_model = "gpt-3.5-turbo"

# Create lists to keep track of GUI elements
textboxes = []
output_textboxes = []
labels = []
buttons = [] # Button Index: 0 Reset, 1 Submit, 2 Add Line, 3 Model
speaker_boxes = []


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
    add_speaker_box()

def update_num_textboxes(event):
    current_boxes = len(textboxes)
    num = int(num_textboxes.get())
    # delete excess boxes
    if num < current_boxes:
        for i in range(current_boxes - 1, num - 1, -1):
            textboxes[i].destroy()
            labels[i].destroy()
            speaker_boxes[i].destroy()
    # add more text boxes
    elif num > current_boxes:
        for i in range(current_boxes, num):
            add_textbox()
    else:
        return

def add_speaker_box():
    speaker_options = config_json["speakers"]
    speaker = tk.StringVar()
    speaker.set(speaker_options[0])
    speaker_box = ttk.Combobox(canvas_frame, textvariable=speaker, values=speaker_options)
    speaker_box.grid(row=len(speaker_boxes) + 1, column=2, padx=10, pady=5)
    speaker_boxes.append(speaker_box)

# Translates text blocks and renders output text boxes
def submit():
    base_prompt = read_file('./BASE_PROMPT')
    translation_json = {"blocks": []}
    for index, textbox in enumerate(textboxes):
        translation_json["blocks"].append({"speaker": speaker_boxes[index].get(), "text": textbox.get('1.0', tk.END)})

    response = client.chat.completions.create(
    model=ai_model,
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": json.dumps(translation_json)}
    ]
    )

    # Parse response JSON and render output to adjacent text boxes
    translated_data = json.loads(response.choices[0].message.content)
    for key, value in translated_data.items():
        output_textbox = ttk.Text(canvas_frame, height=3, width=30)
        output_textbox.insert(tk.END, value)
        output_textbox.grid(row=int(key), column=3, padx=5, pady=5)
        output_textboxes.append(output_textbox)
    
# Clears text inputs and deletes output text boxes
def reset():
    for box in textboxes:
        box.delete(1.0, "end")
    for box in output_textboxes:
        box.destroy()
    output_textboxes.clear()

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
root.minsize(720, 480)

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
submit_button.grid(row=0, column=1, padx=5, pady=5)
buttons.append(submit_button)

# Create a label for the initial textbox
initial_label = ttk.Label(canvas_frame, text="Line 1")
initial_label.grid(row=1, column=0, padx=5, pady=5)
labels.append(initial_label)

# Create initial textboxes for user input
initial_textbox = ttk.Text(canvas_frame, height=3, width=30)
initial_textbox.grid(row=1, column=1, padx=5, pady=5)
textboxes.append(initial_textbox)
add_textbox()
add_textbox()

# Create a combobox to set the number of textboxes
options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Change this list as needed for the desired number of textboxes
num_textboxes = tk.StringVar()
num_textboxes.set(options[2])  # Set default value to 3
combo_box = ttk.Combobox(canvas_frame, textvariable=num_textboxes, values=options, bootstyle=SUCCESS)
combo_box.grid(row=0, column=2, padx=10, pady=5)
combo_box.bind("<<ComboboxSelected>>", update_num_textboxes)

# Create a combobox for the current speaker
add_speaker_box()

# Create a button to toggle between GPT 3.5 Turbo and GPT 4 Turbo
model_button = ttk.Button(canvas_frame, text="Switch to GPT 4 Turbo", command=switch_model, bootstyle=SECONDARY)
model_button.grid(row=0, column=3, padx=5, pady=5)
buttons.append(model_button)

# Run the application
root.mainloop()
