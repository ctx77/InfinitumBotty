import html
import re
import urllib
import json

from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from faustbot import logger


class TitleObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_priv_msg(self, data, connection: Connection):
        regex = r"(?P<url>https?://[^\s]+)"
        url = re.search(regex, data["messageCaseSensitive"])
        if url is not None:
            url = url.group()
            logger.info(f"TitleObserver: {url}")
            try:
                title = self.getTitle(url)
                logger.info(f"TitleObserver: {title}")
                title = title[:350]
                connection.send_back(title, data)
            except Exception as exc:
                logger.error(f"TitleObserver: {exc}")
                pass

    def getTitle(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

        if re.search("https?://\\[[^/]*", url):
            raise (Exception("Refusing to parse bare IPv6 Addresses"))
        if re.search("https?://[^/:]*:[^/:]*", url):
            raise (Exception("Refusing to parse URLs with Ports"))
        if re.search("https?://[0-9]+.[0-9]+.[0-9]+.[^/]*", url):
            raise (Exception("Refusing to parse bare IPv4 Addresses"))
        if re.search("https?://music.youtube.com/", url):
            url = url.replace("music.youtube.com/", "www.youtube.com/", 1)
        if re.search("https?://youtu.be/", url):
            url = url.replace("youtu.be/", "www.youtube.com/watch?v=", 1)
        if re.search("https?://www.youtube.com/shorts/", url):
            url = url.replace("www.youtube.com/shorts/", "www.youtube.com/watch?v=", 1)

        yt_json_data_re = False
        if re.search("https?://[^/]*youtube.com/shorts/", url):
            title_re = re.compile(
                r'''"reelPlayerHeaderRenderer":{"reelTitleText":{"runs":\[{"text":"([^"]*)"'''
            )
            headers["User-Agent"] = "curl/7.81.0"
        elif re.search("https?://[^/]*youtube.com/", url):
            title_re = re.compile(
                r'''"results":{"contents":\[{"videoPrimaryInfoRenderer":{"title":{"runs":\[{"text":"([^"]*)"'''
            )
            yt_json_data_re = re.compile("""var ytInitialData = ([^;]*)""")

        elif re.search("https?://[^/]*buttersafe.com", url):
            title_re = re.compile(r"<title[^>]*.\s*(.+?)</title>")

        else:
            title_re = re.compile("<title[^>]*>(.+?)</title>")

        req = urllib.request.Request(url, None, headers)

        # Keep the urlopen scope as short as possible (connection leaks)
        with urllib.request.urlopen(req, timeout=10) as response:
            encoding = response.headers.get_content_charset()
            content_raw = response.read()

        # der erste Fall kann raus, wenn ein anderer Channel benutzt wird
        if url.find("rehakids.de") != -1:
            encoding = "windows-1252"
        if not encoding:
            encoding = "utf-8"

        content = content_raw.decode(encoding, errors="replace")

        if yt_json_data_re:
            yt_json_data = json.loads(yt_json_data_re.search(content).group(1))
            _vid = yt_json_data["playerOverlays"]["playerOverlayRenderer"][
                "videoDetails"
            ]
            _base = _vid["playerOverlayVideoDetailsRenderer"]
            _title = _base["title"]["simpleText"]
            _creator = _base["subtitle"]["runs"][0]["text"]
            _views = _base["subtitle"]["runs"][2]["text"]
            title = f"{_title} - {_creator} - {_views}"
        else:
            title_matches = title_re.search(content)
            if title_matches:
                title = title_matches.group(1)
            else:
                # with open("content.html", "w") as file:
                #     file.write(content)
                raise Exception(f"Could not Parse Title for {url}")

        title = html.unescape(title)
        title = title.replace("\n", " ").replace("\r", "").replace("\t", "")
        title = title.replace("&lt;", "<")
        title = title.replace("&gt;", ">")
        title = title.replace("&amp;", "&")
        title = title.replace("&raquo;", "»")
        if title == "":
            raise Exception(f"Empty Title for {url}")
        return title
