import sys
import glob
from PyPDF2 import PdfFileMerger


files = glob.glob("*.pdf")

merger = PdfFileMerger()

for file in files:
    merger.append(file)

merger.write("results.pdf")
merger.close()

# inputStream = []
# for fi in files:
#     inputStream.append(open(fi, 'rb'))
# writer = PdfFileWriter()

# for reader in map(PdfFileReader, inputStream):
#     for n in range(reader.getNumPages()):
#         writer.addPage(reader.getPage(n))
# writer.write("asdf.pdf")
# for f in inputStream:
#     f.close()


