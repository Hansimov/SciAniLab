import pandas as pd

# 忽略的 tid： 33, 32, 153, 37, 178, 179, 180, 147, 145, 146, 83, 185, 187
# 番剧区2个国创区1个和放映厅的10个

# 只选取 copyright=1 也即原创的
if __name__ == '__main__':
    input_file = './data/view_gt100w_latest.csv'
    output_file = './data/view_gt100w_latest_out.csv'
    df = pd.read_csv(input_file, sep=',')
    # print(df.iloc[0]['copyright']==2)

    with open(input_file, encoding='utf-8', mode='r') as ipf, \
         open(output_file,encoding='utf-8', mode='w') as opf:

        ignored_tid_list = [33, 32, 153, 37, 178, 179, 180, 147, 145, 146, 83, 185, 187]
        row_tmp = ipf.readline() # header of csv
        print(row_tmp.strip('\n'), file=opf)

        for i in range(0, len(df)):
            row_tmp = ipf.readline()
            if df.iloc[i]['copyright'] != 1:
                continue
            elif df.iloc[i]['tid'] in ignored_tid_list:
                continue
            else:
                print(row_tmp.strip('\n'), file=opf)

