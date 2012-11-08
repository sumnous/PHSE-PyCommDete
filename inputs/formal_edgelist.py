#!/usr/bin/env python
# -*- coding: utf8 -*-
def formal_edgelist(fname):
    f = file(fname, 'r')
    edgelist=[]
    for x in f:
        x = x[:-1].split(' ')
        x[0]=int(x[0])
        x[1] = int(x[1])
        x=tuple(x)
        edgelist.append(x)
    f.close()
    return edgelist
