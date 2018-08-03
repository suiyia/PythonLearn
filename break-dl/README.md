# break-dl
用于下载 [Break](http://www.break.com) 网站的视频，实现了**视频直链，标题、介绍的获取与翻译，实现视频的下载**

## 预览

![视频直链](http://orxtkgfh0.bkt.clouddn.com/break.png)

## 爬取介绍
![爬取流程](http://orxtkgfh0.bkt.clouddn.com/Break.com+%E8%A7%A3%E6%9E%90%E6%B5%81%E7%A8%8B.png)
1. http://www.break.com/most-popular/page/i 根据 i 不同即可导航到不同页面，每个页面包含 18 个视频

2. 点击第一个视频,进入到新的页面，页面包含 视频(*.mp4)、视频标题(class_='Content-title')、视频介绍(class_= "Video-description"),分别利用 bs4 解析库或者正则表达式进行匹配解析

## 已实现功能

1. 获取 [most-popular](http://www.break.com/most-popular) , [animals](http://www.break.com/animals) 两个栏目的视频直链 （2018.04.25）
2. 视频「标题 title」，「介绍 description」分别使用 **有道翻译、谷歌翻译** 进行翻译
3. 视频实现下载，包含 Break 网站内部 和 YouTube 内嵌视频
4. 多线程

## TODO
- [ ] 其它栏目：以后有空可以获取其它栏目直链 
- [x] 多线程：现在仅使用单线程获取，解析，速度太慢，平均解析写入文本需要 3s ,现在已经可以多线程下载 
- [x] 视频直链直接下载，不另外用下载器，直接对视频直链 read() 就行
- [x] 内嵌 YouTube 视频链接进行下载

## 其它
0. 异常情况要考虑，有的页面没有视频只有文字，有的页面没有标题或者介绍，爬取过程中遇到异常应保存日志并跳过
1. Break 网站需要科学上网才能进入，有些视频是 YouTube 内嵌的，解析时候需注意
2. popularByselenium 是用模拟器来爬取，速度太慢，弃用
3. 文件名不能有 ？ 等特殊字符，否则报错
