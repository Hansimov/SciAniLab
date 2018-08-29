import pandas as pd

#### 剔除的 tid
# 番剧区：33, 32,
# 国创区：153,
# 放映厅：37, 178, 179, 180, 147, 145, 146, 83, 185, 187
# 隐藏：完结动画：94，连载动画：120

# 音乐选集：130
# 演讲·公开课：39
# 只选取 copyright=1 也即原创的
if __name__ == '__main__':
    input_file = './data/view_gt100w_latest.csv'
    output_file = './data/view_gt100w_latest_out.csv'
    # input_file  = './data/view_gt100w_180826x.csv'
    # output_file = './data/view_gt100w_180826x_out.csv'
    df = pd.read_csv(input_file, sep=',')

    with open(input_file, encoding='utf-8', mode='r') as ipf, \
         open(output_file,encoding='utf-8', mode='w') as opf:

        ignored_tid_list = [33, 32,  94,  153, 37, 178, 179, 180, 147, 145, 146, 83, 185, 187]
        # ignored_tid_list.extend([94, 120, 130, 39])
        row_tmp = ipf.readline() # header of csv
        print(row_tmp.strip('\n'), file=opf)

        for i in range(0, len(df)):
            row_tmp = ipf.readline()
            if df.iloc[i]['copyright'] != 1:
                continue
            if df.iloc[i]['tid'] in ignored_tid_list:
                continue
            print(row_tmp.strip('\n'), file=opf)

