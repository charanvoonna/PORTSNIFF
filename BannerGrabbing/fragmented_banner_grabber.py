import socket
from colorama import Fore, Style

def run_fragmented_grabber(ip, ports, log_func=print):
    for port in ports:
        try:
            log_func(f"{Fore.CYAN}[*] Sending fragmented packets to {ip}:{port}{Style.RESET_ALL}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((ip, port))
                # Fake fragmented data simulation
                s.sendall(b'GET ')
                s.sendall(b'/index.html ')
                s.sendall(b'HTTP/1.1\r\nHost: ')
                s.sendall(ip.encode())
                s.sendall(b'\r\n\r\n')
                response = s.recv(4096).decode(errors='ignore')
                log_func(f"{Fore.GREEN}[+] {ip}:{port} - Response:\n{response}{Style.RESET_ALL}")
        except Exception as e:
            log_func(f"{Fore.RED}[-] {ip}:{port} - Error: {e}{Style.RESET_ALL}")
