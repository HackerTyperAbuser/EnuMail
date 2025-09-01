from audit.config import BannerInfo, SmtpConfig
from audit.client import SmtpClient

class BannerGrabber:
    def __init__(self, cfg: SmtpConfig):
        self.cfg = cfg

    def smtp(self) -> BannerInfo:
        with SmtpClient(self.cfg) as client:
            code, banner = client.grabBanner()
            usedTls = False

            ehloCode, ehloText = None
            
            return BannerInfo(
                connectCode=code,
                bannerText=banner,
                ehloCode=ehloCode,
                ehloText=ehloText,
                usedStartTLS=usedTls
            )