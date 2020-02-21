import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame as pg
import sys

pg.init()
sfc = pg.display.set_mode((1280//2, 720//2), flags=pg.RESIZABLE)

rect1 = pg.Rect(100,100,20,20)
# sfc.fill((255,255,255))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    sfc.fill((0,0,0))
    rect1.move_ip(-0.1,-0.1)
    pg.draw.rect(sfc,(0,255,255),rect1)
    pg.display.update()
