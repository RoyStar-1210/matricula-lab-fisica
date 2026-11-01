import tkinter as tk
from tkinter import ttk, messagebox
from base_datos.conexion import conectar


class VentanaHorarios(tk.Toplevel):
    DIAS = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado")

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de horarios")
        self.geometry("700x460")
        self.transient(master)
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        marco = ttk.Frame(self, padding=15)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text="Registro de horarios",
                  font=("Arial", 16, "bold")).pack(pady=(0, 12))

        formulario = ttk.LabelFrame(marco, text="Datos del horario", padding=10)
        formulario.pack(fill="x")
        self.dia = tk.StringVar(value=self.DIAS[0])
        self.inicio = tk.StringVar()
        self.fin = tk.StringVar()

        ttk.Label(formulario, text="Día:").grid(row=0, column=0, padx=5, pady=6, sticky="w")
        ttk.Combobox(formulario, textvariable=self.dia, values=self.DIAS,
                     state="readonly", width=15).grid(row=0, column=1, padx=5, pady=6)
        ttk.Label(formulario, text="Hora inicio (HH:MM):").grid(row=0, column=2, padx=5, pady=6)
        ttk.Entry(formulario, textvariable=self.inicio, width=10).grid(row=0, column=3, padx=5, pady=6)
        ttk.Label(formulario, text="Hora fin (HH:MM):").grid(row=1, column=0, padx=5, pady=6, sticky="w")
        ttk.Entry(formulario, textvariable=self.fin, width=10).grid(row=1, column=1, padx=5, pady=6)
        ttk.Button(formulario, text="Registrar", command=self.registrar).grid(row=1, column=3, padx=5, pady=6)

        self.tabla = ttk.Treeview(marco, columns=("id", "dia", "inicio", "fin"), show="headings", height=12)
        for col, titulo, ancho in [
            ("id", "ID", 60), ("dia", "Día", 180),
            ("inicio", "Hora de inicio", 180), ("fin", "Hora de fin", 180)
        ]:
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=ancho, anchor="center")
        self.tabla.pack(fill="both", expand=True, pady=12)
        ttk.Button(marco, text="Actualizar lista", command=self.cargar_datos).pack(anchor="e")

    def registrar(self):
        dia, inicio, fin = self.dia.get(), self.inicio.get().strip(), self.fin.get().strip()
        try:
            from datetime import datetime
            formato = "%H:%M"
            h_inicio = datetime.strptime(inicio, formato)
            h_fin = datetime.strptime(fin, formato)
            if h_inicio >= h_fin:
                raise ValueError
            with conectar() as db:
                db.execute("INSERT INTO horarios(dia, hora_inicio, hora_fin) VALUES (?, ?, ?)",
                           (dia, inicio, fin))
            self.inicio.set("")
            self.fin.set("")
            self.cargar_datos()
            messagebox.showinfo("Correcto", "Horario registrado.", parent=self)
        except ValueError:
            messagebox.showwarning("Validación", "Usa el formato HH:MM y verifica que la hora final sea posterior a la inicial.", parent=self)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo registrar el horario:\n{error}", parent=self)

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        try:
            with conectar() as db:
                filas = db.execute("SELECT id, dia, hora_inicio, hora_fin FROM horarios ORDER BY id").fetchall()
            for fila in filas:
                self.tabla.insert("", "end", values=tuple(fila))
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron cargar los horarios:\n{error}", parent=self)
