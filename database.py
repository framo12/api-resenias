import sqlite3

DB_PATH = "feedbacks.db"


def crear_tabla():
    """Crea la tabla de reseñas si todavia no existe"""
    con = sqlite3.connect(DB_PATH)
    con.execute("""
    CREATE TABLE IF NOT EXISTS resenas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    comentario TEXT,
    calificacion TEXT NOT NULL)
    """)
    con.commit()
    con.close()


def get_db():
    """Dependencia de FASTAPI: abre una conexion por peticion y la cierra al final"""
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    try:
        yield con
    finally:
        con.close()