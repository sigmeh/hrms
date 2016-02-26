#!/usr/bin/env python
import cgi,json
print
def main():
	with open('./ref/major_isotope_masses.txt','r') as f:		#open isotope data file (csv format)
		major_isotopes = [x.split(',') for x in f.read().split()]
	majors = {}
	for i in range(len(major_isotopes)):						#transform csv data into dictionary 'majors'
		majors[major_isotopes[i][0]] = major_isotopes[i][1]
	data = cgi.FieldStorage()['formula'].value				#get user input formula to add 
	data = json.loads(data)
	try:
		formula = data[1].split(' ')
		elements = [];number_each=[]
		for i in range(0,len(formula),2):						#parse data into sister lists (elements/number_each)
			elements.append(formula[i])
			number_each.append(int(formula[i+1]))
		mass=0
		for i in range(len(elements)):							#iteratively add to fragment mass
			mass+=float(majors[elements[i]])*number_each[i]
		with open('./ref/fragments.txt','a') as f:				#append new data to fragments.txt document
			f.write(str(data[0])+','+str(mass)+','+str(data[1])+'\n')			
		print mass												#return new mass to append to frag list
	except:														#throw exception for general formula error
		print 'error'
if __name__ == '__main__':
	main()