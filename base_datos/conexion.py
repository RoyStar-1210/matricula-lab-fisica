
import sqlite3
from pathlib import Path
from contextlib import closing


RUTA_BD = Path(__file__).resolve().parent / "matricula_fisica.db"


def conectar():
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_bd():
    with closing(conectar()) as conexion:
        with conexion:
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS estudiantes (
                    codigo TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    correo TEXT NOT NULL UNIQUE,
                    carrera TEXT NOT NULL
                )
            """)
