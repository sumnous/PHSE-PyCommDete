def partition_list(lst, num):
	"""return list of lists"""
	result=[]
	for i in range(num):
		result.append([lst[x] for x in range(len(lst)) if x%num==i])
	return result

def split_list(lst,num):
	result=[]
	i=0
	while i<len(lst):
		if (len(lst)-1-(i-1)) >= num:
			tmp=lst[i:i+num]
		else:
			tmp=lst[i:]
		i = i+num
		result.append(tmp)

#	print "result, ,,,,",result
	return result

def test():
	print split_list([1,2,3,4,5,6,7,8,9,10,11,12,13],3)

#print range(5,0,-1)
#test()
