#traductor
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from deep_translator import GoogleTranslator

# Diccionario para mapear nombres de idiomas en español a códigos deep_translator
idiomas = {
    "Español": "spanish",
    "Inglés": "english",
    "Francés": "french",
    "Alemán": "german",
    "Italiano": "italian",
    "Portugués": "portuguese",
    "Chino": "chinese",
    "Japonés": "japanese",
    "Hindi": "hindi"
}

class TraductorApp:
    def __init__(self, root):
        self.root = root
        root.title("Traductor tipo Google Translate")
        root.geometry("700x500")
        root.resizable(False, False)

        self.mainframe = ttk.Frame(root, padding="10")
        self.mainframe.pack(fill=tk.BOTH, expand=True)

        self.bold_font = ("Segoe UI", 11, "bold")

        ttk.Label(self.mainframe, text="Idioma origen:", font=self.bold_font, foreground="black").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(self.mainframe, text="Idioma destino:", font=self.bold_font, foreground="black").grid(row=0, column=2, sticky="w", padx=5)

        self.combo_origen = ttk.Combobox(self.mainframe, values=list(idiomas.keys()), state="readonly", font=self.bold_font, width=20)
        self.combo_origen.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.combo_origen.set("Inglés")

        self.combo_destino = ttk.Combobox(self.mainframe, values=list(idiomas.keys()), state="readonly", font=self.bold_font, width=20)
        self.combo_destino.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        self.combo_destino.set("Español")

        self.btn_invertir = ttk.Button(self.mainframe, text="⇄", command=self.intercambiar_idiomas, width=3)
        self.btn_invertir.grid(row=1, column=1, pady=5)

        ttk.Label(self.mainframe, text="Texto a traducir:", font=self.bold_font, foreground="black").grid(row=2, column=0, columnspan=3, sticky="w", pady=(15, 5), padx=5)

        self.text_entrada = ScrolledText(self.mainframe, wrap=tk.WORD, font=("Segoe UI", 10), width=60, height=8)
        self.text_entrada.grid(row=3, column=0, columnspan=3, padx=5, sticky="nsew")

        ttk.Label(self.mainframe, text="Traducción:", font=self.bold_font, foreground="black").grid(row=4, column=0, columnspan=3, sticky="w", pady=(15, 5), padx=5)

        self.text_traducido = ScrolledText(self.mainframe, wrap=tk.WORD, font=("Segoe UI", 10), width=60, height=8, state=tk.DISABLED)
        self.text_traducido.grid(row=5, column=0, columnspan=3, padx=5, sticky="nsew")

        self.btn_traducir = ttk.Button(self.mainframe, text="Traducir", command=self.translate)
        self.btn_traducir.grid(row=6, column=0, columnspan=3, pady=15, sticky="ew")

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=0)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.rowconfigure(3, weight=1)
        self.mainframe.rowconfigure(5, weight=1)

        # Crear menú contextual para copiar, cortar y pegar
        self.menu_contextual = tk.Menu(self.root, tearoff=0)
        self.menu_contextual.add_command(label="Cortar", command=lambda: self.evento_cortar())
        self.menu_contextual.add_command(label="Copiar", command=lambda: self.evento_copiar())
        self.menu_contextual.add_command(label="Pegar", command=lambda: self.evento_pegar())

        # Asignar evento botón derecho para mostrar menú en entrada y salida
        self.text_entrada.bind("<Button-3>", self.mostrar_menu)
        self.text_traducido.bind("<Button-3>", self.mostrar_menu)

    def intercambiar_idiomas(self):
        origen = self.combo_origen.get()
        destino = self.combo_destino.get()
        self.combo_origen.set(destino)
        self.combo_destino.set(origen)

    def translate(self):
        src = idiomas.get(self.combo_origen.get())
        tgt = idiomas.get(self.combo_destino.get())
        text = self.text_entrada.get("1.0", tk.END).strip()
        if not text:
            self.limpiar_salida()
            return
        try:
            traduccion = GoogleTranslator(source=src, target=tgt).translate(text)
            self.mostrar_traduccion(traduccion)
        except Exception as e:
            self.mostrar_traduccion(f"Error: {e}")

    def mostrar_traduccion(self, texto):
        self.text_traducido.config(state=tk.NORMAL)
        self.text_traducido.delete("1.0", tk.END)
        self.text_traducido.insert(tk.END, texto)
        self.text_traducido.config(state=tk.DISABLED)

    def limpiar_salida(self):
        self.mostrar_traduccion("")

    # Funciones para menú contextual
    def evento_copiar(self):
        widget = self.root.focus_get()
        try:
            widget.event_generate("<<Copy>>")
        except Exception:
            pass

    def evento_cortar(self):
        widget = self.root.focus_get()
        try:
            widget.event_generate("<<Cut>>")
        except Exception:
            pass

    def evento_pegar(self):
        widget = self.root.focus_get()
        try:
            widget.event_generate("<<Paste>>")
        except Exception:
            pass

    def mostrar_menu(self, event):
        self.menu_contextual.tk_popup(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = TraductorApp(root)
    root.mainloop()





