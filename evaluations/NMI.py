# -*- coding: utf8 -*-

# karate ground truth:
# [1,2,3,4,5,6,7,8,11,12,13,14,17,18,20,22],[9,10,15,16,19,21,23,24,25,26,27,28,29,30,31,32,33,34]

import numpy
from numpy import *
from scipy import *
from math import log
from get_ground_truth import get_ground_truth

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
	print "N", N
	x_len = len(x)
	y_len = len(y)
	CM = confusion_matrix(x,y)
	A = float(0)
	B = float(0)
#	print sum(map(lambda x:x[2],CM))
	for i in range(x_len):
		for j in range(y_len):
			Ci = float(sum(CM[i]))
			Cj = float(sum(map(lambda x:x[j],CM)))
			Cij = CM[i][j]
			x = (Cij*N)/(Ci*Cj)
			A = A + Cij*judgelog(x)
	A = (-2) * A
	for i in range(x_len):
		Ci = float(sum(CM[i]))
		B = B + Ci*judgelog(Ci/N)
	for j in range(y_len):
		Cj = float(sum(map(lambda x:x[j],CM)))
		B = B + Cj*judgelog(Cj/N)
	if A == 0 or B == 0:
		return 0
	else:
		return A/B

def get_num_nodes(list):
	d={}
	for item in list:
		for i in item:
			d[i]=1
	return len(d)

def judgelog(x):
	if x <= 0:
		return 0
	else:
		return log(x)

if __name__=="__main__":
	#test 01
#	Ground_truth = [[1,2,3],[4,5,6],[7,8,9]]
#	Result = [[1,2],[3,6,9],[3,4,5,6],[6,7,8,9]]

	#test karate nmi=0.546086186904
#	Ground_truth = [[1,2,3,4,5,6,7,8,11,12,13,14,17,18,20,22],\
#	                [9,10,15,16,19,21,23,24,25,26,27,28,29,30,31,32,33,34]]
#	Result = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 20, 22, 29, 31],\
#	          [9, 10, 15, 16, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34]]

	#test GN_128 nmi=0.698494780436
#	Ground_truth = get_ground_truth('../benchmarks/benchmark_2_2/community.dat')
#	Result = [[1, 11, 21, 24, 34, 36, 43, 44, 48, 51, 57, 59, 63, 65, 69, 70, 75, 80, 84, 85, 87, 94, 97, 99, 101, 103, 105, 117, 118, 121, 124, 126, 128],\
#	          [2, 6, 10, 12, 13, 15, 18, 23, 25, 31, 35, 37, 38, 39, 49, 53, 55, 66, 72, 76, 78, 79, 81, 83, 86, 91, 95, 96, 98, 107, 110, 112, 116, 119, 123, 125, 127],\
#	          [3, 5, 7, 8, 9, 15, 16, 20, 22, 25, 28, 30, 32, 33, 40, 46, 55, 58, 60, 61, 62, 64, 72, 79, 82, 89, 90, 92, 95, 100, 102, 106, 108, 110, 113, 127],\
#	          [4, 11, 14, 17, 19, 26, 27, 29, 41, 42, 45, 47, 49, 50, 52, 54, 56, 67, 68, 71, 73, 74, 77, 80, 88, 93, 94, 102, 103, 104, 105, 109, 111, 114, 115, 120, 121, 122, 124]]
	print nmi(Ground_truth,Result)

#	confusion_matrix(Ground_truth,Result)

#	nmi(groundtruth, communities)