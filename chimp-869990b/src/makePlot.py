'''
  This file is part of The Chimp Challenge.
  Copyright (C) 2012, Justin Quillinan <justin@justinq.net>
                      Sean Roberts, <s.g.roberts@sms.ed.ac.uk>

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
  
  
  Usage:
  means = readResults('sampleOutput.txt')
  makeMyGraph(means,otherLabel="Humans")
'''

import matplotlib.pyplot as plt

def readResults(filename):
	d = open(filename)
	dd = d.read()
	d.close()
	
	currentNum_col = 9
	maxNum_col = 5
	latency_col = 7
	
	levels = [210,400,600,1000]
	res = [[],[],[]]
	
	for line in dd.split("\n")[1:-1]:
		bits = line.split("\t")
		lat = int(bits[latency_col])
		curNum = int(bits[currentNum_col])
		maxNum = float(int(bits[maxNum_col]))
		print bits[latency_col],bits[currentNum_col],bits[maxNum_col]
		acc = curNum / maxNum
		if lat in levels and maxNum==5:
			res[levels.index(lat)].append(acc)
	means = []
	for x in res:
		if len(x)>0:
			means.append((100*sum(x))/float(len(x)))
	return means
	
	

def makeMyGraph(myAverages,otherLabel="You"):
	print 'make graph' , myAverages
	# takes list of 3 values representing percentage averages fro 650, 430 and 210ms
	# e.g. makeMyGraph([80,75,30])
	# e.g. makeMyGraph([80,75,30],"Humans")
	auymu = [84,82,80,78]
	
	lightGreen = (167/255.0,180/255.0,13/255.0,255/255.0)
	
	
	darkGreen = (0/255.0,97/255.0,50/255.0)

	p1, = plt.plot( auymu,'b^-',linewidth=5,markersize=12,color=lightGreen)
	p2, = plt.plot(myAverages,'ro-',linewidth=5,markersize=12,color=darkGreen)
	plt.legend([p1, p2], ["Auymu", otherLabel],loc=3,bbox_to_anchor=(0.,1.02,1.,.102),ncol=2)
	plt.ylim(0,100)
	plt.xlim(-0.5,3.5)
	plt.xticks( [0,1,2,3], ('1s','650ms', '430ms', '210ms') )
	plt.yticks( [20,40,60,80,100], ('20%', '40%', '60%','80%','100%') )
	plt.ylabel('Accuracy')
	plt.xlabel('Viewing time')
	#plt.show()
	plt.gcf().set_size_inches(5,2.5)
	plt.draw()
	plt.savefig('results/myGraph.png',dpi=100, bbox_inches='tight', facecolor=(1,1,1))
	plt.close()
	
