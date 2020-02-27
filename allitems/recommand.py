# -*- coding: utf-8 -*-
#!/usr/bin/env python
from jieba import analyse


def getKey(reslist, keyword):
    keyList = []
    text = ""
    for resitem in reslist:
        text += resitem["title"]
    keyWords = analyse.extract_tags(text, topK=10, allowPOS=('ns', 'n', 'vn'))
    try:
        keyWords.remove(keyword)
    except:
        pass
    keyList = keyWords[:5]
    print "......."
    for i in keyList:
        print i
    print "......."
    return keyList

