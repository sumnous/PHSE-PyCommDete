__author__ = 'nourl'
from common.transform import *

from PyCommDete import *
from networkx import nx
from inputs.formal_edgelist import *

from multiprocessing import Pool
from sys import exit

#C = nx.read_gml(filelist[1])
C = nx.Graph(formal_edgelist('./benchmarks/network.dat'))
print "length:",len(C)
betw_ori = nx.betweenness_centrality(C)
degr_ori = C.degree()
nodes = C.nodes()

betw_ori = sorted(betw_ori.iteritems(), key=lambda x:x[1],reverse=True)
average = sum(x[1] for x in betw_ori)/len(betw_ori)
betw=[x for x in betw_ori if x[1]>=0.2*average]
betw_ex_nei=[x[0] for x in betw]
bitmap = [0]*len(betw_ori)

print "len of betw_ex_nei:",len(betw_ex_nei)
for x in betw_ex_nei:
	bitmap[x-1]=x
recover=[]
for x in betw_ex_nei:
	if bitmap[x-1] >0:
		recover.append(x)
		nei = C.neighbors(x)
		for n in nei:
			bitmap[n-1] = 0
for x in recover:
	bitmap[x-1]=x
seed_betw = [node for node in nodes if bitmap[node-1]]
print "len of betw:",len(seed_betw)
print "seed_betw:",seed_betw

degr_ori = sorted(degr_ori.iteritems(), key=lambda x:x[1],reverse=True)
average = sum(x[1] for x in degr_ori)/len(degr_ori)
degr=[x for x in degr_ori if x[1]>=0.2*average]
degr_ex_nei=[x[0] for x in degr]
bitmap = [0]*len(degr_ori)

print "len of degr_ex_nei:",len(degr_ex_nei)
for x in degr_ex_nei:
	bitmap[x-1]=x
recover=[]
for x in degr_ex_nei:
	if bitmap[x-1] >0:
		recover.append(x)
		nei = C.neighbors(x)
		for n in nei:
			bitmap[n-1] = 0
for x in recover:
	bitmap[x-1]=x
seed_degr = [node for node in nodes if bitmap[node-1]]
print "len of degr:",len(seed_degr)
print "seed_degr",seed_degr

seed_cross=list(set(seed_betw).intersection(set(seed_degr)))
print "len of seed_cross:",len(seed_cross)
print "seed_cross:",seed_cross





