import os
from math import *
import time

all_cmds = []

# width, height = 1920+7, 1080+4
width, height = 1280+5, 720+3

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
        '\\usepackage[skins]{tcolorbox}',
        '\\usepackage[export]{adjustbox}',
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

def drawIntroText():
    pass

def drawOriginalText():
    pass

def drawCornerText():
    pass

# 本视频展示了：B 站播放数超过 100 万的“用户原创视频”
# 时间范围：2009 年 06 月 26 日 -- 2018 年 08 月 XX 日
# 横轴：投稿时间
# 纵轴：播放数（为使纵向分布更加合理，将纵坐标用 logistic 函数重新映射）
# 右下角：当前屏幕中播放数最高的视频信息

# 本视频中的“用户原创视频”是指：
# 1. 投稿者标明为“原创”（即后台接口中 copyright 值为 1）；
# 2. 尽可能为 UGC（用户生产内容） 而非 PGC（专业生产内容）。
#     因此剔除了如下分区中的视频：（括号内为分区在后台对应的 tid 值）
#     a. “动画”区：“番剧”和“国创”中的官方内容：
#           番剧：  连载动画（33）、 完结动画（32）
#           国创：  国产动画（153）
#     b. “其他”区 ：“放映厅”下的全部子分区：
#           纪录片：人文历史（37）、 科学探索（178）、热血军事（179）、舌尖上的旅行（180）
#           电影：  华语电影（147）、欧美电影（145）、日本电影（146）、其他国家（83）
#           电视剧：国产剧（185）、  海外剧（187）



def drawBgm():
    pass

def drawTool():
    tmp_cmds = []

    tmp_cmds.extend([
        '\\node [text=white, anchor=center, align=center, font=\\fs{{42}}] at ({},{}) {{ 软~件~工~具 }} ;' \
            .format(round(width/2,2), round(height*6/7, 2))
    ])

    # Python, LaTeX, Ghostscript, FFmpeg, Premiere

    tool_list = [
        ['Python'             , '数据处理' , './images/python.png'      , [ 55,116,167], [255,209, 65]] ,
        ['LaTeX'              , '图形绘制' , './images/latex.png'       , [255,255,255], [120,120,120]] ,
        ['Ghostscript'        , '图像转换' , './images/ghostscript.png' , [  0,117,208], [120,120,120]] ,
        ['FFmpeg'             , '视频转换' , './images/ffmpeg.png'      , [255,255,255], [  0,120,  8]] ,
        ['Adobe Premiere Pro' , '后期制作' , './images/premiere.png'    , [234,119,255], [182,  0,182]]
    ]

    for i in range(0, len(tool_list)):
        name = tool_list[i][0]
        work = tool_list[i][1]
        face = tool_list[i][2]
        colorx = tool_list[i][3]
        colory = tool_list[i][4]

        name_id = 'name' + str(i)
        work_id = 'work' + str(i)
        face_id = 'face' + str(i)

        name_y_offset = 500
        name_y_step   = 90

        name_x = 2/6 * width
        name_y = name_y_offset - i * name_y_step

        work_x = 3/5 * width
        work_y = name_y

        tmp_cmds.extend([
        '\\tikzstyle{{staff}}=[color={{rgb,255: red,{}; green,{}; blue,{}}}, align=left, font=\\fs{{26}}, inner sep=4pt];' \
            .format(colorx[0], colorx[1], colorx[2]),
        '\\tikzstyle{{shadecolor}}=[left color={{rgb,255: red,{}; green,{}; blue,{}}}, right color={{rgb,255: red,{}; green,{}; blue,{}}}, shading angle=45];' \
            .format(colorx[0], colorx[1], colorx[2], colory[0], colory[1], colory[2]),
        '\\node [staff, anchor=west] ({}) at ({},{}) {{ \\shadetext[shadecolor] {{{}}} }} ;'\
            .format(name_id, name_x, name_y, name),
        '\\node [staff, anchor=west] ({}) at ({},{}) {{ \\shadetext[shadecolor] {{{}}} }} ;'\
            .format(work_id, work_x, work_y, work),
        '\\node [staff, anchor=east, xshift=-10pt] ({}) at ({}.west) {{ \\includegraphics[height={}pt, max width={}pt]{{{}}} }} ;'\
            .format(face_id, name_id, 50, 80, face),
        ])

    printTex(tmp_cmds)


def drawStaff():
    tmp_cmds = []

    tmp_cmds.extend([
        '\\node [text=white, anchor=center, align=center, font=\\fs{{42}}] at ({},{}) {{ 工~作~人~员 }} ;' \
            .format(round(width/2,2), round(height*6/7, 2))
    ])

    staff_list = [
        ['狸子\\mbox{LePtC}', '策划'                     , './images/leptc.jpg'     ,[205, 20, 20],[255,255,255]],
        ['yxlllc'          , '审校'             , './images/yxlllc.jpg'    ,[ 2 , 91,142],[255,255,255]],
        ['霜落\\mbox{xss}'  , '数据库维护'                , './images/shuangluo.jpg' ,[167,110, 62],[255,255,255]],
        ['Hansimov'        , '数据处理、动效生成、后期制作', './images/hansimov.jpg',[ 50, 50,255],[255,255,255]],
    ]

    for i in range(0, len(staff_list)):
        name  = staff_list[i][0]
        work  = staff_list[i][1]
        face  = staff_list[i][2]
        colorx = staff_list[i][3]
        colory = staff_list[i][4]

        name_id = 'name' + str(i)
        work_id = 'work' + str(i)
        face_id = 'face' + str(i)

        name_y_offset = 500

        name_y_step   = 120

        name_x = 2/6 * width
        name_y = name_y_offset - i * name_y_step

        work_x = 3/5 * width
        work_y = name_y

        tmp_cmds.extend([
        '\\tikzstyle{{staff}}=[color={{rgb,255: red,{}; green,{}; blue,{}}}, align=left, font=\\fs{{26}}, inner sep=4pt];' \
            .format(colorx[0], colorx[1], colorx[2]),
        '\\tikzstyle{{shadecolor}}=[left color={{rgb,255: red,{}; green,{}; blue,{}}}, right color={{rgb,255: red,{}; green,{}; blue,{}}}, shading angle=45];' \
            .format(colorx[0], colorx[1], colorx[2], colory[0], colory[1], colory[2]),
        # '\\node [staff, anchor=west] ({}) at ({},{}) {{ {} }} ;'.format(name_id, name_x, name_y, name),
        '\\node [staff, anchor=west] ({}) at ({},{}) {{ \\shadetext[shadecolor] {{{}}} }} ;'\
            .format(name_id, name_x, name_y, name),
        # '\\node [staff, anchor=west] ({}) at ({},{}) {{ {} }} ;'.format(work_id, work_x, work_y, work),
        '\\node [staff, anchor=west] ({}) at ({},{}) {{ \\shadetext[shadecolor] {{{}}} }} ;'\
            .format(work_id, work_x, work_y, work),
        # '\\node [staff, anchor=east] ({}) at ({}.west) {{ \\includegraphics [width={}pt,height={}pt] {{{}}} }} ;'\
        #     .format(face_id, name_id, 60, 60,  escChar(face)),
        '\\node [staff, anchor=east, circle, xshift=-10pt, minimum size={}pt, fill overzoom image={}] ({}) at ({}.west) {{}} ;'\
            .format(60, face, face_id, name_id),
        ])

    printTex(tmp_cmds)

def drawOrg():
    tmp_cmds = []

    tmp_cmds.extend([
        '\\node [text=white, anchor=center, align=center, font=\\fs{{42}}] at ({},{}) {{ 出~品 }} ;' \
            .format(round(width/2,2), round(height*6/7, 2))
    ])


    face    = './images/uupers.jpg'
    name_zh = '不科学的\\mbox{UP}组'
    # name_en = '{\\color{white}{\\color{red}U}nited {\\color{green}U}nscientific {\\color{blue}P}roducers}'
    name_en = 'United Unscientific Producers'
    link    = 'https://github.com/uupers'

    face_x = round(width/2, 2)
    face_y = 450

    face_id = 'face'
    name_zh_id = 'namezh'
    name_en_id = 'nameen'
    link_id = 'link'

    tmp_cmds.extend([
        '\\node [anchor=center, circle, minimum size={}pt, fill overzoom image={}] ({}) at ({},{}) {{}} ;'\
            .format(80, face, face_id, face_x, face_y),
        '\\node [anchor=north, yshift={}pt, text=white, font=\\fs{{30}}] ({}) at ({}.south) {{{}}} ;' \
            .format(-40, name_zh_id, face_id, name_zh),
        '\\node [anchor=north, yshift={}pt, text=white, font=\\fs{{30}}] ({}) at ({}.south) {{{}}} ;' \
            .format(-40, name_en_id, name_zh_id, name_en),
        '\\node [anchor=north, yshift={}pt, text=white, font=\\fs{{30}}] ({}) at ({}.south) {{{}}} ;' \
            .format(-40, link_id, name_en_id, link),
    ])

    printTex(tmp_cmds)

def drawStaff():
    global all_cmds
    all_cmds = []

    tex_filename = 'staff.tex'
    t1 = time.time()

    clearTex(tex_filename)
    addPreamble()

    drawing_cmd_list = [
        # 'drawBgm()',
        'drawTool()',
        'drawStaff()',
        'drawOrg()'
    ]

    beginDoc()

    for drawing_cmd in drawing_cmd_list:
        beginTikz()
        setSize(width, height, 'lb')
        eval(drawing_cmd)
        endTikz()

    endDoc()

    outputTex(tex_filename)
    compileTex(tex_filename)

    t2 = time.time()
    dt1 = t2 - t1
    print('Elapsed time 1: {:.7} s'.format(dt1))


if __name__ == '__main__':
    drawStaff()