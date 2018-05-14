import requests
import time
import threading

imagelink = 'http://res.ajiao.com/uploadfiles/Book/255/101_838x979.jpg'

def getImage(img_link, img_name):
    try:
        print('Getting image: {}'.format(img_link))
        img = requests.get(img_link)
    except Exception as e:
        print(e)
    else:
        with open('books/bx1/' + img_name, 'wb') as img_file:
            img_file.write(img.content)
        print('{} successfully dumped!'.format(img_name))



if __name__ == '__main__':
    # getImage(imagelink, '101.jpg')
