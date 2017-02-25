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

from multiprocessing import Process, Pipe

class NoTesseractError(Exception):
    pass

class BadFormatError(Exception):
    pass


# Library for extracting text out of a pdf file.

def checkPdfFile(pdfName):
    open(pdfName)
    if not ("pdf" in magic.from_file(pdfName, mime=True).lower()):
        raise BadFormatError

def getImagesAndTmpDir(pdfName):
    checkPdfFile(pdfName)
    tempDir = os.path.abspath(tempfile.mkdtemp())
    # Fetching images...

    with wand.image.Image(filename=pdfName, resolution=220) as original:
        with original.convert('png') as imgs:
            i = 0
            for imgi in imgs.sequence:
                img = wand.image.Image(image=imgi)
                img.background_color = Color("white")
                img.alpha_channel = 'remove'
                img.save(filename = tempDir  + '/'+ str(i) + '.png')
                i += 1
    images = sorted([f for f in listdir(tempDir)])
    return images, tempDir

def getOCR():
    try:
        tool = (pyocr.get_available_tools())[0] # FIX
                                    # should try to get tesseract
                                    # even if there are other tools
        return tool
    except:
        shutil.rmtree(tempDir)
        raise NoTesseractError

def convertImgPdfPageProcess(chPipe, pageImg, tool, builder):
    txt = tool.image_to_string(
        PIL.Image.open(pageImg),
        lang="spa", builder=builder)
    chPipe.send(txt)
    chPipe.close()

def convertImgPdf(pdfName):
    images, tempDir = getImagesAndTmpDir(pdfName)
    tool = getOCR()
    builder = pyocr.builders.TextBuilder()
    
    # Running tesseract-ocr over the images...
    childs = []
    pipes = []
    for img in images:
        parPipe, chPipe = Pipe()
        pageImg = tempDir  + '/'+ img
        nChild = Process(target=convertImgPdfPageProcess,
                    args=(chPipe, pageImg, tool, builder))
        childs.append(nChild)
        pipes.append(parPipe)

    for c in childs:
        c.start()
    for c in childs:
        c.join()

    returnText = ""
    for p in pipes:
        returnText = returnText + p.recv()

    shutil.rmtree(tempDir)
    return returnText


def convertImgPdf1Process(pdfName):
    images, tempDir = getImagesAndTmpDir(pdfName)
    tool = getOCR()

    builder = pyocr.builders.TextBuilder()
    returnText = ""
    # Running tesseract-ocr over the images... 
    for img in images:
        txt = tool.image_to_string(
            PIL.Image.open(tempDir  + '/'+ img),
            lang="spa", builder=builder)
        returnText = returnText + txt
    shutil.rmtree(tempDir)
    return returnText



def convertImgPdf2HTML(pdfName):
    images, tempDir = getImagesAndTmpDir(pdfName)
    tool = getOCR()

    builder = pyocr.builders.LineBoxBuilder()
    all_lines = []
    for img in images:
        line_boxes = tool.image_to_string(
            PIL.Image.open(tempDir  + '/'+ img),
            lang="spa", builder=builder)

        # list of LineBox (each box points to a list of word boxes)
        all_lines = all_lines + line_boxes

    with codecs.open("htmlOutput.html", 'w', encoding='utf-8') as file_descriptor:
        builder.write_file(file_descriptor, all_lines)
    shutil.rmtree(tempDir)

        

def convertTxtPdf(pdfName):
    checkPdfFile(pdfName)
    pdfFile = open(pdfName, 'rb')
    readPdf = PyPDF2.PdfFileReader(pdfFile)
    numberOfPages = readPdf.getNumPages()
    returnText = ""
    for i in range(numberOfPages):
        returnText = returnText + readPdf.getPage(i).extractText()
    return returnText 
    
