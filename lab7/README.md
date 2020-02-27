# 实验目的
完善上一次lab，增加图片搜索功能，并对网页进行基本的美化

（详情请见lab7.pdf）
# 语言
python 2.7

# 运行方式
在python terminal中运行web1.py，在浏览器中输入`http://localhost:8080`后即可在搜索框中输入待搜索的信息，点击text和image按钮即可进行文字和图片的切换搜索。建议文字搜索输入`梅西`，图片搜索输入`奶粉`。

# 文件说明
finalseg和jieba:   中文分词库

indexWeb:   lab5中通过运行IndexFilesWeb.py建立起的文字索引文件夹

indexImg_v2:   通过之前实验建立起的京东商品图片索引文件夹

WebTemplates:   存放html模板

web1.py:    通过web框架联通各个组件

SearchFilesWeb.py:  针对输入的文字进行检索返回结果集

SearchFiles_image_v2.py:  针对输入的图片信息进行检索返回结果集