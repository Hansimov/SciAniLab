import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_VidxEO_CENTERED'] = '1'
import pygame as pg
import sys
import random
import collections

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

WIN_WH = (1200, 720//2)

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

    return(notes_list)

pg.init()
screen = pg.display.set_mode(WIN_WH, flags=pg.RESIZABLE)
clock = pg.time.Clock()

fps_font = pg.font.SysFont("comicsansms", 30)
num_font = pg.font.SysFont("arial bold", 20)
pit_font = pg.font.SysFont("arial bold", 20)

class Key():
    # count : w: 7*7+3=52 | b: 1+5*7=36
    # b_mod_12_list = [0,2,5,7,10]
    # b_pit_list= ["Bb","Db","Eb","Gb","Ab"]
    b_pit_list= ["As","Cs","Ds","Fs","Gs"]
    # pit_list = ["C","Cs","D","Ds","E","F","Fs","G","Gs","A","As","B"]
    w_idx_list = [1, 3, 4, 6, 8, 9, 11]
    b_idx_list = [2, 5, 7, 10, 12]
    key_w, key_h = 18, 60
    x_tmp, y_tmp = 20, 140

    def __init__(self):
        self.x, self.y, self.w, self.h = (100,100,20,20)

    def num_to_wb(self):
        # white: idx % 12 = 1,3,4,6,8,9,11
        # black: idx % 12 = 0,2,5,7,10
        if self.num <= 52:
            self.wb = "w"
        else:
            self.wb = "b"

    def num_to_pit(self):
        # num:  1  2    3  4  5  6  7  8  9   10     52
        # pit: A0 B0 - C1 D1 E1 F1 G1 A1 B1 - C2 ... C8
        if self.num <= 52:
            self.pit = chr(ord("A")+(self.num-1)%7) + str((self.num+4)//7)
        # num:  53    54  55  56  57  58    59      88
        # pit: Bb0 - Db1 Eb1 Gb1 Ab1 Bb1 - Db2 ... Bb7
        #      As0 - Cs1 Ds1 Fs1 Gs1 As1 - Cs2 ... As7
        else:
            self.pit = b_pit_list[(self.num-53)%5] + str((self.num-53+4)//5)

    def pit_to_idx(self):
        # pit: A0 As0 B0 - C1 Cs1 D1 Ds1 E1 F1 Fs1 G1 Gs1 A1 As1 B1 - C2 Cs2 ... - C8
        # idx:  1   2  3    4   5  6   7  8  9  10 11  12 13  14 15   16  17 ...   88
        pass
    def num_to_idx(self):
        # num: 1 2 3 4 5 6  7 -  8  9 10 11 12 13 14 - 15 16 ...  47 48 49 - 50 51 52
        # idx: 1 3 4 6 8 9 11 - 13 15 16 18 20 21 23 - 25 27 ...  80 81 83 - 85 87 88
        #      1  2  1  2   1 -  1   2    1   2    1 -  1   2       2    1 -  1   2 
        if self.num <= 52:
            self.idx = w_idx_list[(self.num-1)%7] + ((self.num-1)//7)*12
        # num: 53 54 55 56 57 - 58 59 60 61 62 - 63 64 65 ... 83 84 85 86 87 - 88
        # idx:  2  5  7 10 12 - 14 17 19 22 24 - 26 29 31 ... 74 77 79 82 84 - 86
        else:
            self.idx = b_idx_list[(self.num-53)%5] + ((self.num-53)//5)*12

    def setup_wb_pit_pos_num(self):
        if (self.wb == "w"):
            self.color = (255,255,255)
        else:
            self.color = (90,90,90)

    def disp(self):
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.color = (125,255,random.randint(0,255))
        pg.draw.rect(screen,self.color,self.rect)

        num_text = str(self.idx)
        num_text_w, num_text_h = idx_font.size(num_text)
        num_text_x = self.x + (self.w - num_text_w)//2
        num_text_y = self.y + self.h + 4
        num_text_rd = idx_font.render(num_text, 1, (255,255,0))
        screen.blit(num_text_rd,(num_text_x,num_text_y))

        pit_text = self.pit
        pit_text_w, pit_text_h = pit_font.size(self.pit_text)
        pit_text_x = self.x + (self.w - pit_text_w)//2
        pit_text_y = self.y - pit_text_h - 2
        pit_text_rd = pit_font.render(self.pit_text, 1, (255,255,255))
        screen.blit(pit_text_rd,(pit_text_x,pit_text_y))

key_list = []
def createKeyList():
    global key_list
    for i in range(88):
        key_tmp = Key()
        key_tmp.num = i+1
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

def main():
    while True:
        quiter()
        screen.fill((0,0,0))
        drawFPS()
        drawKeyList()
        pg.display.update()
        # pg.image.save(screen,img_path+"/{:0>5d}.jpg".format(frm))

if __name__ == '__main__':
    main()
    # gen_notes()