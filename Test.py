import re


archivo = input("Ingrese el nombre del archivo: ")

def contar_palabras(texto):
            """
            Cuenta la cantidad de palabras en el texto dado.
            Utiliza re.findall para extraer palabras ignorando puntuación y mayúsculas/minúsculas.
            """
            palabras = re.findall(r'\b\w+\b', texto.lower())
            return len(palabras), palabras

def obtener_palabras_mas_comunes(palabras, n=10):
            """
            Devuelve una lista de las n palabras más comunes y sus frecuencias.
            """
            from collections import Counter
            contador = Counter(palabras)
            return contador.most_common(n)

def test_palabras_mas_comunes():
            texto_prueba = "hola hola mundo mundo mundo prueba prueba prueba prueba"
            _, palabras_prueba = contar_palabras(texto_prueba)
            mas_comunes_prueba = obtener_palabras_mas_comunes(palabras_prueba, 2)
            esperado = [("prueba", 4), ("mundo", 3)]
            assert mas_comunes_prueba == esperado, f"Se esperaban {esperado}, pero se obtuvieron {mas_comunes_prueba}"

def test_contar_palabras():
            texto_prueba = "Hola, mundo! Esto es una prueba. ¿Cuántas palabras hay aquí?"
            esperado = 10  # "hola", "mundo", "esto", "es", "una", "prueba", "cuantas", "palabras", "hay", "aquí"
            resultado, _ = contar_palabras(texto_prueba)
            assert resultado == esperado, f"Se esperaban {esperado} palabras, pero se obtuvieron {resultado}"

try:
    test_contar_palabras()
    test_palabras_mas_comunes()

except AssertionError as e:
    print("Uno de los tests unitarios ha fallado:", e)




try:
    with open(archivo, "r", encoding="utf-8") as file:
            # Leer el texto del archivo
        texto = file.read()
        total_palabras, palabras = contar_palabras(texto)

        mas_comunes = obtener_palabras_mas_comunes(palabras, 10)

        print(f"El archivo tiene {total_palabras} palabras")
        
        print("Las 10 palabras más comunes son:")
        for palabra, frecuencia in mas_comunes:
            print(f"{palabra}: {frecuencia}")


except FileNotFoundError:
    print("El archivo no existe")
    exit(1)






