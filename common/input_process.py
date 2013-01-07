__author__ = 'wangting'

import networkx as nx
from inputs.formal_edgelist import  *


def input_type_fun(input_type):
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
    elif input_type==3:
        from inputs.friendster_dataset.friendster_graph import get_friendster_graph
#        C = nx.Graph()
        C = get_friendster_graph()

        print len(C)
    return C