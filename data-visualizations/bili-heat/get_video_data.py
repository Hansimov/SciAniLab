import requests
import json
import glob

# # Get all videos of an upper.

# # https://space.bilibili.com/ajax/member/getSubmitVideos?mid=122879&pagesize=100&tid=0&page=1&keyword=&order=pubdate
# url_body = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&page={}&pagesize={}'

# def getJson(mid=122879, page=1, pagesize=100):
#     req  = requests.get(url_body.format(mid,page,pagesize))
#     json_data = req.json()
#     return req, json_data

# req, json_data = getJson(122879, 1, 100)

# with open('jsons/ao_{:0>3}.json'.format(1), 'w', encoding='utf8') as wf:
#     json.dump(json_data, wf, ensure_ascii=False)
#     page_num = json_data['data']['pages']
#     print(page_num)
#     if page_num == 1:
#         pass
#     else:
#         for i in range(2, page_num+1):
#             req, json_data = getJson(mid=122879, page=i, pagesize=100)
#             with open('jsons/ao_{:0>3}.json'.format(i), 'w', encoding='utf8') as wf:
#                 json.dump(json_data, wf, ensure_ascii=False)

# # Combine all json files

# combined_json_data = []
# for json_file in glob.glob('jsons/ao_*.json'):
#     with open(json_file, 'r', encoding='utf8') as rf:
#         combined_json_data.append(json.load(rf))

# with open('jsons/ao.json', 'w', encoding='utf8') as wf:
#     json.dump(combined_json_data, wf, ensure_ascii=False)


with open('jsons/ao.json', encoding='utf8', mode='r') as f:
    videos = json.load(f)
    page_num = len(videos)
    for page_idx in range(page_num):
        video_num = len(videos[page_idx]['data']['vlist'])
        for video_idx in range(video_num):
            print(videos[page_idx]['data']['vlist'][video_idx]['title'])

