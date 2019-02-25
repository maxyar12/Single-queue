# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 03:40:37 2019

@author: maxya
"""
import SSQ
import numpy
import matplotlib.pyplot as plt

def plot(y,x,xlabel,ylabel,title):

    fig1, ax = plt.subplots()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.plot(x, y)
    ax.scatter(x,y)
    ax.plot() 

trials = 100                         # TO SHOW 1/sqrt(TE) behavior
TEs = [500,750,1000,2000,3000,4000,5000,7500,10000,20000]       # TO SHOW 1/sqrt(TE) behavior

sds = numpy.zeros(len(TEs))
avgs = numpy.zeros(len(TEs))

j=0

for simtime in TEs:
    
    responseTimes = numpy.zeros(trials)
    i = 0
    
    while i < trials:
        
        responseTimes[i] = simulate(simtime,0)
        i += 1
        
    sds[j] = numpy.std(responseTimes)
    avgs[j] = numpy.average(responseTimes)
    
    j+=1
    
plot(sds,TEs,"TEs","standard deviation of S",r'standard deviation of S over 100 simulations vs TE')    

trials = 1000
TEs = [10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500]
sds = numpy.zeros(len(TEs))
avgs = numpy.zeros(len(TEs))

j=0

for simtime in TEs:
    
    responseTimes = numpy.zeros(trials)
    i = 0
    
    while i < trials:
        
        responseTimes[i] = simulate(simtime,0)
        i += 1
        
    sds[j] = numpy.std(responseTimes)
    avgs[j] = numpy.average(responseTimes)
    
    j+=1
    
plot(avgs,TEs,"TEs","mean S",r'mean response time S over 1000 simulations vs TE')