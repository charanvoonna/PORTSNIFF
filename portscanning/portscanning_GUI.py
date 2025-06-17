import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
from portscanning.portmain import run_tcp_scan, run_syn_scan, run_slow_scan, run_decoy_scan

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ttkbootstrap import Style
from threading import Thread
import queue

class PortScanningGUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='both', expand=True)

        self.style = Style("darkly")
        self.log_queue = queue.Queue()

        self.selected_technique = tk.StringVar()
        self.banner_displayed = False

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Select Port Scanning Technique", font=("Helvetica", 16, "bold"), foreground="white").pack(pady=10)

        techniques = ["tcp", "syn", "slow", "decoy"]
        for tech in techniques:
            ttk.Radiobutton(self, text=tech.upper(), variable=self.selected_technique, value=tech, command=self.show_inputs).pack(anchor='w', padx=30)

        self.inputs_frame = ttk.Frame(self)
        self.inputs_frame.pack(pady=10, fill='x', padx=30)

        self.run_button = ttk.Button(self, text="Start Scan", command=self.start_scan)
        self.run_button.pack(pady=10)

        self.log_box = scrolledtext.ScrolledText(self, height=20, bg="black", fg="green", insertbackground='white')
        self.log_box.pack(fill='both', expand=True, padx=20, pady=10)
        self.log_box.config(state='disabled')

    def show_inputs(self):
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()

        self.entries = {}
        common_fields = ["Target IP", "Ports"]
        extra_fields = {
            "tcp": ["Threads"],
            "syn": [],
            "slow": ["Threads", "Delay"],
            "decoy": ["Decoys", "Timeout"]
        }

        fields = common_fields + extra_fields.get(self.selected_technique.get(), [])

        for field in fields:
            label = ttk.Label(self.inputs_frame, text=field)
            entry = ttk.Entry(self.inputs_frame)
            label.pack(anchor='w')
            entry.pack(fill='x', pady=2)
            self.entries[field.lower().replace(" ", "_")] = entry

    def log(self, msg):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        full_msg = f"{timestamp} {msg}"

        if any(keyword in msg.lower() for keyword in ["open"]):
            color = "lime"
        elif any(keyword in msg.lower() for keyword in ["closed"]):
            color = "red"
        elif any(keyword in msg.lower() for keyword in ["filtered"]):
            color = "yellow"
        elif "error" in msg.lower() or "exception" in msg.lower() or "[!]" in msg:
            color = "magenta"
        elif "scan complete" in msg.lower() or "summary" in msg.lower() or "[\u2714]" in msg:
            color = "cyan"
        else:
            color = "green"

        self.log_queue.put((full_msg, color))

    def update_log(self):
        while not self.log_queue.empty():
            msg, color = self.log_queue.get_nowait()
            self.log_box.config(state='normal')
            self.log_box.insert(tk.END, msg + '\n', color)
            self.log_box.tag_config(color, foreground=color)
            self.log_box.see(tk.END)
            self.log_box.config(state='disabled')
        self.after(100, self.update_log)

    def display_banner(self):
        if not self.banner_displayed:
            banner = """
 ____   ___   ____ _____ ____  ____  _____ ______
|  _ \ / _ \ / ___| ____|  _ \|  _ \| ____|  _ \ \ 
| |_) | | | | |  _|  _| | |_) | | | |  _| | | | |\ \ 
|  __/| |_| | |_| | |___|  _ <| |_| | |___| |_| | > >
|_|    \___/ \____|_____|_| \_\____/|_____|____/ /_/
            """
            self.log(banner)
            self.banner_displayed = True

    def start_scan(self):
        method = self.selected_technique.get()
        if not method:
            messagebox.showerror("Error", "Please select a scanning technique.")
            return

        params = {k: v.get() for k, v in self.entries.items()}

        def thread_func():
            self.display_banner()

            target = params.get("target_ip")
            ports = params.get("ports")
            self.log(f"[\u2022] Selected Technique: {method.upper()}")
            self.log(f"[\u2022] Target: {target}")
            self.log(f"[\u2022] Ports: {ports}")

            start_time = time.time()
            self.log("[\u2713] Starting scan...")

            try:
                if method == "tcp":
                    threads = int(params.get("threads", 10))
                    run_tcp_scan(target, ports, threads, log_func=self.log)
                elif method == "syn":
                    run_syn_scan(target, ports, log_func=self.log)
                elif method == "slow":
                    delay = int(params.get("delay", 0))
                    threads = int(params.get("threads", 10))
                    run_slow_scan(target, ports, delay, threads, log_func=self.log)
                elif method == "decoy":
                    decoys = int(params.get("decoys", 5))
                    timeout = int(params.get("timeout", 1))
                    run_decoy_scan(target, ports, decoys, timeout, log_func=self.log)
            except Exception as e:
                self.log(f"[!] Error: {str(e)}")

            end_time = time.time()
            duration = round(end_time - start_time, 2)
            self.log(f"[\u2714] Scan Complete in {duration} seconds")

        Thread(target=thread_func, daemon=True).start()
        self.update_log()