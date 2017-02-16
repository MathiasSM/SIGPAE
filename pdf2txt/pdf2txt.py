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


# Library for extracting text out of a pdf file.

def convertImgPdf(pdfName):
    try:
        open(pdfName)
    except:
        return('')
        # Throw exception

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
        #print("No se encontro una herramienta OCR.")
        #print("Instale tesseract-ocr.")
        shutil.rmtree(tempDir)
        return('')

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
    try:
        pdfFile = open(pdfName, 'rb')
    except:
        return('')
        # Throw exception
    
    readPdf = PyPDF2.PdfFileReader(pdfFile)
    numberOfPages = readPdf.getNumPages()
    returnText = ""
    for i in range(numberOfPages):
        returnText = returnText + readPdf.getPage(i).extractText()
    return returnText 
    
