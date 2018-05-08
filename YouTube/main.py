# -*- coding: utf-8 -*-

import youtube_dl
import codecs
import os

pwd = os.getcwd()
ydl_opts = {
        'proxy':'socks5://127.0.0.1/',
        'ignoreerrors':True,
        'outtmpl': pwd+'/video/%(title)s-%(id)s.%(ext)s'
    }

file =  codecs.open(pwd+'/video.txt','a','utf-8')

# example: https://www.youtube.com/user/BostonDynamics/videos
# 返回各个视频的初始下载链接
def getfirstLink(firstLink):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # 先抽取信息，不下载    
        info = ydl.extract_info(firstLink,download=False)
        for i in range(0,len(info['entries'])):
            yield info['entries'][i]['webpage_url']

def downloadVideo(videolink):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(videolink,download=True)
        file.write('title : '+ str(info['title']) + '\n')
        file.write('description : '+ str(info['description']) + '\n')
        file.write('categories : '+ str(info['categories']) + '\n')
        file.write('tags : '+ ''.join(info['tags']) + '\n')
        file.write('\n')
        file.write('\n')
        
if __name__ == '__main__':

    url = 'https://www.youtube.com/user/BostonDynamics/videos'
    for link in getfirstLink(url):
        try:
            downloadVideo(link)
        except Exception as e:
            print(link)
            print(e)
            continue
    file.close()





