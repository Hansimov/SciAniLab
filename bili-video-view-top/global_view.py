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

axis_l, axis_r = 50, width - 10
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

def compileTex(tex_filename, cp_type='xelatex'):
    if cp_type == 'xelatex' or cp_type == 'x':
        compile_type = '-xelatex'
    else:
        compile_type = '-pdf'

    compile_limits = ' -pool-size=7999999 -extra-mem-top=20000000 -extra-mem-bot=20000000'
    compile_tool = 'latexmk -pv '+ compile_limits + ' ' + compile_type + ' '
    absolute_tex_filename = os.path.join(os.getcwd(), tex_filename)
    os.system(compile_tool + absolute_tex_filename)

def addPreamble():
    preamble_list = [
        '\\documentclass[tikz,border=0pt]{standalone}\n',
        '\\usepackage{tikz}',
        '\\usepackage{graphicx}',
        '\\usetikzlibrary{calc}',
        '\\usepackage{amssymb}',
        '\\usepackage{bm}',
        '\\usetikzlibrary{backgrounds}',
        '\\usepackage[scheme=plain]{ctex}',
        '\\newfontfamily\\hupo{STXingkai}',
        '\\setCJKfamilyfont{hwhp}{STXingkai}',
        '\\newcommand{\\hupozh}{\\CJKfamily{hwhp}}',
        '\\newcommand{\\fs}[1]{\\fontsize{#1}{0pt}\\selectfont}',
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

rgnclr = {} # region color

rgnclr['donghua']  = [0.5, 0.5,  1 ]
rgnclr['yinyue']   = [ 1 ,  1 ,  0 ]
rgnclr['wudao']    = [ 1 , 0.5,  0 ]
rgnclr['youxi']    = [ 1 , 0.1 ,0.1]
rgnclr['keji']     = [ 0 , 0.5,  1 ]
rgnclr['shenghuo'] = [ 0 , 0.5,  0 ]
rgnclr['guichu']   = [0.5,  1 ,  1 ]
rgnclr['qita']     = [ 1 , 0.5,  1 ]

rgnname = ['动画','音乐','舞蹈','游戏','科技','生活','鬼畜','其他']
rgnpinyin = ['donghua','yinyue','wudao','youxi','keji','shenghuo','guichu','qita']

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
        if  self.tid in [1, 24, 25, 47, 27,  13, 33, 32, 51, 152,  167, 153, 168, 169, 170]:
            self.region = 'donghua'
        # 音乐
        elif self.tid in [3, 28, 31, 30, 59, 29, 54, 130]:
            self.region = 'yinyue'
        # 舞蹈
        elif self.tid in [129, 20, 154, 156]:
            self.region = 'wudao'
        # 游戏
        elif self.tid in [4, 17, 171, 172, 65, 173, 121, 136, 19]:
            self.region = 'youxi'
        # 科技
        elif self.tid in [36, 124, 122, 39, 96, 95, 98, 176]:
            self.region = 'keji'
        # 生活
        elif self.tid in [160, 138, 21, 76, 75, 161, 162, 175, 163, 174]:
            self.region = 'shenghuo'
        # 鬼畜
        elif self.tid in [119, 22, 26, 126, 127]:
            self.region = 'guichu'
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
def initVideo():
    global video_all
    df = pd.read_csv('./data/view_gt100w_180820x_out.csv', sep=',')
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

        # video_tmp.title    = str(df['title'][i])
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

def drawGlobalView():
    global all_cmds
    all_cmds = []
    tex_filename = 'global_view.tex'
    t1 = time.time()
    clearTex(tex_filename)
    addPreamble()
    beginDoc()
    beginTikz()

    setSize(width, height, 'lb')

    drawDateAxis()

    num = 0
    for video in video_all:
        num += 1
        video.display()

    endTikz()
    endDoc()

    outputTex(tex_filename)
    compileTex(tex_filename)
    t2 = time.time()
    dt1 = t2 - t1
    print('Elapsed time 1: {:.7} s'.format(dt1))

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

def animateGlobalView():
    global all_cmds
    all_cmds = []

    tex_filename = 'global_view_ani.tex'
    t1 = time.time()
    clearTex(tex_filename)
    addPreamble()
    beginDoc()

    shift_frames_cnt = 60 * 5
    shift_x_step = (width + width_local)/shift_frames_cnt

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

if __name__ == '__main__':
    # drawGlobalView()
    animateGlobalView()

