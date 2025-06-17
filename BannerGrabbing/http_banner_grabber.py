import socket
from colorama import Fore, Style

def run_http_banner_grabber(ip, ports, log_func=print):
    for port in ports:
        try:
            with socket.create_connection((ip, port), timeout=3) as sock:
                http_req = f"HEAD / HTTP/1.0\r\nHost: {ip}\r\n\r\n"
                sock.sendall(http_req.encode())
                response = sock.recv(4096).decode(errors="ignore")

                log_func(f"{Fore.GREEN}[+] {ip}:{port} - HTTP Banner:\n{response}{Style.RESET_ALL}")
        except Exception as e:
            log_func(f"{Fore.RED}[-] {ip}:{port} - Error: {e}{Style.RESET_ALL}")
