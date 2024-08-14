import numpy as np
from stl import mesh

def load_stl(file_path):
    return mesh.Mesh.from_file(file_path)

def get_model_bounds(stl_mesh):
    min_bounds = np.min(stl_mesh.vectors, axis=(0, 1))
    max_bounds = np.max(stl_mesh.vectors, axis=(0, 1))
    return min_bounds, max_bounds

def slice_stl(stl_mesh, monitor_resolution, mm_to_pixels, layer_thickness):
    min_bounds, max_bounds = get_model_bounds(stl_mesh)

    # Calculate the number of layers based on the height of the model
    z_height = max_bounds[2] - min_bounds[2]
    num_layers = int(z_height / layer_thickness) + 1
    
    width, height = monitor_resolution
    slices = np.zeros((num_layers, height, width), dtype=np.uint8)

    # Calculate the model's 2D bounding box in pixels
    model_width = int((max_bounds[0] - min_bounds[0]) * mm_to_pixels)
    model_height = int((max_bounds[1] - min_bounds[1]) * mm_to_pixels)

    # Calculate the offset to center the model
    x_offset = (width - model_width) // 2
    y_offset = (height - model_height) // 2

    # Iterate through each layer
    for layer_idx in range(num_layers):
        z_level = min_bounds[2] + layer_idx * layer_thickness
        print(f"Slicing at Z = {z_level:.1f} mm (Layer {layer_idx + 1}/{num_layers})")
        
        for i, triangle in enumerate(stl_mesh.vectors):
            # Check if the triangle intersects the current Z level
            z_min, z_max = np.min(triangle[:, 2]), np.max(triangle[:, 2])
            if z_min <= z_level <= z_max:
                # Convert the triangle to 2D points in the XY plane
                xy_points = (triangle[:, :2] - min_bounds[:2]) * mm_to_pixels
                xy_points = np.clip(xy_points, 0, [model_width, model_height])

                # Apply the offset to center the model
                xy_points[:, 0] += x_offset
                xy_points[:, 1] += y_offset

                # Fill the corresponding pixels in the 2D slice
                x_min, y_min = np.min(xy_points, axis=0).astype(int)
                x_max, y_max = np.max(xy_points, axis=0).astype(int)

                slices[layer_idx, y_min:y_max, x_min:x_max] = 1
        print(slices[layer_idx])

    return slices

