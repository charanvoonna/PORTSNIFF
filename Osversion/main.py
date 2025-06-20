import argparse
from .active_fingerprint import ActiveFingerprint
from .passive_fingerprint import PassiveFingerprint
from colorama import Fore, init
from scapy.all import get_if_list

init(autoreset=True)

def run_active_fingerprint(target, ports="80,443", threads=5):
    port_list = [int(p.strip()) for p in ports.split(",")]
    scanner = ActiveFingerprint(target, port_list, threads)
    scanner.run()

def run_passive_fingerprint(interface=None, count=100):
    print(Fore.CYAN + "[TraceNet] Available Interfaces:")
    for iface in get_if_list():
        print(Fore.CYAN + f" - {iface}")

    sniffer = PassiveFingerprint(interface, count)
    sniffer.start_sniffing()


def main():
    parser = argparse.ArgumentParser(description="TraceNet OS Fingerprinting (Active & Passive)")
    subparsers = parser.add_subparsers(dest="mode", help="Fingerprinting mode")

    active_parser = subparsers.add_parser("active", help="Run Active OS Fingerprinting")
    active_parser.add_argument("-t", "--target", required=True, help="Target IP address")
    active_parser.add_argument("-p", "--ports", default="80,443", help="Comma-separated list of ports")
    active_parser.add_argument("--threads", type=int, default=5, help="Number of threads (max 10)")

    passive_parser = subparsers.add_parser("passive", help="Run Passive OS Fingerprinting")
    passive_parser.add_argument("-i", "--interface", help="Interface to sniff on")
    passive_parser.add_argument("-c", "--count", type=int, default=100, help="Number of packets to sniff")

    args = parser.parse_args()

    if args.mode == "active":
        run_active_fingerprint(args.target, args.ports, args.threads)
    elif args.mode == "passive":
        run_passive_fingerprint(args.interface, args.count)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
