from tikzpy import *
import os
import csv
import subprocess
from random import random, randint

glyphsfolder = "glyphs"
glyphsfile = glyphsfolder + ".pdf"
if not os.path.exists(glyphsfolder): 
    os.mkdir(glyphsfolder)

wordsfile = "words.pdf"

abspath = os.getcwd()
# cmd_pdf2png = 'gswin64c -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -r{0} -sOutputFile="{1}\\glyphs\\glyphs_%05d.png" "{1}\\glyphs.pdf"'.format(72,abspath)
cmd_pdf2png = 'gswin64c -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -r{0} -sOutputFile="./glyphs/glyphs_%05d.png" "./glyphs.pdf"'.format(72)

def glyphs2xy(glyphs,font_face="Arial Unicode MS",font_size=100):
    pw,ph=len(glyphs)*font_size+1,font_size+1
    newPage(size=[pw,ph])
    nd1 = node(xy=[pw/2,ph/2],text=glyphs,font_face=font_face,font_size=font_size,text_rgba=[0,0,0,1])
    name,ext = os.path.splitext(glyphsfile)

# os.system(cmd_pdf2png)

word_freq_data = "./word-freq-data/"

fs = os.listdir(word_freq_data)

csv_reader = csv.reader(open(word_freq_data+fs[57],mode="r",encoding="utf8"),delimiter=",")
lines = list(csv_reader)


initTikzpy(wordsfile,width=1280,height=720)
for idx, line in enumerate(lines):
    # if idx == 10:
    #     break
    # print(line)
    x,y = randint(100,1100), randint(100,600)
    r,g,b = random(),random(),random()
    node(text_rgba=[r,g,b,1.0],xy=[x,y],font_size=randint(10,40),text=line[0])
outputImg()