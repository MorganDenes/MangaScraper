from MangaCrawler import MangaCrawler


class Manganelo(MangaCrawler):
    website = "https://manganelo.com/"

    def _FindChapters(self, webpage):
        chapterRows = webpage.find_all('div', attrs={'class':'row'})
        chapters = []
        for row in chapterRows:
            chapters.append(row.find('a'))
        return chapters
    pass


# Manganelo("Tomo-chan wa Onnanoko!", "Tomochan", "/manga/tomochan_wa_onnanoko")
