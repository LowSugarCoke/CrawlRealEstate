import os
import pandas as pd
from matplotlib.font_manager import FontProperties

# 自定義需要統計的縣市
location_all = ["台北市", "桃園市", "台中市", "新北市", "苗栗縣", "花蓮縣", "台東縣",
                "基隆市", "南投縣", "澎湖縣", "台南市", "彰化縣", "陽明山", "高雄市",
                "雲林縣", "金門縣", "嘉義縣", "連江縣", "宜蘭縣", "台南縣", "嘉義市",
                "高雄縣", "新竹市", "新竹縣", "屏東縣"]

# Part 1 資料匯入及處裡

# 自定義字體變數
myfont = FontProperties(fname=r'./TaipeiSansTCBeta-Regular.ttf')
myfont.set_size(15)

# 所有縣市對應的英文
location_str = """台北市 A 苗栗縣 K 花蓮縣 U
                  台中市 B 台中縣 L 台東縣 V
                  基隆市 C 南投縣 M 澎湖縣 X
                  台南市 D 彰化縣 N 陽明山 Y
                  高雄市 E 雲林縣 P 金門縣 W
                  新北市 F 嘉義縣 Q 連江縣 Z
                  宜蘭縣 G 台南縣 R 嘉義市 I
                  桃園市 H 高雄縣 S 新竹市 O
                  新竹縣 J 屏東縣 T"""

# list轉成dictionary, 方便用來找縣市對應的英文字母
locToLetter = dict(
    zip(location_str.split()[::2], location_str.lower().split()[1::2]))

# 把real開頭的資料夾的路徑放入dirs,等等要用for走過
dirs = [d for d in os.listdir() if d[:4] == 'real']

# 把每一個real開頭的資料夾，依照自定義的縣市把檔案打開，匯入到dfs裡面
for location in location_all:
    dfs = []
    for d in dirs:
        print(os.path.join(
            d, locToLetter[location] + '_lvr_land_a.csv'))
        if os.path.exists(os.path.join(
                d, locToLetter[location] + '_lvr_land_a.csv')) == True:
            df = pd.read_csv(os.path.join(
                d, locToLetter[location] + '_lvr_land_a.csv'), index_col=False, low_memory=False)

            # 第幾季
            df['Q'] = d[-1]

            # 在list內放入許多pandas資料結構
            dfs.append(df.iloc[1:])

    # 若是沒有該地區的資料內容都沒有新建案則跳過
    if len(dfs) == 0:
        continue

    # concat把list內的所有資料接起來
    df = pd.concat(dfs, sort=True)

    # 新增交易年份(西元)
    # 如果‘coerce’，則無效解析將設置為NaN
    df['year'] = pd.to_numeric(df['交易年月日'].str[:-4], errors='coerce') + 1911

    # 平方公尺換成坪
    df['單價元平方公尺'] = df['單價元平方公尺'].astype(float)
    df['單價元坪'] = df['單價元平方公尺'] * 3.30579

    # 建物型態
    df['建物型態2'] = df['建物型態'].str.split('(').str[0]

    # 刪除有備註之交易（多為親友交易、價格不正常之交易）
    df = df[df['備註'].isnull()]

    df['建築完成年月'] = pd.to_numeric(df['建築完成年月'], errors='coerce')
    df = df.dropna(subset=['建築完成年月'])

    # 將index改成年月日
    df.index = pd.to_datetime(df['year'].astype(
        str) + df['交易年月日'].str[-4:], errors='coerce')
    df.sort_index(inplace=True)

    # Part 2數據分析(自定義)

    # 歷年各區平均價格
    # building_list 是一個 dictionary, key是放哪一區, value 放那區裡面相同建築完成日期地址的list
    building_list = {}

    # 所有區的建物價格加總
    total_money = 0
    total_building = 0

    for district in set(df['鄉鎮市區']):
        # 一個一個區 依序去執行
        # 判斷的情況
        cond = (
            (df['主要用途'] == '住家用')
            & (df['建物型態2'] == '住宅大樓')
            & (df['鄉鎮市區'] == district)
            & (df['單價元坪'] < df["單價元坪"].quantile(0.95))  # 刪除離群值
            & (df['單價元坪'] > df["單價元坪"].quantile(0.05))  # 刪除離群值
            & ((df['建築完成年月'].astype(float) > 1090000)  # 建築完成年月日在2020之後
               | (df['建築完成年月'].isnull()))  # 建築完成年月日為空值
            & (df['交易年月日'].astype(float) > 1090000)  # 交易年月日在2020之後

        )

        # 總共的成交金額與成交量
        total_money += df[cond]['單價元坪'].sum()
        total_building += len(df[cond]['單價元坪'])

        # 列出該地區資訊
        print(district, ", 單價元坪 = ", df[cond]['單價元坪'].astype(
            float).mean())
        print(district, ", 建物價格總和 = ", df[cond]['單價元坪'].sum())
        print(district, ", 建物數量 = ", len(df[cond]['單價元坪']))
        print('建物地址 ', df[cond]['土地位置建物門牌'])

        # 為了之後要分類社區用
        building_group = df[cond]['建築完成年月']  # 分群相同建築完成年月日的
        building_list[district] = df[cond]['土地位置建物門牌'].groupby(
            building_group)  # 放入dictionary中

    # 列出該縣市資訊
    print(location, ", 單價元坪 = ", total_money/total_building)
    print(location, ", 建物價格總和 = ", total_money)
    print(location, ", 建物數量 = ", total_building)

    # 若是該地區都沒有新建案則跳過
    if total_money == 0:
        continue

    # 處理地址資訊
    community_total = {}
    community_num = 0

    for district in building_list:
        community_total[district] = []

        # 把"市"以及"區"資料刪除
        for key, item in building_list[district]:
            community_num += 1
            l = []
            for path in item:
                path = path.replace(district, "").replace(location, "")
                l.append(location+district+path)    # 把"市"以及"區"資料加回去

            community_total[district].append(l)

    # 列印出來所有的社區
    for a in community_total:
        print(a)
        for i in range(len(community_total[a])):
            print(community_total[a][i])

    #存檔, w = write, r = read
    with open(location+'_community.txt', 'w') as f:
        f.write("%s新建案數量:%s (since 2020)\n" % (location, community_num))
        f.write("%s新建案單價元坪 = %s \n" % (location, total_money/total_building))

        for key in community_total.keys():
            f.write("%s\n" % (key))
            index = 1

            # 去跑list_total內所有的list
            for i in range(len(community_total[key])):
                f.write("%s. %s\n" % (str(index), community_total[key][i]))
                index += 1

            # enter的意思
            f.write("\n")
