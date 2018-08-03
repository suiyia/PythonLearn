from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import codecs
from utils import googletrans
from utils import youdao


# 获取 break 网站、most-popular 页面的所有链接 1——100
def getfirstlink(): 
    for i in range(1, 101):
        dr.get("http://www.break.com/most-popular/page/" + str(i))
        videolinks = dr.find_elements_by_xpath("//a[@class='ContentCard-thumb']")
        for link in videolinks:
            # https://www.linuxhub.org/?p=3801
            result = link.get_attribute("href")
            filename = firstlink
            with open(filename, 'a') as f:
                f.write(result + '\n')
    f.close()

# 读取 firstlink.txt 的内容并  现在比较笨的方法就是模拟浏览器操作
def readfirstlink(): 
    file1 = codecs.open(titlecontentlink, 'a', 'utf-8')  # 存入这个文件
    f = open(firstlink)
    lines = f.readlines()
    #  从 count 行开始
    count = 0
    for line1 in lines[count:]:  # 读取链接 最开始的
        try:
            dr.get(str(line1))
            title = dr.find_element_by_class_name("Content-title").text  # 获取网页标题
            description = dr.find_element_by_class_name("Video-description").find_element_by_tag_name("p").text  # 内容

            bsObj = BeautifulSoup(dr.page_source, 'html.parser')
            bsElems = bsObj.find_all('script')
            p1 = re.compile(r".+\.mp4")

            for x in bsElems:  # 查找 scripts
                if p1.findall(str(x)):
                    tempstr = p1.findall(str(x))
                    tempstr = ''.join(tempstr)
                    file1.write("---------" + str(count) + "--------" + '\n')
                    print("---------" + str(count) + "--------" + '\n')
                    count = count + 1
                    file1.write("标题: " + title + '\n')
                    file1.write("谷歌翻译："+ ''.join(googletrans(title)) +'\n')
                    file1.write("有道翻译: "+ ''.join(youdao(title))+'\n')
                    print("标题: " + title + '\n')
                    file1.write("内容: " + description + "\n")
                    file1.write("谷歌翻译: " + ''.join(googletrans(description)) + '\n')
                    file1.write("有道翻译: " + ''.join(youdao(description)) + '\n')
                    print("内容: " + description + "\n")
                    file1.write("链接: " + tempstr[14:len(tempstr)] + "\n")
                    print("链接: " + tempstr[14:len(tempstr)] + "\n")
                    file1.write("\n")
                    file1.write("\n")
        except Exception as e:
            file1.write("---------" + str(count) + "--------" + '\n')
            print("---------" + str(count) + "--------" + '\n')
            file1.write("---------" + str(e) + "--------" + '\n')
            count = count + 1
            continue


if __name__ == '__main__':
    # 基本配置
    abspath = os.path.abspath("chromedriver.exe")
    dr = webdriver.Chrome(abspath)
    firstlink = os.path.abspath("text/mostpopularLink1.txt") # 读取的第一个链接
    titlecontentlink = os.path.abspath("text/mostpopularVideoLink1.txt")  # 存取的链接
    getfirstlink()

    # readfirstlink()

