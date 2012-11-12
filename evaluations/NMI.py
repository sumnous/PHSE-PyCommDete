# -*- coding: utf8 -*-

#[1,2,3,4,5,6,7,8,11,12,13,14,17,18,20,22],[9,10,15,16,19,21,23,24,25,26,27,28,29,30,31,32,33,34]

import numpy
from numpy import *
from scipy import *
from math import log

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
	#Ground_truth = [[1,2,3],[4,5,6],[7,8,9]]
	#Result = [[1,2],[3,6,9],[3,4,5,6],[6,7,8,9]]
	Ground_truth = [[1,2,3,4,5,6,7,8,11,12,13,14,17,18,20,22],\
	                [9,10,15,16,19,21,23,24,25,26,27,28,29,30,31,32,33,34]]
	Result = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 20, 22, 29, 31],\
	          [9, 10, 15, 16, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34]]
	print nmi(Ground_truth,Result)

#	confusion_matrix(Ground_truth,Result)

#	nmi(groundtruth, communities)