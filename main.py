import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def add_textbox():
    new_row_idx = len(textboxes) + 1
    label = ttk.Label(canvas_frame, text=f"Line {new_row_idx}")
    label.grid(row=new_row_idx, column=0, padx=5, pady=5)
    textbox = tk.Text(canvas_frame, height=5, width=30)
    textbox.grid(row=new_row_idx, column=1, padx=5, pady=5)
    textboxes.append(textbox)

def submit():
    for index, textbox in enumerate(textboxes):
        print(f"Textbox {index + 1}: {textbox.get('1.0', tk.END).strip()}")

# Create the main window
root = ttk.Window()
root.title("Open AI Block Translator")
root.minsize(480, 360)

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

# Create a list to keep track of the textboxes
textboxes = []

# Create a button to submit the input
submit_button = ttk.Button(canvas_frame, text="Submit", command=submit, bootstyle=PRIMARY)
submit_button.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# Create a label for the initial textbox
initial_label = ttk.Label(canvas_frame, text="Line 1")
initial_label.grid(row=1, column=0, padx=5, pady=5)

# Create a textbox for user input
initial_textbox = ttk.Text(canvas_frame, height=5, width=30)
initial_textbox.grid(row=1, column=1, padx=5, pady=5)
textboxes.append(initial_textbox)

# Create a button to add more textboxes
add_button = ttk.Button(canvas_frame, text="Add Line", command=add_textbox, bootstyle=SUCCESS)
add_button.grid(row=0, column=2, padx=5, pady=5)

# Run the application
root.mainloop()
