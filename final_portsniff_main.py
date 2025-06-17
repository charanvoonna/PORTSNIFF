
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *

# Import GUI modules from your subdirectories
from portscanning.portscanning_GUI import PortScanningGUI
from BannerGrabbing.Bannergrabber_GUI import BannerSniffGUI
from Osversion.osvs_GUI import OSDetectionGUI


class PortSniffMainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PortSniff - Unified Cybersecurity Recon Tool")

        # Use darkly theme
        self.style = Style("darkly")
        self.style.configure("TFrame", background="#2b2b2b")

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        # Add tabs
        self.create_home_tab()
        self.add_port_scanning_tab()
        self.add_banner_grabbing_tab()
        self.add_os_detection_tab()

    def create_home_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Home")

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)

        frame = ttk.Frame(tab, style="TFrame")
        frame.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        # ASCII Art Banner
        ascii_label = tk.Label(
            frame,
            text="""
 ______           _     _  __ _       
|  ____|         (_)   (_)/ _| |      
| |__ _ __  _   _ _  __ _| |_| |_ ___ 
|  __| '_ \| | | | |/ _` |  _| __/ _ \\
| |  | | | | |_| | | (_| | | | ||  __/
|_|  |_| |_|\__,_|_|\__,_|_|  \__\___|
""",
            font=("Courier", 12),
            fg="#00ffff",
            bg="#2b2b2b",
            justify="center"
        )
        ascii_label.pack(pady=10)

        # Title
        title_label = tk.Label(
            frame,
            text="Welcome to PortSniff",
            font=("Helvetica", 28, "bold"),
            fg="white",
            bg="#2b2b2b"
        )
        title_label.pack(pady=5)

        # Subtitle
        subtitle = tk.Label(
            frame,
            text="Your Cybersecurity Reconnaissance Toolkit",
            font=("Helvetica", 16, "italic"),
            fg="#ff80ff",
            bg="#2b2b2b"
        )
        subtitle.pack(pady=5)

        # Divider Line
        divider = tk.Label(
            frame,
            text="―" * 80,
            fg="#666666",
            bg="#2b2b2b"
        )
        divider.pack(pady=10)

        # Capabilities Section
        capabilities = tk.Label(
            frame,
            text="""
⚡ Port Scanning – Fast, Stealth, and Decoy scans
🛰️ Banner Grabbing – Discover hidden services
🧠 OS & Version Detection – Actively fingerprint targets
""",
            font=("Consolas", 13),
            fg="#00ffcc",
            bg="#2b2b2b",
            justify="left"
        )
        capabilities.pack(pady=10)

        # Footer
        footer = tk.Label(
            frame,
            text="© 2025 PortSniff | Developed by Charan",
            font=("Helvetica", 10),
            fg="#888888",
            bg="#2b2b2b"
        )
        footer.pack(side="bottom", pady=20)

    def add_port_scanning_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Port Scanning")
        PortScanningGUI(tab)

    def add_banner_grabbing_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Banner Grabbing")
        BannerSniffGUI(tab)

    def add_os_detection_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="OS & Version Detection")
        OSDetectionGUI(tab)


if __name__ == "__main__":
    root = tk.Tk()
    app = PortSniffMainApp(root)
    root.mainloop()
