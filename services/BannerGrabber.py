from client import ImapClient, Pop3Client
from client.config import ImapBannerInfo, Pop3BannerInfo, SmtpBannerInfo, SmtpConfig 
from client.SmtpClient import SmtpClient

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class BannerGrabber:
    def __init__(self, cfg, service: str):
        self._cfg = cfg
        self._service = service

    def bannerGrab(self):
        if self._service == "smtp":
            with SmtpClient(self._cfg) as client:
                code, banner = client.grabBanner()
                usedTls = False

                ehloCode, ehloText = client.ehloOrHelo()
                
            return SmtpBannerInfo(
                connectCode=code,
                bannerText=banner,
                ehloCode=ehloCode,
                ehloText=ehloText,
                usedStartTLS=usedTls
            )
        
        if self._service == "pop3":
            with Pop3Client(self._cfg) as client: 
                code, text = client.pop3GrabBanner()
                useTls = False

            return Pop3BannerInfo(
                connectCode=code,
                bannerText=text,
                useTLS=useTls
            )
        
        if self._service == "imap":
            with ImapClient(self._cfg) as client:
                ok, text = client.imapGrabBanner()

            return ImapBannerInfo(
                connectCode=ok,
                bannerText=text
            )  
        raise ValueError("[-] Unknown service")
    
    def createMail(self):
        with SmtpClient(self._cfg) as client:
            print("[!] Preparing to send mail")

            sender = input("Sender: ").strip()
            recipient = input("Recipient: ").strip()
            subject = input("Topic: ").strip()
            body = input("Message: ")
            user = input("SMTP username (leave blank for none): ").strip() or None
            password = input("SMTP password (leave blank for none): ").strip() or None

            success = client.sendConstructMail(sender=sender, recipients=recipient, subject=subject, body=body, username=user, password=password)

            if success:
                print("[+] Message sent!")
            else:
                print("[-] Unable to send message")