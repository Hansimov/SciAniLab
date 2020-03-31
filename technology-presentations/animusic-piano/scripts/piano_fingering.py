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

import sys
path_to_add = "H:/codes/SciAniLab/technology-presentations/animusic-piano/scripts/"
if not path_to_add in sys.path:
    sys.path.append(path_to_add)

import midi_parser
import c4d_kits
reload(midi_parser)
reload(c4d_kits)
from midi_parser import *
from c4d_kits import *

clear_console()
process_midi(path_to_add+"abc.mid",info_level=1)
# process_midi(path_to_add+"secret1.mid",info_level=1)
# note: start, dura, chan_num, pit_dec, vel
# for note in played_note_L:
#     print(note)
# print(len(played_note_L))

pit_L = [note[3] for note in played_note_L]
# print(len(pit_L))
# for pit in pit_L:
#     print(pit)

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

chords = find_obj("chord_.*","chords")

arms_l = find_obj("arm_L.*","arms")
arms_r = find_obj("arm_R.*","arms")

# def init_arms_position():
#     pass
    # print(get_rel_pos(find_obj))
    # print(get_rel_pos(arms_l[0]))

# anchor_chord = [60,64,67,]
# init_arms_position()

for chord in chords:
    

chords[0][c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(1,0,0)