from PyCommDete import *

from inputs.formal_edgelist import *
from common.input_process import *
#from multiprocessing import Pool
#import numpy as np

from graph import Graph
from node import Node
import logging


def get_all_nodes_by_degree(netw, d_threshold=0, min_distance=1):
    nd = netw.degree()
    node_degree = [(node, nd[node]) for node in nd if nd[node] > d_threshold]
    node_degree.sort(key=lambda x: x[1], reverse=True)
    btmap = [0] * len(nd)
    for nd in node_degree:
        btmap[nd[0] - 1] = nd[0]

    def mark_zero(node_lst, deep):
        if deep > 0:
            for i in node_lst:
                if btmap[i - 1]:
                    nei = netw.neighbors(i)
                    nei = [n for n in nei if btmap[n - 1]]
                    for x in nei:
                        btmap[x - 1] = 0

                    nei_nei = [netw.neighbors(n).remove(i) for n in nei if btmap[n - 1]]
                    map(lambda x: mark_zero(x, deep - 1), nei_nei)

    mark_zero([nd[0] for nd in node_degree], min_distance)

    return [node[0] for node in node_degree if btmap[node[0] - 1]]


def get_all_nodes(netw, seeds_type):
    if seeds_type == 1:
        orig = C.degree()
    elif seeds_type == 2:
        orig = nx.betweenness_centrality(netw)
    elif seeds_type == 3:
        betw = nx.betweenness_centrality(netw)
        degr = netw.degree()
        nodes = netw.nodes()
        betw = sorted(betw.iteritems(), key=lambda x: x[1], reverse=True)
        bitmap = [0] * len(betw)
        betw_ex_nei = [x[0] for x in betw]
        print "len of betw_ex_nei:", len(betw_ex_nei)
        for x in betw_ex_nei:
            bitmap[x - 1] = x
        recover = []
        for x in betw_ex_nei:
            if bitmap[x - 1] > 0:
                recover.append(x)
                nei = C.neighbors(x)
                for n in nei:
                    bitmap[n - 1] = 0
        for x in recover:
            bitmap[x - 1] = x
        seed_betw = [node for node in nodes if bitmap[node - 1]]
        print "len of betw:", len(seed_betw)
        print "seed_betw:", seed_betw

        degr = sorted(degr.iteritems(), key=lambda x: x[1], reverse=True)
        bitmap = [0] * len(degr)
        degr_ex_nei = [x[0] for x in degr]
        print "len of degr_ex_nei:", len(degr_ex_nei)
        for x in degr_ex_nei:
            bitmap[x - 1] = x
        recover = []
        for x in degr_ex_nei:
            if bitmap[x - 1] > 0:
                recover.append(x)
                nei = C.neighbors(x)
                for n in nei:
                    bitmap[n - 1] = 0
        for x in recover:
            bitmap[x - 1] = x
        seed_degr = [node for node in nodes if bitmap[node - 1]]
        print "len of degr:", len(seed_degr)
        print "seed_degr", seed_degr

        seed_cross = list(set(seed_betw).intersection(set(seed_degr)))
        print "len of seed_cross:", len(seed_cross)
        print "seed_cross:", seed_cross
        return seed_cross
    nodes = netw.nodes()
    orig = sorted(orig.iteritems(), key=lambda x: x[1], reverse=True)
    bitmap = [0] * len(orig)
    average = sum(x[1] for x in orig) / len(orig)
    orig = [x for x in orig if x[1] >= average]
    orig_over_ave = [x[0] for x in orig]
    for x in orig_over_ave:
        bitmap[x - 1] = x
    recover = []
    for x in orig_over_ave:
        if bitmap[x - 1] > 0:
            recover.append(x)
            nei = C.neighbors(x)
            for n in nei:
                bitmap[n - 1] = 0
    for x in recover:
        bitmap[x - 1] = x
    seed = [node for node in nodes if bitmap[node - 1]]
    return seed


def get_cliques(n):
    """
    type(n) is Node
    """
    if not isinstance(n, Node):
        logging.error("node type error")

    subgraph = n.get_neighbors_id()
    subgraph.append(n.node_id)

    g = Graph(nodes=subgraph)
    print len(g)
    g.find_max_cliques(include_node_id = n.node_id)
    exit()

#    keep use networkx
    g = nx.Graph(nx.subgraph(subgraph))
    cliques = nx.find_cliques(g)
    print "done"
    exit()

    re = []
    for cli in cliques:
        if n.node_id in cli and len(cli) > len(re):
            re = cli
    return re


def get_all_cliques_by_nodes(nodes):
    return map(lambda x: get_cliques(x), nodes)


if __name__ == "__main__":
    logging.basicConfig( level=logging.DEBUG)

    import time

    start = time.time()

    netw = Graph(default=True)
    nodes = netw.get_nodes()
    logging.debug("len of graph nodes: " + str(len(nodes)))

    cliques = get_all_cliques_by_nodes(nodes)
    logging.info(cliques)

    print "len of cliques: ", len(cliques)
    exit()
    seeds = downsides_seeds(cliques)
    print "downsides after:", seeds
    print "number of downsided seeds:", len(seeds)
    seeds = deal_seeds_GCE_inSDD(seeds)

    print "length of seeds: ", len(seeds)
    print "seeds: ", seeds
    #anlysis the cliques's fitness
    seeds_fitness = map(lambda x: get_fitness(x), [nx.Graph(C.subgraph(seed)) for seed in seeds])
    print "seeds_fitness", seeds_fitness
    seedsort = {}
    for i in range(len(seeds)):
        seedsort[i] = seeds_fitness[i]
    after = sorted(seedsort.items(), key=lambda x: x[1], reverse=True)
    print "after sort list of tuple:", after
    seeds_sorted = []
    for x in after:
        seeds_sorted.append(seeds[x[0]])
    print "seeds_sorted", seeds_sorted
    #	seeds_deal = deal_cliques(seeds_sorted)
    #	print "seeds_deal", seeds_deal

    communities = get_all_nature_community(seeds_sorted)
    print "commplete get_all_nature_community"
    results = merge_all_communities(communities)

    f = file(base + '/evaluations/mutual3/result.dat', 'w+')
    for line in results:
        content = " ".join([str(x) for x in line])
        f.write(content)
        f.write('\n')
    f.close()

    # write results in file for evaluating
    #	import pickle
    #	pickle.dump(results, f)


    print "----------------------------------The detection result is: \n"
    print "all communities: "
    i = 1
    for x in results:
        print "i = ", i, ":", sorted(x.nodes())
        i += 1
    overlapping_nodes = set([])
    commu = [set(x) for x in results]
    for x in commu:
        for y in commu[commu.index(x) + 1:]:
            temp = x.intersection(y)
            overlapping_nodes = overlapping_nodes.union(temp)
    print "overlapping nodes are: ", sorted(list(overlapping_nodes)), "\n NOO is: ", len(overlapping_nodes)

    end = time.time() - start
    print "total time is: ", end
