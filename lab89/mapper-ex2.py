#!/usr/bin/env python

import sys

try:
    class Page:
        def __init__(self, id, pk):
            self.id = id
            self.pk = pk


    d = 0.85
    N = 0  # total num of pages
    Pagelist = []
    linkrelation = {}

    for line in sys.stdin:
        N += 1
        line = line.strip()
        page_id, page_pk, strlinkid = line.split(None, 2)
        page_id = int(page_id)
        page_pk = float(page_pk)
        Pagelist.append(Page(page_id, page_pk))
        linkrelation[page_id] = strlinkid

    # initial pagerank and relationship of pages
    for page in Pagelist:
        listlinkid = linkrelation[page.id].split()
        print '%s=%s;%s:%s' % (str(page.id),0,page.id,linkrelation[page.id])
        length = len(listlinkid)
        for i in listlinkid:
            print '%s=%s;%s:%s' % (str(i), page.pk / float(length),page.id,linkrelation[page.id])
#2=0.8333;1:2 3 4

except Exception , Argument:
    print str(Argument)




    
