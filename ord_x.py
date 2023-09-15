# -*- coding: utf-8 -*-
import os, sys

with open("fullformsliste.txt", encoding="utf8", errors='ignore') as f:
    for line in f:
        linje = line.split('\t')
        ord = linje[2]
        klasse = (linje[3].split(' '))
        l = len(ord)

        if ord[0] == 'x' or ord[0] == 'X':
            print(ord)
