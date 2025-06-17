import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import argparse

init(autoreset=True)

class TCPConnectScanner:
    def __init__(self, target, ports):
        self.target = target
        self.ports = ports

    def scan_port(self, port, log_func=print):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((self.target, port))
            if result == 0:
                log_func(f"{Fore.GREEN}[+] Port {port} is open")
            else:
                log_func(f"{Fore.RED}[-] Port {port} is closed")
            s.close()
        except Exception as e:
            log_func(f"{Fore.YELLOW}[!] Error scanning port {port}: {e}")

    def run(self, max_threads=10, log_func=print):
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for port in self.ports:
                executor.submit(self.scan_port, port, log_func)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Connect Port Scanner")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("start_port", type=int, help="Start port number")
    parser.add_argument("end_port", type=int, help="End port number")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads (default: 10)")
    args = parser.parse_args()

    port_range = range(args.start_port, args.end_port + 1)
    scanner = TCPConnectScanner(args.target, port_range)
    scanner.run(max_threads=args.threads)
