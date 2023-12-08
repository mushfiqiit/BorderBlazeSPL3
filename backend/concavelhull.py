import numpy as np
import matplotlib.pyplot as plt
import alphashape
from descartes import PolygonPatch

def ConcaveHull(file_path):
    point_cloud= np.loadtxt(file_path, skiprows=1, max_rows=10000)
    n=len(point_cloud)
    # Assuming point_cloud has three columns (x, y, z)
    points = point_cloud[:, :2]

    alpha_shape = alphashape.alphashape(points, 2.0)
    fig, ax = plt.subplots()
    ax.scatter(*zip(*points))
    ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
    plt.show()
    return []
    
