#coding=utf-8
import web,os,web,lucene,urllib2
from web import form
import SearchFilesWeb,SearchFiles_image_v2
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

try:
    vm_ev = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
except:
    vm_env = lucene.getVMEnv()

urls = (
    '/', 'index',
    '/im','index_image',
    '/s', 'text',#result of text search
    '/i','image'#result of image search
)


render = web.template.render('WebTemplates') # your templates


class index:
    def GET(self):
        vm_env.attachCurrentThread()
        return render.textindex()

class index_image:
    def GET(self):
        vm_env.attachCurrentThread()
        return render.imageindex()

class text:
    def GET(self):
        vm_env.attachCurrentThread()
        STORE_DIR = "indexWeb"#索引文件夹位置
        directory = SimpleFSDirectory(File(STORE_DIR))
        searcher = IndexSearcher(DirectoryReader.open(directory))#建立搜索器
        command = web.input().Google#获取索引目标
        #以下两行通过运行SearchFilesWeb.py里的函数得到索引结果command_dict
        command_dict = SearchFilesWeb.parseCommand(command)
        res_list = SearchFilesWeb.run(command,command_dict,STORE_DIR)

        return render.textresult(command,res_list,searcher)

class image:
    def GET(self):
        vm_env.attachCurrentThread()
        STORE_DIR = "indexImg_v2"#索引文件夹位置
        directory = SimpleFSDirectory(File(STORE_DIR))
        searcher = IndexSearcher(DirectoryReader.open(directory))#建立搜索器
        command = web.input().Google#获取索引目标
        res_list = SearchFiles_image_v2.run(command,STORE_DIR)

        return render.imageresult(command,res_list,searcher)

if __name__ == "__main__":
    #梅西  西甲
    app = web.application(urls, globals())
    app.run()
