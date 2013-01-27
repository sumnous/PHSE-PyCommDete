base="/Users/jingui/workspace/PyCommDete"

filelist=[base +'/inputs/GML/polbooks.gml',\
          base +'/inputs/GML/karate.gml',\
          base +'/inputs/GML/dolphins.gml',\
          base +'/inputs/GML/netscience.gml']

input_type = 2 #1:real gml; 2: benchmark; 3: Friendster
file_num = 1 #0:polbooks;1:karate;2:dolphins;3:netscience
seeds_type = 2 #1:degree_clique hyper ; 2: betweenness_clique hyper; 3: degree_betweenness hyper
alpha = 1.0
beta = 0.6
gama = 0.59
avg_type = 1 #0:3 1:4 2:avg 3:junfangcha  MinSeedSize for downsides_seeds()

#gce parameters
dis_threshold = 0.25 #small than dis_threshold, then delete this community
cch_threshold = 0.25 #similarity more than 1-cch_threshold in at least 2 already accepted seeds, then delete this clique
# #clique coverage heuristic
delta_threshold = 0.6

process_num=32
thread_num=4

