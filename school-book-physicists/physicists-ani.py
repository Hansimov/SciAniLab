import cairo
import os
import math
from time import sleep

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mplimg

width, height = 1280, 720


def drawImage(img_x, img_y, num):
    imgsfc = cairo.ImageSurface(cairo.FORMAT_ARGB32,width,height)
    ctx = cairo.Context(imgsfc)
    # pdfsfc = cairo.PDFSurface('physicists-ani.pdf', width, height)
    # ctx = cairo.Context(pdfsfc)

    img = imgsfc.create_from_png('./images/newton.png')

    ctx.set_source_surface(img, img_x, img_y)
    ctx.paint()

    imgsfc.write_to_png('./frames/physicists-ani-{:0>3}.png'.format(num))

def dispImage(img_filename):
    mpl.rcParams['toolbar'] = 'None'

    # fig = plt.figure(figsize=(width,height), dpi=1)
    # fig.canvas.set_window_title('Test')

    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.axis('off')

    img_disp = mplimg.imread(img_filename)
    imgplot = plt.imshow(img_disp)

    plt.show()

    # from PIL import Image
    # img_disp = Image.open('physicists-ani.png')
    # img_disp.show()

def main():
    for i in range(0,100):
        img_filename = './frames/physicists-ani-{:0>3}.png'.format(i)
        print('Rendering image: {:0>3}'.format(i))
        drawImage(i*4, i*3, i)
    # dispImage(img_filename)
    return img_filename

if __name__ == '__main__':
    img_filename = main()
    irfan    = 'C:/MySoftwares/IrfanView/i_view64.exe'
    img_path = os.path.abspath(img_filename)
    os.system(irfan + ' ' + img_path)
