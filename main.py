import math
import tkinter as tk
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


animation = None  # Global variable to store the animation object
x_values = []  # List to store x-coordinate values of the trajectory
y_values = []  # List to store y-coordinate values of the trajectory

def simulate_trajectory():
    global animation, x_values, y_values  # Use the global variables
    x_values = []
    y_values = []

    try:
        initial_velocity = float(velocity_entry.get())
        launch_angle = math.radians(float(angle_entry.get()))
        initial_height = float(height_entry.get())
        wind_speed = float(wind_speed_entry.get())
        drag_coefficient = 0.47
        bomb_mass = float(bomb_mass_entry.get())
        air_density = 0.9
        time_step = 0.0001  # Time step for simulation
        g = 9.8  # Acceleration due to gravity

        t = 0
        while True:
            # Horizontal motion equation + wind speed
            x = max(0, (initial_velocity * math.cos(launch_angle) + wind_speed) * t)
            # Vertical motion equation
            y = max(0, (initial_velocity * math.sin(launch_angle) - (0.5 * g * (t ** 2))) + initial_height)
            # Calculate weight factor based on current height
            weight_factor = bomb_mass * (g / (1 + (y / 6371000))**2)
            if y >= 0:
                velocity = math.sqrt((initial_velocity * math.cos(launch_angle) - wind_speed) ** 2 +
                                     (initial_velocity * math.sin(launch_angle)) ** 2)

                # Air resistance equation
                drag_force = 0.5 * drag_coefficient * (air_density ** 100) * velocity ** 2
                # Gravitational force equation with weight factor
                gravitational_force = bomb_mass * g * weight_factor
                # Acceleration
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
        fig, ax = plt.subplots(figsize=(8.14,5), facecolor='#464757')
        scatter = ax.scatter([], [], color='#f7a49e')
        ax.set_xlabel("Horizontal Distance (m)")
        ax.set_ylabel("Vertical Distance (m)")
        ax.set_title("Bomb Drop Trajectory", color='white')

        ax.set_facecolor('#464757')

        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')

        ax.tick_params(axis='x', colors='white')    
        ax.tick_params(axis='y', colors='white')

        ax.spines['left'].set_color('white')    
        ax.spines['top'].set_color('white')  
        ax.spines['bottom'].set_color('white')
        ax.spines['right'].set_color('white')

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

        finalDTitle = tk.Label(window, text="Position of Impact:", font=('Comic Sans MS', 20), bg='#464757', fg='white')
        finalDTitle.place(x = 900, y = 600)

        finalDistance_label = tk.Label(window, text=f"{round(final_x, 2)} meters from release                 ", font=('Comic Sans MS', 17), bg='#464757', fg='white')
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
    pop.grab_release()
    pop.destroy()

def errorDis():
    global pop
    
    pop = tk.Toplevel(window)
    pop.title("Error")
    winPosx = window.winfo_x()
    winPosy = window.winfo_y()
    pop.geometry("+%d+%d" %(winPosx+330,winPosy+300))
    pop.config(bg='#464757')
    
    pop_label = tk.Label(pop, text = "There are incorrect inputs, please try again!", font=('Comic Sans MS', 20), bg='#464757', fg='white')
    pop_label.pack(pady=10)
    pop.grab_set()

    ok_button = tk.Button(pop, text = "Ok", font=('Comic Sans MS', 15), command=des_pop)
    ok_button.pack(pady=10)

# ------------------ AutoFill Commands-------------------------

def autoFill():
    angle_entry.insert(0, 0)

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
    bomb_mass_entry.delete(0, tk.END)

# ----------------- INFO BAR HOVER COMMANDS ----------------------

# ======= Main Input Labels ======
def bHover_inVelocity(e):
    velocity_label["bg"] = "#7b7d96"
    status_bar.config(text="The velocity at which the bomb is released.\n (This variable does not accept negative values)")
def bHover_inVelocity_leave(e):
    velocity_label["bg"] = "#464757"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_height(e):
    height_label["bg"] = "#7b7d96"
    status_bar.config(text="The height at which the bomb is dropped.\n(This variable does not accept negative values)")
def bHover_height_leave(e):
    height_label["bg"] = "#464757"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_launchAng(e):
    angle_label["bg"] = "#7b7d96"
    status_bar.config(text="The angle at which the bomb is dropped.\n(0° default for bomb drop)")
def bHover_launchAng_leave(e):
    angle_label["bg"] = "#464757"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_windSpeed(e):
    wind_speed_label["bg"] = "#7b7d96"
    status_bar.config(text="The speed of the wind that effects the trajectory of the bomb.\n (Put a positive value to add the wind in the direction of where the bomb is dropped)\n(Put a negative value to add wind against the direction of where the bomb is dropped)")
def bHover_windSpeed_leave(e):
    wind_speed_label["bg"] = "#464757"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_mass(e):
    bomb_mass_label["bg"] = "#7b7d96"
    status_bar.config(text="The weight of the bomb that is being dropped.\n(This variable does not accept negative values)")
def bHover_mass_leave(e):
    bomb_mass_label["bg"] = "#464757"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_exampleBomb(e):
    exampleBomb_label["bg"] = "#7b7d96"
    status_bar.config(text="A mini-list of example data of different existing bombs. \nPress the buttons to autofill entry data.")
def bHover_exampleBomb_leave(e):
    exampleBomb_label["bg"] = "#464757"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")


# ====== Buttons ========
def bHover_fatMan(e):
    fatMan_button["bg"] = "#eff2c9"
    status_bar.config(text="The nuclear bomb that the United States detonated over the \nJapanese city of Nagasaki.\nPress to autofill entry data.")
def bHover_fatMan_leave(e):
    fatMan_button["bg"] = "#e3e8a9"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_FAB(e):
    FAB_button["bg"] = "#eff2c9"
    status_bar.config(text="An air-dropped bomb with a high-explosive warhead, primarily used by \nthe Russian Aerospace Forces.\nPress to autofill entry data.")
def bHover_FAB_leave(e):
    FAB_button["bg"] = "#e3e8a9"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_PBK(e):
    PBK_button["bg"] = "#eff2c9"
    status_bar.config(text="An inertial and GLONASS-guided cluster glide bomb developed by \nthe Russian Federation.\nPress to autofill entry data.")
def bHover_PBK_leave(e):
    PBK_button["bg"] = "#e3e8a9"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")


def bHover_sim(e):
    simulate_button["bg"] = "#cce8d4"
    status_bar.config(text="Simulate button. \nPress to simulate after filling all entry datas correctly.")
def bHover_sim_leave(e):
    simulate_button["bg"] = "#a9e8ba"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_restart(e):
    restart_button["bg"] = "#ffd9d9"
    status_bar.config(text="Reset button. \nPress to reset the app. The source code requires change if user \nis on mac or other platforms. Some privilages might need to be edited too.")
def bHover_restart_leave(e):
    restart_button["bg"] = "#e8a9a9"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_clear(e):
    clear_button["bg"] = "#d6eeff"
    status_bar.config(text="Clear button. \nPress to clear the all of the entry boxes.")
def bHover_clear_leave(e):
    clear_button["bg"] = "#a9cee8"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

def bHover_autoFill(e):
    autoFill_button["bg"] = "#eed4fc"
    status_bar.config(text="Autofill button. \nPress to fill the Launch Angle entry automatically.")
def bHover_autoFill_leave(e):
    autoFill_button["bg"] = "#d2a9e8"
    status_bar.config(text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.")

# -------------------- Create the GUI window -----------------------
window = tk.Tk()
window.title("Bomb Drop Trajectory Simulator")
window.geometry("1280x900")
window.config(bg='#464757')

# --------------------- Create input fields ------------------------
velocity_label = tk.Label(window, text="Initial Velocity (m/s):", font=('Comic Sans MS', 20), bg='#464757', fg='white')
velocity_label.place(x = 10, y = 5)
velocity_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20), bg='#464757', fg='white', insertbackground="white")
velocity_entry.place(x = 340, y = 10)

angle_label = tk.Label(window, text="Launch Angle (degrees):", font=('Comic Sans MS', 20), bg='#464757', fg='white')
angle_label.place(x = 10, y = 60)
angle_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20), bg='#464757', fg='white', insertbackground="white")
angle_entry.place(x = 340, y = 65)

height_label = tk.Label(window, text="Initial Height (meters):", font=('Comic Sans MS', 20), bg='#464757', fg='white')
height_label.place(x = 10, y = 115)
height_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20), bg='#464757', fg='white', insertbackground="white")
height_entry.place(x = 340, y = 120)

wind_speed_label = tk.Label(window, text="Wind Speed (m/s):", font=('Comic Sans MS', 20), bg='#464757', fg='white')
wind_speed_label.place(x = 10, y = 170)
wind_speed_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20), bg='#464757', fg='white', insertbackground="white")
wind_speed_entry.place(x = 340, y = 175)

bomb_mass_label = tk.Label(window, text="Bomb Mass (kg):", font=('Comic Sans MS', 20), bg='#464757', fg='white')
bomb_mass_label.place(x = 10, y = 225)
bomb_mass_entry = tk.Entry(window, width=30, font=('Comic Sans MS', 20), bg='#464757', fg='white', insertbackground="white")
bomb_mass_entry.place(x = 340, y = 230)

#Example bomb label
exampleBomb_label = tk.Label(window, text="Example Bomb \nData:", font=('Comic Sans MS', 20), bg='#464757', fg='white')
exampleBomb_label.place(x = 865, y = 20)

# ------------------ MAIN BUTTONS ------------------------------

# Create a button to simulate the trajectory
simulate_button = tk.Button(window, text="Simulate", command=simulate_trajectory, font=('Comic Sans MS', 15), padx=7, bg='#a9e8ba')
simulate_button.place(x = 1100, y = 45)

# Create a button to restart the simulation
restart_button = tk.Button(window, text="Reset", command=restart, font=('Comic Sans MS', 15), padx=20, bg='#e8a9a9')
restart_button.place(x = 1100, y = 120)

# Create a button to clear in entry box
clear_button = tk.Button(window, text="Clear", command=clear, font=('Comic Sans MS', 15), padx=22, bg='#a9cee8')
clear_button.place(x = 1100, y = 195)

# Create a button to autofill in entry box
autoFill_button = tk.Button(window, text="Autofill", command=autoFill, font=('Comic Sans MS', 15), padx=12, bg='#d2a9e8')
autoFill_button.place(x = 1100, y = 270)

# --------------- EXAMPLE BUTTONS ------------------------------

# Create a button to fill fat man data
fatMan_button = tk.Button(window, text="Fat Man", command=fill_fatMan, font=('Comic Sans MS', 15), padx=38, bg='#e3e8a9')
fatMan_button.place(x = 870, y = 120)

# Create a button to fill fab data
FAB_button = tk.Button(window, text="FAB-500", command=fill_FAB, font=('Comic Sans MS', 15), padx=33, bg='#e3e8a9')
FAB_button.place(x = 870, y = 195)

# Create a button to fill pkb
PBK_button = tk.Button(window, text="PKB-500U Drel", command=fill_PKB, font=('Comic Sans MS', 15), padx=4, bg='#e3e8a9')
PBK_button.place(x = 870, y = 270)

# ------------------ INFO BAR ----------------------------------

status_bar = tk.Label(window, text="Hover over Buttons or Labels to display information. \nInstructions: \nEnter the data input and press simulate.", bg='#464757', fg='white', bd=2, relief=tk.SUNKEN, font=('Comic Sans MS', 15), anchor='nw', width=66, height=3, padx=10, pady=1)
status_bar.place(x = 10, y = 285)

# === main input labels =====
wind_speed_label.bind("<Enter>", bHover_windSpeed)
wind_speed_label.bind("<Leave>", bHover_windSpeed_leave)

angle_label.bind("<Enter>", bHover_launchAng)
angle_label.bind("<Leave>", bHover_launchAng_leave)

height_label.bind("<Enter>", bHover_height)
height_label.bind("<Leave>", bHover_height_leave)

velocity_label.bind("<Enter>", bHover_inVelocity)
velocity_label.bind("<Leave>", bHover_inVelocity_leave)

bomb_mass_label.bind("<Enter>", bHover_mass)
bomb_mass_label.bind("<Leave>", bHover_mass_leave)

exampleBomb_label.bind("<Enter>", bHover_exampleBomb)
exampleBomb_label.bind("<Leave>", bHover_exampleBomb_leave)


# ==== example buttons ======
fatMan_button.bind("<Enter>", bHover_fatMan)
fatMan_button.bind("<Leave>", bHover_fatMan_leave)

FAB_button.bind("<Enter>", bHover_FAB)
FAB_button.bind("<Leave>", bHover_FAB_leave)

PBK_button.bind("<Enter>", bHover_PBK)
PBK_button.bind("<Leave>", bHover_PBK_leave)

# ====== main buttons =======
simulate_button.bind("<Enter>", bHover_sim)
simulate_button.bind("<Leave>", bHover_sim_leave)

restart_button.bind("<Enter>", bHover_restart)
restart_button.bind("<Leave>", bHover_restart_leave)

clear_button.bind("<Enter>", bHover_clear)
clear_button.bind("<Leave>", bHover_clear_leave)

autoFill_button.bind("<Enter>", bHover_autoFill)
autoFill_button.bind("<Leave>", bHover_autoFill_leave)

# Start the main GUI loop
window.mainloop()