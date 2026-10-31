
from modelos.usuario import Usuario


class Estudiante(Usuario):

    def __init__(self, codigo, nombre, correo, carrera):
        super().__init__(nombre, correo)

        codigo = codigo.strip()
        carrera = carrera.strip()

        if not codigo:
            raise ValueError("El código es obligatorio")

        if not carrera:
            raise ValueError("La carrera es obligatoria")

        self._codigo = codigo
        self._carrera = carrera

    @property
    def codigo(self):
        return self._codigo

    @property
    def carrera(self):
        return self._carrera

    @property
    def rol(self):
        return "Estudiante"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
