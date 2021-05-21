import os
import time

import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()

def main():
    time.sleep(0.4)
    print("hello")
main()

pr.disable()
s = io.StringIO()
sortby = "cumulative"
sortby = "tottime"
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())