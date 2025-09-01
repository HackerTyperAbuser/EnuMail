from dataclasses import dataclass
import smtplib
from typing import Tuple, Optional

@dataclass
class SmtpConfig():
    host: str
    port: int = 25
    timeout: float = 10.0
    useTls: bool = False

@dataclass 
class SmtpBannerInfo:
    connectCode: int
    bannerText: str
    ehloCode: int
    ehloText:str
    usedStartTLS: bool

@dataclass
class Pop3Config():
    host: str
    port: int = 110
    timeout: float = 10.0
    useTls: bool = False

@dataclass
class Pop3BannerInfo:
    connectCode: int
    bannerText: str
    useTls: bool
    capabilities: str

@dataclass
class ImapConfig():
    host: str
    port: int = 143
    timeout: float = 10.0
    useTls: bool = False
    

@dataclass
class ImapBannerInfo:
    connectCode: int
    bannerText: str
    capabilities: str = ""
    useTls: bool = False