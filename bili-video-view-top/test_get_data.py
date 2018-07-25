import csv

video_static_file = './data/video_static.csv'              # header = False, all string
# aid, tid, videos, pubdate, mid, copyright, duration, title, pic

video_top_file = './data/video_dynamic_180723_top1000.csv' # header = True,  all numeric
# aid, view[, danmaku, reply, favorite, coin, share, like, dislike]

# up_data
# mid, name, sex, regtime, birthday, sign, face, level, vipStatus, vipType


# up 头像
# https://i0.hdslb.com/bfs/face/
# 视频封面
# https://i2.hdslb.com/bfs/archive/

# select s.aid, d.view, s.tid, s.videos, s.pubdate, s.copyright, s.duration, s.title, s.pic, s.mid, up.name from
# (select aid, view from video_dynamic_180723 order by view desc limit 5000) as d,
# (select aid, tid, videos, pubdate, mid, copyright, duration, title, pic from video_static) as s,
# (select mid, name from up_data) as up
# where d.aid=s.aid and s.mid=up.mid

# select d.view, s.videos, d.view / s.videos as view_avg, s.title, s.aid, up.name, s.mid, s.pubdate, s.tid, s.duration, s.copyright, s.pic, up.face from
# (select aid, view from video_dynamic_180723) as d,
# (select * from video_static) as s,
# (select mid, name, face from up_data) as up
# where d.aid=s.aid and s.mid=up.mid
# order by view_avg desc limit 2000


# 视频id、up主id、播放量、收藏量、硬币量、弹幕量、视频标题、封面地址

# select d.view, s.videos, d.coin, d.favorite, d.danmaku, s.title, s.aid, up.name, up.mid, s.pubdate, s.tid, s.duration, s.copyright, s.pic, up.face from
# (select * from video_dynamic_180725 order by view) as d,
# (select * from video_static) as s,
# (select * from up_data) as up
# where (d.aid=s.aid and s.mid=up.mid and (d.view<0 or d.view>=100000))

# select d.view, s.videos, d.coin, s.title, d.favorite, d.danmaku, s.aid, up.name, up.mid, s.pubdate, s.tid, s.duration, s.copyright, s.pic, up.face from
# (select * from video_dynamic_180725 order by view desc limit 200000) as d,
# (select * from video_static) as s,
# (select * from up_data) as up
# where (d.aid=s.aid and s.mid=up.mid and d.view>=1000000)


# # Errors
# CREATE TABLE `up_data` (
#   `mid` int(11) NOT NULL,
#   `name` varchar(80) DEFAULT NULL,
#   `sex` tinyint(4) DEFAULT NULL,
#   `regtime` char(50) DEFAULT NULL,
#   `birthday` date DEFAULT NULL,
#   `sign` varchar(100) DEFAULT NULL,
#   `face` char(50) DEFAULT NULL,
#   `level` tinyint(4) DEFAULT NULL,
#   `vipStatus` tinyint(4) DEFAULT NULL,
#   `vipType` tinyint(4) DEFAULT NULL,
#   PRIMARY KEY (`mid`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

# CREATE TABLE `video_dynamic_180724` (
#   `aid` int(11) NOT NULL,
#   `view` int(11) DEFAULT NULL,
#   `danmaku` int(11) DEFAULT NULL,
#   `reply` int(11) DEFAULT NULL,
#   `favorite` int(11) DEFAULT NULL,
#   `coin` int(11) DEFAULT NULL,
#   `share` int(11) DEFAULT NULL,
#   `like` int(11) DEFAULT NULL,
#   `dislike` int(11) DEFAULT NULL,
#   PRIMARY KEY (`aid`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

# # Work!
# LOAD DATA 
#     INFILE 'F:/Sources/git/SciAniLab/bili-video-view-top/data/video_dynamic_180724.csv' 
#     INTO TABLE video_dynamic_180724 
#     FIELDS TERMINATED BY ','
#     OPTIONALLY ENCLOSED BY '"'
#     LINES TERMINATED BY '\r\n'
#     IGNORE 1 LINES
# ;

# -- show variables like '%secure%';


# (@vmid,@vname,@vsex,@vregtime,@vbirthday,@vsign,@vface,@vlevel,@vvipStatus,@vvipType)

