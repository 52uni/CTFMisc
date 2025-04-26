res=[]
res1=[]
with open("rgb.txt", "r") as f:
    data = f.readlines()
for i in data:
	if len(i)!=1:
		res.append(int(i.replace("\n","")))
for i in res:
	if i<=128 and i>=(ord('0')):
		res1.append(chr(i))
	else:
		continue
res3=[]
for i in res1:
	res3.append("{} : {}".format(i,res1.count(i)))
print(set(res3))	
