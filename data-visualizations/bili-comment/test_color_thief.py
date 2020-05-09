import os
import time
from operator import add, sub
from p5 import setup, draw, run
import p5 as pf
vec = pf.Vector
from colorthief import ColorThief

import cProfile, pstats, io
pr = cProfile.Profile()

t0 = time.time()

frame_path = "./frames/"
if not os.path.exists(frame_path):
    os.mkdir(frame_path)


font = pf.create_font("c:/windows/fonts/arialuni.ttf",16)

cover_path = "./covers/"
img_L = []
w,h = (80,60)
for i,file in enumerate(os.listdir(cover_path)[:50]):
    img_path = cover_path + file
    img = pf.load_image(img_path)
    img.size = (w,h)
    clr_thf = ColorThief(img._img)
    d_color = clr_thf.get_color(quality=10)
    # pf.fill(*d_color)
    palette = clr_thf.get_palette(color_count=2,quality=20)
    # palette = None
    img_L.append([img,img_path,d_color,palette])

win_w, win_h = (1280, 720)
t1 = None
def setup():
    global img_L, t1
    ratio = 1.2
    pf.size(win_w/ratio,win_h/ratio)
    pf.text_font(font)
    # pf.no_stroke()
    # pf.no_loop()
    t1 = time.time()
    pr.enable()

frm = 0
def draw():
    global frm
    # pf.image_mode("center")
    pf.background(255)

    x,y = (10,10)
    xgap,ygap = 2*w+20, h+20
    for i,item in enumerate(img_L):
        t0 = time.time()
        img, img_path, d_color, palette = item
        px = x + (i//7)*xgap
        py = y + (i%7)*ygap
        # pf.image(img,(px,py),(w,h))

        pf.fill(*d_color)
        pf.rect((px+w,py), *(w/3,h))
        # pf.circle((px+w,py), w/3)

        pf.fill(*palette[0])
        pf.rect((px+w+w*1/3,py), *(w/3,h))
        # pf.circle((px+w+w*1/3,py), w/3)

        pf.fill(*palette[1])
        pf.rect((px+w+w*2/3,py), *(w/3,h))
        # pf.circle((px+w+w*2/3,py), w/3)

        # print("{}s".format(time.time()-t0))

    frm += 1
    print(frm)
    # pf.save_frame(img_path + "screen_.png")

    if frm == 30:
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("tottime")
        # ps = pstats.Stats(pr, stream=s).sort_stats("cumtime")
        ps.print_stats()
        with open("res.txt","w") as wf:
            print(s.getvalue(),file=wf)
        print("Writing profile to res.txt")
        print("Total elapsed time: {}s".format(round(time.time()-t1,1)))

def main():
    run()
    pass

if __name__ == '__main__':
    main()
    # print("Total elapsed time: {}s".format(round(time.time()-t0,1)))
