PHSE (PyCommDete)
==========
This is a novel algorithm to detect overlapping communities in social networks. 

Firstly, config --> /config/*.py , create a config file named by your computer. Choose the input network (input_type) and config the other parameters.

Secondly, if you want to use LFR benchmark, go to /benchmark_LFR_OC_UU to generate the benchmark. I write a script to run my program (run.sh). 

Thirdly, detect communities in networks (SeedDrivenDete.py). I also implemente the LFM.py method and the GCE.py method.

At last, evaluate the detection results using NMI figure. --> /evaluations/mutual3/

Basiclly, the run.sh file (in /benchmark_LFR_OC_UU)can do all the detection work from generating the benchmark, detecting the communities, to evaluating the results of NMI. 

Paper: An Improved Parallel Hybrid Seed Expansion (PHSE) Method for Detecting Highly Overlapping Communities in Social Networks, Ting Wang, Xu Qian, Hui Xu, ADMA, 2013. 
Link: http://link.springer.com/chapter/10.1007%2F978-3-642-53914-5_33#page-1
