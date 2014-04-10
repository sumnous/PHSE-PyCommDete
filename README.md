PHSE (PyCommDete)
==========
This is a novel algorithm to detect overlapping communities in social networks. 

Firstly, config --> /config/*.py , create a config file named by your computer. Choose the input network (input_type) and config the other parameters.

Secondly, if you want to use LFR benchmark, go to /benchmark_LFR_OC_UU to generate the benchmark. I write a script to run my program (run.sh). 

Thirdly, detect communities in networks (SeedDrivenDete.py). I also implemente the LFM.py method and the GCE.py method.

At last, evaluate the detection results using NMI figure. --> /evaluations/mutual3/

Basiclly, the run.sh file (in /benchmark_LFR_OC_UU)can do all the detection work from generating the benchmark, detecting the communities, to evaluating the results of NMI. 
