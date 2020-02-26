#!/usr/bin/env python
#coding=utf-8

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time,re
from datetime import datetime
import finalseg
import jieba

from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
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

    def __init__(self,storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))   #索引文件存放的位置
        analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576) #analyzer是用来对文档进行词法分析和语言处理的
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)
        # 创建一个IndexWriter用来写索引文件

        self.indexDocs(writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, writer):

        t1 = FieldType()#title,url,imgurl
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)
        
        t2 = FieldType()#alt
        t2.setIndexed(True)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        with open("/media/sf_UbuntuFile/lab4/imgdata_v2.txt","r") as imgfile:
            for line in imgfile.readlines():
                doc = Document()

                linelist = line.split('\t')
                imgurl = linelist[0]
                url = linelist[1]
                alt = linelist[2]

                doc.add(Field("imgurl", imgurl,t1))
                doc.add(Field("url",url,t1))
                doc.add(Field("title", alt, t1))

                seg_list = jieba.cut(alt)
                altTokened = " ".join(seg_list)

                doc.add(Field("alt",altTokened,t2))

                writer.addDocument(doc)




if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()

    IndexFiles("indexImg_v2")
    end = datetime.now()
    print end - start

