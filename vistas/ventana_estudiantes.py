
import tkinter as tk
from tkinter import ttk, messagebox

from servicios.estudiantes_servicio import EstudiantesServicio


class VentanaEstudiantes(tk.Toplevel):

    def __init__(self, principal):
        super().__init__(principal)

        self.title("Gestión de Estudiantes")
        self.geometry("850x550")
        self.servicio = EstudiantesServicio()

        self.variables = {
            campo: tk.StringVar()
            for campo in ("codigo", "nombre", "correo", "carrera")
        }

        self.crear_interfaz()
        self.cargar_estudiantes()

    def crear_interfaz(self):
        marco = ttk.Frame(self, padding=20)
        marco.pack(fill="both", expand=True)

        ttk.Label(
            marco,
            text="Gestión de Estudiantes",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=15)

        campos = [
            ("Código:", "codigo"),
            ("Nombre:", "nombre"),
            ("Correo:", "correo"),
            ("Carrera:", "carrera")
        ]

        for i, (etiqueta, campo) in enumerate(campos, start=1):
            ttk.Label(
                marco, text=etiqueta
            ).grid(row=i, column=0, sticky="w", pady=5)

            entrada = ttk.Entry(
                marco,
                textvariable=self.variables[campo],
                width=45
            )
            entrada.grid(row=i, column=1, sticky="ew", pady=5)

            if campo == "codigo":
                self.entrada_codigo = entrada

        botones = ttk.Frame(marco)
        botones.grid(row=5, column=0, columnspan=2, pady=15)

        acciones = [
            ("Registrar", self.registrar),
            ("Actualizar", self.actualizar),
            ("Eliminar", self.eliminar),
            ("Limpiar", self.limpiar)
        ]

        for texto, comando in acciones:
            ttk.Button(
                botones, text=texto, command=comando
            ).pack(side="left", padx=5)

        columnas = ("codigo", "nombre", "correo", "carrera")

        self.tabla = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings"
        )

        for columna in columnas:
            self.tabla.heading(
                columna,
                text=columna.capitalize()
            )
            self.tabla.column(columna, width=160)

        self.tabla.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="nsew"
        )

        self.tabla.bind(
            "<<TreeviewSelect>>", self.seleccionar
        )

        marco.columnconfigure(1, weight=1)
        marco.rowconfigure(6, weight=1)

    def obtener_datos(self):
        return {
            campo: variable.get().strip()
            for campo, variable in self.variables.items()
        }

    def cargar_estudiantes(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for estudiante in self.servicio.listar():
            self.tabla.insert(
                "", "end",
                values=(
                    estudiante.codigo,
                    estudiante.nombre,
                    estudiante.correo,
                    estudiante.carrera
                )
            )

    def registrar(self):
        try:
            self.servicio.registrar(**self.obtener_datos())
        except ValueError as error:
            messagebox.showerror("Error", str(error), parent=self)
            return

        messagebox.showinfo(
            "Éxito", "Estudiante registrado", parent=self
        )
        self.cargar_estudiantes()
        self.limpiar()

    def actualizar(self):
        try:
            self.servicio.actualizar(**self.obtener_datos())
        except ValueError as error:
            messagebox.showerror("Error", str(error), parent=self)
            return

        messagebox.showinfo(
            "Éxito", "Estudiante actualizado", parent=self
        )
        self.cargar_estudiantes()
        self.limpiar()

    def eliminar(self):
        codigo = self.variables["codigo"].get().strip()

        if not codigo:
            messagebox.showwarning(
                "Aviso", "Selecciona un estudiante", parent=self
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmación",
            "¿Deseas eliminar este estudiante?",
            parent=self
        )

        if not confirmar:
            return

        try:
            self.servicio.eliminar(codigo)
        except ValueError as error:
            messagebox.showerror("Error", str(error), parent=self)
            return

        self.cargar_estudiantes()
        self.limpiar()

    def seleccionar(self, evento):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0], "values"
        )

        for campo, valor in zip(self.variables, valores):
            self.variables[campo].set(valor)

        self.entrada_codigo.configure(state="readonly")

    def limpiar(self):
        self.entrada_codigo.configure(state="normal")

        for variable in self.variables.values():
            variable.set("")

        self.tabla.selection_remove(self.tabla.selection())
