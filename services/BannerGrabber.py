from client import ImapClient, Pop3Client
from client.config import ImapBannerInfo, Pop3BannerInfo, SmtpBannerInfo
from client.SmtpClient import SmtpClient

class BannerGrabber:
    def __init__(self, cfg, service: str):
        self._cfg = cfg
        self._service = service

    def bannerGrab(self):
        if self._service == "smtp":
            with SmtpClient(self._cfg) as client:
                print("[+] SMTP server connected")
                code, banner = client.smtpGrabBanner()
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

    def smtpBrute(self, usernames: list[str]):
        with SmtpClient(self._cfg) as client:
            ok, code, msg = client.isVrfyAvailable()
            if not ok:
                print(f"[-] VRFY command not available")
                return 1
            else:
                print(f"[+] VRF command available, checking responses")
                
            testUsers = ["root", "admin", "user", "invalid"]
            is_enum_possible, responses = client.isVrfyBruteForceable(testUsers)

            if is_enum_possible:
                print("[!] Server returns different responses, attempting brute force")
            else:
                print("[-] Responses looks similar, username enumeration may not be possible.")
                return 1
            
            print("[*] Attempting brute force...")
            validUsers = client.vrfyBruteForce(usernames)
            for user, code, msg in validUsers:
                print(f"[+] Found user: {user} ({code} {msg})")
            return 0
    
    def loginPop3(self, username: str, password: str):
        with Pop3Client(self._cfg) as client:
            # Return login success true false
            success = client.authenPop3(username, password)

            if success:
                print(f"[+] Logged in to POP3 with credential {username}:{password}")
                print("[*] Attempting email dump...")
                messsages = client.listMessages()
                for message in messsages:
                    print(f"{message['index']}: From {message['from']} | Subject: {message['subject']} | Date: {message['date']}")
                    return 0

            print("[-] Pop3 Authentication Failed")
            return 1


            