import socket
import tkinter as tk
from tkinter import ttk
import threading
from ttkthemes import ThemedStyle

# Raspberry Pi's IP address and port to listen on
host = '192.168.48.107'  # Replace with your Raspberry Pi's IP address
port = 12345  # Use the same port as on the Arduino

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)

print("Listening for incoming connections...")

# Function to receive data from Arduino
def receive_data():
    while True:
        # Accept a connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Receive data from the Arduino
        data = client_socket.recv(1024).decode()
        print(f"Received data: {data}")

        # Process the received data here, update labels or perform actions
        update_sensor_data(data)

        # Close the client socket
        client_socket.close()

# Create a Tkinter application
app = tk.Tk()
app.title("CleanFlow URV-210 Water Treatment Control Panel")
app.geometry("800x600")  # Set window dimensions

# Apply a theme to enhance GUI aesthetics
style = ThemedStyle(app)
style.set_theme("plastik")

# Create a header label
header_label = ttk.Label(app, text="CleanFlow URV-210", style="TLabel")
header_label.grid(row=0, column=0, padx=10, pady=10)

# Define variables for sensor readings
turbidity_value = tk.StringVar()
ph_value = tk.StringVar()

# Function to update sensor readings
def update_sensor_data(data):
    # Update the sensor readings from received data
    # Split the data into pH and turbidity values
    parts = data.split(" ")
    if len(parts) >= 2:
        ph_value.set("pH: " + parts[1])
        turbidity_value.set("Turbidity: " + parts[3] + " NTU")

# Create a frame for sensor readings
sensor_frame = ttk.LabelFrame(app, text="Sensor Readings")
sensor_frame.grid(row=1, column=0, padx=10, pady=10)

turbidity_label = ttk.Label(sensor_frame, textvariable=turbidity_value, style="TLabel")
turbidity_label.grid(row=0, column=0, padx=5, pady=5)

ph_label = ttk.Label(sensor_frame, textvariable=ph_value, style="TLabel")
ph_label.grid(row=1, column=0, padx=5, pady=5)

# Create a frame for the coagulation and sedimentation process
coagulation_frame = ttk.LabelFrame(app, text="Coagulation and Sedimentation")
coagulation_frame.grid(row=2, column=0, padx=10, pady=10)

coagulation_button = ttk.Button(coagulation_frame, text="Start Process")
coagulation_button.grid(row=0, column=0, padx=5, pady=5)

# Create a frame for the filtration process (you can customize this part)
filtration_frame = ttk.LabelFrame(app, text="Filtration")
filtration_frame.grid(row=3, column=0, padx=10, pady=10)

filtration_button = ttk.Button(filtration_frame, text="Start Process")
filtration_button.grid(row=0, column=0, padx=5, pady=5)

pump1_button = ttk.Button(app, text="Turn On Pump T1-T2")
pump1_button.grid(row=4, column=0, padx=10, pady=10)

pump2_button = ttk.Button(app, text="Turn On Pump T2-T1")
pump2_button.grid(row=5, column=0, padx=10, pady=10)

pump3_button = ttk.Button(app, text="Turn On Pump T2-T3")
pump3_button.grid(row=6, column=0, padx=10, pady=10)

stir_motor_button = ttk.Button(app, text="Start Stir Motor")
stir_motor_button.grid(row=7, column=0, padx=10, pady=10)

def control_nano(command):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.send(command.encode())
        client_socket.close()
    except Exception as e:
        print("Error:", e)

# Button click event handlers
def on_pump1_click():
    control_nano("Pump1On")

def on_pump2_click():
    control_nano("Pump2On")

def on_pump3_click():
    control_nano("Pump3On")

def on_stir_motor_click():
    control_nano("StirMotorStart")

# Attach button click event handlers
pump1_button.config(command=on_pump1_click)
pump2_button.config(command=on_pump2_click)
pump3_button.config(command=on_pump3_click)
stir_motor_button.config(command=on_stir_motor_click)

# Start receiving data from the Arduino in the background
data_thread = threading.Thread(target=receive_data)
data_thread.daemon = True
data_thread.start()

# Run the Tkinter application
app.mainloop()
