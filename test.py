import requests

url = "https://plvr.land.moi.gov.tw/Index"

response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print("Something error")
