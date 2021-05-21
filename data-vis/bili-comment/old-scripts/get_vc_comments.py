from getcomments import *

import csv


if __name__ == '__main__':
    oid_list = []

    # with open('./tmp/vclist.csv',encoding='utf8',mode='r') as vcf:
    #     reader = csv.reader(vcf)
    #     next(reader, None)
    #     for row in reader:
    #         oid = int(row[0])
    #         oid_list.append(oid)

    oid_list = [24180113] # Temp

    cnt = 0
    for oid in oid_list:
        cnt += 1
        print('=== {:0>2d} / {:0>2d} ==='.format(cnt, len(oid_list)))
        if os.path.exists('replies/{:0>10d}.csv'.format(oid)):
            print('- {:0>10d}.csv has already existed.\n'.format(oid))
        else:
            getAllRepliesFiles(oid)
            combineRepliesFiles(oid)
            exportReplies(oid, fmt='full', ext='.csv')