from tikz import *
import os
import csv
import subprocess


glyphsfolder = "glyphs"
glyphsfile = glyphsfolder + ".pdf"
if not os.path.exists(glyphsfolder): 
    os.mkdir(glyphsfolder)

abspath = os.getcwd()
# cmd_pdf2png = 'gswin64c -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -r{0} -sOutputFile="{1}\\glyphs\\glyphs_%05d.png" "{1}\\glyphs.pdf"'.format(72,abspath)
cmd_pdf2png = 'gswin64c -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -r{0} -sOutputFile="{1}\\glyphs\\glyphs_%05d.png" "{1}\\glyphs.pdf"'.format(72,abspath)

def glyphs2xy(glyphs,font_face="Arial Unicode MS",font_size=100):
    pw,ph=len(glyphs)*font_size+1,font_size+1
    newPage(size=[pw,ph])
    nd1 = node(xy=[pw/2,ph/2],text=glyphs,font_face=font_face,font_size=font_size,text_rgba=[0,0,0,1])
    name,ext = os.path.splitext(glyphsfile)

initTikzpy(glyphsfile,width=0,height=0)
glyphs2xy("HELLO你好","微软雅黑",30)
glyphs2xy("你好世界","微软雅黑",30)
glyphs2xy("英雄联盟","微软雅黑",30)
glyphs2xy("搞笑","微软雅黑",30)
glyphs2xy("鬼畜","微软雅黑",30)
outputImg()



# word_freq_data = "./word-freq-data/"

# fs = os.listdir(word_freq_data)

# csv_reader = csv.reader(open(word_freq_data+fs[57],mode="r",encoding="utf8"),delimiter=",")
# lines = list(csv_reader)

# for idx,line in enumerate(lines):
#     if idx == 10:
#         break
#     print(line)
# print(rows)
# print(len(rows))
