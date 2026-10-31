
from abc import ABC, abstractmethod


class Usuario(ABC):

    def __init__(self, nombre, correo):
        nombre = nombre.strip()
        correo = correo.strip().lower()

        if not nombre:
            raise ValueError("El nombre es obligatorio")

        if "@" not in correo:
            raise ValueError("El correo no es válido")

        self._nombre = nombre
        self._correo = correo

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    @abstractmethod
    def rol(self):
        pass


class Administrador(Usuario):

    @property
    def rol(self):
        return "Administrador"
