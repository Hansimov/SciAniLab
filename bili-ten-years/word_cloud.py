from tikzpy import *
# import tikzpy
import os
# import pandas as pd
import csv

word_freq_data = "./word-freq-data/"

fs = os.listdir(word_freq_data)

csv_reader = csv.reader(open(word_freq_data+fs[57],mode="r",encoding="utf8"),delimiter=",")
lines = list(csv_reader)

for line in lines:
    print(line)
# print(rows)
# print(len(rows))


# initTikzpy('word_cloud.pdf', width=1280, height=720)

# word1 = "你好"
# word2 = "世界"
# word3 = "TEST"

# box1 = node(xy=[200,200],text=word1,font_size=40)


# outputImg()