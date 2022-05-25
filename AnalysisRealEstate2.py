from itertools import groupby
import os
import pandas as pd
import plotly.express as px
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

# Part 1 資料匯入及處裡

# 自定義字體變數
myfont = FontProperties(fname=r'./TaipeiSansTCBeta-Regular.ttf')
myfont.set_size(15)

location = "台北市"

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

locToLetter = dict(
    zip(location_str.split()[::2], location_str.lower().split()[1::2]))


# 歷年資料夾

# for d in os.listdir():
#     # print(d)
#     if d[:4] == 'real':
#         continue


dirs = [d for d in os.listdir() if d[:4] == 'real']

dfs = []

for d in dirs:
    # print(d)
    # print(locToLetter[location]+'_lvr_land_a.csv')
    df = pd.read_csv(os.path.join(
        d, locToLetter[location] + '_lvr_land_a.csv'), index_col=False, low_memory=False)
    # print(df) #row data

    # 第幾季
    df['Q'] = d[-1]
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

# # # 將index改成年月日
df.index = pd.to_datetime(df['year'].astype(
    str) + df['交易年月日'].str[-4:], errors='coerce')
df.sort_index(inplace=True)

# # print(df)


# # Part 2數據分析
# # 長寬
# plt.rcParams['figure.figsize'] = (10, 6)

# # 歷年各區平均價格
# prices = {}
# for district in set(df['鄉鎮市區']):
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
# price_history = pd.DataFrame(prices)
# price_history.plot()
# plt.title('各區平均單價', fontproperties=myfont)
# plt.legend(prop=myfont)
# plt.show()

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