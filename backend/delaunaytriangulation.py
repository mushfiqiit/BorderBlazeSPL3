from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
from scipy.spatial import Delaunay
from collections import defaultdict
import open3d as o3d
from fastapi.middleware.cors import CORSMiddleware
from scipy.spatial import distance
import math


app = FastAPI()

destination_path = f"uploads/file1.pts"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])*(point1[0]-point2[0])+(point1[1]-point2[1])*(point1[1]-point2[1]))

@app.get("/method/3/")
async def delaunay_approach():
    point_cloud_data = np.loadtxt(destination_path, skiprows=1, max_rows=10000)
    n = len(point_cloud_data)
    point_cloud_data[:, 2] = 0
    point_cloud_data = point_cloud_data[:, :3]
    points_2d = []

    for i in range(n):
        points_2d.append([point_cloud_data[i][0], point_cloud_data[i][1]])

    points_2d = np.array(points_2d)  # Convert to NumPy array

    # Example of scaling coordinates
    points_2d /= 100000000  # Scale by dividing


    # Example of removing duplicate points
    #points_2d = np.unique(points_2d, axis=0)

    xavg=0.0
    yavg=0.0
    for i in range(n):
        xavg+=points_2d[i][0]
        yavg+=points_2d[i][1]
    xavg/=n
    yavg/=n
    for i in range(n):
        points_2d[i][0]-=xavg
        points_2d[i][1]-=yavg


    tri = Delaunay(points_2d, furthest_site=False, incremental=False, qhull_options='Qbb Qc Qz')


    # Create a dictionary to store the count for each edge
    edge_triangle_count = defaultdict(int)

    """ for simplex in tri.simplices:
        print(simplex[0])
        print(simplex[1])
        print(simplex[2]) """
    
    threshold=0.0

    # Iterate over each simplex to collect unique edges
    for simplex in tri.simplices:
        if(simplex[0]==simplex[1] or simplex[1]==simplex[2] or simplex[1]==simplex[2]):
            continue
        for i in range(3):  # A triangle has three edges
            edge = tuple(sorted([simplex[i], simplex[(i + 1) % 3]]))
            edge_triangle_count[edge] += 1

    # Convert the set of edges to a list for easier handling
    edges_list = list(edge_triangle_count.keys())

    isBoundary = [0] * n

    # Identify boundary points
    for edge in edges_list:
        point1, point2 = edge
        threshold+=distance(points_2d[point1], points_2d[point2])
        if edge_triangle_count[edge]<=1:
            ##print(edge)
            isBoundary[point1] = 1
            isBoundary[point2] = 1

    threshold/=len(edges_list)

    for edge in edges_list:
        point1, point2 = edge
        if(distance(points_2d[point1], points_2d[point2])>2.2*threshold):
            isBoundary[point1]=1
            isBoundary[point2]=1

    red_points = []
    green_points = []

    for i in range(n):
        if isBoundary[i] == 1:
            red_points.append(point_cloud_data[i])
        else:
            green_points.append(point_cloud_data[i])

    # Create Open3D point cloud objects
    red_point_cloud = o3d.geometry.PointCloud()
    red_point_cloud.points = o3d.utility.Vector3dVector(red_points)
    red_point_cloud.paint_uniform_color([1, 0, 0])  # Red color

    green_point_cloud = o3d.geometry.PointCloud()
    green_point_cloud.points = o3d.utility.Vector3dVector(green_points)
    green_point_cloud.paint_uniform_color([0, 1, 0])  # Green color

    # Merge the two point clouds
    merged_point_cloud = red_point_cloud + green_point_cloud

    # Visualize the point cloud
    o3d.visualization.draw_geometries([merged_point_cloud])

    # Convert the plot to an image
    plt.scatter(points_2d[:, 0], points_2d[:, 1], color='blue', marker='o', label='Original Points')
    plt.triplot(points_2d[:, 0], points_2d[:, 1], tri.simplices, color='red', label='Delaunay Triangulation')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Delaunay Triangulation on 2D Points')
    plt.legend()

    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plt.clf()  # Clear the plot for the next request

    # Return the image as a response
    return StreamingResponse(content=img_stream, media_type="image/png")
