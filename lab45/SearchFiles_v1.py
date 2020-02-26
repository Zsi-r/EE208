#!/usr/bin/env python
#coding=utf-8

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
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
def parseCommand(command):

    command_dict = {}
    opt = u"contents"
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()#大写转小写
            if opt ==u"site" and value != '':
                command_dict[opt] = ' '+value#get取回键对应的值
        else:
            command_dict[opt] = command_dict.get('contents', '') + ' ' + i
    return command_dict

def run(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query:")
        command = unicode(command, 'utf-8',"ignore")

        if command == '':
            return

        print "Searching for:", command.encode("utf-8","ignore")
        #seg_list = finalseg.cut(command, find_new_word=True)
        #command1 = " ".join(seg_list)

        command_dict = parseCommand(command)
        querys = BooleanQuery()
        for k,v in command_dict.iteritems():
            if k == u"contents":#如果是对内容搜索，需要分词
                seg_list = finalseg.cut(v, find_new_word=True)
                v = " ".join(seg_list)
            query = QueryParser(Version.LUCENE_CURRENT, k,
                                analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)

        #querys = QueryParser(Version.LUCENE_CURRENT, "contents",
        #                   analyzer).parse(command1)

        scoreDocs = searcher.search(querys, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            """
            print 'path:', doc.get("path"), 'title:', doc.get("title")
            print 'url:', doc.get("url"),'name:', doc.get("name")
            """
            print "------------------------------------"
            print 'path:',doc.get("path")
            print "title:",doc.get("title")
            print "url:",doc.get("url")
            print "name:",doc.get("name")
            print "site:",doc.get("site")

if __name__ == '__main__':#enter : 梅西 site:2018.sina.com.cn  or  enter:曼城 site:sports.sina.com.cn
    STORE_DIR = "index_v1"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
