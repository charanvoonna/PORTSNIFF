import tkinter as tk
from tkinter import ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext
import threading
from .tcp_banner_grabber import run_tcp_grabber
from .http_banner_grabber import run_http_banner_grabber
from .fragmented_banner_grabber import run_fragmented_grabber
from .proxy_banner_grabber import run_proxy_banner_grabber

class BannerSniffGUI:
    def __init__(self, parent):
        self.root = parent  # It's a frame, NOT a Tk window

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        self.create_tcp_tab()
        self.create_http_tab()
        self.create_proxy_tab()
        self.create_fragmented_tab()

    def create_tcp_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="TCP Banner Grabber")

        ttk.Label(tab, text="Target IP(s)").pack(pady=2)
        self.tcp_targets_entry = ttk.Entry(tab)
        self.tcp_targets_entry.pack(pady=2)

        ttk.Label(tab, text="Ports (comma-separated)").pack(pady=2)
        self.tcp_ports_entry = ttk.Entry(tab)
        self.tcp_ports_entry.pack(pady=2)

        self.tcp_log = scrolledtext.ScrolledText(tab, height=15)
        self.tcp_log.pack(padx=5, pady=5, fill=BOTH, expand=True)

        ttk.Button(tab, text="Run TCP Grab", command=self.run_tcp_grab_thread).pack(pady=4)

    def create_http_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="HTTP Header Grabber")

        ttk.Label(tab, text="Target IP(s)").pack(pady=2)
        self.http_targets_entry = ttk.Entry(tab)
        self.http_targets_entry.pack(pady=2)

        ttk.Label(tab, text="Ports (comma-separated)").pack(pady=2)
        self.http_ports_entry = ttk.Entry(tab)
        self.http_ports_entry.pack(pady=2)

        self.http_log = scrolledtext.ScrolledText(tab, height=15)
        self.http_log.pack(padx=5, pady=5, fill=BOTH, expand=True)

        ttk.Button(tab, text="Run HTTP Grab", command=self.run_http_grab_thread).pack(pady=4)

    def create_proxy_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Proxy Banner Grabber")

        ttk.Label(tab, text="Proxy IP").pack(pady=2)
        self.proxy_ip_entry = ttk.Entry(tab)
        self.proxy_ip_entry.pack(pady=2)

        ttk.Label(tab, text="Ports (comma-separated)").pack(pady=2)
        self.proxy_ports_entry = ttk.Entry(tab)
        self.proxy_ports_entry.pack(pady=2)

        self.proxy_log = scrolledtext.ScrolledText(tab, height=15)
        self.proxy_log.pack(padx=5, pady=5, fill=BOTH, expand=True)

        ttk.Button(tab, text="Run Proxy Grab", command=self.run_proxy_grab_thread).pack(pady=4)

    def create_fragmented_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Fragmented Packet Grabber")

        ttk.Label(tab, text="Target IP(s)").pack(pady=2)
        self.frag_targets_entry = ttk.Entry(tab)
        self.frag_targets_entry.pack(pady=2)

        ttk.Label(tab, text="Ports (comma-separated)").pack(pady=2)
        self.frag_ports_entry = ttk.Entry(tab)
        self.frag_ports_entry.pack(pady=2)

        self.frag_log = scrolledtext.ScrolledText(tab, height=15)
        self.frag_log.pack(padx=5, pady=5, fill=BOTH, expand=True)

        ttk.Button(tab, text="Run Fragmented Grab", command=self.run_fragmented_grab_thread).pack(pady=4)

    # ---------------- Threaded Functions ---------------- #
    def run_tcp_grab_thread(self):
        targets = self.tcp_targets_entry.get().split(',')
        ports = [int(p.strip()) for p in self.tcp_ports_entry.get().split(',')]
        threading.Thread(target=run_tcp_grabber, args=(targets[0], ports, self.log_tcp)).start()

    def run_http_grab_thread(self):
        targets = self.http_targets_entry.get().split(',')
        ports = [int(p.strip()) for p in self.http_ports_entry.get().split(',')]
        threading.Thread(target=self.run_http_multiple_targets, args=(targets, ports)).start()

    def run_http_multiple_targets(self, targets, ports):
        for ip in targets:
            run_http_banner_grabber(ip, ports, self.log_http)

    def run_proxy_grab_thread(self):
        ip = self.proxy_ip_entry.get()
        ports = [int(p.strip()) for p in self.proxy_ports_entry.get().split(',')]
        threading.Thread(target=run_proxy_banner_grabber, args=(ip, ports, self.log_proxy)).start()

    def run_fragmented_grab_thread(self):
        targets = self.frag_targets_entry.get().split(',')
        ports = [int(p.strip()) for p in self.frag_ports_entry.get().split(',')]
        threading.Thread(target=self.run_fragmented_multiple, args=(targets, ports)).start()

    def run_fragmented_multiple(self, targets, ports):
        for ip in targets:
            run_fragmented_grabber(ip, ports, self.log_frag)

    # ---------------- Logging ---------------- #
    def log_tcp(self, msg):
        self.tcp_log.insert(tk.END, msg + '\n')
        self.tcp_log.see(tk.END)

    def log_http(self, msg):
        self.http_log.insert(tk.END, msg + '\n')
        self.http_log.see(tk.END)

    def log_proxy(self, msg):
        self.proxy_log.insert(tk.END, msg + '\n')
        self.proxy_log.see(tk.END)

    def log_frag(self, msg):
        self.frag_log.insert(tk.END, msg + '\n')
        self.frag_log.see(tk.END)
