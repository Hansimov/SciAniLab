# encoding: utf-8

# * Correct Piano Fingering: The Why and How 
# ** https://www.onlinepianocoach.com/piano-fingering.html

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
# process_midi(path_to_add+"abc.mid")
process_midi(path_to_add+"secret1.mid")

