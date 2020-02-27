#!/usr/bin/env python
#coding=utf-8

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, jieba
import finalseg
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader,Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

def run(command,STORE_DIR):

    res_list = []
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)

    command = unicode(command)

    if command == '':
        return

    #print "Searching for:", command

    seg_list = jieba.cut(command)
    command1 = " ".join(seg_list)
    print command1

    querys = QueryParser(Version.LUCENE_CURRENT, "alt",
                       analyzer).parse(command1)
    # 用analyzer来对查询语句进行词法分析和语言处理。
    # QueryParser调用parser进行语法分析，形成查询语法树，放到Query中。
    scoreDocs = searcher.search(querys, 50).scoreDocs#IndexSearcher调用search对查询语法树Query进行搜索，得到结果
    print "%s total matching documents." % len(scoreDocs)

    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        temp = {}
        temp["imgurl"] = doc.get("imgurl")
        temp["url"] = doc.get("url")
        temp["urltitle"] = doc.get("alt")
        res_list.append(temp)
    return res_list

'''
    print "------------------------------------"
    print 'imgurl:',doc.get("imgurl")
    print "url:",doc.get("url")
    print "urltitle:",doc.get("alt")
    # print 'explain:', searcher.explain(query, scoreDoc.doc)
'''

'''
if __name__ == '__main__':#enter:婴儿 or  enter:雀巢 or enter:奶粉
    STORE_DIR = "indexImg_v2"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])#初始化Java虚拟机
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))#索引文件存放的位置
    searcher = IndexSearcher(DirectoryReader.open(directory))#索引信息读入到内存，创建IndexSearcher准备进行搜索
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)#analyzer用来对查询语句进行词法分析和语言处理的，和IndexFiles.py中使用同样的analyzer。
    run(searcher, analyzer)
    del searcher
'''