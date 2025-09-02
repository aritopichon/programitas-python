import tkinter as tk

# Función para actualizar el texto en el campo de entrada
def agregar_numero(numero):
    actual = entrada.get()
    entrada.delete(0, tk.END)
    entrada.insert(0, actual + str(numero))

# Función para limpiar la entrada
def limpiar():
    entrada.delete(0, tk.END)

# Función para calcular el resultado
def calcular():
    try:
        resultado = eval(entrada.get())
        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))
    except:
        entrada.delete(0, tk.END)
        entrada.insert(0, "Error")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora Simple")
ventana.geometry("300x400")

# Campo de entrada (pantalla)
entrada = tk.Entry(ventana, font=("Arial", 24), borderwidth=2, relief="ridge", justify="right")
entrada.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="we")

# Botones: números y operaciones
botones = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
    ('=', 5, 0, 4)
]

# Crear y posicionar botones
for boton in botones:
    texto = boton[0]
    fila = boton[1]
    columna = boton[2]
    colspan = boton[3] if len(boton) == 4 else 1

    if texto == 'C':
        accion = limpiar
    elif texto == '=':
        accion = calcular
    else:
        accion = lambda x=texto: agregar_numero(x)

    b = tk.Button(ventana, text=texto, command=accion, font=("Arial", 18), height=2, width=5)
    b.grid(row=fila, column=columna, columnspan=colspan, sticky="nsew", padx=5, pady=5)

# Configurar las filas y columnas para que se expandan
for i in range(6):
    ventana.grid_rowconfigure(i, weight=1)
for j in range(4):
    ventana.grid_columnconfigure(j, weight=1)

# Ejecutar la app
ventana.mainloop()
