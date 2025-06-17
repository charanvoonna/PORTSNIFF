import tkinter as tk
from ttkbootstrap import Style, Button
from ttkbootstrap.constants import *
from tkinter import messagebox
import subprocess
import os

# Set Dark Theme Style
style = Style("darkly")
root = style.master
root.title("PortSniff - Cybersecurity Recon Tool")
root.geometry("800x550")
root.configure(bg="black")

# Title Label
title_label = tk.Label(
    root,
    text="PortSniff - Cybersecurity Recon Tool Dashboard",
    font=("Helvetica", 22, "bold"),
    fg="white",
    bg="black"
)
title_label.pack(pady=20)
def launch_module(module_name):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Detect current script directory

        paths = {
            "Port Scanning": os.path.join(base_dir, "portscanning", "portscanning_GUI.py"),
            "Banner Grabbing": os.path.join(base_dir, "BannerGrabbing", "Bannergrabber_GUI.py"),
            #"OS & Version Detection": os.path.join(base_dir, "Os&version", "os&vs_GUI.py")
            "OS & Version Detection": os.path.join(base_dir, "OsVersion", "osvs_GUI.py")
        }

        path = paths.get(module_name)
        print(f"[DEBUG] Launching: {path}")  # Log actual path

        if not os.path.isfile(path):
            messagebox.showerror("Error", f"{module_name} file not found at:\n{path}")
            return

        subprocess.Popen(["python", path], shell=True)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch {module_name}:\n{str(e)}")

# Section Heading
section_label = tk.Label(
    root,
    text="Select a Module to Launch",
    font=("Helvetica", 16, "bold"),
    fg="#00ff00",
    bg="black"
)
section_label.pack(pady=10)

# Buttons Frame
button_frame = tk.Frame(root, bg="black")
button_frame.pack(pady=10)

# Module Buttons
modules = [
    ("Port Scanning", "info"),
    ("Banner Grabbing", "info"),
    ("OS & Version Detection", "info")
]

for mod, style_name in modules:
    btn = Button(
        button_frame,
        text=mod,
        bootstyle=style_name,
        width=30,
        command=lambda m=mod: launch_module(m)
    )
    btn.pack(pady=10)

# Exit Button
exit_btn = Button(
    root,
    text="Exit Tool",
    bootstyle="danger",
    width=20,
    command=root.quit
)
exit_btn.pack(pady=30)

# Footer
footer = tk.Label(
    root,
    text="© 2025 PortSniff Tool | Developed by Charan",
    font=("Helvetica", 10),
    fg="gray",
    bg="black"
)
footer.pack(side="bottom", pady=10)

# Run the App
if __name__ == "__main__":
    root.mainloop()
