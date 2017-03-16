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

def getCode(txt):
    match = re.search(r'([A-Zl][A-Zl][A-Zl]).?(\d\d\d)|([A-Zl][A-Zl1]).?(\d\d\d\d)',txt)
    print()
    if match:
        if match.group(1) is None:
            dpt = match.group(3).replace('l','I').replace('1','I')
            num = match.group(4)
        else:
            dpt = match.group(1).replace('l','I')
            num = match.group(2)
        if dpt == 'CO':
            return 35, dpt+num, ''
        elif dpt == 'EP':
            return -1, dpt+num, 'Cursos en Cooperación (carreras largas)'
        elif dpt == 'ET':
            return -1, dpt+num, 'Cursos en Cooperación (carreras cortas)'
        elif dpt == 'CI' or dpt == 'CIB':
            return 34, dpt+num, ''
        elif dpt == 'BC' or dpt == 'BCB':
            return 27, dpt+num, ''
        elif dpt == 'BO' or dpt == 'BOB':
            return 28, dpt+num, ''
        elif dpt == 'MT' or dpt == 'CMT':
            return 30, dpt+num, ''
        elif dpt == 'GC':
            return 29, dpt+num, ''
        elif dpt == 'CE' or dpt == 'CEA':
            return 31, dpt+num, ''
        elif dpt == 'CS' or dpt == 'CSA' or dpt == 'CSX' or dpt == 'CSY' or dpt == 'CSZ' or dpt == 'EGS':
            return 32, dpt+num, ''
        elif dpt == 'CC' or dpt == 'CCE':
            return 33, dpt+num, ''
        elif dpt == 'CT' or dpt == 'CTE':
            return 3, dpt+num, ''
        elif dpt == 'DA' or dpt == 'DAP' or dpt == 'DAA':
            return 37, dpt+num, ''
        elif dpt == 'EC' or dpt == 'EYC':
            return 38, dpt+num, ''
        elif dpt == 'EA' or dpt == 'EAD':
            return 39, dpt+num, ''
        elif dpt == 'FF' or dpt == 'FL':
            return 40, dpt+num, ''
        elif dpt == 'FS' or dpt == 'FSI' or dpt == 'FIS':
            return 41, dpt+num, ''
        elif (dpt == 'FC' or dpt == 'FCR' or dpt == 'FCA' or dpt == 'FCB'
                or dpt == 'FCC' or dpt == 'FCE' or dpt == 'FCF' or dpt == 'FCG'
                or dpt == 'FCH' or dpt == 'FCI' or dpt == 'FCL' or dpt == 'FCR'
                or dpt == 'FCX' or dpt == 'FCZ' or dpt == 'FCW'):
            return 42, dpt+num, ''
        elif dpt == 'ID' or dpt == 'IDM':
            return 43, dpt+num, ''
        elif (dpt == 'LL' or dpt == 'LLA' or dpt == 'LLB' or dpt == 'LLC'
                or dpt == 'LLE' or dpt == 'EGL'):
            return 44, dpt+num, ''
        elif dpt == 'MA' or dpt == 'MAT':
            return 45, dpt+num, ''
        elif dpt == 'MC' or dpt == 'MEC':
            return 46, dpt+num, ''
        elif dpt == 'PL' or dpt == 'PLC' or dpt == 'PLY':
            return 47, dpt+num, ''
        elif dpt == 'PS' or dpt == 'PRS':
            return 48, dpt+num, ''
        elif dpt == 'QM' or dpt == 'QIM':
            return 49, dpt+num, ''
        elif dpt == 'PB':
            return 50, dpt+num, ''
        elif dpt == 'TS' or dpt == 'TSX':
            return 51, dpt+num, ''
        elif dpt == 'TI':
            return 52, dpt+num, ''
        elif dpt == 'TF' or dpt == 'TFT':
            return 53, dpt+num, ''
        elif dpt == 'PG':
            return -1, dpt+num, 'Proyecto de Grado'
        elif dpt == 'TD':
            return -1, dpt+num, 'Tesis Doctoral'
        elif dpt == 'TEG':
            return -1, dpt+num, 'Trabajo Especial de Grado'
        elif dpt == 'TG':
            return -1, dpt+num, 'Trabajo de Grado'
        elif dpt == 'USB':
            return -1, dpt+num, 'Trabajo de Grado'
        else:
            return -2, dpt+num, ''
    else:
        return -3, '', ''