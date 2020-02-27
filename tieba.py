# -*- coding: utf-8 -*-
#   贴吧签到脚本
import re
import time
import requests
import urllib
import os


class Baidu():
    def baidu(self, cookies):
        self.base_url = "http://www.baidu.com"
        self.session = requests.session()
        self.session.cookies.update(cookies)
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
        self.username = self.get_username()
        print 'Username is :', self.username
        if self.username:
            self.Tiebas = self.get_Tiebas()
            for name in self.Tiebas:
                if self.sign_wap(urllib.quote(name.encode('utf-8'))): time.sleep(0.5)
        return True

    def get_username(self):
        '''
        获取用户名
        :return:
        '''
        res = self.session.get(self.base_url)
        # 测试是否登录成功
        print 'Login in True' if re.search("'login':'1'", res.text) else 'Login in False'

        username = re.search("=user-name>(.+?)<", res.text)
        return username.group(1) if username else None

    def get_Tiebas(self):
        '''
        获取贴吧列表
        :return:
        '''
        try:
            res = self.session.get("https://tieba.baidu.com/mo/")
            likes_url = "https://tieba.baidu.com" + \
                        re.search('"([^"]+tab=favorite)"', res.text).group(1).replace("&amp;", "&")
            res = self.session.get(likes_url)
            Tiebas = re.findall('kw.+?">(.+?)<', res.text)
            return Tiebas
        except:
            return False

    def sign_wap(self, tieba_name):
        '''
        贴吧签到
        :param tieba_name:
        :return:True(执行签到) False(已经签到)
        '''

        res = self.session.get("https://tieba.baidu.com/mo/m?kw=" + tieba_name)

        if u"已签到" in res.text:
            print "已经签到：", urllib.unquote(tieba_name)
            return False
        else:
            s = '签到'.decode('utf-8')
            match = re.search('(/mo/q[^<]+?)">' + s, res.text)
            if match:
                sign_url = "https://tieba.baidu.com" + match.group(1)
                sign_url = sign_url.replace("&amp;", "&")
                res = self.session.get(sign_url)
                print "成功签到： " + urllib.unquote(
                    tieba_name) if u"已签到" in res.text else "签到失败： " + urllib.unquote(tieba_name)
            return True


def main():
    '''
    用户列表
    '''
    BAIDUID1 = os.getenv('BAIDUID1')
    BDUSS1 = os.getenv('BDUSS1')
    cookies = [
        {
            'BAIDUID': 'BAIDUID1',
            'BDUSS': 'BDUSS1'
        },
    ]

    for i in cookies:
        Baidu().baidu(i)


if __name__ == '__main__':
    main()