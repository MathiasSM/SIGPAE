from os import listdir
import os.path
import tempfile
import shutil
import sys

import wand.image
from wand.color import Color

import codecs
import PIL.Image

import pyocr
import pyocr.builders

import PyPDF2

import magic

class NoTesseractError(Exception):
    pass

class BadFormatError(Exception):
    pass


# Library for extracting text out of a pdf file.

def checkPdfFile(pdfName):
    open(pdfName)
    if not ("pdf" in magic.from_file(pdfName, mime=True).lower()):
        raise BadFormatError

def convertImgPdf(pdfName):
    checkPdfFile(pdfName)

    tempDir = os.path.abspath(tempfile.mkdtemp())
    # Fetching images...
    with wand.image.Image(filename=pdfName, resolution=300) as original:
        with original.convert('png') as imgs:
            i = 0
            for imgi in imgs.sequence:
                img = wand.image.Image(image=imgi)
                img.background_color = Color("white")
                img.alpha_channel = 'remove'
                img.save(filename = tempDir  + '/'+ str(i) + '.png')
                i += 1
    images = sorted([f for f in listdir(tempDir)])
    returnText = ""
    
    try:
        tool = (pyocr.get_available_tools())[0]
    except:
        shutil.rmtree(tempDir)
        raise NoTesseractError

    # Running tesseract-ocr over the images... 
    for img in images:
        builder = pyocr.builders.TextBuilder()
        txt = tool.image_to_string(
            PIL.Image.open(tempDir  + '/'+ img),
            lang="spa",
            builder=builder)
        returnText = returnText + txt
    shutil.rmtree(tempDir)
    return returnText


def convertTxtPdf(pdfName):
    checkPdfFile(pdfName)
    pdfFile = open(pdfName, 'rb')
    readPdf = PyPDF2.PdfFileReader(pdfFile)
    numberOfPages = readPdf.getNumPages()
    returnText = ""
    for i in range(numberOfPages):
        returnText = returnText + readPdf.getPage(i).extractText()
    return returnText 
    
