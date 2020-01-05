from bs4 import BeautifulSoup as bs 
import requests
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
import time
import os

from MangaToPDF import MangaToPDF


class MangaCrawler:
    website = "https://mangakisa.com"
    scraper = 0
    currentChapter = 1
    outDir = ''

    def __init__(self, name, output, extention, startingchapter = 0):
        self._CreateDirectory(output)
        MangaPage = self._GetPage(self.website + extention)
        ChapterPages = self._FindChapters(MangaPage)
        print("%s chapters found!"%len(ChapterPages))
        time.sleep(1)
        print("Starting download:")
        for chapter in ChapterPages[::-1]:
            if self.currentChapter < startingchapter:
                self.currentChapter += 1
                continue
            print("\n\nStarting chapter %s:"%self.currentChapter)
            self._DownloadChapter(chapter['href'])
            print("Chapter %s of %s finished!"%(self.currentChapter, len(ChapterPages)))
            self.currentChapter += 1
            time.sleep(10)
        # MangaToPDF(name, output)


    def _CreateDirectory(self, output):
        self.outDir = output
        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)
    
    def _GetPage(self, url):
        r = requests.get(url)
        return bs(r.text, 'html.parser')

    def _FindChapters(self, webpage):
        return webpage.find_all('a', attrs={'class':'infovan'})

    def _FindImages(self, webpage):
        vung = webpage.find_all('div', attrs={'class':'vung-doc'})
        images = []
        for doc in vung:
            images.append(doc.find('img'))
        return images

    def _DownloadImage(self, url, img, imageName):
        r = requests.get(img['src'])
        with open("%s/%s"%(self.outDir, imageName), 'wb') as outfile:
            outfile.write(r.content)

    def _DownloadChapter(self, url):
        chapterPage = self._GetPage(url if self.website in url else self.website + '/' + url)
        chapterImages = self._FindImages(chapterPage)
        print("\t%s page(s) found! Starting to download:"%len(chapterImages))
        page = 1
        for img in chapterImages:
            imageName = "chp%spg%s.jpg"%(str(self.currentChapter).zfill(4), str(page).zfill(3))
            self._DownloadImage(url, img, imageName)
            print("\t%s: %s"%(str(page).zfill(3), imageName))
            page += 1
