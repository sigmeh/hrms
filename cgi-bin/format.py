#!/usr/bin/env python
# Format csv files located in the 'data_files' directory for further processing

import cgi,os,subprocess,time
print
def format_data(lines):										#create folder; separate header from data; save files
	foldername = filename[:len(filename)-4]					#drop extension to generate folder name from filename
	subprocess.Popen(['mkdir ./data_files/'+foldername],shell=True)	#create folder
	time.sleep(.5)
	head_body = lines.split('Intensity')					#separate head/body
	head = head_body[0]+'Intensity'
	body = head_body[1].split()
	headname = foldername + '_head.txt'
	open('./data_files/'+foldername + '/' + headname,'w').write(head)	#save header file
	xVals = []; yVals = []
	for xy_pair in body:									#separate x,y pairs and append to respective lists
		xVals.append(float(xy_pair.split(',')[0]))
		yVals.append(int(float(xy_pair.split(',')[1])))
	xFormatted = ''; yFormatted = '';
	for i in range(len(xVals)):
		xFormatted += str(xVals[i]) + ' '					#convert x array to string
		yFormatted += str(yVals[i]) + ' '					#convert y array to string
	xname = foldername + '_xVals.txt' 
	yname = foldername + '_yVals.txt'	
	open('./data_files/'+foldername + '/' + xname,'w').write(xFormatted)	#save x values
	open('./data_files/'+foldername + '/' + yname,'w').write(yFormatted)	#save y values	
	maxY = 0; xAtMaxY = 0
	for i in range(len(yVals)):								#find maxY value for normalization
		if yVals[i] > maxY:
			maxY = yVals[i]
			xAtMaxY = i
	massAtMaxY = xVals[xAtMaxY]
	yNormalized = []
	for i in range(len(yVals)):								#normalize y values
		y = yVals[i] * 400 / maxY							#normalized to 400!
		yNormalized.append(y)
	yNormVals = ''
	for i in range(len(yNormalized)):						#convert normalized y values to string
		yNormVals += str(yNormalized[i]) + ' '
	yNorm = foldername + '_yValsNorm.txt'
	open('./data_files/'+foldername + '/' + yNorm,'w').write(yNormVals)
	data = ''
	for word in body:
		data += word + '\n'									#format for saving
	dataname = foldername + '_data.csv'
	open('./data_files/'+foldername + '/' + dataname,'w').writelines(data)		#make data file
	originalFile = foldername + '_original.csv'
	open('./data_files/'+foldername + '/' + originalFile,'w').writelines(lines)	#place original data in new folder
	print; print "Folder \'%s\' was created. Folder \'%s\' contains:<br>" %(foldername, foldername)
	print "&nbsp&nbsp %s <br>" %headname
	print "&nbsp&nbsp %s <br>" %dataname
	print "&nbsp&nbsp %s <br>" %xname
	print "&nbsp&nbsp %s <br>" %yname
	print "&nbsp&nbsp %s <br>" %yNorm
	print "&nbsp&nbsp %s <br>" %originalFile
	#print "The maximum intensity (%s), which occurs at data point %s (m/z = %s), has been normalized to 400." %(maxY,xAtMaxY,massAtMaxY)

#script starts here
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
		format_data(lines)
	
