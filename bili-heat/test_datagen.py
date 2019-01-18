from tikzpy import *
from random import randint, random


num = 81
r = 20
video_time = [i+randint(1,2) for i in range(0,num)]
# print(video_time)


circs = []
step = sqrt(num)

width, height = 4 * step * r, 4 * step * r
initTikzpy('test_datagen.pdf',width=width, height=height)

for i in range(0,90):
    for j in range(num):
        if video_time[j] >= i:
            continue
        else:
            x = 2*r + 3 * r * (j % step)
            y = 2*r + 3 * r * (j//step)
            circ = circle(xy=[x,y], r=r)
            circ.fill_rgba[0:3] = vec([randint(0,255),140,0])/255
            circ.stroke_rgba = [0,0,0,0]
            # circ.is_stroke = False
            # circs.append(circ)
    box(xy=[width-10,height-60], anchor='br',text='2018年01月{:0>2}日'.format(i//3), font_size=30)
    newPage()

outputImg()