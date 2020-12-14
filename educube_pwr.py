#Functions to extract relevant data from Educube telemetry.

def reader(file):

    '''
    Reads raw file and parses it.
    '''

    with open(file,'r') as f:

        data = f.readlines()

    return data

def eps_data(data):

    '''
    Extracts EPS data from file.
    '''
    
    eps_ = []

    for i in range(len(data)):

        line = data[i].split('|')

        if line[1] == 'EPS':

        	eps_.append(line[1:])

    return eps_

def val(data,index):
    
    '''
    Returns a value as a float from data line.
    '''
    
    x = float(data.split(',')[index])

    return x

def stat(val):

	'''
	Returns the mean and stddev of a list. 
	'''

	return (np.mean(val),np.std(val))

#---------------------------------------------------------------

#Script to determine the total power consumption.

import numpy as np
import matplotlib.pyplot as plt

tel = reader('eps_real.raw')

eps_tel = eps_data(tel)

#Need to parse for each subsystem (*DEFINE NAMES).

d0 = np.zeros((2,len(eps_tel)))
d1 = np.zeros((2,len(eps_tel)))
d2 = np.zeros((2,len(eps_tel)))
d3 = np.zeros((2,len(eps_tel)))
d4 = np.zeros((2,len(eps_tel)))

for i in range(len(eps_tel)):
     
	data = eps_tel[i][2:7]

	d0[0,i] = float(data[0].split(',')[2])
	d0[1,i] = float(data[0].split(',')[3])

	d1[0,i] = float(data[1].split(',')[2])
	d1[1,i] = float(data[1].split(',')[3])

	d2[0,i] = float(data[2].split(',')[2])
	d2[1,i] = float(data[2].split(',')[3])

	d3[0,i] = float(data[3].split(',')[2])
	d3[1,i] = float(data[3].split(',')[3])

	d4[0,i] = float(data[4].split(',')[2])
	d4[1,i] = float(data[4].split(',')[3])

#Using current and voltage values to find power.
#Error found through MC analysis.

def pwr(V_,I_):
     
     '''
     Inputs: Voltage and Current.
     Returns power (mW) of a subsystem with error.
     '''

     V = np.mean(V_) #stats.
     V_err = np.std(V_)
     I = np.mean(I_)
     I_err = np.std(I_)

     p = V*I
     p_err = p * np.sqrt((V_err/V)**2 + (I_err/I)**2)

     return (p,p_err)

p0 = pwr(d0[0],d0[1])
print(p0)
p1 = pwr(d1[0],d1[1])
print(p1)
p2 = pwr(d2[0],d2[1])
print(p2)
p3 = pwr(d3[0],d3[1])
print(p3)
p4 = pwr(d4[0],d4[1])
print(p4)

#Total power consumption.

total_pwr = (p0[0]+p1[0]+p2[0]+p3[0]+p4[0])
  
total_pwr_err = (p0[1]+p1[1]+p2[1]+p3[1]+p4[1])

print('')
print(total_pwr,total_pwr_err)

#Solar panel area

A = (total_pwr)/(0.22*(1361*1e3))

print('')
print(A)