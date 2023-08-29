# POINT SELECTOR APP

## STEP 1

The idea behind this tool is to select points first using ```app.py```. Run the following and select 3 points on the mesh

For source mesh:
```python pointselector/app.py --obj_path '/home/abhishek/BundleSDF/obj_meshes/femur_surgistud.stl' --point_size 50 --save_points_filename 'ct_landmarks.txt'```

For target mesh:
```python pointselector/app.py --obj_path '/home/abhishek/BundleSDF/obj_meshes/femur_wcartilage_surgistud.obj' --point_size 50 --save_points_filename 'reconstruction_landmarks.txt'```

## STEP 2

Once you are done with step 1, then run ```meshaligner.py```. Select the right txt files which contain the source and target landmarks( eg: ct_landmarks.txt and reconstruction_landmarks.txt). The two meshes are aligned using ```vtkLandmarkTransform```. The code outputs a ```transformation.txt``` file that give you the transformation from the source to the target. 

```python pointselector/meshaligner.py --source_points 'ct_landmarks.txt' --target_points 'reconstruction_landmarks.txt' --source_mesh '/home/abhishek/BundleSDF/obj_meshes/femur_surgistud.stl' --target_mesh '/home/abhishek/BundleSDF/obj_meshes/femur_wcartilage_surgistud.obj' ```

## STEP 3

After you get the ```transformation.txt```, to visualise the source and target meshes on top of each other, use the following, 

```python pointselector/transform_and_overlay_meshes.py --source_obj_path '/home/abhishek/BundleSDF/obj_meshes/femur_surgistud.stl' --target_obj_path '/home/abhishek/BundleSDF/obj_meshes/femur_wcartilage_surgistud.obj' --transformation_matrix 'transformation_matrix.txt'  ```






