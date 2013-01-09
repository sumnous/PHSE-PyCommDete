__author__ = 'wangting'

from PyCommDete import *
from config.config import *


def pick_random_node(nodes):
    len_nodes = len(nodes)
    random_num = int(random()*len_nodes)
    random_node = nodes[random_num]
    return random_node

def get_all_nature_community_multiprocess(left_nodes_list):
    random_nodes = []

    pool_result = []
    global process_num
    if len(left_nodes_list) < process_num:
        process_num = len(left_nodes_list)

    for i in range(process_num):
        random_node = pick_random_node(left_nodes_list)
        random_nodes.append([random_node])
        left_nodes_list.remove(random_node)
    print "print random_nodes:", random_nodes

    pool = Pool(process_num)

    group_list = split_list(random_nodes, process_num)

    for i in range(1, len(group_list), 2):
        group_list[i].reverse()

    for i in range(process_num):
        args=[]
        for gr in group_list:
            if len(gr)>i:
                args.append(gr[i])
        args=(args,)
        #		args=([random_nodes[j] for j in range(process_num) if j%process_num==i],)
        print "args__________", args
        pool_result.append(pool.apply_async(process_f,args))

    pool.close()
    pool.join()

    communities=[]
    for x in pool_result:
        communities = communities+x.get()
    print "finish process_num processes get single node nature community___________________"
    return communities

def get_all_nature_community_LFM(network):
    all_nodes = network.nodes()
    left_nodes_list = all_nodes
    communities = []
    while left_nodes_list != []:
        tem_communities = get_all_nature_community_multiprocess(left_nodes_list)
        communities = communities + tem_communities
        for x in tem_communities:
            if x != network:
                for y in x.nodes():
                    if y in left_nodes_list:
                        left_nodes_list.remove(y)
        print "length of left_nodes_list__________: ", len(left_nodes_list)
    return communities

def deal_communities_LFM(communities):
    len_comm = len(communities)
    fits = map(get_fitness, communities)
    fits_dic = {}
    for x in range(len_comm):
        fits_dic[communities[x]] = fits[x]
    print "fits_dic",len(fits_dic)
    ave_fits = sum(fits)/len_comm
    result = filter(lambda x:fits_dic[x]>ave_fits, communities)
    print "above ave fitness communities", len(result), [fits_dic[x] for x in result]
    return result

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
    print "commplete get_all_nature_community, length: ",len(communities)
    communities = deal_communities(communities)
    print "after deal_communities, length:______________", len(communities)
    results = deal_communities_LFM(communities)


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

