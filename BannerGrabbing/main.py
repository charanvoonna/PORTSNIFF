import argparse
from colorama import init, Fore, Style
import sys

from .tcp_banner_grabber_multiport import BannerGrabber
from .proxy_banner_grabber import ProxyBannerGrabber
from .fragmented_banner_grabber import FragmentedBannerGrabber
from .http_banner_grabber import HTTPBannerGrabber

init(autoreset=True)

def run_tcp_banner_grab(targets, ports, timeout=3, max_threads=10, log_func=print):
    grabber = BannerGrabber(targets, ports, timeout, max_threads, log_func=log_func)
    grabber.run()

def run_proxy_banner_grab(target, port, proxy_ip, proxy_port, proxy_type, log_func=print):
    grabber = ProxyBannerGrabber(target, port, proxy_ip, proxy_port, proxy_type, log_func=log_func)
    grabber.grab_banner()

def run_fragmented_banner_grab(target, port, log_func=print):
    grabber = FragmentedBannerGrabber(target, port, log_func=log_func)
    grabber.send_fragments()

def run_http_banner_grab(targets, port=80, threads=5, log_func=print):
    grabber = HTTPBannerGrabber(targets, port, threads, log_func=log_func)
    grabber.run()


def main(log_func=print):
    parser = argparse.ArgumentParser(description="TraceNet Banner Grabbing Tool - Main Launcher")
    subparsers = parser.add_subparsers(dest='technique', help='Choose a banner grabbing technique')

    # TCP
    parser_tcp = subparsers.add_parser('tcp', help='Simple TCP Banner Grabber')
    parser_tcp.add_argument('targets', nargs='+', help='Target IP(s) or hostname(s)')
    parser_tcp.add_argument('-p', '--ports', type=int, nargs='+', required=True, help='Port(s) to scan')
    parser_tcp.add_argument('-t', '--timeout', type=int, default=3, help='Timeout in seconds')
    parser_tcp.add_argument('-mt', '--max_threads', type=int, default=10, help='Max threads')

    # Proxy
    parser_proxy = subparsers.add_parser('proxy', help='Proxy Banner Grabber')
    parser_proxy.add_argument('-t', '--target', required=True, help='Target IP or domain')
    parser_proxy.add_argument('-p', '--port', type=int, required=True, help='Target port')
    parser_proxy.add_argument('-x', '--proxy_ip', required=True, help='Proxy IP address')
    parser_proxy.add_argument('-q', '--proxy_port', type=int, required=True, help='Proxy port')
    parser_proxy.add_argument('-y', '--proxy_type', choices=['socks4', 'socks5', 'http'], required=True, help='Proxy type')

    # Fragmented
    parser_frag = subparsers.add_parser('fragmented', help='Fragmented Packet Banner Grabber')
    parser_frag.add_argument('-t', '--target', required=True, help='Target IP address')
    parser_frag.add_argument('-p', '--port', type=int, required=True, help='Target port')

    # HTTP
    parser_http = subparsers.add_parser('http', help='HTTP Header Banner Grabber')
    parser_http.add_argument('targets', nargs='+', help='Target IP(s) or domain(s)')
    parser_http.add_argument('-p', '--port', type=int, default=80, help='Port (default 80)')
    parser_http.add_argument('-t', '--threads', type=int, default=5, help='Number of threads (max 10)')

    args = parser.parse_args()

    if args.technique == 'tcp':
        run_tcp_banner_grab(args.targets, args.ports, args.timeout, args.max_threads, log_func=log_func)

    elif args.technique == 'proxy':
        run_proxy_banner_grab(args.target, args.port, args.proxy_ip, args.proxy_port, args.proxy_type, log_func=log_func)

    elif args.technique == 'fragmented':
        run_fragmented_banner_grab(args.target, args.port, log_func=log_func)

    elif args.technique == 'http':
        run_http_banner_grab(args.targets, args.port, args.threads, log_func=log_func)

    else:
        log_func(Fore.RED + "[-] No valid technique selected. Use -h for help." + Style.RESET_ALL)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
