-- Activa la validación de llaves foráneas.
-- SQLite la trae apagada y hay que activarla en cada conexión.
PRAGMA foreign_keys = ON;

CREATE TABLE fact_presupuesto(
    anio_mes       TEXT NOT NULL,
    subcategoria   TEXT NOT NULL REFERENCES dim_categorias(subcategoria),
    gran_categoria TEXT,
    tipo_flujo     TEXT REFERENCES dim_tipo_flujo(tipo_flujo),
    monto          REAL,
    PRIMARY KEY (anio_mes, subcategoria)
);

CREATE TABLE fact_transaccion(
    id_trx         INTEGER PRIMARY KEY NOT NULL,
    fecha          TEXT REFERENCES dim_calendario(fecha),
    anio_mes       TEXT,
    id_cuenta      TEXT REFERENCES dim_cuentas(id_cuenta),
    nombre_cuenta  TEXT,
    subcategoria   TEXT REFERENCES dim_categorias(subcategoria),
    gran_categoria TEXT,
    comentario     TEXT,
    tipo_flujo     TEXT REFERENCES dim_tipo_flujo(tipo_flujo),
    tipo_mov       TEXT,
    signo          TEXT CHECK (signo IN ('POSITIVE', 'NEGATIVE')),
    monto          REAL,
    moneda         TEXT,
    monto_signado  REAL

);

CREATE TABLE fact_valuaciones(
    fecha             TEXT NOT NULL REFERENCES dim_calendario(fecha),
    id_cuenta         TEXT NOT NULL REFERENCES dim_cuentas(id_cuenta),
    valor_mercado_gtq REAL,
    nota              TEXT,
    PRIMARY KEY (fecha, id_cuenta)
);

CREATE TABLE dim_tipo_flujo(
    tipo_flujo        TEXT PRIMARY KEY NOT NULL,
    definicion        TEXT,
    afecta_patrimonio INTEGER CHECK (afecta_patrimonio IN (0, 1)),
    en_FCF_operativo  INTEGER CHECK (en_FCF_operativo IN (0, 1)),
    en_FCF_disponible INTEGER CHECK (en_FCF_disponible IN (0, 1)),
    es_transferencia_entre_cuentas INTEGER CHECK (es_transferencia_entre_cuentas IN (0, 1))
);

CREATE TABLE dim_categorias(
    gran_categoria TEXT NOT NULL,
    subcategoria   TEXT PRIMARY KEY NOT NULL,
    tipo_flujo     TEXT REFERENCES dim_tipo_flujo(tipo_flujo)
);

CREATE TABLE dim_cuentas(
    id_cuenta           TEXT PRIMARY KEY NOT NULL,
    nombre_cuenta       TEXT,
    clase               TEXT,
    tipo_cuenta         TEXT,
    saldo_inicial       REAL,
    activa              INTEGER CHECK (activa IN (0, 1)),
    saldo_movimiento    REAL
);

CREATE TABLE dim_objetivos(
    id_objetivo     INTEGER PRIMARY KEY,
    nombre_objetivo TEXT,
    id_cuenta       TEXT REFERENCES dim_cuentas(id_cuenta),
    monto_meta      REAL,
    fecha_inicio    TEXT,
    fecha_meta      TEXT,
    saldo_actual    REAL,
    progreso        REAL,
    meses_restantes REAL,
    aporte_mensual  REAL
);

CREATE TABLE dim_calendario (
    fecha       TEXT PRIMARY KEY NOT NULL,
    anio        INTEGER,
    mes         INTEGER,
    anio_mes    TEXT,
    nombre_mes  TEXT,
    trimestre   TEXT
);

WITH RECURSIVE dias(fecha) AS (
    SELECT '2025-12-01'
    UNION ALL
    SELECT date(fecha, '+1 day') FROM dias
    WHERE fecha < '2027-12-31'
)
INSERT INTO dim_calendario (fecha)
SELECT fecha FROM dias;