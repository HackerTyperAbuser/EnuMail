from __future__ import annotations
from typing import Optional, Tuple
import poplib
import re

from client.config import Pop3Config

class Pop3Client:
    def __init__(self, cfg: Pop3Config):
        self._cfg = cfg
        self._server: Optional[poplib.POP3] = None
        self._connected = False
        self._lastBanner: Optional[Tuple[int, bytes]] = None
    
    def __enter__(self) -> "Pop3Client":
        self._server = poplib.POP3(self._cfg.host, self._cfg.port, timeout=self._cfg.timeout)
        self._connected = True
        return self
    
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
    
    # Pop3 banner returns bytes like b'+OK POP3 server ready'
    def pop3GrabBanner(self) -> Tuple[int, str]:
        if not self._connected or not self._server:
            raise RuntimeError("[-] Not connected to POP3 server")
        
        banner = self._server.getwelcome()
        text = banner.decode(errors="replace").strip()
        code = 1 if text.startswith("+OK") else 0
        return code, text
    
    def authenPop3(self, username: str, password: str) -> bool:
        if not self._connected or not self._server:
            raise RuntimeError("[-] Not connected to POP3 server")
        
        try:
            userResponse= self._server.user(username)
            passwordResponse = self._server.pass_(password)

            return userResponse.startswith(b'+OK') and passwordResponse.startswith(b'+OK')
        except Exception:
            return False

    def listMessages(self) -> list[dict]:
        if not self._connected or not self._server:
            raise RuntimeError("[-] Not connected to POP3 server")
        
        summaries = []
        try:
            resp, mails, octets = self._server.list()

            for i in range(1, len(mails) + 1):
                resp, lines, octets = self._server.top(i, 0)
                headers = b"\n".join(lines).decode(errors="replace")
                from_ = re.search(r"^From:\s+(.+)", headers, re.MULTILINE | re.IGNORECASE)
                subject = re.search(r"^Subject:\s+(.+)", headers, re.MULTILINE | re.IGNORECASE)
                date = re.search(r"^Date:\s+(.+)", headers, re.MULTILINE | re.IGNORECASE)

                summaries.append({
                    "index": i,
                    "from": from_.group(1).strip() if from_ else "(unknown)",
                    "subject": subject.group(1).strip() if subject else "(no subject)",
                    "date": date.group(1).strip() if date else "(no date)"
                })
            return summaries
        
        except Exception as e:
            print(f"[-] Failed to list messages: {e}")
            return []