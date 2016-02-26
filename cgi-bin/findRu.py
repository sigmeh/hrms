#!/usr/bin/env python
# Find candidates for ruthenium-containing species in data set

import matplotlib; matplotlib.use('Agg') 
import numpy as np; import pylab as pl; print
from pylab import rcParams
import cgi,json,os,sys,copy
rcParams['figure.figsize'] = 28,22
def save(saveName, saveContents):						#save function
	saveName = './data_files/'+path + '/' + saveName
	saveFile = ''
	for i in range(len(saveContents)):
		saveFile += str(saveContents[i]) + ' '
	open(saveName, 'w').write(saveFile)

#start script here
data = cgi.FieldStorage()['package'].value				#retrieve json-encoded information request
data = json.loads(data)
filename = data[0]
threshold = data[1]
if not os.path.exists('./data_files/'+filename):		#handle filenames that don't exist
	print 'File not formatted or file does not exist'
path = filename.split('.')[0]							#derive filename to retrieve formatted data
datapath = './data_files/'+path + '/' + path + '_data.csv'
with open(datapath,'r') as f:
	data = f.read()
dataArray = data.split('\n')
points = []
for i in range(0,len(dataArray)-1):						#add number pairs to array points[]
	point = dataArray[i].split(',')
	points.append([ float(point[0]),float(point[1]) ]) 

peaks = [] 												#collected peak data (all peaks)
peak = []												#temp data for each peak, added to peaks
onPeak = False											
if points[0][1] > 0:									#starting point has intensity > 0
	onPeak = True
else:													#starting point has intensity = 0
	onPeak = False
for i in range(len(points)):
	if points[i][1] > 0:								#add point to peak[] if it has intensity
		onPeak = True									#currently on peak
		peak.append(points[i])							#add current point to current peak
	else:
		if (onPeak):									#arrived at first zero after peak
			peaks.append(peak)							#add new (complete) peak to peaks[]
			onPeak = False
		peak = []										#reset temp peak holder

save('peaks.txt',peaks)									#save peaks data through save function
														#peaks data is list of peak lists with all zero intensity data removed

maxPeaks = []											#create array of peak maxima (one point for each peak)
for i in range(len(peaks)):								#iterate over all peaks
	max = [0,0]
	for j in range(len(peaks[i])):						#iterate over accumulated points within each peak
		if float(peaks[i][j][1]) > max[1]:
			max = peaks[i][j]							#record maximum intensity point within each peak
	maxPeaks.append(max)								#add maximum intensity for each peak to maxPeaks[]
maxPeakSort = sorted(maxPeaks, key=lambda intensity: intensity[1])
maxPeakSort.reverse()									#sort by intensity
save('maxPeaks.txt',maxPeaks)							#save maxPeaks data

def checkPeak(origin, newLimit, direction):				#check all available peaks within range for suitable displacement
	for i in range(origin, newLimit, direction):
		val = abs(maxPeaksTrunc[i][0] - maxPeaksTrunc[origin][0])
		if val > .99 and val < 1.01:					#if suitably displaced, 
			return i									#return index value of relevant point
	return False										#return False if no relevant point is found

def checkNearbyPeaks(loc):								#check for cluster of five peaks around current most intense peak (from truncating list)
	candidateLines = [maxPeaksTrunc[loc]]				#create list candidateLines with first data point
	positions = [loc]
	num = loc
	for i in range(loc, len(maxPeaksTrunc)):			#determine effective range of peaks to test 
		if maxPeaksTrunc[i][0] - maxPeaksTrunc[loc][0] > 1.01:	#exclude data points outside this range
			num = i
			break
	newLimit = checkPeak(loc,num,1)
	if newLimit:										#found relevant new point
		candidateLines.append(maxPeaksTrunc[newLimit])							#add maxPeaks point to candidateLines
		positions.append(newLimit)												#add to positions list
		for i in range(newLimit,len(maxPeaks)):									#generate suitable range for testing additional peaks
			if maxPeaksTrunc[i][0] - maxPeaksTrunc[newLimit][0] > 1.01:
				num = i
				break	
		newLimit = checkPeak(newLimit,num,1)									#test new range for presence of applicable peak
		if newLimit:															#new peak found; continue
			candidateLines.append(maxPeaksTrunc[newLimit])						#add peak to candidateLines
			positions.append(newLimit)											#update positions
			for i in range(loc, 0, -1):											#check opposite direction from original (most intense) peak
				if abs(maxPeaksTrunc[i][0] - maxPeaksTrunc[loc][0]) > 1.01:		#determine suitable testing range
					num = i
					break
			newLimit = checkPeak(loc, num,-1)									#check for applicable peak in testing range
			if newLimit:														#applicable peak found
				candidateLines.append(maxPeaksTrunc[newLimit])					#update candidateLines
				positions.append(newLimit)										#update positions
				for i in range(newLimit, 0, -1):								#generate test range for 5th peak
					if abs(maxPeaksTrunc[i][0] - maxPeaksTrunc[newLimit][0]) > 1.01:
						num = i
						break
				newLimit = checkPeak(newLimit, num,-1)							#check for applicable peak within test range
				if newLimit:													#peak found
					candidateLines.append(maxPeaksTrunc[newLimit])				#update candidateLines
					positions.append(newLimit)									#update positions
					return candidateLines										#found five regularly-spaced peaks indicating possible presence of ruthenium
	return candidateLines								#test failed (5 evenly-spaced peaks not identified); peak likely not ruthenium

RuCount = 0												#count number of ruthenium candidates
RuList = []
maxPeaksTrunc = copy.copy(maxPeaks)						#new list for truncating data as it is examined
maxPeakSortTrunc = copy.copy(maxPeakSort)				#new list for truncating line data

while len(maxPeakSortTrunc) > 1:						#points remain to be analyzed
	testPeak = maxPeakSortTrunc[0]						#select first peak (highest intensity peak)
	checknum = maxPeaksTrunc.index(testPeak)			#find location of highest intensity peak in original maxPeaks list
	candidateLines = checkNearbyPeaks(checknum)			#check for nearby peaks (isotopic distribution)
	if len(candidateLines) == 5:						#equally-spaced 5-peak cluster suggestive of ruthenium
		RuCount += 1									#increment count
		RuList.append(candidateLines)					#record the five points
	for i in range(len(candidateLines)):
		maxPeakSortTrunc.pop(maxPeakSortTrunc.index(candidateLines[i]))			#truncate list by removing each candidate line
		maxPeaksTrunc.pop(maxPeaksTrunc.index(candidateLines[i]))				#truncate list by removing each candidate line
				
columns = round(RuCount**0.5)							#format for figure based on number of plots	
rows = columns + 1										#format for figure
f1 = pl.figure(1)
for i in range(int(rows*columns)):						#create figure containing subplots for each Ru candidate
	if i < len(RuList):									
		xmin = int(RuList[i][0][0]) - 12				#estimate "arbitrary" xmin value for plotting
		for j in range(0, len(points)):					
			if points[j][0] > xmin:						#find actual x value
				xmin = j
				break
		xmax = int(RuList[i][0][0]) + 12				#estimate "arbitrary" xmax for plotting
		for j in range(xmin, len(points)):
			if points[j][0] > xmax:						#find actual x value
				xmax = j
				break
		subplotX = []; subplotY = []					#generate each subplot x,y pair array
		for j in range(xmin, xmax):						
			subplotX.append(points[j][0])				#x values
			subplotY.append(points[j][1])				#y values

		pl.subplot(rows,columns,i+1).plot(subplotX, subplotY)
		pl.subplot(rows,columns,i+1).xlabel = ''
		pl.subplot(rows,columns,i+1).ylabel = ''
		
pl.tight_layout()
figurename = 'RuCandidates'
matplotlib.pyplot.savefig('./data_files/'+path + '/' + path + '_' + figurename + '.png')

RuCandidatesHtml = """\									
<head></head>
<body>
	<div id='title'>""" + path + '_' + figurename + """ </div>
	
	<img src='""" + path + '_' + figurename + """.png'/>
	<style>
		#title{
			font-size:30px;
		}
		img{
			width:100%;
			margin:0px;
			
		}
	</style>
</body>
"""
open('./data_files/'+path + '/' + path + '_' + figurename+ '.html','w').write(RuCandidatesHtml)

#print 'File'
#print str(len(maxPeakSort))


#print 'File saved... no data to print'	
#save('maxPeaks.txt', maxPeaks)
#print json.dumps(RuList)
print RuList
