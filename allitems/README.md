# 项目说明
本实验为本课程的大作业final projects。

我们小组制作了足篮球搜索引擎**F&B**，意为Football & Basketball。你可以查看demo.mp4
查看程序运行方式和具体的网站功能。

本次实验中我主要负责前端的设计和书写，队友HJX负责爬虫，ZR负责建立索引，WCH负责实现图片匹配，此外HJX和ZR还负责了report的书写和PPT的制作。

这是我们团队一起努力的成果，感谢老师和助教们一个学期的教导，感谢队友们的帮助和贡献！

# 实验目的
综合本学期所学知识，制作一个搜索引擎，要求包括：
1.  输入文字得到搜索结果，并能对搜索结果进行相关度排序、时间升降序排序、翻页等操作。
2.  上传图片，进行图片匹配，返回匹配结果。
3.  对网页进行一定的前端美化。

# 运行方式
首先需要在你的电脑中下载jieba库。运行程序前你需要将initWeb.py里第22行path替换成电脑中allitems文件夹的绝对地址，然后在python终端中输入“python ”+initWeb.py的地址即可运行网页服务器。

要搜索的图片需要放在allitems文件夹中（如1193.jpg），与static等文件夹同级。另外还需将该图片放在allitems/static/img/bg-img文件夹中。

# 文件说明
initWeb.py: 在本文件中构建web.py框架，并联合各个组件。

## 前端部分
1. template文件夹中存放4个html模板，其中：
    + webindex.html文件——文字搜索首页
    + index2.html——图片搜索首页
    + Rtext.html——文字搜索结果页面
    + image.html——图片搜索结果页面
    
2. static文件夹中存放前端所需的css和JavaScript库文件，其中
    + allitems/static/style.css存放两个首页的css样式
    + allitems/static/assets/style.css存放两个搜索结果页面的css样式

