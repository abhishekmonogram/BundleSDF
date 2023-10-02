# POINT SELECTOR APP

## STEP 1

Set your proper source and target mesh destinations. Source is usally the CT based 3D Model. Target is the Reconstructed mesh

```SOURCE='/home/abhishek/markerless/instant-ngp/cadaverlab-0929-S230867(L)/Femur3DModel.stl'```

```TARGET='/home/abhishek/markerless/instant-ngp/cadaverlab-0929-S230867(L)/cutBone.stl'``` 

The idea behind this tool is to select points first using ```app.py```. Run the following and select 3 points on the mesh

For source mesh:

```python pointselector/app.py --obj_path=${SOURCE} --point_size 50 --save_points_filename 'ct_landmarks.txt'```


For target mesh:

```python pointselector/app.py --obj_path=${TARGET} --point_size 50 --save_points_filename 'reconstruction_landmarks.txt'```

## STEP 2

Once you are done with step 1, then run ```meshaligner.py```. Select the right txt files which contain the source and target landmarks( eg: ct_landmarks.txt and reconstruction_landmarks.txt). The two meshes are aligned using ```vtkLandmarkTransform```. The code outputs a ```transformation.txt``` file that give you the transformation from the source to the target. 


```python pointselector/meshaligner.py --source_points 'ct_landmarks.txt' --target_points 'reconstruction_landmarks.txt' --source_mesh=${SOURCE} --target_mesh=${TARGET}```

## STEP 3

After you get the ```transformation.txt```, to visualise the source and target meshes on top of each other, use the following, 

```python pointselector/transform_and_overlay_meshes.py --source_obj_path=${SOURCE} --target_obj_path=${TARGET} --transformation_matrix 'transformation_matrix.txt'```






