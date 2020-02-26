# 语言
python 2.7
# 工具
python库：Lucene  finalseg
# 实验目的
1. 爬取一定的中文网页（本次实验我爬取了网页2018.sina.com.cn），并对这些中文网页建立索引并进行搜索
2. 实现搜索引擎的 “site:” 功能（对搜索的网站进行限制）
3. 实现一个图片索引（本次实验我对京东商品图片页面进行爬取和建立索引），输入文本，输出相关的图片地址，图片所在网页的网址， 图片所在网页的标题。

（详情请见报告EE report45_v1.pdf）
# 文件说明
文件夹finalseg和jieba:  中文分词库

index_v1:   存放爬取的中文网页源码

indexImg_v2:    存放爬取的京东图片所在的网页源码

index_v1.txt:   存放所有爬取的中文网页url

indexImg_v2.txt:    存放所有爬取的京东图片所在的网页url

imgdata_v2.txt: 存放爬取的京东商品信息，格式为“图片url  网页url 图片名称”

IndexFiles_v1.py:   对中文网页进行爬取

IndexFilesImage_v2.py:  对京东商品图片网页进行爬取

IndexFilesImgData2.py:  对爬取到的图片进行信息提取，得到imgdata_v2.txt

SearchFiles_v1.py:  对爬取的中文网页建立索引

SearchFilesImage_v2.py: 对爬取的图片建立索引