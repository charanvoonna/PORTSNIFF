import tkinter as tk
from tkinter import ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext
import threading
from .active_fingerprint import run_active_os_detection
from .passive_fingerprint import run_passive_os_detection

class OSDetectionGUI:
    def __init__(self, parent):
        self.root = parent  # Parent is a Frame, not a Tk window

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        self.create_active_tab()
        self.create_passive_tab()

    def create_active_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Active Fingerprinting")

        ttk.Label(tab, text="Target IP").pack(pady=2)
        self.active_ip_entry = ttk.Entry(tab)
        self.active_ip_entry.pack(pady=2)

        self.active_log = scrolledtext.ScrolledText(tab, height=15)
        self.active_log.pack(padx=5, pady=5, fill=BOTH, expand=True)

        ttk.Button(tab, text="Run Active Detection", command=self.run_active_thread).pack(pady=4)

    def create_passive_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Passive Fingerprinting")

        ttk.Label(tab, text="Interface / Packet File").pack(pady=2)
        self.passive_input_entry = ttk.Entry(tab)
        self.passive_input_entry.pack(pady=2)

        self.passive_log = scrolledtext.ScrolledText(tab, height=15)
        self.passive_log.pack(padx=5, pady=5, fill=BOTH, expand=True)

        ttk.Button(tab, text="Run Passive Detection", command=self.run_passive_thread).pack(pady=4)

    def run_active_thread(self):
        ip = self.active_ip_entry.get()
        threading.Thread(target=run_active_os_detection, args=(ip, self.log_active)).start()

    def run_passive_thread(self):
        source = self.passive_input_entry.get()
        threading.Thread(target=run_passive_os_detection, args=(source, self.log_passive)).start()

    def log_active(self, msg):
        self.active_log.insert(tk.END, msg + '\n')
        self.active_log.see(tk.END)

    def log_passive(self, msg):
        self.passive_log.insert(tk.END, msg + '\n')
        self.passive_log.see(tk.END)
