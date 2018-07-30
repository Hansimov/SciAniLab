video_fadeout = [0,1,2,3,4,5,6,7,8]

fadeout_cnt = len(video_fadeout)
idx_tmp = 0

for i in range(0, fadeout_cnt):
    video_tmp = video_fadeout[idx_tmp]
    if video_tmp % 2 != 0:
        print(video_tmp)
        video_fadeout.pop(idx_tmp)
        # continue
    else:
        print(video_tmp)
        idx_tmp += 1

print(video_fadeout)