import argparse 

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
    
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("host", help="Mail server host (IP or domain)")
    common.add_argument("-p", "--port", type=int, help="Port number of service")
    common.add_argument("-e", "--timeout", type=float, default=10.0, help="Timeout duration (default: 10)")
    common.add_argument("-s", "--tls", action="store_true", help="Attempt TLS/SSL connection")

    subparsers = parser.add_subparsers(dest="service", required=True, help="Service to target (SMTP, POP3, IMAP)")

    # ----------------------------------------------------------------------------------------------------------------
    #                                                 SMTP PARSER
    # ----------------------------------------------------------------------------------------------------------------
    smtpParser = subparsers.add_parser("smtp", parents=[common], help="Target SMTP service")
    smtpParser.set_defaults(default_port=25)
    smtpParser.add_argument("-c", "--create", action="store_true", help="Create and send a test email (SMTP)")

    # ----------------------------------------------------------------------------------------------------------------
    #                                                 POP3 PARSER
    # ----------------------------------------------------------------------------------------------------------------
    # pop3Parser = subparsers.add_parser("smtp", parents=[common], help="Target Pop3 service")
    # pop3Parser.set_defaults(default_port=25)
    # pop3Parser.add_argument("-d", "--dump", action="store_true", help="Read stored emails on Pop3")

    # ----------------------------------------------------------------------------------------------------------------
    #                                                 IMAP PARSER
    # ----------------------------------------------------------------------------------------------------------------
    # imapParser = subparsers.add_parser("imap", parents=[common], help="Target IMAP service")
    # imapParser.set_defaults(default_port=25)
    # imapParser.add_argument("-d", "--dump", action="store_true", help="Read stored emails on IMAP")

    return parser

def main():
    args = buildParser().parse_args()
    service = args.service.lower()
    port = args.port

    if service == "smtp":
        if port is None:
            port = 587 if args.tls else args.default_port
        cfg = SmtpConfig(
            host=args.host,
            port=port,
            timeout=args.timeout,
            useTls=args.tls
        )
        print("[*] SMTP config: {cfg}")

        if args.create:
            print("[!] Create email mode")
            grabberService.createmail()
            return 0
        
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