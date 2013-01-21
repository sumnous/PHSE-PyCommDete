# -*- coding: utf8 -*-
from __future__ import division

import logging
from common.transform import split_list
from multiprocessing import Pool
#from inputs.formal_edgelist import *
from config import config

from graph import Graph
from graph import get_graph_nodes_len
from graph import get_neighbors_id


logging.basicConfig( level=logging.DEBUG)
GRAPH_LEN = get_graph_nodes_len()
MAX_LEN = GRAPH_LEN
if MAX_LEN >= 1000:
    MAX_LEN = MAX_LEN * 0.1
#
dgraph = Graph(default=True)

##used in PyCommDete main
def get_maximum_cliques(network):
    # find the maximum cliques in network dgraph, clique's nodes are over 2.
    # http://networkx.lanl.gov/reference/algorithms.clique.html
    cl = [x for x in nx.find_cliques(network)]

    cl_over_2 = filter(lambda x: len(x) > 2, cl)
    print "_________len", len(cl_over_2)
    #	seeds = deal_cliques(cl_over_2)
    seeds = cl_over_2
    print ":::::::::::", seeds

    seeds = downsides_seeds(seeds)

    print "seeds:\n", seeds
    print "number of seeds for computing: ", len(seeds)
    return seeds


def downsides_seeds(seeds, avg_type=1):
    count_len = [len(x) for x in seeds]
    if avg_type == 0:
        MinSeedSize = 3
    elif avg_type == 1:
        MinSeedSize = 4
    elif avg_type == 2:
        MinSeedSize = sum(count_len) / len(seeds)
    elif avg_type == 3:
        logging.debug("len of seeds" + str(len(seeds)))
        ave = sum(count_len) / len(seeds)
        sum_tem = sum(map(lambda x: pow((ave - x), 2), count_len))
        MinSeedSize = ave - pow(sum_tem / len(seeds), 0.5)
    #    cliques.sort(key=lambda x:len(x), reverse=True)
    seeds = [x for x in seeds if len(x) >= MinSeedSize]
    seeds.sort(key=lambda x: len(x), reverse=True)
    return seeds


def deal_cliques(cliques):
    new_cliques = deal_cliques_once(cliques)
    while new_cliques != cliques:
        cliques = new_cliques
        new_cliques = deal_cliques_once(cliques)
    return new_cliques


def deal_cliques_once(cliques):
    """return a list containing cliques"""

    le = len(cliques)
    if le == 0:
        return []
    if le == 1:
        return list(cliques[0])

    # sort the list of lists based on the length of the list
    cliques.sort(key=lambda x: len(x), reverse=True)
    # merge the cliques if they are shared n-1 nodes
    result = []
    current = []
    le = len(cliques)
    bitmap = [0] * le

    while sum(bitmap) < le:
        for i, e in enumerate(bitmap):
            if e == 0:
                current.append(i)
                bitmap[i] = 1
                break

        remain = [i for i, e in enumerate(bitmap) if e == 0]

        def c_match(current_list, c):
            x = set(cliques[c])
            for i in current_list:
                y = set(cliques[i])
                if len(x) == len(y) and len(x.intersection(y)) == len(y) - 1:
                    return True
            return False

        for c in remain:
            if c_match(current, c):
                current.append(c)
                bitmap[c] = 1
        tmp = set()
        for x in current:
            tmp = tmp.union(cliques[x])
        result.append(tmp)
        current = []
    return result


#def get_neighbors(Graph):
#    """find subgraph's(or graph, type is Graph) neighbor nodes in original graph dgraph"""
#    flag = {}
#
#    def mark_true(x):
#        t = dgraph.neighbors(x)
#        for x in t:
#            flag[x] = 1
#
#    map(mark_true, Graph.get_nodes())
#    for x in Graph.nodes():
#        flag[x] = 0
#
#    return [x for x in nodes_C if flag.get(x)]


##done
def get_fitness(g):
    """
    type(g) is Graph
    compute the fitness of the graph
    """
    if len(g.nodes_id) <= 1:
        return float(0)

    neighbor_g = Graph(nodes=g.get_neighbors_with_self())
    kin = g.get_edges_num()
    kout = neighbor_g.get_edges_num() - kin
    logging.debug("len of pow((2 * kin + kout), config.alpha)" + str(pow((2 * kin + kout), config.alpha)))
    return  (2 * kin) / pow((2 * kin + kout), config.alpha)

#def get_fitness_v_max(Graph):
#	"""这有个问题，如果最大贡献度所对应的节点有多个怎么处理，是添加第一个最大的节点，还是所有的都添加
#	compute the fitness_v(dic, {node, fitness of adding vertex}), find fitness_v_max"""
#	G_neighbors = get_neighbors(Graph)
#	v_max_node=[[], float(-100)]
#	G_nodes = Graph.nodes()
#	#	vertex_list = [] # 添加一个初始值,将最大贡献度所对应的一些节点一起加入社区
#	if G_neighbors != []:
#		result = map(lambda x:[get_fitness(nx.Graph(dgraph.subgraph((G_nodes+[x])))), x], G_neighbors)
#
#		result.sort(key=lambda x:x[0], reverse=True)
#		max_value = result[0][0]
#		nodelist = [x[1] for x in result if x[0]>=max_value]
#		v_max_node = [nodelist, max_value]
#
#	return v_max_node
#
#def get_fitness_v_community(Graph):
#	"""节点对社区的贡献度"""
#	r = get_fitness_v_max(Graph)
#	fitness_v_max_value = r[1]  #return (node_list, max_value)
#	fitness_v_community_value = fitness_v_max_value - get_fitness(Graph)
#	return (r[0], fitness_v_community_value)


## done
def get_nature_community_short(cli_list):
    if len(cli_list) >= MAX_LEN:
        return dgraph

    #    TODO change cli_list to list type
    g = Graph(nodes=list(cli_list))
    g_fitness = get_fitness(g)
    g_nodes = g.get_nodes() #nodes id list
    nei = g.get_neighbors() # neighbors id list
    if len(nei) == 0:
        return g

    # each node in nei, get its neighbors, return as set
#    TODO v_nei is possible == 0
    v_nei = [set(x) for x in filter(lambda x:len(x) > 0, map(get_neighbors_id, nei))]

    def get_connection(x):
        return set(g_nodes).intersection(x)

    #TODO confirm!
    v_con = map(get_connection, v_nei)
    v_all = []
#    change nei to v_nei
    for i in range(len(v_nei)):
        logging.debug("len of v_nei" + str(len(v_nei[i])))
        temp = [nei[i], len(v_nei[i]), len(v_con[i]), float(len(v_con[i]) / len(v_nei[i]))]
        v_all.append(temp)

    v_nei_max = 0
    v_con_max = 0
    v_con_nei_max = 0
    v_max = -1
    fitness_max = 0
    for v in v_all:
        if v[3] > v_con_nei_max:
            if v[1] > v_nei_max and v[2] > v_con_max:
                vg = Graph(nodes=g_nodes + [v[0]])
                #                vg =  nx.Graph(dgraph.subgraph(g_nodes + [v[0]]))
                incr_fitness = get_fitness(vg) - g_fitness
                if incr_fitness > 0 and incr_fitness > fitness_max:
                    v_max = v[0]
                    fitness_max = incr_fitness
                    v_nei_max = v[1]
                    v_con_max = v[2]
                    v_con_nei_max = v[3]
            else:
                v_nei_max = v[1]
                v_con_max = v[2]
                v_con_nei_max = v[3]
                v_max = v[0]

    if v_max > 0:
    #        new_graph = nx.Graph(dgraph.subgraph(g_nodes+[v_max]))
    #        return get_nature_community_short(new_graph)
        return get_nature_community_short(g_nodes + [v_max])
    else:
        return cli_list


def get_nature_community(Graph):
    if len(Graph) > MAX_LEN:
        return dgraph
    g_fitness = get_fitness(Graph)
    g_nodes = Graph.nodes()

    v_fitness = []
    nei = get_neighbors(Graph)

    if len(nei) == 0:
        return Graph

    for v in nei:
        vg = nx.Graph(dgraph.subgraph(g_nodes + [v]))
        incr_fitness = get_fitness(vg) - g_fitness

        if incr_fitness > 0:
            v_fitness.append([v, incr_fitness])

    if len(v_fitness) > 0:
        v_fitness.sort(key=lambda x: x[1], reverse=True)
        extends_list = [x[0] for x in v_fitness if x[1] >= v_fitness[0][1]]
        #		extends_list = [v_fitness[0][0]]
        if len(extends_list) > 0:
            new_graph = nx.Graph(dgraph.subgraph(g_nodes + extends_list))
            return get_nature_community(new_graph)
        else:
            return Graph
    else:
        return Graph

## done
def process_clique_list(cli_list):
    """
    type(cli_list) is list
    type(cli_list[0]) is set
    """
    r = map(get_nature_community_short, cli_list)
    #	print "origin len is", len(r)
    return filter(lambda x: len(x) < GRAPH_LEN, r)
#	print "filter len is", len(nr)

def get_all_nature_community(cliques):
    process_num = int(config.process_num)
    pool_result = []

    if len(cliques) < process_num:
        process_num = len(cliques)

    pool = Pool(process_num)
    #	cli_len = len(cliques)

    group_list = split_list(cliques, process_num)

    for i in range(1, len(group_list), 2):
        group_list[i].reverse()

    for i in range(process_num):
        args = []
        for gr in group_list:
            if len(gr) > i:
                args.append(gr[i])
        args = (args,)
        #		args=([cliques[j] for j in range(cli_len) if j%process_num==i],)
        print "args__________", args
        pool_result.append(pool.apply_async(process_clique_list, args))

    pool.close()
    pool.join()

    communities = []
    for x in pool_result:
        communities = communities + x.get()
    print "finish process___________________"
    all_nodes = dgraph.get_nodes()
    comm_nodes = {}

    print type(communities)
    print type(communities[0]), len(communities[0])

    for x in communities:
        for n in x:
            comm_nodes[n] = 1
    left_list = [x for x in all_nodes if x not in comm_nodes]

    while len(left_list) > 0:
        single_seed_communities = get_single_seed_nature_community_once(left_list)
        communities = communities + single_seed_communities
        for comm in communities:
            for x in comm:
                if x in left_list:
                    left_list.remove(x)

    i = 0
    for x in communities:
        print "i = ", i, x
        i = i + 1

    print "finish get all communities"
    communities = deal_communities(communities)
    print "complete deal_communities"
    return communities


def get_single_seed_nature_community_once(nodes):
    process_num = config.process_num
    if len(nodes) >= process_num:
        tem_list = get_betweenness_max_num(nodes, process_num)
    else:
        tem_list = get_betweenness_max_num(nodes, len(nodes))

    from SeedDrivenDete import get_all_cliques_by_nodes

    cliques = get_all_cliques_by_nodes(dgraph, tem_list)

    pool_result = []
    if len(cliques) < process_num:
        process_num = len(cliques)
    pool = Pool(process_num)
    #    cli_len = len(cliques)
    group_list = split_list(cliques, process_num)

    for i in range(1, len(group_list), 2):
        group_list[i].reverse()

    for i in range(process_num):
        args = []
        for gr in group_list:
            if len(gr) > i:
                args.append(gr[i])
        args = (args,)
        #		args=([cliques[j] for j in range(cli_len) if j%process_num==i],)
        print "args__________", args
        pool_result.append(pool.apply_async(process_clique_list, args))

    pool.close()
    pool.join()

    communities = []
    for x in pool_result:
        communities = communities + x.get()
    print "finish single seed process___________________"

    return communities


def deal_communities(communities):
    # if there are some communities are the same, than delete
    le = len(communities)

    bm = [0] * le
    for i in range(le):
        if not bm[i]:
            for j in range(i + 1, le):
                if compare_communities(communities[i], communities[j]):
                    bm[j] = 1

    for i in range(le - 1, -1, -1):
        if bm[i] or len(communities[i]) == GRAPH_LEN:
            communities.pop(i)

    # is_sub_graph
    def to_be_del(item, com):
        for x in com:
            if len(x) > len(item) and set(item).issubset(set(x)):
                return True
        return False

    bitmap = [0] * len(communities)
    for i in range(len(communities)):
        if to_be_del(communities[i], communities):
            bitmap[i] = 1
    for i in range(len(bitmap) - 1, -1, -1):
        if bitmap[i]:
            communities.pop(i)
    return communities


def get_communities_overlapping_degree(community1, community2):
    nei1 = get_neighbors(community1)
    nei2 = get_neighbors(community2)
    val_o = get_overlapping_nodes(community1.nodes(), community2.nodes())
    val_m = get_merging_nodes(community1.nodes(), community2.nodes())

    logging.debug("len of val_m" + str(val_m))
    if len(nei1) == 0 and len(nei2) == 0:
        cod = len(val_o) / len(val_m)
    else:
        logging.debug("len of  len(get_merging_nodes(nei1, nei2))" + str(len(get_merging_nodes(nei1, nei2))))
        cod = beta * len(val_o) / len(val_m) +\
              (1 - beta) * len(get_overlapping_nodes(nei1, nei2)) / len(get_merging_nodes(nei1, nei2))
    return cod


def compare_communities(community1_nodes, community2_nodes):
    len1 = len(community1_nodes)
    len2 = len(community2_nodes)

    if len1 != len2:
        return False

    i = 0
    while i < len1:
        if community1_nodes[i] != community2_nodes[i]:
            return False
        i = i + 1
    return True


def get_degree_max(nodes):
    max = -1
    node = -1
    for x in nodes:
        if degree_dict[x] > max:
            max = degree_dict[x]
            node = x
    return node


def get_degree_max_num(nodes, k):
    sorted(nodes, key=lambda x: degree_dict[x])
    print "sorted nodes by degree", nodes
    return nodes[:k]


def get_betweenness_max_num(nodes, k):
    print "left nodes numner:_______", len(nodes)
    sorted(nodes, key=lambda x: betweenness_dict[x])
    print "sorted nodes by betweenness", nodes
    return nodes[:k]


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
    result = community1_nodes
    for x in community2_nodes:
        if x not in community1_nodes:
            result.append(x)
    return result


def merge_communities(community1, community2):
    community_new = nx.Graph(dgraph.subgraph((community1.nodes() + community2.nodes())))
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
    bm = [0] * le
    result = []
    for i in range(le):
        for j in range(i + 1, le):
            x = communities[i]
            y = communities[j]

            cod = get_communities_overlapping_degree(x, y)

            def is_subset(a, b):
                if len(a) > len(b):
                    return False
                for x in a:
                    if x not in b:
                        return False
                return True

            if cod > gama:
                if is_subset(y, x):
                    bm[j] = 1
                    break
                elif is_subset(x, y):
                    bm[i] = 1
                    break
                else: #other
                    merge_graph = merge_communities(x, y)
                    bm[i] = 1
                    bm[j] = 1
                    result.append(merge_graph)
                    break

    for x in range(len(bm) - 1, -1, -1):
        if bm[x]:
            communities.pop(x)
    for x in result:
        communities.append(x)

    if len(communities) != le:
        return merge_all_communities(communities)
    else:
        return communities


def deal_seeds_GCE_inSDD(cliques):
    print cliques
    cliques.sort(key=lambda x: len(x), reverse=True)
    print "after sorted: ", cliques
    print "before num: ", len(cliques)
    len_cli = len(cliques)
    if len_cli > 2:
        results = [cliques[0], cliques[1]]
    else:
        return cliques

    def inter_perception(seed, non_seed):
        inter_nodes = set(seed).intersection(set(non_seed))
        logging.debug("non_seed len" + str(len(non_seed)))
        percent = float(len(inter_nodes)) / float(len(non_seed))
        return percent

    for i in range(2, len_cli):
        count = 0
        for j in results:
            if inter_perception(j, cliques[i]) >= 1 - config.cch_threshold:
                count += 1
            if count >= 2:
                break
        if count < 2:
            results.append(cliques[i])

    print "befor deal_cliques: ", len(results)
    results = deal_cliques(results)
    print "after deal_cliques: ", len(results)
    #results = downsides_seeds(results,2)
    #print "after downside to ave: ",len(results)

    return results


def main():
    import sys

    global alpha, beta, gama, avg_type

    if len(sys.argv) > 2:
        avg_type = int(sys.argv[1])

    # read network dataset as graph dgraph
    #nx.draw(dgraph)
    #plt.savefig("karate_club_graph.png")
    # init
    cliques = get_maximum_cliques(dgraph)
    communities = get_all_nature_community(cliques)


    # 合并
    results = merge_all_communities(communities)

    print "----------------------------------The detection result is: \n"
    print "all communities: "
    i = 1
    for x in communities:
        print "i = ", i, ":", sorted(x)
        i += 1
    overlapping_nodes = set([])

    communities = [set(x) for x in communities]
    for x in communities:
        for y in communities[communities.index(x) + 1:]:
            temp = x.intersection(y)
            overlapping_nodes = overlapping_nodes.union(temp)
    print "overlapping nodes are: ", sorted(list(overlapping_nodes))

#	for x in results:
#		nx.draw(x, node_color = (random(), random(), random()))
#	#nx.draw(nx.Graph(dgraph.subgraph(overlapping_nodes)), node_color = "r")
#	plt.savefig("CD_output.png")

#if __name__ == '__main__':
#	import time
#	start = time.time()
#	#	import profile
#	#	profile.run("main()",sort=1)
#	main()
#	print "total time:", time.time() - start
#	#
#	#import pstats
#	#p = pstats.Stats('./pro_out')
#	#p.sort_stats("time").print_stats()

