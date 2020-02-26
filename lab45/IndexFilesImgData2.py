#!/usr/bin/env python
#coding=utf-8


import  os,re
from bs4 import BeautifulSoup

if __name__ == '__main__':

    root = "/media/sf_UbuntuFile/lab4/htmlImg_v2"
    indextxt = "/media/sf_UbuntuFile/lab4/indexImg_v2.txt"

    f = open(indextxt, 'r')
    files = {}
    for line in f.readlines():
        temp = line.strip().split('\t')
        if len(temp) <= 1:
            continue
        files[temp[1]] = temp[0] # filename --> url
    f.close()

    crawled = []

    for root, dirnames, filenames in os.walk(root):
        for filename in filenames:
            print "adding", filename
            try:
                imgurl = ''
                alt = ''
                path = os.path.join(root, filename)
                file = open(path,'r')
                contents = file.read()
                file.close()

                soup = BeautifulSoup(contents,"html.parser")

                title = soup.title.text.strip()
                if title == None:
                    continue

                for linkline in soup.findAll('img',{"id":re.compile('spec-img')}):
                    imgurl = linkline.get('data-origin')
                    alt = linkline.get("alt")
                    if imgurl == None or alt == None:
                        continue

                if imgurl in crawled:#如果图片已经爬取过
                    continue
                else :
                    crawled.append(imgurl)

                if filename in files:
                    url = files[filename]
                else:
                    continue

                print '-----------------------------------------'
                print "url: ",url
                print "alt: ",alt
                print "imgurl: ",imgurl
                print "title: ",title
                print '-----------------------------------------'
                with open("imgdata_v2.txt",'a') as f2:
                    line = imgurl+'\t'+url+'\t'+alt+"\t"
                    f2.write(line.encode('utf-8','ignore')+'\n')


            except Exception, e:
                print "Failed : ", e