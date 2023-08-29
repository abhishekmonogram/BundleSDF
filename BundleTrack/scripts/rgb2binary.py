import os
import cv2
import numpy as np

def convert_to_binary_mask(rgb_mask):
    binary_mask = np.zeros_like(rgb_mask[:, :, 0], dtype=np.uint8)

    # Check if any channel is non-black (excluding the alpha channel if present)
    non_black_pixels = np.any(rgb_mask[:, :, :3] > 0, axis=-1)

    # Set non-black pixels to white (255)
    binary_mask[non_black_pixels] = 255

    return binary_mask

def process_files_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_list = os.listdir(input_folder)

    for filename in file_list:
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            rgb_mask = cv2.imread(input_path)
            binary_mask = convert_to_binary_mask(rgb_mask)

            cv2.imwrite(output_path, binary_mask)

if __name__ == "__main__":
    input_folder = "/home/abhishek/XMem/workspace/output/masks"
    output_folder = "/home/abhishek/XMem/workspace/output/masks_b"

    process_files_in_folder(input_folder, output_folder)





