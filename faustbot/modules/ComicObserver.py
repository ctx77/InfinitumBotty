import random
import urllib
import urllib.request
import requests
import html
import re
import json

from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from faustbot.modules.TitleObserver import TitleObserver

from comics import *


# Comic scraper scrapes comics from urls that have no website based random functionality. Comic URLs have to be in comics.py
class ComicScraper(PrivMsgObserverPrototype):
    # Scrapers for specific websites follow here:
    # Scraper for betamonkeys.co.uk removed

    # scraper for Nichtlustig
    def scrapeNichtlustig(self):
        # get content of get_cartoons_list.php

        request = requests.get("https://joscha.com/get_cartoons_list.php")
        slugs = re.findall(r"\"[0-9]{6}\"", request.text)
        for i in range(len(slugs)):
            slugs[i] = re.sub('"', "", slugs[i])

        # Choose random index
        comic = random.choice(slugs)

        # return random comic
        return "https://joscha.com/nichtlustig/" + comic

    def scrapeExplosmNet(self):
        # get content from https://explosm.net/_next/static/chunks/pages/comics-64414b42d3dfeef0.js
        request = requests.get(
            "https://explosm.net/_next/static/chunks/pages/comics-64414b42d3dfeef0.js"
        )

        # format request body
        json1 = re.split(r"[\[\]]", request.text)
        json1 = re.sub(r"\\", "", json1[6])
        json1 = re.sub(r"},{", r"\n", json1)
        json1 = re.sub(r"[\{\}]", "", json1)
        lines = json1.splitlines()

        # format for seperate "slugs"
        slugs = []
        for line in lines:
            slugMitAZ = re.split(r"\"slug\":", line)
            slugClean = re.sub(r"\"", "", slugMitAZ[1])
            slugs.append(slugClean)

        comic = random.choice(slugs)
        return "https://explosm.net/comics/" + comic

    # your custom scraper here
    # def scrapeYourCustomComic(url):
    # return "Your custom scraped URL"

    # Main scraping function. Takes url, decides scraping method to use. If no scraping method is found: return "No parser found"
    def getRandomComic(self, url):
        if "joscha.com" in url:
            return ComicScraper.scrapeNichtlustig(self)

        if "explosm.net" in url:
            return ComicScraper.scrapeExplosmNet(self)
        else:
            return "No parser found for comic URL: " + url


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

        if data["message"].startswith(".comic"):

            # Join list of comics that have a web based random functionality and those that need a scraper
            all_comics = comics + scraper_comics

            if connection.details.get_channel() == "#autistenchat-fsk18":
                all_comics = comics + scraper_comics + scraper_comics_fsk

            # Choose from the joined list
            comic = random.choice(all_comics)

            # Check which type of comic it is: If it's one that doesn't need a scraper, get the url and return it.
            # If it needs a scraper, use ComicScraper to scrape the comic.
            # If you want to add custom comic scrapers: Look at ComicScraper.py and insert your functionality.
            if comic not in scraper_comics and comic not in scraper_comics_fsk:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
                req = urllib.request.Request(comic, None, headers)
                resource = urllib.request.urlopen(req)
                title = TitleObserver.getTitle(TitleObserver(), resource.url)
                connection.send_back(resource.url + " " + title, data)
            else:
                url = ComicScraper.getRandomComic(self, comic)
                title = TitleObserver.getTitle(TitleObserver(), url)
                connection.send_back(url + " " + title, data)
        else:
            return
