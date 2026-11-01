import tkinter as tk
from tkinter import ttk


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Matrícula - Laboratorios de Física")
        self.geometry("850x600")
        self.minsize(700, 500)
        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = ttk.Frame(self, padding=30)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(contenedor, text="Sistema de Matrícula",
                  font=("Arial", 24, "bold")).pack(pady=15)
        ttk.Label(contenedor, text="Gestión de Laboratorios de Física",
                  font=("Arial", 14)).pack(pady=10)
        ttk.Separator(contenedor, orient="horizontal").pack(fill="x", pady=15)

        seccion = ttk.LabelFrame(contenedor, text="Módulos del sistema", padding=18)
        seccion.pack(fill="x", pady=8)

        modulos = [
            "Gestión de estudiantes y docentes",
            "Gestión de laboratorios y grupos",
            "Inscripción y cancelación de matrículas",
            "Consultas y reportes"
        ]
        for modulo in modulos:
            ttk.Label(seccion, text="• " + modulo, font=("Arial", 10)).pack(anchor="w", pady=3)

        botones = ttk.Frame(contenedor)
        botones.pack(pady=12)
        ttk.Button(botones, text="Gestionar estudiantes",
                   command=self.abrir_estudiantes).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(botones, text="Gestionar laboratorios",
                   command=self.abrir_laboratorios).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(botones, text="Gestionar horarios",
                   command=self.abrir_horarios).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(botones, text="Gestionar grupos",
                   command=self.abrir_grupos).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(contenedor, text="Salir del sistema",
                   command=self.destroy).pack(pady=12)

    def abrir_estudiantes(self):
        from vistas.ventana_estudiantes import VentanaEstudiantes
        VentanaEstudiantes(self)

    def abrir_laboratorios(self):
        from vistas.ventana_laboratorios import VentanaLaboratorios
        VentanaLaboratorios(self)

    def abrir_horarios(self):
        from vistas.ventana_horarios import VentanaHorarios
        VentanaHorarios(self)

    def abrir_grupos(self):
        from vistas.ventana_grupos import VentanaGrupos
        VentanaGrupos(self)
