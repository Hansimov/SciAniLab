import requests
import json
import math
import glob
from datetime import datetime
import os
import time
import sys
# import jieba, jieba.analyse

# https://api.bilibili.com/x/v2/reply?oid=22755224&type=1&sort=0&nohot=1&pn=1

url_head = 'https://api.bilibili.com/x/v2/reply?'
# headers = {
#         'Referer':'https://www.bilibili.com/video'
#         }

'''
### File Structure
  replies
    |- 0000123456
      |- pages
        |- 00001.json
        |- 00002.json
        |- 00003.json
        |- ...
      |- __0000123456.json
    |- 0000654321
      |- pages
        |- ...
      |- __0000123456.json
    |- 0000123456.csv
    |- 0000123456.md
    |- 0000654321.csv
    |- 0000654321.md
    |- ...

'''

def nameRepliesDir(oid):
    # replies_dir = 'replies_' + '{:0>10d}'.format(oid)
    replies_dir = 'replies/' + '{:0>10d}'.format(oid)
    return replies_dir

def getRepliesFile(oid, xtype=1, sort=0, nohot=1, pn=1, is_get_page_num=1, is_get_req_json=0):
    if not os.path.exists('replies'):
        os.mkdir('replies')

    replies_dir = nameRepliesDir(oid)
    if not os.path.exists(replies_dir):
        os.mkdir(replies_dir)

    replies_pages_dir = replies_dir + '/pages'
    if not os.path.exists(replies_pages_dir):
        os.mkdir(replies_pages_dir)

    url_full = url_head \
               + '&oid='   + str(oid) \
               + '&type='  + str(xtype) \
               + '&sort='  + str(sort) \
               + '&nohot=' + str(nohot) \
               + '&pn='    + str(pn)

    # print('> Getting replies of av {:0>10d} at page: {:0>4d}'.format(oid,pn))
    req_info = requests.get(url_full)
    req_json = req_info.json()

    try:
        del req_json['data']['upper']
    except:
        pass

    with open((replies_dir+'/pages/{:0>5d}.json').format(pn),'w', encoding='utf-8') as jsonfile:
        json.dump(req_json, jsonfile)

    if is_get_page_num == 1:
        page_num = getPageNum(req_json)
    else:
        page_num = -1

    sys.stdout.write('\r> Getting replies of av {:0>10d} at page: {:0>5d} / {:0>5d}'.format(oid,pn,page_num))

    if is_get_req_json == 1:
        pass
    else:
        req_json = ''

    return page_num, req_json

def getPageNum(req_json):
    replies_count = req_json['data']['page']['count']
    page_size = req_json['data']['page']['size']
    page_num = math.ceil(replies_count/page_size)
    return page_num

def getAllRepliesFiles(oid, xtype=1, sort=0, nohot=1, pn=1):
    page_num, _ = getRepliesFile(oid=oid, xtype=xtype, sort=sort, nohot=nohot, pn=pn, is_get_page_num=1)
    for i in range(2, page_num + 1):
        time.sleep(0.1) # Slow down crawler to avoid being banned.
        getRepliesFile(oid=oid, xtype=xtype, sort=sort, nohot=nohot, pn=i)
    print('')

def combineRepliesFiles(oid):
    # Issue with merging multiple JSON files in Python:
    #   https://stackoverflow.com/a/23520673/8328786
    combined_replies_file = []
    page_num = 0
    replies_dir = nameRepliesDir(oid)
    replies_pages_dir = replies_dir + '/pages'
    combined_replies_file_name = '{}/__{:0>10d}.json'.format(replies_dir, oid)
    for jsonfile in glob.glob(replies_pages_dir+'/*.json'):
        page_num += 1
        with open(jsonfile, 'r') as infile:
            combined_replies_file.append(json.load(infile))

    # I may add a de-duplication step later.
    # Duplication will happen when new comment is added while crawling.

    print('+ Number of combined json files: {}'.format(page_num))
    with open(combined_replies_file_name, 'w') as outfile:
         json.dump(combined_replies_file, outfile)

    return combined_replies_file_name

def exportReplies(oid, fmt='full',ext=''):
    replies_dir = nameRepliesDir(oid)
    combined_replies_file_name = '{}/__{:0>10d}.json'.format(replies_dir, oid)

    if fmt == 'full':
        if ext == '':
            ext = '.md'
        replies_export_file_name = 'replies/{:0>10d}{}'.format(oid, ext)
    elif fmt == 'only':
        if ext == '':
            ext = '.txt'
        replies_export_file_name = 'replies/{:0>10d}{}'.format(oid, ext)

    with open(combined_replies_file_name, 'r') as combined_replies_file:
        replies_export_file = open(replies_export_file_name,'w')
        combined_data = json.load(combined_replies_file)

        if fmt == 'full':
            if ext == '.md':
                # print('|楼层|消息|点赞数|回复数|用户|')
                print('| 楼层 | 时间 | 用户 | 消息 | 点赞数 | 回复数 |', file=replies_export_file)
                # print(' |  -   |  -   |   -    | -      | -    |')
                print('| :-:  |  :-:   |  -   |   -  | :-:  | :-: |', file=replies_export_file)
            elif ext == '.csv':
                print('楼层 , 时间 , 用户 , 消息 , 点赞数 , 回复数 ', file=replies_export_file)

        for page in range(0, len(combined_data)):
            current_page_replies = combined_data[page]['data']['replies']
            item_num = len(current_page_replies)
            # print('# Num of items in this page: '.format(item_num))
            # print('-------- Page #{:0>4d} --------'.format(page+1))
            for item in range(0, item_num):
                current_reply = current_page_replies[item]

                floor_str = current_reply['floor']
                time_str = datetime.fromtimestamp(current_reply['ctime'])
                # [gitbook markdown] How to insert vertical line "|" into table?
                #   https://github.com/GitbookIO/gitbook/issues/1004
                if ext == '.md':
                    uname_str = current_reply['member']['uname'] \
                                .replace('|','&#124;').encode('gbk','ignore').decode('gbk')
                    message_str = current_reply['content']['message'] \
                                .replace('|','&#124;').replace('\r','').replace('\n','<br>') \
                                .encode('gbk','ignore').decode('gbk')
                    like_num = current_reply['like']
                    replies_num = current_reply['rcount']
                elif ext == '.csv':
                    uname_str = current_reply['member']['uname'] \
                                .replace(',','，').encode('gbk','ignore').decode('gbk')
                    message_str = current_reply['content']['message'] \
                                .replace(',','，').replace('\r','').replace('\n',' ') \
                                .encode('gbk','ignore').decode('gbk')
                    like_num = current_reply['like']
                    replies_num = current_reply['rcount']

                if fmt =='full':
                    if ext == '.md':
                        reply_str = '| {} | {} | {} | {} | {} | {} |'.format( 
                            floor_str, time_str, uname_str, message_str, like_num, replies_num)
                    elif ext == '.csv':
                        reply_str = '{} , {} , {} , {} , {} , {}'.format( 
                            floor_str, time_str, uname_str, message_str, like_num, replies_num)

                elif fmt == 'only':
                    reply_str = message_str

                print(reply_str, file = replies_export_file)

        print('Exporting {} ...\n'.format(replies_export_file_name))
        replies_export_file.close()

        return replies_export_file_name

# def calcWordFrequency(replies_only_txt_name, topnum=-1):
#     jieba.load_userdict('bili_dict.txt')
#     with open(replies_only_txt_name,'r') as replies_only_txt:
#         # replies_only_txt_content = replies_only_txt.read()
#         # print('---')
#         # print(replies_only_txt_content)
#         # with open(nameRepliesDir(this_oid)+'_word_freq','w') as word_freq_file:
#         #     print(replies_only_txt_content,file=word_freq_file)

#         # 使用python对中文文档进行词频统计
#         #   https://blog.csdn.net/levy_cui/article/details/53129506

#         tag_dict = {}
#         with open('bili_dict.txt','r',encoding='utf-8') as bili_dict:
#             for line in bili_dict:
#                 tag = line.strip('\n')
#                 tag_dict[tag] = 0
#                 # print(tag)

#         for line in replies_only_txt:
#             tags = jieba.analyse.extract_tags(line)
#             # print(line.strip('\n'))
#             for tag in tags:
#                 if tag in tag_dict:
#                     tag_dict[tag] +=1

#                 # print(tag, tag_dict[tag])
#         for tag in sorted(tag_dict, key=tag_dict.get, reverse=True):
#             print(tag, tag_dict[tag])

if __name__ == '__main__':
    oid_list = [
        13592834, # Test Video
    ]
    # oid = 22755224 # B站分区播放量
    # oid = 24929108 # 黑凤梨VC
    # oid =   308040 # 千年食谱颂
    for oid in oid_list:
        getAllRepliesFiles(oid)
        combineRepliesFiles(oid)
        exportReplies(oid, fmt='full', ext='.csv')
        # exportReplies(oid, fmt='full', ext='.md')
        # replies_only_txt_name = exportReplies(oid, fmt='only')

        # calcWordFrequency(replies_only_txt_name)
