# -*- coding: utf-8 -*-
''' time-advance- simple queue '''

import numpy as np       # DEPENDENCY - to make random numbers easily

    
def simulate(TE,wantreport,ma,ms,sd):
    
    #---------------INITIALIZE STATISTICS------------------------------
    muA = ma
    muS= ms
    sigma = sd
    B = 0                 # total server busy time
    w = 0                 # sum departed cust response times UP TO CLOCK
    wQ = 0
    Nd = 0                # total number of departures UP TO CLOCK
    avg_LQ = 0    
    L = 0
    # INITIZIALIZE SYSTEM VARS and LISTS -------------------------------------
    
    CLOCK = 0                 # simulation time
    LQ = 0                    # number of cust in queue
    LS = 1                   # server status (0-idle or 1-busy)
    checkoutline = []        # list of cust in line or being served
    FEL = []                 # future event notice list
    C_ID = 1                 # counter to keep track of customers
    
    checkoutline.append((customer(C_ID,CLOCK)))      # add cust number 1
    FEL.append(eventnotice(1,np.random.exponential(muA),C_ID))          # add D notice
    
    C_ID += 1
    
    FEL.append(eventnotice(0,np.random.exponential(muA),C_ID))         # add next A notice
    
    # -------MAIN PROGRAM ------------
    
    while CLOCK < TE:    
              
        FEL = sorted(FEL, key=lambda x: x.futuretime)   # SORT THE FEL BY TIME
        IE = FEL.pop(0)                                 # remove IMMINENT EVENT
        advance = IE.futuretime - CLOCK                 # get CHANGE IN TIME 
        CLOCK = IE.futuretime                           # advance the CLOCK
        
        avg_LQ = avg_LQ + advance*LQ
        L = L + advance*(LQ + LS)
        
        if IE.eventtype == 0:                          #arrival logic
            if LS == 1:
                LQ = LQ + 1
                B = B + advance
                checkoutline.append((customer(IE.customerid,CLOCK)))            
            else:
                LS = 1
                FEL.append(eventnotice(1,CLOCK + np.random.normal(muS,sigma),IE.customerid))
                checkoutline.append((customer(IE.customerid,CLOCK)))
            #SCHEDULE NEXT ARRIVAL       
            C_ID += 1        
            FEL.append(eventnotice(0,CLOCK + np.random.exponential(muA),C_ID))
        
        else:                                                #departure logic
            departing = next((x for x in checkoutline if \
                              x.customerid == IE.customerid), None) 
            w = w + CLOCK - departing.arrivaltime
            Nd = Nd + 1
            checkoutline.remove(departing)
            B = B + advance
            
            if LQ > 0:
                LQ = LQ - 1
                checkoutline = sorted(checkoutline, key=lambda x: x.arrivaltime)  
                firstinline = checkoutline[0]
                wQ = wQ + CLOCK - firstinline.arrivaltime
                FEL.append(eventnotice(1,CLOCK + np.random.normal(muS,sigma),firstinline.customerid))
            else:
                LS = 0
             
    #-------REPORT GENERATOR-----------------------
    
    if wantreport == 1:
        print("U = ", B/CLOCK)
        print("L = ", L/CLOCK)
        print("L_Q = ", avg_LQ/CLOCK)
        print("w = ", w/Nd) 
        print("w_Q = ", wQ/Nd)          
        print("simulation run length = ", CLOCK) 
        print("s= ", Nd) 
 
    #------------ return statements -------------------
    
    return (L/CLOCK,avg_LQ/CLOCK,w/Nd,wQ/Nd,B/CLOCK)
#----------------END SIMULATION------------------------
    
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

if __name__ == '__main__':
    simulate(1000000,1,4.5,3.2,0.6)