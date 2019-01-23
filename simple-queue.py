# -*- coding: utf-8 -*-
''' time-advance- simple queue '''

import numpy as np

# We will use unordered lists (arrays) and search for the event with
# minimum time, this is not efficient for large systems but fine just
# for working with most examples... we will discuss options for more
# efficient simulations as well (ARENA, etc.)

# define customers, eventnotice, and methods for random number generation
class customer():
    def __init__(self, customerid, arrivaltime):
        self.customerid = customerid
        self.arrivaltime = arrivaltime
        
class eventnotice():
    def __init__(self, eventtype, futuretime,customerid):
        self.eventtype = eventtype
        self.futuretime = futuretime
        self.customerid = customerid
        
def atime():
    muA = 4.5
    return np.random.exponential(muA)

def stime():
    muS= 3.2
    sigma = 0.6
    return np.random.normal(muS,sigma)

#init stats
maxqueuelength = 0
totalbusytime = 0
S = 0 # sum customer response times for customers WHO HAVE DEPARTED
Nd = 0 # total number of departures UP TO CURRENT simulation time
F = 0 # total number of customers who spend 4 minutes or more in system

# initialization: note you can assume customer 1 shows up at CLOCK = 0
# and proceeds directly to service so schedule their dep, and next arrival
# event_types - 0 is arrival, 1 means departure
TE = 4500      #when to stop simulation after this time (can use number of departures instead)
CLOCK = 0
LQ = 0 
LS = 1
numcustomers = 1 #counter: total number of customers that have ENTERED system
checkoutline = [] 
FEL = [] 

checkoutline.append((customer(numcustomers,CLOCK))) 
FEL.append(eventnotice(1,stime(),numcustomers))

numcustomers = numcustomers + 1
FEL.append(eventnotice(0,atime(),numcustomers))

# -------MAIN PROGRAM ------------
while CLOCK < TE:                  #stop condition Nd departures
    #imminentevent =  min(FEL, key=attrgetter('futuretime'))
    FEL = sorted(FEL, key=lambda x: x.futuretime)
    IE = FEL.pop(0)
    advance = IE.futuretime - CLOCK
    CLOCK = IE.futuretime
    if IE.eventtype == 0:        #arrival logic
        if LS == 1:
            LQ = LQ + 1
            if LQ > maxqueuelength:
                maxqueuelength = LQ
            totalbusytime = totalbusytime + advance
            checkoutline.append((customer(IE.customerid,CLOCK)))            
        else:
            LS = 1
            FEL.append(eventnotice(1,CLOCK + stime(),IE.customerid))
            checkoutline.append((customer(IE.customerid,CLOCK)))
        #SCHEDULE NEXT ARRIVAL       
        numcustomers = numcustomers + 1         
        FEL.append(eventnotice(0,CLOCK + atime(),numcustomers))
    
    else:                                     #departure logic
        departing = next((x for x in checkoutline if x.customerid == IE.customerid), None) #inefficient search
        S = S + CLOCK - departing.arrivaltime
        Nd = Nd + 1
        if CLOCK - departing.arrivaltime >= 4:
            F = F + 1
        checkoutline.remove(departing)
        totalbusytime = totalbusytime + advance
        
        if LQ > 0:
            LQ = LQ - 1
            checkoutline = sorted(checkoutline, key=lambda x: x.arrivaltime)  # don't worry about this
            firstinline = checkoutline[0]
            FEL.append(eventnotice(1,CLOCK + stime(),firstinline.customerid))
        else:
            LS = 0
         
#-------REPORT GENERATOR-----------------------
print("U = ", totalbusytime/CLOCK)
print("S = ", S/Nd) 
print("F = ", F/Nd)  
print("MaxLinelength = ", maxqueuelength)        
print("simulation run length = ", CLOCK) 
print("number of departures= ", Nd) 
