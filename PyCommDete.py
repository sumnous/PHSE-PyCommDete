# -*- coding: utf8 -*-
from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
from math import pow
from random import random
from inputs.formal_edgelist import formal_edgelist

from Queue import Queue
from threading import Thread
from multiprocessing import *

#import numpy, matplotlib
#from scipy.cluster import hierarchy
#from scipy.spatial import distance

f = file('./interdata', 'w+')
fr = file('./result', 'w+')
#C = nx.read_gml('./inputs/GML/polbooks.gml')
#C = nx.read_gml('./inputs/GML/karate.gml')
#C = nx.read_gml('./inputs/GML/dolphins.gml')
C = nx.Graph(formal_edgelist('./benchmarks/benchmark_2_2/network.dat'))

correct = float(-0.01)
alpha = 1.0
beta = 0.6
gama = 0.6
NodeMaxValue=max(C.nodes())+1
MinSeedSize = 5

class ThreadGetNature(Thread):
	def __init__(self, queue, result):
		Thread.__init__(self)
		self.queue = queue
		self.result = result
	def run(self):
#		while self.queue.qsize():
		clique = self.queue.get()
		print self.queue.qsize()
		Graph = nx.Graph(C.subgraph(clique))
		self.result.append(get_nature_community(Graph))
		self.queue.task_done()

class ThreadGetFitness(Thread):
	def __init__(self, queue, result, G_nodes):
		Thread.__init__(self)
		self.queue = queue
		self.result = result
		self.G_nodes = G_nodes
	def run(self):
#		while self.queue.qsize():
		x = self.queue.get()
		val = get_fitness(nx.Graph(C.subgraph((self.G_nodes+[x]))))
		self.result.append([val, x])
		self.queue.task_done()

def get_maximum_cliques(network):
	# find the maximum cliques in network C, clique's nodes are over 2.
	# http://networkx.lanl.gov/reference/algorithms.clique.html
	cl = [x for x in nx.find_cliques(network)]
	cl_over_2 = [set(m) for m in cl if len(m) > 2]

	seeds = deal_cliques(cl_over_2)
	count_len = []
	for x in seeds:
		count_len.append(len(x))
	MinSeedSize = sum(count_len)/len(seeds)
	print "MinSeedSize: ", MinSeedSize
	seeds = [x for x in seeds if len(x) >= MinSeedSize]
#	seeds = seeds[:10]
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
	# sort the list of lists based on the length of the list
	cliques.sort(key=lambda x:len(x), reverse=True)
	# merge the cliques if they are shared n-1 nodes
	result=[]
	le = len(cliques)
	if le == 0:
		return result
	elif le == 1:
		return list(cliques[0])

	current=[]
	bitmap=[0]*len(cliques)
	btlen = len(bitmap)
	while sum(bitmap) < btlen:
		for i in range(btlen):
			if not bitmap[i]:
				current.append(i)
				bitmap[i] = 1
				break

		remain=[x for x in range(btlen) if bitmap[x]==0]

		def c_match(current_list, c):
			for i in current_list:
				if len(cliques[c].intersection(cliques[i])) == len(cliques[i])-1 \
				and len(cliques[c]) ==  len(cliques[i]):
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

#
#	current = cliques[0]
#	current_len = len(current)
#	i=1
#	cliques_len = len(cliques)
#	while i < cliques_len:
#		if len(current.intersection(cliques[i])) == current_len-1 and len(cliques[i]) == current_len:
#			current = current.union(cliques[i])
#		else:
#			result.append(set(current))
#			current = cliques[i]
#			current_len = len(current)
#		i = i+1
#	result.append(set(current))
#	result = [sorted(m) for m in result]
#	result.sort(key=lambda x:len(x), reverse=True)
	return result

def get_neighbors(Graph):
	"""find subgraph's(or graph, type is Graph) neighbor nodes in original graph C"""
	G_neighbors = [0]*NodeMaxValue
	def mark_true(x):
		t = C.neighbors(x)
		for x in t:
			G_neighbors[x] = 1
	map(mark_true, Graph.nodes())

	for x in Graph.nodes():
		G_neighbors[x]=0
	result=[x for x in range(len(G_neighbors)) if G_neighbors[x]]

	return result

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
	vertex_list = [] # 添加一个初始值,将最大贡献度所对应的一些节点一起加入社区
	if G_neighbors == []:
		pass
	else:
		G_nodes = Graph.nodes()
		result=[]
		for x in G_neighbors:
			val = get_fitness(nx.Graph(C.subgraph((G_nodes+[x]))))
			result.append([val, x])
#
#		queue = Queue()
#		for x in G_neighbors:
#			queue.put(x)
#		result=[]
#		for x in range(len(G_neighbors)):
#			t = ThreadGetFitness(queue, result, G_nodes)
#			t.start()
#		queue.join()

#		print "len of G_neighbors:", len(G_neighbors)
#		print "len of result is :",len(result)
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

def get_all_nature_community(network):
	cliques = get_maximum_cliques(network)
	all_nodes = network.nodes()
	def process_f(cli):
		Graph = nx.Graph(C.subgraph(cli))
		return get_nature_community(Graph)
	communities = map(process_f, cliques)

	comm_nodes = []
	for x in communities:
		comm_nodes = comm_nodes + x.nodes()
	left_list = [x for x in all_nodes if x not in comm_nodes]

	single_node_Graph = nx.Graph()
	while len(left_list)>0:
		seed_node = get_degree_max(left_list)
		print "seed_node",seed_node
		single_node_Graph.add_node(seed_node)
		single_node_Graph = get_nature_community(single_node_Graph)
		communities.append(single_node_Graph)
		s_nodes = single_node_Graph.nodes()
		for x in s_nodes:
			if x in left_list:
				left_list.remove(x)
		single_node_Graph.clear()

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
			if len(x)<= len(item):
				continue
			else:
				if set(item).issubset(set(x.nodes())):
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
		COD = len(val_o) / len(val_m)
	else:
		COD = beta*len(val_o) / len(val_m) + \
		      (1-beta)*len(get_overlapping_nodes(nei1, nei2)) / len(get_merging_nodes(nei1, nei2))
	return COD

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
	return x

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

def is_sub_graph(graph1, graph2):
	len1 = len(graph1.nodes())
	len2 = len(graph2.nodes())
	set1 = set(graph1.nodes())
	set2 = set(graph2.nodes())
	min_graph = nx.Graph()
	if len1 >= len2:
		if set2.issubset(set1) == True:
			min_graph = graph2
		return (set2.issubset(set1), min_graph)
	else:
		if set1.issubset(set2) == True:
			min_graph = graph1
		return (set1.issubset(set2), min_graph)

def merge_communities(community1, community2):
	community_new = nx.Graph(C.subgraph((community1.nodes() + community2.nodes())))
	out_list = ["merge:",str(community_new.nodes()),'\n']
	f.writelines(out_list)
	return community_new

def get_all_COD(communities):
	#计算社区中两两社区的社区重叠度,,未用
	COD = []
	for x in communities:
		for y in communities[(communities.index(x)+1):]:
			cod = get_communities_overlapping_degree(x, y)
			COD.append([cod, x, y])
	return COD

def merge_all_communities(communities):####TODO  pop y可以,pop x会多pop出去  我觉得应该把cod的判断放在外边
	# 遍历一遍
	le = len(communities)
	communities_end = []
	communities_iter = communities
#	flag = -1
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
	return communities


def main():
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
	print "overlapping nodes are: ", list(overlapping_nodes)
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
	main()
	print "total time:", time.time() - start
	f.close()
	fr.close()
#	import profile
#	profile.run("main()")
	#import pstats
	#p = pstats.Stats('./pro_out')
	#p.sort_stats("time").print_stats()
