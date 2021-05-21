import os
import time
from p5 import setup, draw, run
import p5 as pf
vec = pf.Vector
from operator import add, sub

from reply_parser import *

img_path = "./frames/"
if not os.path.exists(img_path):
    os.mkdir(img_path)

cover_path = "./covers/"

img0 = pf.load_image(cover_path+"784489.jpg")
font = pf.create_font("c:/windows/fonts/arialuni.ttf",16)
def setup():
    # pass
    ratio = 1
    pf.size(1280/ratio,720/ratio)
    pf.title("Patato")
    pf.no_loop()

# f = create_font("Arial.tiff", 16,) # Arial, 16 point, anti-aliasing on

def draw():
    # pf.image_mode("center")
    # pf.tint()
    # img_size[0]-=1
    pf.background(255)
    # pf.image(img0,(100,100))
    pf.text_font(font)

    # pf.stroke_weight(0)
    pf.text_align("center","center")
    # pf.stroke(255,0,0)
    # pf.no_fill()

    pf.text_size(100)

    en_str = "hello 你好"

    pf.fill(255,0,0)

    gap = 100
    height = 20
    pf.text(en_str,(50,height))

    pf.stroke(0,0,255)
    pf.stroke_weight(5)

    height += gap
    pf.text(en_str,(50,height))

    pf.stroke_weight(-5)
    height += gap
    pf.text(en_str,(50,height))

    pf.no_fill()
    height += gap
    pf.stroke_weight(5)
    pf.text(en_str,(50,height))

    height += gap
    pf.stroke_weight(-5)
    pf.text(en_str,(50,height))

    # pf.save_frame(img_path + "screen_.png")


def main():
    run(frame_rate = 10)

if __name__ == '__main__':
    main()
