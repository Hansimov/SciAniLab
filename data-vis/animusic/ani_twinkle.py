from tikzpy import *

outputfile = "ani_twinkle.pdf"
width, height = 1280, 720

# pitch, start time, duration
# C#8, 0
notes = 

initTikzpy(outputfile,width=width,height=height)
node(xy=[width/2,height/2],font_size=100, text_rgba=[0,0,0.5,1], text="hello")
outputImg()

