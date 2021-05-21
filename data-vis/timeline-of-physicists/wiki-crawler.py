from lxml import etree

# wikihtml = open('list-of-physicists-wikipedia.html',mode='r',encoding='utf8')
# wikicontent = wikihtml.read()
# print(wikicontent)

wikihtml = etree.parse('list-of-physicists-wikipedia.html')
# print(type(html))

result0 = wikihtml.xpath('//*[@id="mw-content-text"]/div/ul[1]/li[9]/a')
result1 = wikihtml.xpath('//*[@id="mw-content-text"]/div/ul[1]/li[9]/a/@href')
result2 = wikihtml.xpath('//*[@id="mw-content-text"]/div/ul[1]/li[9]/a/@title')
# print(result1[0],result2[0])
print(result0[0].getchildren)
print(dir(result0[0]))
