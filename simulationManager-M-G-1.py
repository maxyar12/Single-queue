# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 03:40:37 2019

@author: maxya
"""
import SSQMG1
import numpy
import matplotlib.pyplot as plt
from matplotlib import rcParams

plt.rcParams["figure.figsize"] = [10,7.5]
rcParams['axes.titlepad'] = 20 
rcParams['axes.labelpad'] = 10 
def plot(y,x,xlabel,ylabel,title,x2,y2,lb,lbb):

    fig1, ax = plt.subplots()
    ax.tick_params(axis = 'both', which = 'major', labelsize = 18)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = 18)
    ax.set_xlabel(xlabel,fontsize=20)
    ax.set_ylabel(ylabel,fontsize=20)
    ax.set_title(title,fontsize=20)
    ax.plot(x, y,'--o',label = lbb)
    ax.plot(x2,y2, label = lb)
    ax.annotate(r"$\mu = $"+str(mu),(1,1),(0.75,20),fontsize='xx-large')
    ax.legend(loc='upper left',prop={'size': 18})
    
def plot2(y,x,xlabel,ylabel,title,x2,y2,y3,y4):

    fig1, ax = plt.subplots()
    ax.tick_params(axis = 'both', which = 'major', labelsize = 18)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = 18)
    ax.set_xlabel(xlabel,fontsize=20)
    ax.set_ylabel(ylabel,fontsize=20)
    ax.set_title(title,fontsize=20)
    ax.plot(x, y,'--ro',label = r'$\hat{L}$')
    ax.plot(x2,y2,'-r', label = r'$L = \rho + \frac{\lambda^2(\frac{1}{\mu^2}+\sigma^2)}{2(1-\rho)}} $')
    ax.annotate(r"$\mu = $"+str(mu),(1,1),(0.75,20),fontsize='xx-large')
    ax.plot(x,y3,'--gx',label = r'$\hat{LQ}$')
    ax.plot(x2,y4,'-g',label = r'$LQ =\frac{\lambda^2(\frac{1}{\mu^2}+\sigma^2)}{2(1-\rho)} } $')
    ax.legend(loc='upper left',prop={'size': 18})

                        # TO SHOW 1/sqrt(TE) behavior
lambdas = numpy.linspace(0.82,0.97,10)      # TO SHOW 1/sqrt(TE) behavior
mu = 1.0
sigma = 0.0
j=0
rhos = numpy.zeros(len(lambdas))
ws = numpy.zeros(len(lambdas))
Ls = numpy.zeros(len(lambdas))
LQs = numpy.zeros(len(lambdas))
wQs = numpy.zeros(len(lambdas))
for l in lambdas:
    r = simulate(100000,0,1/l,1/mu,sigma)
    ws[j] = r[2]
    Ls[j] = r[0]
    LQs[j] = r[1]
    wQs[j] =r[3]
    rhos[j] = r[4]
    j+=1

x2 = numpy.linspace(0.82,0.97,1000) 
wts = 1/mu + x2*(1/mu**2 + sigma**2)/(2*(1-x2/mu))  
Lts = x2/mu + x2**2*(1/mu**2 + sigma**2)/(2*(1-x2/mu)) 
LQts = x2**2*(1/mu**2 + sigma**2)/(2*(1-x2/mu)) 
rhots = x2
eq = r'$\frac{\lambda}{\mu}$'
es = r'$\hat{\rho}$'
plot(rhos,lambdas,r"$\lambda$",r"$\rho$",r'M/G/1 queue, $\hat{\rho}$ vs $\lambda \qquad  , \mu = '+str(mu)+'$',x2,rhots,eq,es)
es = r'$\hat{w}$'
eq = r'$w = \frac{1}{\mu} + \frac{\lambda(\frac{1}{\mu^2}+\sigma^2)}{2(1-\rho)} } $'
plot(ws,lambdas,r"$\lambda$","w",r'M/G/1 queue, w vs $\lambda \qquad \sigma ='+str(sigma)+'  , \mu = '+str(mu)+'$',x2,wts,eq,es)
plot2(Ls,lambdas,r"$\lambda$","",r'M/G/1 queue, L,$L_Q$ vs $\lambda \qquad \sigma ='+str(sigma)+'  , \mu = '+str(mu)+'$',x2,Lts,LQs,LQts)
     

