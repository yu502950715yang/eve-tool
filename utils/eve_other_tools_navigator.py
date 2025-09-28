from venv import logger
import webbrowser

"""
EVE 其他工具网址导航
"""
class EveOtherToolsNavigator:

    DEFAULT_URLS = {
        "kb": "https://kb.ceve-market.org",
        "market": "https://www.ceve-market.org",
        "tools": "https://tools.ceve-market.org",
    }

    def __init__(self):
        pass

    def open_url(self, url_key):
        if url_key not in self.DEFAULT_URLS:
            logger.error(f"未知的URL键: {url_key}")
            return False
        return webbrowser.open(self.DEFAULT_URLS[url_key])
