import re

def cleanText(txt):
    txt = re.sub('  +', '  ', txt)
    txt = re.sub('[ º.<>!\*\':]{4,}','',txt)
    txt = txt + "\n\n\n"
    txt = re.sub('( *\n){3,}', '\n\n\n', txt)
    return txt

def htmlParagraph(par):
    return '<p>\n' + par.group(0) + '<\p>\n'

def txt2HTML(txt):
    txt = re.sub('>', '\>', txt)
    txt = re.sub('<', '\<', txt)
    txt = re.sub('([^\n]+\n{0,2})+\n\n\n', htmlParagraph, txt)
    return txt