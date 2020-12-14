#!/usr/bin/env python
# coding: utf-8

# # Educube
# ## Determining position via GPS telemetry data
# #### Kate Kiernan

# The following code reads in the GPS telemetry data, extracts the measured position, and plots the location on a map of UCD. It also calculates the mean, standard deviation, and standard error of the latitude and longitude values.

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import scipy.stats


# In[2]:


#Read in the file with the GPS telemetry data
GPSPath = r'C:\Users\kateh\Documents\Masters\Space Detector Lab\gps_datacourtyard.txt'

with open(GPSPath, 'r') as allData:
    GPSData = allData.readlines()

#Print a snippet of the data in GPSData
for i in range(5):
    print(GPSData[i])


# It can be seen that GPSData contains the commands sent by the C&DH board along with the GPS data. The next step is to extract only the GPS data.

# In[3]:


#Create a list containing only the lines containing the GPS information
extract_useful = []

for i in range(len(GPSData)):
    line = GPSData[i]
        
    if '-6' in line:
        extract_useful.append(line)

gps_full_line=np.array(extract_useful)

#Print a snippet of the data in gps_full_line
for i in range(5):
    print(gps_full_line[i])


# This new list contains only the GPS data collected by the comms board. From this data, the position of the EduCube can be determined.

# The function get_GPS extracts the latitude and longitude values and adds them to two lists. A dataframe is created containing these lists, and read to a csv file that can be viewed for further analysis.

# In[4]:


def get_GPS(data):
    
    #Create empty lists
    latitude = []
    longitude = []
    
    for i in range(len(data)):
        line = data[i]
        line_split = line.split('|')
        
        info = line_split[2]
        info_split = info.split(',')
        
        #The 2nd and 3rd elements of info_split contain the latitude and longitude values without a decimal
        lat_no_dec = info_split[2]
        long_no_dec = info_split[3]
        
        #Add in a decimal point to get the latitude and longitude values in degrees and append them to the empty lists
        lat_split=lat_no_dec.split('53')
        lat_str = '53' + '.' + lat_split[1]
        lat = float(lat_str)
        latitude.append(lat)
        
        long_split = long_no_dec.split('-6')
        long_str = '-6' + '.' + long_split[1]
        long = float(long_str)
        longitude.append(long)
    
    #Create a dataframe containg the latitude and longitude values
    d = {'Latitude':latitude, 'Longitude':longitude}
    df = pd.DataFrame(d)
    
    #Write the dataframe to a csv file for further use
    df.to_csv(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\gps_data_outside.csv', index = False)
    
get_GPS(gps_full_line)


# The function plot_GPS reads in the dataframe created in the previous function, and plots the values over a map of a section of UCD.

# In[5]:


def plot_GPS():
    #Import the csv file
    df = pd.read_csv(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\gps_data_outside.csv')
    
    #Import the map image of the Science Building in UCD
    ucd = plt.imread(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\UCD_map_courtyard.png')
    bounds = (-6.22554, -6.22345, 53.30796, 53.30921) #Set the bounds of the map image
    
    #Plot the values on the map
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.scatter(df.Longitude, df.Latitude, zorder=1, alpha= 0.2, c='black', s=10)
    ax.set_title('EduCube Telemetry GPS Data (Outside)')
    ax.set_xlabel('Longitude (degrees)')
    ax.set_ylabel('Latitude (degrees)')
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])
    ax.imshow(ucd, zorder=0, extent = bounds, aspect= 'equal')
    fig.tight_layout()
    fig.savefig(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\GPS_Courtyard.png')
    
plot_GPS()


# The function get_uncertainty calculates the mean, standad deviation, and uncertainty values for the latitude and longitude. It then converts the uncertainties into distances in metres.

# In[6]:


def get_uncertainty():
    #Import the csv file
    df = pd.read_csv(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\gps_data_outside.csv')
    
    #Calculate the mean values
    mean_long = np.mean(df.Longitude)
    mean_lat = np.mean(df.Latitude)
    
    #Calculate the standard deviations
    sd_long = np.std(df.Longitude)
    sd_lat = np.std(df.Latitude)
    
    #Get the number of values in the dataframe
    points=df.Longitude.count()
    
    #Standard error for a normal distribution
    uncertainty_long = sd_long/math.sqrt(points)
    uncertainty_lat = sd_lat/math.sqrt(points)

    r=6371000 #Radius of Earth
    
    #Calculate the uncertainties in metres
    uncertainty_long=uncertainty_long*r
    uncertainty_lat=uncertainty_lat*r
    
    print('Mean latitude:\t\t\t', mean_lat, 'degrees\nMean longitude:\t\t\t', mean_long, 
          'degrees\nStandard deviation latitude:\t', sd_lat, 'degrees\nStandard deviation longitude\t', sd_long, 
          'degrees\nLatitude uncertainty:\t\t', uncertainty_lat, 'm\nLongitude uncertainty:\t\t', uncertainty_long, 'm')
    
    return(mean_long, mean_lat, sd_long, sd_lat, uncertainty_long, uncertainty_lat)

get_uncertainty()


# The above table shows the mean and standard deviation of the positional values in degrees, and the uncertainties of the position in metres.

# In[7]:


mean_long, mean_lat, sd_long, sd_lat, uncertainty_long, uncertainty_lat = get_uncertainty()


# The final step is to create a histogram to show the distribution of the values, and plot a Gaussian distribution for both sets of data.

# In[8]:


def hist_GPS(mean_long, mean_lat, sd_long, sd_lat):
    df = pd.read_csv(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\gps_data_outside.csv')
    
    get_uncertainty()
    
    #Set mean, variance for longitude
    mu = mean_long
    variance = sd_long
    sigma = math.sqrt(variance)
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    
    #Set mean, variance for latitude
    mu2 = mean_lat
    variance2 = sd_lat
    sigma2 = math.sqrt(variance2)
    x2 = np.linspace(mu2 - 3*sigma2, mu2 + 3*sigma2, 100)
    
    
    #Plot longitude
    fig = plt.figure()
    plt.hist(x=df.Longitude, bins=30)
    plt.title('Longitude Values of EduCube Telemetry Data (Outside)')
    plt.xlabel('Longitude (degrees)')
    plt.ylabel('Counts')
    plt.grid(True)
    fig.tight_layout()
    fig.savefig(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\Outside_Long.png')
    
    #Plot normal distribution for longitude
    fig2 = plt.figure()
    plt.plot(x, scipy.stats.norm.pdf(x, mu, sigma))
    plt.title('Gaussian Distribution for EduCube Longitude Data (Outside)')
    plt.xlabel('Longitude (degrees)')
    plt.ylabel('Gaussian Distribution')
    plt.grid(True)
    fig2.tight_layout()
    fig2.savefig(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\Outside_Long_Gaussian.png')
    
    
    #Plot latitude
    fig3 = plt.figure()
    plt.hist(x=df.Latitude, bins=30)
    plt.title('Latitude Values of EduCube Telemetry Data (Outside)')
    plt.xlabel('Latitude (degrees)')
    plt.ylabel('Counts')
    plt.grid(True)
    fig3.tight_layout()
    fig3.savefig(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\Outside_Lat.png')
    
    #Plot normal distribution for longitude
    fig4 = plt.figure()
    plt.plot(x2, scipy.stats.norm.pdf(x2, mu2, sigma2))
    plt.title('Gaussian Distribution for EduCube Latitude Data (Outside)')
    plt.xlabel('Latitude (degrees)')
    plt.ylabel('Gaussian Distribution')
    plt.grid(True)
    fig4.tight_layout()
    fig4.savefig(r'C:\Users\kateh\Documents\Masters\Space Detector Lab\Outside_Lat_Gaussian.png')
    
    
hist_GPS(mean_long, mean_lat, sd_long, sd_lat)

