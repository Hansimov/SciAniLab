
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame as pg
import sys
import random
import collections

FPS = 30
# Beats Per Minutes
BPM = 120
# Beats Per Bar | Division of One Beat
NUME, DENO = 4, 4
SEC_PER_BEAT = 60 / BPM
SEC_PER_BAR = SEC_PER_BEAT * NUME
SEC_WHOLE_NOTE = SEC_PER_BEAT * DENO
SEC_QUART_NOTE = SEC_PER_BEAT * DENO / 4

def sec_to_frm(sec):
    frm = int(sec * FPS)
def frm_to_sec(frm):
    sec = frm * FPS

def gen_notes():
    # return list of [start_sec, dura_sec, note_idx] lists

    # note_cnt = 200
    # whole note is 1
    # dura_divi_population = [1/128,1/64,1/32,1/16,1/8,1/4, 1/2, 1, 2, 4, 8, 16]
    # dura_divi_weights =    [    1,   1,   2,  20, 40, 20,   2, 2, 2, 1, 1,  1]
    # dura_divi_list = random.choices(division_population, division_weights, note_cnt)

    note_cnt_population = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    note_cnt_weights =    [1, 4,20,20,20, 4, 4, 1, 1]
    bar_cnt = 10
    main_note_divi = 4
    main_note_dura_sec = SEC_WHOLE_NOTE / main_note_divi

    notes_list = []
    note_cnt_list = []
    tmp_start_sec = 0
    for i in range(bar_cnt):
        for j in range(main_note_divi):
            tmp_note_cnt = random.choices(note_cnt_population, note_cnt_weights, k=1)[0]
            for k in range(tmp_note_cnt):
                tmp_note_idx = random.randint(0,87)
                # notes_list.append([tmp_start_sec,main_note_dura_sec,tmp_note_idx])
            note_cnt_list.append(tmp_note_cnt)
            tmp_start_sec += main_note_dura_sec

    # for note in notes_list:
    #     # [start_sec, dura_sec, note_idx]
    #     print(note)
    # for note_cnt in note_cnt_list:
    #     print(note_cnt)
    print(collections.Counter(note_cnt_list))

    return(notes_list)

# notes_list = gen_notes()
pg.init()
screen = pg.display.set_mode((1100, 720//2), flags=pg.RESIZABLE)
clock = pg.time.Clock()

fps_font = pg.font.SysFont("comicsansms", 30)
key_font = pg.font.SysFont("arial bold", 20)

class Key():
    def __init__(self):
        self.x, self.y, self.w, self.h = (100,100,20,20)
        self.id = -1

    def disp(self):
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        pg.draw.rect(screen,(0,255,255),self.rect)

        id_text = str(self.id)
        id_text_w, id_text_h = key_font.size(id_text)
        id_text_x = self.x + (self.w - id_text_w)//2
        id_text_y = self.y + self.h + 4
        key_text = key_font.render(str(self.id), 1, (255,255,0))
        screen.blit(key_text,(id_text_x,id_text_y))

key_list = []
def createKeyList():
    global key_list
    # white: 7*7+3=52 | black: 1+5*7=36
    key_w, key_h = 15, 60
    x_tmp, y_tmp = 50, 100
    for i in range(52):
        key_tmp = Key()
        key_tmp.x, key_tmp.y = x_tmp, y_tmp
        key_tmp.w, key_tmp.h = key_w, key_h
        key_tmp.id = i+1
        x_tmp += key_w + 4
        key_list.append(key_tmp)

createKeyList()

def drawKeyList():
    for key in key_list:
        key.disp()

def quiter():
    clock.tick_busy_loop(30)
    for event in pg.event.get():
        if (event.type == pg.QUIT) or \
           (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()

frm = 0

def drawFPS():
    global frm
    frm += 1
    fps_text = fps_font.render(str(frm),1,(0,255,0))
    screen.blit(fps_text,(0,0))

while True:
    quiter()
    screen.fill((0,0,0))
    drawFPS()
    drawKeyList()
    pg.display.update()