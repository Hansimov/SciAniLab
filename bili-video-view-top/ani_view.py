import os

def compileTex(cp_type='xelatex'):
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

def preamble():
    preamble_list = [
        '\\documentclass[tikz]{standalone}\n',
        '\\usepackage{tikz}',
        '\\usetikzlibrary{backgrounds}'
    ]
    printTex(preamble_list)

def beginDoc(doctype='standalone'):
    printTex('\\begin{document}\n')

def endDoc():
    printTex('\n\\end{document}')

def beginTikz():
    begin_tikz = '\\begin{tikzpicture}'
    global_setting = '''
    [ x=1pt,y=1pt,
      background rectangle/.style={fill=black},
      show background rectangle
    ]
    '''
    printTex(begin_tikz + global_setting + '\n')

def endTikz():
    printTex('\n\\end{tikzpicture}\n')

def printTex(commands):
    with open(tex_filename, 'a') as txf:
        if isinstance(commands, str):
            print(commands, file=txf)
        elif isinstance(commands, list):
            for line in commands:
                print(line, file=txf)
        # print('',file=txf)

def setSize(width, height, anchor='lb'):
    # anchor is the center of the origin point of the bounding box
    #   - left right up bottom center
    #   - l,r,u,b, lu, lb, ru, rb, c
    if   anchor == 'c':
        set_size = '\path (-{0:}, -{1:}) rectangle ({0:}, {1:});'.format(width/2,height/2)
    elif anchor == 'lb':
        set_size = '\path ({0:}, {1:}) rectangle ({0:}, {1:});'.format(width,height)
    else: # TODO
        set_size = '\path ({0:}, {1:}) rectangle ({0:}, {1:});'.format(width,height)
    printTex(set_size)

'''
第四期视频的话，300万以上的显示封面，200万~300万的作为背景墙吧
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

if __name__ == '__main__':
    tex_filename = 'ani_view.tex'

    clearTex()
    preamble()
    beginDoc()
    for i in range(0, 1):
        beginTikz()
        width, height = 1280, 720
        setSize(width, height, 'c')
        # printTex('\\fill[blue] ({0:}, {1:}) rectangle ({0:}, {1:});'.format(width/2,height/2))
        radius = 200
        cmd_list = [
            '\\draw [fill=yellow, radius=6] (5,0) circle;'
        ]

        printTex(cmd_list)
        endTikz()
    endDoc()
    compileTex()