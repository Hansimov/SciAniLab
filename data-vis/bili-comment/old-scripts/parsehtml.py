# python爬虫入门教程--HTML文本的解析库BeautifulSoup
#   http://www.jb51.net/article/114663.htm

# python中html解析-Beautiful Soup
#   https://www.cnblogs.com/hester/p/5495875.html

'''
Beautiful Soup 将复杂 HTML 文档转换成一个复杂的树形结构，每个节点都是Python对象，所有对象可以归纳为4种:

1. Tag
    soup.<tag> 查找所有内容中第一个符合要求的标签
    属性：name, attrs

2. NavigableString
    soup.<tag>.string 获取标签内部文本

3. BeautifulSoup
    BeautifulSoup 对象表示的是一个文档的全部内容。
    大部分时候,可以把它当作 Tag 对象，是一个特殊的 Tag。
4. Comment
    Comment 对象是一个特殊类型的 NavigableString 对象，其实输出的内容仍然不包括注释符号。
    但是如果不好好处理它，可能会对我们的文本处理造成意想不到的麻烦。
'''

from bs4 import BeautifulSoup

htmlfile = open('example.html','r',encoding='utf-8')
htmltext = htmlfile.read()

soup= BeautifulSoup(htmltext,"html.parser")

print(soup.prettify())
htmlfile.close()
