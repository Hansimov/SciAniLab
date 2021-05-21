import requests
import time
import threading
import random
import os.path

img_link_body_list = [ 'http://res.ajiao.com/uploadfiles/Book/255/{}_838x979.jpg', # 1-101
                       'http://res.ajiao.com/uploadfiles/Book/276/{}_838x979.jpg'  # 1-87
                    ]
img_num = [101, 87]
remaining_num = 0

for num in img_num:
    remaining_num = remaining_num + num
total_num = remaining_num

def getImage(img_link, img_name, retry_count=0):
    global remaining_num, total_num
    # time.sleep(5*random.random())
    # print('img_link:{}, img_name:{}'.format(img_link,img_name))
    if os.path.exists(img_name):
        print('+++ Existed: {}'.format(img_name))
        remaining_num = remaining_num - 1
        print('Remaining: {:0>3d}/{:0>3d}'.format(remaining_num, total_num))
        return

    try:
        print('>>> Getting image: {}'.format(img_link))
        img = requests.get(img_link)
    except Exception as e:
        # print(e)
        retry_count = retry_count + 1
        if retry_count >= 5:
            print('--- Exceeded retry limits: {}'.format(img_name))
            return
        else:
            print('*** Retry {} times to get: {} ...'.format(retry_count, img_name))
            getImage(img_link, img_name, retry_count)
    else:
        with open(img_name, 'wb') as img_file:
            img_file.write(img.content)
        print('+++ Successfully dumped: {}'.format(img_name))
        remaining_num = remaining_num - 1
        print('Remaining: {:0>3d}/{:0>3d}'.format(remaining_num, total_num))

def createThreads(num, img_link_body, idx):
    thread_pool = []
    print('Creating Threads: {}'.format(img_link_body))
    for i in range(1,num+1):
        img_link = img_link_body.format(i)
        img_name = 'books/bx{}/{:0>3d}.jpg'.format(idx+1, i)
        tmp = threading.Thread(target=getImage, args=[img_link, img_name])
        thread_pool.append(tmp)
    return thread_pool

def startThreads(thread_pool):
    for thrd in thread_pool:
        thrd.daemon = True
        thrd.start()

def joinThreads(thread_pool):
    for thrd in thread_pool:
        thrd.join()

if __name__ == '__main__':

    thread_pool_list = []
    for idx, img_link_body in enumerate(img_link_body_list):
        thread_pool = createThreads(img_num[idx], img_link_body, idx)
        thread_pool_list.append(thread_pool)

    for thread_pool in thread_pool_list:
        startThreads(thread_pool)

    for thread_pool in thread_pool_list:
        joinThreads(thread_pool)

    # while True:
    #     time.sleep(1)


