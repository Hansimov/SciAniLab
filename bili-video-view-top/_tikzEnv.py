import os
from math import *
from datetime import date, datetime, timedelta

tex_filename = 'ani_view.tex'
all_cmds = []

def compileTex(cp_type='xelatex'):
    if cp_type == 'xelatex' or cp_type == 'x':
        compile_type = '-xelatex'
    else:
        compile_type = '-pdf'

    # compile_limits = ' -pool-size=7999999 -main-memory=7999999 '
    compile_limits = ' -pool-size=7999999 -extra-mem-top=20000000 -extra-mem-bot=20000000'
    compile_tool = 'latexmk -pv '+ compile_limits + ' ' + compile_type + ' '
    absolute_tex_filename = os.path.join(os.getcwd(), tex_filename)
    os.system(compile_tool + absolute_tex_filename)

def clearTex():
    with open(tex_filename, 'w'):
        pass

def addPreamble():
    preamble_list = [
        '\\documentclass[tikz,border=0pt]{standalone}\n',
        '\\usepackage{tikz}',
        '\\usetikzlibrary{calc}',
        '\\usepackage{amssymb}',
        '\\usepackage{bm}',
        '\\usetikzlibrary{backgrounds}',
        '\\usepackage[scheme=plain]{ctex}',
        # '\\usepackage[UTF8]{ctex}',
        # '\\usepackage{fontspec, xunicode, xltxtra}',
        # '\\usepackage[utf8]{inputenc}',
        # '\\usepackage[T1]{fontenc}',
        '\\newfontfamily\\hupo{STXingkai}',
        '\\setCJKfamilyfont{hwhp}{STXingkai}',
        '\\newcommand{\\hupozh}{\\CJKfamily{hwhp}}',
        '\\newcommand{\\fs}[1]{\\fontsize{#1}{0pt}\\selectfont}',
        '\\setCJKmainfont{Microsoft YaHei}',
        '\\CJKsetecglue{\\hskip0.05em plus0.05em minus 0.05em}',
        # '\\setmainfont{Microsoft YaHei}'，
        '\\setmainfont{Arial Unicode MS}',
    ]
    printTex(preamble_list)

def beginDoc(doctype='standalone'):
    printTex('\\begin{document}\n')

def endDoc():
    printTex('\n\\end{document}')

def beginTikz():
    begin_tikz = [
        '\\begin{tikzpicture}',
        '[',
        'x=1pt,y=1pt,',
        'background rectangle/.style={fill=black},',
        'show background rectangle,',
        # 'scale=1.5',
        ']\n'
    ]

    printTex(begin_tikz)

def endTikz():
    printTex('\n\\end{tikzpicture}\n')

def printTex(commands):
    global all_cmds
    if isinstance(commands, str):
        all_cmds.append(commands)
    elif isinstance(commands, list):
        for line in commands:
            all_cmds.append(line)

def outputTex():
    global all_cmds
    with open(tex_filename, 'a', encoding='utf-8') as txf:
        for line in all_cmds:
            print(line, file=txf)

def setSize(width, height, anchor='lb'):
    # anchor is the center of the origin point of the bounding box
    #   - left right up bottom center
    #   - l,r,u,b, lu, lb, ru, rb, c
    if   anchor == 'c':
        set_size = [
            '\\useasboundingbox (-{0:}, -{1:}) rectangle ({0:}, {1:});'.format(width/2,height/2),
        ]
    elif anchor == 'lb':
        set_size = [
            '\\path[clip] (0, 0) rectangle ({0:}, {1:});'.format(width,height),
        ]
    else: # TODO
        set_size = [
            '\\useasboundingbox (0, 0) rectangle ({0:}, {1:});'.format(width,height),
        ]
    printTex(set_size)