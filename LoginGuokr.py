import requests
import lxml.html


class GuokrSpider(object):

    def __init__(self):
        self.s = requests.Session()
        form = self.get_form()
        self.login(form)

    def get_form(self):
        # 获取验证码相关信息: token和图片请求地址url
        html = lxml.html.fromstring(self.s.get('https://account.guokr.com/sign_in/').content.decode())
        captcha_rand = html.xpath('//input[@id="captchaRand"][1]/@value')[0].strip()
        # 下载验证码图片
        with open('captcha.png', 'wb') as f:
            f.write(self.s.get('https://account.guokr.com/captcha/' + captcha_rand).content)
        # 返回登录所需的表单信息
        return {
            'username': 'greensouth@foxmail.com',
            'password': 'iamtheone847',
            'csrf_token': html.xpath('//input[@id="csrf_token"][1]/@value')[0],
            'captcha_rand': captcha_rand,
            'captcha': input('请查看captcha.png, 输入验证码:\n').strip()
        }

    def login(self, form):
        # 请求登录接口
        self.s.post('https://account.guokr.com/sign_in/', data=form)
        # 获取个人主页
        print(self.s.get('http://www.guokr.com/settings/profile/').content.decode())


if __name__ == '__main__':
    GuokrSpider()