import random
import re
import requests


# Comic scraper scrapes comics from urls that have no website based random functionality. Comic URLs have to be in comics.py
class ComicScraper:
    # Scrapers for specific websites follow here:
    # Scraper for betamonkeys.co.uk removed

    # scraper for Nichtlustig
    def scrapeNichtlustig(self):
        # TODO: Write a scraper for Nichtlustig!
        # get content of get_cartoons_list.php

        request = requests.get("https://joscha.com/get_cartoons_list.php")
        slugs = re.findall(r"\"[0-9]{6}\"", request.text)
        for i in range(len(slugs)):
            slugs[i] = re.sub('"', "", slugs[i])

        # Choose random index
        comic = random.choice(slugs)

        # return random comic
        return "https://joscha.com/nichtlustig/" + comic

    # your custom scraper here
    # def scrapeYourCustomComic(url):
    # return "Your custom scraped URL"

    # Main scraping function. Takes url, decides scraping method to use. If no scraping method is found: return "No parser found"
    def getRandomComic(self, url):
        if "joscha.com" in url:
            return ComicScraper.scrapeNichtlustig(self)

        else:
            return "No parser found for comic URL: " + url
