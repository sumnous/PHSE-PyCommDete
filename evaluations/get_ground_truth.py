# -*- coding: utf8 -*-
__author__ = 'nourl'


def get_ground_truth(fn):
	f = file(fn, 'r')
	d={}
	for line in f:
		kv = line[:-1].split('\t')
		kv =[int(kv[0]), int(kv[1])]
		if d.get(kv[1]):
			d[kv[1]].append(kv[0])
		else:
			d[kv[1]]=[kv[0]]
	ground_truth = []
	for x in d:
		ground_truth.append(d[x])

	f.close()
	return ground_truth