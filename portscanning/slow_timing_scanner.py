import socket
import argparse
import time
from queue import Queue
from threading import Thread
from colorama import init, Fore

init(autoreset=True)

class PortScanner:
    def __init__(self, target, ports, delay, log_func=print):
        self.target = target
        self.ports = ports
        self.delay = delay
        self.queue = Queue()
        self.open_ports_found = False
        self.log = log_func

    def scan_port(self):
        while not self.queue.empty():
            port = self.queue.get()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    self.log(Fore.GREEN + f"[+] Port {port} is OPEN")
                    self.open_ports_found = True
                else:
                    self.log(Fore.RED + f"[-] Port {port} is CLOSED")
                s.close()
            except Exception as e:
                self.log(Fore.YELLOW + f"[!] Error scanning port {port}: {e}")
            time.sleep(self.delay)
            self.queue.task_done()

    def start_scan(self, max_threads=10):
        start_time = time.time()
        self.log(Fore.CYAN + f"\n[⚙] Starting Slow Timing Scan on {self.target}")
        self.log(Fore.CYAN + f"[🔢] Ports: {', '.join(map(str, self.ports))}")
        self.log(Fore.MAGENTA + f"[🐢] Delay: {self.delay}s | Threads: {max_threads}")
        self.log(Fore.BLUE + "─" * 50)

        for port in self.ports:
            self.queue.put(port)

        for _ in range(min(max_threads, len(self.ports))):
            t = Thread(target=self.scan_port)
            t.daemon = True
            t.start()

        self.queue.join()

        elapsed = round(time.time() - start_time, 2)
        self.log(Fore.BLUE + "─" * 50)
        self.log(Fore.GREEN + f"[✅] Slow Scan Completed in {elapsed} seconds")

def run_slow_scan(target, ports_str, delay=0, threads=10, log_func=print):
    ports = parse_ports(ports_str)
    scanner = PortScanner(target, ports, delay, log_func=log_func)
    scanner.start_scan(max_threads=threads)


def parse_ports(port_str):
    ports = set()
    parts = port_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part.strip()))
    return sorted(ports)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slow Timing Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", required=True, help="Ports to scan (e.g. 20-25,80,443)")
    parser.add_argument("--delay", type=int, default=0, help="Delay between scans in seconds")
    parser.add_argument("--threads", type=int, default=10, help="Maximum number of threads (default: 10)")

    args = parser.parse_args()
    run_slow_scan(args.target, args.ports, args.delay, args.threads)
