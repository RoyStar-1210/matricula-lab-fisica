# modelos/excepciones.py

class CuposAgotadosException(Exception):
    """Excepción lanzada cuando un grupo de laboratorio alcanzó su aforo máximo."""
    def __init__(self, mensaje="Error: El grupo de laboratorio seleccionado ya no cuenta con cupos vacantes."):
        super().__init__(mensaje)

class HorarioDuplicadoException(Exception):
    """Excepción lanzada cuando hay un cruce de horarios con otra matrícula existente."""
    def __init__(self, mensaje="Error: Ya estás inscrito en otro laboratorio en el mismo día y hora."):
        super().__init__(mensaje)

class EstudianteNoEncontradoException(Exception):
    """Excepción lanzada si el estudiante no está registrado en el sistema."""
    def __init__(self, mensaje="Error: El código de estudiante ingresado no existe."):
        super().__init__(mensaje)

class YaMatriculadoException(Exception):
    """Excepción lanzada si el alumno intenta matricularse dos veces en el mismo grupo."""
    def __init__(self, mensaje="Error: El estudiante ya se encuentra matriculado en este grupo."):
        super().__init__(mensaje)                