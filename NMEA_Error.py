#!/usr/bin/env python
# coding: utf-8

# ## NMEA Error Calculation
# #### Kate Kiernan

# A short function to calculate the error of the NMEA GPS data in metres.

# In[22]:


def nmea_error():
    #mean values of latitude and longitude obtained from telemetry data
    telem_mean_lat = 53.3091176484536
    telem_mean_long = -6.224815077319589
    
    #mean values of latitude and longitude obtained from nmea data
    nmea_mean_lat = 53.309608074142155
    nmea_mean_long = -6.22480473345588
    
    #get error of nmea latitude and longitude using error = (measured-expected)/expected
    error_lat = (nmea_mean_lat-telem_mean_lat)/telem_mean_lat
    error_long = (nmea_mean_long-telem_mean_long)/telem_mean_long
    
    r=6371000
    
    #Calculate error in metres
    error_long_dist=error_long*r
    error_lat_dist=error_lat*r
    
    print('Latitude error in metres:\t ', error_lat_dist, 'm\nLongitude error in metres:\t', error_long_dist, 'm')
    print('\nLatitude error in degrees:\t ', error_lat, 'degrees\nLongitude error in degrees:\t', error_long, 'degrees')

nmea_error()

