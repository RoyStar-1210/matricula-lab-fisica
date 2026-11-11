# base_datos/conexion_matricula.py

import sqlite3

class ConexionMatricula:
    def __init__(self, db_name="sistema_matricula.db"):
        self.db_name = db_name
        self.crear_tabla()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        """Crea la tabla de matrículas en SQLite si aún no existe."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matriculas (
                id_matricula TEXT PRIMARY KEY,
                codigo_estudiante TEXT NOT NULL,
                id_grupo TEXT NOT NULL,
                fecha_inscripcion TEXT NOT NULL
            )
        """)
        conexion.commit()
        conexion.close()

    def guardar_matricula(self, matricula):
        """Inserta una nueva matrícula en la base de datos."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO matriculas (id_matricula, codigo_estudiante, id_grupo, fecha_inscripcion)
                VALUES (?, ?, ?, ?)
            """, (
                matricula.id_matricula, 
                matricula.estudiante.codigo, 
                matricula.grupo_laboratorio.id_grupo, 
                str(matricula.fecha_inscripcion)
            ))
            conexion.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conexion.close()

    def eliminar_matricula(self, id_matricula: str):
        """Elimina una matrícula de la base de datos por su ID (RF-10)."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM matriculas WHERE id_matricula = ?", (id_matricula,))
        filas_afectadas = cursor.rowcount
        conexion.commit()
        conexion.close()
        return filas_afectadas > 0

    def obtener_todas(self):
        """Recupera todas las matrículas registradas (RF-12)."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_matricula, codigo_estudiante, id_grupo, fecha_inscripcion FROM matriculas")
        registros = cursor.fetchall()
        conexion.close()
        return registros