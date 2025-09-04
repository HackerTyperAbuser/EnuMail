from __future__ import annotations
from typing import Optional, Tuple
import imaplib
import socket

class ImapClient:
    def __init__(self, cfg: ImapClient):
        self._cfg = cfg
        self._server: Optional[imaplib.IMAP4] = None
        self._connected = False
        self._lastBanner: Optional[Tuple[int, bytes]] = None

    def __enter__(self) -> "ImapClient":
        # imaplib takes 'timeout' via socket default
        old = socket.getdefaulttimeout
        socket.setdefaulttimeout(self._cfg.timeout)

        try:
            self._server = imaplib.IMAP4(self._cfg.host, self._cfg.port)
            self._connected = True
        finally:
            socket.setdefaulttimeout(old)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._server:
                self._server.logout()
        except Exception:
            try:
                if self._server and getattr(self._server, "shutdown", None):
                    self._server.shutdown()
            except Exception:
                pass

    def imapGrabBanner(self) -> Tuple[bool, str]:
        if not self._connected or not self._server:
            raise RuntimeError("[-] Not conntected to IMAP server")

        raw = getattr(self._server, "welcome", b"") or b""
        text = raw.decode(errors="replace").strip()
        ok = text.upper().startswith("* OK")
        return ok, text