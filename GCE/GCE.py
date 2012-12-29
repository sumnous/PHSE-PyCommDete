__author__ = 'wangting'

import networkx as nx
from PyCommDete import *
from config import *
from inputs.formal_edgelist import *

dis_threshold = 0.25 #small than dis_threshold, then delete this community
communities = [[1,2,3,4,5],[2,3,4,5,6],[2,3,4,5,6,7]]

def find_maximum_clique_GCE(network):
    # find the maximum cliques in network C, clique's nodes are over 4.
    # http://networkx.lanl.gov/reference/algorithms.clique.html
    cl = [x for x in nx.find_cliques(network)]
    seeds = filter(lambda x:len(x)>=4, cl)
    print "seeds:\n", seeds
    print "number of seeds for computing: ", len(seeds)
    return seeds

def get_all_nature_community_GCE(cliques):
    pool_result = []

    from config import process_num
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
    print "comm1_len: ", len(comm1)
    jointed = set(comm1).intersection(set(comm2))
    print "jointed: ",len(jointed)
    print "min of comm: ", min(len(comm1),len(comm2))
    distance = 1 - float(len(jointed)) / float(min(len(comm1), len(comm2)))
    print "distance:", distance
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
    if input_type==1:
        C = nx.read_gml(filelist[file_num])
    elif input_type==2:
        C = nx.Graph(formal_edgelist(base +'/benchmark_LFR_OC_UU/network.dat'))
        # get true.dat
        f = file(base +'/benchmark_LFR_OC_UU/community.dat', 'r')
        fw = file(base +'/evaluations/mutual3/true.dat','w+')
        d={}
        for line in f:
            kx = line.strip().split('\t')
            kv = []
            if ' ' in kx[1]:
                kc = kx[1].strip().split(' ')
                kv.append(int(kx[0]))
                for x in kc:
                    kv.append(int(x))
            else:
                kv =[int(kx[0]), int(kx[1])]
            for kk in kv[1:]:
                if d.get(kk):
                    d[kk].append(kv[0])
                else:
                    d[kk]=[kv[0]]
        ground_truth = []
        for x in d:
            ground_truth.append(d[x])
        print "lens of ground_truth: ", len(ground_truth)
        print "ground_truth is:", ground_truth
        for line in ground_truth:
            content = " ".join([str(x) for x in line])
            fw.write(content)
            fw.write('\n')
        f.close()
        fw.close()

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