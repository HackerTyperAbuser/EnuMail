from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import List, Optional, Tuple
from client.config import SmtpConfig

class SmtpClient:
    # Constructor with SmtpConfig injected
    def __init__(self, cfg: SmtpConfig):
        self._cfg = cfg
        self._server: Optional[smtplib.SMTP] = None
        self._connected = False
        self._lastBanner: Optional[Tuple[int, bytes]] = None

    # Called when SmtpClient(cfg) is called when entering the with block
    def __enter__(self) -> "SmtpClient":
        self._server = smtplib.SMTP(timeout=self._cfg.timeout)
        # Connect SMTP server with configuration
        code, banner = self._server.connect(self._cfg.host, self._cfg.port) 

        # Encrypted traffic upgrade after first plaintext connection
        try:
            if self._cfg.useTls:
                print("[*] Attempting to upgrade to TLS using STARTTLS")
                self._server.starttls()
                print("[+] STARTTLS handshake successful")
        except smtplib.SMTPException as e:
            print(f"[-] STARTTLS failed: {e}")
            self._server.quit()
            raise

        self._connected = True
        self._lastBanner = (code, banner)
        return self
    
    # Called when exiting the with block
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._server:
                self._server.quit()
        except Exception:
            try:
                if self._server:
                    self._server.close()
            except Exception:
                pass

    # Helper method to check maintain connection
    def ensureConnected(self):
        if not self._connected or not self._server:
            raise RuntimeError("[-] Not connected to SMTP server.")
    
    # Banner retrieval
    def smtpGrabBanner(self) -> Tuple[int, str]:
        self.ensureConnected()
        if self._lastBanner is None:
            raise RuntimeError("[!] Connection established, no banner received.")
        code, banner = self._lastBanner
        return code, banner.decode(errors="replace").strip()
    
    # Attempt to EHLO or HELO 
    def ehloOrHelo(self) -> Tuple[int, str]:
        self.ensureConnected()
        code, response = self._server.ehlo()
        if code != 250:
            code, response = self._server.helo()
        return code, response.decode(errors="replace").strip()
    
    def sendConstructMail(self, sender:str, recipients: List[str] | str, subject: str, body: str, username: Optional[str] = None, password: Optional[str] = None) -> bool:
        self.ensureConnected()

        """
        Build and send a simple plaintext email.
        - sender: "alice@example.com"
        - recipients: ["bob@example.com", "charlie@example.com"]
        - subject: "Hello"
        - body: "This is a test"
        - username/password: for servers requiring authentication
        """

        if isinstance(recipients, str):
            recipients = [recipients]

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg["Subject"]  = subject
        msg.attach(MIMEText(body, "plain"))

        if username and password:
            self._server.login(username, password)
        
        try:
            self._server.sendmail(sender, recipients, msg.as_string())
        except Exception:
            return False
        return True

    # Check VRFY Command SMTP
    def isVrfyAvailable(self) -> Tuple[bool, int, str]:
        self.ensureConnected()
        try:
            code, msg = self._server.verify("root")
            msg_str = msg.decode(errors="replace") if isinstance(msg, bytes) else str(msg)
            return True, code, msg_str.strip()
        except smtplib.SMTPNotSupportedError:
            return False, 500, "VRFY command not supported"
        except smtplib.SMTPResponseException as e:
            return True, e.smtp_code, e.smtp_error.decode(errors="replace")
        except Exception as e:
            return False, 500, f"Error: {e}"

    # Check SMTP different responses
    def isVrfyBruteForceable(self, usernames: list[str]) -> Tuple[bool, dict]:
        self.ensureConnected()
        responses = {}
        for user in usernames:
            try:
                code, msg = self._server.verify(user)
                msg_str = msg.decode(errors="replace") if isinstance(msg, bytes) else str(msg)
            except smtplib.SMTPResponseException as e:
                code, msg_str = e.smtp_code, e.smtp_error.decode(errors="replace")
            except Exception as e:
                code, msg_str = 0, f"Error: {e}"
            
            responses[user] = (code, msg_str.strip())
        
        unique_values = set(responses.values())
        is_enum_possible = len(unique_values) > 1
        return is_enum_possible, responses

    # Attempt VRFY brute forcing
    def vrfyBruteForce(self, usernames: list[str]) -> list[Tuple[str, int, str]]:
        self.ensureConnected()
        valid_users = []
        for user in usernames:
            try:
                code, msg = self._server.verify(user)
                msg_str = msg.decode(errors="replace") if isinstance(msg, bytes) else str(msg)
            except smtplib.SMTPResponseException as e:
                code, msg_str = e.smtp_code, e.smtp_error.decode(errors="replace")
            except Exception as e:
                continue  # skip on unexpected error
            if code in [250, 252]:
                valid_users.append((user, code, msg_str.strip()))
        return valid_users
    


