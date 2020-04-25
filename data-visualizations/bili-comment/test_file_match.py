import os
import re

for filename in os.listdir():
    # name,ext = os.path.splitext(filename)
    # if ext==".html":
    if re.match("free-proxy-list[\s\S]*",filename):
        print(filename)
    # print(filename)