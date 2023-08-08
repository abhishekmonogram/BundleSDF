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
            sphere.SetRadius(args.point_size * 0.0005)  # Adjust the radius as needed

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
    # parser.add_argument('--use_gui', type=int, default=1)
    # parser.add_argument('--stride', type=int, default=1, help='interval of frames to run; 1 means using every frame')
    # parser.add_argument('--debug_level', type=int, default=0, help='higher means more logging')
    args = parser.parse_args()

    app = PointPickerApp(args)
