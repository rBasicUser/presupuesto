import csv
from datetime import datetime
from pathlib import Path



# Muestra para probar el flujo: salida del parser de tarjeta BAC
RUTA_MUESTRA = r'data/silver/bac_credito.csv'

# Subcategoría con la que sale cada fila antes de la clasificación manual
# (es la subcategoría de control que ya está en seed.sql)
SUBCATEGORIA_INICIAL = "(SIN CLASIFICAR)"


def enriquecer(filas):
    # Recibe las filas con el contrato de salida del parser:
    # fecha, id_cuenta, descripcion, monto, moneda
    # Devuelve las filas con las columnas de fact_transaccion, sin id_trx
    # (id_trx lo asigna SQLite en el paso Insertar)
    enriquecidas = []

    for fila in filas:
        # 1. anio_mes sale de fecha. strptime se detiene con error
        #    si la fecha no viene en AAAA-MM-DD
        fecha = datetime.strptime(fila["fecha"], "%Y-%m-%d")
        anio_mes = fecha.strftime("%Y-%m")

        # 2. Armar la fila con el orden de columnas de fact_transaccion
        enriquecidas.append({
            "fecha": fila["fecha"],
            "anio_mes": anio_mes,
            "id_cuenta": fila["id_cuenta"],
            "subcategoria": SUBCATEGORIA_INICIAL,
            "comentario": fila["descripcion"],
            "monto": float(fila["monto"]),
            "moneda": fila["moneda"],
        })

    return enriquecidas


# Esto solo corre cuando ejecutas este archivo directamente
if __name__ == "__main__":
    # 1. Leer la muestra de silver
    with open(RUTA_MUESTRA, mode="r", encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.DictReader(archivo))

    # 2. Enriquecer en memoria (no se guarda ningún archivo)
    enriquecidas = enriquecer(filas)

    # 3. Revisar el resultado
    print(len(filas), "filas leídas de", RUTA_MUESTRA)
    print(len(enriquecidas), "filas enriquecidas")
    print(enriquecidas[0])
    print(enriquecidas[-1])