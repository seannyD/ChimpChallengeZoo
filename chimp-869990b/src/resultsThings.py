import pygame
import random
import datetime
import csv
import os

from player import *

def saveRound(latency,num_numerals,buttons_selected,buttons_correct,roundTime,gridpos):	
	player = Player() # singleton
	
	now = datetime.datetime.now()
	
	buttons_selected = '_'.join([str(x) for x in buttons_selected])
	buttons_correct = '_'.join([str(x) for x in buttons_correct])
	print gridpos
	grid_positions = '_'.join([str(x[0])+'-'+str(x[1]) for x in gridpos])
	
	writeToCSV('results/rounds.csv',[latency,num_numerals,buttons_selected,buttons_correct,roundTime,now,player.name,player.age,grid_positions])

def setUpResultsFiles():
	""" Set up column heads"""
	f = 'results/rounds.csv'
	if not os.path.isfile(f):
		o = open(f,'w')
		o.write("latency,numerals,selected,correct,RT,time,name,age,grid\n")
		o.close()
	f = 'results/keyRounds.csv'
	if not os.path.isfile(f):
		o = open(f,'w')
		o.write("latency,numerals,correct\n")
		o.close()
	f= 'results/highscores.csv'
	if not os.path.isfile(f):
		o = open(f,'w')
		o.write("name,score\n")
		o.close()


def saveKeyRound(latency,num_numerals,correct):
	writeToCSV('results/keyRounds.csv',[latency,num_numerals,correct])
	
def saveScore():
	player = Player()
	writeToCSV('results/highscores.csv',[player.name,player.score])
	
def writeToCSV(fileName,data):
	""" Write a single line to a csv file
	"""
	o = open(fileName,'a')
	o.write(','.join([str(x) for x in data])+"\n")
	o.close()
	
def readFromCSV(fileName):
	with open(fileName,'rb') as f:
		return csv.DictReader(f, quotechar='\"')
    
def getResultsData(fileName,fields):
# this function used to convert text to int, but some files have text fields.
#	try:
	res = []
	with open(fileName,'rb') as f:
		for row in csv.DictReader(f, quotechar='\"'):
			res.append([row[x] for x in fields])
	return res
#	except:
#		return []