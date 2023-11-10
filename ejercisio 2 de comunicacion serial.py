import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import time

# Configuración del puerto serie (ajusta el puerto y la velocidad baud según tu configuración)
ser = serial.Serial('COM3', 9600)  # Reemplaza 'COM3' con el puerto de tu Arduino

# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación de Control")
root.geometry("800x600")

# Crear pestañas
tab_control = ttk.Notebook(root)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text="Pestaña de Control")
tab_control.pack(expand=1, fill="both")

# Variables para almacenar datos
voltage_values = []
temperature_values = []

# Funciones para simular lecturas de sensores
def read_voltage():
    voltage = random.uniform(0, 5)  # Simulación de lectura de voltaje
    voltage_values.append(voltage)
    voltage_label.config(text=f"Voltaje: {voltage} V")
    update_voltage_plot()
    return voltage

def read_temperature():
    temperature = random.uniform(20, 30)  # Simulación de lectura de temperatura
    temperature_values.append(temperature)
    temperature_label.config(text=f"Temperatura: {temperature} °C")
    temperature_bar["value"] = temperature
    update_temperature_plot()
    return temperature

# Función para establecer la velocidad del motor en Arduino
def set_motor_speed(speed):
    ser.write(f'M{speed}\n'.encode())  # Envía el comando al Arduino para ajustar la velocidad

# Etiquetas para mostrar los valores de voltaje y temperatura
voltage_label = tk.Label(tab2, text="Voltaje: ")
voltage_label.pack()

temperature_label = tk.Label(tab2, text="Temperatura: ")
temperature_label.pack()

# Configuración de la salida PWM
motor_pin = 9  # Reemplaza con el pin de salida PWM de tu Arduino
motor_speed = 0  # Variable para almacenar la velocidad del motor

# Controles para ajustar la velocidad del motor
speed_label = tk.Label(tab2, text="Velocidad del Motor:")
speed_label.pack()

speed_scale = tk.Scale(tab2, from_=0, to=255, orient="horizontal", length=200, label="0-255")
speed_scale.pack()

set_speed_button = tk.Button(tab2, text="Establecer Velocidad", command=lambda: set_motor_speed(speed_scale.get()))
set_speed_button.pack()

# Gráficos para mostrar los valores de voltaje y temperatura
fig = plt.Figure(figsize=(6, 4), dpi=100)
voltage_plot = fig.add_subplot(111)
voltage_plot.set_xlabel('Muestras')
voltage_plot.set_ylabel('Voltaje (V)')
voltage_plot.set_title('Gráfico de Voltaje')

fig2 = plt.Figure(figsize=(6, 4), dpi=100)
temperature_plot = fig2.add_subplot(111)
temperature_plot.set_xlabel('Muestras')
temperature_plot.set_ylabel('Temperatura (°C)')
temperature_plot.set_title('Gráfico de Temperatura')

# Creación de lienzo para los gráficos
voltage_canvas = FigureCanvasTkAgg(fig, master=tab2)
voltage_canvas.get_tk_widget().pack()

temperature_canvas = FigureCanvasTkAgg(fig2, master=tab2)
temperature_canvas.get_tk_widget().pack()

# Barra de progreso para mostrar el último valor adquirido de temperatura
temperature_bar = ttk.Progressbar(tab2, orient="horizontal", length=200, mode="determinate")
temperature_bar.pack()

# Funciones para actualizar los gráficos de voltaje y temperatura
def update_voltage_plot():
    voltage_plot.clear()
    voltage_plot.plot(range(len(voltage_values)), voltage_values, marker='o', linestyle='-', color='b')
    voltage_plot.set_xlabel('Muestras')
    voltage_plot.set_ylabel('Voltaje (V)')
    voltage_plot.set_title('Gráfico de Voltaje')
    voltage_canvas.draw()

def update_temperature_plot():
    temperature_plot.clear()
    temperature_plot.plot(range(len(temperature_values)), temperature_values, marker='o', linestyle='-', color='r')
    temperature_plot.set_xlabel('Muestras')
    temperature_plot.set_ylabel('Temperatura (°C)')
    temperature_plot.set_title('Gráfico de Temperatura')
    temperature_canvas.draw()

# Función para actualizar datos y controlar el motor
def update_data():
    voltage = read_voltage()
    temperature = read_temperature()
    set_motor_speed(motor_speed)  # Actualiza la velocidad del motor
    root.after(1000, update_data)

# Iniciar la actualización de datos
update_data()

root.mainloop()