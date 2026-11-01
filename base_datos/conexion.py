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
    """Crea las tablas del módulo de laboratorios sin eliminar estudiantes."""
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
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS laboratorios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    ubicacion TEXT NOT NULL,
                    capacidad INTEGER NOT NULL CHECK(capacidad > 0)
                )
            """)
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS horarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dia TEXT NOT NULL,
                    hora_inicio TEXT NOT NULL,
                    hora_fin TEXT NOT NULL,
                    CHECK(hora_inicio < hora_fin)
                )
            """)
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS grupos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    laboratorio_id INTEGER NOT NULL,
                    horario_id INTEGER NOT NULL,
                    capacidad INTEGER NOT NULL CHECK(capacidad > 0),
                    FOREIGN KEY(laboratorio_id) REFERENCES laboratorios(id),
                    FOREIGN KEY(horario_id) REFERENCES horarios(id)
                )
            """)
