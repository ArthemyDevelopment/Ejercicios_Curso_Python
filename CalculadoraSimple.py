while True:
    operación = input("Ingrese la operación (+, -, *, /) o salir para terminar: ")
    if operación == "salir":
        print("Gracias por usar la calculadora")
        break

    num1= float(input("Ingrese el primer número: "))
    num2= float(input("Ingrese el segundo número: "))

    if operación == "+":
        resultado = num1 + num2
    elif operación == "-":
        resultado = num1 - num2
    elif operación == "*":
        resultado = num1 * num2
    elif operación == "/":
        if num2 == 0:
            print("Error: División por cero")
            continue
        resultado = num1 / num2
    else:
        print("Operación no válida")
        continue
    print(f"El resultado de {num1} {operación} {num2} es: {resultado}")
    
    