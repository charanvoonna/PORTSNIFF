import socket
import socks
from colorama import Fore, Style

def run_proxy_banner_grabber(ip, ports, log_func=print):
    for port in ports:
        try:
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, ip, port)
            s.settimeout(3)
            s.connect(("example.com", 80))
            s.sendall(b"GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")
            banner = s.recv(1024).decode(errors="ignore")
            log_func(f"{Fore.GREEN}[+] {ip}:{port} - Proxy Banner:\n{banner}{Style.RESET_ALL}")
            s.close()
        except Exception as e:
            log_func(f"{Fore.RED}[-] {ip}:{port} - Error: {e}{Style.RESET_ALL}")
