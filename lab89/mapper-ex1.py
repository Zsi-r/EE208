#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    for word in words:
        word = word.lower()
        lenth = len(word)
        for character in list(word):
            if (character>='a' and character <='z'):
                print '%s\t%s' % (character,lenth)