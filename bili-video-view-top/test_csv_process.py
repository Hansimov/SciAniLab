import pandas as pd
import datetime

if __name__ == '__main__':
    df = pd.read_csv('./data/view_gt100w_180725_x.CSV', sep=',')
    # view, videos, view_avg, title, coin, favorite, danmaku, aid, name, mid, pubdate, tid, duration, copyright, pic, face
    
    # for i in range(0, len(df)):
    for i in range(0, 10):
        pubdate = df['pubdate'][i]
        # 0123456789012345678
        # 2010/12/1 13:54:15
        # 2011/7/9 8:56:02
        # 2012/8/27 18:46:30
        # 2012/11/30 14:47:09
        
        this_date = datetime.datetime.strptime(pubdate,'%Y/%m/%d %H:%M:%S')

        print(this_date)
        print(this_date.year,this_date.month,this_date.day,this_date.hour,this_date.minute,this_date.second)
    '''
    view       4129416
    videos     1
    view_avg   4129416 
    title      “吔屎啦，梁非凡”非凡哥原版片段
    coin       18922
    favorite   106596
    danmuku    47168
    aid        40162
    name       着火·薫
    mid        39475
    pubdate    2010/12/1 13:54:15
    tid        74
    duration   222
    copyright  1
    pic        0013ef0670e4d60c299f118fdf0fbc4c784859b6.jpg
    face       e0620a0097022e9566e14cc61fda27b1df691ed3.gif
    '''

