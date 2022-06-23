import urllib
import requests
import re
from bs4 import BeautifulSoup

# 591
# https://market.591.com.tw/

# 樂居
# https://www.leju.com.tw/
url = 'https://www.leju.com.tw/page_search_result?oid=L5891107499320f'


# 樂屋
# url = 'https://www.rakuya.com.tw/realprice/result?city=0&zipcode=106&search=community&keyword=%E6%88%90%E5%BE%B7%E8%8F%81%E9%81%B8%E9%9B%86&sort=11'

# print(urllib.parse.unquote(url))

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Mobile Safari/537.36',
# }

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Mobile Safari/537.36',
    'referer': 'https://www.leju.com.tw/',
    'authority': 'api.leju.com.tw',
    'path': '/api/data/objectPageView?hoid=L5891107499320f'
}


r = requests.get(url, headers=headers)

if r.status_code == 200:
    print(r.content.decode('utf-8'))

    # soup = BeautifulSoup(r.text, 'html.parser')
    # household = soup.find_all("div", {"class": "point__info"})
    # print(household[0].text)

    # total_sales = soup.find_all("span", {"class": "top__numb setSearchTotal"})
    # print(total_sales[0].text)

else:
    print("status code = ", r.status_code)

# data = {
#     'id': 'L5891107499320f',
#     'lejuToken': '500508584d67763bae50a05247d91392'
# }

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Mobile Safari/537.36',
#     'referer': 'https://www.leju.com.tw/',
#     'authority': 'api.leju.com.tw'
# }


# r = requests.get(
#     'https://api.leju.com.tw/api/data/objectPageView?hoid=Lb365009a731c', headers=headers)
# url = "https://api.leju.com.tw/api/search/objectData"
# url = "https://api.leju.com.tw/api/search/TransactionsObject"
# r = requests.post(url, data=data, headers=headers)

# r.encoding = 'unicode-escape'
# if r.status_code == 200:
#     subject = re.findall(r'本社區共有',
#                          r.content.decode('unicode-escape'))
#     print(r.content.decode('unicode-escape'))
#     # print(subject)
# else:
#     print(r.status_code)
