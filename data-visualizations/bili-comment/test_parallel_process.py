import multiprocessing
import random
import time
import threading


def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]

ip_L = [1,2,3,4]
ip_cnt = len(ip_L)
def add_ip():
    global ip_L, ip_cnt
    add_ip_sema.acquire()
    time.sleep(0.6)

    p_lock.acquire()
    if ip_cnt <= 20:
        ip = ip_cnt+1
        ip_L.append(ip)
        ip_cnt += 1
        print("Add ip {}".format(ip))
        print("New ip_L:", ip_L)

    p_lock.release()
    add_ip_sema.release()

def get_ip():
    global ip_L
    # print("Getting ip")
    p_lock.acquire()
    # while ip_L == []:
    #     p_lock.release()
    #     print("ip_L is empty!")
    #     print(ip_L)
    #     time.sleep(0.5)
    #     p_lock.acquire()
    if ip_L == []:
        p_lock.release()
        print("ip_L is empty!")
        return -1

    ip = ip_L[0]
    ip_L.pop(0)
    print("Get ip {}".format(ip))
    print("Reamining ip_L", ip_L)
    p_lock.release()
    return ip

def put_back_ip(ip):
    global ip_L, ip_cnt
    p_lock.acquire()
    print("Put back ip {}".format(ip))
    ip_L.append(ip)
    p_lock.release()

def use_ip(thread_num):
    use_ip_sema.acquire()
    print("- Thread {}".format(thread_num))
    ip = get_ip()
    while ip == -1:
        time.sleep(0.5)
        ip = get_ip()

    print("Using ip {}".format(ip))
    time.sleep(2)

    put_back_ip(ip)
    use_ip_sema.release()

p_lock = multiprocessing.Lock()
use_ip_sema_num_max = 5
use_ip_sema = threading.BoundedSemaphore(use_ip_sema_num_max)
def run_use_ip_threads():
    pool = []
    for i in range(50):
        tmp_thread = threading.Thread(target=use_ip, args=(i,), daemon=True)
        pool.append(tmp_thread)

    for tmp_thread in pool:
        tmp_thread.start()

    while is_any_thread_alive(pool):
        time.sleep(0)

add_ip_sema_num_max = 5
add_ip_sema = threading.BoundedSemaphore(add_ip_sema_num_max)
def run_add_ip_threads():
    pool = []
    for i in range(40):
        tmp_thread = threading.Thread(target=add_ip, args=(), daemon=True)
        pool.append(tmp_thread)

    for tmp_thread in pool:
        tmp_thread.start()

    while is_any_thread_alive(pool):
        time.sleep(0)

if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        ip_L = manager.list()
        p1 = multiprocessing.Process(target=run_add_ip_threads,)
        p2 = multiprocessing.Process(target=run_use_ip_threads, args=ip_L)
        p1.start()
        p2.start()
