import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt

def calculadora():
    while True:
        operación = simpledialog.askstring("Calculadora", "Ingrese la operación (+, -, *, /) o salir para terminar: ")
        if operación == "salir":
            messagebox.showinfo("Gracias por usar la calculadora")
            break

        try:
            num1= float(simpledialog.askfloat("Calculadora", "Ingrese el primer número: "))
            num2= float(simpledialog.askfloat("Calculadora", "Ingrese el segundo número: "))
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
            continue

        if operación == "+":
            resultado = num1 + num2
        elif operación == "-":
            resultado = num1 - num2
        elif operación == "*":
            resultado = num1 * num2
        elif operación == "/":
            if num2 == 0:
                messagebox.showerror("Error", "División por cero")
                continue
            resultado = num1 / num2
        else:
            messagebox.showerror("Error", "Operación no válida")
            continue
        messagebox.showinfo("Resultado", f"El resultado de {num1} {operación} {num2} es: {resultado}")

def FizzBuzz():
    while True:
        userRange = (simpledialog.askstring("FizzBuzz", "Ingrese el rango de números: "))

        if(userRange=="salir" or userRange=="exit" or userRange=="Salir" or userRange=="Exit" or userRange==""):
            break
        else:
            try:
                _range = int(userRange)
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")
                continue

        resultado=[]
        for i in range(1, _range + 1):
            if i % 3 == 0 and i % 5 == 0:
                resultado.append("FizzBuzz")
            elif i % 3 == 0:
                resultado.append("Fizz")
            elif i % 5 == 0:
                resultado.append("Buzz")
            else:
                resultado.append(str(i))    
        messagebox.showinfo("FizzBuzz", "\n".join(resultado))

def analisisDatos():
    while True:
        nombre_archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos CSV", "*.csv")])
        if not nombre_archivo:
            break
        else:
            try:
                df = pd.read_csv(nombre_archivo, sep=";")
                
                stats=""
                for idx in range(2):
                    stats += f"Estadisticas de la columna {idx+1}:\n"
                    stats += f"Media: {df.iloc[:, idx].mean()}\n"
                    stats += f"Mediana: {df.iloc[:, idx].median()}\n"
                    stats += f"Desviación estándar: {df.iloc[:, idx].std()}\n"
                    stats += "\n"

                messagebox.showinfo("Estadísticas", stats)
                plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
                plt.xlabel("Columna 1")
                plt.ylabel("Columna 2")
                plt.title("Gráfico de dispersión")
                plt.show()
            except FileNotFoundError:
                messagebox.showerror("Error", "El archivo no existe")
                continue


root = tk.Tk()
root.title("Ejercicios de Python con IA")
root.geometry("300x200")
root.configure(bg="black")

titulo=tk.Label(root, text="Ejercicios de Python con IA", font=("Arial", 16), fg="white", bg="black")
titulo.pack(pady=10)

descripcion=tk.Label(root, text="Seleccione el ejercicio que desea realizar", font=("Arial", 12), fg="white", bg="black")
descripcion.pack(pady=10)

tk.Button(root, text="Calculadora", width=30,command=calculadora).pack(pady=10)
tk.Button(root, text="FizzBuzz", width=30,command=FizzBuzz).pack(pady=10)
tk.Button(root, text="Análisis de datos", width=30,command=analisisDatos).pack(pady=10)

salir_btn = tk.Button(root, text="Salir", width=30,command=root.destroy)
salir_btn.pack(pady=10)

root.mainloop()










