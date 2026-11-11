# vistas/ventana_matricula.py

import tkinter as tk
from tkinter import messagebox, ttk
from controladores.controlador_matricula import ControladorMatricula
from modelos.excepciones import (
    CuposAgotadosException, 
    HorarioDuplicadoException, 
    EstudianteNoEncontradoException, 
    YaMatriculadoException
)

class VentanaMatricula(tk.Toplevel):
    def __init__(self, parent, controlador: ControladorMatricula):
        super().__init__(parent)
        self.controlador = controlador
        self.title("Módulo de Matrículas - Laboratorios de Física")
        self.geometry("650x500")
        self.config(bg="#f4f6f9")

        # Título de la sección
        titulo = tk.Label(self, text="Gestión e Inscripción de Matrículas", font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#333")
        titulo.pack(pady=15)

        # --- Frame del Formulario ---
        frame_form = tk.LabelFrame(self, text=" Datos de Inscripción ", font=("Arial", 11, "bold"), bg="#f4f6f9", padx=15, pady=15)
        frame_form.pack(fill="x", padx=20, pady=10)

        # Entrada Código Estudiante
        tk.Label(frame_form, text="Código de Estudiante:", bg="#f4f6f9", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.txt_codigo = tk.Entry(frame_form, font=("Arial", 10), width=25)
        self.txt_codigo.grid(row=0, column=1, pady=5, padx=10)

        # Entrada ID Grupo de Laboratorio
        tk.Label(frame_form, text="ID de Grupo Laboratorio:", bg="#f4f6f9", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.txt_grupo = tk.Entry(frame_form, font=("Arial", 10), width=25)
        self.txt_grupo.grid(row=1, column=1, pady=5, padx=10)

        # Botón de Matricular
        btn_matricular = tk.Button(frame_form, text="Registrar Matrícula", bg="#28a745", fg="white", font=("Arial", 10, "bold"), command=self.ejecutar_matricula, width=20)
        btn_matricular.grid(row=2, column=0, columnspan=2, pady=15)

        # --- Frame de Listado / Tabla ---
        frame_tabla = tk.LabelFrame(self, text=" Matrículas Registradas ", font=("Arial", 11, "bold"), bg="#f4f6f9", padx=10, pady=10)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        # Tabla (Treeview)
        columns = ("ID", "Estudiante", "Grupo", "Fecha")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, side="left")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Botón Cancelar Matrícula Seleccionada
        btn_cancelar = tk.Button(self, text="Cancelar Matrícula Seleccionada", bg="#dc3545", fg="white", font=("Arial", 10, "bold"), command=self.ejecutar_cancelacion)
        btn_cancelar.pack(pady=10)

    def ejecutar_matricula(self):
        codigo = self.txt_codigo.get().strip()
        id_grupo = self.txt_grupo.get().strip()

        if not codigo or not id_grupo:
            messagebox.showerror("Error de Validación", "Por favor completa todos los campos del formulario.")
            return

        # Clases simuladas de apoyo para la prueba de interfaz (pueden enlazarse con los objetos reales de tus compañeros)
        class EstudianteMock:
            def __init__(self, codigo):
                self.codigo = codigo
                self.nombre = f"Estudiante {codigo}"

        class GrupoMock:
            def __init__(self, id_grupo):
                self.id_grupo = id_grupo
                self.nombre_lab = "Física General"
                self.dia = "Lunes"
                self.hora_inicio = "08:00"
                self.capacidad_maxima = 2
                self.inscritos = []

        try:
            estudiante = EstudianteMock(codigo)
            grupo = GrupoMock(id_grupo) # En integración final, se obtiene del controlador del Integrante 2

            # Ejecutamos la lógica del controlador (incluyendo validaciones y SQLite)
            nueva_mat = self.controlador.matricular_estudiante(estudiante, grupo)
            
            # Actualizamos la tabla visual
            self.tree.insert("", "end", values=(nueva_mat.id_matricula, nueva_mat.estudiante.codigo, nueva_mat.grupo_laboratorio.id_grupo, str(nueva_mat.fecha_inscripcion)[:19]))
            
            messagebox.showinfo("Éxito", f"¡Matrícula registrada correctamente!\nID: {nueva_mat.id_matricula}")
            self.txt_codigo.delete(0, tk.END)
            self.txt_grupo.delete(0, tk.END)

        except (CuposAgotadosException, HorarioDuplicadoException, EstudianteNoEncontradoException, YaMatriculadoException) as e:
            messagebox.showwarning("Advertencia de Negocio", str(e))
        except Exception as ex:
            messagebox.showerror("Error Crítico", str(ex))

    def ejecutar_cancelacion(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Por favor selecciona una matrícula de la tabla para cancelar.")
            return

        item = self.tree.item(seleccion)
        id_matricula = item['values'][0]

        exito = self.controlador.cancelar_matricula(id_matricula)
        if exito:
            self.tree.delete(seleccion)
            messagebox.showinfo("Información", f"La matrícula {id_matricula} ha sido anulada con éxito.")
        else:
            messagebox.showerror("Error", "No se pudo anular la matrícula en el sistema.")