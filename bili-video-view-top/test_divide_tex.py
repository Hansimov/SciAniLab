import os
import time
import threading
from math import *

all_cmds = []

preamble = [
    '\\documentclass[tikz,border=0pt]{standalone}\n',
    '\\usepackage{tikz}',
    '\\usepackage[skins]{tcolorbox}',
    '\\usepackage{graphicx}',
    # '\\usepackage{calc}',
    '\\usetikzlibrary{calc}',
    '\\usepackage{amssymb}',
    '\\usepackage{bm}',
    '\\usetikzlibrary{backgrounds}',
    '\\usepackage[scheme=plain]{ctex}',
    # '\\usepackage{ctexcap}',
    # '\\newfontfamily\\hupo{STXingkai}',
    # '\\setCJKfamilyfont{hwhp}{STXingkai}',
    # '\\newcommand{\\hupozh}{\\CJKfamily{hwhp}}',
    '\\newcommand{\\fs}[1]{\\fontsize{#1}{0pt}\\selectfont}',
    '\\setCJKmainfont{Microsoft YaHei}',
    '\\CJKsetecglue{\\hskip0.05em plus0.05em minus 0.05em}',
    '\\ctexset{space=true}',
    # '\\setmainfont{Microsoft YaHei}',
    '\\setmainfont{Arial Unicode MS}',
    # '\\setmainfont{FreeSerif}',
]

# Some other not common commands
preamble.extend([
    '''
    \\newcommand\\shadetext[2][]{%
    \\setbox0=\\hbox{{\\special{pdf:literal 7 Tr }#2}}%
    \\tikz[baseline=0]\\path [#1] \\pgfextra{\\rlap{\\copy0}} (0,-\\dp0) rectangle (\\wd0,\\ht0);%
    }
    '''
])

begin_doc = ['\\begin{document}\n']
end_doc   = ['\n\\end{document}']

begin_tikz = [
    '\\begin{tikzpicture}',
    '[',
    'x=1pt,y=1pt,',
    'background rectangle/.style={fill=black},',
    'show background rectangle,',
    # 'scale=1.5',
    ']\n'
]

end_tikz = '\n\\end{tikzpicture}\n'

def clearTex(tex_filename):
    with open(tex_filename, 'w'):
        pass

def printTex(commands):
    global all_cmds
    if isinstance(commands, str):
        all_cmds.append(commands)
    elif isinstance(commands, list):
        for line in commands:
            all_cmds.append(line)

def outputTex(tex_filename, parts=1, compilex=True, threads=1):
    global all_cmds
    if parts == 1:
        selected_cmds = all_cmds

        part_cmds = []
        part_cmds.extend(preamble)
        part_cmds.extend(begin_doc)
        part_cmds.extend(selected_cmds)
        part_cmds.extend(end_doc)

        with open(tex_filename, 'a', encoding='utf-8') as txf:
            for line in part_cmds:
                print(line, file=txf)
        if compilex == True:
            compileTex(tex_filename)
    else:
        frame_row_bgn = []
        frame_row_end = []

        frame_cnt, row_num = 0, 0
        for row in all_cmds:
            row = row.strip('\n')
            if row == '\\begin{tikzpicture}':
                frame_row_bgn.append([frame_cnt, row_num])
            if row == '\\end{tikzpicture}':
                frame_row_end.append([frame_cnt, row_num])
                frame_cnt += 1

            row_num += 1

        tex_filename_list = []
        frame_cnt_each_part = ceil(frame_cnt/parts)
        bgn_frame_cnt, end_frame_cnt = 0, -1
        for i in range(0, parts):
            bgn_frame_cnt = end_frame_cnt + 1
            if i < parts-1:
                end_frame_cnt = bgn_frame_cnt + frame_cnt_each_part - 1
            else:
                end_frame_cnt = frame_cnt - 1

            bgn_row_num = frame_row_bgn[bgn_frame_cnt][1]
            end_row_num = frame_row_end[end_frame_cnt][1]
            print(bgn_frame_cnt, bgn_row_num, end_frame_cnt, end_row_num)

            selected_cmds = all_cmds[bgn_row_num : end_row_num+1]

            part_cmds = []
            part_cmds.extend(preamble)
            part_cmds.extend(begin_doc)
            part_cmds.extend(selected_cmds)
            part_cmds.extend(end_doc)

            tex_filename_tmp = os.path.splitext(tex_filename)[0] + '_{:0>4d}'.format(i+1) + '.tex'
            tex_filename_list.append(tex_filename_tmp)
            clearTex(tex_filename_tmp)
            with open(tex_filename_tmp, 'a', encoding='utf-8') as txf:
                for line in part_cmds:
                    print(line, file=txf)
        if compilex == True:
            threads_cnt_max = min(threads, parts)
            semlock = threading.BoundedSemaphore(threads_cnt_max)
            compile_tex_list=[]
            for tex_filename_tmp in tex_filename_list:
                semlock.acquire()
                compile_tex_tmp = threading.Thread(target=compileTex, args=(tex_filename_tmp,), kwargs={'multithreads':True, 'semlock':semlock})
                compile_tex_list.append(compile_tex_tmp)
                compile_tex_tmp.start()

def compileTex(tex_filename, engine='xelatex', preview=True, multithreads=False, semlock={}):
    if engine == 'xelatex' or engine == 'x':
        engine_cfg = '-xelatex'
    else:
        engine_cfg = '-pdf'

    if preview == True:
        preview_cfg = '-pv'
    else:
        preview_cfg = ''

    compile_limits = ' -pool-size=7999999 -extra-mem-top=20000000 -extra-mem-bot=20000000'

    compile_tool = ' '.join(('latexmk', preview_cfg, compile_limits, engine_cfg, ' '))
    absolute_tex_filename = os.path.join(os.getcwd(), tex_filename)
    os.system(compile_tool + absolute_tex_filename)

    if multithreads == True:
        semlock.release()


def addPreamble():
    printTex(preamble)

def beginDoc():
    printTex(begin_doc)

def endDoc():
    printTex(end_doc)

def beginTikz():
    printTex(begin_tikz)

def endTikz():
    printTex(end_tikz)

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


if __name__ == '__main__':
    
    width_local, height_local = 1280+5, 720+3
    # global all_cmds
    all_cmds = []
    tex_filename = 'test_divide.tex'
    t1 = time.time()

    for i in range(0, 10):
        beginTikz()
        setSize(width_local, height_local, 'lb')

        all_cmds.extend([
            '\\node [text=white, font=\\fs{{30}}, anchor=center, align=center] at ({},{}) {{{}}};'\
                .format(width_local/2, height_local/2, i)
        ])

        endTikz()

    outputTex(tex_filename, parts=4, threads=3)

    t2 = time.time()
    dt1 = t2 - t1
    print('Elapsed time 1: {:.7} s'.format(dt1))