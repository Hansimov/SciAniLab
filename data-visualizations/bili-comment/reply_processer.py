
""" Fetch vlist
# func:  fetch_mid_vlist(mid)
# retn:  ---
# dump:  "./infos/{mid}-vlist.json"
"""

""" Parse vlist
# func:  parse_vlist(mid)
# retn:  ---
# open:  "./infos/{mid}-vlist.json"
# dump:  "./infos/{mid}-vinfo.pkl"
         vinfo: 2d list (video_num x dim)
            each row: [aid, created, title, pic_url, length]
"""


""" Fetch replies
# func:  fetch_replies(mid)
# retn:  ---
# open:  "./infos/{mid}-vinfo.pkl"
# save:  "./replies/mid-{mid}/aid-{*}/reply-{*}-{size}.json"
"""


""" Parse replies
# func:  parse_replies(mid)
# retn:  ---
# open:  "./replies/mid-{mid}/aid-{*}/reply-{*}-{size}.json"
# dump:  "./infos/{mid}-finfo.pkl"
         finfo: dict of list (x video_num)
            each key,val: {aid: flr_ct_L}
                flr_ct_L: 2d list (flr_num x 2)
                    each row: [flr_idx, ctime]
                    flr_num: total num of all floors
                    flr_idx: index of current floor
"""


""" Accumulate replies
# func:  accum_replies(mid)
# retn:  ---
# open:  "./infos/{mid}-finfo.pkl"
# dump:  "./infos/{mid}-tinfo.pkl", "./infos/{mid}-ninfo.pkl"
        tinfo: list of ctime (1 x ct_group_cnt)
        ninfo: 2d list (video_num x ct_group_cnt)
            each row: list, accumulate floor nums of all ctime groups
"""

""" Sort replies with ctime
# func:  sort_replies(mid)
# retn:  ---
# open:  "./infos/{mid}-tinfo.pkl", "./infos/{mid}-ninfo.pkl"
# dump:  "./infos/{mid}-sinfo.pkl"
         sinfo: 2d list (ct_group_cnt x k)
            each row: list (1 x k), top k aids ranked by accumulated floor nums at each ctime group
"""



""" [Not in this file] Animation """

