__author__ = 'nourl'

import networkx as nx
from inputs.formal_edgelist import *
from sys import exit
from copy import deepcopy

C = nx.DiGraph(formal_edgelist('./benchmark_directed_networks/network.dat'))
print C.in_edges(2)
print C.out_edges(2)
eg = nx.DiGraph()
outedges = C.out_edges(2)
out_edges_final = deepcopy(outedges)
a = len(outedges)
print a
for x in outedges:
	out_two = C.out_edges(x[1])
	out_edges_final += out_two

print len(out_edges_final),"_______",out_edges_final

out_edges_weighted = []
for x in out_edges_final:
	out_edges_weighted.append((x[0],x[1],1))
eg.add_weighted_edges_from(out_edges_weighted)
egnodes=eg.nodes()
nw = {}
for x in egnodes:
	weight = eg.degree(x,weight=True) * nx.closeness_centrality(C,x)
	nw[x] = weight
#print "node_weighted: ",nw
nw_nor = {}
for key in nw.keys():
	nw_nor[key] = nw[key]/nw[2]
#print "nw_nor:",nw_nor
nw_sorted = sorted(nw_nor.iteritems(), key=lambda x:x[1],reverse=True)
#print "nw_sorted",nw_sorted
w_mean = sum(nw_nor.itervalues())/len(eg)
w_mean_filter = filter(lambda x:x>w_mean, nw_nor.itervalues())
w_mean_mean = sum(w_mean_filter)/len(w_mean_filter)
#print "w_mean: ",w_mean
#print "w_mean_mean: ",w_mean_mean
nw_percent = []
nw_percent_dic = {}
for nwx in nw_sorted:
	if nwx[0] != 2:
		nw_percent.append((nwx[0],nwx[1]))
nw_percent_dic[2] = nw_percent
print "nw_percent_dic",nw_percent_dic


