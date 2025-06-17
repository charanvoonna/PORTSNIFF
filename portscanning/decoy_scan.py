import argparse
import socket
import threading
from colorama import Fore, Style
from random import randint
import time

class DecoyScanner:
    def __init__(self, target, ports, decoys=5, timeout=1, log_func=print):
        self.target = target
        self.ports = ports
        self.decoys = decoys
        self.timeout = timeout
        self.lock = threading.Semaphore(10)
        self.open_ports = []
        self.log = log_func

    def scan_port(self, port):
        with self.lock:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    self.log(f"{Fore.GREEN}[+] Port {port} is OPEN{Style.RESET_ALL}")
                    self.open_ports.append(port)
                else:
                    self.log(f"{Fore.RED}[-] Port {port} is CLOSED{Style.RESET_ALL}")
                sock.close()
            except Exception as e:
                self.log(f"{Fore.YELLOW}[!] Error on port {port}: {e}{Style.RESET_ALL}")

    def spoof_ip(self):
        return ".".join(str(randint(1, 254)) for _ in range(4))

    def start_scan(self):
        self.log(Fore.CYAN + f"\n[⚙] Starting Decoy Scan on {self.target} with {self.decoys} decoys" + Style.RESET_ALL)
        self.log(Fore.MAGENTA + f"[📡] Target Ports: {', '.join(map(str, self.ports))}" + Style.RESET_ALL)
        self.log(Fore.BLUE + "─" * 50 + Style.RESET_ALL)

        start_time = time.time()
        threads = []

        for port in self.ports:
            for _ in range(self.decoys):
                fake_ip = self.spoof_ip()
                self.log(f"{Fore.YELLOW}[*] Sending decoy packet from {fake_ip} to port {port}{Style.RESET_ALL}")
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        elapsed = round(time.time() - start_time, 2)
        self.log(Fore.BLUE + "─" * 50 + Style.RESET_ALL)
        if self.open_ports:
            self.log(Fore.GREEN + f"[✅] Open Ports: {', '.join(map(str, self.open_ports))}" + Style.RESET_ALL)
        else:
            self.log(Fore.MAGENTA + "[!] No open ports found" + Style.RESET_ALL)
        self.log(Fore.CYAN + f"[⏱️] Scan completed in {elapsed} seconds" + Style.RESET_ALL)


def run_decoy_scan(target, ports_str, decoys=5, timeout=1, log_func=print):
    ports = parse_ports(ports_str)
    scanner = DecoyScanner(target, ports, decoys, timeout, log_func=log_func)
    scanner.start_scan()

def parse_ports(port_str):
    ports = set()
    for part in port_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part.strip()))
    return sorted(ports)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Decoy Port Scanner")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("-p", "--ports", nargs="+", type=int, required=True, help="Ports to scan")
    parser.add_argument("-d", "--decoys", type=int, default=5, help="Number of decoy IPs")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout for each connection")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    run_decoy_scan(args.target, ",".join(map(str, args.ports)), args.decoys, args.timeout)
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Decoy Port Scanner")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("-p", "--ports", nargs="+", type=int, required=True, help="Ports to scan")
    parser.add_argument("-d", "--decoys", type=int, default=5, help="Number of decoy IPs")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout for each connection")
    return parser.parse_args()
