import urllib.request
from html.parser import HTMLParser
import re
import os
import shutil
import time

#设置url和存储路径
url = "http://www.douban.com/"
filePath = "D:\\temp"

# 读取HTML
urlContent = urllib.request.urlopen(url);
data = str(urlContent.read())

# 初始化文件目录
if os.path.isdir(filePath):
    shutil.rmtree(filePath) # 递归删除目录树
elif os.path.isfile(filePath):
    os.remove(filePath) # 删除文件
os.makedirs(filePath) # 创建目录

# 生成唯一文件名 
intFlag = 0
def getTimeStr():
    global intFlag
    intFlag = intFlag + 1
    return time.strftime("%H%M%S") + str(intFlag)

# 解析HTML 
# HTMLParser方式解析,这里HTMLParser类似于抽象类 
class MyHtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        '获取 img标签'
        if tag == "img":
            for imageUrl in attrs:
                '获取src属性'
                print(imageUrl)
                if imageUrl[0] == 'src':
                     imageUrl = imageUrl[1]
                     #print(imageUrl)
                     imageUrl = re.sub("[\\\\']", "", imageUrl)
                     iamgeUrlArr = imageUrl.split("/")
                     #print(iamgeUrlArr)
                     imgFilePath = iamgeUrlArr[len(iamgeUrlArr) - 1]
                     #print("len(iamgeUrlArr)={0}, imgFilePath={1}".format(len(iamgeUrlArr), imgFilePath))
                     try:
                       imgData = urllib.request.urlopen(imageUrl).read()
                       imgFilePath = filePath + os.sep + imgFilePath + getTimeStr() + ".jpg"
                       imageFile = open(imgFilePath, "wb")
                       imageFile.write(imgData)
                       imageFile.close()
                       print("下载文件", imageUrl, "成功,另存路径:" + imgFilePath)
                     except:
                       print("****下载文件 ", imageUrl, " 出错:")

# 调用抓取图片的API进行抓取
parser = MyHtmlParser()
# 解析HTML 
parser.feed(data)
print("获取图片操作完成")


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')
