# drawViewAxis
# drawDateAxis
# drawViewPoint

import os
from math import *
from datetime import *

import pandas as pd
import time

# tex_filename = 'global_view.tex'
all_cmds = []

# width, height = 1920+7, 1080+4
# width, height = 1280+5, 720+3
width, height = 1280*8, 720+3

axis_l, axis_r = 25, width - 25
axis_b, axis_t = 70, 650

date_axis_segs = 200

video_view_threshold = 1e6

date_head = datetime(2009, 6, 24, 0, 0, 0)
date_tail = datetime(2018, 8, 21, 0, 0, 0)
total_seconds_max = (date_tail - date_head).total_seconds()


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

def outputTex(tex_filename):
    global all_cmds
    with open(tex_filename, 'a', encoding='utf-8') as txf:
        for line in all_cmds:
            print(line, file=txf)

def compileTex(tex_filename, engine='xelatex', preview=True):
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

def addPreamble():
    preamble_list = [
        '\\documentclass[tikz,border=0pt]{standalone}\n',
        '\\usepackage{tikz}',
        '\\usepackage[skins]{tcolorbox}',
        '\\usepackage{graphicx}',
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
        # '\\setmainfont{Microsoft YaHei}',
        '\\setmainfont{Arial Unicode MS}',
        # '\\setmainfont{FreeSerif}',
    ]

    # Some other not common commands
    preamble_list.extend([
        '''
        \\newcommand\\shadetext[2][]{%
        \\setbox0=\\hbox{{\\special{pdf:literal 7 Tr }#2}}%
        \\tikz[baseline=0]\\path [#1] \\pgfextra{\\rlap{\\copy0}} (0,-\\dp0) rectangle (\\wd0,\\ht0);%
        }
        '''
    ])
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

def logisticX(base=2, val=0, offset=0, ratio=1):
    # map [0, +∞] to [0, 1]
    return 2*(1/(1+base**(-(val-offset)/ratio))-0.5)

def escChar(texstr):
    # char_macro = ['~', '^', '\\']
    texstr = texstr.replace('\\','\\textbackslash ')
    # Put all after backslash
    texstr = texstr.replace('~','\\textasciitilde ')
    texstr = texstr.replace('^','\\textasciicircum ')

    char_slash = ['&', '%', '$', '#', '_', '{', '}']
    for char in char_slash:
        texstr = texstr.replace(char, '\\'+char+' ')

    return texstr

rgnclr = {} # region color

rgnclr['donghua']  = [0.6, 0.4, 0.9] # 动画
rgnclr['yinyue']   = [ 1 ,  1 ,  0 ] # 音乐
rgnclr['wudao']    = [ 1 , 0.4,  0 ] # 舞蹈
rgnclr['youxi']    = [ 1 , 0.1, 0.1] # 游戏
rgnclr['keji']     = [ 0 , 0.4,  1 ] # 科技
rgnclr['shenghuo'] = [ 0 , 0.5,  0 ] # 生活
rgnclr['guichu']   = [0.5,  1 ,  1 ] # 鬼畜
rgnclr['yingshi']  = [ 1 , 0.5,  1 ] # 影视
# rgnclr['yule']     = [ 1 , 0.5,  1 ] # 娱乐
# rgnclr['guanggao'] = [ 1 , 0.5,  1 ] # 广告
rgnclr['qita']     = [0.5, 0.5, 0.5] # 其他

rgnname = ['动画','音乐','舞蹈','游戏','科技','生活','鬼畜','影视','其他']
rgnpinyin = ['donghua','yinyue','wudao','youxi','keji','shenghuo','guichu','yingshi','qita']

class VideoPoint(object):
    @property
    def tid(self):
        return self._tid
    @tid.setter
    def tid(self, val):
        self._tid = val
        self.calcRegion()

    @property
    def view_avg(self):
        return self._view_avg
    @view_avg.setter
    def view_avg(self, val):
        self._view_avg = val
        self.calcRadius()

    def calcRadius(self):
        self.radius = round(20 * logisticX(base=1.3, val=self.view_avg, ratio=video_view_threshold/2), 2)

    def calcRegion(self):
        # 动画：动画 + 番剧 + 国创
        if  self.tid in [  1, 24, 25, 47, 27, 13, 33, 32, 51, 152,
                         167, 153, 168, 169, 170,  46, 53]:
            self.region = 'donghua'
        # 音乐
        elif self.tid in [3, 28, 31, 30, 59, 29, 54, 130]:
            self.region = 'yinyue'
        # 舞蹈
        elif self.tid in [129, 20, 154, 156]:
            self.region = 'wudao'
        # 游戏
        elif self.tid in [4, 17, 171, 172, 65, 173, 121, 136, 19,  67]:
            self.region = 'youxi'
        # 科技
        elif self.tid in [36, 124, 122, 39, 96, 95, 98, 176]:
            self.region = 'keji'
        # 生活
        elif self.tid in [160, 138, 21, 76, 75, 161, 162, 175, 163, 174,  74]:
            self.region = 'shenghuo'
        # # 娱乐（+时尚）
        # elif self.tid in [155, 157, 158, 164, 159,  5, 71, 137, 131,  134]:
        #     self.region = 'yule'
        # 鬼畜
        elif self.tid in [119, 22, 26, 126, 127]:
            self.region = 'guichu'
        # 影视
        elif self.tid in [181, 182, 183, 85, 184, 86]:
            self.region = 'yingshi'
        ## 放映厅
        # elif self.tid in [177, 37, 178, 179, 180,  23, 147, 145, 146, 83,  11, 185, 187]:
        #     self.region = 'fangyingting'
        # # 广告
        # elif self.tid in [165, 166]:
        #     self.region = 'guanggao'
        # 其他：娱乐 + 广告 + 影视 + 时尚 + 放映厅
        else:
            self.region = 'qita'

        self.color = rgnclr[self.region]

    def display(self):
        tmp_cmds = [
            '\\node [fill={{rgb,1: red,{}; green,{}; blue,{}}}, shape=circle, minimum size={}, opacity=0.8] ({}) at ({},{}) {{}};' \
                .format(self.color[0], self.color[1], self.color[2], 2*self.radius, self.aid, self.x, self.y),
        ]
        printTex(tmp_cmds)

video_all = []
# df = pd.read_csv('./data/view_gt100w_latest_out.csv', sep=',')
df = pd.read_csv('./data/view_gt100w_180826x_out.csv', sep=',')
def initVideo():
    global video_all
    # view, videos, view_avg, title, coin, favorite, danmaku, aid, name, mid, pubdate, tid, duration, copyright, pic, face
    # add property of video point
    for i in range(len(df)):
        video_tmp = VideoPoint()
        video_tmp.view     = int(df['view'][i])
        video_tmp.videos   = int(df['videos'][i])
        # video_tmp.view_avg = int(df['view_avg'][i])
        video_tmp.view_avg = int(df['view'][i])
        # video_tmp.favorite = int(df['favorite'][i])
        # video_tmp.coin     = int(df['coin'][i])
        # video_tmp.danmaku  = int(df['danmaku'][i])

        video_tmp.title    = str(df['title'][i])
        video_tmp.aid      = int(df['aid'][i])
        video_tmp.tid      = int(df['tid'][i])
        # video_tmp.name     = str(df['name'][i])
        # video_tmp.mid      = int(df['mid'][i])
        # video_tmp.pic      = str(df['pic'][i])
        # video_tmp.face     = str(df['face'][i])

        video_tmp.pubdate  = datetime.strptime(df['pubdate'][i], '%Y/%m/%d %H:%M:%S')

        video_tmp.x = axis_l + (axis_r-axis_l) * (video_tmp.pubdate-date_head).total_seconds()/total_seconds_max
        video_tmp.y = axis_b + (axis_t-axis_b) * logisticX(base=1.3, val=video_tmp.view_avg, offset=0.8e6, ratio=video_view_threshold/2)
        video_tmp.x, video_tmp.y = round(video_tmp.x, 2), round(video_tmp.y, 2)

        video_all.append(video_tmp)
initVideo()

def drawDateAxis():
    date_bgn = date_head.date()
    date_end = date_tail.date()
    date_delta_all = (date_end-date_bgn).days

    tmp_cmds = []
    for i in range(0, date_delta_all + 1):
        date_tmp = date_bgn + timedelta(days=i)
        # print(date_tmp)

        if date_tmp.day == 1:
            date_tmp_x = axis_l + (axis_r-axis_l) * (date_tmp-date_bgn).days/date_delta_all
            date_tmp_x = round(date_tmp_x, 2)
            tmp_cmds.extend([
                '\\node [text=white, align=center, font=\\fs{{15}}] at ({0},{1}) {{ {2}-{3:0>2d} }};' \
                    .format(date_tmp_x, axis_b-30, date_tmp.year, date_tmp.month),
                '\\draw [white,line width=2] ({0},{1}) -- ({0}, {2});'.format(date_tmp_x, axis_b-10, axis_b+10)
            ])
    printTex(tmp_cmds)

# ===================================================================
def drawGlobalViewRaw():
    global all_cmds
    all_cmds = []
    tex_filename = 'ending_global_view_raw.tex'
    t1 = time.time()
    clearTex(tex_filename)
    addPreamble()
    beginDoc()

    beginTikz()
    setSize(width, height, 'lb')

    drawDateAxis()

    for video in video_all:
        video.display()

    endTikz()
    endDoc()

    outputTex(tex_filename)
    compileTex(tex_filename)
    t2 = time.time()
    dt1 = t2 - t1
    print('Elapsed time 1: {:.7} s'.format(dt1))


# ===================================================================
width_local, height_local = 1280+5, 720+3

def shiftGlobalView(shift_x):
    tmp_cmds = []
    tmp_cmds.extend([
        '\\node [anchor=west] at ({},{}) {{ \\includegraphics {{global_view.pdf}} }};' \
            .format(round(width_local-shift_x, 2), round(height_local/2, 2))
    ])
    printTex(tmp_cmds)

def zoomGlobalView(zoom_x):
    tmp_cmds = []
    tmp_cmds.extend([
        '\\node [anchor=east] at ({},{}) {{ \\includegraphics [width={}pt] {{global_view.pdf}} }};' \
            .format(round(width_local, 2), round(height_local/2, 2), round(zoom_x, 2))
    ])
    printTex(tmp_cmds)

def drawGlobalViewAll():
    drawGlobalViewRaw()
    global all_cmds
    all_cmds = []

    tex_filename = 'ending_global_view_all.tex'
    t1 = time.time()
    clearTex(tex_filename)
    addPreamble()
    beginDoc()

    shift_frames_cnt = 60 * 5
    # shift_x_step = (width + width_local)/shift_frames_cnt
    shift_x_step = width / shift_frames_cnt

    for i in range(0, shift_frames_cnt):
        beginTikz()
        setSize(width_local, height_local, 'lb')

        shift_x = shift_x_step * i
        shiftGlobalView(shift_x)
        endTikz()

    zoom_frames_cnt = 60 * 2
    # width_of_includegraphics: width -> width_local
    for i in range(0, zoom_frames_cnt+1):
        beginTikz()
        setSize(width_local, height_local, 'lb')

        zoom_x = width - (width - width_local) * i /zoom_frames_cnt
        zoomGlobalView(zoom_x)

        endTikz()

    endDoc()
    outputTex(tex_filename)
    compileTex(tex_filename)
    t2 = time.time()
    dt1 = t2 - t1
    print('Elapsed time 1: {:.7} s'.format(dt1))

# ===================================================================
def drawRegionViewRaw():
    global all_cmds
    all_cmds = []
    tex_filename = 'ending_region_view_raw.tex'
    t1 = time.time()
    clearTex(tex_filename)
    addPreamble()
    beginDoc()

    for rgnpinyin_tmp in rgnpinyin:
        beginTikz()
        setSize(width, height, 'lb')
        drawDateAxis()

        for video in video_all:
            if video.region == rgnpinyin_tmp:
                video.display()
        endTikz()

    endDoc()

    outputTex(tex_filename)
    compileTex(tex_filename)
    t2 = time.time()
    dt1 = t2 - t1
    print('Elapsed time 1: {:.7} s'.format(dt1))


# ===================================================================
def drawRegionSeperate():
    # draw seperate region
    tmp_cmds = []
    for i in range(0, len(rgnname)):
        rgnpinyin_tmp = rgnpinyin[i]
        rgnname_tmp = rgnname[i]
        rgnclr_tmp = rgnclr[rgnpinyin_tmp]

        beginTikz()
        setSize(width_local, height_local, 'lb')

        tmp_cmds.extend([
            '\\node [anchor=center] at ({},{}) {{ \\includegraphics [page={}, width={}pt] {{region_view.pdf}} }};' \
                .format(round(width_local/2,2), round(height_local/2, 2), i+1, width_local),
            '\\node [text={{rgb,1: red,{}; green,{}; blue,{}}}, font=\\fs{{35}}] at ({},{}) {{ {} }};'\
                .format(rgnclr_tmp[0], rgnclr_tmp[1], rgnclr_tmp[2], round(width_local/10,2), round(height_local/2, 2), rgnname_tmp)
        ])
        printTex(tmp_cmds)
        tmp_cmds = []

        endTikz()

def drawRegionCombination():
    # draw all region
    tmp_cmds = []
    beginTikz()
    setSize(width_local, height_local, 'lb')
    for i in range(0, len(rgnname)):
        rgnpinyin_tmp = rgnpinyin[i]
        rgnname_tmp = rgnname[i]
        rgnclr_tmp = rgnclr[rgnpinyin_tmp]

        height_per = round(height_local/len(rgnname), 2)
        x_tmp = round(width_local/2,2)
        y_tmp = round(height_local - i * (height_local/len(rgnname)) - height_per/2, 2)
        tmp_cmds.extend([
            '\\node [anchor=center] at ({},{}) {{ \\includegraphics [page={}, height={}pt] {{region_view.pdf}} }};' \
                .format(x_tmp, y_tmp, i+1, height_per),
            '\\node [text={{rgb,1: red,{}; green,{}; blue,{}}}, font=\\fs{{35}}] at ({},{}) {{ {} }};'\
                .format(rgnclr_tmp[0], rgnclr_tmp[1], rgnclr_tmp[2], round(width_local/10,2), y_tmp, rgnname_tmp)
        ])
    printTex(tmp_cmds)
    endTikz()

def drawSumOfVideos():
    tmp_cmds = []
    beginTikz()
    setSize(width_local, height_local, 'lb')
    tmp_cmds.extend([
            '\\tikzstyle{{shadecolor}}=[left color={{rgb,1: red,{}; green,{}; blue,{}}}, middle color={{rgb,1: red,{}; green,{}; blue,{}}}, right color={{rgb,1: red,{}; green,{}; blue,{}}}, shading angle=45];' \
            .format(rgnclr['youxi'][0], rgnclr['youxi'][1], rgnclr['youxi'][2],\
                    rgnclr['guichu'][0], rgnclr['guichu'][1], rgnclr['guichu'][2],\
                    rgnclr['shenghuo'][0], rgnclr['shenghuo'][1], rgnclr['shenghuo'][2]),
        '\\node [text=white, anchor=center, align=center, font=\\fs{{38}}] (comp) at ({},{}) {{ 截至 2018 年 08 月 26 日 \\\\[40pt] 播放数超过100万的用户原创视频 \\\\[40pt] 共计 \\shadetext[shadecolor] {{{}}} 个 }} ;' .format(round(width_local/2,2), round(height_local/2+40, 2), len(video_all)),
    ])
    printTex(tmp_cmds)
    endTikz()

def drawRegionChart():
    tmp_cmds = []
    beginTikz()
    setSize(width_local, height_local, 'lb')

    origin_x = width_local/4
    origin_y = height_local/3 + 40

    tmp_cmds.extend([
        '\\node [text=white, anchor=center, align=center, font=\\fs{{38}}] (comp) at ({},{}) {{ 各分区对比 }} ;' \
            .format(round(width_local/2,2), round(height_local*6/7, 2)),
        # '\\node [text=white, anchor=north, align=center, font=\\fs{{20}}, yshift=-10pt] at (comp.south) {{ （播放数超过100万的用户原创视频共计{}个） }} ;' \
        #     .format(len(video_all))
        '\\tikzstyle{{shadecolor}}=[left color={{rgb,1: red,{}; green,{}; blue,{}}}, middle color={{rgb,1: red,{}; green,{}; blue,{}}}, right color={{rgb,1: red,{}; green,{}; blue,{}}}, shading angle=45];' \
            .format(rgnclr['youxi'][0], rgnclr['youxi'][1], rgnclr['youxi'][2],\
                    rgnclr['guichu'][0], rgnclr['guichu'][1], rgnclr['guichu'][2],\
                    rgnclr['shenghuo'][0], rgnclr['shenghuo'][1], rgnclr['shenghuo'][2]),
        '\\node [anchor=center, align=center, font=\\fs{{40}}] at ({},{}) {{ \\shadetext[shadecolor] {{{}}} }};' \
            .format(origin_x, origin_y, len(video_all))
    ])

    # calc ratio pie chart
    video_num = 0
    view_num_list = [0] * len(rgnname)
    for video_tmp in video_all:
        rgn_idx = rgnpinyin.index(video_tmp.region)
        view_num_list[rgn_idx] += 1
        video_num += 1
        # if video_tmp.region == 'qita':
        #     print(video_tmp.tid, video_tmp.aid, video_tmp.title)

    ratio_list = [0] * len(rgnname)
    for i in range(0, len(ratio_list)):
        ratio_list[i] = round(view_num_list[i]/video_num, 4)

    # calc rank bar chart
    ratio_list_sorted = ratio_list.copy()
    ratio_list_sorted.sort(reverse=True)

    order_list = [0] * len(rgnname)
    for i in range(0, len(ratio_list)):
        order_list[i] = ratio_list_sorted.index(ratio_list[i])
        # print(rgnname[i], ratio_list[i], order_list[i])

    radius_outer = 180
    radius_inner = 120
    text_dist = 245
    ang_bgn = 0

    for i in range(0, len(rgnname)):
        rgnclr_tmp = rgnclr[rgnpinyin[i]]
        rgnname_tmp = rgnname[i]
        ratio_tmp = round(ratio_list[i] * 100, 2)
        ang_val = round(ratio_list[i] * 360, 2)
        ang_end = round(ang_bgn + ang_val, 2)
        ang_mid = round((ang_bgn+ang_end)/2, 2)

        bar_x = round(width_local/2 + 200, 2)
        bar_y = round(3/4*height_local-40 - order_list[i] * 50, 2)
        bar_w = round(ratio_list[i]/ratio_list_sorted[0] * 300, 2)
        bar_h = 35

        rect_id = 'rect'+str(i)

        if   rgnpinyin[i] == 'yinyue':
            correct_x, correct_y = 10, -10
        elif rgnpinyin[i] == 'youxi':
            correct_x, correct_y = -10, 0
        else:
            correct_x, correct_y = 0, 0

        tmp_cmds.extend([
            # draw ratio pie chart
            '\\tikzstyle{{fillcolor}}=[fill={{rgb,1:red,{}; green,{}; blue,{}}}];' \
                .format(rgnclr_tmp[0], rgnclr_tmp[1], rgnclr_tmp[2]),
            '\\tikzstyle{{textcolor}}=[text={{rgb,1:red,{}; green,{}; blue,{}}}];' \
                .format(rgnclr_tmp[0], rgnclr_tmp[1], rgnclr_tmp[2]),
            '\\path [fillcolor, shift={{({},{})}}] (0,0) -- ({}:{}) arc ({}:{}:{}) -- ({}:{}) arc ({}:{}:{});'\
                .format(round(origin_x,2), round(origin_y,2), \
                        ang_bgn, radius_outer, ang_bgn, ang_end, radius_outer, \
                        ang_end, radius_inner, ang_end, ang_bgn, radius_inner),
            '\\node [textcolor, shift={{({},{})}}, font=\\fs{{25}}, align=center, anchor=center] at ({}:{}) {{{} \\\\[10pt] {}\\%}};'\
                .format(round(origin_x+correct_x,2), round(origin_y+correct_y,2), \
                        ang_mid, text_dist, rgnname_tmp, ratio_tmp),
            # draw rank bar chart
            '\\node [fillcolor, minimum width={}pt, minimum height={}pt, shape=rectangle, anchor=west, xshift=-30pt, inner sep=0pt] ({}) at ({},{}) {{}};' \
                .format(bar_w, bar_h, rect_id, bar_x, bar_y),
            '\\node [textcolor, anchor=east, font=\\fs{{25}}, align=right, xshift=-10pt] at ({}.west) {{{} {}}};' \
                .format(rect_id, order_list[i]+1, rgnname[i]),
            '\\node [textcolor, anchor=west, font=\\fs{{20}}, align=left, xshift=5pt] at ({}.east) {{{} ({}\\%)}};' \
                .format(rect_id, view_num_list[i], ratio_tmp),
        ])
        ang_bgn = ang_end

    printTex(tmp_cmds)
    endTikz()

def drawLevelChart():
    tmp_cmds = []
    beginTikz()
    setSize(width_local, height_local, 'lb')

    origin_x = width_local/4
    origin_y = height_local/3 + 40

    level_color = [ [190, 190, 255],
                    [136, 170, 220],
                    [110, 140, 200],
                    [ 42, 122, 185],
                    [ 11,  85, 159],
                    [ 10,  50, 130]]

    tmp_cmds.extend([
        '\\node [text=white, anchor=center, align=center, font=\\fs{{38}}] (comp) at ({},{}) {{ 播放数等级对比 }} ;' \
            .format(round(width_local/2,2), round(height_local*6/7, 2)),
        '\\tikzstyle{{shadecolor}}=[left color={{rgb,255: red,{}; green,{}; blue,{}}}, middle color={{rgb,255: red,{}; green,{}; blue,{}}}, right color={{rgb,255: red,{}; green,{}; blue,{}}}, shading angle=45];' \
            .format(level_color[0][0], level_color[0][1], level_color[0][2],\
                    level_color[2][0], level_color[2][1], level_color[2][2],\
                    level_color[4][0], level_color[4][1], level_color[4][2]),
        '\\node [anchor=center, align=center, font=\\fs{{40}}] at ({},{}) {{ \\shadetext[shadecolor] {{{}}} }};' \
            .format(origin_x, origin_y, len(video_all))
    ])

    # calc level pie chart
    level_range = [[1e6, 2e6], [2e6, 3e6], [3e6, 4e6], [4e6, 5e6], [5e6, 1e7], [1e7, inf]]
    level_name = ['[100万, 200万)', '[200万, 300万)','[300万, 400万)','[400万, 500万)','[500万, 1000万)','[1000万, +$\\infty$)']

    level_num = [0] * len(level_range)
    for video_tmp in video_all:
        for i in range(0, len(level_range)):
            level_range_tmp = level_range[i]
            if level_range_tmp[0] <= video_tmp.view_avg < level_range_tmp[1]:
                level_num [i] += 1
                break

    ratio_list = [0] * len(level_num)
    for i in range(0, len(ratio_list)):
        ratio_list[i] = round(level_num[i]/len(video_all), 4)
        print(level_name[i], ratio_list[i])

    # calc level bar chart
    ratio_list_sorted = ratio_list.copy()
    ratio_list_sorted.sort(reverse=True)

    radius_outer = 180
    radius_inner = 120
    text_dist = 245
    ang_bgn = 0

    for i in range(0, len(level_name)):
        level_color_tmp = level_color[i]
        level_name_tmp = level_name[i]
        ratio_tmp = round(ratio_list[i] * 100, 2)
        ang_val = round(ratio_list[i] * 360, 2)
        ang_end = round(ang_bgn + ang_val, 2)
        ang_mid = round((ang_bgn+ang_end)/2, 2)

        bar_x = round(width_local/2 + 200, 2)
        bar_y = round(3/4*height_local-100 - i * 60, 2)
        bar_w = round(ratio_list[i]/ratio_list_sorted[0] * 300, 2)
        bar_h = 35

        rect_id = 'rect'+str(i)

        correct_x, correct_y = 0, 0

        tmp_cmds.extend([
            # draw ratio pie chart
            '\\tikzstyle{{fillcolor}}=[fill={{rgb,255:red,{}; green,{}; blue,{}}}];' \
                .format(level_color_tmp[0], level_color_tmp[1], level_color_tmp[2]),
            '\\tikzstyle{{textcolor}}=[text={{rgb,255:red,{}; green,{}; blue,{}}}];' \
                .format(level_color_tmp[0], level_color_tmp[1], level_color_tmp[2]),
            '\\path [fillcolor, shift={{({},{})}}] (0,0) -- ({}:{}) arc ({}:{}:{}) -- ({}:{}) arc ({}:{}:{});'\
                .format(round(origin_x,2), round(origin_y,2), \
                        ang_bgn, radius_outer, ang_bgn, ang_end, radius_outer, \
                        ang_end, radius_inner, ang_end, ang_bgn, radius_inner),
            # '\\node [textcolor, shift={{({},{})}}, font=\\fs{{25}}, align=center, anchor=center] at ({}:{}) {{{} \\\\[10pt] {}\\%}};'\
            #     .format(round(origin_x+correct_x,2), round(origin_y+correct_y,2), \
            #             ang_mid, text_dist, level_name_tmp, ratio_tmp),
            # draw rank bar chart
            '\\node [fillcolor, minimum width={}pt, minimum height={}pt, shape=rectangle, anchor=west, xshift=-30pt, inner sep=0pt] ({}) at ({},{}) {{}};' \
                .format(bar_w, bar_h, rect_id, bar_x, bar_y),
            '\\node [textcolor, anchor=east, font=\\fs{{25}}, align=right, xshift=-10pt] at ({}.west) {{{}}};' \
                .format(rect_id, level_name_tmp),
            '\\node [textcolor, anchor=west, font=\\fs{{20}}, align=left, xshift=5pt] at ({}.east) {{{} ({}\\%)}};' \
                .format(rect_id, level_num[i], ratio_tmp),
        ])
        ang_bgn = ang_end

    printTex(tmp_cmds)
    endTikz()

def drawRegionViewAll():
    # drawRegionViewRaw()
    global all_cmds
    all_cmds = []
    tex_filename = 'ending_region_view_all.tex'
    t1 = time.time()
    clearTex(tex_filename)
    addPreamble()
    beginDoc()

    # drawRegionSeperate()
    # drawRegionCombination()

    endDoc()

    outputTex(tex_filename)
    compileTex(tex_filename)
    t2 = time.time()
    dt1 = t2 - t1
    print('Elapsed time 1: {:.7} s'.format(dt1))

# ===================================================================

def drawChartsAll():
    global all_cmds
    all_cmds = []
    tex_filename = 'ending_charts_all.tex'
    t1 = time.time()
    clearTex(tex_filename)
    addPreamble()
    beginDoc()
    # drawSumOfVideos()
    # drawLevelChart()
    drawRegionChart()
    endDoc()

    outputTex(tex_filename)
    compileTex(tex_filename)
    t2 = time.time()
    dt1 = t2 - t1
    print('Elapsed time 1: {:.7} s'.format(dt1))

# ===================================================================
def drawTopVideoRaw():
    global all_cmds
    all_cmds = []
    tex_filename = 'ending_top_video_raw.tex'
    t1 = time.time()
    clearTex(tex_filename)
    addPreamble()
    beginDoc()

    df_sorted = df.sort_values(by='view', ascending=False)
    top_video = []
    for i in range(200):
        # print('{} {} {} {}'.format(*list(map(lambda x: df_sorted.iloc[i][x], ['view', 'pubdate', 'aid', 'title']))))
        video_tmp = VideoPoint()
        video_tmp.view     = int(df_sorted.iloc[i]['view'])
        video_tmp.videos   = int(df_sorted.iloc[i]['videos'])
        video_tmp.view_avg = int(df_sorted.iloc[i]['view'])
        video_tmp.title    = str(df_sorted.iloc[i]['title'])
        video_tmp.aid      = int(df_sorted.iloc[i]['aid'])
        video_tmp.tid      = int(df_sorted.iloc[i]['tid'])
        video_tmp.name     = str(df_sorted.iloc[i]['name'])
        video_tmp.mid      = int(df_sorted.iloc[i]['mid'])
        video_tmp.pic      = str(df_sorted.iloc[i]['pic'])
        video_tmp.face     = str(df_sorted.iloc[i]['face'])
        video_tmp.pubdate  = datetime.strptime(df_sorted.iloc[i]['pubdate'], '%Y/%m/%d %H:%M:%S')

        face_ext  = os.path.splitext(video_tmp.face)[1]
        if not face_ext in ['.jpg', '.png']:
            face_ext = '.jpg'
        face_body = 'mid_{:0>10d}'.format(video_tmp.mid)
        face_path = './face/{}{}'.format(face_body, face_ext)

        video_tmp.face_path = face_path

        top_video.append(video_tmp)

    tmp_cmds = []
    beginTikz()
    # setSize(width_local, height_local, 'lb')
    tmp_cmds.extend([
        '\\node [text=white, anchor=center, align=center, font=\\fs{{38}}] (comp) at ({},{}) {{ TOP 100 }} ;' \
            .format(round(width_local/2,2), round(height_local*6/7, 2)),
    ])

    for i in range(0, len(top_video)):
        video_tmp = top_video[i]
        rgnclr_tmp = rgnclr[video_tmp.region]
        text_x = 500
        text_y = 500 - i * 40

        title_id = 'title' + str(i)
        view_id  = 'view' + str(i)
        rank_id  = 'rank' + str(i)
        name_id  = 'name' + str(i)
        face_id  = 'name' + str(i)

        # rank 播放数 标题  up头像+昵称 [投稿时间 分区]
        tmp_cmds.extend([
            '\\tikzstyle{{fillcolor}}=[fill={{rgb,1:red,{}; green,{}; blue,{}}}];' \
                .format(rgnclr_tmp[0], rgnclr_tmp[1], rgnclr_tmp[2]),
            '\\tikzstyle{{drawcolor}}=[draw={{rgb,1:red,{}; green,{}; blue,{}}}];' \
                .format(rgnclr_tmp[0], rgnclr_tmp[1], rgnclr_tmp[2]),
            '\\tikzstyle{{textcolor}}=[text={{rgb,1:red,{}; green,{}; blue,{}}}, font=\\fs{{30}}];' \
                .format(rgnclr_tmp[0], rgnclr_tmp[1], rgnclr_tmp[2]),
            '\\node [textcolor, anchor=west, align=left] ({}) at ({}, {}) {{{}}};' \
                .format(title_id, text_x, text_y, escChar(video_tmp.title)),
            # '\\node [textcolor, anchor=east, align=left, xshift=-5pt] ({}) at ({}.west) {{{}}};' \
            #     .format(name_id, title_id, escChar(video_tmp.name)),
            '\\node [textcolor, anchor=east, align=left, xshift=-5pt, circle, minimum size=30pt, fill overzoom image={}] ({}) at ({}.west) {{}};' \
                .format(video_tmp.face_path, face_id, title_id),
            '\\node [textcolor, anchor=east, align=right, xshift=-5pt] ({}) at ({}.west) {{{} 万}};' \
                .format(view_id, face_id, round(video_tmp.view/1e4)),
            '\\node [textcolor, drawcolor, circle, anchor=east, align=right, xshift=-5pt] ({}) at ({}.west) {{{}}};' \
                .format(rank_id, view_id, i+1)
        ])
    printTex(tmp_cmds)
    endTikz()

    endDoc()

    outputTex(tex_filename)
    compileTex(tex_filename)
    t2 = time.time()
    dt1 = t2 - t1
    print('Elapsed time 1: {:.7} s'.format(dt1))

def drawTopVideoAll():
    drawTopVideoRaw()


if __name__ == '__main__':
    # drawGlobalViewAll()
    # drawRegionViewAll()
    drawChartsAll()
    # drawTopVideoAll()

