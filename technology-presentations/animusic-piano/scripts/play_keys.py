import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame as pg
import sys
import random
import collections
from operator import add, sub

img_path = "./frames"
if not os.path.exists(img_path):
    os.mkdir(img_path)

FPS = 30
# Beats Per Minutes
BPM = 120
# Beats Per Bar | Division of One Beat
NUME, DENO = 4, 4
SEC_PER_BEAT = 60 / BPM
SEC_PER_BAR = SEC_PER_BEAT * NUME
SEC_WHOLE_NOTE = SEC_PER_BEAT * DENO
SEC_QUART_NOTE = SEC_PER_BEAT * DENO / 4

frm = 0
WIN_WH = (1200, 720//2)

def sec_to_frm(sec):
    frm = int(sec * FPS)
def frm_to_sec(frm):
    sec = frm * FPS

def gen_notes():
    # return list of [start_sec, dura_sec, note_idx]

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
            tmp_note_idx_list = random.sample(range(0,88),tmp_note_cnt)
            for tmp_note_idx in tmp_note_idx_list:
                notes_list.append([tmp_start_sec,main_note_dura_sec,tmp_note_idx])
            note_cnt_list.append(tmp_note_cnt)
            tmp_start_sec += main_note_dura_sec

    # for note in notes_list:
    #     # [start_sec, dura_sec, note_idx]
    #     print(note)
    # for note_cnt in note_cnt_list:
    #     print(note_cnt)
    print(collections.Counter(note_cnt_list))

    return notes_list

# count : w: 7*7+3=52 | b: 1+5*7=36
def num_to_wb(num):
    return "w" if num<=52 else "b"

# pit_list = ["C","Cs","D","Ds","E","F","Fs","G","Gs","A","As","B"]
# b_pit_list = ["Bb","Db","Eb","Gb","Ab"]
b_pit_list = ["As","Cs","Ds","Fs","Gs"]
def num_to_pit(num):
    # num:  1  2    3  4  5  6  7  8  9   10     52
    # pit: A0 B0 - C1 D1 E1 F1 G1 A1 B1 - C2 ... C8
    if num <= 52:
        pit = chr(ord("A")+(num-1)%7) + str((num+4)//7)
    # num:  53    54  55  56  57  58    59      88
    # pit: Bb0 - Db1 Eb1 Gb1 Ab1 Bb1 - Db2 ... Bb7
    #      As0 - Cs1 Ds1 Fs1 Gs1 As1 - Cs2 ... As7
    else:
        pit = b_pit_list[(num-53)%5] + str((num-53+4)//5)
    return pit

w_idx_list = [1, 3, 4, 6, 8, 9, 11]
b_idx_list = [2, 5, 7, 10, 0]
def num_to_idx(num):
    # num: 1 2 3 4 5 6  7 -  8  9 10 11 12 13 14 - 15 16 ...  47 48 49 - 50 51 52
    # idx: 1 3 4 6 8 9 11 - 13 15 16 18 20 21 23 - 25 27 ...  80 81 83 - 85 87 88
    #      1  2  1  2   1 -  1   2    1   2    1 -  1   2       2    1 -  1   2 
    if num <= 52:
        idx = w_idx_list[(num-1)%7] + ((num-1)//7)*12
    # num: 53 54 55 56 57 - 58 59 60 61 62 - 63 64 65 ... 83 84 85 86 87 - 88
    # idx:  2  5  7 10 12 - 14 17 19 22 24 - 26 29 31 ... 74 77 79 82 84 - 86
    else:
        idx = b_idx_list[(num-53)%5] + ((num-52)//5)*12
    return idx

def idx_to_num(idx):
    # idx: 1 2  3 4  5 6  7 8 9 10 11 12 - 13 14 15 16 17 18 19 20 21 22 23 24 ... 88
    # num: 1 53 2 3 54 4 55 5 6 56  7 57 -  8 58  9 10 59 11 60 12 13 61 14 62 ... 52
    idx_mod_12 = idx % 12
    idx_div_12 = (idx-1) // 12
    if idx_mod_12 in w_idx_list:
        num = w_idx_list.index(idx_mod_12) + 1 + idx_div_12 * 7
    else:
        num = b_idx_list.index(idx_mod_12) + 53 + idx_div_12 * 5
    return num

w_color = (255,255,255)
b_color = (90,90,90)
g_color = (0,200,0)
def num_to_color(num):
    return w_color if num<=52 else b_color

w_key_w, w_key_h = 18, 60
b_key_w, b_key_h = 14, 40
x_off, y_off = 20, 200
gap_w = 4
wb_y_off = 80
bef_cnt_list = [1,3,4,6,7]
def num_to_whxy(num):
    if num <= 52:
        w_tmp, h_tmp = (w_key_w, w_key_h)
    else:
        w_tmp, h_tmp = (b_key_w, b_key_h)

    if num <= 52:
        x_tmp = x_off + num * (w_key_w + gap_w)
        y_tmp = y_off
    else:
        # num-53: 0 1 2 3 4 - 5  6  7  8  9 - ... - 35
        # before: 1 3 4 6 7 - 8 10 11 13 14 - ... - 50
        x_tmp = x_off + (bef_cnt_list[(num-53)%5] + ((num-53)//5)*7)*(w_key_w+gap_w) \
              + w_key_w - b_key_w//2 + gap_w//2
        y_tmp = y_off - wb_y_off

    return (w_tmp, h_tmp, x_tmp, y_tmp)

pg.init()
screen = pg.display.set_mode(WIN_WH, flags=pg.RESIZABLE)
clock = pg.time.Clock()

fps_font = pg.font.SysFont("comicsansms", 30)
num_font = pg.font.SysFont("arial bold", 20)
pit_font = pg.font.SysFont("arial bold", 17)

class Key():
    def __init__(self, num):
        self.num = num
        self.num_to_all()
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.is_play = False
        self.end_frm = -1

    def num_to_all(self):
        self.wb = num_to_wb(self.num)
        self.pit = num_to_pit(self.num)
        self.idx = num_to_idx(self.num)
        self.w, self.h, self.x, self.y = num_to_whxy(self.num)
        self.color = num_to_color(self.num)

    def disp_text(self):
        num_text = str(self.num)
        num_text_w, num_text_h = num_font.size(num_text)
        num_text_xy = tuple(map(sub,self.rect.midbottom, (num_text_w//2,-3)))
        num_text_rd = num_font.render(num_text, 1, (255,255,0))
        screen.blit(num_text_rd,num_text_xy)

        pit_text = self.pit
        pit_text_w, pit_text_h = pit_font.size(pit_text)
        pit_text_xy = tuple(map(sub,self.rect.midtop, (pit_text_w//2,pit_text_h+2)))
        pit_text_rd = pit_font.render(pit_text, 1, (255,255,255))
        screen.blit(pit_text_rd, pit_text_xy)

    @property
    def is_play(self):
        return self._is_play
    @is_play.setter
    def is_play(self,val):
        self._is_play = val
        if val == True:
            self.color = g_color
        else:
            self.color = num_to_color(self.num)

        
    def disp_rect(self):
        # self.color = (125,255,random.randint(0,255))
        if self.is_play:
            self.color = (0,255,0)
        else:
            self.color = num_to_color(self.num)
        pg.draw.rect(screen,self.color,self.rect)

    def disp(self):
        self.disp_rect()
        self.disp_text()

key_list = []
def create_key_list():
    global key_list
    for i in range(88):
        key_tmp = Key(i+1)
        key_list.append(key_tmp)

def draw_key_list():
    for key in key_list:
        key.disp()

def quiter():
    clock.tick_busy_loop(FPS)
    for event in pg.event.get():
        if (event.type == pg.QUIT) or \
           (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()

def draw_fps():
    global frm
    frm += 1
    fps_text = fps_font.render(str(frm),1,(0,255,0))
    screen.blit(fps_text,(0,0))

def notes_into_keys():
    # list of [start_sec, dura_sec, note_idx]
    # notes_list = gen_notes()
    # for note in gen_notes:
    #     start_frm_tmp, dura_frm_tmp = sec_to_frm(note[0]), sec_to_frm(note[1])
    #     key_list[note[2]].notes_list.append([start_frm_tmp,dura_frm_tmp])
    pass

def main():
    create_key_list()
    
    while True:
        quiter()
        screen.fill((0,0,0))
        draw_fps()
        key_list[3].is_play = True if frm%2==1 else False
        draw_key_list()
        pg.display.update()
        # pg.image.save(screen,img_path+"/{:0>5d}.jpg".format(frm))

if __name__ == '__main__':
    main()
