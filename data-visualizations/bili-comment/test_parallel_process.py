from multiprocessing import Process, Manager
import random
import time
import threading

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]


def add_ip(ip_L, add_ip_sema, add_ip_lock):
    add_ip_sema.acquire()
    time.sleep(0.5)

    add_ip_lock.acquire()
    if ip_L[0] <= 50:
        ip = ip_L[0]+1
        ip_L.append(ip)
        ip_L[0] += 1
        print("Add ip {}".format(ip))
        # print("New ip_L:", ip_L)

    add_ip_lock.release()
    add_ip_sema.release()

def get_ip(ip_L,use_ip_lock):
    # print("Getting ip")
    # p_lock.acquire()
    # while ip_L == []:
    #     p_lock.release()
    #     print("ip_L is empty!")
    #     print(ip_L)
    #     time.sleep(0.5)
    #     p_lock.acquire()
    use_ip_lock.acquire()
    if len(ip_L)<=1:
        use_ip_lock.release()
        # print("ip_L is empty!")
        return -1

    ip = ip_L[1]
    ip_L.pop(1)
    print("Get ip {}".format(ip))
    # print("Reamining ip_L", ip_L)
    use_ip_lock.release()
    return ip

def put_back_ip(ip, ip_L, use_ip_lock):
    use_ip_lock.acquire()
    print("Put back ip {}".format(ip))
    ip_L.append(ip)
    use_ip_lock.release()

def use_ip(thread_num, ip_L, use_ip_sema, use_ip_lock):
    use_ip_sema.acquire()
    print("- Thread {}".format(thread_num))
    ip = get_ip(ip_L, use_ip_lock)
    while ip == -1:
        time.sleep(0.2)
        ip = get_ip(ip_L, use_ip_lock)

    print("Using ip {}".format(ip))
    time.sleep(2)

    put_back_ip(ip, ip_L, use_ip_lock)
    use_ip_sema.release()

# p_lock = multiprocessing.Lock()

def run_use_ip_threads(ip_L):
    use_ip_lock = threading.Lock()
    use_ip_sema_num_max = 15
    use_ip_sema = threading.BoundedSemaphore(use_ip_sema_num_max)
    pool = []
    for i in range(100):
        tmp_thread = threading.Thread(target=use_ip, args=(i+1,ip_L,use_ip_sema,use_ip_lock), daemon=True)
        pool.append(tmp_thread)

    for tmp_thread in pool:
        tmp_thread.start()

    while is_any_thread_alive(pool):
        time.sleep(0)


def run_add_ip_threads(ip_L):
    add_ip_sema_num_max = 20
    add_ip_sema = threading.BoundedSemaphore(add_ip_sema_num_max)
    add_ip_lock = threading.Lock()
    pool = []
    for i in range(40):
        tmp_thread = threading.Thread(target=add_ip, args=(ip_L, add_ip_sema, add_ip_lock), daemon=True)
        pool.append(tmp_thread)

    for tmp_thread in pool:
        tmp_thread.start()

    while is_any_thread_alive(pool):
        time.sleep(0)

if __name__ == '__main__':
    t1 = time.time()
    manager = Manager()
    ip_L = manager.list([4,1,2,3,4])
    p1 = Process(target=run_add_ip_threads,args=(ip_L,))
    p2 = Process(target=run_use_ip_threads,args=(ip_L,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    t2 = time.time()
    print("Elapsed time: {}s".format(round(t2-t1,1)))