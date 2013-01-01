__author__ = 'wangting'

import networkx as nx
from PyCommDete import *
from PyCommDete import deal_cliques
from inputs.formal_edgelist import *
from socket import gethostname

hn=gethostname()
exec("from config.%s import *" % hn)

def find_maximum_clique_GCE(network):
    # find the maximum cliques in network C, clique's nodes are over 4.
    # http://networkx.lanl.gov/reference/algorithms.clique.html
    cl = [x for x in nx.find_cliques(network)]
    cl_over_4 = filter(lambda x:len(x)>=4, cl)
    seeds = deal_seeds_GCE(cl_over_4)
    print "seeds:\n", seeds
    print "number of seeds for computing: ", len(seeds)
    return seeds

def deal_seeds_GCE(cliques):
    print cliques
    cliques.sort(key=lambda x:len(x), reverse=True)
    print "after sorted: ",cliques
    print "before num: ",len(cliques)
    len_cli = len(cliques)
    if len_cli > 2:
        results = [cliques[0],cliques[1]]
    else:
        return cliques
    def inter_perception(seed,non_seed):
        inter_nodes = set(seed).intersection(set(non_seed))
        percent = float(len(inter_nodes)) / float(len(non_seed))
        return percent

    for i in range(2,len_cli):
        count = 0
        for j in results:
            if inter_perception(j,cliques[i]) >= 1-cch_threshold:
                count += 1
            if count >= 2:
                break
        if count < 2:
            results.append(cliques[i])

    print "befor deal_cliques: ", len(results)
    results = deal_cliques(results)
    print "after deal_cliques: ",len(results)
    results = downsides_seeds(results,2)
    print "after downside to ave: ",len(results)

    return results

def get_all_nature_community_GCE(cliques):
    pool_result = []
    global process_num
    if len(cliques) < process_num:
        process_num = len(cliques)

    pool = Pool(process_num)
    cli_len = len(cliques)

    group_list = split_list(cliques, process_num)

    for i in range(1, len(group_list), 2):
        group_list[i].reverse()

    for i in range(process_num):
        args=[]
        for gr in group_list:
            if len(gr)>i:
                args.append(gr[i])
        args=(args,)
        #		args=([cliques[j] for j in range(cli_len) if j%process_num==i],)
        print "args__________", args
        pool_result.append(pool.apply_async(process_f,args))

    pool.close()
    pool.join()

    communities=[]
    for x in pool_result:
        communities = communities+x.get()
    print "finish process___________________"

    i = 0
    for x in communities:
        print "i = ",i,x.nodes()
        i = i+1
    print "finish get all communities"
    communities = deal_communities(communities)
    print "complete deal_communities"
    return communities

def distance_percent_non_embedded(comm1, comm2):
    jointed = set(comm1).intersection(set(comm2))
    distance = 1 - float(len(jointed)) / float(min(len(comm1), len(comm2)))
#    print "distance:", distance
    return distance

def deal_communities_with_distance(communities):
    le = len(communities)
    bm = [0]*le
    result = []
    for i in range(le):
        for j in range(i+1, le):
            x = communities[i]
            y = communities[j]

            dis = distance_percent_non_embedded(x, y)

            def is_subset(a,b):
                if len(a)>len(b):
                    return False
                for x in a:
                    if x not in b:
                        return False
                return True

            if dis < dis_threshold:
                if is_subset(y,x):
                    bm[j]=1
                    break
                elif is_subset(x,y):
                    bm[i] = 1
                    break
                else: #other
                    if len(x) >= len(y):
                        bm[j] = 1
                        break
                    else:
                        bm[i] = 1
                        break

    for x in range(len(bm)-1, -1, -1):
        if bm[x]:
            communities.pop(x)
    for x in result:
        communities.append(x)

    if len(communities) != le:
        return deal_communities_with_distance(communities)
    else:
        return communities

if __name__ == "__main__":
    import time
    start = time.time()

    C = input_type_fun(input_type)

    seeds = find_maximum_clique_GCE(C)
    print "length of seeds: ", len(seeds)
    print "seeds: ", seeds
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

    communities = get_all_nature_community_GCE(seeds)
    print "commplete get_all_nature_community"
    results = deal_communities_with_distance(communities)

    f = file(base +'/evaluations/mutual3/result_GCE.dat', 'w+')
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