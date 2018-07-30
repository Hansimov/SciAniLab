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
            '\\node [fill={{rgb,1: red,{}; green,{}; blue,{}}}, shape=circle, minimum size={}] ({}) at ({},{}) {{}};' \
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
                '\\node [text={{rgb,1: red,{}; green,{}; blue,{}}}, shape=rectangle, font=\\fs{{{}}}, inner sep=3, opacity={}] ({}) at ({},{}) {{{}}};' \
                    .format(self.color[0], self.color[1], self.color[2], \
                            15+2*(10-self.shake_cnt), self.shake_cnt/self.shake_cnt_max-0.2,\
                            this_region.pinyin, this_region.x, this_region.y, this_region.name)
            ]
            self.shake_cnt -= 1
            printTex(tmp_cmds)

    # def draw(self):
    #     self.display()
    #     self.halo()
