import vtk
import argparse
import numpy as np

class MeshAligner:
    def __init__(self, source_points, target_points, source_mesh_path, target_mesh_path):
        self.source_points = np.array(source_points)
        self.target_points = np.array(target_points)

        self.source_reader = vtk.vtkSTLReader()  # Use vtkOBJReader for OBJ files
        self.source_reader.SetFileName(source_mesh_path)
        self.source_reader.Update()

        self.target_reader = vtk.vtkOBJReader()  # Use vtkOBJReader for OBJ files
        self.target_reader.SetFileName(target_mesh_path)
        self.target_reader.Update()

        # Create landmark transform based on the source and target points
        landmark_transform = vtk.vtkLandmarkTransform()
        source_landmarks = vtk.vtkPoints()
        target_landmarks = vtk.vtkPoints()

        for i in range(3):
            source_landmarks.InsertNextPoint(self.source_points[i])
            target_landmarks.InsertNextPoint(self.target_points[i])

        landmark_transform.SetSourceLandmarks(source_landmarks)
        landmark_transform.SetTargetLandmarks(target_landmarks)
        landmark_transform.Update()

        # Apply the transformation to the source mesh
        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputConnection(self.source_reader.GetOutputPort())
        transform_filter.SetTransform(landmark_transform)

        # Create mapper and actor for the transformed source mesh
        transformed_mapper = vtk.vtkPolyDataMapper()
        transformed_mapper.SetInputConnection(transform_filter.GetOutputPort())
        transformed_actor = vtk.vtkActor()
        transformed_actor.SetMapper(transformed_mapper)

        # Visualize both meshes
        renderer = vtk.vtkRenderer()
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)

        renderer.AddActor(self.create_outline_actor(self.target_reader.GetOutput()))
        renderer.AddActor(transformed_actor)

        renderer.GetActiveCamera().Azimuth(30)
        renderer.GetActiveCamera().Elevation(30)
        renderer.ResetCamera()

        render_window.Render()
        render_window_interactor.Start()

        # Get the transformation matrix and save to a file
        transformation_matrix = landmark_transform.GetMatrix()
        self.save_transformation_matrix(transformation_matrix)

    def create_outline_actor(self, input_data):
        outline = vtk.vtkOutlineFilter()
        outline.SetInputData(input_data)
        outline_mapper = vtk.vtkPolyDataMapper()
        outline_mapper.SetInputConnection(outline.GetOutputPort())
        outline_actor = vtk.vtkActor()
        outline_actor.SetMapper(outline_mapper)
        outline_actor.GetProperty().SetColor(0, 0, 0)
        return outline_actor

    def save_transformation_matrix(self, matrix):
        with open("transformation_matrix.txt", "w") as f:
            for i in range(4):
                row = [matrix.GetElement(i, j) for j in range(4)]
                f.write(" ".join(map(str, row)) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_points', type=str, default="ct_landmarks.txt", help="Path to the source points text file")
    parser.add_argument('--target_points', type=str, default="reconstruction_landmarks.txt", help="Path to the target points text file")
    parser.add_argument('--source_mesh', type=str, default="/home/abhishek/BundleSDF/obj_meshes/femur_surgistud.stl", help="Path to the source STL file")
    parser.add_argument('--target_mesh', type=str, default="obj_meshes/femur_wcartilage_surgistud.obj", help="Path to the target STL file")
    args = parser.parse_args()

    # Load source points from file
    source_points = []
    with open(args.source_points, 'r') as f:
        for line in f:
            coords = line.strip().split()
            if len(coords) == 3:
                source_points.append([float(coords[0]), float(coords[1]), float(coords[2])])

    # Load target points from file
    target_points = []
    with open(args.target_points, 'r') as f:
        for line in f:
            coords = line.strip().split()
            if len(coords) == 3:
                target_points.append([float(coords[0]), float(coords[1]), float(coords[2])])

    if len(source_points) != 3 or len(target_points) != 3:
        print("Error: Please provide 3 source and 3 target points in the text files.")
    else:
        aligner = MeshAligner(source_points, target_points, args.source_mesh, args.target_mesh)
