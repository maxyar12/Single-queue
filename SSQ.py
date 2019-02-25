# -*- coding: utf-8 -*-
''' time-advance- simple queue '''

import numpy as np       # DEPENDENCY - to make random numbers easily

def simulate(runtime,wantreport):
    
    #---------------INITIALIZE STATISTICS------------------------------
    
    MQ = 0                # maximum queue length
    B = 0                 # total server busy time
    S = 0                 # sum departed cust response times UP TO CLOCK
    Nd = 0                # total number of departures UP TO CLOCK
    F = 0                 # total number of departed cust who spend >= 4 m
    
    # INITIZIALIZE SYSTEM VARS and LISTS -------------------------------------
    
    CLOCK = 0                 # simulation time
    LQ = 0                    # number of cust in queue
    LS = 1                   # server status (0-idle or 1-busy)
    checkoutline = []        # list of cust in line or being served
    FEL = []                 # future event notice list
    C_ID = 1                 # counter to keep track of customers
    
    checkoutline.append((customer(C_ID,CLOCK)))      # add cust number 1
    FEL.append(eventnotice(1,stime(),C_ID))          # add D notice
    
    C_ID += 1
    
    FEL.append(eventnotice(0,iatime(),C_ID))         # add next A notice
    
    TE = runtime                                       # stopping condition
    
    # -------MAIN PROGRAM ------------
    
    while CLOCK < TE:    
              
        FEL = sorted(FEL, key=lambda x: x.futuretime)   # SORT THE FEL BY TIME
        IE = FEL.pop(0)                                 # remove IMMINENT EVENT
        advance = IE.futuretime - CLOCK                 # get CHANGE IN TIME 
        CLOCK = IE.futuretime                           # advance the CLOCK
        
        if IE.eventtype == 0:                          #arrival logic
            if LS == 1:
                LQ = LQ + 1
                if LQ > MQ:
                    MQ = LQ
                B = B + advance
                checkoutline.append((customer(IE.customerid,CLOCK)))            
            else:
                LS = 1
                FEL.append(eventnotice(1,CLOCK + stime(),IE.customerid))
                checkoutline.append((customer(IE.customerid,CLOCK)))
            #SCHEDULE NEXT ARRIVAL       
            C_ID += 1        
            FEL.append(eventnotice(0,CLOCK + iatime(),C_ID))
        
        else:                                                #departure logic
            departing = next((x for x in checkoutline if \
                              x.customerid == IE.customerid), None) 
            S = S + CLOCK - departing.arrivaltime
            Nd = Nd + 1
            if CLOCK - departing.arrivaltime >= 4:
                F = F + 1
            checkoutline.remove(departing)
            B = B + advance
            
            if LQ > 0:
                LQ = LQ - 1
                checkoutline = sorted(checkoutline, key=lambda x: x.arrivaltime)  
                firstinline = checkoutline[0]
                FEL.append(eventnotice(1,CLOCK + stime(),firstinline.customerid))
            else:
                LS = 0
             
    #-------REPORT GENERATOR-----------------------
    
    if wantreport == 1:
        print("U = ", B/CLOCK)
        print("S = ", S/Nd) 
        print("F = ", F/Nd)  
        print("MaxLinelength = ", MQ)        
        print("simulation run length = ", CLOCK) 
        print("number of departures= ", Nd) 
    return S/Nd

#---------classes and RN generation ------------------------
    
class customer():
    def __init__(self, customerid, arrivaltime):
        self.customerid = customerid
        self.arrivaltime = arrivaltime
        
class eventnotice():
    def __init__(self, eventtype, futuretime,customerid):
        self.eventtype = eventtype
        self.futuretime = futuretime
        self.customerid = customerid
        
def iatime():
    muA = 4.5
    return np.random.exponential(muA)

def stime():
    muS= 3.2
    sigma = 0.6
    return np.random.normal(muS,sigma)

if __name__ == '__main__':
    simulate(4500,1)