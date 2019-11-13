import threading
import time

def showfun(n):
    print("%s start -- %d"%(time.ctime(),n))
    print("working")
    time.sleep(2)
    print("%s end -- %d" % (time.ctime(), n))
    semlock.release()

if __name__ == '__main__':
    maxconnections = 5
    semlock = threading.BoundedSemaphore(maxconnections)
    list=[]
    for i in range(8):
        semlock.acquire()
        t = threading.Thread(target=showfun, args=(i,))
        list.append(t)
        t.start()