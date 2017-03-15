import sys
from pdf2txt import convertImgPdf, convertImgPdf1Process

# usage:

# for one process:
# python convertImgPdfScript.py 0 file.pdf


# for one multiprocess:
# python convertImgPdfScript.py 1 file.pdf

if sys.argv[1] == '1':
    print(convertImgPdf(sys.argv[2]))
elif sys.argv[1] == '0':
    print(convertImgPdf1Process(sys.argv[2]))
else:
    print(':(')