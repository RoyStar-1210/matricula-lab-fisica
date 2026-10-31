
import tkinter as tk
from tkinter import ttk


class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Sistema de Matrícula - Laboratorios de Física")
        self.geometry("850x550")
        self.minsize(700, 450)

        self.crear_interfaz()

    def crear_interfaz(self):

        contenedor = ttk.Frame(self, padding=30)
        contenedor.pack(fill="both", expand=True)

        titulo = ttk.Label(
            contenedor,
            text="Sistema de Matrícula",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=15)

        subtitulo = ttk.Label(
            contenedor,
            text="Gestión de Laboratorios de Física",
            font=("Arial", 14)
        )
        subtitulo.pack(pady=10)

        separador = ttk.Separator(
            contenedor,
            orient="horizontal"
        )
        separador.pack(fill="x", pady=20)

        seccion = ttk.LabelFrame(
            contenedor,
            text="Módulos del sistema",
            padding=20
        )
        seccion.pack(fill="x", pady=10)

        modulos = [
            "Gestión de estudiantes y docentes",
            "Gestión de laboratorios y grupos",
            "Inscripción y cancelación de matrículas",
            "Consultas y reportes"
        ]

        for modulo in modulos:
            ttk.Label(
                seccion,
                text="• " + modulo,
                font=("Arial", 11)
            ).pack(anchor="w", pady=5)

        ttk.Button(
            contenedor,
            text="Salir del sistema",
            command=self.destroy
        ).pack(pady=20)
