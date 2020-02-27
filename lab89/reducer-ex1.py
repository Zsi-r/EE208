#!/usr/bin/env python

from operator import itemgetter
import sys

current_character = None
current_count = 0
character = None
numofword = 0

for line in sys.stdin:
    line = line.strip()

    character,count = line.split('\t',1)

    try:
        count = int(count)
    except ValueError:
        continue

    if current_character == character:
        numofword += 1
        current_count += count
    else :
        if current_character:
            print '%s\t%s' % (current_character,current_count/float(numofword))
        current_count = count
        current_character = character
        numofword = 1

if current_character == character:
    print '%s\t%s' % (current_character,current_count/float(numofword))