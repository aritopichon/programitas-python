# adivina numero de 1,10
print ("¡BIENVENIDO/A A ADIVINA EL NUMERO!")
print("-----------------------------")
import random  # Importamos random para generar un número aleatorio

numero_secreto = random.randint(1, 10)  # Genera un número entero entre 1 y 10
intentos = 0  # Contador de intentos del usuario

while True:  # Bucle infinito hasta que se adivine el número o se rompa con break
    intento = input("Adivina el número entre 1 y 10: ")  # Entrada del usuario (por defecto cadena)
    intentos += 1  # Aumentamos el contador en 1

    if not intento.isdigit():  # Verificamos si lo ingresado es un número válido
        print("Por favor, ingresa un número válido.")
        continue  # Volvemos a pedir el dato sin contar este como intento válido

    intento = int(intento)  # Convertimos la cadena a entero

    if intento == numero_secreto:  # Comparación para saber si el usuario acertó
        print(f"¡Felicidades! Adivinaste el número en {intentos} intentos.")
        break  # Salimos del bucle porque el número fue adivinado

    elif intento < numero_secreto:
        print("Muy bajo, intenta de nuevo.")
    else:
        print("Muy alto, intenta de nuevo.")
