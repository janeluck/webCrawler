import  requests

proxy = {
    'http': 'http://115.231.105.109:8081'
}

ip = requests.get('http://icanhazip.com').content

# 使用代理
proxy_ip = requests.get('http://icanhazip.com', proxies=proxy).content

print(ip)
print(proxy_ip)