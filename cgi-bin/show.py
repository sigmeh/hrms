#!/usr/bin/env python
# Load formatted spectral data and
# process according to view specifications (full spectrum or custom zoom)
# data passed as [SpectralData] json object

import cgi,json,os,sys
import matplotlib; matplotlib.use('Agg') 
import pylab as pl
from pylab import rcParams
rcParams['figure.figsize'] = 8,3
print

#--------begin main --------#
def main():
	#--------begin extract json data and ensure file exists--------#
	data = cgi.FieldStorage()['spectralData'].value
	spectralData = json.loads(data)
	
	filename = str(spectralData[0])
	path = filename.split('.')[0]			
	
	if not os.path.exists('./data_files/'+path):	
		print 'File not formatted or file does not exist'; return
	else:
		path = './data_files/'+path + '/' + path
	#--------end extract json data and ensure file exists--------#
	
	
	#--------begin load data files (x,y)--------#
		#----x data ----#
	with open(path + '_xVals.txt','r') as f:
		xArrayNum = [float(x) for x in f.read().split()]		
		#----y data ----#
	with open(path + '_yValsNorm.txt','r') as f:					#y vals normalized to 100
		yArrayNum = [float(x) for x in f.read().split()]	
	#--------end load data files (x,y)--------#
	
	
	#--------begin determine spectral window size--------#
	if spectralData[2] != 'full':				
		#----custom zoom specified----#
			#----x zoom ----#
		xmin = int(spectralData[1])			
		xminLocation = xArrayNum.index( filter( lambda x: x<xmin,xArrayNum ) [-1] )
		
		xmax = int(spectralData[2])				
		xmaxLocation = xArrayNum.index( filter( lambda x: x<xmax,xArrayNum ) [-1] )	
		if not xmaxLocation:					#if max not found, use final data point
			xmaxLocation = len(xArrayNum)-1
			
			#----y zoom ----#	
		ymin = int(spectralData[3])			
		ymax = int(spectralData[4])				

	else:										
		#----show full spectrum----#
		xminLocation = 0						
		xmaxLocation = len(xArrayNum)			
		ymin = 0								
		ymax = max(yArrayNum)					
	#--------end determine spectral window size--------#
	
	
	#--------begin generate plot and save--------#
	pl.plot(xArrayNum, yArrayNum)				#plot data as pylab plot
	pl.title('DESI HRMS spectrum')				#title
	pl.xlabel('m/z')							#x label	
	pl.ylabel('intensity')						#yl abel	

	xmin = round(xArrayNum[xminLocation])		#set xmin from xArrayNum data
	xmax = round(xArrayNum[xmaxLocation-1])		#set xmax

	pl.xlim(xmin, xmax)							#set x limits
	pl.ylim(ymin, ymax)							#set y limits

	pl.tight_layout()
	savedFilePath = path + '_fig_full.png'		#set filename for save

	matplotlib.pyplot.savefig(savedFilePath)	#save new figure for transfer to DOM
	#--------end generate plot and save--------#
	
	
	#--------begin send data back to hrms.js--------#
	spectralData[0] = savedFilePath				
	spectralData[1] = xmin						
	spectralData[2] = xmax						
	spectralData[3] = ymin					
	spectralData[4] = ymax						
	spectralData[5] = xmaxLocation - xminLocation

	print json.dumps(spectralData)				#json-encode for transfer to html
	#--------end send data back to hrms.js--------#
	
#--------end main --------#	
if __name__ == '__main__':
	main()