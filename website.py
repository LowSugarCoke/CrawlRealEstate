
import requests
import re

# 591
# https://market.591.com.tw/

# 樂居
# https://www.leju.com.tw/

# 樂屋
# https://www.rakuya.com.tw/realprice/result?city=0&zipcode=106&search=community&keyword=%E6%88%90%E5%BE%B7%E8%8F%81%E9%81%B8%E9%9B%86&sort=11


# r = requests.get(
#     'https://www.leju.com.tw/page_search_result?oid=L4021038888b2d9')
# r.encoding = 'utf-8'
# if r.status_code == 200:
#     # print(r.content.decode('utf-8'))

#     subject = re.findall(r'本社區共有',
#                          r.content.decode('utf-8'))
#     print(subject)


# print("status code = ", r.status_code)


r = requests.get(
    'https://www.leju.com.tw/page_search_result?oid=L5891107499320f')
r.encoding = 'utf-8'
if r.status_code == 200:
    print(r.content.decode('utf-8'))
else:
    print(r.status_code)
