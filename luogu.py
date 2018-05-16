# encoding=utf8
import sys
import re
import os
import urllib
import urllib.request as urllib2
import http.cookiejar as cookielib
import html.parser
# os.system('pip3 install BeautifulSoup4')
# os.system('pip3 install xlwings')
from bs4 import BeautifulSoup
# import xlwings as xw

username = ''
password = ''
breaker = '	'
to_download = 0
the_largest_user_id = 30 # 110000

def geturl(url):
    return 'https://www.luogu.org/' + url
def getrespath(path):
    return 'result/'+ path

def build_soup(content):
    return BeautifulSoup(content, "html.parser")
def find_soup(div, name, content):
    global soup
    return soup.find_all(name = div, attrs = {name : content})

def printer(a):
    global breaker
    ret = ''
    for i in a:
        ret += i + breaker
    ret += '\n'
    return ret
def download(url, filepath):
    global opener
    file = open(filepath, 'wb+')
    file.write(opener.open(url).read())
    file.close()

def Build():
    global opener
    filename = 'cookie.txt' # 保存cookie的文件
    cookie = cookielib.MozillaCookieJar(filename) # 创建一个实例
    handler = urllib2.HTTPCookieProcessor(cookie) # 创建urllib2的cookie处理器
    opener = urllib2.build_opener(handler) # 通过之前的cookie处理器构造opener
    opener.open(geturl('')) # 获得一个cookie
    cookie.save(ignore_discard=True, ignore_expires=True) # 保存cookie到文件

def Login():
    global username, password, rooturl, opener
    # 还未修改
    url = geturl('login.php')
    data = urllib.urlencode({"user_id": username, "password": password, })
    response = opener.open(url, data) # 登录请求

def UserAnalysis():
    global opener, the_largest_user_id, breaker, soup
    file = open(getrespath('user/information.txt'), 'w+', encoding = 'utf8')
    file.write(printer(['用户ID', '用户名',
                        '提交', '解决', '贡献', '活跃', '积分',
                        '用户类型', '注册时间', 
                        '博客网址', '解决题目数', '通过的题目']))
    for user_id in [1, 53495]:
        # for user_id in range(-1, the_largest_user_id + 1):
        url = geturl('space/show?uid=%d' % user_id)
        page = opener.open(url)
        content = page.read()
        soup = build_soup(content)
        open('test_output.txt', 'w+', encoding = 'utf8').write(soup.prettify())
        if soup.title.string == '提示 - 洛谷 ' :
            continue # 用户不存在

        user_name = soup.find_all(name='span',attrs={"name":"username"})[0].string
        user_img_url = 'https://cdn.luogu.org/upload/usericon/%d.png' % user_id
        user_blog_id = soup.find_all(name='a',attrs={"class":"am-btn am-btn-sm am-btn-primary"})[0]['href'][8:-1]
        user_inf_submit = find_soup('span', 'class', 'lg-bignum-num')[0].string
        user_inf_solved = find_soup('span', 'class', 'lg-bignum-num')[1].string
        user_inf_right = find_soup('span', 'class', 'lg-right')[0].string
        user_inf_gongxian = re.split(' / ', user_inf_right)[0]
        user_inf_huoyue = re.split(' / ', user_inf_right)[1]
        user_inf_jifen = re.split(' / ', user_inf_right)[2]
        user_inf_class = find_soup('span', 'class', 'lg-right')[1].string[1:]
        user_inf_register = find_soup('span', 'class', 'lg-right')[2].string[1:]
        user_solved = 0
        user_solved_base = soup.find_all(name='div',attrs={"class":"lg-article am-hide-sm"})[0].find_all('a')
        user_solved_id = ''
        for user_solved_data in user_solved_base:
            user_solved_id += user_solved_data.string + ' '
            user_solved += 1
        file.write(printer([str(user_id), user_name,
                            user_inf_submit, user_inf_solved, user_inf_gongxian, user_inf_huoyue, user_inf_jifen,
                            user_inf_class, user_inf_register,
                            user_blog_id, str(user_solved), user_solved_id]))
        if to_download:
            download(user_img_url, getrespath('user/img/%d.png' % user_id))
        print('[UserAnalysis] id = %d has finished' % user_id)
    file.close()




Build()
# Login()
UserAnalysis()
