from _tikzEnv import *
from _initVariable import *

rgnclr = {} # region color

rgnclr['donghua']  = [0.5, 0.5,  1 ]
rgnclr['yinyue']   = [ 1 ,  1 ,  0 ]
rgnclr['wudao']    = [ 1 , 0.5,  0 ]
rgnclr['youxi']    = [ 1 , 0.1 ,0.1]
rgnclr['keji']     = [ 0 , 0.5,  1 ]
rgnclr['shenghuo'] = [ 0 , 0.5,  0 ]
rgnclr['guichu']   = [0.5,  1 ,  1 ]
rgnclr['qita']     = [ 1 , 0.5,  1 ]

rgnname = ['动画','音乐','舞蹈','游戏','科技','生活','鬼畜','其他']
rgnpinyin = ['donghua','yinyue','wudao','youxi','keji','shenghuo','guichu','qita']

class RegionBlock(object):
    def display(self):
        tmp_cmds = [
            '\\node [text={{rgb,1: red,{}; green,{}; blue,{}}}, shape=rectangle, font=\\fs{{15}}, inner sep=3] ({}) at ({},{}) {{{}}};' \
                .format(self.color[0], self.color[1], self.color[2], self.pinyin, self.x, self.y, self.name)
        ]
        printTex(tmp_cmds)

region_all = {}
def initRegion():
    global region_all
    rgn_cnt = 0
    for clrkey, name, pinyin in zip(rgnclr, rgnname, rgnpinyin):
        region_tmp = RegionBlock()
        region_tmp.color = rgnclr[pinyin]
        region_tmp.name = name
        region_tmp.pinyin = pinyin
        region_tmp.x = width - 80
        region_tmp.y = height - 100 - 30 * rgn_cnt
        region_all[pinyin] = region_tmp
        rgn_cnt += 1

initRegion()

def drawRegion():
    for _ , region_tmp in region_all.items():
        region_tmp.display()

class VideoPoint(object):
    # def __init__(self, view=-1, videos=-1, view_avg=-1, title ='', aid=-1, name='', mid=-1, pubdate={}, tid=-1):
    #     self.view, self.videos, self.view_avg = view, videos, view_avg
    #     self.title = title
    #     self.pubdate = pubdate
    #     self.aid, self.tid = aid, tid
    #     self.name, self.mid = name, mid

    def __init__(self):
        self.halo_cnt_max = 15
        self.halo_cnt = self.halo_cnt_max
        self.laser_cnt_max = 15
        self.laser_cnt = self.laser_cnt_max
        self.shake_cnt_max = 10
        self.shake_cnt = self.shake_cnt_max

    @property
    def tid(self):
        return self._tid
    @tid.setter
    def tid(self, val):
        self._tid = val
        self.calcRegion()

    @property
    def view_avg(self):
        return self._view_avg
    @view_avg.setter
    def view_avg(self, val):
        self._view_avg = val
        self.calcRadius()

    def calcRadius(self):
        self.radius = 10 * self.view_avg / 5e6

    def calcRegion(self):
        # https://github.com/uupers/BiliSpider/wiki/%E8%A7%86%E9%A2%91%E5%88%86%E5%8C%BA%E5%AF%B9%E5%BA%94%E8%A1%A8
        # 动画： 0.5  0.5  1
        #     动画： 0.5  0.5  1
        #     番剧： 0.5  0.5  1
        #     国创： 0.5  0.5  1

        # 音乐：  1    1   0
        # 舞蹈：  1   0.5  0
        # 游戏：  1    0   0
        # 科技：  0   0.5  1
        # 生活：  0   0.5  0 
        # 鬼畜： 0.5   1   1
        # 其他：  1   0.5  1
        #     时尚：  1   0.5  1
        #     广告：  1   0.5  1 
        #     娱乐：  1   0.5  1
        #     影视：  1   0.5  1
        #     放映：  1   0.5  1

        # 动画：动画 + 番剧 + 国创
        if  self.tid in [1, 24, 25, 47, 27,  13, 33, 32, 51, 152,  167, 153, 168, 169, 179]:
            self.region = 'donghua'
        # 音乐
        elif self.tid in [3, 28, 31, 30, 59, 29, 54, 130]:
            self.region = 'yinyue'
        # 舞蹈
        elif self.tid in [129, 29, 154, 156]:
            self.region = 'wudao'
        # 游戏
        elif self.tid in [4, 17, 171, 172, 65, 173, 121, 136, 19]:
            self.region = 'youxi'
        # 科技
        elif self.tid in [36, 124, 122, 39, 96, 95, 98, 176]:
            self.region = 'keji'
        # 生活
        elif self.tid in [160, 138, 21, 76, 75, 161, 162, 175, 163, 174]:
            self.region = 'shenghuo'
        # 鬼畜
        elif self.tid in [119, 22, 26, 126, 127]:
            self.region = 'guichu'
        # 其他：娱乐 + 广告 + 影视 + 时尚 + 放映厅
        else:
            self.region = 'qita'

        self.color = rgnclr[self.region]

    def display(self):
        tmp_cmds = [
            '\\node [fill={{rgb,1: red,{}; green,{}; blue,{}}}, shape=circle, minimum size={}, opacity=0.8] ({}) at ({},{}) {{}};' \
                .format(self.color[0], self.color[1], self.color[2], 2*self.radius, self.aid, self.x, self.y)
        ]
        printTex(tmp_cmds)

    def halo(self):
        if self.halo_cnt > 0:
            tmp_cmds = [
                '\\draw [fill={{rgb,1: red,{}; green,{}; blue,{}}}, even odd rule, opacity={}]  ({},{}) circle ({}) ({},{}) circle ({});' \
                    .format(self.color[0], self.color[1], self.color[2], self.halo_cnt/self.halo_cnt_max, \
                            self.x, self.y, self.radius*(1+(1-self.halo_cnt/self.halo_cnt_max)+0.6), \
                            self.x, self.y, self.radius*(1+(1-self.halo_cnt/self.halo_cnt_max)+0.1))
            ]
            self.halo_cnt -= 1
            printTex(tmp_cmds)
    def laser(self):
        if self.laser_cnt > 0:
            tmp_cmds = [
                # '\\draw [draw={{rgb,1: red,{}; green,{}; blue,{}}}, opacity={}, line width={}] ({}) -- ({});'\
                    # .format(self.color[0], self.color[1], self.color[2], self.laser_cnt/self.laser_cnt_max, \
                    #         self.region, self.radius, self.region, self.aid)
                '\\fill [fill={{rgb,1: red,{}; green,{}; blue,{}}}, opacity={}] ({}.west) -- (tangent cs:node={},point={{({}.west)}},solution=1) -- ({}.center) -- (tangent cs:node={},point={{({}.west)}}, solution=2) -- cycle;'\
                    .format(self.color[0], self.color[1], self.color[2], self.laser_cnt/self.laser_cnt_max-0.1, \
                            self.region, self.aid, self.region, self.aid, self.aid, self.region)
            ]
            self.laser_cnt -= 1
            printTex(tmp_cmds)

    def shake(self):
        if self.shake_cnt > 0:
            this_region = region_all[self.region]
            tmp_cmds = [
                '\\node [text={{rgb,1: red,{}; green,{}; blue,{}}}, shape=rectangle, font=\\fs{{{}}}, inner sep=3, opacity={}] at ({},{}) {{{}}};' \
                    .format(self.color[0], self.color[1], self.color[2], \
                            15+2*(self.shake_cnt_max-self.shake_cnt), self.shake_cnt/self.shake_cnt_max-0.2,\
                            this_region.x, this_region.y, this_region.name)
            ]
            self.shake_cnt -= 1
            printTex(tmp_cmds)

class HitBox(object):
    def __init__(self):
        self.hit_cnt_max = 15
        self.hit_cnt = self.hit_cnt_max

    def hit(self):
        if self.hit_cnt > 0:
            tmp_cmds = [
                '\\node [text={{rgb,1: red,{}; green,{}; blue,{}}}, shape=rectangle, font=\\fs{{{}}}, anchor=west, inner sep=5, opacity={}] ({}) at ({},{}) {{{}}};' \
                    .format(self.color[0], self.color[1], self.color[2], 30, self.hit_cnt/self.hit_cnt_max,\
                            'hit', axis_l, axis_t+40, 'HITs'),
                '\\node [text={{rgb,1: red,{}; green,{}; blue,{}}}, shape=rectangle, font=\\fs{{{}}}, align=right, anchor=east, inner sep=5, opacity={}] at ({}.west) {{{}}};' \
                    .format(self.color[0], self.color[1], self.color[2], 30, self.hit_cnt/self.hit_cnt_max,\
                            'hit', '{}'.format(self.num))
            ]
            self.hit_cnt -= 1
            printTex(tmp_cmds)

class LevelBoard(object):
    def __init__(self):
        self.highlight_cnt_max = 40
        self.highlight_cnt = self.highlight_cnt_max

    def highlight(self):
        if   self.level == 3:
            # print(name, level, 'Triple Kill !')
            # print(name, level, 'Killing spree!')
            self.adj_en = 'Killing spree!'
            self.adj_zh = '正在大杀特杀！'
        elif self.level == 4:
            # print(name, level, 'Quodra Kill!')
            # print(name, level, 'Rampage!')
            self.adj_en = 'Rampage!'
            self.adj_zh = '接近暴走了！'
        elif self.level == 5:
            # print(name, level, 'Penta Kill !')
            # print(name, level, 'Unstoppable!')
            self.adj_en = 'Unstoppable!'
            self.adj_zh = '已经无人能挡了！'
        elif self.level == 6:
            # print(name, level, 'Hexa Kill !')
            # print(name, level, 'Dominating!')
            self.adj_en = 'Dominating!'
            self.adj_zh = '已经主宰比赛了！'
        elif self.level == 7:
            # print(name, level, 'Godlike!')
            self.adj_en = 'Godlike!'
            self.adj_zh = '已经接近神了！'
        elif self.level >= 8:
            # print(name, level, 'Legendary!')
            self.adj_en = 'Legendary!'
            self.adj_zh = '已经超神了！'

        if self.level >= 3:
            tmp_cmds = [
                '\\node [text={{rgb,1: red,{}; green,{}; blue,{}}}, shape=rectangle, font=\\hupo\\hupozh\\fs{{{}}}, align=center, anchor=center, inner sep=5, opacity={}] at ({},{}) {{{}}};' \
                            .format(self.color[0], self.color[1], self.color[2], 60,\
                                self.highlight_cnt/self.highlight_cnt_max, width/2, height*3/5, \
                                str(self.level)+ '连击' + '\\\\ \\vspace*{40pt}\\\\ ' + region_all[self.region].name+'区'+self.adj_zh +'\\\\ \\vspace*{40pt}\\\\ ' + self.adj_en.upper())
            ]
            self.highlight_cnt -= 1
            printTex(tmp_cmds)

# League of Legends Wiki - Kill
#   http://leagueoflegends.wikia.com/wiki/Kill
# Penta kill - 百度百科
#   https://baike.baidu.com/item/Penta%20kill
# 双杀是 (enemy) Double kill
# 三杀是 (enemy) Triple kill
# 四杀是 (enemy) Quadra kill
# 五杀是 (enemy) Penta kill
# 六杀是 (enemy) Hexa kill (只有在活动“六杀争夺战”活动中得到)
# 如果是敌方玩家得到连杀，音效会在前面多加 Enemy

# 一血是 First blood
# 第三个 Killing Spree (正在大杀特杀)
# 第四个 rampage (接近暴走了)
# 第五个 unstoppable (已经无人能挡了)
# 第六个 dominating (已经主宰比赛了)
# 第七个 (An enemy is) godlike (已经接近神了)
# 第八个 (An enemy is) legendary (已经超神了)

# Great  Amazing  UnbilePerfect

# Choosing Natural Adjective Ladders
# http://www.mcdonald.me.uk/storytelling/lichert_article.htm
# = Adjective     mean   SD  = #
#   Phenomenal    9.5    1.2
#   World-Class   9.5    0.6
#   Incredible    9.0    0.9
#   Amazing       8.9    1.0
#   Exceptional   8.7    1.1
#   Excellent     8.3    1.0
#   Superior      8.2    1.0
#   Great         8.0    1.1
#   Good          6.9    1.1
#   Fine          6.6    1.2
#   Decent        6.2    0.9
#   Fair          5.4    0.9
#   Middling      5.0    0.8
#   Mediocre      4.4    0.9
#   Limited       3.8    1.0
#   Weak          3.4    0.9
#   Deficient     3.2    0.9
#   Inferior      3.1    1.0
#   Poor          2.9    1.1
#   Bad           2.6    1.0
#   Awful         1.9    0.9
#   Terrible      1.8    1.3
#   Dreadful      1.9    0.9
#   Abysmal       1.3    0.8
  