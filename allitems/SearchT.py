# -*- coding: utf-8 -*-
#!/usr/bin/env python


import  os, lucene

import sys

reload(sys)

sys.setdefaultencoding("utf8")

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search import highlight


import re

vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
STORE_TEXT_DIR = "SPORTS_INDEXDIR"
searcher = None
analyzer = None

def cleantxt(raw):
	fil = re.compile(u'[^\u4e00-\u9fa5]+', re.UNICODE)
	return fil.sub(' ', raw)

def getdate(date):
    date = date[0:4] + '年' + date[4:6] + '月' + date[6:] + '日'
    return date

def parseCommand(command):
    allowed_opt = ['site']
    command_dict = {}
    opt = 'contents'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict


def runstext(command, cpage, meth):

    global vm_env, searcher, analyzer
    text = []
    print(command)
    if command == '':
        return

    command_dict = parseCommand(command)
    querys = BooleanQuery()


    for k, v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 1000).scoreDocs
    maxnum = len(scoreDocs)

    keywords = QueryParser(Version.LUCENE_CURRENT, "contents",
                          analyzer).parse(command_dict['contents'])
    reslist = []
    maxnum = min(maxnum, 100)
    for i, scoreDoc in enumerate(scoreDocs[:maxnum]):
        doc = searcher.doc(scoreDoc.doc)
        date = doc.get("date")
        score = float(scoreDoc.score)
        reslist.append([doc, date, score])


    style = highlight.SimpleHTMLFormatter("<b><font color=\'red\'>", "</font></b>")
    high_seg = highlight.Highlighter(style, highlight.QueryScorer(keywords))
    high_seg.setTextFragmenter(highlight.SimpleFragmenter(50))

    if meth == "rel":
        reslist = sorted(reslist, key=lambda res: res[2], reverse=True)
    elif meth == "td":
        reslist = sorted(reslist, key=lambda res: res[1], reverse=True)
    elif meth == "tu":
        reslist = sorted(reslist, key=lambda res: res[1], reverse=False)
    print keywords
    start = (cpage - 1) * 10
    end = min(start + 10, maxnum)
    print start, end
    for i in reslist[start: end]:
        doc = i[0]
        score = i[2]
        date = str(getdate(i[1]))
        text_dic = {}
        text_dic['title'] = doc.get("title").strip('-直播吧zhibo8.cc').strip('_新浪竞技风暴_新浪网')
        text_dic['url'] = doc.get("url")
        tmpcontent = cleantxt(doc.get("contents"))
        keyword = high_seg.getBestFragment(analyzer, "contents", tmpcontent)
        text_dic['keyword'] = keyword
        text_dic['score'] = score
        text_dic['date'] = date
        text.append(text_dic)

    '''for i, scoreDoc in enumerate(scoreDocs):
        text_dic = {}
        doc = searcher.doc(scoreDoc.doc)

        text_dic['title'] = doc.get("title")
        text_dic['url'] = doc.get("url")
        keyword = high_seg.getBestFragment(analyzer, "contents", cleantxt(doc.get('contents')))
        text_dic['keyword'] = keyword
        text.append(text_dic)'''

    return text, maxnum

def text_search(command, cpage, meth):
    global vm_env, searcher, analyzer

    vm_env.attachCurrentThread()
    print 'lucene', lucene.VERSION
    directory = SimpleFSDirectory(File(STORE_TEXT_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    text, maxnum = runstext(command, cpage, meth)

    del searcher

    return text, maxnum