import time, threading
import random


def singlePrint():
    print('{} is running'.format(threading.current_thread().name))
    time.sleep(random.random())
    print('{} is ended'.format(threading.current_thread().name))

def parallelPrint(num):
    thread_pool = []
    for i in range(1,num+1):
        thread_name = 'mythread--{:0>4d}'.format(i)
        tmp = threading.Thread(target=singlePrint,name=thread_name)
        thread_pool.append(tmp)
    return thread_pool

thread_pool = parallelPrint(10)

for thrd in thread_pool:
    thrd.start()

for thrd in thread_pool:
    thrd.join()


# ------------------------------------ #

# import time, threading

# # 新线程执行的代码:
# def loop():
#     print('thread %s is running...' % threading.current_thread().name)
#     n = 0
#     while n < 5:
#         n = n + 1
#         print('thread %s >>> %s' % (threading.current_thread().name, n))
#         time.sleep(1)
#     print('thread %s ended.' % threading.current_thread().name)

# print('thread %s is running...' % threading.current_thread().name)
# t = threading.Thread(target=loop, name='LoopThread')
# t.start()
# t.join()
# print('thread %s ended.' % threading.current_thread().name)

# ------------------------------------ #

# import threading
# import time

# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print ("开启线程： " + self.name)
#         # 获取锁，用于线程同步
#         threadLock.acquire()
#         print_time(self.name, self.counter, 3)
#         # 释放锁，开启下一个线程
#         threadLock.release()

# def print_time(threadName, delay, counter):
#     while counter:
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1

# threadLock = threading.Lock()
# threads = []

# # 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)

# # 开启新线程
# thread1.start()
# thread2.start()

# # 添加线程到线程列表
# threads.append(thread1)
# threads.append(thread2)

# # 等待所有线程完成
# for t in threads:
#     t.join()
# print ("退出主线程")