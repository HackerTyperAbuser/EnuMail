from __future__ import annotations
from typing import Optional, Tuple
import poplib

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
    
    def __exit__(self):
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
            raise RuntimeError("[-] Not conntected to POP3 server")
        
        banner = self._server.getwelcome()
        text = banner.decode(errors="replace").strip()
        code = 1 if text.startswith("+OK") else 0
        return code, text