import re

def cleanText(txt):
    txt = re.sub('  +', '  ', txt)
    txt = re.sub('[ º.<>!\*\':]{4,}','',txt)
    txt = txt + "\n\n\n"
    txt = re.sub('( *\n){3,}', '\n\n\n', txt)
    return txt

def htmlParagraph(par):
    return '<p>\n' + par.group(0)[:-2] + '<\p>\n'

def txt2HTML(txt):
    txt = re.sub('>', '\>', txt)
    txt = re.sub('<', '\<', txt)
    txt = re.sub('([^\n]+\n{0,2})+\n\n\n', htmlParagraph, txt)
    return txt


def cleangs(txt):
    txt = re.sub('\nPage \d+\n', '\n', txt)
    txt = re.sub('\n        ', '\n', txt)
    txt = re.sub('GPL Ghostscript[^\n]+\n', ' ', txt)
    txt = re.sub('Copyright \(C\) 2015 Artifex[^\n]+\n', ' ', txt)
    txt = re.sub('Processing pages [^\n]+\n', ' ', txt)
    txt = re.sub('This software comes with[^\n]+\n', ' ', txt)
    txt = re.sub('Can\'t find \(o[^\n]+\n', ' ', txt)
    txt = re.sub('Querying operating syste[^\n]+\n', ' ', txt)
    txt = re.sub('Loading [^\n]+\n', ' ', txt)

    return txt