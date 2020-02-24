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

gen_notes()