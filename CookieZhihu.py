import requests

session = requests.Session()

#need user-agent
cookie = {'Cookie': ''}
html = session.get('https://www.zhihu.com/', cookies=cookie).content

print(html.decode())