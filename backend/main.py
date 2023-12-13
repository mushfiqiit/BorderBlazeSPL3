from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import open3d as o3d
from fastapi.middleware.cors import CORSMiddleware

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
    #point_cloud_data[:, 2] = 0

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

