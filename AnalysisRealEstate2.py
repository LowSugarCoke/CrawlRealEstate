from itertools import groupby
import os
import pandas as pd
import plotly.express as px
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import difflib
import csv


# Part 1 資料匯入及處裡

# 自定義字體變數
myfont = FontProperties(fname=r'./TaipeiSansTCBeta-Regular.ttf')
myfont.set_size(15)

location_all = ["台北市", "桃園縣"]

location_str = """台北市 A 苗栗縣 K 花蓮縣 U
                  台中市 B 台中縣 L 台東縣 V
                  基隆市 C 南投縣 M 澎湖縣 X
                  台南市 D 彰化縣 N 陽明山 Y
                  高雄市 E 雲林縣 P 金門縣 W
                  台北縣 F 嘉義縣 Q 連江縣 Z
                  宜蘭縣 G 台南縣 R 嘉義市 I
                  桃園縣 H 高雄縣 S 新竹市 O
                  新竹縣 J 屏東縣 T"""

# List切片用法
# print(location_str.split())
# print(location_str.split()[::2])  # 步長為2
# print(location_str.split()[1::2])  # 從1開始步長為2


print(location_str.split()[::2])
print(location_str.lower().split()[1::2])

# '台北市', 'A', '苗栗縣', 'K', '花蓮縣', 'U', '台中市', 'B', '台中縣', 'L', '台東縣', 'V', '基隆市', 'C', '南投縣', 'M', '澎湖縣', 'X', '台南市', 'D', '彰化縣', 'N', '陽明山', 'Y', '高雄市', 'E', '
# 雲林縣', 'P', '金門縣', 'W', '台北縣', 'F', '嘉義縣', 'Q', '連江縣', 'Z', '宜蘭縣', 'G', '台南縣',
# 'R', '嘉義市', 'I', '桃園縣', 'H', '高雄縣', 'S', '新竹市', 'O', '新竹縣', 'J', '屏東縣', 'T'

# dictionary {key = 縣市, value = 小寫英文字母}
locToLetter = dict(
    zip(location_str.split()[::2], location_str.lower().split()[1::2]))


# 歷年資料夾

# for d in os.listdir():
#     # print(d)
#     if d[:4] == 'real':
#         continue


dirs = [d for d in os.listdir() if d[:4] == 'real']

# list []
# dictionary {}

for location in location_all:
    dfs = []
    # pd => pandas (讀取excel的)
    for d in dirs:
        # print(d)
        # print(locToLetter[location]+'_lvr_land_a.csv')
        # os.path C:\Users\jack2\OneDrive\Desktop\part_time\CrawlRealEstate\read_estate1021\a_lvr_land_a.csv
        print(os.path.join(
            d, locToLetter[location] + '_lvr_land_a.csv'))
        df = pd.read_csv(os.path.join(
            d, locToLetter[location] + '_lvr_land_a.csv'), index_col=False, low_memory=False)
        # print(df) #row data

        # 第幾季
        df['Q'] = d[-1]

        # 在list內放入許多pandas資料結構
        dfs.append(df.iloc[1:])
        # print(df.iloc[1:])

    # concat把list內的所有資料接起來
    df = pd.concat(dfs, sort=True)

    # print(df)

    # # 新增交易年份(西元)
    # 如果‘coerce’，則無效解析將設置為NaN
    # str to int
    df['year'] = pd.to_numeric(df['交易年月日'].str[:-4], errors='coerce') + 1911

    # # # 平方公尺換成坪
    df['單價元平方公尺'] = df['單價元平方公尺'].astype(float)
    df['單價元坪'] = df['單價元平方公尺'] * 3.30579

    # # # 建物型態
    df['建物型態2'] = df['建物型態'].str.split('(').str[0]

    # # # 刪除有備註之交易（多為親友交易、價格不正常之交易）
    df = df[df['備註'].isnull()]
    df = df[df['建築完成年月'].notnull()]

    # # # 將index改成年月日
    df.index = pd.to_datetime(df['year'].astype(
        str) + df['交易年月日'].str[-4:], errors='coerce')
    df.sort_index(inplace=True)

    print(df)

    # # Part 2數據分析
    # # 長寬
    # plt.rcParams['figure.figsize'] = (10, 6)

    # # 歷年各區平均價格
    # # prices 是一個 dictionary, key是放哪一區, value 放每年每坪的價格
    # prices = {}

    # for district in set(df['鄉鎮市區']):
    #     # 一個一個區 依序去執行
    #     # print(district)
    #     cond = (
    #         (df['主要用途'] == '住家用')
    #         & (df['鄉鎮市區'] == district)
    #         & (df['單價元坪'] < df["單價元坪"].quantile(0.95))
    #         & (df['單價元坪'] > df["單價元坪"].quantile(0.05))
    #     )
    #     groups = df[cond]['year']

    #     # print(df[cond]['單價元坪'].astype(
    #     #     float).groupby(groups).mean().loc[2012:])

    #     prices[district] = df[cond]['單價元坪'].astype(
    #         float).groupby(groups).mean().loc[2012:]

    # print(prices)

    # # 固定用法
    # price_history = pd.DataFrame(prices)
    # price_history.plot()
    # plt.title('各區平均單價', fontproperties=myfont)
    # plt.legend(prop=myfont)
    # plt.show()

    # Part 2數據分析(自定義)
    # 長寬
    plt.rcParams['figure.figsize'] = (10, 6)

    # 歷年各區平均價格
    # prices 是一個 dictionary, key是放哪一區, value 放每年每坪的價格
    prices = {}

    building_list = {}

    # 所有區的建物價格加總
    total_money = 0
    total_building = 0

    for district in set(df['鄉鎮市區']):
        # 一個一個區 依序去執行
        # print(district)
        cond = (
            (df['主要用途'] == '住家用')
            & (df['建物型態2'] == '住宅大樓')
            & (df['鄉鎮市區'] == district)
            & (df['單價元坪'] < df["單價元坪"].quantile(0.95))
            & (df['單價元坪'] > df["單價元坪"].quantile(0.05))
            & (df['建築完成年月'].astype(float) > 1090000)  # 新增
            & (df['交易年月日'].astype(float) > 1090000)  # 新增
        )
        groups = df[cond]['year']

        # print(df[cond]['單價元坪'].astype(
        #     float).groupby(groups).mean().loc[2012:])

        # 原本的code
        prices[district] = df[cond]['單價元坪'].astype(
            float).groupby(groups).mean().loc[2020:]

        # 新增
        # 總共的成交金額與成交量
        total_money += df[cond]['單價元坪'].sum()
        total_building += len(df[cond]['單價元坪'])

        # 新增
        print(district, ", 單價元坪 = ", df[cond]['單價元坪'].astype(
            float).mean())
        print(district, ", 建物價格總和 = ", df[cond]['單價元坪'].sum())
        print(district, ", 建物數量 = ", len(df[cond]['單價元坪']))
        print('建物地址 ', df[cond]['土地位置建物門牌'])

        # 為了之後要分類社區用
        building_list[district] = df[cond]['土地位置建物門牌'].tolist()

    # 新增
    print(location, ", 單價元坪 = ", total_money/total_building)
    print(location, ", 建物價格總和 = ", total_money)
    print(location, ", 建物數量 = ", total_building)

    # 原本的code
    print(prices)

    # 固定用法
    price_history = pd.DataFrame(prices)
    price_history.plot()
    plt.title('各區平均單價', fontproperties=myfont)
    plt.legend(prop=myfont)
    # plt.show()

    def string_similar(s1, s2):
        return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

    # 處理地址資訊
    community_total = {}

    for district in building_list:

        # 把"市"以及"區"資料刪除
        for i in range(len(building_list[district])):
            building_list[district][i] = building_list[district][i].replace(
                district, "").replace("臺北市", "")

        # 初始化communitry_total 每個district
        community_total[district] = []

        r = len(building_list[district])
        i = 0
        while i < r:
            l = []
            # 把第0個抓進新的群
            l.append(location+district + building_list[district][i])

            # for 倒過來做
            for j in range(len(building_list[district])-1, i, -1):
                if string_similar(building_list[district][i], building_list[district][j]) > 0.7:
                    l.append(location+district +
                             building_list[district][j])
                    del building_list[district][j]  # 刪除
            # 刪除第i個index
            del building_list[district][i]

            # 把分好的社區接在list_total的後面
            community_total[district].append(l)

            r = len(building_list[district])

    # 列印出來所有的社區
    for a in community_total:
        print(a)
        for i in range(len(community_total[a])):
            print(community_total[a][i])

    #存檔, w = write, r = read
    with open(location+'_community.txt', 'w') as f:
        for key in community_total.keys():
            f.write("%s\n" % (key))
            index = 1

            # 去跑list_total內所有的list
            for i in range(len(community_total[key])):
                f.write("%s. %s\n" % (str(index), community_total[key][i]))
                index += 1

            # enter的意思
            f.write("\n")

    # print(community_total)
    # # dropna丟棄空值的行列
    # district_price = df.reset_index()[['鄉鎮市區', '單價元坪']].dropna()
    # district_price = district_price[district_price['單價元坪'] < 2000000]

    # fig = px.histogram(district_price, x="單價元坪", color="鄉鎮市區",
    #                    marginal="rug", nbins=50)  # can be `box`, `violin`)

    # # Overlay both histograms
    # fig.update_layout(barmode='overlay')
    # # Reduce opacity to see both histograms
    # fig.update_traces(opacity=0.75)
    # fig.show()

    # # '店面', '套房', '其他', '農舍', '倉庫', '廠辦', '透天厝', '工廠']
    # types = ['華廈', '公寓', '住宅大樓', '套房']

    # building_type_prices = {}
    # for building_type in types:
    #     cond = (
    #         (df['主要用途'] == '住家用')
    #         & (df['單價元坪'] < df["單價元坪"].quantile(0.8))
    #         & (df['單價元坪'] > df["單價元坪"].quantile(0.2))
    #         & (df['建物型態2'] == building_type)
    #     )
    #     building_type_prices[building_type] = df[cond]['單價元坪'].groupby(
    #         df[cond]['year']).mean().loc[2012:]
    # pd.DataFrame(building_type_prices).plot()

    # plt.title('不同建物的價格', fontproperties=myfont)
    # plt.legend(prop=myfont)
    # plt.show()

    # # @title 價格與漲跌的相關性
    # mean_value = price_history.mean()

    # print("hello world", price_history.iloc[-1])

    # gain = (price_history.iloc[-1] / price_history.iloc[0])
    # mean = price_history.mean()

    # compare = pd.DataFrame({'上漲幅度': gain, '平均價格': mean}).dropna()
    # corr = (compare.corr().iloc[0, 1])

    # print('相關性：', corr)
    # if corr > 0:
    #     print('意涵：價格越高越保值')
    # else:
    #     print('意涵：價格越低越保值')
    # print()
    # print('各區平均價格')
    # print(mean.sort_values())

    # gain = (price_history.iloc[-1] / price_history.iloc[0])
    # # print("gain", gain)
    # mean = price_history.mean()

    # compare = pd.DataFrame({'上漲幅度': gain, '平均價格': mean}).dropna()
    # # print(compare.corr().iloc[0, 1])

    # compare.plot()
    # # plt.title('aaa', fontproperties=myfont)
    # # plt.legend(prop=myfont )
    # plt.show()
