#!/usr/bin/env python
# Format csv files located in the 'data_files' directory for further processing

import cgi,os,subprocess,time
print

#--------begin format data
def format_data(lines,filename):										
	#--------create folder; separate and save header
	foldername = filename[:len(filename)-4]								#drop extension to generate folder name from filename
	subprocess.Popen(['mkdir ./data_files/'+foldername],shell=True)		#create folder
	time.sleep(.5)
	head_body = lines.split('Intensity')								#separate head/body
	head = head_body[0]+'Intensity'
	body = head_body[1].split()
	headname = foldername + '_head.txt'
	open('./data_files/'+foldername + '/' + headname,'w').write(head)	#save header file
	#--------end create folder; separate and save header
	
	
	#--------separate and save x and y data
		#----x vals
	xFormatted = ' '.join([x.split(',')[0] for x in body])				#formatted for save
	xVals = [float(x) for x in xFormatted.split()]						#floats
	xname = foldername + '_xVals.txt' 
	open('./data_files/'+foldername + '/' + xname,'w').write(xFormatted)									
		#----end x vals
		
		#----y vals
	yFormatted = ' '.join([x.split(',')[1] for x in body])				#formatted for save
	yVals = [float(x) for x in yFormatted.split()]						#floats
	yname =  foldername + '_yVals.txt'	
	open('./data_files/'+foldername + '/' + yname,'w').write(yFormatted)									
		#----end y vals
	#--------end separate and save x and y data
	
	
	#--------normalize y values (max intensity = 100) and save
	max_y = max(yVals)
	yNormalized = [y*100/max_y for y in yVals]
	yNormVals = ' '.join([str(x) for x in yNormalized])
	yNorm = foldername + '_yValsNorm.txt'
	open('./data_files/'+foldername + '/' + yNorm,'w').write(yNormVals)
	#--------end normalize y values (max intensity = 100) and save
	
	xy_norm = '\n'.join([str(str(xVals[i])+','+str(yNormalized[i])) for i in range(len(xVals))])	#save normalized pairs
	open('./data_files/'+foldername+'/'+foldername+'_xy_norm.csv','w').write(xy_norm)
	
	data = '\n'.join([line for line in body])									#save body of data
	dataname = foldername + '_data.csv'
	open('./data_files/'+foldername + '/' + dataname,'w').writelines(data)		#make data file
	originalFile = foldername + '_original.csv'
	open('./data_files/'+foldername + '/' + originalFile,'w').writelines(lines)	#place original data in new folder
	
	#--------return message data
	print; print "Folder \'%s\' was created. Folder \'%s\' contains:<br>" %(foldername, foldername)
	print "&nbsp&nbsp %s <br>" %headname
	print "&nbsp&nbsp %s <br>" %dataname
	print "&nbsp&nbsp %s <br>" %xname
	print "&nbsp&nbsp %s <br>" %yname
	print "&nbsp&nbsp %s <br>" %yNorm
	print "&nbsp&nbsp %s <br>" %originalFile
	
#--------end format data


#--------begin main--------#
def main():
	#--------get filename and ensure it exists
	filename = cgi.FieldStorage()['package'].value					#get filename
	if not os.path.exists('./data_files/'+filename):				#if file does not exist
		print "\'%s\' does not exist" %filename						#end script
	else:
		folder = filename.rsplit('.')								#drop the csv extension to get folder name	
		if os.path.exists('./data_files/'+folder[0]):				#check for previously-formatted data
			print "\'%s\' is formatted" %filename					#if previously formatted, end script
		else:														#data not previously formatted; format now
			with open('./data_files/'+filename,'r') as f:	
				lines = f.read()
			#--------format data
			format_data(lines,filename)
#--------end main--------#
	
if __name__ == '__main__':
	main()