# controladores/controlador_matricula.py

from modelos.excepciones import CuposAgotadosException, HorarioDuplicadoException
from modelos.matricula import Matricula

class ControladorMatricula:
    def __init__(self):
        self.lista_matriculas = []

    def matricular_estudiante(self, estudiante, grupo):
        # 1. Validación de Cupos (RF-08)
        if len(grupo.inscritos) >= grupo.capacidad_maxima:
            raise CuposAgotadosException()

        # 2. Validación de Cruce de Horarios (RF-09)
        for mat in self.lista_matriculas:
            if mat.estudiante.codigo == estudiante.codigo:
                if (mat.grupo_laboratorio.dia == grupo.dia and 
                    mat.grupo_laboratorio.hora_inicio == grupo.hora_inicio):
                    raise HorarioDuplicadoException()

        # 3. Registro Exitoso (RF-07)
        id_mat = f"MAT-{len(self.lista_matriculas) + 1:03d}"
        nueva_matricula = Matricula(id_mat, estudiante, grupo)
        
        # Añadir al grupo y al sistema
        grupo.inscritos.append(estudiante)
        self.lista_matriculas.append(nueva_matricula)
        
        return nueva_matricula

    def cancelar_matricula(self, id_matricula: str):
        # RF-10: Cancelación de Matrícula y liberación de cupo
        for mat in self.lista_matriculas:
            if mat.id_matricula == id_matricula:
                mat.grupo_laboratorio.inscritos.remove(mat.estudiante)
                self.lista_matriculas.remove(mat)
                return True
        return False

    def generar_reporte_grupo(self, grupo):
        # RF-11: Reporte de asistencia por grupo
        return grupo.inscritos

    def generar_reporte_ocupacion(self, lista_grupos):
        # RF-12: Reporte global de porcentaje de ocupación y vacantes
        reporte = []
        for g in lista_grupos:
            ocupacion = (len(g.inscritos) / g.capacidad_maxima) * 100
            reporte.append({
                "grupo": g.id_grupo,
                "laboratorio": g.nombre_lab,
                "inscritos": len(g.inscritos),
                "capacidad": g.capacidad_maxima,
                "porcentaje": f"{ocupacion:.2f}%"
            })
        return reporte