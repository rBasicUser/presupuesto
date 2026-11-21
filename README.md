# Presupuesto Personal

Aplicación para diseñar y ejecutar un **presupuesto personal**. El uso consiste en registrar transacciones,que pueden venir de estados de cuenta de instituciones financieras y/o de forma manual clasificar cada movimiento. La aplicación calcula cuánto he gastado en alguna categoría, cuanto puedo gastar por día en lo que queda del mes, mi razón de endeudamiento, ahorro y mi patrimonio. En resumen quiero **entender cómo gasto mi dinero.**

El segundo objetivo es aprender a hacer una app de principio a fin. Parte de un modelo que armé en Excel (`PRESUPUESTO_modelo`). De momento, he aprendido muchísimo sobre Bases de Datos.

## MPV

1. Subir los estados de cuenta de Micoope, BAC, BI y NEXA y digitalizarlos. Los subo a mano porque Micoope no tiene API para desarrolladores, y el estado de cuenta que está disponible para el cliente, no permite entender los movimientos que genera.
2. Clasificar a mano cada movimiento, en la pantalla de vista previa, antes de confirmar la carga.
3. Ver en grande la fecha de la última actualización.
4. Ver el presupuesto diario disponible.

Regla del presupuesto diario:

```
presupuesto diario = (líquido − ahorro − inversión − ya gastado) ÷ días restantes del mes
```

"Líquido" es el dinero con el que arranca el mes. No se restan los gastos fijos pendientes.


### Backlog (después del MVP)

- **Carga**: clasificación por reglas, detección de duplicados, emparejar transferencias entre cuentas propias.

- **Personaliar Presupuesto Personal**: crear subcategorías, presupuestos por subcategoría, evolución del presupuesto mensual (disponible en Q y %), objetivos de ahorro, qué hacer con el dinero cada quincena.

- **Patrimonio e inversiones**: Cálculo de patrimonio personal. Activos y pasivos, evolución mensual del patrimonio, P&L de la cuenta de Interactive Brokers.

- **Deudas**: lista de deudas con proyección de cancelación aportando X extra en N aportaciones, y recomendación de qué deuda amortizar primero con el método avalancha.

- **Gráficas**: Daily Cashflow, Cumulative Daily Cashflow, gastos fijos vs variables, cambio neto en el patrimonio.


## Flujo para actualizar una transacción

1. Parser respectivo
2. Flujo de enriquecimiento (añadir xyz columnas)
3. Insertar

## El modelo de origen (Excel)

La app hereda su lógica de `PRESUPUESTO_modelo`, un libro de Excel con esquema estrella en base devengo.

**Reglas del modelo:**

- Toda transferencia entre cuentas propias son dos filas con el mismo `ID_Transferencia`: una Salida y una Entrada. La salida lleva el tipo de flujo real. La entrada siempre lleva la subcategoría "Transferencia entre cuentas". Si las dos llevaran el tipo de flujo real, se anularían. 

- Para identificar una transferencia, se hará manualmente, indicando con un boton dentro de la aplicación si es transferencia entre cuentas. De momento, para el MVP se va dejar solo indicado que consiste en transferencia entre cuentas. En el backlog quiero incluir que va a incluir un módulo de cuadre las transferencias.

- El pago de la tarjeta no cuenta como gasto. Bajo devengo, el gasto ya se registró el día de la compra; el pago solo baja el efectivo y baja el pasivo.

En la app, emparejar las transferencias entre cuentas propias está en el backlog.

Definiciones:

```
FCF Operativo  = Ingreso − Gasto_Fijo − Gasto_Variable − Impuesto − Interes_Deuda − Comision_Bancaria
FCF Disponible = FCF Operativo − Amortizacion_Principal − CapEx_Personal
FCF Neto       = FCF Disponible − Inversion_Aporte
Patrimonio     = suma del saldo actual de todas las cuentas (los pasivos van en negativo)
```

Tipos de flujo del modelo (hoja `dim_TipoFlujo` de la v10). Cada bandera define cómo participa el flujo en cada medida:

| Tipo_Flujo | Definición | Afecta_Patrimonio | En_FCF_Operativo | En_FCF_Disponible | Es_Transferencia |
|---|---|---|---|---|---|
| Ingreso | Entrada de dinero por trabajo, rendimientos u otros. Aumenta patrimonio. | 1 | 1 | 1 | 0 |
| Gasto_Fijo | Gasto recurrente comprometido (renta, servicios). Destruye patrimonio. | 1 | 1 | 1 | 0 |
| Gasto_Variable | Gasto discrecional. Destruye patrimonio. | 1 | 1 | 1 | 0 |
| Impuesto | Impuestos y contribuciones sociales. Destruye patrimonio. | 1 | 1 | 1 | 0 |
| Interes_Deuda | Costo financiero de la deuda. Destruye patrimonio. | 1 | 1 | 1 | 0 |
| Comision_Bancaria | Comisiones y tarifas. Destruye patrimonio. | 1 | 1 | 1 | 0 |
| Amortizacion_Principal | Pago de capital de deuda. PATRIMONIO-NEUTRO (baja efectivo, baja pasivo) pero consume caja. | 0 | 0 | 1 | 1 |
| CapEx_Personal | Compra de activo durable con cuenta de activo contraparte. PATRIMONIO-NEUTRO, consume caja. | 0 | 0 | 1 | 1 |
| Inversion_Aporte | Aporte a instrumento de inversion o ahorro. PATRIMONIO-NEUTRO. Es un USO del FCF, no una merma. | 0 | 0 | 0 | 1 |
| Transferencia | Movimiento entre cuentas propias. Neutro en todo. Usar en la pierna contraparte de todo par. | 0 | 0 | 0 | 1 |
| Sin_Clasificar | CONTROL: fila sin Tipo_Flujo asignado. Debe llegar a cero. Excluida de toda medida. | 0 | 0 | 0 | 0 |

## Arquitectura Medallion

```
data/bronze/    estado de cuenta en CSV, como lo entrega el banco
      |
      |  parser del banco
      v
data/silver/    CSV con el contrato de salida
      |
      |  carga a la base (pendiente)
      v
data/gold/      presupuesto.db (SQLite)
```

Las columnas de la tabla de movimientos se llenan en tres capas: el parser, el enriquecimiento y la clasificación manual.

`data/` está en `.gitignore` y no se sube al repo.

## Clonar el repo

Requisitos: Python 3 y Git.

Instalar (Windows):

```
git clone https://github.com/rBasicUser/presupuesto
cd presupuesto
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

En macOS o Linux el entorno se activa con `source .venv/bin/activate`.

Crear las carpetas de datos, que no vienen en el repo:

```
mkdir data\bronze
mkdir data\silver
mkdir data\gold
```

Crear la base:

```
python src/presupuesto/db/connection.py
```

El archivo crea la base de datos: `data/gold/presupuesto.db`. Si el archivo ya existe, el script falla porque las tablas ya están creadas. Para rehacer la base, borro el `.db` y lo corro otra vez.

**Correr un parser, desde la raíz del proyecto porque las rutas son relativas:**

```
python src/presupuesto/parsers/bac_credito.py
```

El archivo de entrada, el de salida y el `id_cuenta` se cambian en los parámetros al inicio de cada parser.

## Contrato de salida de los parsers

Todo parser devuelve estas cinco columnas, sin importar el banco:

| Columna | Tipo | Nota |
|---|---|---|
| `fecha` | TEXT | Formato `AAAA-MM-DD` |
| `id_cuenta` | TEXT | Lo defino yo y el parser lo recibe como parámetro |
| `descripcion` | TEXT | |
| `monto` | REAL | |
| `moneda` | TEXT | `GTQ` o `USD` |

## Parsers

### BAC ahorro (`bac_ahorro.py`)

- Lee `data/bronze/CTA_BAC_AHORRO.csv`.
- Toma la moneda y el saldo inicial del encabezado de la cuenta (fila 2 del archivo). `QTZ` pasa a `GTQ`; cualquier otro valor se toma como `USD`.
- Ubica la tabla en la fila "Fecha de Transacción" y la termina en la primera fila que no empieza con una fecha.
- Calcula el monto como crédito menos débito: positivo si entra dinero, negativo si sale.
- Una fila con débito y crédito en cero, o con valor en los dos, queda con monto 0 y `revisar = True`.
- Compara saldo inicial + suma de montos contra el último balance del archivo y avisa si no cuadra. No se detiene.
- Guarda `data/silver/bac_ahorro.csv` con las cinco columnas del contrato más `revisar`.

### BAC tarjeta de crédito (`bac_credito.py`)

- Lee `data/bronze/CTA_BAC_CrED_oct_2026.csv`.
- Ubica la tabla en la fila que empieza con "Date". Arriba de esa fila lee la fecha de corte.
- Separa el saldo anterior ("Previous balance"), las filas que marcan a qué tarjeta pertenecen las transacciones y las transacciones. Termina en la fila "CURRENT".
- Un movimiento sin fecha, por ejemplo una bonificación, recibe la fecha de corte. Una fila sin fecha y con los dos montos en cero se descarta.
- El estado trae una columna en quetzales y otra en dólares. De ahí salen `monto` y `moneda`. El monto conserva el signo que trae el archivo.
- Si una fila trae las dos columnas en cero, o las dos con valor, el parser se detiene con error.
- Cuadre: saldo anterior + transacciones + intereses debe ser igual al saldo al corte, en quetzales y en dólares. Si no cuadra, el parser se detiene.
- Guarda `data/silver/bac_credito.csv` con las cinco columnas del contrato. Mis dos tarjetas comparten el mismo `id_cuenta` (`CTA01`).

### Micoope

Sin parser. El PDF del estado de cuenta solo dice "VISA" y no trae el comercio (por ejemplo "GASOLINERA PUMA"), entonces no hay insumos para sugerir la subcategoría correspondiente. Capturo a mano fecha, descripción y monto. Se deposita en Silver y listo

## Base de datos

SQLite, en un solo archivo: `data/gold/presupuesto.db`. Los nombres van en snake_case y sin tildes. Las fechas se guardan como texto `AAAA-MM-DD`.

| Tabla | Llave primaria | Columnas |
|---|---|---|
|`fact_transaccion` | `id_trx` | `id_trx`, `fecha`, `anio_mes`, `id_cuenta`, `nombre_cuenta`, `subcategoria`, `gran_categoria`, `comentario`, `tipo_flujo`, `tipo_mov`, `signo`, `monto`, `moneda`, `monto_signado` |
| `fact_presupuesto` | `anio_mes` + `subcategoria` | `anio_mes`, `subcategoria`, `gran_categoria`, `tipo_flujo`, `monto` |
| `fact_valuaciones` | `fecha` + `id_cuenta` | `fecha`, `id_cuenta`, `valor_mercado_gtq`, `nota` |
| `dim_tipo_flujo` | `tipo_flujo` | `tipo_flujo`, `definicion`, `afecta_patrimonio`, `en_FCF_operativo`, `en_FCF_disponible`, `es_transferencia_entre_cuentas` |
| `dim_categorias` | `subcategoria` | `gran_categoria`, `subcategoria`, `tipo_flujo` |
| `dim_cuentas` | `id_cuenta` | `id_cuenta`, `nombre_cuenta`, `clase`, `tipo_cuenta`, `saldo_inicial`, `activa`, `saldo_movimiento` |
| `dim_objetivos` | `id_objetivo` | `id_objetivo`, `nombre_objetivo`, `id_cuenta`, `monto_meta`, `fecha_inicio`, `fecha_meta`, `saldo_actual`, `progreso`, `meses_restantes`, `aporte_mensual` |
| `dim_calendario` | `fecha` | `fecha`, `anio`, `mes`, `anio_mes`, `nombre_mes`, `trimestre` |

Notas del esquema:

- `v_objetivos` es una vista sobre `dim_objetivos`. Calcula `progreso`, `meses_restantes` y `aporte_mensual` con la fecha del día cada vez que se consulta.
- `dim_calendario` se llena al crear la base, con un día por fila del 2025-12-01 al 2027-12-31. Solo se llena `fecha`; las demás columnas quedan vacías.
- `moneda` va solo en `fact_transaccion`. Sirve para identificar si la transacción fue en quetzales o en dólares y convertirla a quetzales, porque mi tarjeta de crédito es multimoneda.
- `anio_mes` va sin llave foránea en las tablas de hechos. La granularidad del presupuesto (mes contra día) frente a `dim_calendario` queda para una versión 2.
- `saldo_inicial` vive en `dim_cuentas`. El parser lo detecta en el archivo más antiguo y lo propone, y yo lo confirmo en la vista previa.
- SQLite trae apagada la validación de llaves foráneas. `schema.sql` la activa con `PRAGMA foreign_keys = ON` y hay que activarla en cada conexión.



## Decisiones de diseño

- Python para todo el proyecto.
- SQLite en lugar de CSV para guardar las tablas. Es una base relacional sin servidor: el motor va embebido en Python y la base es un solo archivo.
- Desarrollo bottom-up, por capas, en lugar de una rebanada vertical. Primero van los parsers y la base; la interfaz va al final.
- En el MVP clasifico cada movimiento a mano. La clasificación por reglas queda en el backlog.
- La clasificación ocurre en la pantalla de vista previa, antes de confirmar la carga. Con eso el MVP cabe en un solo flujo de usuario.
- Cada pantalla tiene un botón "Volver" a la pantalla anterior.
- La fecha de la última actualización y el presupuesto diario van en una sola vista, la que se ve al abrir la app.
- El frontend será una página web local, en el navegador. El framework del servidor aún no está elegido.
- Los pagos a la tarjeta desde la cuenta de ahorro se clasifican como transferencia entre cuentas.
- No hay pruebas automatizadas. Decidí saltarme el unit testing.

## Roadmap

Trabajo por sesiones: 1 hora diaria, una sesión cada 2 días. Lo que falta para cerrar el MVP, en orden:

1. Parsers de BI y de NEXA.
2. Carga de la salida de los parsers a SQLite.
3. Enriquecimiento: las columnas que en Excel eran fórmulas se calculan solas.
4. Clasificación manual.
5. Presupuesto diario calculado desde la base.
6. Interfaz del MVP: una pantalla con la fecha de la última actualización y el presupuesto diario.
7. Despliegue mínimo: abrir la app con un comando o un acceso directo, sin pasar por Positron.



### Descartado

- Moneda / tipo de cambio. Queda solo la columna `moneda` de `fact_transaccion`.

## Documentación

- MVP, backlog y roadmap por sesiones: página privada de Notion "APP: Presupuesto Personal".
- Flujos de usuario: archivo de Figma "User-Flows-miPrespuesto".
