from bs4 import BeautifulSoup as bs 
import requests
import cfscrape
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
import time
import os

from MangaToPDF import MangaToPDF
from MangaCrawler import MangaCrawler


class MangaKisa(MangaCrawler):
    website = "https://mangakisa.com"
    scraper = None
    currentChapter = 1
    outDir = ''

    def _CreateDirectory(self, output):
        self.outDir = output
        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)
    
    def _CreateScraper(self):
        session = requests.Session()
        self.scraper = cfscrape.create_scraper(sess=session)

    def _GetPage(self, url):
        r = self.scraper.get(url)
        return bs(r.text, 'html.parser')

    def _FindChapters(self, webpage):
        return webpage.find_all('a', attrs={'class':'infovan'})

    def _FindImages(self, webpage):
        return webpage.find_all('img')

    def _DownloadImage(self, url, img, imageName):
        r = self.scraper.get(img['src'])
        with open("%s/%s"%(self.outDir, imageName), 'wb') as outfile:
            outfile.write(r.content)

    def _DownloadChapter(self, url):
        chapterPage = self._GetPage(self.website + '/' + url)
        chapterImages = self._FindImages(chapterPage)
        print("\t%s page(s) found! Starting to download:"%len(chapterImages))
        page = 1
        for img in chapterImages:
            imageName = "chp%spg%s.jpg"%(str(self.currentChapter).zfill(4), str(page).zfill(3))
            self._DownloadImage(url, img, imageName)
            print("\t%s: %s"%(str(page).zfill(3), imageName))
            page += 1


# MangaKisa("Dr. Stone", "DrStone", "/dr-stone", 86)
# MangaKisa("Komi-San", "KomiSan", "/komi-san-wa-komyushou-desu", 212)
# MangaKisa("Kumo desu ga, "Spider", nani ka?", "/kumo-desu-ga-nani-ka", 79)
# MangaKisa("UQ Holder!", "UQHolder", "/uq-holder!", 165)
# MangaKisa("Fire Force", "FireForce", "/enen-no-shouboutai", 39)
# MangaKisa("Only Sense Online", "OnlySense", "/only-sense-online", 54)


