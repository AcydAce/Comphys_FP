import math
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

animation = None  # Global variable to store the animation object
x_values = []  # List to store x-coordinate values of the trajectory
y_values = []  # List to store y-coordinate values of the trajectory

def calculate_trajectory():
    global animation, x_values, y_values  # Use the global variables
    x_values = []
    y_values = []

    try:
        initial_velocity = float(velocity_entry.get())
        launch_angle = math.radians(float(angle_entry.get()))
        initial_height = float(height_entry.get())
        wind_speed = float(wind_speed_entry.get())
        drag_coefficient = float(drag_coefficient_entry.get())
        bomb_mass = float(bomb_mass_entry.get())
        air_density = float(air_density_entry.get())

        time_step = 0.01  # Time step for simulation
        g = 9.8  # Acceleration due to gravity

        t = 0
        while True:
            
            # horizontal motion equation + wind speed
            # vertical motion equation
            x = max(0, (initial_velocity * math.cos(launch_angle) + wind_speed) * t)
            y = max(0, (initial_velocity * math.sin(launch_angle) - (0.5 * g * (t ** 2))) + initial_height)

            if y >= 0:
                

                velocity = math.sqrt((initial_velocity * math.cos(launch_angle) - wind_speed) ** 2 +
                                     (initial_velocity * math.sin(launch_angle)) ** 2)

                # Air resistance equation
                drag_force = 0.5 * drag_coefficient * air_density * velocity ** 2
                # gravitational force equation
                gravitational_force = bomb_mass * g
                # acceleration
                acceleration = (gravitational_force - drag_force) / bomb_mass
                horizontal_velocity = (initial_velocity * math.cos(launch_angle) - wind_speed)
                vertical_velocity = initial_velocity * math.sin(launch_angle) - acceleration * t
                x = x + horizontal_velocity * t
                y = y + vertical_velocity * t - (0.5 * acceleration * t ** 2)

                if y >= 0:
                    x_values.append(x)
                    y_values.append(y)
                    t += time_step
                else:
                    final_t = (-vertical_velocity + math.sqrt(vertical_velocity**2 - 2 * (-0.5 * acceleration) * y)) / (-0.5 * acceleration)
                    final_x = x + horizontal_velocity * final_t
                    x_values.append(final_x)
                    y_values.append(0)
                    break

        if animation is not None:
            animation.event_source.stop()

        # Set up the plot
        fig, ax = plt.subplots()
        scatter = ax.scatter([], [])
        ax.set_xlabel("Horizontal Distance (m)")
        ax.set_ylabel("Vertical Distance (m)")
        ax.set_title("Bomb Drop Trajectory")
        ax.grid(True)

        # Adjust axis limits
        ax.set_xlim(0, math.ceil(max(x_values)))
        ax.set_ylim(0, math.ceil(max(y_values)))

        def update(frame):
            if frame < len(x_values):
                scatter.set_offsets([x_values[frame], y_values[frame]])
            return scatter,

        interval = 1  # 1 milliseconds
        frames = len(x_values)

        # Create the animation
        animation = FuncAnimation(fig, update, frames=frames, interval=interval, blit=True)

        # Display the plot
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except ValueError:
        output_label.config(text="Invalid input. Please enter numeric values.")

def update_simulation():
    if animation is not None:
        animation.event_source.stop()  # Stop the current animation if it's running
    calculate_trajectory()  # Run the simulation with the updated inputs

# Create the GUI window
window = tk.Tk()
window.title("Bomb Drop Trajectory Simulator")

# Create input fields
velocity_label = tk.Label(window, text="Initial Velocity (m/s):")
velocity_label.pack()
velocity_entry = tk.Entry(window)
velocity_entry.pack()

angle_label = tk.Label(window, text="Launch Angle (degrees):")
angle_label.pack()
angle_entry = tk.Entry(window)
angle_entry.pack()

height_label = tk.Label(window, text="Initial Height (meters):")
height_label.pack()
height_entry = tk.Entry(window)
height_entry.pack()

wind_speed_label = tk.Label(window, text="Wind Speed (m/s):")
wind_speed_label.pack()
wind_speed_entry = tk.Entry(window)
wind_speed_entry.pack()

drag_coefficient_label = tk.Label(window, text="Drag Coefficient (0.47):")
drag_coefficient_label.pack()
drag_coefficient_entry = tk.Entry(window)
drag_coefficient_entry.pack()

bomb_mass_label = tk.Label(window, text="Bomb Mass (kg):")
bomb_mass_label.pack()
bomb_mass_entry = tk.Entry(window)
bomb_mass_entry.pack()

air_density_label = tk.Label(window, text="Air Density (kg/m^3):")
air_density_label.pack()
air_density_entry = tk.Entry(window)
air_density_entry.pack()

# Create a button to calculate the trajectory
calculate_button = tk.Button(window, text="Calculate", command=calculate_trajectory)
calculate_button.pack()

# Create a button to update the simulation
update_button = tk.Button(window, text="Update Simulation", command=update_simulation)
update_button.pack()

# Start the main GUI loop
window.mainloop()