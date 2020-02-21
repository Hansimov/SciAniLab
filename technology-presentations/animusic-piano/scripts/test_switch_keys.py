"""
Revision: Pygame fundamentals — pygame v2.0.0.dev5 documentation 
    https://www.pygame.org/docs/tut/tom_games2.html
PyGame Tutorial: Fonts and Text : Nerd Paradise 
    https://nerdparadise.com/programming/pygame/part5
Python | Display text to PyGame window - GeeksforGeeks 
    https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
python - How to display text in pygame? - Stack Overflow 
    https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
pygame.time — pygame v2.0.0.dev5 documentation 
    https://www.pygame.org/docs/ref/time.html?highlight=clock%20tick#pygame.time.Clock.tick
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import sys

FPS = 30

def Key():
    pass

pg.init()
screen = pg.display.set_mode((1280//2, 720//2), flags=pg.RESIZABLE)

rect1 = pg.Rect(100,100,20,20)
# screen.fill((255,255,255))
font = pg.font.SysFont("comicsansms", 30)
clock = pg.time.Clock()

frm = 0
while True:
    clock.tick_busy_loop(30)
    for event in pg.event.get():
        if (event.type == pg.QUIT) or \
           (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
    screen.fill((0,0,0))
    frm = frm + 1
    text = font.render(str(frm),1,(0,255,0))
    pg.draw.rect(screen,(0,255,255),rect1)
    screen.blit(text,(0,0))
    pg.display.update()
