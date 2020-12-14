#!/usr/bin/env python
# coding: utf-8

# # EduCube
# ## Thermal Experiment
# #### Kate Kiernan

# The following code reads the temperature data from telemetry packets obtained using EduCube and plots the temperature increase and decrease over time. From this data, the power usage of the two aluminium panels is calculated.

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import math


# In[2]:


#Read in the file with the thermal experiment data
thermPath = r'C:\Users\kateh\Documents\Masters\Space Detector Lab\ThermalData.txt'

with open(thermPath, 'r') as allData:
    thermData = allData.readlines()


# Create a list containing only the lines with the temperatures of the three temperature sensors for the solar black and solar white panels:

# In[3]:


useful = []

for i in range(len(thermData)):
    line = thermData[i]
        
    if 'THERM' in line:
        useful.append(line)


# Function to make three lists of the data from the temperature sensors for a single panel:

# In[4]:


def get_individ_temp(pxy):
    a = pxy[0]
    b = pxy[1]
    c = pxy[2]
    
    #Split the strings to extract only the temperature value in degrees celcius
    aT_str = a.split(',')
    aT = float(aT_str[1])
    
    bT_str = b.split(',')
    bT = float(bT_str[1])
    
    cT_str = c.split(',')
    cT = float(cT_str[1])
    
    #Calculate the mean temperature from the three thermocouples
    panel_temp = (aT+bT+cT)/3
    
    return(panel_temp)


# Function to plot the temperature of the two panels against the time interval over which data was obtained:

# In[5]:


def plot_Temp(p1_h, p2_h, p1_c, p2_c):
    time_heat = []
    time_cool = []
    
    #Get number of data points taken over heating and cooling periods
    heat = len(p1_h)
    cool = len(p1_c)
    
    th = 0
    tc = 0
    
    time_heated_mins = 22
    time_cooled_mins = 28
    
    for i in range(len(p1_h)):
        th+=(time_heated_mins/heat) #Time interval
        time_heat.append(th)
    
    for i in range(len(p1_c)):
        tc+=(time_cooled_mins/cool) #Time interval
        time_cool.append(tc)
    
    
    #Plot temperature increase of the two panels
    fig = plt.figure(figsize=(6,4))
    plt.scatter(time_heat, p1_h, s=2, color='black')
    plt.scatter(time_heat, p2_h, s=2, color='cyan')
    plt.title('Temperature increase with time', size=15, color='black')
    plt.xlabel('Time (mins)', size=12, color='black')
    plt.ylabel('Temperature (degrees)', size=12, color='black')
    plt.legend(['Solar Black', 'Solar White'], loc='center right', prop={'size':12})
    plt.grid(True)
    fig.tight_layout()
    fig.savefig(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\SolarBW_Heat.png')
    
    #Plot temperature decrease of the two panels
    fig2 = plt.figure(figsize=(6,4))
    plt.scatter(x=time_cool, y=p1_c, s=2, color='black')
    plt.scatter(x=time_cool, y=p2_c, s=2, color='cyan')
    plt.title('Temperature decrease with time', size=15, color='black')
    plt.xlabel('Time (mins)', size=12, color='black')
    plt.ylabel('Temperature (degrees)', size=12, color='black')
    plt.legend(['Solar Black', 'Solar White'], loc='upper right', prop={'size':12})
    plt.grid(True)
    fig2.tight_layout()
    fig2.savefig(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\SolarBW_Cool.png')
        


# Function to get the temperatures for both panels as they heated and cooled and plot them against the time intervals:

# In[6]:


def get_temps(data):
    p1_Tlist = []
    p2_Tlist = []
    
    
    for i in range(len(data)):
        line = data[i]
        line_split = line.split('|')
        
        #Get the temperature of the three temperature sensors for panel 1
        p1a = line_split[6]
        p1b = line_split[7]
        p1c = line_split[8]
        
        p1 = [p1a, p1b, p1c]
        
        #Get the temperature of the three temperature sensors for panel 2
        p2a = line_split[9]
        p2b = line_split[10]
        p2c = line_split[11]
        
        p2 = [p2a, p2b, p2c]
        
        #Calculate the temperatures of P1 and P2
        x=get_individ_temp(p1)
        y=get_individ_temp(p2)
        
        #Fill empty lists with temperature values
        p1_Tlist.append(x)
        p2_Tlist.append(y)
        
    
    p1_array = np.array(p1_Tlist)
    p1_max = np.argmax(p1_array)
    p1_max_i = int(p1_max)
    
    p2_array = np.array(p2_Tlist)
    
    p1_heating = []
    p2_heating = []
    
    p1_cooling = []
    p2_cooling = []
    
    #Fill lists with temperature values as the temperature increased and decreased 
    for i in range(330, p1_max_i+1):
        p1_heating.append(p1_array[i])
        p2_heating.append(p2_array[i])
        
    for i in range(p1_max_i+1, 3057):
        p1_cooling.append(p1_array[i])
        p2_cooling.append(p2_array[i])
        
    #Plot the temperature increase/decrease over time
    plot_Temp(p1_heating, p2_heating, p1_cooling, p2_cooling)

get_temps(useful)


# The following equation calculates the mean power of the SolarBlack panel (a similar method was used for the SolarWhite panel).

# In[7]:


def power():
    p100 = []
    
    #Extract data points when the resistors were on
    for i in range(len(useful)):
        line = useful[i]
        
        if 'THERM_P1,100' in line:
            p100.append(line)
    
    
    p1_Volt = []
    p1_Curr = []
    
    for i in range(len(p100)):
        #Split each line into separate elements
        line = p100[i]
        split = line.split('|')
        
        #The current and voltage values of p1 are contained in the 4th element of the line, the values for p2 in the 5th
        p1 = split[4]
        p2 = split[5]
        
        #Extract the voltage and current
        p1_split = p1.split(',')
        p1_V = p1_split[3]
        p1_I = p1_split[4]
        
        p1_V = float(p1_V)
        p1_I = float(p1_I)
        
        p1_Volt.append(p1_V)
        p1_Curr.append(p1_I)
        
    p1_Volt = p1_Volt[1:]
    p1_Curr = p1_Curr[1:]
    
    #Calculate the mean values for the voltage (mV) and current (mA)
    mean_p1V = np.mean(p1_Volt)
    mean_p1I = np.mean(p1_Curr)
      
    #Calculate the time interval in seconds
    time = 23*60
    
    #Caluclate the voltage and current in V and A
    p1V_volt = mean_p1V/1000
    p1I_amp = mean_p1I/1000
    
    #Calculate the power of the panel, and the heat in
    P = p1V_volt * p1I_amp #Heat per second
    Q = P * time
    
    print('Panel 1\nMean voltage:\t', mean_p1V, '\nMean current:\t', mean_p1I, '\nPower:\t\t', P, 'W\nHeat in:\t', Q, 'J')

power()


# The final function calculates the uncertainty in the power:

# In[8]:


def error():
    #Set the min and max value of the voltage
    volt_max = 11.42/1000
    volt_min = 11.22/1000
    #Calculate the range of the values
    volt_range = volt_max = volt_min
    n=1233 #The number of data points
    
    #Calculate the uncertainty on the voltage
    error_volt = (0.5*volt_range)/math.sqrt(n)
    
    #Repeat for current
    i_max = 183.0/1000
    i_min = 179.7/1000
    i_range = i_max - i_min
    
    error_i = (0.5*i_range)/math.sqrt(n)
    
    v = 11.243949716139497/1000
    i = 180.44744525547446/1000
    p = 0.0020289420008583895
    
    #Calculate the total uncertainty for the power 
    error = p*math.sqrt((error_volt**2)/v+(error_i**2)/i)
    print('Error in power: +/-', error, 'W')

error()

