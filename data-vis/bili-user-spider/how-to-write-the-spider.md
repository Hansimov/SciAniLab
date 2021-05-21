## 用户信息
`https://space.bilibili.com/ajax/member/GetInfo`

### 输入：

Header
- Content-Type => 请求类型，eg： application/x-www-form-urlencoded; charset=UTF-8
- Referer => 上一跳地址，格式：https://space.bilibili.com/{mid}/ ，eg：https://space.bilibili.com/2654670/

Body
- mid => 用户ID， eg：2654670
- csrf => 防跨域攻击签名，对应cookie中 key=bili_jct 的数据, eg: 3600d0307c09615eb75ca5ec42ac565a

PS: 本API必须使用POST请求, cookie中必须包含key=bili_jct 的数据

### 输出 Post：
```
{
    "status": true,
    "data": {
        "mid": "2654670",   //用户信息
        "name": "LePtC",    //用户名
        "approve": false,   
        "sex": "保密",    //性别
        "rank": "10000",    //等级
        "face":     "http://i1.hdslb.com/bfs/face/3a2799018636c9c43774dd7bf6685387bb219011.jpg",    //头像
        "DisplayRank": "10000",
        "regtime": 1382895515, //注册时间
        "spacesta": 0,
        "birthday": "0000-01-01",
        "place": "",
        "description": "",
        "article": 0,
        "sign": "学物理的都好萌～", //签名
        "level_info": {
            "current_level": 5,
            "current_min": 10800,
            "current_exp": 14312,
            "next_exp": 28800
        },
        "pendant": {
            "pid": 0,
            "name": "",
            "image": "",
            "expire": 0
        },
        "nameplate": {
            "nid": 0,
            "name": "",
            "image": "",
            "image_small": "",
            "level": "",
            "condition": ""
        },
        "official_verify": {
            "type": -1,
            "desc": ""
        },
        "vip": {
            "vipType": 1,
            "vipDueDate": 1491235200000,
            "dueRemark": "",
            "accessStatus": 1,
            "vipStatus": 0,
            "vipStatusWarn": ""
        },
        "toutu": "bfs/space/c9dae917e24b4fc17c4d544caf6b6c0b17f8692b.jpg",
        "toutuId": 3,
        "theme": "default",
        "theme_preview": "",
        "coins": 0,
        "im9_sign": "6159621e1268bab1c81824f21bb5ae2c",
        "playNum": 210014,
        "fans_badge": false
    }
}
```



### Post
{
    "status":true,
    "data":{
        "mid":"15870477",
        "name":"IAsimov",
        "approve":false,
        "sex":"\u4fdd\u5bc6",
        "rank":"10000",
        "face":"http:\/\/i1.hdslb.com\/bfs\/face\/edc89e05e79c65ecb190678c05f3018eedcccc36.jpg",
        "DisplayRank":"10000",
        "regtime":1444813638,
        "spacesta":0,
        "birthday":"0000-01-01",
        "place":"",
        "description":"",
        "article":0,
        "sign":"Scientific Animations",
        "level_info":{
            "current_level":4,
            "current_min":4500,
            "current_exp":7954,
            "next_exp":10800
        },
        "pendant":{
            "pid":0,
            "name":"",
            "image":"",
            "expire":0
        },
        "nameplate":{
            "nid":0,
            "name":"",
            "image":"",
            "image_small":"",
            "level":"",
            "condition":""
        },
        "official_verify":{
            "type":-1,
            "desc":""
        },
        "vip":{
            "vipType":0,
            "vipDueDate":0,
            "dueRemark":"",
            "accessStatus":1,
            "vipStatus":0,
            "vipStatusWarn":""
        },
        "toutu":"bfs\/space\/1f4eaf70d1bb981f6057b3e440249d7a1f65774f.jpg",
        "toutuId":4,
        "theme":"default",
        "theme_preview":"",
        "im9_sign":"8823a6d8dcc8e65289e45e15d5d7f07c",
        "playNum":2817,
        "fans_badge":false
    }
}


### Get
{
    "code":0,
    "message":"0",
    "ttl":1,
    "data":{
        "card":
        {
            "mid":"15870477",
            "name":"IAsimov",
            "approve":false,
            "sex":"保密",
            "rank":"10000",
            "face":"http://i2.hdslb.com/bfs/face/edc89e05e79c65ecb190678c05f3018eedcccc36.jpg",
            "DisplayRank":"0",
            "regtime":0,
            "spacesta":0,
            "birthday":"",
            "place":"",
            "description":"",
            "article":0,
            "attentions":[12306331,488744,14593294,26728556,261192708,2654670,10707223,2374194,22502833,1388774,288239,11383630,27062311,5096780,775788,145716,97177641,389088,5382268,4163591,26798384,125357401,10050850,10783631,3557916,28266043,14254182,7349,261036,802255,88461692,20503549,75304607,13974176,730732,6997378,249118,301940,56704364,7771992,234256,1398957,2835818,433351,122879,1347989,20990353,28758032],
            "fans":56,
            "friend":48,
            "attention":48,
            "sign":"Scientific Animations",
            "level_info":{
                "current_level":4,
                "current_min":4500,
                "current_exp":7974,
                "next_exp":10800
            },
            "pendant":{
                "pid":0,
                "name":"",
                "image":"",
                "expire":0
            },
            "nameplate":{
                "nid":0,
                "name":"",
                "image":"",
                "image_small":"",
                "level":"",
                "condition":""
            },
            "official_verify":{
                "type":-1,
                "desc":""
            },
            "vip":{
                "vipType":0,
                "vipDueDate":0,
                "dueRemark":"",
                "accessStatus":1,
                "vipStatus":0,
                "vipStatusWarn":""
            }
        },
        "space":{
            "s_img":"http://i1.hdslb.com/bfs/space/1f4eaf70d1bb981f6057b3e440249d7a1f65774f.jpg",
            "l_img":"http://i1.hdslb.com/bfs/space/3ab888c1d149e864ab44802dea8c1443e940fa0d.png"
        },
        "following":false,
        "archive_count":1,
        "article_count":0,
        "follower":56
    }
}
