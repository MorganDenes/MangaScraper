# import MangaKisa

from PIL import Image


try:
    o = Image.open('darling\\chp0035pg025.jpg')
    w, h = o.size

    if w == h:
        print("ew")
except:
    pass
