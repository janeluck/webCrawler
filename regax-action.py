import re
a = '我是kingname, 我的微博账号是:kingname, 密码是:12345678, QQ账号是:99999, 密码是:890abcd, 银行卡账号是:000001, 密码是:654321, Github账号是:99999@qq.com, 密码是:7777love8888, 请记住他们。'
print(re.findall('密码是:(.*)', a))
print(re.findall('密码是:(.*),', a))
print(re.findall('密码是:(.*?)', a)) #???
print(re.findall('密码是:(.*?),', a))