import os

def rename_images(directory):
    files = os.listdir(directory)
    image_files = [file for file in files if file.endswith('.png')]
    image_files.sort()

    for i, filename in enumerate(image_files, start=0):
        new_filename = f'{i:07d}.png'
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)
        print(f'Renamed {filename} to {new_filename}')

if __name__ == "__main__":
    directory_path = "/home/abhishek/BundleSDF/femur_3005/depth"  # Replace this with the actual directory path
    rename_images(directory_path)
