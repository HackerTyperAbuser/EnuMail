import argparse
import sys 

from services.BannerGrabber import BannerGrabber
from client.config import ImapConfig, Pop3Config, SmtpConfig

def buildParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mail Service Security Tool",
            epilog=(
                "Example:\n"
                " python3 enumail.py smtp 192.168.20.54 -p 25\n"
                " python3 enumail.py pop3 192.168.20.54 -p 110\n"
                " python3 enumail.py imap 192.168.20.54 -p 143\n"
            ),
            formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument("service", help="Service to target (SMTP, POP3, IMAP)")
    parser.add_argument("host", help="Mail server host (IP or domain)")
    parser.add_argument("-p", "--port", type=int, help="Port number of service")
    parser.add_argument("-e", "--timeout", type=float, default=10.0, help="Timeout duration (default: 10)")
    parser.add_argument("-s", "--tls", action="store_true", help="Attempt TLS/SSL connection")
    return parser

def main():
    args = buildParser().parse_args()
    service = args.service.lower()

    if service == "smtp":
        cfg = SmtpConfig(
            host=args.host,
            port=args.port or 25,
            timeout=args.timeout,
            useTls=args.tls
        )
        print("[*] SMTP config: {cfg}")
    elif service == "pop3":
        cfg = Pop3Config(
            host=args.host,
            port=args.port or 110,
            timeout=args.timeout,
            useTls=args.tls
        )
        print("[*] POP3 config: {cfg}")
    elif service == "imap":
        cfg = ImapConfig(
            host=args.host,
            port=args.port or 143,
            timeout=args.timeout,
            useTls=args.tls
        )
        print("[*] IMAP config: {cfg}")
    else:
        print("[-] Unknown service. Use smtp, pop3, or imap")
        return 1
    
    grabberService = BannerGrabber(cfg, service)
    print(f"[+] {service.upper()} Banner: {grabberService.bannerGrab()}")
    return 0

if __name__ == "__main__":
    main()