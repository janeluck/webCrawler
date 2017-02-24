import requests
import re

#
# s = requests.Session()
#
# # 获取验证码相关信息: token和图片请求地址url
# captchaInfo = s.get('https://www.douban.com/j/misc/captcha').json()
#
#
# # 下载验证码图片, 人工打码
# with open('captcha.png', 'wb') as f:
#     f.write(s.get('https:' + captchaInfo['url']).content)
#
# captcha = input('请输入验证码')
#
# # 请求登录接口
# html = s.post('https://accounts.douban.com/login', data={
#     'source': 'None',
#     'redir': 'https://www.douban.com/',
#     'form_email': 'janeluck9158@gmail.com',
#     'form_password': 'janeluck9158',
#     'login': '登录',
#     'captcha-id': captchaInfo['token'],
#     'captcha-solution': captcha,
# }).content
# #print(html.decode())
#
# print(s.get('https://www.douban.com/people/66524852').content.decode())

#类注释
class DoubanUserSpider(object):

    def __init__(self):
        self.s = requests.Session()
        token = self.get_captcha()
        self.login(token)



    def get_captcha(self):
        # 获取验证码相关信息: token和图片请求地址url
        captchaInfo = self.s.get('https://www.douban.com/j/misc/captcha').json()

        # 下载验证码图片
        with open('captcha.png', 'wb') as f:
            f.write(self.s.get('https:' + captchaInfo['url']).content)

        # 返回登录所需的验证码token
        return captchaInfo['token']


    def login(self, token):


        # 请求登录接口
        self.s.post('https://accounts.douban.com/login', data={
            'source': 'None',
            'redir': 'https://www.douban.com/',
            'form_email': 'janeluck9158@gmail.com',
            'form_password': 'janeluck9158',
            'login': '登录',
            'captcha-id': token,
            'captcha-solution': input('请输入验证码\n'),
        })


        # 获取输入的用户id
        command  = 'command'

        while command != 'exit':
            command = input('请输入用户ID: \n').strip()
            self.get_userInfo(command)

        exit()


    def get_userInfo(self, user_id):

        # 获取用户主页
        user_page = self.s.get('https://www.douban.com/people/' + user_id).content.decode()

        # 截取title标签里的内容, 拿到用户名
        print(re.findall('title>(.*?)</title>', user_page, re.S)[0].strip())



if __name__ == '__main__':
    DoubanUserSpider()