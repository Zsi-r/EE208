# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import urllib
import sys


def valid_filename(s):#delete backslash (and colon)
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)#生成所有大小写字母和数字,add ':'
    s = ''.join(c for c in s if c in valid_chars)#以指定字符串作为分隔符，将 ()中所有的元素(的字符串表示)合并为一个新的字符串
    return s


def get_page(page):
    try:
        content = urllib2.urlopen(page,timeout=0.3).read()
    except Exception as e:
        content = ''
        print ('TIMEOUT:'+str(e))
    return content


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content,'html.parser')
    for linkline in soup.findAll('a', {'href': re.compile('^http|^/')}):
        rlturl = linkline.get('href')#relative url
        absurl = urlparse.urljoin(page,rlturl)# absolute url
        links.append(str(absurl))
    return links


def union_dfs(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def union_bfs(a, b):
    for e in b:
        if e not in a:
            a.insert(0, e)


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)  # 将网页存入文件
    f.close()


def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    count = 0

    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            print page
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            globals()['union_%s' % method](tocrawl, outlinks)
            crawled.append(page)
            graph[page] = outlinks
            count += 1
            if count >= max_page: break
    return graph, crawled


if __name__ == '__main__':

    seed = 'https://www.runoob.com/'
    method = 'bfs'
    max_page = 20

    if len(sys.argv)>1:
        seed = sys.argv[1]
        method = sys.argv[2]
        max_page = int(sys.argv[3])

    graph, crawled = crawl(seed, method, max_page)
