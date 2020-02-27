#!/usr/bin/env python
#coding=utf-8

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
from org.apache.lucene.search.highlight import Fragmenter,Highlighter,QueryScorer,SimpleHTMLFormatter,SimpleFragmenter

def parseCommand(command):

    command_dict = {}
    opt = "contents"
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()#大写转小写
            if opt =="site" and value != '':
                command_dict[opt] = ' '+value#get取回键对应的值
        else:
            command_dict[opt] = command_dict.get('contents', '') + ' ' + i
    return command_dict

def run(command,command_dict,STORE_DIR):
    res_list = []
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)

    command = unicode(command)

    if command == '':
        return

    querys = BooleanQuery()
    for k,v in command_dict.iteritems():
        if k == "contents":#如果是对内容搜索，需要分词
            seg_list = finalseg.cut(v, find_new_word=True)
            v = " ".join(seg_list)
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 50).scoreDocs

    #构建Formatter格式化最终显示(将字体颜色设置为斜体红色),_blank_用于后面替换成空格
    simpleHTMLFormatter = SimpleHTMLFormatter("<i><font_blank_color='red'>", "</font></i>")
    #构造FieldQuery
    queryHlt = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(command_dict['contents'])
    #构建Scorer,用于选取最佳切片
    scorer = QueryScorer(queryHlt)
    #实例化Highlighter组件
    highlighter = Highlighter(simpleHTMLFormatter, scorer)
    #默认字符为100
    highlighter.setTextFragmenter(SimpleFragmenter(100))

    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        temp = {}
        temp["url"] = doc.get("url")
        temp["title"]= doc.get("title")
        temp["site"] = doc.get("site")
        temp["highlight"]= highlighter.getBestFragment(analyzer, "contents",doc.get("contents"))
        res_list.append(temp)
    return res_list

'''
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
'''

'''
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
'''