import sqlite3
from pathlib import Path

# Carpeta donde está este archivo: src/presupuesto/db
CARPETA_DB = Path(__file__).resolve().parent

# Raíz del proyecto: subir 3 niveles (db -> presupuesto -> src -> raíz)
RAIZ = CARPETA_DB.parents[2]

# Rutas de los dos archivos
RUTA_SCHEMA = CARPETA_DB / "schema.sql"
RUTA_DB = RAIZ / "data" / "presupuesto.db"


def crear_base():
    # 1. Leer el texto de schema.sql
    texto_schema = RUTA_SCHEMA.read_text(encoding="utf-8")

    # 2. Abrir la base (si presupuesto.db no existe, SQLite lo crea vacío)
    conn = sqlite3.connect(RUTA_DB)

    # 3. Ejecutar todos los CREATE TABLE del archivo
    conn.executescript(texto_schema)

    # 4. Confirmar y cerrar
    conn.commit()
    conn.close()

    print(f"Base creada en: {RUTA_DB}")


# Esto solo corre cuando ejecutas este archivo directamente
if __name__ == "__main__":
    crear_base()