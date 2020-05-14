It is necessary and better to rewrite all the codes into one script, to combine and automate the processes of fething, parsing, dumping and animating, in order to quicker make later reply data visualizations of more other uppers' videos.

---

Whole processes of reply data visualization:

* fetch vlist of certain mid
  * parse vlist to get [oid, created, title, pic_url, length] list, dump to vinfo.pkl (videos_info)
    * get all video covers with pic_url and resize to small sizes (or it will take long to render)
    * fetch replies of all videos with oid
      * parse replies to get [floor, ctime] list, dump to rinfo.pkl (replies_info)
        * use rinfo.pkl to create divided ctime list and accumulated floor cnt of each video between two ctime points, dump to ninfo.pkl (num_info)
        * use ninfo.pkl to sort the rank of videos (oid) with accumulated floor cnt at each divided ctime point, and dump to sinfo.pkl (sorted_info)
        * use sinfo.pkl to create bar chart animation

---

The filenames below might be modified through programming, all should  be in accordance with the docstring in the python scripts.

All data that chart animation needed are:

* `vinfo.pkl` (to use oid, created, title and length)
  * fetch_vlist -> [vlist.json] -> parse_vlist -> [vinfo.pkl]
* `sinfo.pkl` (to use rank of each video at each divided ctime point and corresponding accumulated floor cnt)
  * [vinfo.pkl] -> fetch_replies -> [./mid-* /oid-*/*.json] -> parse_replies -> [rinfo.pkl] -> calc_accumlated_floor_num -> [ninfo.pkl] -> sort_accumulated_floor_num -> [sinfo.pkl]

path of .pkl: "./pkls/"

The num 7224 below is not a real num, just represent the num of divided/grouped ctime points.

* `vinfo.pkl`: (293x5) 2d list of [oid, created, title, pic_url, length]
* `rinfo.pkl`: (293xfloor) dict of {oid: finfo_L}
           finfo_L: (floorx2) 2d list of [floor, ctime]
           floor: total floor cnt of each video replies
* `ninfo.pkl`: [ct_L, ninfo_L] 
           ct_L: (7224x1)
           ninfo_L: (293x7224) 2d list of accumulated floor cnt of each video at each divided ctime
* `sinfo.pkl`: (7224x20) 2d list of [top 20 oids ranked by accumulated floor cnt at each divided ctime]

---

Animation flows: (See "ideas.pptx")

* top 15 videos rank changes
  * cover, bar, title, acc_flr_cnt, aid, idx
* newest video cover

- find dominant color (color-thief-py)
- if hottest and newest is the same one
  - the below fly to the above, combined and faded

