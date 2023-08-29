import cv2
import os

# Paths to your mask and RGB image folders
mask_folder = "/home/abhishek/XMem/workspace/output/masks_b/"
rgb_folder = "/home/abhishek/XMem/workspace/output/old_images_full"
output_folder = "/home/abhishek/XMem/workspace/output/images"


# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all files in both folders
mask_files = os.listdir(mask_folder)
rgb_files = os.listdir(rgb_folder)

count =0 
# Iterate through each mask file
for mask_file in mask_files:
    if mask_file.endswith(".png") or mask_file.endswith(".jpg"):
        # Construct paths for mask and corresponding RGB image
        mask_path = os.path.join(mask_folder, mask_file)
        rgb_file = mask_file.replace(".png", ".jpg")  # Assuming naming convention "_mask" in mask filenames
        rgb_path = os.path.join(rgb_folder, rgb_file)

        # Load the mask image using OpenCV
        mask_img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        # Load the RGB image using OpenCV
        rgb_img = cv2.imread(rgb_path)

        # Create a new alpha channel by using the mask
        alpha_channel = mask_img

        # Add the alpha channel to the RGB image
        rgba_img = cv2.merge((rgb_img[:, :, 0], rgb_img[:, :, 1], rgb_img[:, :, 2], alpha_channel))

        # Save the resulting image with added alpha channel as PNG to the output folder
        output_path = os.path.join(output_folder, mask_file)
        cv2.imwrite(output_path, rgba_img)
        count+=1
        print(f'{count=}')

print("Images with alpha channel appended saved to the output folder.")

