import re



def cleanText(txt):
    txt = re.sub('  +', '  ', txt)
    txt = re.sub('[ º.<>!\*\':]{4,}','',txt)
    txt = re.sub('( *\n){2,}', '\n\n', txt)
    return txt