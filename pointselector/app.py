import vtk
import argparse

class PointPickerApp:
    def __init__(self, args):
        # Load OBJ file
        reader = vtk.vtkOBJReader()
        reader.SetFileName(args.obj_path)
        reader.Update()

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Create a renderer
        renderer = vtk.vtkRenderer()

        # Create a render window
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)

        # Create a render window interactor
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)

        # Set the size of the render window and interactor
        render_window.SetSize(5120, 2880)
        render_window_interactor.SetSize(5120, 2880)

        # Add the actor to the renderer
        renderer.AddActor(actor)

        # Enable picking
        picker = vtk.vtkPointPicker()
        render_window_interactor.SetPicker(picker)

        # Create a list to store picked points
        self.picked_points = []

        # Set the point size as a variable
        point_size = 5

        def pick_callback(obj, event):
            click_pos = render_window_interactor.GetEventPosition()
            picker.Pick(click_pos[0], click_pos[1], 0, renderer)
            picked_point = picker.GetPickPosition()

            # Object frame of reference
            self.picked_points.append(picked_point)

            # Update the visualization to display picked points
            points = vtk.vtkPoints()
            vertices = vtk.vtkCellArray()

            for point in self.picked_points:
                id = points.InsertNextPoint(point)
                vertices.InsertNextCell(1)
                vertices.InsertCellPoint(id)

            point_cloud = vtk.vtkPolyData()
            point_cloud.SetPoints(points)
            point_cloud.SetVerts(vertices)

            point_mapper = vtk.vtkPolyDataMapper()
            point_mapper.SetInputData(point_cloud)

            point_actor = vtk.vtkActor()
            point_actor.SetMapper(point_mapper)
            point_actor.GetProperty().SetPointSize(point_size)  # Set point size

            renderer.AddActor(point_actor)
            
            print("Picked Point:", picked_point)
            render_window.Render()

            # for point in self.picked_points:
            #     sphere = vtk.vtkSphereSource()
            #     sphere.SetCenter(point)
            #     sphere.SetRadius(point_size * 0.001)  # Adjust the radius as needed

            #     sphere_mapper = vtk.vtkPolyDataMapper()
            #     sphere_mapper.SetInputConnection(sphere.GetOutputPort())

            #     sphere_actor = vtk.vtkActor()
            #     sphere_actor.SetMapper(sphere_mapper)
            #     renderer.AddActor(sphere_actor)

            #     render_window.Render()

        # Connect the pick callback
        render_window_interactor.AddObserver("MiddleButtonPressEvent", pick_callback)

        # Add object's axis for visualization
        axes = vtk.vtkAxesActor()
        renderer.AddActor(axes)

        # Set up camera
        renderer.GetActiveCamera().Azimuth(30)
        renderer.GetActiveCamera().Elevation(30)
        renderer.ResetCamera()

        # Enable interaction styles for panning and rotating
        interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        render_window_interactor.SetInteractorStyle(interactor_style)

        # Initialize and start the render loop
        render_window.Render()
        render_window_interactor.Start()

        # Save picked points to a text file
        output_filename = "picked_points.txt"
        with open(output_filename, "w") as f:
            for point in self.picked_points:
                f.write(f"{point[0]} {point[1]} {point[2]}\n")
        print("Picked points saved to", output_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--obj_path', type=str, default="/home/abhishek/BundleSDF/obj_meshes/highres_7.obj", help="Select the path to the obj file")
    # parser.add_argument('--video_dir', type=str, default="/home/digitalstorm/BundleSDF/femur_3005_truncated")
    # parser.add_argument('--out_folder', type=str, default="/home/digitalstorm/BundleSDF/femur_3005_truncated/output_3")
    # parser.add_argument('--use_segmenter', type=int, default=0)
    # parser.add_argument('--use_gui', type=int, default=1)
    # parser.add_argument('--stride', type=int, default=1, help='interval of frames to run; 1 means using every frame')
    # parser.add_argument('--debug_level', type=int, default=0, help='higher means more logging')
    args = parser.parse_args()

    app = PointPickerApp(args)
