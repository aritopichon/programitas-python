# juego piedra papel o tijera
print("¡BIENVENIDO AL JUEGO!")
print("------------------------")
import random

print("¡Bienvenido al juego de Piedra, Papel o Tijeras!")
print("Elige tu opción:")
print("1. Piedra")
print("2. Papel")
print("3. Tijeras")
print("Escribe 's' para salir del juego.")

while True:
    jugador = input("Ingresa el número de tu elección (1, 2, 3) o 's' para salir: ").lower()
    if jugador == 's':
        print("¡Gracias por jugar!")
        break

    if jugador not in ['1', '2', '3']:
        print("Opción no válida, intenta de nuevo.")
        continue

    jugador = int(jugador)
    opciones = {1: "Piedra", 2: "Papel", 3: "Tijeras"}
    computadora = random.randint(1, 3)

    print(f"Tú elegiste: {opciones[jugador]}")
    print(f"La computadora eligió: {opciones[computadora]}")

    if jugador == computadora:
        print("Empate.")
    elif (jugador == 1 and computadora == 3) or (jugador == 2 and computadora == 1) or (
            jugador == 3 and computadora == 2):
        print("¡Ganaste!")
    else:
        print("Perdiste, intenta otra vez.")
