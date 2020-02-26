#coding=utf-8
import sys
import urllib2
import re
from bs4 import BeautifulSoup


def parseIMG(content):
    imgset = set()
    soup=BeautifulSoup(content,'html.parser')
    for i1 in soup.findAll('img'):
        i2=i1.get('src')
        imgset.add(str(i2))
    return imgset


def write_outputs(imgs, filename):
    with open(filename, 'w') as f:
        for img in imgs:
            f.write(img)
            f.write('\n')


def main():
    # url = 'http://www.sjtu.edu.cn'
    # url = 'https://www.bilibili.com/'
    url = 'http://www.baidu.com'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    content = urllib2.urlopen(url).read()
    imgs = parseIMG(content)
    write_outputs(imgs, 'res2.txt')


if __name__ == '__main__':
    main()
