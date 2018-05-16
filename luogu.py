# encoding=utf8
import sys
import re
import os
import urllib
import urllib.request as urllib2
import http.cookiejar as cookielib
import html.parser
# os.system('pip3 install BeautifulSoup4')
from bs4 import BeautifulSoup

username = ''
password = ''
breaker = ' '
the_largest_user_id = 30 # 110000

def geturl(url):
    return 'https://www.luogu.org/' + url
def getrespath(path):
    return 'result/'+ path

def build_soup(content):
    return BeautifulSoup(content, "html.parser")

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
    global opener, the_largest_user_id, breaker
    file = open(getrespath('user/information.txt'), 'w+', encoding = 'utf8')
    file.write(printer(['用户ID', '用户名', '解决题目数']))
    for user_id in [1]:
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
        user_solved = 0
        user_solved_base = soup.find_all(name='div',attrs={"class":"lg-article am-hide-sm"})[0].find_all('a')
        for user_solved_data in user_solved_base:
            user_solved_id = user_solved_data.string
            user_solved += 1
        file.write(printer([str(user_id), user_name, str(user_solved)]))
        download(user_img_url, getrespath('user/img/%d.png' % user_id))
        print('[UserAnalysis] id = %d has finished' % user_id)
    file.close()




Build()
# Login()
UserAnalysis()
