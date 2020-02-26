#coding=utf-8

def bbs_set(id, pw, text):
    import urllib2, cookielib, urllib
    from bs4 import BeautifulSoup

    #First, login and store cookies
    cj = cookielib.CookieJar()  # 初始化cookie, 它从HTTP请求中提取cookie，并在HTTP响应中返回它们
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)  # 将cookie加入opener
    postdata1 = urllib.urlencode({  # 编写针对bbslogin的request-body
        'id': id,
        'pw': pw,
        'submit':'login',
    })
    req1 = urllib2.Request(url = 'https://bbs.sjtu.edu.cn/bbslogin', data = postdata1)
    urllib2.urlopen(req1)

    #Second, edit 'bbdplan' page
    postdata2 = urllib.urlencode({  #编写针对bbsplan的request-body
        'type': 'update',
        'text':text,
    })
    req2 = urllib2.Request(url = 'https://bbs.sjtu.edu.cn/bbsplan', data = postdata2)#再打开个人说明档页面
    urllib2.urlopen(req2)

    #Third, check for success
    content = urllib2.urlopen('https://bbs.sjtu.edu.cn/bbsplan').read()
    soup = BeautifulSoup(content,'html.parser')
    print str(soup.find('textarea').string).strip().decode('utf8')#查看是否修改成功,strip()去除首尾空格


def main():
    import sys
    id = 'Zsir'
    pw = 'DIANGONGDAO'
    text = 'Hello world!'
    if len(sys.argv) > 1:
        id = sys.argv[1]
        pw = sys.argv[2]
        text = ' '.join(sys.argv[3:])

    bbs_set(id,pw,text)



if __name__== '__main__' :
    main()