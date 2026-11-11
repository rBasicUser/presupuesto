# Parser BAC - Ahorro
# Lee el estado de cuenta de ahorro BAC (CSV) desde bronze
# y lo guarda en silver con el contrato de salida:
# fecha, id_cuenta, descripcion, monto, moneda (+ revisar)

import csv
from datetime import datetime

# 0. Parámetros
ruta = "data/bronze/CTA_BAC_AHORRO.csv"
ruta_salida = "data/silver/bac_ahorro.csv"
id_cuenta = "CTA_XX"  # <- pon aquí el id_cuenta de tu cuenta de ahorro BAC


# 1. Leer el archivo
with open(ruta, mode= 'r', encoding= "latin-1") as filas:
    datos = filas.readlines()

# 1.1 Leer el encabezado de la cuenta (fila 2 del archivo): moneda y saldo inicial
encabezado = next(csv.reader(datos[1:2], skipinitialspace = True))
moneda_archivo = encabezado[3].strip()          # "QTZ"
saldo_inicial = float(encabezado[4].strip())    # 109.57

if moneda_archivo == "QTZ":
    moneda = "GTQ"
else:
    moneda = "USD"

print("Moneda de la cuenta: ", moneda)
print("Saldo inicial propuesto: ", saldo_inicial)

# 2. Recorrer las filas para detectar "Fecha de Transacción"

inicio = None

for fila in datos:
    if fila.__contains__("Fecha de Transacción"):
        inicio = datos.index(fila)
        print("Esta fila tiene la primera transacción: ",inicio)
        break

# 2.1 Detectar dónde termina la tabla
final = None

for transaccion in datos[inicio + 1:]:
    fecha_texto = transaccion.split(",")[0].strip()
    try:
        datetime.strptime(fecha_texto, "%d/%m/%Y")
    except ValueError:  # no es fecha
        final = datos.index(transaccion, inicio + 1)
        print("A la mierda entonces, aquí termina el archivo: ", final)
        break

# Si el archivo termina justo en la última transacción (sin línea vacía)
if final is None:
    final = len(datos)

# 3. Tener los datos como tabla (sin la fila de encabezado: inicio + 1)

print("Transformar los datos en tabla")

nombres = ["fecha", "referencia", "codigo", "descripcion", "debito", "credito", "balance"]
tabla = csv.DictReader(datos[inicio + 1:final], fieldnames = nombres, skipinitialspace = True)
print("Se lee sin problemas")

# 4. Construir los movimientos con el contrato de salida

movimientos = []

for transaccion in tabla:
    fecha = datetime.strptime(transaccion["fecha"].strip(), "%d/%m/%Y").date().isoformat()
    descripcion = transaccion["descripcion"].strip()
    debito = float(transaccion["debito"].strip())
    credito = float(transaccion["credito"].strip())

    # Monto: entra dinero = positivo, sale dinero = negativo
    # Anomalía: ambos en cero o ambos distintos de cero -> monto 0 y se marca para revisión
    if (debito == 0 and credito == 0) or (debito != 0 and credito != 0):
        monto = 0.0
        revisar = True
    else:
        monto = credito - debito
        revisar = False

    movimientos.append({
        "fecha": fecha,
        "id_cuenta": id_cuenta,
        "descripcion": descripcion,
        "monto": round(monto, 2),
        "moneda": moneda,
        "revisar": revisar,
    })

print("Movimientos leídos: ", len(movimientos))

# 5. Validar contra el saldo final del archivo
# saldo inicial + suma de montos debe ser igual al último balance

saldo_calculado = round(saldo_inicial + sum(m["monto"] for m in movimientos), 2)
saldo_archivo = float(datos[final - 1].split(",")[-1].strip())

if saldo_calculado == saldo_archivo:
    print("Cuadra el saldo: ", saldo_calculado)
else:
    print("NO cuadra el saldo. Calculado: ", saldo_calculado, " Archivo: ", saldo_archivo)

# 6. Guardar en silver

columnas = ["fecha", "id_cuenta", "descripcion", "monto", "moneda", "revisar"]

with open(ruta_salida, mode= 'w', encoding= "utf-8", newline= "") as salida:
    escritor = csv.DictWriter(salida, fieldnames = columnas)
    escritor.writeheader()
    escritor.writerows(movimientos)

print("Archivo guardado en: ", ruta_salida)