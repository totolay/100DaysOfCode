import tkinter as tk
from tkinter import filedialog, ttk
import os
import shutil
import sys
from pathlib import Path
import subprocess
import json
import os
import subprocess
import sys
from tkinter import messagebox

CONFIG_FILE = "gui_config.json"

def load_config():
    """Load settings from file if available"""
    if os.path.exists(CONFIG_FILE):
        with open(os.path.join(os.getcwd(), CONFIG_FILE), "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_config():
    """Save settings to JSON file"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(button_actions, f, indent=4, ensure_ascii=False)
    status_label.config(text="✅ Settings saved!", fg="green")

def add_button_action():
    """Add a new item to the list"""
    name = name_entry.get()
    image = image_path_var.get()
    action = action_var.get()
    text = text_entry.get() if action == "Type Text" else ""
    wait_time = wait_time_entry.get() if action == "Wait" else ""
    executable_path = executable_path_var.get()

    if not name or not action:
        status_label.config(text="⚠️ Please enter all fields and select an action!", fg="red")
        return

    if action == "Up":
        move_up()
    elif action == "Down":
        move_down()
    elif action == "Left":
        move_left()
    elif action == "Right":
        move_right()
    elif action == "Execute":
        pass

    button_actions.append({"name": name, "image": image, "actions": [action.lower().replace(" ", "_")], "text": text, "wait_time": wait_time, "executable_path": executable_path})
    update_table()
    save_config()
    status_label.config(text="✅ Action added!", fg="green")

def delete_selected():
    """Delete selected item from the table"""
    selected_items = table.selection()
    if selected_items:
        # Get indices of selected items at the beginning
        indices_to_delete = [table.index(item) for item in selected_items]

        # Sort indices in reverse order to avoid index issues during deletion
        indices_to_delete.sort(reverse=True)

        for index in indices_to_delete:
            del button_actions[index]

        update_table()
        save_config()

def move_up():
    """Move selected item up"""
    selected_item = table.selection()
    if selected_item:
        index = table.index(selected_item)
        if index > 0:
            button_actions[index], button_actions[index - 1] = button_actions[index - 1], button_actions[index]
            update_table()
            table.selection_set(table.get_children()[index - 1])
            save_config()

def move_down():
    """Move selected item down"""
    selected_item = table.selection()
    if selected_item:
        index = table.index(selected_item)
        if index < len(button_actions) - 1:
            button_actions[index], button_actions[index + 1] = button_actions[index + 1], button_actions[index]
            update_table()
            table.selection_set(table.get_children()[index + 1])
            save_config()

def move_left():
    """Move selected item left"""
    selected_item = table.selection()
    if selected_item:
        index = table.index(selected_item)
        button_actions[index]["actions"].append("left")
        update_table()
        save_config()

def move_right():
    """Move selected item right"""
    selected_item = table.selection()
    if selected_item:
        index = table.index(selected_item)
        button_actions[index]["actions"].append("right")
        update_table()
        save_config()

def update_table():
    """Update the table after adding, deleting, or reordering items"""
    for row in table.get_children():
        table.delete(row)
    for item in button_actions:
        actions_list = item.get("actions", [])
        table.insert("", "end", values=(item.get("name", "Unknown"), item.get("image", "No Image"), ", ".join(actions_list), item.get("text", ""), item.get("wait_time", ""), item.get("executable_path", "")))

def browse_image():
    """Select an image from the device"""
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path_var.set(file_path)

def browse_executable():
    """Select an executable from the device"""
    file_path = filedialog.askopenfilename(filetypes=[("Executables", "*.exe;*.bat;*.cmd")])
    if file_path:
        executable_path_var.set(file_path)

import json

def load_config_from_file():
    """Load settings from JSON file"""
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                global button_actions
                button_actions = json.load(f)
                update_table()
                save_config()
                status_label.config(text="✅ Settings loaded!", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {e}")
            status_label.config(text="⚠️ Failed to load settings!", fg="red")

def save_config_to_file():
    """Save settings to JSON file using a file dialog"""
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(button_actions, f, indent=4, ensure_ascii=False)
            status_label.config(text="✅ Settings saved!", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            status_label.config(text="⚠️ Failed to save settings!", fg="red")

def start_execution():
    """Start executing all actions"""
    status_label.config(text="🚀 Executing actions...", fg="blue")
    # Convert button_actions to JSON string
    actions_json = json.dumps(button_actions, ensure_ascii=False)
    # Pass JSON string as command-line argument
    subprocess.Popen(["python", "automation_script.py", actions_json], shell=True)
    status_label.config(text="✅ Execution started!", fg="green")

# Load existing settings
button_actions = load_config()

# Create main window
root = tk.Tk()
root.title("Alsafa-Foods Automation")
root.geometry("750x650")

# Frames for grouping input fields
element_frame = ttk.LabelFrame(root, text="Element Details")
element_frame.pack(pady=10, padx=10, fill=tk.X)

executable_frame = ttk.LabelFrame(root, text="Executable Details")
executable_frame.pack(pady=10, padx=10, fill=tk.X)

action_frame = ttk.LabelFrame(root, text="Action Details")
action_frame.pack(pady=10, padx=10, fill=tk.X)

# Element Input fields
name_label = tk.Label(element_frame, text="Element Name:")
name_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
name_entry = tk.Entry(element_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

image_label = tk.Label(element_frame, text="Element Image:")
image_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
image_path_var = tk.StringVar()
image_entry = tk.Entry(element_frame, textvariable=image_path_var, state="readonly")
image_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
browse_button = tk.Button(element_frame, text="📂 Select Image", command=browse_image)
browse_button.grid(row=1, column=2, padx=5, pady=5)
element_frame.columnconfigure(1, weight=1) # Make column 1 expandable

# Executable Input fields
executable_label = tk.Label(executable_frame, text="Executable Path:")
executable_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
executable_path_var = tk.StringVar()
executable_entry = tk.Entry(executable_frame, textvariable=executable_path_var, state="readonly")
executable_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
executable_browse_button = tk.Button(executable_frame, text="📂 Select Executable", command=browse_executable)
executable_browse_button.grid(row=0, column=2, padx=5, pady=5)
executable_frame.columnconfigure(1, weight=1) # Make column 1 expandable

def browse_executable():
    """Select an executable from the device"""
    file_path = filedialog.askopenfilename(filetypes=[("Executables", "*.exe;*.bat;*.cmd")])
    if file_path:
        executable_path_var.set(file_path)

# Action Input fields
action_label = tk.Label(action_frame, text="Action Type:", anchor="e")
action_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)

action_options = ["Click", "Type Text", "Hover", "Wait", "Up", "Down", "Left", "Right", "Esc", "Enter", "Execute"]
action_var = tk.StringVar(value=action_options[0])
action_combo = ttk.Combobox(action_frame, textvariable=action_var, values=action_options, state="readonly")
action_combo.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky="ew")

text_label = tk.Label(action_frame, text="Text Input:", anchor="e")
text_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
text_entry = tk.Entry(action_frame)
text_entry.grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky="ew")

wait_time_label = tk.Label(action_frame, text="Wait Time (seconds):", anchor="e") # Align text to the right
wait_time_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
wait_time_entry = tk.Entry(action_frame)
wait_time_entry.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky="ew")

action_frame.columnconfigure(1, weight=1)
action_frame.columnconfigure(2, weight=1)
action_frame.columnconfigure(3, weight=1)
action_frame.columnconfigure(4, weight=1)


# Table to display actions
table_frame = ttk.LabelFrame(root, text="Action List")
table_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

columns = ('name', 'image', 'actions', 'text', 'wait_time', 'executable_path')
table = ttk.Treeview(table_frame, columns=columns, show='headings')

table.heading('name', text='Element Name')
table.heading('image', text='Image Path')
table.heading('actions', text='Actions')
table.heading('text', text='Text Input')
table.heading('wait_time', text='Wait Time')
table.heading('executable_path', text='Executable Path')


for col in columns:
    table.column(col, anchor=tk.W)

table.pack(fill=tk.BOTH, expand=True)

update_table() # Populate table on startup

# Buttons Frame
buttons_frame = ttk.Frame(root)
buttons_frame.pack(pady=10, padx=10, fill=tk.X)

add_button = tk.Button(buttons_frame, text="Add Action", command=add_button_action)
add_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(buttons_frame, text="Delete Action", command=delete_selected)
delete_button.pack(side=tk.LEFT, padx=5)

move_up_button = tk.Button(buttons_frame, text="Move Up", command=move_up)
move_up_button.pack(side=tk.LEFT, padx=5)

move_down_button = tk.Button(buttons_frame, text="Move Down", command=move_down)
move_down_button.pack(side=tk.LEFT, padx=5)

def edit_selected_action():
    selected_item = table.selection()
    if selected_item:
        index = table.index(selected_item)
        item_values = table.item(selected_item, 'values')
        if item_values:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, item_values[0])
            image_path_var.set(item_values[1])
            actions_str = item_values[2]
            actions_list = [action.strip() for action in actions_str.split(',')] if actions_str else []
            if actions_list:
                action_var.set(actions_list[0].replace("_", " ").title())
            text_entry.delete(0, tk.END)
            text_entry.insert(0, item_values[3])
            wait_time_entry.delete(0, tk.END)
            wait_time_entry.insert(0, item_values[4])
            status_label.config(text=f"✅ Editing action: {item_values[0]}", fg="green")
        else:
            status_label.config(text="⚠️ No action details found to edit.", fg="red")
    else:
        status_label.config(text="⚠️ Please select an action to edit.", fg="red")


edit_button = tk.Button(buttons_frame, text="Edit Action", command=edit_selected_action)
edit_button.pack(side=tk.LEFT, padx=5)

load_button = tk.Button(buttons_frame, text="Load Config", command=load_config_from_file)
load_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(buttons_frame, text="Save Config", command=save_config_to_file)
save_button.pack(side=tk.LEFT, padx=5)

import os
import shutil

def convert_to_exe():
    """Convert automation_script.py to exe using PyInstaller"""
    status_label.config(text="⚙️ Converting to exe...", fg="blue")
    try:
        # Use the full path to pyinstaller.exe
        pyinstaller_path = r"C:\Users\MH\AppData\Roaming\Python\Python313\Scripts\pyinstaller.exe"
        #subprocess.check_call([pyinstaller_path, "automation_script.spec"], shell=False)
        subprocess.check_call([pyinstaller_path, "automation_script.spec"], shell=False)

        status_label.config(text="✅ Conversion complete!", fg="green")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")
        status_label.config(text="⚠️ Conversion failed!", fg="red")
        
def start_execution():
    """Start executing all actions"""
    status_label.config(text="🚀 Executing actions...", fg="blue")
    # Convert button_actions to JSON string
    actions_json = json.dumps(button_actions, ensure_ascii=False)
    # Pass JSON string as command-line argument
    try:
        subprocess.Popen([os.path.join(os.getcwd(), "dist", "automation_script", "automation_script.exe"), actions_json], shell=False)
        status_label.config(text="✅ Execution started!", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Execution failed: {e}")
        status_label.config(text="⚠️ Execution failed!", fg="red")

execute_button = tk.Button(buttons_frame, text="Execute Automation", command=start_execution)
execute_button.pack(side=tk.RIGHT, padx=5)

convert_exe_button = tk.Button(buttons_frame, text="Convert to EXE", command=convert_to_exe)
convert_exe_button.pack(side=tk.LEFT, padx=5)

# Status Label
status_label = tk.Label(root, text="", fg="black")
status_label.pack(pady=5)

root.bind("<Up>", lambda event: move_up())
root.bind("<Down>", lambda event: move_down())
root.bind("<Left>", lambda event: move_left())
root.bind("<Right>", lambda event: move_right())

root.mainloop()
