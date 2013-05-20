current=-1

with file('./valueid','r') as f:
	result=[]
	for line in f:
		line = line.strip().split('\t')
		if int(line[0]) == current:
			result.append(int(line[1]))
		else:
			for value in result:
				print value,
			print
			current = int(line[0])
			result=[int(line[1])]

	for value in result:
		print value,
