import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math

def KNearestNeighbor(file_path):
    point_cloud= np.loadtxt(file_path, skiprows=1, max_rows=10000)
    n=len(point_cloud)
    k=min(1000, n-1)
    averageDistance=[]
    for nodeToFindNeighbor in range(0, n):
        ##print(nodeToFindNeighbor)
        neighbors=[]

        for i in range(0, n):
            distanceOfNodeI=0.0
            if(i==nodeToFindNeighbor):
                    continue
            for j in range(0, 3):
                distanceOfNodeI+=(point_cloud[i][j]-point_cloud[nodeToFindNeighbor][j])*(point_cloud[i][j]-point_cloud[nodeToFindNeighbor][j])
            distanceOfNodeI=math.sqrt(distanceOfNodeI)
            neighbors.append([distanceOfNodeI, i])
        neighbors.sort()
        """print("Coordinates of desired point ", end=" ")
        for j in range(0, 3):
                if(j==2):
                    print(point_cloud[nodeToFindNeighbor][j])
                else:
                    print(point_cloud[nodeToFindNeighbor][j], end=" ")"""
        totalDistance=0.0
        for i in range(0, k):
            totalDistance+=neighbors[i][0]
            """print("Distance: ", end=" ")
            print(neighbors[i][0], end="  ")
            print("Index: ", end=" ")
            print(neighbors[i][1], end="  ")
            print("Coordinates: ", end=" ")
            for j in range(0, 3):
                if(j==2):
                    print(point_cloud[neighbors[i][1]][j])
                else:
                    print(point_cloud[neighbors[i][1]][j], end=" ")"""
        averageDistance.append(totalDistance/k)
    sumOfAverageKDistances=0.0
    for item in averageDistance:
        sumOfAverageKDistances+=item
    threshold=sumOfAverageKDistances/n
    isBoundaryPoint=[]
    for i in range(0, n):
        if(averageDistance[i]>threshold):
            isBoundaryPoint.append(1)
        else:
            isBoundaryPoint.append(0)
    return isBoundaryPoint


