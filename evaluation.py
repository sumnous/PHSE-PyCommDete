#!/usr/bin/env python
# -*- coding: utf8 -*-

import numpy
from numpy import *
from scipy import *
from common.clustering import Cover
from common.clustering import compare_communities


#Mutual information
def mutual_info(x,y):
	print "x",x
	N=double(x.size)
	I=0.0
	eps = numpy.finfo(float).eps
	for l1 in unique(x):
		for l2 in unique(y):
			#Find the intersections
			l1_ids=nonzero(x==l1)[0]
			l2_ids=nonzero(y==l2)[0]
			pxy=(double(intersect1d(l1_ids,l2_ids).size)/N)+eps
			I+=pxy*log2(pxy/((l1_ids.size/N)*(l2_ids.size/N)))
	return I

#Normalized mutual information
def nmi(x,y):
    N=x.size
    I=mutual_info(x,y)
    Hx=0
    for l1 in unique(x):
        l1_count=nonzero(x==l1)[0].size
        Hx+=-(double(l1_count)/N)*log2(double(l1_count)/N)
    Hy=0
    for l2 in unique(y):
        l2_count=nonzero(y==l2)[0].size
        Hy+=-(double(l2_count)/N)*log2(double(l2_count)/N)
    return I/((Hx+Hy)/2)

def data_formal(communities):
	####TODO
	k = len(communities)
	
	return array


if __name__=="__main__":
    #Example from http://nlp.stanford.edu/IR-book
    #/html/htmledition/evaluation-of-clustering-1.html
    Ground_truth = array(Cover([[0,1,2,3,4,5,6,7,10,11,12,13,16,17,19,21], \
							[8,9,14,15,18,20,22,23,24,25,26,27,28,29,30,31,32,33]]))
    Result = array(Cover([[32, 33, 8, 9, 14, 15, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31], \
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 19, 21, 28, 30]]))
    print compare_communities(Ground_truth, Result, method="nmi", remove_none=False)
    print "G", Ground_truth
    print "R", Result
    print "nmi", nmi(Ground_truth, Result)
    #print nmi(array([1,1,1,1,1,1,1,1,3,3,1,1,1,1,2,2,1,1,2,3,2,1,2,2,2,2,2,2,3,2,3,2,2,2])
     #         ,array([1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,2,1,2,1,2,2,2,2,2,2,2,2,2,2,2]))
    #print nmi(array([1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3])
    #          ,array([1,2,1,1,1,1,1,2,2,2,2,3,1,1,3,3,3]))
              
              
           
