import os
import time
from p5 import setup, draw, run
import p5 as pf
vec = pf.Vector

def setup():
    # print("start p5 at {}".format(time.time()))
    start = vec(306, 72)
    control_1 = vec(36, 36)
    control_2 = vec(324, 324)
    end = vec(54, 288)
    # bp = pf.bezier_point(start, control_1, control_2, end, 0.5)
    # print(bp.x)
    # print(bp.y)


frm_path = "./frames/"
if not os.path.exists(frm_path):
    os.mkdir(frm_path)
def draw():
    # print("Elapsed: {}s".format)
    # print(frm)
    # pf.circle([10,10],5)
    pf.bezier([0,0],[100,100],[200,300],[200,300])
    pf.save_frame(frm_path + "screen.png")
    # pf.no_loop()
    # pass

def main():
    run(frame_rate = 10)

if __name__ == '__main__':
    main()
