#coding=utf-8
import sys
import urllib2
import re
from bs4 import BeautifulSoup


def parseURL(content):
    urlset = set()
    soup=BeautifulSoup(content,'html.parser')
    for i1 in soup.findAll('a',{'href':re.compile('^http.*$')}):
        i2 = i1.get('href')
        urlset.add(str(i2))
    for i3 in soup.findAll('a',{'href':re.compile('^//.*$')}):
        i4 = i3.get('href')
        urlset.add(str(i4))
    return urlset


def write_outputs(urls, filename):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(url)
            f.write('\n')


def main():
    #url = 'http://www.sjtu.edu.cn'
    #url = 'https://www.bilibili.com/'
    url = 'http://www.baidu.com'
    if len(sys.argv) > 1:#get url from the terminal; sys.argv[0]==the py file itself; sys.argv[1:]==the parameter(i.e. url) from the terminal
        url = sys.argv[1]
    content = urllib2.urlopen(url).read()
    urls = parseURL(content)
    write_outputs(urls, 'res1.txt')


if __name__ == '__main__':
    main()







