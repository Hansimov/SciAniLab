import os
import time
from p5 import setup, draw, run
import p5 as pf
vec = pf.Vector
from operator import add, sub

from reply_parser import *

t0 = time.time()

img_path = "./frames/"
if not os.path.exists(img_path):
    os.mkdir(img_path)

cover_path = "./covers/"

img0 = pf.load_image(cover_path+"784489.jpg")
font = pf.create_font("c:/windows/fonts/arialuni.ttf",16)
with open("ninfo_rank.pkl","rb") as rf:
    # ninfo_L: list of floor_num_L
    ct_L, ninfo_L, idx_LL = pickle.load(rf)


# print(len(ninfo_L), len(idx_LL))


def setup():
    ratio = 1.8
    pf.size(1280/ratio,720/ratio)
    pf.text_font(font)
    pf.title("Patato")
    pf.no_loop()

def draw():
    # pf.image_mode("center")
    pf.background(255)
    pf.image(img0,(100,100))
    pf.fill(255,0,0)

    # pf.text_align("LEFT","CENTER")

    pf.text_size(100)

    # pf.image_mode("corner")

    en_str = "hello 你好"
    pf.text(en_str,(200,200))

    pf.rect((100,100), *[100,100])

    # pf.save_frame(img_path + "screen_.png")


def main():
    # run(frame_rate = 10)
    pass

if __name__ == '__main__':
    main()
    print("Total elapsed time: {}s".format(round(time.time()-t0,1)))
