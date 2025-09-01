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
class BannerInfo:
    connectCode: int
    bannerText: str
    ehloCode: int
    ehloText:str
    usedStartTLS: bool