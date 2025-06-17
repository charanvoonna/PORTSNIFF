import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style

def grab_banner(ip, port, log_func=print):
    try:
        with socket.create_connection((ip, port), timeout=3) as s:
            banner = s.recv(1024).decode(errors="ignore")
            if banner:
                log_func(f"{Fore.GREEN}[+] {ip}:{port} - Banner: {banner.strip()}{Style.RESET_ALL}")
            else:
                log_func(f"{Fore.YELLOW}[!] {ip}:{port} - No banner received{Style.RESET_ALL}")
    except Exception as e:
        log_func(f"{Fore.RED}[-] {ip}:{port} - Error: {e}{Style.RESET_ALL}")

def run_tcp_grabber(ip, ports, log_func=print):
    with ThreadPoolExecutor(max_workers=10) as executor:
        for port in ports:
            executor.submit(grab_banner, ip, port, log_func)
