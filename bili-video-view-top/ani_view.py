from _videoClass import *
from _tikzEnv import *
from _initVariable import *

import pandas as pd

'''
>=300w 显示封面，<=300w 只绘制圆点
    100w+ 4103
    200w+ 932
    300w+ 388
    400w+ 161
    500w+ 70

    天数：3287 days 
          2009.07.25-2018.07.25
    帧率：60 fps
          3287 / 60 = 54.783 = 55 sec
    时长：55 * 6 = 5.5 min = 330 sec
    帧数：3287 * 6 = 19722 frm

    精度：6 帧/天 = 4 h/帧 
    速度：10 天/秒

    视频点数（4102） = 天数（3287）
    阈值：100w 
        考虑到点的分布集中在后 7/9，因此
        有效帧数：19722*7/9=15340
        两个点间隔的帧数为： 15340/4103 = 3.74

    点之间要尽可能分辨出来：
        假设点的直径为 10~20 pt，可利用的屏幕宽度为 900 pt，
        那么 900/15 = 60，
        因此屏幕上同时存在的点数不应超过 60 个
        考虑到由于点的纵坐标存在差异，因此 60 个点应该足够空旷，可以考虑增加到 100个
    如果按照同屏不能超过 100 个计算的话：
        同屏的帧数为：3.74 * 100 = 374
        用时：374/60 = 6.23 秒
        对应数据走过时长为：374/6 = 62.3 天 = 2 月
        嗯，这个值还是比较合理的
        需要留出一定的调整空间，因此同屏的现实时长范围约为 1-3 月
'''

'''
右侧分区向轴发射 -> 散射 -> 光柱 -> 闪电
圆圈周围光环 -> 尾迹 -> 相同颜色的连接 -> 积累一定数目全部消除
光环出现在坐标快消失时
分区文字闪烁 -> 重影
hit数 -> 小飞机打砖块
声音 -> 不同分区音调不同 -> 不同播放数音量不同

100-500-1000-1500-2000-3000-4000-4500

一开始就有的：
  - 分区字块、播放数纵轴、视频点颜色、Hit 数（带颜色）、到达左侧边缘光环
逐渐增加的：
  - 分区字块闪烁/重影
  - 同颜色的 Hit 数连击到一定数目（带颜色） -> good->...->perfect
  - 光柱（渐隐） -> 闪电（为了保证绘制速度和简洁性，不模拟分叉效果）
  - 视频点之间相互连接 -> 到达一定数目会消除（透明）
  - 尾迹
  - 音效：http://touchpianist.com/

'''

date_all = []

date_head = date(2018, 1, 25)
date_tail = date(2018, 7, 25)
def initDate():
    global date_all
    date_delta = date_tail - date_head

    for i in range(date_delta.days + 1):
        date_this = date_head + timedelta(days=i)
        for j in range(0, 6):
            date_tmp = {}
            date_tmp['year']  = date_this.year
            date_tmp['month'] = date_this.month
            date_tmp['day']   = date_this.day
            date_tmp['hour']  = 4*j
            date_tmp['minute']  = 0
            date_all.append(date_tmp)

date_onscreen = []
video_fadeout = []

initDate()
def drawDateAxis(date_ptr):
    global date_onscreen

    if date_ptr >= date_axis_segs+1:
        date_onscreen.pop(0)
        ptr_left = date_ptr-date_axis_segs
    else:
        ptr_left = 0

    current_date = date_all[date_ptr]
    date_onscreen.append(current_date)

    if len(video_fadeout) <= 0:
        color_tmp = [0, 0, 0]
        width_tmp = 0
    else:
        color_tmp = video_fadeout[-1].color
        width_tmp = video_fadeout[-1].radius

    tmp_cmds = []
    tmp_cmds.extend([
        '\\draw [line width=2, gray]  ({0},{2}) -- ({1},{2});'.format(axis_l, axis_r+50,axis_b,axis_t),
        f'\\draw [line width={width_tmp}, draw={{rgb,1:red,{color_tmp[0]};green,{color_tmp[1]};blue,{color_tmp[2]}}}]  ({axis_l},{axis_b}) -- ({axis_l},{axis_t});',
        # '\\draw [line width=2pt, green, opacity=0.5] ({0},{1}) -- ({0},{2});'.format(axis_r,axis_b,axis_t),
        '\\node [text=white, align=right, font=\\fs{{20}}] at ({0},{1}) {{ {2} 年 {3:0>2d} 月 {4:0>2d} 日 }};' \
            .format(1100, 680, current_date['year'], current_date['month'], current_date['day'])
        ])

    cnt = 0
    for date_tmp in date_onscreen:
        if date_tmp['hour'] == 4:
            date_tmp_x = axis_l + (axis_r-axis_l)*(1-(len(date_onscreen)-1-cnt)/(date_axis_segs))
            if date_tmp['day'] == 1:
                tmp_cmds.extend([
                    '\\node [text=white, align=center, font=\\fs{{15}}] at ({0},{1}) {{ {2}-{3:0>2d} }};' \
                        .format(date_tmp_x, axis_b-30, date_tmp['year'], date_tmp['month']),
                    '\\draw [white,line width=2] ({0},{1}) -- ({0}, {2});'.format(date_tmp_x, axis_b-10, axis_b+10)
                ])
            elif date_tmp['day'] % 5 == 0:
                tmp_cmds.extend([
                    '\\draw [gray] ({0},{1}) -- ({0}, {2});'.format(date_tmp_x, axis_b-7, axis_b+7)
                ])
            else:
                tmp_cmds.extend([
                    '\\draw [gray] ({0},{1}) -- ({0}, {2});'.format(date_tmp_x, axis_b-3, axis_b+3)
                ])

        cnt +=1

    printTex(tmp_cmds)

def drawCover():
    tmp_cmds = [
        # '\\fill [green,radius={}] ({},{}) circle;'.format(radius,80+80*sin(i*0.2),80+80*cos(i*0.2)),
        '\\fill [opacity=0.8, fill={{rgb,1: red,1; green,1; blue,0}}] ({},{}) rectangle ({}, {});'.format(cover_x, cover_y, cover_x+cover_w, cover_y+cover_h)
    ]
    printTex(tmp_cmds)

video_all = []
def initVideo():
    global video_all
    df = pd.read_csv('./data/view_gt100w_180725.CSV', sep=',')
    # view, videos, view_avg, title, coin, favorite, danmaku, aid, name, mid, pubdate, tid, duration, copyright, pic, face
    for i in range(len(df)):
        video_tmp = VideoPoint()
        video_tmp.view     = int(df['view'][i])
        video_tmp.videos   = int(df['videos'][i])
        video_tmp.view_avg = int(df['view_avg'][i])
        video_tmp.title    = str(df['title'][i])
        video_tmp.aid      = int(df['aid'][i])
        video_tmp.tid      = int(df['tid'][i])
        video_tmp.name     = str(df['name'][i])
        video_tmp.mid      = int(df['mid'][i])

        pubdate_this = datetime.strptime(df['pubdate'][i], '%Y/%m/%d %H:%M:%S')
        pubdate_tmp = {}
        pubdate_tmp['year']    = pubdate_this.year
        pubdate_tmp['month']   = pubdate_this.month
        pubdate_tmp['day']     = pubdate_this.day
        pubdate_tmp['hour']    = pubdate_this.hour
        pubdate_tmp['minute']  = pubdate_this.minute

        video_tmp.pubdate = pubdate_tmp
        video_all.append(video_tmp)
    # print('Video initialized!')

video_onscreen = []
video_ptr = 0
initVideo()

video_view_threshold = 2e6

def drawVideoPoint():
    global video_ptr

    video_onscreen_len_old = len(video_onscreen)
    pop_cnt = 0

    while (len(date_onscreen) >= 1) and compareDate(video_all[video_ptr].pubdate, date_onscreen[-1]) <= 0:
        video_this = video_all[video_ptr]

        if video_this.view_avg >= video_view_threshold and compareDate(video_this.pubdate, date_all[0]) > 0:
            # date_tmp_x = axis_l + (axis_r-axis_l)*(1-(len(date_onscreen)-1-cnt)/(date_axis_segs))
            if video_this.pubdate['day'] < date_onscreen[-1]['day']:
                video_this.x = axis_r - (axis_r-axis_l)/date_axis_segs * (24 - video_this.pubdate['hour'] - video_this.pubdate['minute']/60)
            else:
                video_this.x = axis_r - (axis_r-axis_l)/date_axis_segs * (date_onscreen[-1]['hour'] - video_this.pubdate['hour'] - video_this.pubdate['minute']/60)

            video_this.y = axis_b + (axis_t-axis_b) * 2*(1/(1+1.3**(-2*(video_this.view_avg)/video_view_threshold))-0.5)
            video_onscreen.append(video_this)
        video_ptr += 1

    # while (len(video_onscreen) >= 1) and compareDate(video_onscreen[0].pubdate, date_onscreen[0]) <= -1:
    while (len(video_onscreen) >= 1)  \
        and (compareDate(video_onscreen[0].pubdate, date_onscreen[0]) <= 0 \
             or video_onscreen[0].x <= axis_l + 1.7*(axis_r-axis_l)/(date_axis_segs)):
        video_pop = video_onscreen.pop(0)
        pop_cnt += 1
        # if video_pop.x <= axis_l + 2*(axis_r-axis_l)/date_axis_segs:
        video_fadeout.append(video_pop)

    for i in range(0, video_onscreen_len_old-pop_cnt):
        video_onscreen[i].x -= (axis_r-axis_l)/(date_axis_segs)

    for video_tmp in video_onscreen:
        video_tmp.display()
        video_tmp.laser()
        video_tmp.shake()

    fadeout_cnt = len(video_fadeout)
    idx_tmp = 0
    for i in range(0, fadeout_cnt):
        video_tmp = video_fadeout[idx_tmp]
        if video_tmp.halo_cnt < 0:
            video_fadeout.pop(idx_tmp)
        else:
            video_tmp.x = axis_l
            video_tmp.halo()
            idx_tmp += 1

    # print('Video points drawn!')

if __name__ == '__main__':
    clearTex()
    addPreamble()
    beginDoc()
    for i in range(0, 400):
        beginTikz()

        setSize(width, height, 'lb')

        drawDateAxis(i)
        drawCover()
        drawRegion()
        drawVideoPoint()

        endTikz()
    endDoc()
    compileTex()
