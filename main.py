import math
import tkinter as tk
import os
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
        time_step = 0.0001  # Time step for simulation
        g = 9.8  # Acceleration due to gravity

        t = 0
        while True:
<<<<<<< HEAD
            # Horizontal motion equation + wind speed
=======
            
            # horizontal motion equation + wind speed
            # vertical motion equation
>>>>>>> 987e47ffbdc1c6ebcf017bc4aea1d9f0bc0fa9c6
            x = max(0, (initial_velocity * math.cos(launch_angle) + wind_speed) * t)
            # Vertical motion equation
            y = max(0, (initial_velocity * math.sin(launch_angle) - (0.5 * g * (t ** 2))) + initial_height)
            # Calculate weight factor based on current height
            weight_factor = bomb_mass * (g / (1 + (y / 6371000))**2)
            if y >= 0:
                

                velocity = math.sqrt((initial_velocity * math.cos(launch_angle) - wind_speed) ** 2 +
                                     (initial_velocity * math.sin(launch_angle)) ** 2)

                # Air resistance equation
<<<<<<< HEAD
                drag_force = 0.5 * drag_coefficient * (air_density ** 100) * velocity ** 2
                # Gravitational force equation with weight factor
                gravitational_force = bomb_mass * g * weight_factor
                # Acceleration
=======
                drag_force = 0.5 * drag_coefficient * air_density * velocity ** 2
                # gravitational force equation
                gravitational_force = bomb_mass * g
                # acceleration
>>>>>>> 987e47ffbdc1c6ebcf017bc4aea1d9f0bc0fa9c6
                acceleration = (gravitational_force - drag_force) / bomb_mass
                horizontal_velocity = ((initial_velocity * math.cos(launch_angle) + wind_speed ) / weight_factor)
                vertical_velocity = initial_velocity * math.sin(launch_angle) - acceleration * t
                x = x + horizontal_velocity * t
                y = y + vertical_velocity * t - (0.5 * acceleration * t ** 2)
                
                if y >= 0:
                    x_values.append(x)
                    y_values.append(y)
                    t += time_step
                else:
                    final_t = (-vertical_velocity + math.sqrt(vertical_velocity ** 2 - 2 * (-0.5 * acceleration) * y)) / (-0.5 * acceleration)
                    final_x = x + horizontal_velocity * final_t
                    x_values.append(final_x)
                    y_values.append(0)
                    break

        if animation is not None:
            animation.event_source.stop()

        # Set up the plot
        fig, ax = plt.subplots(figsize=(8.14,5))
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
        canvas.get_tk_widget().place(x = 10, y = 400)

        # --------------- DISPLAY RESULTS -----------------------

        finalDTitle = tk.Label(window, text="Position of Impact:", font=('Comic Sans MS', 20))
        finalDTitle.place(x = 900, y = 600)            

        finalDistance_label = tk.Label(window, text=f"{round(final_x, 2)} meters from release", font=('Comic Sans MS', 17))
        finalDistance_label.place(x = 900, y = 700)

    except ValueError:
        errorDis()

# --------------- RESET PROGRAM ------------------------------
def restart():
    window.destroy() #destroy current window
    os.startfile("main.py") #reload the py file
    # --------- MAC VERSION ---------------
    #python = sys.executable
    #subprocess.Popen([python, "main.py"])
    # -------------------------------------

# ---------------- MINI ERROR POP UP ----------------------------
def des_pop():
    pop.destroy()

def errorDis():
    global pop
    pop = tk.Toplevel(window)
    pop.title("Error")
    winPosx = window.winfo_x()
    winPosy = window.winfo_y()
    pop.geometry("+%d+%d" %(winPosx+330,winPosy+300))
    
    pop_label = tk.Label(pop, text = "There are incorrect inputs, please try again!", font=('Comic Sans MS', 20))
    pop_label.pack(pady=10)

    ok_button = tk.Button(pop, text = "Ok", font=('Comic Sans MS', 15), command=des_pop)
    ok_button.pack(pady=10)

# ------------------ AutoFill Commands-------------------------

def autoFill():
    angle_entry.insert(0, 0)
    drag_coefficient_entry.insert(0, .47)
    air_density_entry.insert(0, .4)

def fill_fatMan():
    bomb_mass_entry.insert(0, 370)

def fill_FAB():
    bomb_mass_entry.insert(0, 300)

def fill_PKB():
    bomb_mass_entry.insert(0, 540)

# ------------------ CLEAR -------------------------

def clear():
    velocity_entry.delete(0, tk.END)
    angle_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    wind_speed_entry.delete(0, tk.END)
    drag_coefficient_entry.delete(0, tk.END)
    bomb_mass_entry.delete(0, tk.END)
    air_density_entry.delete(0, tk.END)

# -------------------- Create the GUI window -----------------------
window = tk.Tk()
window.title("Bomb Drop Trajectory Simulator")
window.geometry("1280x900")

# --------------------- Create input fields ------------------------
velocity_label = tk.Label(window, text="Initial Velocity (m/s):", font=('Comic Sans MS', 20))
velocity_label.place(x = 10, y = 5)
velocity_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20))
velocity_entry.place(x = 340, y = 10)

angle_label = tk.Label(window, text="Launch Angle (degrees):", font=('Comic Sans MS', 20))
angle_label.place(x = 10, y = 60)
angle_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20))
angle_entry.place(x = 340, y = 65)

height_label = tk.Label(window, text="Initial Height (meters):", font=('Comic Sans MS', 20))
height_label.place(x = 10, y = 115)
height_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20))
height_entry.place(x = 340, y = 120)

wind_speed_label = tk.Label(window, text="Wind Speed (m/s):", font=('Comic Sans MS', 20))
wind_speed_label.place(x = 10, y = 170)
wind_speed_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20))
wind_speed_entry.place(x = 340, y = 175)

<<<<<<< HEAD
drag_coefficient_label = tk.Label(window, text="Drag Coefficient (Cd):", font=('Comic Sans MS', 20))
drag_coefficient_label.place(x = 10, y = 225)
drag_coefficient_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20))
drag_coefficient_entry.place(x = 340, y = 230)
=======
drag_coefficient_label = tk.Label(window, text="Drag Coefficient (0.47):")
drag_coefficient_label.pack()
drag_coefficient_entry = tk.Entry(window)
drag_coefficient_entry.pack()
>>>>>>> 987e47ffbdc1c6ebcf017bc4aea1d9f0bc0fa9c6

bomb_mass_label = tk.Label(window, text="Bomb Mass (kg):", font=('Comic Sans MS', 20))
bomb_mass_label.place(x = 10, y = 280)
bomb_mass_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20))
bomb_mass_entry.place(x = 340, y = 285)

air_density_label = tk.Label(window, text="Air Density (kg/m^3):", font=('Comic Sans MS', 20))
air_density_label.place(x = 10, y = 335)
air_density_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20))
air_density_entry.place(x = 340, y = 340)

#Example bomb label
air_density_label = tk.Label(window, text="Example Bomb \nData:", font=('Comic Sans MS', 20))
air_density_label.place(x = 865, y = 20)

# ------------------ MAIN BUTTONS ------------------------------

# Create a button to calculate the trajectory
calculate_button = tk.Button(window, text="Simulate", command=calculate_trajectory, font=('Comic Sans MS', 15), padx=7, bg='#a9e8ba')
calculate_button.place(x = 1100, y = 45)

# Create a button to update the simulation
update_button = tk.Button(window, text="Reset", command=restart, font=('Comic Sans MS', 15), padx=20, bg='#e8a9a9')
update_button.place(x = 1100, y = 120)

# Create a button to clear in entry box
clear_button = tk.Button(window, text="Clear", command=clear, font=('Comic Sans MS', 15), padx=22, bg='#a9cee8')
clear_button.place(x = 1100, y = 195)

# Create a button to autofill in entry box
clear_button = tk.Button(window, text="Autofill", command=autoFill, font=('Comic Sans MS', 15), padx=12, bg='#d2a9e8')
clear_button.place(x = 1100, y = 270)

# --------------- EXAMPLE BUTTONS ------------------------------

# Create a button to fill fat man data
fatMan_button = tk.Button(window, text="Fat Man", command=fill_fatMan, font=('Comic Sans MS', 15), padx=38, bg='#e3e8a9')
fatMan_button.place(x = 870, y = 120)

# Create a button to fill fab data
FAB_button = tk.Button(window, text="FAB-500", command=fill_FAB, font=('Comic Sans MS', 15), padx=33, bg='#e3e8a9')
FAB_button.place(x = 870, y = 195)

# Create a button to fill pkb
PKB_button = tk.Button(window, text="PKB-500U Drel", command=fill_PKB, font=('Comic Sans MS', 15), padx=4, bg='#e3e8a9')
PKB_button.place(x = 870, y = 270)

# Start the main GUI loop
window.mainloop()