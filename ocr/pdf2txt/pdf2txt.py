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

from ocr.pdf2txt.txtlibs import *

from multiprocessing import Process, Pipe

class NoTesseractError(Exception):
    pass

class BadFormatError(Exception):
    pass


# Library for extracting text out of a pdf file.

def checkPdfFile(pdfName):
    tmp = open(pdfName)
    if not ("pdf" in magic.from_file(pdfName, mime=True).lower()):
        raise BadFormatError


def getSeparatePages(pdfName, pdfsDir):
    pdfFileObj = open(pdfName, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, False)

    # saves pages in pdfsDir
    for i in range(pdfReader.numPages):
        pdfWriter = PyPDF2.PdfFileWriter()
        pageObj = pdfReader.getPage(i)
        pdfWriter.addPage(pageObj)
        pdfOutput = open(pdfsDir  + '/'+ str(i) + '.pdf', 'wb')
        pdfWriter.write(pdfOutput)
        pdfOutput.close()

    return pdfReader.numPages


def getImagesAndTmpDir(pdfName):
    checkPdfFile(pdfName)
    tempDir = os.path.abspath(tempfile.mkdtemp())
    pdfsDir = os.path.abspath(tempfile.mkdtemp())

    nPages = getSeparatePages(pdfName, pdfsDir)

    for i in range(nPages):
        with wand.image.Image(filename=pdfsDir + '/' + str(i) + '.pdf', resolution=220) as original:
            with original.convert('png') as imgs:
                for imgi in imgs.sequence:
                    img = wand.image.Image(image=imgi)
                    img.background_color = Color("white")
                    img.alpha_channel = 'remove'
                    img.save(filename = tempDir  + '/'+ str(i) + '.png')
                    break

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


# Function of a process that runs OCR over an Img and sends
# the output through a pipe.
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

    returnText = cleanText(returnText)

    shutil.rmtree(tempDir)
    return returnText




# JustInCase
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
    return cleanText(returnText)


# HOCR
# Unnaceptable
def convertImgPdf2HOCR(pdfName):
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
    return cleanText(returnText)