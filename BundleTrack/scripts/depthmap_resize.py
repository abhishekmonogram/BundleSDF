import os
import cv2

def resize_depth_maps_with_nearest_neighbor(folder_path, target_height, target_width):
    depth_map_files = [file for file in os.listdir(folder_path) if file.endswith('.png')]

    for depth_map_file in depth_map_files:
        depth_map_path = os.path.join(folder_path, depth_map_file)
        # Load the original depth map (e.g., in grayscale format)
        original_depth_map = cv2.imread(depth_map_path, cv2.IMREAD_UNCHANGED)

        # Resize the depth map using nearest-neighbor interpolation
        resized_depth_map = cv2.resize(original_depth_map, (target_width, target_height), interpolation=cv2.INTER_NEAREST)

        # Save the resized depth map, overwriting the original file
        cv2.imwrite(depth_map_path, resized_depth_map)

if __name__ == "__main__":
    # Replace "/path/to/depth_maps_folder" with the actual folder path containing depth maps
    depth_maps_folder = "/path/to/depth_maps_folder"

    # Define the target resolution
    target_height = 480
    target_width = 777

    # Resize the depth maps using nearest-neighbor interpolation and overwrite the original files
    resize_depth_maps_with_nearest_neighbor(depth_maps_folder, target_height, target_width)
