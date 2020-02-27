#!/usr/bin/env python

from operator import itemgetter
import sys

try:
    N = 4
    d = 0.85
    totalpk = 0
    current_page = None
    current_pk = 0
    pk_dic={}
    linkrelation = {}
    page_id = None
    linkid = None

    #in the form: 
    # 2=0.8333;1:2 3 4

    for line in sys.stdin:
        line = line.strip()
        if line:
            PageandRank,PageandRelation = line.split(';')

        Pageid_in_relation,linkid = PageandRelation.split(':')
        linkrelation[Pageid_in_relation] = linkid

        page_id,page_pk = PageandRank.split('=')
        page_pk = float(page_pk)

        if page_id in pk_dic:
            pk_dic[page_id].append(page_pk)
        else:
            pk_dic[page_id]=[]
            pk_dic[page_id].append(page_pk)

    for page in pk_dic.keys():
        for pk in pk_dic[page]:
            totalpk += pk
        finalpk = (1-d)/N + d*(totalpk)
        print '%s\t%s\t%s' % (page,finalpk,linkrelation[page])
        totalpk = 0

except Exception,e:
    print e

