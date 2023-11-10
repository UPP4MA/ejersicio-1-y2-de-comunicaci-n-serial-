import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import serial
import time

# Variable global para el puerto serial
ser = None

# Función para abrir el puerto serial
def open_port():
    global ser
    if ser is None or not ser.is_open:
        port = port_combo.get()
        try:
            ser = serial.Serial(port, baudrate=int(baud_rate_combo.get()))
            messagebox.showinfo("Puerto Serial", f"Puerto {port} abierto")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showinfo("Puerto Serial", "Puerto ya está abierto")

# Función para cerrar el puerto serial
def close_port():
    global ser
    if ser and ser.is_open:
        ser.close()
        messagebox.showinfo("Puerto Serial", "Puerto cerrado")
    else:
        messagebox.showinfo("Puerto Serial", "Puerto ya está cerrado")

# Función para enviar datos por el puerto serial
def send_data():
    if ser and ser.is_open:
        data = data_entry.get()
        ser.write(data.encode())
    else:
        messagebox.showerror("Error", "El puerto serial no está abierto")

# Función para recibir datos por el puerto serial
def receive_data():
    if ser and ser.is_open:
        try:
            received_data = ser.read(100).decode()
            received_data_label.config(text=received_data)
        except serial.SerialException as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "El puerto serial no está abierto")

# Función para enviar números en secuencia con retardo
def send_sequence():
    if ser and ser.is_open:
        try:
            start = int(start_spinbox.get())
            end = int(end_spinbox.get())
            delay = int(delay_spinbox.get())

            for i in range(start, end + 1):
                ser.write(str(i).encode())
                time.sleep(delay)
            
            messagebox.showinfo("Enviar Secuencia", "Secuencia enviada correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "El puerto serial no está abierto")

# Función para enviar un archivo TXT a una computadora remota
def send_file():
    if ser and ser.is_open:
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    ser.write(file_data)
                messagebox.showinfo("Envío de archivo", f"Archivo {file_path} enviado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo enviar el archivo: {str(e)}")
    else:
        messagebox.showerror("Error", "El puerto serial no está abierto")


# Configuración de la ventana principal
root = tk.Tk()
root.title("Aplicación GUI")

# Configuración de las pestañas
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Comunicación Simple")
tab_control.add(tab2, text="Enviar Archivo")

# Pestaña 1: Comunicación Simple
port_label = tk.Label(tab1, text="Puerto Serial:")
port_label.pack()
port_combo = ttk.Combobox(tab1, values=["COM1", "COM2", "COM3"])
port_combo.set("COM3")  # Establece un valor predeterminado
port_combo.pack()
baud_rate_label = tk.Label(tab1, text="Velocidad:")
baud_rate_label.pack()
baud_rate_combo = ttk.Combobox(tab1, values=["9600", "115200"])
baud_rate_combo.set("9600")  # Establece un valor predeterminado
baud_rate_combo.pack()
open_port_button = tk.Button(tab1, text="Abrir Puerto seleccionado", command=open_port)
open_port_button.pack()
close_port_button = tk.Button(tab1, text="Cerrar Puerto seleccionado", command=close_port)
close_port_button.pack()
data_label = tk.Label(tab1, text="Escriba el Dato a enviar:")
data_label.pack()
data_entry = tk.Entry(tab1)
data_entry.pack()
send_data_button = tk.Button(tab1, text="Enviar un Dato", command=send_data)
send_data_button.pack()
receive_data_button = tk.Button(tab1, text="Recibir Dato", command=receive_data)
receive_data_button.pack()
received_data_label = tk.Label(tab1, text="")
received_data_label.pack()
start_label = tk.Label(tab1, text="Inicio de secuencia:")
start_label.pack()
start_spinbox = ttk.Spinbox(tab1, from_=1, to=100)
start_spinbox.pack()
end_label = tk.Label(tab1, text="Fin de secuencia:")
end_label.pack()
end_spinbox = ttk.Spinbox(tab1, from_=1, to=100)
end_spinbox.pack()
delay_label = tk.Label(tab1, text="Retardo (segundos):")
delay_label.pack()
delay_spinbox = ttk.Spinbox(tab1, from_=0, to=10)
delay_spinbox.pack()
send_sequence_button = tk.Button(tab1, text="Enviar Secuencia seleccionada", command=send_sequence)
send_sequence_button.pack()

# Pestaña 2: Enviar Archivo
send_file_button = tk.Button(tab2, text="Enviar Archivo", command=send_file)
send_file_button.pack()

# Mostrar la aplicación
tab_control.pack()
root.mainloop()