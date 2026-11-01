import tkinter as tk
from tkinter import ttk, messagebox
from base_datos.conexion import conectar


class VentanaLaboratorios(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de laboratorios")
        self.geometry("720x480")
        self.transient(master)
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        marco = ttk.Frame(self, padding=15)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Registro de laboratorios",
                  font=("Arial", 16, "bold")).pack(pady=(0, 12))

        formulario = ttk.LabelFrame(marco, text="Datos del laboratorio", padding=10)
        formulario.pack(fill="x")

        self.nombre = tk.StringVar()
        self.ubicacion = tk.StringVar()
        self.capacidad = tk.StringVar()

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(formulario, textvariable=self.nombre, width=28).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(formulario, text="Ubicación:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(formulario, textvariable=self.ubicacion, width=25).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(formulario, text="Capacidad:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(formulario, textvariable=self.capacidad, width=12).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(formulario, text="Registrar", command=self.registrar).grid(row=1, column=3, sticky="e", padx=5, pady=5)

        self.tabla = ttk.Treeview(marco, columns=("id", "nombre", "ubicacion", "capacidad"),
                                  show="headings", height=12)
        for col, titulo, ancho in [
            ("id", "ID", 50), ("nombre", "Laboratorio", 220),
            ("ubicacion", "Ubicación", 220), ("capacidad", "Capacidad", 100)
        ]:
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=ancho, anchor="center")
        self.tabla.pack(fill="both", expand=True, pady=12)

        ttk.Button(marco, text="Actualizar lista", command=self.cargar_datos).pack(anchor="e")

    def registrar(self):
        nombre, ubicacion = self.nombre.get().strip(), self.ubicacion.get().strip()
        try:
            capacidad = int(self.capacidad.get())
            if not nombre or not ubicacion or capacidad <= 0:
                raise ValueError
            with conectar() as db:
                db.execute(
                    "INSERT INTO laboratorios(nombre, ubicacion, capacidad) VALUES (?, ?, ?)",
                    (nombre, ubicacion, capacidad)
                )
            self.nombre.set("")
            self.ubicacion.set("")
            self.capacidad.set("")
            self.cargar_datos()
            messagebox.showinfo("Correcto", "Laboratorio registrado.", parent=self)
        except ValueError:
            messagebox.showwarning("Validación", "Completa los campos y coloca una capacidad entera mayor que cero.", parent=self)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo registrar el laboratorio:\n{error}", parent=self)

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        try:
            with conectar() as db:
                filas = db.execute("SELECT id, nombre, ubicacion, capacidad FROM laboratorios ORDER BY id").fetchall()
            for fila in filas:
                self.tabla.insert("", "end", values=tuple(fila))
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron cargar los laboratorios:\n{error}", parent=self)
