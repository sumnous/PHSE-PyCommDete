# -*- coding: utf8 -*-

# karate ground truth:
# [1,2,3,4,5,6,7,8,11,12,13,14,17,18,20,22],[9,10,15,16,19,21,23,24,25,26,27,28,29,30,31,32,33,34]

import numpy
from numpy import *
from scipy import *
from math import log
from get_ground_truth import *

#Mutual information
#def mutual_info(x,y):

#Confusion Matrix
def confusion_matrix(x,y):
	x_len = len(x)
	y_len = len(y)
	CMatrix = zeros([x_len, y_len], int)
	for i in range(x_len):
		for j in range(y_len):
			x_set = set(x[i])
			y_set = set(y[j])
			CMatrix[i][j] = len(x_set.intersection(y_set))
#	print "CMatrix: ",CMatrix
	return CMatrix

#Normalized mutual information
def nmi(x,y):
	N = get_num_nodes(x)

	CM = confusion_matrix(x,y)

	def get_A():
		tsum=0
		for i in range(len(CM)):
			for j in range(len(CM[0])):
				t = judge_log(CM[i][j])+log(N)-judge_log(sum(CM[i]))-judge_log(sum([x[j] for x in CM]))
				tsum += CM[i][j]*t
		return tsum*(-2)

	def get_B1():
		tsum=0
		for i in range(len(CM)):
			ci = sum(CM[i])
			tsum += ci*(judge_log(ci) - judge_log(N))
		return tsum
	def get_B2():
		tsum=0
		for j in range(len(CM[0])):
			cj = sum([x[j] for x in CM])
			tsum += cj*(judge_log(cj) - judge_log(N))
		return tsum

	return get_A()/(get_B1()+get_B2())


def get_num_nodes(list):
	d={}
	for item in list:
		for i in item:
			d[i]=1
	return len(d)

def judge_log(x):
	if x == 0:
		return 0
	else:
		return log(x)
if __name__=="__main__":
	#test 01
#	Ground_truth = [[1,2,3],[4,5,6]]
#	Result = [[1,2,3,4],[2,4,5,6]]

	#test karate nmi=0.546086186904
#	Ground_truth = [[1,2,3,4,5,6,7,8,11,12,13,14,17,18,20,22],\
#	                [9,10,15,16,19,21,23,24,25,26,27,28,29,30,31,32,33,34]]
#	Result = [[1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 17, 18, 20, 22],\
#	          [9, 10, 15, 16, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]]

	#test GN_128 nmi=0.698494780436
	Ground_truth = get_ground_truth('../benchmarks/community.dat')
	Result = get_result('../result.dat')
	print "nmi is: ", nmi(Ground_truth,Result)

#	confusion_matrix(Ground_truth,Result)

#	nmi(groundtruth, communities)