import argparse 
import smtplib
import socket 
import ssl

from audit.banner import BannerGrabber
from audit.config import SmtpConfig

def buildParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mail Service Security Tool")
    parser.add_argument("host", help="SMTP server host (IP or domain)")
    parser.add_argument("-p", "--port", type=int, default=25, help="SMTP port (default: 25)")
    parser.add_argument("-e", "--timeout", type=float, default=10.0, help="Timeout duration (default: 10)")
    parser.add_argument("-s", "--tls", type=bool, default=False, help="Attmpt TLS/SSL connection")
    return parser

def main():
    args = buildParser.parse_args()

    cfg = SmtpConfig(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        useTls=args.tls
    )

    grabber = BannerGrabber(cfg)
    info = grabber.smtp()

    print(f"[+] Connected to {cfg.host}:{cfg.port}")
    print(f"[+] Banner ({info.connectCode}): {info.bannerText}")

if __name__ == "__main__":
    main()