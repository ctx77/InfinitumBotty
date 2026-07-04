import random
import urllib
import urllib.request
import requests
import html

from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from faustbot.modules.TitleObserver import TitleObserver
from faustbot.modules.ComicScraper import ComicScraper

from comics import *


class ComicObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".comic"]

    @staticmethod
    def help():
        return ".comic - liefert einen Link zu einem zufälligen Comic"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].find(".comic") == -1:
            return

        # Join list of comics that have a web based random functionality and those that need a scraper
        all_comics = comics + scraper_comics

        # Choose from the joined list
        comic = random.choice(all_comics)

        # Check which type of comic it is: If it's one that doesn't need a scraper, get the url and return it.
        # If it needs a scraper, use ComicScraper to scrape the comic.
        # If you want to add custom comic scrapers: Look at ComicScraper.py and insert your functionality.
        if comic not in scraper_comics:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
            req = urllib.request.Request(comic, None, headers)
            resource = urllib.request.urlopen(req)
            title = TitleObserver.getTitle(TitleObserver(), resource.url)
            connection.send_back(resource.geturl() + " " + title, data)
        else:
            connection.send_back(ComicScraper.getRandomComic(self, comic), data)
