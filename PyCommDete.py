# -*- coding: utf8 -*-
from __future__ import division

import sys
import networkx as nx
import matplotlib.pyplot as plt

from config import *
from random import random
from multiprocessing import Process, Pool
from inputs.formal_edgelist import formal_edgelist

filelist=['./inputs/GML/polbooks.gml', \
		  './inputs/GML/karate.gml',   \
		  './inputs/GML/dolphins.gml', \
		  './inputs/GML/netscience.gml']

f = file('./interdata', 'w+')
fr = file('./result', 'w+')
#C = nx.read_gml(filelist[1])
C = nx.Graph(formal_edgelist('./benchmarks/benchmark_2_2/network.dat'))

def get_maximum_cliques(network):
	# find the maximum cliques in network C, clique's nodes are over 2.
	# http://networkx.lanl.gov/reference/algorithms.clique.html
	cl = [x for x in nx.find_cliques(network)]
	cl_over_2 = filter(lambda x:len(x)>2, cl)
	seeds = deal_cliques(cl_over_2)
	#print ":::::::::::",seeds
#	sys.exit(0)

	count_len = [len(x) for x in seeds]

	if avg_type == 0:
		MinSeedSize = 3
	elif avg_type == 1:
		MinSeedSize = 4
	elif avg_type == 2:
		MinSeedSize = sum(count_len)/len(seeds)
	elif avg_type ==3:
		ave = sum(count_len)/len(seeds)
		sum_tem = sum(map(lambda x:pow((ave-x),2),count_len))
		MinSeedSize = ave - pow(sum_tem/len(seeds),0.5)
	#		for x in count_len:
	#			sum_tem = sum_tem + pow((ave-x),2)

	print "MinSeedSize: ", MinSeedSize
	seeds = [x for x in seeds if len(x) >= MinSeedSize]
	out_list = ["seeds", str(seeds), '\n']
	f.writelines(out_list)
	print "seeds:\n", seeds
	print "number of seeds for computing: ", len(seeds)
	return seeds

def deal_cliques(cliques):
	new_cliques = deal_cliques_once(cliques)
	while new_cliques != cliques:
		cliques = new_cliques
		new_cliques = deal_cliques_once(cliques)
	return new_cliques

def deal_cliques_once(cliques):
	le = len(cliques)
	if le == 0:
		return []
	if le == 1:
		return list(cliques[0])

	# sort the list of lists based on the length of the list
	cliques.sort(key=lambda x:len(x), reverse=True)
	# merge the cliques if they are shared n-1 nodes
	result=[]
	current=[]
	bitmap=[0]*len(cliques)
	btlen = len(bitmap)
	while sum(bitmap) < btlen:
		for i in range(btlen):
			if not bitmap[i]:
				current.append(i)
				bitmap[i] = 1
				break
#				TODO

		remain=[x for x in range(btlen) if bitmap[x]==0]

		def c_match(current_list, c):
			x = set(cliques[c])
			for i in current_list:
				y = set(cliques[i])
				if len(x) == len(y) and len(x.intersection(y)) == len(y)-1:
					return True
			return False

		for c in remain:
			if c_match(current, c):
				current.append(c)
				bitmap[c] = 1
		tmp=set()
		for x in current:
			tmp = tmp.union(cliques[x])
		result.append(tmp)
		current=[]
	return result

def get_neighbors(Graph):
	"""find subgraph's(or graph, type is Graph) neighbor nodes in original graph C"""
	flag={}
	def mark_true(x):
		t = C.neighbors(x)
		for x in t:
			flag[x]=1
	map(mark_true, Graph.nodes())
	for x in Graph.nodes():
		flag[x]=0

	return [x for x in C.nodes() if flag.get(x)]

def get_fitness(Graph):
	"""compute the fitness of the graph"""
	if len(Graph.nodes()) == 1:
		return float(0)
	kin = 2 * len(Graph.edges())
	G_neighbors = get_neighbors(Graph)   # find G's neighbor nodes
	G_with_neighbors = G_neighbors + Graph.nodes()
	G_nei = nx.Graph(C.subgraph(G_with_neighbors))
	kout = len(G_nei.edges()) - len(Graph.edges())
	fitness_G = kin / pow((kin+kout), alpha)
	return fitness_G

def get_fitness_v_max(Graph):
	"""这有个问题，如果最大贡献度所对应的节点有多个怎么处理，是添加第一个最大的节点，还是所有的都添加
	compute the fitness_v(dic, {node, fitness of adding vertex}), find fitness_v_max"""
	G_neighbors = get_neighbors(Graph)
	v_max_node=[float(-100),-1]
#	vertex_list = [] # 添加一个初始值,将最大贡献度所对应的一些节点一起加入社区
	if G_neighbors == []:
		pass
	else:
		G_nodes = Graph.nodes()
		result=[]
		for x in G_neighbors:
			val = get_fitness(nx.Graph(C.subgraph((G_nodes+[x]))))
			result.append([val, x])

		for c in result:
			if c[0]>v_max_node[0]:
				v_max_node = []
				v_max_node = c
			elif c[0] == v_max_node[0]:
				v_max_node.append(c[1])
			else:
				pass
	return (v_max_node[1:], v_max_node[0])

def get_fitness_v_community(Graph):
	"""节点对社区的贡献度"""
	(vertex_list, fitness_v_max) = get_fitness_v_max(Graph)
	fitness_v_community	= fitness_v_max - get_fitness(Graph)
	#fitness_v_community += correct
	return (vertex_list, fitness_v_community)

def get_nature_community(Graph):
	# form the new community G_iter, if fitness_v_max > 0
	(vertex_list, fitness_v_community) = get_fitness_v_community(Graph)
	G_nature_community = Graph
	if vertex_list == []:
		return G_nature_community
	out_list = ["(vertex_list, fitness_v_community)", str((vertex_list, fitness_v_community)), '\n']
	f.writelines(out_list)
	G_nodes = Graph.nodes()
	if fitness_v_community > 0: # 将节点对社区的贡献度大于0的节点加入社区.为什么不是0的时候这么慢？？？
		G_nodes += vertex_list
		G_iter = nx.Graph(C.subgraph(G_nodes))
		out_list = [str(G_iter.nodes()), '\n']
		f.writelines(out_list)
		G_nature_community = get_nature_community(G_iter)
	return G_nature_community

def process_f(cli_list):
	tmp_result = []
	while len(cli_list) > 0:
		c = cli_list.pop()
		comm = get_nature_community(nx.Graph(C.subgraph(c)))
		if len(comm) == len(C):
			continue
		tmp_result.append(comm)
		def is_not_subset(a):
			for x in a:
				if x not in comm:
					return True
			return False
		cli_list = filter(is_not_subset, cli_list)
	return tmp_result

def get_all_nature_community(network):
	cliques = get_maximum_cliques(network)
	pool_result = []
	process_num=6
	pool = Pool(process_num)
	cli_len = len(cliques)
	for i in range(process_num):
		args=([cliques[j] for j in range(cli_len) if j%process_num==i],)
		pool_result.append(pool.apply_async(process_f,args))
		
	pool.close()
	pool.join()
	
	communities=[]
	for item in [x.get() for x in pool_result]:
		communities = communities+item
	
	all_nodes = network.nodes()
	comm_nodes=[]
	for x in communities:
		comm_nodes = comm_nodes + x.nodes()
	left_list = [x for x in all_nodes if x not in comm_nodes]

	while len(left_list)>0:
		seed_node = get_degree_max(left_list)
		print "seed_node",seed_node
		single_node_Graph = nx.Graph()
		single_node_Graph.add_node(seed_node)
		single_node_Graph = get_nature_community(single_node_Graph)
		sngn = single_node_Graph.nodes()
		print "seed_community: ", sngn
		communities.append(single_node_Graph)
		for x in sngn:
			if x in left_list:
				left_list.remove(x)

	i = 0
	for x in communities:
		print "i = ",i,x.nodes()
		i = i+1

	communities = deal_communities(communities)
	return communities

def deal_communities(communities):
	# if there are some communities are the same, than delete
	le = len(communities)
	cnode_len = len(C.nodes())

	bm=[0]*le
	for i in range(le):
		if not bm[i]:
			for j in range(i+1,le):
				if compare_communities(communities[i].nodes(), communities[j].nodes()):
					bm[j] = 1

	for i in range(le-1,-1,-1):
		if bm[i] or len(communities[i])==cnode_len:
			communities.pop(i)

	f.writelines("++++++++++++++++++++++\n")
	out_list = [str(x.nodes()) for x in communities]
	f.writelines(out_list)
	f.writelines("\n\n\n")

	# is_sub_graph
	def to_be_del(item, com):
		for x in com:
			if len(x)> len(item) and set(item).issubset(set(x.nodes())):
					return True
		return False

	bitmap=[0]*len(communities)
	for i in range(len(communities)):
		if to_be_del(communities[i].nodes(), communities):
			bitmap[i]=1
	for i in range(len(bitmap)-1, -1, -1):
		if bitmap[i]:
			communities.pop(i)
	return communities

def get_communities_overlapping_degree(community1, community2):
	nei1 = get_neighbors(community1)
	nei2 = get_neighbors(community2)
	val_o = get_overlapping_nodes(community1.nodes(), community2.nodes())
	val_m = get_merging_nodes(community1.nodes(), community2.nodes())
	if len(nei1)==0 and len(nei2)==0:
		cod = len(val_o) / len(val_m)
	else:
		cod = beta*len(val_o) / len(val_m) + \
			  (1-beta)*len(get_overlapping_nodes(nei1, nei2)) / len(get_merging_nodes(nei1, nei2))
	return cod

def compare_communities(community1_nodes, community2_nodes):
	len1 = len(community1_nodes)
	len2 = len(community2_nodes)
	i = 0
	if len1 != len2:
		return False

	while i < len1:
		if community1_nodes[i] != community2_nodes[i]:
			return False
		i = i + 1
	return True

def get_degree_max(nodes):
	max= -1
	node  = -1
	degree_dict = C.degree()
	for x in nodes:
		if degree_dict[x] > max:
			max = degree_dict[x]
			node = x
	return node

def get_overlapping_nodes(community1_nodes, community2_nodes):
	return [x for x in community1_nodes if x in community2_nodes]
#
#	overlapping_nodes=[]
#	for x in community1_nodes:
#		if x in community2_nodes:
#			overlapping_nodes.append(x)
#	return overlapping_nodes

def get_merging_nodes(community1_nodes, community2_nodes):
#	return list(set(community1_nodes + community2_nodes))
	result=community1_nodes
	for x in community2_nodes:
		if x not in community1_nodes:
			result.append(x)
	return result

#def is_sub_graph(graph1, graph2):
#	len1 = len(graph1.nodes())
#	len2 = len(graph2.nodes())
#	set1 = set(graph1.nodes())
#	set2 = set(graph2.nodes())
#	min_graph = nx.Graph()
#	if len1 >= len2:
#		if set2.issubset(set1) == True:
#			min_graph = graph2
#		return (set2.issubset(set1), min_graph)
#	else:
#		if set1.issubset(set2) == True:
#			min_graph = graph1
#		return (set1.issubset(set2), min_graph)

def merge_communities(community1, community2):
	community_new = nx.Graph(C.subgraph((community1.nodes() + community2.nodes())))
	out_list = ["merge:",str(community_new.nodes()),'\n']
	f.writelines(out_list)
	return community_new

#
#def get_all_cod(communities):
#	#计算社区中两两社区的社区重叠度,,未用
#	cod = []
#	for x in communities:
#		def inner_get_cod(y):
#			return get_communities_overlapping_degree(x, y)
#		cod.append(map(inner_get_cod, communities))
#	return cod

def merge_all_communities(communities):
	le = len(communities)
	communities_iter = communities
	bm = [0]*le
	result = []
	for i in range(le):
		for j in range(i+1, le):
			x = communities[i]
			y = communities[j]

			out_list = [str(communities_iter.index(x)), str(x.nodes()), '\n']
			f.writelines(out_list)
			out_list = [str(communities_iter.index(y)), str(y.nodes()), '\n']
			f.writelines(out_list)
			cod = get_communities_overlapping_degree(x, y)
			out_list = ["cod:", str(cod)]
			f.writelines(out_list)
			def is_subset(a,b):
				if len(a)>len(b):
					return False
				for x in a:
					if x not in b:
						return False
				return True

			if cod > gama:
				if is_subset(y,x):
					bm[j]=1
					break
				elif is_subset(x,y):
					bm[i] = 1
					break
				else: #other
					merge_graph = merge_communities(x, y)
					bm[i] = 1
					bm[j] = 1
					result.append(merge_graph)
					break

	for x in range(len(bm)-1, -1, -1):
		if bm[x]:
			communities.pop(x)
	for x in result:
		communities.append(x)

	if len(communities) != le:
		return merge_all_communities(communities)
	else:
		return communities

def main():
	import sys
#	print "syaargv0 is", sys.argv[0]
#	sys.exit(0)
	global alpha,beta,gama,avg_type

	if len(sys.argv) > 2:
		avg_type=int(sys.argv[1])

# read network dataset as graph C

	#nx.draw(C)
	#plt.savefig("karate_club_graph.png")
	# init
	# communities = []
	communities = get_all_nature_community(C)
	#i = 0
	#while i < len(communities):
	#	print "i = ", i
	#	print communities[i].nodes()
	#	i = i+1
	f.write("++++++++++++++++++++++++++++++\n")
	out_list = [str(communities[i].nodes()) for i in range(len(communities))]
	f.writelines(out_list)
	f.write("++++++++++++++++++++++++++++++end\n")

	# 合并
	results = merge_all_communities(communities)

	print "----------------------------------The detection result is: \n"
	print "all communities: "
	i = 1
	for x in communities:
		print "i = ", i, ":" , sorted(x.nodes())
		i += 1

	fr.write("----------------------------------The detection result is: \n")
	out_list = [str(sorted(results[i].nodes())) for i in range(len(results))]
	for item in out_list:
		fr.write(item)
		fr.write("\n")
	fr.write("----------------------------------end\n")

	overlapping_nodes = set([])
	fr.write("overlapping nodes are: ------------\n")
	communities = [set(x) for x in communities]
	for x in communities:
		for y in communities[communities.index(x)+1:]:
			temp = x.intersection(y)
			overlapping_nodes = overlapping_nodes.union(temp)
	print "overlapping nodes are: ", sorted(list(overlapping_nodes))
	fr.writelines(str(list(overlapping_nodes)))
	fr.write("----------------------------------end\n")
	f.close()
	fr.close()

	for x in results:
		nx.draw(x, node_color = (random(), random(), random()))
	#nx.draw(nx.Graph(C.subgraph(overlapping_nodes)), node_color = "r")
	plt.savefig("CD_output.png")

if __name__ == '__main__':
	import time
	start = time.time()
#	import profile
#	profile.run("main()",sort=1)
	main()

	print "total time:", time.time() - start
	f.close()
	fr.close()
#
	#import pstats
	#p = pstats.Stats('./pro_out')
	#p.sort_stats("time").print_stats()
