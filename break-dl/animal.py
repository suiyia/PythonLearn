# -*- coding:utf-8 -*-
import urllib.request as request
from bs4 import BeautifulSoup
import codecs
import re
import os
from multiprocessing.pool import Pool
import time

import youtube_dl
from utils import googletrans
from translateyoudao.translate import translate  
from utils import baidu

proxies = {
    'https': 'https://127.0.0.1:1080',
    'http': 'http://127.0.0.1:1080'
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
opener = request.build_opener(request.ProxyHandler(proxies))
request.install_opener(opener)

path1 = os.path.abspath('text/animalsvideoLink.txt') # 视频直链存入这个文件
file1 = codecs.open(path1, 'a', 'utf-8')  # 追加写入

# 每一页有 18 个视频链接, 每次返回一个链接 ，然后给下面解析
def get_page(offset):
    url = "http://www.break.com/animals/page/" + str(offset)
    try:
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        if response:
            bf = BeautifulSoup(response, 'html.parser')
            targets_url = bf.find_all(class_='ContentCard-thumb')  # 依次匹配找到 18 个链接
            for link in targets_url:
                yield{
                    'url': link.get('href')
                }
    except Exception as e:
        print('get_page error: '+ str(offset) +str(e))

def write_files(item):
    url = item.get('url')
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    bf = BeautifulSoup(response, 'html.parser')
    title = bf.find(class_='Content-title').contents
    # 多个 title 只选择第一个
    if len(title) > 1:
        title = ''.join(title[0])
    else:
        title = ''.join(title) 
    # <title>标签也包含一个子节点:字符串 “The Dormouse’s story”,这种情况下字符串 “The Dormouse’s story”也属于<head>标签的子孙节点. 
    description = bf.find(class_= "Video-description").contents[1].contents
    # 多个 description 只选择第一个
    if len(description) > 1:
        description = ''.join(description[0])     
    else:
        description = ''.join(description)
    pattern = re.compile(r'https?://video1.[^\s]*.mp4')  # 匹配网站内视频直链
    responsetext = request.urlopen(req).read().decode('utf-8')
    videolink = pattern.findall(responsetext)

    flag = 1  # 标识视频是否是 youtube 还是 网站视频直链.mp4
    if len(videolink) == 0:  # 如果是 YouTube 视频 则找出油管的链接，然后设置标志位
        pattern = re.compile(r'https?://www.youtube.com/embed[^\s]+rel=0')
        videolink = pattern.findall(responsetext)
        videolink = ''.join(videolink[0])
        flag = 0
    elif len(videolink) > 1:
        videolink = ''.join(videolink[0])
    else:
        videolink = ''.join(videolink)

    # 写入文件
    file1.write("\n")
    file1.write("初始链接: "+ url + '\n')
    file1.write("标题: " + title + '\n')
    file1.write("谷歌翻译："+ ''.join(googletrans(title)) +'\n')
    # file1.write("有道翻译: "+ ''.join(youdao(title))+'\n')
    file1.write("有道翻译: "+ ''.join(translate(title).get(title))+'\n')
    file1.write("百度翻译: " + ''.join(baidu(title)) + '\n')
    file1.write("内容: " + description + "\n")
    file1.write("谷歌翻译: " + ''.join(googletrans(description)) + '\n')
    file1.write("有道翻译: " + ''.join(translate(description).get(description)) + '\n')
    file1.write("百度翻译: " + ''.join(baidu(description)) + '\n')
    file1.write("视频链接: " + ''.join(videolink) + "\n")
    file1.write("\n")

    # # 保存视频
    title = title.replace('?','') # 去掉文件名中的 特殊字符 ？
    path = 'video/'+ title + '.mp4'
    if flag == 1:
        with open(path,'ab') as ft:
            req = request.Request(videolink, headers=headers)
            ft.write(request.urlopen(req).read())
            ft.flush()
    else:
        ydl = youtube_dl.YoutubeDL()
        ydl_opts = {
            'proxy':'socks5://127.0.0.1/',
            'outtmpl':path
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(videolink.split())

def main(offset):
    for item in get_page(offset):
        try:
            write_files(item)
        except Exception as e:
            print('main error ' + item.get('url'))
            print(e)
            continue


if __name__ == '__main__':

    startTime = time.time()
    pool = Pool(20)
    groups = ([x for x in range(1,2)])
    # groups = ([x for x in range(2,20)])   # 第2页到20页 给不同线程
    pool.map(main, groups)
    pool.close()
    pool.join()
    endTime = time.time()
    print("used time is ", endTime - startTime)
