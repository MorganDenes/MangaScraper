import time
from MangaCrawler import MangaCrawler
from MangaToPDF import MangaToPDF


class TenManga(MangaCrawler):
    website = "https://www.mangareader.net/the-promised-neverland/"


    def __init__(self, name, output, extention, startingchapter = 0):
        self._CreateDirectory(output)

        self.currentChapter = 116
        while self.currentChapter <= 161:
            chaperPage = self.website + str(self.currentChapter)
            chapterSoup = self._GetPage(chaperPage)
            print("\n\nStarting chapter %s:"%self.currentChapter)

            pageCount = chapterSoup.find('select', attrs={'name':'pageMenu'}).text.split('\n')[-2]
            for i in range(1, int(pageCount) + 1):
                imagePage = chaperPage + '/' + str(i)
                pageSoup = self._GetPage(imagePage)
                time.sleep(1.1)
                image = pageSoup.find('img')
                imageName = "chp%spg%s.jpg"%(str(self.currentChapter).zfill(4), str(i).zfill(3))
                self._DownloadImage(image['src'], image, imageName)
                print("\t%s: %s"%(str(i).zfill(3), imageName))
            print("Chapter %s of %s finished!"%(self.currentChapter, len(chapterSoup)))
            self.currentChapter += 1
            time.sleep(2)
        print("Finished Crawling")
        # MangaToPDF(name, output)




# Manganelo("Tomo-chan wa Onnanoko!", "Tomochan", "/manga/tomochan_wa_onnanoko")
# TenManga("Lucifer and Biscuit Hammer", "biscut", "the-lucifer-and-biscuit-hammer//book/The+Lucifer+and+Biscuit+Hammer.html?waring=1")
