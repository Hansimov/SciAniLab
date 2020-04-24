# * multiprocessing — Process-based parallelism — Python 3.7.7 documentation 
# ** https://docs.python.org/3.7/library/multiprocessing.html

import os
from multiprocessing import Pool, Process

# def square(x):
#     return x*x

# if __name__ == "__main__":
#     with Pool(4) as p:
#         print(p.map(square,list(range(0,20))))

def info(title):
    print(title)
    print("module name: ", __name__)
    print("parent process: ", os.getppid())
    print("process id: ", os.getpid())
def outname(name):
    print("hello, ", name)

if __name__ == '__main__':
    info("main line")
    p = Process(target=outname,args=("bob",))
    p.start()
    p.join()