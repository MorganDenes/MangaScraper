from fpdf import FPDF
from PIL import Image
from statistics import mode
import math
import glob
import os

class MangaToPDF:
    pdf = 0
    width = 0
    height = 0
    w = []
    h = []
    imageList = []

    def __init__(self, pdfname, directory):
        self._GetImages(directory)
        self._CreatePDF(pdfname)
    
    def _CreatePDF(self, output):
        self._ModeSize()
        self.pdf = FPDF('P','pt', (self.width, self.height))
        count = 0
        pdfcount = 1
        for image in self.imageList:
            self._AddPage(image)
            if count >= 100:
                print("Creating PDF")
                self.pdf.output(output + "_{}.pdf".format(str(pdfcount).zfill(3)),"F")
                self.pdf = None
                self.pdf = FPDF('P','pt', (self.width, self.height))
                count = 0
                pdfcount += 1
            count += 1
        print("Creating PDF")
        self.pdf.output(output + "_{}.pdf".format(pdfcount),"F")

    def _AddPage(self, filename):
        self.pdf.add_page()
        print("Adding " + filename)
        self.pdf.image(filename, 0, 0, self.width, self.height)

    def _AddSize(self, width, height):
        self.w.append(width)
        self.h.append(height)
    
    def _ModeSize(self):
        self.width = mode(self.w)
        self.height = mode(self.h)
        print("Mode: %s, %s"%(self.width, self.height))

    def _GetImages(self, directory):
        for filename in glob.glob(directory + '/*.jpg'):
            name = [filename]
            try:
                img = Image.open(name[0])
                # if img.mode != "L":
                #     img = self._CleanImage(filename, img)
                width, height = img.size
                if width > (height * 1.3):
                    name = self._SplitPage(img, name[0])
                else:
                    self._AddSize(width, height)
                for i in name:
                    self.imageList.append(i)
            except:
                print("%s is a bad file."%filename)


    def _CleanImage(self, filename, img):
        print("Cleaning %s"%filename)
        img = img.convert("L")
        img.save(filename)
        return img

    def _SplitPage(self, image, imageName):
        filenames = []
        width, height = image.size
        half = [0, width/2, width]
        extentionless = imageName.replace(".jpg", "")
        for i in range(0, 2):
            o = image.crop((half[1-i], 0, half[2-i], height))
            halfname = extentionless + "_{}.jpg".format(i + 1)
            o.save(halfname)
            print("added " + halfname)
            self._AddSize(width/2, height)
            filenames.append(halfname)
        os.remove(imageName)
        print('removed ' + imageName)
        return filenames

# MangaToPDF("Kumo Desu Ga, Nani Ka", "Spider")
# MangaToPDF("UQ Holder!", "UQHolder")
# MangaToPDF("Lucifer and Biscuit Hammer", "biscut")
