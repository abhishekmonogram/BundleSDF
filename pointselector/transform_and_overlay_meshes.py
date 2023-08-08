import vtk
import numpy as np
import argparse

def load_mesh(file_path):
    if file_path.lower().endswith('.obj'):
            reader = vtk.vtkOBJReader()
    elif file_path.lower().endswith('.stl'):
        reader = vtk.vtkSTLReader()
    else:
        raise ValueError("Unsupported file format. Only OBJ and STL files are supported.")
    
    reader.SetFileName(file_path)
    reader.Update()
    return reader.GetOutput()

def apply_transformation(matrix, input_mesh):
    transform = vtk.vtkTransform()
    transform.SetMatrix(matrix.flatten())

    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(input_mesh)
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    return transform_filter.GetOutput()

def create_outline_actor(input_data):
    outline = vtk.vtkOutlineFilter()
    outline.SetInputData(input_data)
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(1, 1, 1)
    return outline_actor

def create_mesh_actor(input_data,color,opacity=1):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(input_data)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)  # Set mesh color to gray
    actor.GetProperty().SetOpacity(opacity) 
    return actor

def main(args):
    # Load the two mesh files
    source_mesh = load_mesh(args.source_obj_path)
    target_mesh = load_mesh(args.target_obj_path)

    # Apply a transformation matrix to the source mesh
    transformation_matrix = np.loadtxt(args.transformation_matrix)
    transformed_mesh = apply_transformation(transformation_matrix, source_mesh)

    # Create a renderer for visualization
    renderer = vtk.vtkRenderer()

    # Create a render window and add the renderer
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # Set the size of the render window
    render_window.SetSize(args.ui_window_width, args.ui_window_height) 

     # Create a render window interactor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Add actors to the renderer
    renderer.AddActor(create_outline_actor(target_mesh))
    renderer.AddActor(create_outline_actor(transformed_mesh))
    renderer.AddActor(create_mesh_actor(target_mesh, color=(1, 0, 0)))
    renderer.AddActor(create_mesh_actor(transformed_mesh, color=(0, 1, 0))) 

    # Set up camera
    renderer.GetActiveCamera().Azimuth(30)
    renderer.GetActiveCamera().Elevation(30)
    renderer.ResetCamera()

    # Initialize and start the render loop
    render_window.Render()
    render_window_interactor.Start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_obj_path', type=str, default="/home/abhishek/BundleSDF/obj_meshes/femur_surgistud.stl", help="Select the path to the obj/stl file")
    parser.add_argument('--target_obj_path', type=str, default="/home/abhishek/BundleSDF/obj_meshes/femur_wcartilage_surgistud.obj", help="Select the path to the obj/stl file")
    parser.add_argument('--transformation_matrix', type=str, default="transformation_matrix.txt")
    parser.add_argument('--point_size', type=int, default=5)
    parser.add_argument('--ui_window_width', type=int, default=5120)
    parser.add_argument('--ui_window_height', type=int, default=2880)
    
    args = parser.parse_args()
    main(args)
