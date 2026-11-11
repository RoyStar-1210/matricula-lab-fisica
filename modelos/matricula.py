# modelos/matricula.py

from datetime import datetime

class Matricula:
    def __init__(self, id_matricula: str, estudiante, grupo_laboratorio):
        self.id_matricula = id_matricula
        self.estudiante = estudiante             # Objeto Estudiante
        self.grupo_laboratorio = grupo_laboratorio # Objeto GrupoLaboratorio
        self.fecha_inscripcion = datetime.now()

    def __str__(self):
        return f"Matrícula {self.id_matricula} - Estudiante: {self.estudiante.nombre} - Grupo: {self.grupo_laboratorio.id_grupo}"