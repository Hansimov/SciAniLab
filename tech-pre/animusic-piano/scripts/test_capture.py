import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame as pg
import sys

WIN_WH = (1280//2, 720//2)

pg.init()
screen = pg.display.set_mode(WIN_WH, flags=pg.RESIZABLE)

rect1 = pg.Rect(100,100,20,20)

screen.fill((0,0,0))
rect1.move_ip(1,1)
pg.draw.rect(screen,(0,255,255),rect1)

# pg.image.save(screen, "screenshot.jpg")
img_path = "./frames"
if not os.path.exists(img_path):
    os.mkdir(img_path)

img_str = pg.image.tostring(screen,"RGBA")
img = pg.image.frombuffer(img_str,WIN_WH,"RGBA")
pg.image.save(img,"hello.jpg")

# shot_cnt = 1
# for shot_str in shot_str_list:
#     shot_img = pg.image.frombuffer(shot_str,WIN_WH,"RGBA")
#     pg.image.save(shot_img, img_path+"/{:0>5d}.jpg".format(shot_cnt))
#     shot_cnt += 1
pg.display.update()
