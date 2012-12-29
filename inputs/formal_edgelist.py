# -*- coding: utf8 -*-

from config import *

def formal_edgelist(fname):
    f = file(fname, 'r')
    f_write = file(base +'/inputs/network.edgelist', 'w+')

    edgelist=[]
    for x in f:
        # x = x[:-1].split(' ')
        x = x[:-1].split('\t')
        x[0]=int(x[0])
        x[1] = int(x[1])
        x=tuple(x)
        edgelist.append(x)
    f_write.writelines(str(edgelist))
    f_write.close()
    f.close()
    return edgelist
