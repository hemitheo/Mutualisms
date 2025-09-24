# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 15:23:48 2024

@author: tl5
"""

import numpy as np
import matplotlib.pyplot as plt
import random

# Parameters
T = 600 # Number of periods
epsilon = 0.2 # Mutation rate
n = 50  # State space maximum

lowerBound = 0.2 # lower region boundary of utility function
upperBound = 0.7 # upper region boundary of utility function

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

def doMutation(z, m): #returns mutated z value based on aggregate probability
    for i in range(n):
        roll = random.random()
        if roll <= epsilon: #mutation case
            roll2 = random.randint(0,1)
            if roll2 == 1:
                z += 1/n
            else:
                z -= 1/n
    return z

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
    print(region_values)
    # NOTE: PERCENTAGE MATH IS NOT PERFECT AND MIGHT NEED TO BE DONE AS 100 - SUM OF 2 OTHER VARIABLES SO IT IS ALWAYS 100%
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("The system was in region R2 for " + str(c1) + " iterations, corresponding to " + str(round(100 * (c1 / T), 5)) + "% of the time.")
    print("The system was in region R0 for " + str(c2) + " iterations, corresponding to " + str(round(100 * (c2 / T), 5)) + "% of the time.")
    print("The system was in region R1 for " + str(c3) + " iterations, corresponding to " + str(round(100 * (c3 / T), 5)) + "% of the time.")
    return 
    
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
        
    print("Crossover statistics:")
    print("Number of direct transitions R2-R1: " + str(cover13))
    print("Number of direct transitions R1-R2: " + str(cover31))
    print("Number of indirect transitions R2-R0-R1: " + str(cover123))
    print("Number of indirect transitions R1-R0-R2: " + str(cover321))
    print("Number of returns R2-R0-R2: " + str(creturn1))
    print("Number of returns R1-R0-R1: " + str(creturn3))
    print("Number of escapes from R2 to R0: " + str(c12))
    print("Number of escapes from R1 to R0: " + str(c32))
    
    return

# Iterative process
for t in range(T):
    u1 = u_s1(z) #determine u of s1 in this period
    u2 = u_s2(z) #determine u of s2 in this period
    
    zprime = z*(u1 / (z * u1 + (1-z)*u2)) #calculate zprime, but this value does not conserve individuality...
    
    zprime = round_z(zprime) # clean value of z to respect individuals

    # Apply mutation
    zprime = doMutation(zprime, epsilon)

    # Enforce bounds
    if zprime > 1:
        zprime = 1
    elif zprime < 0:
        zprime = 0
        
    print(zprime)
    z = zprime
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

do_stats()
do_crossovers()

