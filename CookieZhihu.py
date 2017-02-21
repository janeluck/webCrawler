import requests

session = requests.Session()


cookie = {'Cookie': ''}
html = session.get('https://www.zhihu.com/', cookies=cookie).content

print(html.decode())