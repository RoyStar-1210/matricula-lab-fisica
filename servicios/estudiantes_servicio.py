
import sqlite3
from contextlib import closing

from base_datos.conexion import conectar
from modelos.estudiante import Estudiante


class EstudiantesServicio:

    def registrar(self, codigo, nombre, correo, carrera):
        estudiante = Estudiante(
            codigo, nombre, correo, carrera
        )

        with closing(conectar()) as conexion:
            try:
                with conexion:
                    conexion.execute("""
                        INSERT INTO estudiantes
                        (codigo, nombre, correo, carrera)
                        VALUES (?, ?, ?, ?)
                    """, (
                        estudiante.codigo,
                        estudiante.nombre,
                        estudiante.correo,
                        estudiante.carrera
                    ))
            except sqlite3.IntegrityError as error:
                raise ValueError(
                    "El código o correo ya está registrado"
                ) from error

    def listar(self):
        with closing(conectar()) as conexion:
            filas = conexion.execute("""
                SELECT codigo, nombre, correo, carrera
                FROM estudiantes
                ORDER BY nombre
            """).fetchall()

        return [
            Estudiante(
                fila["codigo"],
                fila["nombre"],
                fila["correo"],
                fila["carrera"]
            )
            for fila in filas
        ]

    def actualizar(self, codigo, nombre, correo, carrera):
        estudiante = Estudiante(
            codigo, nombre, correo, carrera
        )

        with closing(conectar()) as conexion:
            try:
                with conexion:
                    resultado = conexion.execute("""
                        UPDATE estudiantes
                        SET nombre = ?, correo = ?, carrera = ?
                        WHERE codigo = ?
                    """, (
                        estudiante.nombre,
                        estudiante.correo,
                        estudiante.carrera,
                        estudiante.codigo
                    ))

                    if resultado.rowcount == 0:
                        raise ValueError(
                            "El estudiante no existe"
                        )

            except sqlite3.IntegrityError as error:
                raise ValueError(
                    "El correo ya está registrado"
                ) from error

    def eliminar(self, codigo):
        with closing(conectar()) as conexion:
            with conexion:
                resultado = conexion.execute("""
                    DELETE FROM estudiantes
                    WHERE codigo = ?
                """, (codigo,))

                if resultado.rowcount == 0:
                    raise ValueError(
                        "El estudiante no existe"
                    )
