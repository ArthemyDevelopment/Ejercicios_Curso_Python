
while True:
    userRange = (input("Ingrese el rango de números: "))

    if(userRange=="salir" or userRange=="exit" or userRange=="Salir" or userRange=="Exit"):
        break
    else:
        _range = int(userRange)


    for i in range(1, _range + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)    