import numpy as np
from matplotlib import pyplot as plt
import math
import random

def ransac2D(obj, env, iters, thres):
    # Samples len(obj) points and finds points in env within a threshold of error thres
    # returns best matched points and associated error

    bestFit = []
    bestError = math.inf

    obj_vectors = findPointVectors(obj)
    
    # Apply RANSAC using random points on env and fit to obj
    i = 0
    while i < iters:
        temp_points = []
        temp_vectors = []

        # select len(obj) random points from env 
        rand = random.sample(range(len(env)), len(obj))
        for j in rand:
            temp_points.append(env[j])

        # find vectors
        temp_vectors = findPointVectors(temp_points)
        
        #print(rand)
        print(temp_points)
        #print(temp_vectors)

        # compare to obj vectors to find error
        curr_error = np.sum(vector_differences_and_norms(obj_vectors, temp_vectors))
        print(curr_error)
        if curr_error < bestError and curr_error < thres:
            bestFit = temp_points
            bestError = curr_error
            print(bestError)
            print(bestFit)
        i += 1
    
    # find centre of best fit points
    x_com = 0
    y_com = 0
    for p in bestFit:
        x_com += p[0]
        y_com += p[1]
    x_com = x_com / len(bestFit)
    y_com = y_com /len(bestFit)

    return (bestFit, bestError,(x_com,y_com))
    


def findPointVectors(points):
    # take n points and return n(n-1)/2 unique vectors for each line between them
    # e.g. a triangle of 3 points returns 3 vectors corresponding to all 3 unique 
    # connections between points

    vectors = set()  # Set to store unique vectors
    n = len(points)
    
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            
            # Ensure the vector is always from the smaller to the larger point
            if p1 < p2:
                vector = (p2[0] - p1[0], p2[1] - p1[1])
            else:
                vector = (p1[0] - p2[0], p1[1] - p2[1])
            
            vectors.add(vector)
    
    return list(vectors)


def vector_difference(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def vector_norm(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)

def vector_differences_and_norms(vectors1, vectors2):
    if len(vectors1) != len(vectors2):
        raise ValueError("Both lists must have the same length.")
    
    norms = []
    
    for v1, v2 in zip(vectors1, vectors2):
        diff_vector = vector_difference(v1, v2)
        norm = vector_norm(diff_vector)
        norms.append(norm)
    
    return norms



# example, find a triangle on a 5 point cloud

obj1 = [(0,0),(1,1),(1,0)]
env1 = [(0,0),(1,1),(0,1),(2,3),(5,2),(9,9)]
env1_x = []
env1_y = []

for p in env1:
    env1_x.append(p[0])
    env1_y.append(p[1])
    
fit, err, com = ransac2D(obj1,env1,100,5)

print('best fitting points are: {}, error = {}, com = {}'.format(fit,err,com))
plt.scatter(env1_x, env1_y, c='blue')
plt.scatter(com[0],com[1], c='g')
