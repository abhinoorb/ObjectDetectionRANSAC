import numpy as np
from matplotlib import pyplot as plt
from numpy import random
import math

# %%

import math

def linepointDistance(x,y,m,b):
    # returns closest distance from the point (x,y) to the line y=mx+b as int
    temp = abs(b + (m*x) - y)
    temp =  temp / math.sqrt(1 + (m**2))
    return temp

linepointDistance(0,2,0.825454545454546,1.916363636363637)

# %%

import random

def RANSAC_linear(n_inliers, x, y, iters, thres, n_fit):
    # This function assumes x and y are ordered arrays of the same size s.t. the nth point is given by (x[n], y[n])
    # Initialize empty best fit model
    bestFit = (0,0)
    bestError = None
    bestinliers = 0
    i = 0
   
    # Iterate over data, sampling n_inliers and fitting to linear model, y = mx + b
    while i < iters:
        temp_x = []
        temp_y = []
        temp_inliers = 0
       
        # sample data for n_inliers points
        rand = random.sample(range(len(x)), n_inliers)
        for j in rand:
            temp_x.append(x[j])
            temp_y.append(y[j])
           
        print(temp_x)
        print(temp_y)
       
        # fit to linear model
        m,b = np.polyfit(temp_x,temp_y, 1)
        print(m,b)
       

        # find the num of points which are within given threshold t to inliers
        for k in range(len(x)):
            if not (x[k] in temp_x):
                if linepointDistance(x[k], y[k], m, b) <= thres:
                    temp_inliers += 1
                   
        # if the model fits n_fit or more points save it to bestFit
        if temp_inliers >= n_fit and temp_inliers > bestinliers:
            bestinliers = temp_inliers
            bestFit = m,b
       
        i += 1
       
    # return the x,y coordinates of the best fitting model  
    bestFit_x = x
    bestFit_y = bestFit[0]*x+bestFit[1]
    print(bestinliers)
   
    return bestFit, bestFit_x, bestFit_y

# Scattered data set
# %%

x = np.random.randint(0,10, size = 30)
y = np.random.randint(0,10, size = 30)

# %%

bestFit, bestx, besty = RANSAC_linear(3,x,y,100,0.5,5)
plt.plot(bestx, besty)
plt.scatter(x,y)

# %%
