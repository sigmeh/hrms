#!/usr/bin/env python
# Load formatted spectral data and
# process according to view specifications (full spectrum or custom zoom)
# data passed as [SpectralData] json object

import cgi,json,os,sys
import matplotlib; matplotlib.use('Agg') 
import numpy as np; import pylab as pl; print
from pylab import rcParams
rcParams['figure.figsize'] = 8,3

def findLocation(number):
	for i in range(len(xArrayNum)):
		if (xArrayNum[i] >= number):
			return i							#return array location for target number

data = cgi.FieldStorage()['spectralData'].value
spectralData = json.loads(data)
filename = str(spectralData[0])
if not os.path.exists('./data_files/'+filename[:len(filename)-4]):	#ensure file has been formatted
	print 'File not formatted or file does not exist'
else:
	path = filename.split('.')[0]				#derive foldername from filename
	path = './data_files/'+path + '/' + path	#format path to folder contents
	xPath = path + '_xVals.txt'					#path to x values
	yPath = path + '_yValsNorm.txt'				#path to y values
	with open(xPath,'r') as f:
		xData = f.read()						#read x values from formatted data
	xArray = xData.split()
	with open(yPath,'r') as f:					#read y values from normalized data
		yData = f.read()
	yArray = yData.split()
	xArrayNum = []; yArrayNum = []
	for i in range(len(xArray)):
		xArrayNum.append(float(xArray[i]))		#convert xArray(string) to float
		yArrayNum.append(int(float(yArray[i])))		#convert yArray(string) to int

	if spectralData[2] != 'full':				#custom zoom specified 
		xmin = int(spectralData[1])				#xmin 
		xmax = int(spectralData[2])				#xmax 
		xminLocation = findLocation(xmin)		#find location of xmin in data file 
		xmaxLocation = findLocation(xmax)		#find location of xmas in data file
		if not xmaxLocation:					#if max not found, use final data point
			xmaxLocation = len(xArrayNum)-1
		ymin = int(spectralData[3])				#ymin 
		ymax = int(spectralData[4])				#ymax
	
	else:										#'Show Full' button clicked; showing full spectrum
		xminLocation = 0						#first x data point
		xmaxLocation = len(xArray)				#final x data point
		ymin = 0								#ymin
		ymax = max(yArrayNum)					#ymax

	pl.plot(xArrayNum, yArrayNum)				#plot data as pylab plot
	pl.title('DESI HRMS spectrum')				#title
	pl.xlabel('m/z')							#x label	
	pl.ylabel('intensity')						#yl abel	

	xmin = round(xArrayNum[xminLocation])		#set xmin from xArrayNum data
	xmax = round(xArrayNum[xmaxLocation-1])		#set xmax

	pl.xlim(xmin, xmax)							#set x limits
	pl.ylim(ymin, ymax)							#set y limits

	fignum = str(1)
	pl.tight_layout()
	savedFilePath = path + '_fig_full.png'		#set filename for save

	matplotlib.pyplot.savefig(savedFilePath)	#save new figure for transfer to DOM
	spectralData[0] = savedFilePath				#reset SpectralData parameters for 
	spectralData[1] = xmin						#	transfer back to DOM messageBox
	spectralData[2] = xmax						#
	spectralData[3] = ymin						#
	spectralData[4] = ymax						#
	spectralData[5] = xmaxLocation - xminLocation

	print json.dumps(spectralData)				#json-encode for transfer to html
	