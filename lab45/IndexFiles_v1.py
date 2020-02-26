#!/usr/bin/env python
#coding=utf-8

INDEX_DIR = "IndexFiles.index"

import urlparse
import finalseg
import sys, os, lucene, threading, time
from datetime import datetime
from bs4 import BeautifulSoup
import re

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir,indextxtpath):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))

        analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)

        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer,indextxtpath)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer,indextxtpath):

        t1 = FieldType()#文档的文件名name,路径path,标题title,网址url的FieldType
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)
        
        t2 = FieldType()#文档内容contents2相关的FieldType
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        t3 = FieldType()#site相关的FieldType
        t3.setIndexed(True)
        t3.setStored(True)
        t3.setTokenized(False)
        t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                print "adding", filename
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    contents = unicode(file.read(), 'utf-8')
                    file.close()

                    doc = Document()#创建一个Document代表我们要索引的文档
                    doc.add(Field("name", filename, t1))
                    doc.add(Field("path", path, t1))
                    if len(contents) > 0:
                        charset1 = re.search("charset(?:=\"|=)([^\"]*)", contents)
                        charset = charset1.groups()[0]

                        soup= BeautifulSoup(contents,"html.parser")
                        contents2 = ''.join(soup.findAll(text=True))#unicode
                        seg_list = finalseg.cut(contents2, find_new_word=True)
                        contents3 = " ".join(seg_list)
                        doc.add(Field("contents",contents3, t2))

                        i1 = soup.find('title')
                        title = i1.string.encode(charset,"ignore")
                        doc.add(Field('title',title,t1))
                    else:
                        print "warning: no content in %s" % filename

                    doc.add(Field('url',files[filename],t1))

                    domain = urlparse.urlparse(files[filename]).netloc
                    doc.add(Field('site',domain,t3))

                    writer.addDocument(doc)

                except Exception, e:
                    print "Failed in indexDocs:", e

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    indextxt = "/media/sf_UbuntuFile/ex4/index_v1.txt"

    f = open(indextxt,'r')
    files = {}
    for line in f.readlines():
        temp = line.strip().split('\t')
        if len(temp)<=1:
            continue
        files[temp[1]]=temp[0]
    f.close()

    try:
        IndexFiles('html_v1', "index_v1",indextxt)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
