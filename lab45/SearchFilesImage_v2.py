#!/usr/bin/env python
#coding=utf-8

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

def run(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query:")#输入查询语句
        command = unicode(command, 'utf-8')

        if command == '':
            return

        print "Searching for:", command

        seg_list = jieba.cut(command)
        command1 = " ".join(seg_list)
        print command1

        querys = QueryParser(Version.LUCENE_CURRENT, "alt",
                           analyzer).parse(command1)

        scoreDocs = searcher.search(querys, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)

            print "------------------------------------"
            print 'imgurl:',doc.get("imgurl")
            print "url:",doc.get("url")
            print "urltitle:",doc.get("title")
            # print 'explain:', searcher.explain(query, scoreDoc.doc)


if __name__ == '__main__':#enter:婴儿 or  enter:雀巢 or enter:奶粉
    STORE_DIR = "indexImg_v2"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])#初始化Java虚拟机
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
