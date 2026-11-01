import tkinter as tk
from tkinter import ttk, messagebox
from base_datos.conexion import conectar


class VentanaGrupos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de grupos de práctica")
        self.geometry("850x500")
        self.transient(master)
        self.labs = {}
        self.horarios = {}
        self.crear_interfaz()
        self.cargar_opciones()
        self.cargar_datos()

    def crear_interfaz(self):
        marco = ttk.Frame(self, padding=15)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text="Registro de grupos de práctica",
                  font=("Arial", 16, "bold")).pack(pady=(0, 12))

        formulario = ttk.LabelFrame(marco, text="Datos del grupo", padding=10)
        formulario.pack(fill="x")
        self.nombre = tk.StringVar()
        self.laboratorio = tk.StringVar()
        self.horario = tk.StringVar()
        self.capacidad = tk.StringVar()

        ttk.Label(formulario, text="Nombre del grupo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(formulario, textvariable=self.nombre, width=22).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(formulario, text="Laboratorio:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.combo_lab = ttk.Combobox(formulario, textvariable=self.laboratorio, state="readonly", width=25)
        self.combo_lab.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(formulario, text="Horario:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_hor = ttk.Combobox(formulario, textvariable=self.horario, state="readonly", width=25)
        self.combo_hor.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(formulario, text="Capacidad:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(formulario, textvariable=self.capacidad, width=10).grid(row=1, column=3, padx=5, pady=5, sticky="w")
        ttk.Button(formulario, text="Registrar grupo", command=self.registrar).grid(row=2, column=3, padx=5, pady=8, sticky="e")

        self.tabla = ttk.Treeview(marco, columns=("id", "nombre", "lab", "horario", "capacidad"),
                                  show="headings", height=12)
        for col, titulo, ancho in [
            ("id", "ID", 45), ("nombre", "Grupo", 160), ("lab", "Laboratorio", 190),
            ("horario", "Horario", 250), ("capacidad", "Capacidad", 100)
        ]:
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=ancho, anchor="center")
        self.tabla.pack(fill="both", expand=True, pady=12)
        ttk.Button(marco, text="Actualizar lista", command=self.actualizar).pack(anchor="e")

    def cargar_opciones(self):
        try:
            with conectar() as db:
                labs = db.execute("SELECT id, nombre, capacidad FROM laboratorios ORDER BY nombre").fetchall()
                horarios = db.execute("SELECT id, dia, hora_inicio, hora_fin FROM horarios ORDER BY dia, hora_inicio").fetchall()
            self.labs = {f"{r['nombre']} (ID {r['id']})": (r["id"], r["capacidad"]) for r in labs}
            self.horarios = {f"{r['dia']} {r['hora_inicio']}-{r['hora_fin']} (ID {r['id']})": r["id"] for r in horarios}
            self.combo_lab["values"] = list(self.labs.keys())
            self.combo_hor["values"] = list(self.horarios.keys())
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron cargar las opciones:\n{error}", parent=self)

    def registrar(self):
        nombre = self.nombre.get().strip()
        try:
            capacidad = int(self.capacidad.get())
            lab = self.labs.get(self.laboratorio.get())
            horario_id = self.horarios.get(self.horario.get())
            if not nombre or not lab or not horario_id or capacidad <= 0:
                raise ValueError
            laboratorio_id, capacidad_lab = lab
            if capacidad > capacidad_lab:
                messagebox.showwarning("Capacidad", "La capacidad del grupo no puede superar la capacidad del laboratorio.", parent=self)
                return
            with conectar() as db:
                db.execute(
                    "INSERT INTO grupos(nombre, laboratorio_id, horario_id, capacidad) VALUES (?, ?, ?, ?)",
                    (nombre, laboratorio_id, horario_id, capacidad)
                )
            self.nombre.set("")
            self.capacidad.set("")
            self.cargar_datos()
            messagebox.showinfo("Correcto", "Grupo registrado.", parent=self)
        except ValueError:
            messagebox.showwarning("Validación", "Completa todos los campos y coloca una capacidad entera mayor que cero.", parent=self)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo registrar el grupo:\n{error}", parent=self)

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        try:
            with conectar() as db:
                filas = db.execute("""
                    SELECT g.id, g.nombre, l.nombre AS laboratorio,
                           h.dia, h.hora_inicio, h.hora_fin, g.capacidad
                    FROM grupos g
                    JOIN laboratorios l ON l.id = g.laboratorio_id
                    JOIN horarios h ON h.id = g.horario_id
                    ORDER BY g.id
                """).fetchall()
            for r in filas:
                horario = f"{r['dia']} {r['hora_inicio']}-{r['hora_fin']}"
                self.tabla.insert("", "end", values=(r["id"], r["nombre"], r["laboratorio"], horario, r["capacidad"]))
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron cargar los grupos:\n{error}", parent=self)

    def actualizar(self):
        self.cargar_opciones()
        self.cargar_datos()
