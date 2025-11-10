# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 15:23:48 2024
Edited on Sat Nov 8 9:49:55 2025

@author: tl5
"""

import numpy as np
import matplotlib.pyplot as plt
import random

# Parameters
T = 5000 # Number of periods 
epsilon = 0.1 # Mutation rate 
n = 50 # State space maximum 

sims = 500 # Number of simulations to run

lowerBound = 0.3 # 0.2 lower region boundary of utility function
upperBound = 0.65 # 0.7 upper region boundary of utility function

# Initialize z_0 as a random fraction in [0, 1]
z = np.random.uniform(0, 1)
z_values = [z]  # To store the values of z_t over time
region_values = [0] * T # list storing values

# Utility function
def u_t(z):
    if z < lowerBound:
        return -1
    elif lowerBound <= z <= upperBound:
        return 0
    elif z > upperBound:
        return 1
    else:
        print("Error in determining Utility. Out of bounds! Z=" +str(z))
        return 0
    
def u_s1(z): # return utility of strategy 1 for a given z
    if z < lowerBound:
        return 2
    elif lowerBound <= z <= upperBound:
        return 2.5
    elif z > upperBound:
        return 3
    else:
        print("Error in determining Utility 1. Out of bounds! Z=" +str(z))
        return 
    
def u_s2(z): # return utility of strategy 2 for a given z
    if z < lowerBound:
        return 3
    elif lowerBound <= z <= upperBound:
        return 2.5
    elif z > upperBound:
        return 2
    else:
        print("Error in determining Utility 2. Out of bounds! Z = " +str(z))
        return 

def doMutation(z, m):
    #defunct
    #k = int(round(z * n))
    # each of n individuals mutates with prob ε, half up and half down
    #ups   = np.random.binomial(n - k, m / 2)
    #downs = np.random.binomial(k, m / 2)
    #new_k = k + ups - downs
    #new_k = min(max(new_k, 0), n)
    #return new_k / n

    s1 = int(z * n) #number of individuals playing S1, (top strategy)
    s2 = int((1-z) * n) # number of individuals playing S2, (bottom strategy)
    s1Adds = 0
    s2Adds = 0 
    for i in range(s1):
        roll = random.random()
        if roll <= m: # mutation case
            roll2 = round(np.random.uniform(0, 1))
            if roll2 == 1 or roll2 == 1.0:
                s2Adds += 1
                s1Adds -= 1

    
    for j in range(s2):
        roll = random.random()
        if roll <= m: # mutation case
            roll2 = round(np.random.uniform(0, 1))
            if roll2 == 1 or roll2 == 1.0:
                s1Adds += 1
                s2Adds -= 1

    s1 += s1Adds
    if s1 > n:
        s1 = n
    elif s1 + s1Adds < 0:
        s1 = 0.0
    return (s1 / n)

def round_z(z): #takes a given z value, and returns new z that has been modified to stay true to individuals.
    ind = z * n
    #print("individuals number = " +str(ind))
    indclean = round(ind)
    zclean = indclean / n # return new z value calculated from rounding number of individuals
    #print("individuals number cleaned = " +str(indclean))
    return zclean

def do_stats(): # Develop statistics
    c1 = 0
    c2 = 0
    c3 = 0
    
    for i in range(T):
        
        if z_values[i] < lowerBound: # in region 1
            region_values[i] = 1
            c1 += 1
            
        elif z_values[i] > upperBound: # in region 3
            region_values[i] = 3
            c3 += 1
            
        else:
            region_values[i] = 2 # in region 2
            c2 += 1
    #print(region_values)
    # print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    # print("The system was in region R2 for " + str(c1) + " iterations, corresponding to " + str(round(100 * (c1 / T), 5)) + "% of the time.")
    # print("The system was in region R0 for " + str(c2) + " iterations, corresponding to " + str(round(100 * (c2 / T), 5)) + "% of the time.")
    # print("The system was in region R1 for " + str(c3) + " iterations, corresponding to " + str(round(100 * (c3 / T), 5)) + "% of the time.")
    return c1, c2, c3
    
def do_crossovers():
    rprev = 0 # initialize rprev to initial region
    rprevprev = 0
    
    #crossover 1-3 and 3-1 init
    cover13 = 0
    cover31 = 0

    #crossover 1-2-3 and 3-2-1 init
    cover123 = 0
    cover321 = 0
    
    #return 1-2-1 and 3-2-3 init
    creturn1 = 0
    creturn3 = 0
    
    #cross 1-2 and 3-2 init
    c12 = 0
    c32 = 0
    
    for i in range(T):
        if region_values[i] != rprev: # change of region...
            if region_values[i] == 1: # entering bottom region
                if rprev == 2: # coming from middle region check prev prev
                    if rprevprev == 1: # return 1 to 2 to 1
                        creturn1 += 1
                    elif rprevprev == 3: # crossover 3 to 2 to 1
                        cover321 += 1
                elif rprev == 3: # coming from top region - direct Crossover!
                    cover31 += 1
            elif region_values[i] == 2: # entering region 2
                if rprev == 1: # coming from region 1
                    c12 += 1
                elif rprev == 3: # coming from region 3
                    c32 += 1
            elif region_values[i] == 3:
                if rprev == 2: # coming from middle region - check prevprev
                    if rprevprev == 3: # return 3 to 1 to 3
                        creturn3 += 1
                    elif rprevprev == 1: # crossover 1 to 2 to 3
                        cover123 += 1
                elif rprev == 1: # Crosover direct from 1 to 3
                    cover13 += 1
                
            rprevprev = rprev
            rprev = region_values[i]
        
    # print("Crossover statistics:")
    # print("Number of direct transitions R2-R1: " + str(cover13))
    # print("Number of direct transitions R1-R2: " + str(cover31))
    # print("Number of indirect transitions R2-R0-R1: " + str(cover123))
    # print("Number of indirect transitions R1-R0-R2: " + str(cover321))
    # print("Number of returns R2-R0-R2: " + str(creturn1))
    # print("Number of returns R1-R0-R1: " + str(creturn3))
    # print("Number of escapes from R2 to R0: " + str(c12))
    # print("Number of escapes from R1 to R0: " + str(c32))
    
    return cover13, cover31, cover123, cover321

def do_POI(): # looks at points of interest and determines if a single step crossover takes place with it.
    r2POI = 0 # POIs in region 2; points where z = 0, and t != T
    r2POIC = 0 # POIs in region 2 where z[t] = 0, and z[t + 1] >= lowerbound
    r1POI = 0 # POIs in region 1; points where z = 1, and t != T
    r1POIC = 0 # POIs in region 1 where z[t] = 1, and z[t + 1] <= upperbound
    for i in range(T):
        #print(str(i))
        if z_values[i] == round_z((8 / n)): # previously == 0.0
            r2POI += 1
            if z_values[i + 1] >= lowerBound:
                r2POIC += 1
        elif z_values[i] == round_z((42 / n)): # previously == 1.0
            r1POI += 1
            if z_values[i + 1] <= upperBound:
                r1POIC += 1
    return r2POI, r2POIC, r1POI, r1POIC

# Simulation process
rlist = [0] * 3 # Initialize list containing number of Z values in each region in order (R2, R0, R1)
clist = [0] * 4 # Initialize list containing aggregated crossover data in order [R2-R1, R1-R2, R2-R0-R1, R1-R0-R2]
POIlist = [0] * 4 # Initialize list containing POI data in order [r2POI, r2POIC, r1POI, r1POIC]
# Iterative process
for s in range(sims):
    #Reinitialize z, z_values, and region_values
    k = np.random.random_integers(0, n)
    z = round_z(k / n)
    z_values = [z]  # To store the values of z_t over time
    region_values = [0] * T
    
    for t in range(T):
        u1 = u_s1(z) #determine u of s1 in this period
        u2 = u_s2(z) #determine u of s2 in this period
        
        #zprime = z
        #print()
        #print("zprime region:")
        zprime = z*(u1 / (z * u1 + (1-z)*u2)) #calculate zprime
        #print(zprime)
        zprime = round_z(zprime) # clean value of z to respect individuals
        #print("Pre mutation: " + str(zprime))
        # Apply mutation
        zprime = doMutation(zprime, epsilon)
        #print("Post mutation: " + str(zprime))
    
        #Enforce bounds
        if zprime > 1:
            zprime = 1
        elif zprime < 0:
            zprime = 0
            
        #print(zprime)
        z = round_z(zprime)
        z_values.append(z)
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(range(T + 1), z_values, marker='o', linestyle='-', color='b')
    plt.xlabel('Time Period (t)')
    plt.ylabel('z_t')
    plt.title('Over time evolution of z_t')
    plt.grid()
    plt.axhline(y = lowerBound, color = 'r', linestyle = '-')
    plt.axhline(y = upperBound, color = 'r', linestyle = '-')
    ax = plt.gca()
    ax.set_xlim(-5, T+5)
    ax.set_ylim(-0.1, 1.1)
    plt.show()
    
    print(str(int((s / sims) * 100)) + "% of the way done; " + str(s) + "/" + str(sims) + " sims")
    
    slist = do_stats() # Run statistics function and append region data to global list for each simulation.
    for i in range(len(rlist)):
        rlist[i] += slist[i]
        
    crlist = do_crossovers() # Run crossover tally function and append crossover data to global list for each simulation.
    for j in range(len(clist)):
        clist[j] += crlist[j]
    
    sPOIlist = do_POI()
    for k in range(len(POIlist)):
        POIlist[k] += sPOIlist[k]
    
    

# Find sum of crossovers:
csum = 0
for k in range(len(clist)):
    csum += clist[k]

    
print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
print("Region residency statistics:")
print("Across all " + str(sims) + " simulations, the system was in region R2 for " + str(rlist[0]) + " iterations, corresponding to " + str(round(100 * (rlist[0] / (T * sims)), 5)) + "% of the time.")
print("Across all " + str(sims) + " simulations, the system was in region R0 for " + str(rlist[1]) + " iterations, corresponding to " + str(round(100 * (rlist[1] / (T * sims)), 5)) + "% of the time.")
print("Across all " + str(sims) + " simulations, the system was in region R1 for " + str(rlist[2]) + " iterations, corresponding to " + str(round(100 * (rlist[2] / (T * sims)), 5)) + "% of the time.")
print()
print("Crossover statistics:")
if csum != 0:
    print("Number of direct transitions R2-R1: " + str(clist[0]) + ". This corresponds to " + str(round(100 * (clist[0] / csum), 5)) + "% of all transitions.")
    print("Number of direct transitions R1-R2: " + str(clist[1]) + ". This corresponds to " + str(round(100 * (clist[1] / csum), 5)) + "% of all transitions.")
    print("Number of indirect transitions R2-R0-R1: " + str(clist[2]) + ". This corresponds to " + str(round(100 * (clist[2] / csum), 5)) + "% of all transitions.")
    print("Number of indirect transitions R1-R0-R2: " + str(clist[3]) + ". This corresponds to " + str(round(100 * (clist[3] / csum), 5)) + "% of all transitions.")
elif csum == 0:
    print("No crossover events detected across all simulations.")
print()
print("POI statistics:")
if POIlist[0] > 0:
    print(str(POIlist[0]) + " POIs for R2, with " + str(POIlist[1]) + " of them immediately crossing over in next interval, or " + str(round(100 * (POIlist[1] / POIlist[0]), 5)) + "% of POIs in R2")
else:
    print("No POIS for R2 detected across all simulations")
if POIlist[2] > 0:
    print(str(POIlist[2]) + " POIs for R1, with " + str(POIlist[3]) + " of them immediately crossing over in next interval, or " + str(round(100 * (POIlist[3] / POIlist[2]), 5)) + "% of POIs in R1")
else:
    print("No POIS for R1 detected across all simulations")
#print(POIlist)
#print(z_values)
#number = 0
#for i in range(1000):
#    number += random.randint(0,1)
#print(number)