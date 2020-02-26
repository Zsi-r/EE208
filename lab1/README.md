# 实验目的
通过bs4和urllib2实现基本的爬虫功能

（详情请见报告EE report 1.pdf）
# 语言
python 2.7
# 工具
python库urllib2	bs4	urlparse	sys	re
# 命令行输入说明
三个py文件都可以在python命令行窗口运行，格式为“python 文件名 目标网页的URL”。
建议在这条命令前添加“cd pycharm的绝对地址”，以免res.txt文件不知道建在哪了。
如：

	>> cd ~/PycharmProjects/ex1
	>> python ex1-1.py https://www.bilibili.com/

# 函数参数说明
1.	```parseURL(content)```,  ```parseIMG(content)```只有一个参数，其中```content```从```content = urllib2.urlopen(url).read()```得到。
2. ```parseZhihu(content,url)```有两个参数，其中```content```同上，```url```是目标网页的URL，可以是py文件里默认的或从命令行窗口输入的。
3.	```write_outputs(set1, 'res.txt')```有两个参数，第一个是从函数parseUR()(或函数parseIMG()，函数parseZhihu())得到的结果集，第二个是存入爬取结果的txt文件