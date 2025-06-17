import sys, os
sys.path.append(os.path.dirname(__file__))

import argparse
from portscanning.Tcpconnectscanner_fixed import TCPConnectScanner
from portscanning.syn_scan import SynPortScanner
from portscanning.slow_timing_scanner import PortScanner
from portscanning.decoy_scan import DecoyScanner

def parse_ports(port_str):
    ports = set()
    parts = port_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

def run_tcp_scan(target, ports_str, threads=10, log_func=print):
    ports = [int(p.strip()) for p in ports_str.split(',') if p.strip().isdigit()]
    scanner = TCPConnectScanner(target, ports)
    scanner.run(max_threads=threads, log_func=log_func)

def run_syn_scan(target, port_str, log_func=print):
    ports = parse_ports(port_str)
    scanner = SynPortScanner(target, ports, log_func=log_func)
    scanner.scan()

def run_slow_scan(target, port_str, delay=0, threads=10, log_func=print):
    ports = parse_ports(port_str)
    scanner = PortScanner(target, ports, delay, log_func=log_func)  
    scanner.start_scan(max_threads=threads)

def run_decoy_scan(target, port_str, decoys=5, timeout=1, log_func=print):
    ports = parse_ports(port_str)
    scanner = DecoyScanner(target, ports, decoys, timeout, log_func=log_func)  
    scanner.start_scan()

def main():
    parser = argparse.ArgumentParser(
        description="Main VAPT Scanner",
        usage="python main.py <method> <target> -p <ports> [--threads N] [--delay N] [--decoys N] [--timeout N]"
    )
    parser.add_argument("method", nargs="?", choices=["tcp", "syn", "slow", "decoy"], help="Scan technique")
    parser.add_argument("target", nargs="?", help="Target IP address")
    parser.add_argument("-p", "--ports", required=True, help="Ports to scan (e.g. 22,80,443 or 20-25)")
    parser.add_argument("--threads", type=int, default=10, help="Max threads (default: 10)")
    parser.add_argument("--delay", type=int, default=0, help="Delay in seconds (for slow scan)")
    parser.add_argument("--decoys", type=int, default=5, help="Number of decoy IPs")
    parser.add_argument("--timeout", type=int, default=1, help="Connection timeout (for decoy only)")

    args = parser.parse_args()

    if args.method == "tcp":
        run_tcp_scan(args.target, args.ports, args.threads)
    elif args.method == "syn":
        run_syn_scan(args.target, args.ports)
    elif args.method == "slow":
        run_slow_scan(args.target, args.ports, args.delay, args.threads)
    elif args.method == "decoy":
        run_decoy_scan(args.target, args.ports, args.decoys, args.timeout)

if __name__ == "__main__":
    main()
