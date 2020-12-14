#!/usr/bin/env python
# coding: utf-8

#    ## Radio Range
#    #### Kate Kiernan 

# This is a short piece of code to calculate the distance between the location of the EduCube and the location to which radio transmission was possible.

# In[17]:


from math import cos, asin, sqrt, pi

def distance(lat1, long1, lat2, long2):
    RE = 6371 #Radius of Earth
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((long2-long1)*p))/2
    dist = 2 * RE * asin(sqrt(a))
    dist_m = dist*1000
    
    print('Range: ', dist_m, 'm')

#lat1, long1 = position of EduCube
lat1 = 53.308976
long1 = -6.223973

#lat2, long2 = final position of the launch adapter
lat2 = 53.309063
long2 = -6.224862

distance(lat1, long1, lat2, long2)

