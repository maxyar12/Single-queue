# -*- coding: utf-8 -*-
''' time-advance- simple queue '''

import numpy as np

# We will use unordered lists (arrays) and search for the event with
# minimum time, this is not efficient for large systems but fine just
# for working with most examples... we will discuss options for more
# efficient simulations as well (ARENA, etc.)

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

# initialization: note you can assume customer 1 shows up at clock = 0
# and proceeds directly to service so schedule their dep, and next arrival
# event_types - 0 is arrival, 1 means departure
CLOCK = 0   
TE = 4500   # simulation END time
LQ = 0      # size of queue
LS = 1      # server status 1 = busy , 0 = idle
numcustomers = 1 # counter for number of customers entered
checkoutline = []  # list of customers in system, yet to depart, both in queue and at counter
FEL = []           # future event notice list

checkoutline.append((customer(numcustomers,clock))) # update membership list
FEL.append(eventnotice(1,stime(),numcustomers))     # insert departure event-notice into FEL

numcustomers = numcustomers + 1                     # update counter
FEL.append(eventnotice(0,atime(),numcustomers))     # insert arrival event-notice into FEL

# -------MAIN PROGRAM ------------
while clock < TE:
    #imminentevent =  min(FEL, key=attrgetter('futuretime'))
    FEL = sorted(FEL, key=lambda x: x.futuretime)
    IE = FEL.pop(0)
    advance = IE.futuretime - clock
    clock = IE.futuretime
    if IE.eventtype == 0:        #arrival logic
        if LS == 1:
            LQ = LQ + 1
            if LQ > maxqueuelength:
                maxqueuelength = LQ
            totalbusytime = totalbusytime + advance
            checkoutline.append((customer(IE.customerid,clock)))            
        else:
            LS = 1
            FEL.append(eventnotice(1,clock + stime(),IE.customerid))
            checkoutline.append((customer(IE.customerid,clock)))
        #SCHEDULE NEXT ARRIVAL       
        numcustomers = numcustomers + 1         
        FEL.append(eventnotice(0,clock + atime(),numcustomers))
    
    else:                                     #departure logic
        departing = next((x for x in checkoutline if x.customerid == IE.customerid), None) #inefficient search
        S = S + clock - departing.arrivaltime
        Nd = Nd + 1
        if clock - departing.arrivaltime >= 4:
            F = F + 1
        checkoutline.remove(departing)
        totalbusytime = totalbusytime + advance
        
        if LQ > 0:
            LQ = LQ - 1
            checkoutline = sorted(checkoutline, key=lambda x: x.arrivaltime)
            firstinline = checkoutline[0]
            FEL.append(eventnotice(1,clock + stime(),firstinline.customerid))
        else:
            LS = 0
         
#-------REPORT GENERATOR-----------------------
print("U = ", totalbusytime/clock)
print("S = ", S/Nd) 
print("F = ", F/Nd)  
print("MaxLinelength = ", maxqueuelength)        
print("simulation run length = ", clock) 
print("number of departures= ", Nd) 
