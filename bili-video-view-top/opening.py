# 02 min 00 sec 慢速
# 01 min 30 sec 中速
# 极乐净土
# 01:57- Unity
#   03:30 普通Disco（伴奏）-花僮
#   03:52 桃源恋歌（古筝）
#   06:48 So Eletric
# Kid suit up
# Space Rocks

# 02 min 30 sec 快速
#   02:58 Asturias
#   04:01 千本桜（古筝、二胡、电吉他、小提琴）

import os
import time

from _tikzEnv import *

# width, height = 1920+7, 1080+4
width, height = 1280+5, 720+3

# 本视频展示了：B 站播放数超过 100 万的“用户原创视频”
# 时间范围：2009 年 06 月 26 日 -- 2018 年 08 月 28 日

def drawIntroText():
    tmp_cmds = []

    tmp_cmds.extend([
        '\\tikzstyle{{plaintext}}=[text=white, align=center, font=\\fs{{42}}];'
        '\\node [plaintext, anchor=north] at ({},{}) {{{}}};'\
            .format(round(width/2,2), 550, \
                '{\\fs{50} \\textcolor{yellow!50}{本视频展示了}}' \
                '\\\\[70pt] \\textcolor{green!50}{B站播放数超过100万的}'\
                '\\\\[30pt] \\textcolor{green!50}{“用户原创视频”} \\color{white}'\
                '\\\\[70pt] \\textcolor{white}{{\\fs{30}（投稿时间：2009.06.26 -- 2018.08.28）}}'\
                )
    ])

    printCmds(tmp_cmds)

# 横轴：投稿时间
# 纵轴：播放数（为使纵向分布更加合理，将纵坐标用类 logistic 函数重新映射）
# 右下角：当前屏幕中播放数最高的视频信息
def drawCornerText():
    tmp_cmds = []

    tmp_cmds.extend([
        '\\tikzstyle{{plaintext}}=[text=white, font=\\fs{{30}}];'
        '\\node [plaintext, anchor=north west, align=left, text width = 1000pt] at ({},{}) {{{}}};'\
            .format(200, 560, \
                """
            \\begin{itemize}[align=left, itemsep=35pt]

            \\item \\clr{yellow!50}{横轴：}\\clr{green!50}{投稿时间}  （{\\romanft \\kaishu 2009.06.26 -- 2018.08.28}）

            \\item \\clr{yellow!50}{纵轴：}\\clr{green!50}{播放数} （{\\romanft \\kaishu 100万、200万、300万、400万、500万、$\\geqslant$1000万}）
            \\\\[15pt] \\quad\\quad\\quad 为使纵向分布更加合理，将纵坐标用类 Logistic 函数重新映射：
            \\\\[20pt] \\quad\\quad\\quad {\\fs{25} \\kaishu $ \\text{纵坐标} = \\text{纵向偏移} + \\text{伸缩因子} \\cdot 2 \\cdot \\left[\\frac{1}{ {\\text{底数}}^{-\\frac{\\text{播放数}-\\text{基准值}}{\\text{尺度因子}}}+1}-0.5\\right]  $ }

            \\item \\clr{yellow!50}{右下：}\\clr{green!50}{当前屏幕中播放数最高的视频信息}
            \\\\[15pt] \\quad\\quad\\quad 若当前屏幕无视频，则保留历史视频信息
            
            \\end{itemize}

                """
            )
    ])

    printCmds(tmp_cmds)


# 本视频中的“用户原创视频”是指：
# 1. 投稿者标明为“原创”（即后台接口中 copyright 值为 1）；
# 2. 尽可能为 UGC（用户生产内容） 而非 PGC（专业生产内容）。
#     因此剔除了如下分区中的视频：（括号内为分区在后台对应的 tid 值）
#     a. “动画”区：“番剧”和“国创”中的官方内容：
#           番剧：  连载动画（33）、完结动画（32）
#           国创：  国产动画（153）
#     b. “其他”区 ：“放映厅”下的全部子分区：
#           纪录片：人文历史（37）、 科学探索（178）、热血军事（179）、舌尖上的旅行（180）
#           电影：  华语电影（147）、欧美电影（145）、日本电影（146）、其他国家（83）
#           电视剧：国产剧（185）、  海外剧（187）
def drawOriginalText():
    tmp_cmds = []
    tmp_cmds.extend([
        '\\tikzstyle{{plaintext}}=[text=white, font=\\fs{{25}}];'
        '\\node [plaintext, anchor=north west, align=left, text width = 1000pt] at ({},{}) {{{}}};'\
            .format(150, 660, \
                    """
                    {\\fs{40} \\textcolor{red}{【太长慎看】} \\textcolor{yellow!50}{本期中“用户原创视频”是指：}}
                    \\begin{enumerate}[topsep=50pt, itemsep=20pt, partopsep=0pt, parsep=20pt]
                    { \\color{green!50} \\item 投稿者标明为“原创”} \\color{white}

                    该筛选标准会影响那些没有标明为“原创”的原创视频，尤其是不少早期投稿

                    所以我们对该标准展开了反复讨论，出于如下原因，我们最终保留了这一标准：

                        \\begin{enumerate}[topsep=0pt,itemsep=20pt,partopsep=0pt,parsep=0pt, leftmargin=*, labelsep=12pt, align=left]
                        \\item 保证筛选标准的合理、简洁和统一
                        \\item “宁缺毋滥”，尽可能剔除非原创视频，而忍痛放弃未标明“原创”的真·原创视频
                        \\item 经过人工辨识，超过百万播放的视频中，\\\\[10pt]
                        未标明“原创”的占全部原创投稿的百分比约为 5\\% -- 10\\%，这一误差可以接受
                        \\end{enumerate}

                    { \\color{green!50} \\item 尽可能为 UGC（用户生产内容） 而非 PGC（专业生产内容）} \\color{white}

                   因此在满足第1条标准的情况下，还剔除了如下内容：

                       \\begin{enumerate}[topsep=0pt,itemsep=20pt,partopsep=0pt,parsep=0pt, leftmargin=*, labelsep=12pt, align=left]
                       \\item “番剧”和“国创”中的官方作品
                       \\item “放映厅”下的全部视频
                       \\end{enumerate}
                    \\end{enumerate}
                    """
                )
    ])

    printCmds(tmp_cmds)

def drawOpeningAll():
    global all_cmds
    all_cmds =[]
    tex_filename = 'opening.tex'

    t1 = time.time()

    drawing_cmd_list = [
        'drawIntroText()',
        'drawCornerText()',
        'drawOriginalText()',
    ]


    for drawing_cmd in drawing_cmd_list:
        beginTikz()
        setSize(width, height, 'lb')
        eval(drawing_cmd)
        endTikz()

    outputTex(tex_filename, compiletex=True, pdf2png=True)

    t2 = time.time()
    dt1 = t2 - t1

    print('Elapsed time 1: {} s'.format(round(dt1, 2)))


if __name__ == '__main__':
    drawOpeningAll()