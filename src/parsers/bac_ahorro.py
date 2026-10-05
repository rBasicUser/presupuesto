# 1. Leer el archivo línea por línea
ruta = "data/raw/CUENTA_AHORRO_BAC.csv"

with open(ruta, encoding="latin-1") as archivo:
    lineas = archivo.readlines()

# 2. Encontrar el encabezado de la tabla de transacciones
inicio = None

for numero, linea in enumerate(lineas):
    if linea.startswith("Fecha de Transacción"):
        inicio = numero

# 3. La primera transacción está justo después del encabezado
primera_transaccion = inicio + 1

# 4. Encontrar la primera línea vacía después de las transacciones
fin = None

for numero in range(primera_transaccion, len(lineas)):
    if lineas[numero].strip() == "":
        fin = numero
        break

# 5. Extraer solo las líneas de transacciones
lineas_transacciones = lineas[primera_transaccion:fin]

# 6. Separar la primera transacción en columnas
primera = lineas_transacciones[0]
columnas = primera.split(",")

print(columnas)
print(len(columnas))

columnas_limpias = []

for columna in columnas:
    columna_limpia = columna.strip()
    columnas_limpias.append(columna_limpia)

print(columnas_limpias)
