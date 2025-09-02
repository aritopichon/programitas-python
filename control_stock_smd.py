import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Base de datos y tablas
DB_NAME = 'smartfix_stock.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabla componentes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS componentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo TEXT UNIQUE NOT NULL,
            cantidad INTEGER NOT NULL,
            descripcion TEXT,
            ubicacion TEXT,
            fecha_mod TEXT NOT NULL
        )
    ''')
    # Tabla proveedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            contacto TEXT,
            telefono TEXT,
            email TEXT,
            direccion TEXT
        )
    ''')
    # Tabla compras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            componente_id INTEGER NOT NULL,
            proveedor_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            costo_unitario REAL,
            costo_total REAL,
            FOREIGN KEY(componente_id) REFERENCES componentes(id),
            FOREIGN KEY(proveedor_id) REFERENCES proveedores(id)
        )
    ''')
    conn.commit()
    conn.close()


class SmartFixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartFix - Control de Stock SMD")
        self.geometry("900x600")
        self.resizable(False, False)

        self.create_widgets()
        self.load_componentes()
        self.load_proveedores()
        self.load_compras()

    def create_widgets(self):
        tabControl = ttk.Notebook(self)
        self.tab_componentes = ttk.Frame(tabControl)
        self.tab_proveedores = ttk.Frame(tabControl)
        self.tab_compras = ttk.Frame(tabControl)

        tabControl.add(self.tab_componentes, text='Componentes')
        tabControl.add(self.tab_proveedores, text='Proveedores')
        tabControl.add(self.tab_compras, text='Histórico de Compras')
        tabControl.pack(expand=1, fill="both")

        self.create_tab_componentes()
        self.create_tab_proveedores()
        self.create_tab_compras()

    #######################
    # TAB COMPONENTES
    #######################
    def create_tab_componentes(self):
        frame = self.tab_componentes

        # Campos de entrada
        labels = ['Nombre', 'Código', 'Cantidad', 'Descripción', 'Ubicación']
        self.comp_entries = {}
        for idx, text in enumerate(labels):
            lbl = ttk.Label(frame, text=text)
            lbl.grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
            self.comp_entries[text.lower()] = entry

        # Botones
        btn_add = ttk.Button(frame, text="Agregar", command=self.agregar_componente)
        btn_add.grid(row=0, column=2, padx=10, pady=5)
        btn_mod = ttk.Button(frame, text="Modificar", command=self.modificar_componente)
        btn_mod.grid(row=1, column=2, padx=10, pady=5)
        btn_del = ttk.Button(frame, text="Eliminar", command=self.eliminar_componente)
        btn_del.grid(row=2, column=2, padx=10, pady=5)
        btn_clear = ttk.Button(frame, text="Limpiar", command=self.limpiar_campos_componente)
        btn_clear.grid(row=3, column=2, padx=10, pady=5)

        # Treeview para lista de componentes
        self.tree_comp = ttk.Treeview(frame, columns=('id', 'nombre', 'codigo', 'cantidad', 'descripcion', 'ubicacion',
                                                      'fecha_mod'), show='headings', height=15)
        columnas = {
            'id': 'ID',
            'nombre': 'Nombre',
            'codigo': 'Código',
            'cantidad': 'Cantidad',
            'descripcion': 'Descripción',
            'ubicacion': 'Ubicación',
            'fecha_mod': 'Fecha Modificación'
        }
        for col, title in columnas.items():
            self.tree_comp.heading(col, text=title)
            self.tree_comp.column(col, width=100, anchor='center')
        self.tree_comp.column('descripcion', width=150)
        self.tree_comp.column('ubicacion', width=100)
        self.tree_comp.grid(row=5, column=0, columnspan=3, padx=5, pady=10)
        self.tree_comp.bind('<<TreeviewSelect>>', self.on_select_componente)

        # Buscador
        lbl_search = ttk.Label(frame, text="Buscar por nombre o código:")
        lbl_search.grid(row=6, column=0, sticky='w', padx=5)
        self.entry_search_comp = ttk.Entry(frame, width=30)
        self.entry_search_comp.grid(row=6, column=1, sticky='w', padx=5)
        btn_search = ttk.Button(frame, text="Buscar", command=self.buscar_componente)
        btn_search.grid(row=6, column=2, sticky='w', padx=5)

    def agregar_componente(self):
        nombre = self.comp_entries['nombre'].get()
        codigo = self.comp_entries['código'].get()
        cantidad = self.comp_entries['cantidad'].get()
        descripcion = self.comp_entries['descripción'].get()
        ubicacion = self.comp_entries['ubicación'].get()
        if not nombre or not codigo or not cantidad.isdigit():
            messagebox.showerror("Error", "Complete nombre, código y cantidad numérica válida.")
            return

        cantidad = int(cantidad)
        fecha_mod = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO componentes (nombre, codigo, cantidad, descripcion, ubicacion, fecha_mod)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, codigo, cantidad, descripcion, ubicacion, fecha_mod))
            conn.commit()
            messagebox.showinfo("Éxito", "Componente agregado correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Código ya existe. Use modificar para actualizar.")
        conn.close()
        self.limpiar_campos_componente()
        self.load_componentes()

    def load_componentes(self):
        for row in self.tree_comp.get_children():
            self.tree_comp.delete(row)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        for row in c.execute('SELECT * FROM componentes ORDER BY nombre'):
            self.tree_comp.insert('', tk.END, values=row)
        conn.close()

    def on_select_componente(self, event):
        selected = self.tree_comp.selection()
        if not selected:
            return
        item = self.tree_comp.item(selected[0])['values']
        if not item:
            return
        self.comp_entries['nombre'].delete(0, tk.END)
        self.comp_entries['nombre'].insert(0, item[1])
        self.comp_entries['código'].delete(0, tk.END)
        self.comp_entries['código'].insert(0, item[2])
        self.comp_entries['cantidad'].delete(0, tk.END)
        self.comp_entries['cantidad'].insert(0, item[3])
        self.comp_entries['descripción'].delete(0, tk.END)
        self.comp_entries['descripción'].insert(0, item[4])
        self.comp_entries['ubicación'].delete(0, tk.END)
        self.comp_entries['ubicación'].insert(0, item[5])

    def modificar_componente(self):
        selected = self.tree_comp.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un componente para modificar.")
            return
        item = self.tree_comp.item(selected[0])['values']
        id_componente = item[0]

        nombre = self.comp_entries['nombre'].get()
        codigo = self.comp_entries['código'].get()
        cantidad = self.comp_entries['cantidad'].get()
        descripcion = self.comp_entries['descripción'].get()
        ubicacion = self.comp_entries['ubicación'].get()
        if not nombre or not codigo or not cantidad.isdigit():
            messagebox.showerror("Error", "Complete nombre, código y cantidad numérica válida.")
            return

        cantidad = int(cantidad)
        fecha_mod = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute('''
                UPDATE componentes
                SET nombre=?, codigo=?, cantidad=?, descripcion=?, ubicacion=?, fecha_mod=?
                WHERE id=?
            ''', (nombre, codigo, cantidad, descripcion, ubicacion, fecha_mod, id_componente))
            conn.commit()
            messagebox.showinfo("Éxito", "Componente modificado correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Código duplicado, no se pudo modificar.")
        conn.close()
        self.limpiar_campos_componente()
        self.load_componentes()

    def eliminar_componente(self):
        selected = self.tree_comp.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un componente para eliminar.")
            return
        item = self.tree_comp.item(selected[0])['values']
        id_componente = item[0]
        respuesta = messagebox.askyesno("Confirmar", "¿Eliminar componente seleccionado?")
        if respuesta:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('DELETE FROM componentes WHERE id=?', (id_componente,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Componente eliminado.")
            self.limpiar_campos_componente()
            self.load_componentes()

    def limpiar_campos_componente(self):
        for entry in self.comp_entries.values():
            entry.delete(0, tk.END)

    def buscar_componente(self):
        texto = self.entry_search_comp.get().strip().lower()
        for row in self.tree_comp.get_children():
            self.tree_comp.delete(row)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        query = '''
            SELECT * FROM componentes
            WHERE LOWER(nombre) LIKE ? OR LOWER(codigo) LIKE ?
            ORDER BY nombre
        '''
        like_text = f'%{texto}%'
        for row in c.execute(query, (like_text, like_text)):
            self.tree_comp.insert('', tk.END, values=row)
        conn.close()

    #######################
    # TAB PROVEEDORES
    #######################
    def create_tab_proveedores(self):
        frame = self.tab_proveedores

        labels = ['Nombre', 'Contacto', 'Teléfono', 'Email', 'Dirección']
        self.prov_entries = {}
        for idx, text in enumerate(labels):
            lbl = ttk.Label(frame, text=text)
            lbl.grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
            self.prov_entries[text.lower()] = entry

        btn_add = ttk.Button(frame, text="Agregar", command=self.agregar_proveedor)
        btn_add.grid(row=0, column=2, padx=10, pady=5)
        btn_mod = ttk.Button(frame, text="Modificar", command=self.modificar_proveedor)
        btn_mod.grid(row=1, column=2, padx=10, pady=5)
        btn_del = ttk.Button(frame, text="Eliminar", command=self.eliminar_proveedor)
        btn_del.grid(row=2, column=2, padx=10, pady=5)
        btn_clear = ttk.Button(frame, text="Limpiar", command=self.limpiar_campos_proveedor)
        btn_clear.grid(row=3, column=2, padx=10, pady=5)

        self.tree_prov = ttk.Treeview(frame, columns=('id', 'nombre', 'contacto', 'telefono', 'email', 'direccion'),
                                      show='headings', height=15)
        cols = {
            'id': 'ID',
            'nombre': 'Nombre',
            'contacto': 'Contacto',
            'telefono': 'Teléfono',
            'email': 'Email',
            'direccion': 'Dirección'
        }
        for col, title in cols.items():
            self.tree_prov.heading(col, text=title)
            self.tree_prov.column(col, width=120, anchor='center')
        self.tree_prov.grid(row=5, column=0, columnspan=3, padx=5, pady=10)
        self.tree_prov.bind('<<TreeviewSelect>>', self.on_select_proveedor)

        # Buscador
        lbl_search = ttk.Label(frame, text="Buscar por nombre o contacto:")
        lbl_search.grid(row=6, column=0, sticky='w', padx=5)
        self.entry_search_prov = ttk.Entry(frame, width=30)
        self.entry_search_prov.grid(row=6, column=1, sticky='w', padx=5)
        btn_search = ttk.Button(frame, text="Buscar", command=self.buscar_proveedor)
        btn_search.grid(row=6, column=2, sticky='w', padx=5)

    def agregar_proveedor(self):
        nombre = self.prov_entries['nombre'].get()
        contacto = self.prov_entries['contacto'].get()
        telefono = self.prov_entries['teléfono'].get()
        email = self.prov_entries['email'].get()
        direccion = self.prov_entries['dirección'].get()
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO proveedores (nombre, contacto, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, contacto, telefono, email, direccion))
            conn.commit()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Proveedor ya existe. Use modificar para actualizar.")
        conn.close()
        self.limpiar_campos_proveedor()
        self.load_proveedores()

    def load_proveedores(self):
        for row in self.tree_prov.get_children():
            self.tree_prov.delete(row)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        for row in c.execute('SELECT * FROM proveedores ORDER BY nombre'):
            self.tree_prov.insert('', tk.END, values=row)
        conn.close()

    def on_select_proveedor(self, event):
        selected = self.tree_prov.selection()
        if not selected:
            return
        item = self.tree_prov.item(selected[0])['values']
        if not item:
            return
        self.prov_entries['nombre'].delete(0, tk.END)
        self.prov_entries['nombre'].insert(0, item[1])
        self.prov_entries['contacto'].delete(0, tk.END)
        self.prov_entries['contacto'].insert(0, item[2])
        self.prov_entries['teléfono'].delete(0, tk.END)
        self.prov_entries['teléfono'].insert(0, item[3])
        self.prov_entries['email'].delete(0, tk.END)
        self.prov_entries['email'].insert(0, item[4])
        self.prov_entries['dirección'].delete(0, tk.END)
        self.prov_entries['dirección'].insert(0, item[5])

    def modificar_proveedor(self):
        selected = self.tree_prov.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para modificar.")
            return
        item = self.tree_prov.item(selected[0])['values']
        id_prov = item[0]

        nombre = self.prov_entries['nombre'].get()
        contacto = self.prov_entries['contacto'].get()
        telefono = self.prov_entries['teléfono'].get()
        email = self.prov_entries['email'].get()
        direccion = self.prov_entries['dirección'].get()
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute('''
                UPDATE proveedores
                SET nombre=?, contacto=?, telefono=?, email=?, direccion=? 
                WHERE id=?
            ''', (nombre, contacto, telefono, email, direccion, id_prov))
            conn.commit()
            messagebox.showinfo("Éxito", "Proveedor modificado correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Nombre de proveedor duplicado, no se pudo modificar.")
        conn.close()
        self.limpiar_campos_proveedor()
        self.load_proveedores()

    def eliminar_proveedor(self):
        selected = self.tree_prov.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar.")
            return
        item = self.tree_prov.item(selected[0])['values']
        id_prov = item[0]
        respuesta = messagebox.askyesno("Confirmar", "¿Eliminar proveedor seleccionado?")
        if respuesta:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('DELETE FROM proveedores WHERE id=?', (id_prov,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor eliminado.")
            self.limpiar_campos_proveedor()
            self.load_proveedores()

    def limpiar_campos_proveedor(self):
        for entry in self.prov_entries.values():
            entry.delete(0, tk.END)

    def buscar_proveedor(self):
        texto = self.entry_search_prov.get().strip().lower()
        for row in self.tree_prov.get_children():
            self.tree_prov.delete(row)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        query = '''
            SELECT * FROM proveedores
            WHERE LOWER(nombre) LIKE ? OR LOWER(contacto) LIKE ?
            ORDER BY nombre
        '''
        like_text = f'%{texto}%'
        for row in c.execute(query, (like_text, like_text)):
            self.tree_prov.insert('', tk.END, values=row)
        conn.close()

    #######################
    # TAB COMPRAS
    #######################
    def create_tab_compras(self):
        frame = self.tab_compras

        # Campos
        labels = ['Componente', 'Proveedor', 'Cantidad', 'Fecha (YYYY-MM-DD)', 'Costo Unitario']
        self.compra_vars = {}
        for idx, text in enumerate(labels):
            lbl = ttk.Label(frame, text=text)
            lbl.grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            if text in ['Componente', 'Proveedor']:
                combo = ttk.Combobox(frame, state='readonly', width=37)
                combo.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                self.compra_vars[text.lower()] = combo
            else:
                entry = ttk.Entry(frame, width=40)
                entry.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                self.compra_vars[text.lower()] = entry

        btn_add = ttk.Button(frame, text="Agregar Compra", command=self.agregar_compra)
        btn_add.grid(row=0, column=2, padx=10, pady=5)
        btn_clear = ttk.Button(frame, text="Limpiar", command=self.limpiar_campos_compra)
        btn_clear.grid(row=1, column=2, padx=10, pady=5)

        self.tree_compra = ttk.Treeview(frame,
                                        columns=('id', 'componente', 'proveedor', 'cantidad', 'fecha', 'costo_unitario',
                                                 'costo_total'), show='headings', height=15)
        cols = {
            'id': 'ID',
            'componente': 'Componente',
            'proveedor': 'Proveedor',
            'cantidad': 'Cantidad',
            'fecha': 'Fecha',
            'costo_unitario': 'Costo Unitario',
            'costo_total': 'Costo Total'
        }
        for col, title in cols.items():
            self.tree_compra.heading(col, text=title)
            self.tree_compra.column(col, width=110, anchor='center')
        self.tree_compra.column('fecha', width=120)
        self.tree_compra.column('costo_total', width=120)
        self.tree_compra.grid(row=5, column=0, columnspan=3, padx=5, pady=10)

        self.load_comboboxes()

    def load_comboboxes(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT id, nombre FROM componentes ORDER BY nombre')
        componentes = c.fetchall()
        c.execute('SELECT id, nombre FROM proveedores ORDER BY nombre')
        proveedores = c.fetchall()
        conn.close()
        # Actualizar combo componentes
        comp_ids = [str(cmp[0]) for cmp in componentes]
        comp_names = [f"{cmp[1]} (ID:{cmp[0]})" for cmp in componentes]
        self.compra_vars['componente']['values'] = comp_names
        self.compra_vars['componente'].comp_map = dict(zip(comp_names, comp_ids))
        # Actualizar combo proveedores
        prov_ids = [str(pv[0]) for pv in proveedores]
        prov_names = [f"{pv[1]} (ID:{pv[0]})" for pv in proveedores]
        self.compra_vars['proveedor']['values'] = prov_names
        self.compra_vars['proveedor'].prov_map = dict(zip(prov_names, prov_ids))

    def agregar_compra(self):
        comp_sel = self.compra_vars['componente'].get()
        prov_sel = self.compra_vars['proveedor'].get()
        cantidad = self.compra_vars['cantidad'].get()
        fecha = self.compra_vars['fecha (yyyy-mm-dd)'].get()
        costo_unit = self.compra_vars['costo unitario'].get()
        if not comp_sel or not prov_sel or not cantidad.isdigit() or not fecha or not costo_unit.replace('.', '',
                                                                                                         1).isdigit():
            messagebox.showerror("Error", "Complete todos los campos correctamente (cantidad numérica, costo decimal).")
            return
        cantidad = int(cantidad)
        costo_unit = float(costo_unit)
        costo_total = round(cantidad * costo_unit, 2)
        comp_id = int(self.compra_vars['componente'].comp_map.get(comp_sel, 0))
        prov_id = int(self.compra_vars['proveedor'].prov_map.get(prov_sel, 0))
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD.")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO compras (componente_id, proveedor_id, cantidad, fecha, costo_unitario, costo_total)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (comp_id, prov_id, cantidad, fecha, costo_unit, costo_total))
        # Actualizar stock componente
        c.execute('SELECT cantidad FROM componentes WHERE id=?', (comp_id,))
        stock_actual = c.fetchone()
        if stock_actual:
            nuevo_stock = stock_actual[0] + cantidad
            fecha_mod = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute('UPDATE componentes SET cantidad=?, fecha_mod=? WHERE id=?', (nuevo_stock, fecha_mod, comp_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Compra agregada y stock actualizado.")
        self.limpiar_campos_compra()
        self.load_compras()
        self.load_componentes()
        self.load_comboboxes()

    def load_compras(self):
        for row in self.tree_compra.get_children():
            self.tree_compra.delete(row)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''SELECT compras.id, componentes.nombre, proveedores.nombre, compras.cantidad, compras.fecha, compras.costo_unitario, compras.costo_total
                     FROM compras
                     JOIN componentes ON compras.componente_id = componentes.id
                     JOIN proveedores ON compras.proveedor_id = proveedores.id
                     ORDER BY compras.fecha DESC''')
        for row in c.fetchall():
            self.tree_compra.insert('', tk.END, values=row)
        conn.close()

    def limpiar_campos_compra(self):
        for widget in self.compra_vars.values():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')


if __name__ == "__main__":
    init_db()
    app = SmartFixApp()
    app.mainloop()
