import os
from math import *
from datetime import date, datetime, timedelta

all_cmds = []
def compileTex(cp_type='xelatex'):
    outputTex()
    if cp_type == 'xelatex' or cp_type == 'x':
        compile_type = '-xelatex'
    else:
        compile_type = '-pdf'

    compile_tool = 'latexmk -pv '+ compile_type + ' '
    absolute_tex_filename = os.path.join(os.getcwd(), tex_filename)
    os.system(compile_tool + absolute_tex_filename)

def clearTex():
    with open(tex_filename, 'w'):
        pass

def addPreamble():
    preamble_list = [
        '\\documentclass[tikz,border=0pt]{standalone}\n',
        '\\usepackage{tikz}',
        '\\usetikzlibrary{backgrounds}',
        '\\usepackage[scheme=plain]{ctex}',
        '\\newcommand{\\fs}[1]{\\fontsize{#1 pt}{0pt}\\selectfont}',
        '\\setCJKmainfont{Microsoft YaHei}',
        '\\setmainfont{Microsoft YaHei}'
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

'''
第四期视频的话，>=300w 显示封面，<=300w 只绘制点
    100w+ 4103
    200w+ 932
    300w+ 388
    400w+ 161
    500w+ 70

    天数：3287 days 
          2009.07.25-2018.07.25
    帧率：60 fps
          3287 / 60 = 54.783 = 55 sec
    时长：55 * 6 = 5.5 min = 330 sec
    帧数：3287 * 6 = 19722 frm

    精度：6 帧/天 = 4 h/帧 
    速度：10 天/秒
    
    视频点数（4102） = 天数（3287）
    阈值：100w 
        考虑到点的分布集中在后 7/9，因此
        有效帧数：19722*7/9=15340
        两个点间隔的帧数为： 15340/4103 = 3.74

    点之间要尽可能分辨出来：
        假设点的直径为 10~20 pt，可利用的屏幕宽度为 900 pt，
        那么 900/15 = 60，
        因此屏幕上同时存在的点数不应超过 60 个
        考虑到由于点的纵坐标存在差异，因此 60 个点应该足够空旷，可以考虑增加到 100个
    如果按照同屏不能超过 100 个计算的话：
        同屏的帧数为：3.74 * 100 = 374
        用时：374/60 = 6.23 秒
        对应数据走过时长为：374/6 = 62.3 天 = 2 月
        嗯，这个值还是比较合理的
        需要留出一定的调整空间，因此同屏的现实时长范围约为 1-3 月
'''
date_all = []

video_all = []
video_onscreen = [] # obj: info, x, y, color
video_active = []

date_head = date(2009, 7, 30)
date_tail = date(2018, 7, 25)
def initDate():
    global date_all
    date_delta = date_tail - date_head

    for i in range(date_delta.days + 1):
        current_date = date_head + timedelta(days=i)
        for j in range(0, 6):
            date_obj_tmp = {}
            date_obj_tmp['year']  = current_date.year
            date_obj_tmp['month'] = current_date.month
            date_obj_tmp['day']   = current_date.day
            date_obj_tmp['hour']  = 4*(j+1)
            date_all.append(date_obj_tmp)

ptr_left = 0
ptr_righ = 0

def compareDate(date1, date2):
    # -1 A before B
    #  0 A equal  B
    #  1 A after  B
    if   date1['year'] <  date2['year']:
        return -1
    elif date1['year'] >  date2['year']:
        return  1
    else:
        if   date1['month'] <  date2['month']:
            return -1
        elif date1['month'] >  date2['month']:
            return  1
        else:
            if   date1['day'] <  date2['day']:
                return -1
            elif date1['day'] <  date2['day']:
                return  1
            else:
                if   date1['hour'] <  date2['hour']:
                    return -1
                elif date1['hour'] <  date2['hour']:
                    return  1
                else:
                    return  0

date_onscreen = []

cover_x, cover_y = 920, 50
cover_w, cover_h = 350, 350*9/16

axis_l, axis_r = 100, cover_x-50
axis_b, axis_t = 100, 600

initDate()
def updateDateOnscreen(ptr_righ):
    global date_onscreen

    if ptr_righ >= 381:
        date_onscreen.pop(0)
        ptr_left = ptr_righ-380
    else:
        ptr_left = 0

    current_date = date_all[ptr_righ]
    date_onscreen.append(current_date)

    tmp_cmds = []
    tmp_cmds.extend([
        '\\draw [line width=2pt, gray]  ({0},{2}) -- ({1},{2});'.format(axis_l, axis_r+50,axis_b,axis_t),
        '\\draw [line width=2pt, gray]  ({0},{2}) -- ({0},{3});'.format(axis_l, axis_r,axis_b,axis_t),
        '\\draw [line width=2pt, green, opacity=0.5] ({0},{1}) -- ({0},{2});'.format(axis_r,axis_b,axis_t),
        '\\node [text=white, align=right, font=\\fs{{20}}] at ({0},{1}) {{ {2} 年 {3:0>2d} 月 {4:0>2d} 日 }};' \
            .format(1100, 680, current_date['year'], current_date['month'], current_date['day'])
        ])

    cnt = 0
    for date_tmp in date_onscreen:
        if (date_tmp['day']==1) and (date_tmp['hour']==4):
            date_tmp_x = axis_l + (axis_r-axis_l)*(1-(len(date_onscreen)-1-cnt)/381)
            tmp_cmds.extend([
                '\\node [text=white, align=center, font=\\fs{{15}}] at ({0},{1}) {{ {2}-{3:0>2d} }};' \
                    .format(date_tmp_x, axis_b-20, date_tmp['year'], date_tmp['month'])
                ])
        cnt +=1

    printTex(tmp_cmds)

def drawCover():
    tmp_cmds = [
        # '\\fill [green,radius={}] ({},{}) circle;'.format(radius,80+80*sin(i*0.2),80+80*cos(i*0.2)),
        '\\fill [yellow, opacity=0.8] ({},{}) rectangle ({}, {});'.format(cover_x, cover_y, cover_x+cover_w, cover_y+cover_h)
    ]
    printTex(tmp_cmds)

if __name__ == '__main__':
    # initDate()
    # for i in range(0, 40):
    #     axisDate(i)
    #     print('{} {} {} {:02d}'.format(*list(map(lambda x:date_onscreen[-1][x], ['year', 'month','day','hour']))))

# '''
    tex_filename = 'ani_view.tex'

    clearTex()
    addPreamble()
    beginDoc()
    for i in range(0, 400):
        beginTikz()

        # width, height = 1920+7, 1080+4
        width, height = 1280+5, 720+3
        setSize(width, height, 'lb')
        radius = 10

        updateDateOnscreen(i)
        drawCover()

        endTikz()
    endDoc()
    compileTex()
# '''