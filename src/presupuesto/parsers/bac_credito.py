import csv
from datetime import datetime
from decimal import Decimal

# 1. Ruta del archivo
ruta = "data/bronze/CTA_BAC_CrED_oct_2026.csv"

# 2. Cargar archivo
with open(ruta, mode="r", encoding="utf-8-sig") as archivo:
    filas = archivo.readlines()

# 3. Encontrar el encabezado
inicio = None
for numero, fila in enumerate(filas):
    if fila.startswith("Date"):
        inicio = numero
        break

if inicio is None:
    raise ValueError("No se encontró el encabezado 'Date'")

# 4. Leer la fecha de corte (bloque de resumen arriba del encabezado 'Date')
resumen_superior = list(csv.DictReader(filas[:inicio], skipinitialspace=True))
fecha_corte = datetime.strptime(resumen_superior[0]["Date"].strip(), "%d/%m/%Y").date()

# 5. Validar el encabezado original y renombrar columnas
encabezado = next(csv.reader([filas[inicio]]))

if len(encabezado) != 4:
    raise ValueError(f"Se esperaban 4 columnas y hay {len(encabezado)}")

nombres = ["fecha", "descripcion", "monto_quetzales", "monto_dolares"]
datos = list(csv.DictReader(filas[inicio + 1:], fieldnames=nombres))

# 6. Clasificar filas: saldo anterior, tarjeta, transacciones y final
saldo_anterior = None
tarjeta = None
transacciones = []
fin = None

for numero, fila in enumerate(datos):
    fecha = fila["fecha"].strip()
    descripcion = fila["descripcion"].strip()

    if fecha.startswith("CURRENT"):
        fin = numero
        break  # aquí empieza el resumen de intereses: se acabaron las transacciones

    if descripcion == "Previous balance":
        saldo_anterior = fila
        continue  # el saldo anterior no es una transacción

    if "**-****-" in descripcion:
        tarjeta = descripcion[-4:]
        continue  # fila separadora: las siguientes transacciones son de esta tarjeta

    fila["tarjeta"] = tarjeta
    transacciones.append(fila)

if fin is None:
    raise ValueError("No se encontró la fila 'CURRENT Interest'")

if saldo_anterior is None:
    raise ValueError("No se encontró la fila 'Previous balance'")

# 7. Convertir tipos de dato
registros = []
for fila in transacciones:
    fecha = fila["fecha"].strip()
    quetzales = fila["monto_quetzales"].replace(",", "").strip()
    dolares = fila["monto_dolares"].replace(",", "").strip()

    monto_quetzales = Decimal(quetzales) if quetzales else None
    monto_dolares = Decimal(dolares) if dolares else None

    if not fecha and monto_quetzales == 0 and monto_dolares == 0:
        continue  # fila informativa sin fecha ni monto (puntos, cashback)

    registros.append({
        "fecha": datetime.strptime(fecha, "%d/%m/%Y").date() if fecha else fecha_corte,  # sin fecha: fecha de corte
        "tarjeta": fila["tarjeta"],
        "descripcion": fila["descripcion"].strip(),
        "monto_quetzales": monto_quetzales,
        "monto_dolares": monto_dolares,
    })

# 8. Leer intereses y saldo al corte (la fila debajo de 'CURRENT Interest')
# DictReader le puso nuestros nombres, pero en esta fila cada columna significa otra cosa
resumen = datos[fin + 1]
interes_quetzales = Decimal(resumen["fecha"].replace(",", "").strip())
interes_dolares = Decimal(resumen["descripcion"].replace(",", "").strip())
saldo_corte_quetzales = Decimal(resumen["monto_quetzales"].replace(",", "").strip())
saldo_corte_dolares = Decimal(resumen["monto_dolares"].replace(",", "").strip())

# 9. Cuadre: saldo anterior + transacciones + intereses = saldo al corte
total_quetzales = Decimal(saldo_anterior["monto_quetzales"].replace(",", "").strip())
total_dolares = Decimal(saldo_anterior["monto_dolares"].replace(",", "").strip())

for registro in registros:
    total_quetzales += registro["monto_quetzales"] or 0
    total_dolares += registro["monto_dolares"] or 0

total_quetzales += interes_quetzales
total_dolares += interes_dolares

if total_quetzales != saldo_corte_quetzales:
    raise ValueError(f"No cuadra en quetzales: {total_quetzales} vs {saldo_corte_quetzales}")

if total_dolares != saldo_corte_dolares:
    raise ValueError(f"No cuadra en dólares: {total_dolares} vs {saldo_corte_dolares}")

print(len(registros), "transacciones")
print("Cuadre OK:", saldo_corte_quetzales, "Q /", saldo_corte_dolares, "USD")
print(registros[0])
print(registros[-1])