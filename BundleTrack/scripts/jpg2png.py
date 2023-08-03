import os
import cv2


# path to the folder containing your JPEG images
input_folder = '/home/abhishek/BundleSDF/femur_3005/images'

# List all files with '.jpg' extension in the input folder
jpg_files = [file for file in os.listdir(input_folder) if file.lower().endswith('.jpg')]

# Convert each JPEG image to PNG and overwrite the original images
for jpg_file in jpg_files:
    jpg_path = os.path.join(input_folder, jpg_file)
    png_file = os.path.splitext(jpg_file)[0] + '.png'
    png_path = os.path.join(input_folder, png_file)

    # Read the JPEG image
    image = cv2.imread(jpg_path)

    # Save the image as PNG, it will overwrite the original JPEG image
    cv2.imwrite(png_path, image)

print("Conversion completed successfully!") 
