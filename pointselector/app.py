import vtk
import argparse

class PointPickerApp:
    def __init__(self, args):
        # Load OBJ or STL file
        if args.obj_path.lower().endswith('.obj'):
            reader = vtk.vtkOBJReader()
        elif args.obj_path.lower().endswith('.stl'):
            reader = vtk.vtkSTLReader()
        else:
            raise ValueError("Unsupported file format. Only OBJ and STL files are supported.")

        reader.SetFileName(args.obj_path)
        reader.Update()

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Get the bounds of the loaded model
        bounds = reader.GetOutput().GetBounds()
        x_range = bounds[1] - bounds[0]
        y_range = bounds[3] - bounds[2]
        z_range = bounds[5] - bounds[4]
        max_range = max(x_range, y_range, z_range)

        # Create a renderer
        renderer = vtk.vtkRenderer()

        # Create a render window
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)

        # Create a render window interactor
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)

        # Set the size of the render window and interactor
        render_window.SetSize(args.ui_window_width, args.ui_window_height)
        render_window_interactor.SetSize(args.ui_window_width, args.ui_window_height)

        # Add the actor to the renderer
        renderer.AddActor(actor)

        # Enable picking
        picker = vtk.vtkPointPicker()
        render_window_interactor.SetPicker(picker)

        # Create a list to store picked points
        self.picked_points = []

        def pick_callback(obj, event):
            click_pos = render_window_interactor.GetEventPosition()

            # Use vtkWorldPointPicker to pick points in world coordinates
            world_picker = vtk.vtkWorldPointPicker()
            world_picker.Pick(click_pos[0], click_pos[1], 0, renderer)

            # Get the picked point in world coordinates
            picked_point = world_picker.GetPickPosition()
            print(f"Picked Point is visible at co-ordinate: {picked_point}")

            # Create a sphere source for the picked point
            sphere = vtk.vtkSphereSource()
            sphere.SetCenter(picked_point)
            sphere.SetRadius(max_range * args.point_size * 0.0005)  # Scale by max range

            sphere_mapper = vtk.vtkPolyDataMapper()
            sphere_mapper.SetInputConnection(sphere.GetOutputPort())

            sphere_actor = vtk.vtkActor()
            sphere_actor.SetMapper(sphere_mapper)
            renderer.AddActor(sphere_actor)

            render_window.Render()

        # Connect the pick callback
        render_window_interactor.AddObserver("RightButtonPressEvent", pick_callback)

        # Add object's axis for visualization
        axes = vtk.vtkAxesActor()
        axes.AxisLabelsOff()  # Turn off axis labels
        axes.SetTotalLength(max_range , max_range , max_range )  # Adjust the axis size
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
        output_filename = args.save_points_filename
        with open(output_filename, "w") as f:
            for point in self.picked_points:
                f.write(f"{point[0]} {point[1]} {point[2]}\n")
        print("Picked points saved to", output_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--obj_path', type=str, default="/home/abhishek/BundleSDF/obj_meshes/highres_7.obj", help="Select the path to the obj file")
    parser.add_argument('--save_points_filename', type=str, default="ct_landmarks.txt", help =" ct_landmarks.txt / reconstruction_landmarks.txt")
    parser.add_argument('--point_size', type=int, default=5)
    parser.add_argument('--ui_window_width', type=int, default=5120)
    parser.add_argument('--ui_window_height', type=int, default=2880)
    
    args = parser.parse_args()

    app = PointPickerApp(args)
