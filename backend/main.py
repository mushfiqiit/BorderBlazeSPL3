from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import open3d as o3d
from fastapi.middleware.cors import CORSMiddleware
from concavelhull import ConcaveHull

app = FastAPI()

# Fixed filename for the uploaded file

# Specify the destination path with the fixed filename
destination_path = f"uploads/file1.pts"

# Allow all origins in development (for testing purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_empty_plot(x, y, z, colors):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c=colors)
    ax.set_title("Point Cloud Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return buffer

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file with the fixed filename
        with open(destination_path, "wb") as dest_file:
            dest_file.write(file.file.read())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    # Load the point cloud data from the file
    point_cloud_data = np.loadtxt(destination_path, skiprows=1, max_rows=10000)
    point_cloud_data[:, 2] = 0

    point_cloud_data = point_cloud_data[:, :3]
    # Create an Open3D PointCloud object
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(point_cloud_data)

    green_color = np.array([0, 1, 0])
    point_cloud.colors = o3d.utility.Vector3dVector(np.tile(green_color, (
        len(point_cloud_data), 1)))

    # Visualize the point cloud
    o3d.visualization.draw_geometries([point_cloud])

    # Extract X, Y, Z coordinates from the point cloud data
    x = point_cloud_data[:, 0]
    y = point_cloud_data[:, 1]
    z = point_cloud_data[:, 2]

    # Create an array to hold the colors for each point
    colors = ['green'] * len(point_cloud_data)

    # Generate the empty plot
    empty_plot_buffer = generate_empty_plot(x, y, z, colors)

    # Return the empty plot as part of the API response
    return StreamingResponse(empty_plot_buffer, media_type="image/png")


@app.get("/method/1/")
async def neighborhoodapproach():
    isBoundaryPoint=KNearestNeighbor(destination_path)

    point_cloud_data = np.loadtxt(destination_path, skiprows=1, max_rows=10000)
    # Extract X, Y, Z coordinates from the point cloud data
    x = point_cloud_data[:, 0]
    y = point_cloud_data[:, 1]
    z = point_cloud_data[:, 2]
    # Create an array to hold the colors for each point
    colors = []

    # Example condition: If intensity value is greater than 0.5, color the point green, otherwise red

    for item in isBoundaryPoint:
        if item==1:
            colors.append('red')
        else:
            colors.append('green')
    
    empty_plot_buffer = generate_empty_plot(x, y, z, colors)

    # Return the empty plot as part of the API response
    return StreamingResponse(empty_plot_buffer, media_type="image/png")

@app.get("/method/2/")
async def ConcaveHullapproach():
    isBoundaryPoint=ConcaveHull(destination_path)

    point_cloud_data = np.loadtxt(destination_path, skiprows=1, max_rows=10000)
    # Extract X, Y, Z coordinates from the point cloud data
    x = point_cloud_data[:, 0]
    y = point_cloud_data[:, 1]
    z = point_cloud_data[:, 2]
    # Create an array to hold the colors for each point
    colors = []

    # Example condition: If intensity value is greater than 0.5, color the point green, otherwise red

    for item in isBoundaryPoint:
        if item==1:
            colors.append('red')
        else:
            colors.append('green')
    
    empty_plot_buffer = generate_empty_plot(x, y, z, colors)

    # Return the empty plot as part of the API response
    return StreamingResponse(empty_plot_buffer, media_type="image/png")

def generate_open3d_frame():
    # Create a simple point cloud for demonstration
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))

    # Create a simple scene
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)

    # Render the scene and get the image
    image = vis.capture_screen_float_buffer()

    # Convert the image to bytes
    image_bytes = np.asarray(image).astype(np.uint8).tobytes()

    # Close the window
    vis.destroy_window()

    return image_bytes

@app.get("/open3d_frame")
async def get_open3d_frame():
    # Generate some random 3D points for demonstration purposes
    np.random.seed(42)
    points_3d = np.random.rand(500, 3)

    # Create an Open3D PointCloud object
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points_3d)

    # Visualize the point cloud
    o3d.visualization.draw_geometries([point_cloud])

