#coding=utf-8
#不要对str使用编码，不要对unicode使用解码
#以str输出，用encode转换，以unicode（utf8）输入，用decode转换
import sys
import urllib2
import urlparse
from bs4 import BeautifulSoup


def parseZhihu(content,url):
    set1 = set()
    soup = BeautifulSoup(content,'html.parser')
    for i in soup.findAll('a',{'class':'link-button'}):
        picsrc = i.contents[0].get('src')#get picture source

        titleline = i.contents[1]#get title
        title = titleline.string.encode('utf8')#string is unicode ,need to be encode
        if ( not title ): title = ''#if title==None

        linkpage = i.get('href')#get hyperlink address
        linkpage = urlparse.urljoin(url, linkpage)

        set1.add(str(picsrc)+'\n'+str(title)+'\n'+str(linkpage))

    return set1


def write_outputs(set1, filename):
    with open(filename, 'w') as f:
        for i in set1:
            f.write(i)
            f.write('\n')


def main():
    url = 'http://daily.zhihu.com/'
    if len(sys.argv) > 1:#get url from the terminal; sys.argv[0]==the py file itself; sys.argv[1:]==the parameter(i.e. url) from the terminal
        url = sys.argv[1]
    content = urllib2.urlopen(url).read()
    set1 = parseZhihu(content,url)# !!! changed: add the new parameter 'url' to pass the target url to parseZhihu
    write_outputs(set1, 'res3.txt')

if __name__ == '__main__':
    main()
