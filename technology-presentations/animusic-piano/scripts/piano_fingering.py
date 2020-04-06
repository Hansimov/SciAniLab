# encoding: utf-8

# * Correct Piano Fingering: The Why and How 
# ** https://www.onlinepianocoach.com/piano-fingering.html

# * Finger positions – four piano finger exercises that will set you on your way 
# ** https://www.skoove.com/blog/finger-positions-four-piano-finger-exercises-that-will-set-you-on-your-way/

# * 简单分享：钢琴入门指法的知识 - 简书 
# ** https://www.jianshu.com/p/d15ddddb745e

# * 指法 | 钢琴演奏中五种必备指法，你是否烂熟于心？ - 知乎 
# ** https://zhuanlan.zhihu.com/p/25526000

# 一对一、穿指、跨指、扩指、缩指

from __future__ import print_function, division
import sys
path_to_add = "H:/codes/SciAniLab/technology-presentations/animusic-piano/scripts/"
if not path_to_add in sys.path:
    sys.path.append(path_to_add)

import midi_parser as mp
import c4d_kits as ck
reload(mp)
reload(ck)
from midi_parser import *
from c4d_kits import *

# TPQN, USPQN = mp.TPQN, mp.USPQN

clear_console()

chords = find_obj("Chords","")[0]
chord_L = find_obj("chord_.*","chords")
arms = find_obj("Arms","")[0]

# arm_L = find_obj("arm_.*","arms")
d_r_arms = sorted(find_obj("arm_d_r.*","arms"),key=lambda obj:obj.GetName())
d_l_arms = sorted(find_obj("arm_d_l.*","arms"),key=lambda obj:obj.GetName())
# u_r_arms = find_obj("arm_u_r.*","arms")
# u_l_arms = find_obj("arm_u_l.*","arms")
# for arm in d_l_arms:
#     print(arm.GetName())
# print(is_rot_reachable(10,70,77))


start_undo()
add_undo(c4d.UNDOTYPE_CHANGE, chords)
add_undo(c4d.UNDOTYPE_CHANGE, arms)
end_undo()

hiting_arm_L = []
moving_arm_L = []

# note: start, dura, chan_num, pit_dec, vel
# played_note_L = process_midi(path_to_add+"abc.mid",info_level=1)
# pit_L = [note[3] for note in played_note_L]

# def schedule_arms():
#     arm_idx_L = 

played_note_L = process_midi(path_to_add+"secret.mid",info_level=0)
# for note in played_note_L:
#     print(note)
# print(len(played_note_L))


# print(len(pit_L))
# for pit in pit_L:
#     print(pit)
# print(midi_parser.TPQN)
# note0 = played_note_L[0]
# print(tick2frm(note0[1]),note0)
# print(mp.USPQN)

# a = [1,1,1,1,2,2,2,2,3,3,4,5,5]
# counter = collections.Counter(pit_L)

# for key,val in zip(counter.keys(),counter.values()):
#     print(key,val)
# for i in counter.most_common():
#     print(i)


# chords = find_obj("chords","")[0]
# for i,chord in enumerate(chords.GetChildren()):
#     print(chord.GetName())
#     chord.SetName("chord_{:03}".format(i+21))
    # print(chord.GetName())

# for key in keys:
#     print(key.GetName())


# def init_arms_position():
#     pass
    # print(get_rel_pos(find_obj))
    # print(get_rel_pos(arms_l[0]))

# anchor_chord = [60,64,67,]
# init_arms_position()

# for chord in chord_L:
#     # print(chord.GetName())
#     if int(chord.GetName()[-3:]) % 12 ==0:
#         chord[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(1,1,1)
# print(get_rel_pos_desc_id())
# level_1_1 = c4d.ID_BASEOBJECT_REL_POSITION
# level_1 = c4d.DescLevel(level_1_1,c4d.DTYPE_VECTOR,0)
# desc_id = c4d.DescID(level_1)
# print(level_1_1,level_1,desc_id)
# print(chord_L[-1][get_rel_pos_desc_id()])

# set_key_with_id(arm_L[0],get_rel_pos_desc_id(dim=0),900)
# print(arm_L[0][get_rel_pos_desc_id(dim=0)])
# for chord in chord_L:
#     chord[c4d.ID_BASEOBJECT_COLOR]  = c4d.Vector(1,1,1)

for note in played_note_L:
    # start,dura,chan_num,pit,vel
    start,dura,chan_num,pit_num,vel = note
    chord_idx = pit_num - 21
    set_key_with_id(chord_L[chord_idx],c4d.ID_BASEOBJECT_COLOR,c4d.Vector(1,1,1),frm=sec2frm(start)-1)
    set_key_with_id(chord_L[chord_idx],c4d.ID_BASEOBJECT_COLOR,c4d.Vector(1,0,0),frm=sec2frm(start))
    # set_key_with_id(chord_L[chord_idx],c4d.ID_BASEOBJECT_COLOR,c4d.Vector(1,0,0),frm=sec2frm(start+dura//3))
    set_key_with_id(chord_L[chord_idx],c4d.ID_BASEOBJECT_COLOR,c4d.Vector(1,0,0),frm=sec2frm(start+dura))
    set_key_with_id(chord_L[chord_idx],c4d.ID_BASEOBJECT_COLOR,c4d.Vector(1,1,1),frm=sec2frm(start+dura)+1)
    # print(sec2frm(start),sec2frm(start+dura),sec2frm(dura),pit_num)

# print(get_key_with_id(chord_L[0],c4d.ID_BASEOBJECT_COLOR,frm=0).GetValue())
# set_key_with_id(chord_L[0],c4d.ID_BASEOBJECT_COLOR,val=c4d.Vector(0,1,0),frm=30)
# print(get_key_with_id(chord_L[0],(c4d.ID_BASEOBJECT_COLOR,c4d.VECTOR_Y),frm=0).GetValue())

# print(TPQN,USPQN)

# chord_L[0][c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(1,0,0)

event_add()

