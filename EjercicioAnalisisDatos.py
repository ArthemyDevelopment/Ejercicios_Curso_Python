import pandas as pd
import matplotlib.pyplot as plt

nombre_archivo = input("Ingrese el nombre del archivo: ")

while True:
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    if nombre_archivo == "salir" or nombre_archivo == "exit" or nombre_archivo == "Salir" or nombre_archivo == "Exit":
        break
    else:
        try:
            df = pd.read_csv(nombre_archivo, sep=";")
            print("Archivo cargado correctamente")


            print("Estadisticas de la columna 1:")
            print("Media:", df.iloc[:, 0].mean())
            print("Mediana:", df.iloc[:, 0].median())
            print("Desviación estándar:", df.iloc[:, 0].std())


            print("\nEstadisticas de la columna 2:")
            print("Media:", df.iloc[:, 1].mean())
            print("Mediana:", df.iloc[:, 1].median())
            print("Desviación estándar:", df.iloc[:, 1].std())
            
            plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
            plt.xlabel("Columna 1")
            plt.ylabel("Columna 2")
            plt.title("Gráfico de dispersión")
            plt.show()
        except FileNotFoundError:
            print("El archivo no existe")
            continue








