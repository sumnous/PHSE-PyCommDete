__author__ = 'wangting'

from PyCommDete import *
from socket import gethostname

hn=gethostname()
exec("from config.%s import *" % hn)


def pick_random_node(nodes):
    len_nodes = len(nodes)
    random_num = int(random()*len_nodes)
    random_node = nodes[random_num]
    return random_node

def get_all_nature_community_LFM(network):
    all_nodes = network.nodes()
    left_nodes_list = all_nodes
    communities = []
    while left_nodes_list != []:
        tem_node = pick_random_node(left_nodes_list)
        community = get_nature_community_short(nx.Graph(C.subgraph(tem_node)))
        communities.append(community)
        if community != network:
            for x in left_nodes_list:
                if x in community.nodes():
                    left_nodes_list.remove(x)
    return communities

if __name__ == "__main__":
    import time
    start = time.time()

    C = input_type_fun(input_type)

    #anlysis the cliques's fitness
    #    seeds_fitness = map(lambda x: get_fitness(x), [nx.Graph(C.subgraph(seed)) for seed in seeds])
    #    print "seeds_fitness",seeds_fitness
    #    seedsort = {}
    #    for i in range(len(seeds)):
    #        seedsort[i] = seeds_fitness[i]
    #    after = sorted(seedsort.items(), key = lambda x:x[1], reverse=True)
    #    print "after sort list of tuple:",after
    #    seeds_sorted = []
    #    for x in after:
    #        seeds_sorted.append(seeds[x[0]])
    #    print "seeds_sorted", seeds_sorted
    #	seeds_deal = deal_cliques(seeds_sorted)
    #	print "seeds_deal", seeds_deal

    communities = get_all_nature_community_LFM(C)
    print "commplete get_all_nature_community"
    results = deal_communities(communities)

    f = file(base +'/evaluations/mutual3/result_LFM.dat', 'w+')
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
        print "i = ", i, ":" , sorted(x.nodes())
        i += 1
    overlapping_nodes = set([])
    commu = [set(x) for x in results]
    for x in commu:
        for y in commu[commu.index(x)+1:]:
            temp = x.intersection(y)
            overlapping_nodes = overlapping_nodes.union(temp)
    print "overlapping nodes are: ", sorted(list(overlapping_nodes)), "\n NOO is: ", len(overlapping_nodes)

    end = time.time() - start
    print "total time is: ", end

