#!/usr/bin/env python
import cgi,json
print
def main():

	#---------extract major isotope mass data from text file (comma-separated) and generate majors dict
	with open('./ref/major_isotope_masses.txt','r') as f:		
		major_isotopes = [x.split(',') for x in f.read().split()]	
	majors = {}
	for i in range(len(major_isotopes)):						
		majors[major_isotopes[i][0]] = major_isotopes[i][1]	
	
	
	#----------load user input formula
	data = cgi.FieldStorage()['formula'].value					
	data = json.loads(data)
	
	
	try:
		#-------------parse formula data and generate elements/number_each sister lists
		formula = data[1].split(' ')
		elements = [];number_each=[]
		for i in range(0,len(formula),2):						
			elements.append(formula[i])
			number_each.append(int(formula[i+1]))
		
		
		#---------------iterate over formula to generate mass
		mass=0
		for i in range(len(elements)):							
			mass+=float(majors[elements[i]])*number_each[i]
		
		
		#------------append new data to fragments.txt document
		with open('./ref/fragments.txt','a') as f:				
			f.write(str(data[0])+','+str(mass)+','+str(data[1])+'\n')			
		print mass		#return new mass to append to frag list
	except:		
		#--------------formula parse error												
		print 'error'
	
		
if __name__ == '__main__':
	main()