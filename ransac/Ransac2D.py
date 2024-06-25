import numpy as np
from matplotlib import pyplot as plt
import math
import random

def ransac2D(obj, env, iters, thres):
    # Samples len(obj) points and finds points in env within a threshold of error thres
    # returns best matched points and associated error, threshold is the threshold
    # of error !!per point!!

    thres = thres * len(obj)
    bestFit = []
    bestError = math.inf

    obj_vectors = findPointVectors(obj)
    # Apply RANSAC sampling random points on env and fit to obj
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
        print(len(temp_vectors))
        #print(rand)
        #print(temp_points)
        #print(temp_vectors)

        # compare to obj vectors to find error
        curr_error = np.sum(vector_differences_and_norms(obj_vectors, temp_vectors))
        #print(curr_error)
        if curr_error < bestError and curr_error < thres:
            bestFit = temp_points
            bestError = curr_error
            #print(bestError)
            #print(bestFit)
        i += 1
    
    # find centre of best fit points
    x_com = 0
    y_com = 0
    
    for p in bestFit:
        x_com += p[0]
        y_com += p[1]
    
    if len(bestFit) == 0:
        raise Exception("Object not found within given threshold.")
    else: 
        x_com = x_com / len(bestFit)
        y_com = y_com /len(bestFit)

    return (bestFit, bestError,(x_com,y_com))
    


def findPointVectors(points):
    # take n points and return n(n-1)/2 unique vectors for each line between them
    # e.g. a shape of 6 points returns 15 vectors corresponding to all 15 unique 
    # connections between points

    n = len(points)
    vectors = []
    for i in range(n):
        for j in range(i + 1, n):
            vector = (points[j][0] - points[i][0], points[j][1] - points[i][1])
            vectors.append(vector)
    return vectors


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


# Tests, run in order
# %% findPointVector tests

# triangle - 3 lines
triangle_test1 = [(0,0),(1,1),(1,0)]
print('fpv_test1 triangle: {}'.format(len(findPointVectors(triangle_test1))))

# %% pentagon - 15 lines
pentagon_test2 = [(0,2),(1,1.5),(-1,1.5),(1,0),(-1,0),(0,0)]
print('fpv_test2 pentagon: {}'.format(len(findPointVectors(pentagon_test2))))

# %% 20 points - 190 lines
fpv_test3 = []
for _ in range(20):
    x = random.uniform(-10, 10)  # Random x coordinate between -10 and 10
    y = random.uniform(-10, 10)  # Random y coordinate between -10 and 10
    fpv_test3.append((x, y))

print('fpv_test3 20: {}'.format(len(findPointVectors(fpv_test3))))

# %% RANSAC2D tests

# find triangle in a 5 point cloud
obj1 = [(0,0),(1,1),(1,0)]
env1 = [(0,0),(1,1),(0,1),(2,3),(5,2),(9,9)]
env1_x = []
env1_y = []

for p in env1:
    env1_x.append(p[0])
    env1_y.append(p[1])
    
fit, err, com = ransac2D(obj1,env1,100,3)

print('best fitting points are: {}, error = {}, com = {}'.format(fit,err,com))
plt.scatter(env1_x, env1_y, c='blue')
plt.scatter(com[0],com[1], c='g')
plt.show()
# %% find house shape 

# make data
r2d_test1 = fpv_test3
r2d_test1.extend(pentagon_test2)
x_r2d_test1, y_r2d_test1 = zip(*r2d_test1)

fit, err, com = ransac2D(pentagon_test2, r2d_test1, 1000, 5)
print('best fitting points are: {}, error = {}, com = {}'.format(fit,err,com))


plt.scatter(x_r2d_test1, y_r2d_test1, c='blue')
plt.scatter(com[0],com[1], c = 'g')
plt.show()

# %%
