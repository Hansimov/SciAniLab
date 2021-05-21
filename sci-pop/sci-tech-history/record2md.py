import re

# \d{4}-\d{2}-\d{2}\s\d{1,2}:\d{2}:\d{2}\s

ptime = re.compile('\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{2}:\d{2}\s')

with open('records_20180609.txt', encoding='utf-8', mode='r') as rcdfile:
    cnt = 0
    for line in rcdfile:
        cnt = cnt + 1
        if ptime.match(line):
            print('{:0>5d}: {}'.format(cnt, ptime.findall(line)[0]))



# test_string = 'a1b2c3d4'
# p = re.compile("[a-z]\d")
# # for m in p.finditer(test_string):
# #     print(m.start(), m.group())

# if p.match(test_string):
#     print(True)
# else:
#     print(False)
