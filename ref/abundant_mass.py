#!/usr/bin/env python
#format exact mass data and save as
#major isotope masses (csv)
with open('massData.txt','r') as f:
	doc = f.read().replace('#','')
doc = doc.split('\r')
newdoc = [[x.split()[2],float(x.split()[3]),float(x.split()[5])] for x in doc]
doc2={}
for i in newdoc:
	if i[0] in doc2:
		doc2[i[0]].append([i[2],i[1]])
	else:
		doc2[i[0]] = [[i[2],i[1]]]
doc3={}
for i in doc2:
	doc3[i] = sorted(doc2[i],reverse=True)[0][1]
csv=''
for i in doc3:
	csv+=i[0]+','+str(i[1])+'\n'
with open('major_isotope_masses.txt','w') as f:
	f.write(str(csv))
