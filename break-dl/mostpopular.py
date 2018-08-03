# 内容模块化  getpage  parsepage  save video
# 多线程
# -*- coding:utf-8 -*-
import urllib.request as request
from bs4 import BeautifulSoup
import codecs
import re
import os
from multiprocessing.pool import Pool
import time

from utils import googletrans
from utils import youdao

proxies = {
    'https': 'https://127.0.0.1:1080',
    'http': 'http://127.0.0.1:1080'
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
opener = request.build_opener(request.ProxyHandler(proxies))
request.install_opener(opener)

path1 = os.path.abspath('text/popularvideoLink.txt') # 视频直链存入这个文件
file1 = codecs.open(path1, 'a', 'utf-8')

# 每一页有 18 个视频链接, 每次返回一个链接 ，然后给下面解析
def get_page(offset):
    url = "http://www.break.com/most-popular/page/" + str(offset)
    try:
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        if response:
            bf = BeautifulSoup(response, 'html.parser')
            targets_url = bf.find_all(class_='ContentCard-thumb')
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
    if len(title) > 1:
        title = ''.join(title[0])
    else:
        title = ''.join(title) 
    # <title>标签也包含一个子节点:字符串 “The Dormouse’s story”,这种情况下字符串 “The Dormouse’s story”也属于<head>标签的子孙节点. 
    description = bf.find(class_= "Video-description").contents[1].contents
    if len(description) > 1:
        description = ''.join(description[0])     
    else:
        description = ''.join(description)
    pattern = re.compile(r'https?://video1.[^\s]*.mp4')
    responsetext = request.urlopen(req).read().decode('utf-8')
    videolink = pattern.findall(responsetext)
    if len(videolink) > 1:
        videolink = ''.join(videolink[0])
    else:
        videolink = ''.join(videolink)
    print(''.join(videolink))  

    # 写入文件
    file1.write("\n")
    file1.write("初始链接: "+ url + '\n')
    file1.write("标题: " + title + '\n')
    file1.write("谷歌翻译："+ ''.join(googletrans(title)) +'\n')
    file1.write("有道翻译: "+ ''.join(youdao(title))+'\n')
    file1.write("内容: " + description + "\n")
    file1.write("谷歌翻译: " + ''.join(googletrans(description)) + '\n')
    file1.write("有道翻译: " + ''.join(youdao(description)) + '\n')
    file1.write("链接: " + ''.join(videolink) + "\n")
    file1.write("\n")

    # 保存视频
    path = 'video/'+ title + '.mp4'
    with open(path,'ab') as ft:
        req = request.Request(videolink, headers=headers)
        ft.write(request.urlopen(req).read())
        ft.flush()

def main(offset):
    for item in get_page(offset):
        try:
            write_files(item)
        except Exception as e:
            print('main error ' + item.get('url'))
            continue

if __name__ == '__main__':

    startTime = time.time()
    pool = Pool(20)
    groups = ([x for x in range(1,2)])
    pool.map(main, groups)
    pool.close()
    pool.join()
    endTime = time.time()
    print("used time is ", endTime - startTime)

    
