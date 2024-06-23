import numpy as np
from matplotlib import pyplot as plt
import math


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