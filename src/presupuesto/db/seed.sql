INSERT INTO dim_cuentas(
    id_cuenta,
    nombre_cuenta,
    clase,
    tipo_cuenta,
    saldo_inicial,
    activa,
    saldo_movimiento
)
VALUES
('CTA01', 'BAC - Credito 6641', 'Pasivo', 'Tarjeta_Credito', 0, 1, NULL),
('CTA02', 'BAC - Ahorro', 'Activo', 'Monetaria', 0.00, 1, NULL),
('CTA04', 'G&T - Monetaria', 'Activo', 'Monetaria', 0, 1, NULL),
('CTA05', 'Nexa - Monetaria', 'Activo', 'Monetaria', 1221.21, 1, NULL),
('CTA07', 'BAM - Prestamo', 'Pasivo', 'Prestamo', -50235, 1, NULL),
('CTA08', 'BI - Monetaria', 'Activo', 'Monetaria', 0, 1, NULL),
('CTA09', 'Micoope - Aportaciones', 'Activo', 'Inversion', 700.03, 1, NULL),
('CTA10', 'Micoope - Corriente', 'Activo', 'Monetaria', 0, 1, NULL),
('CTA11', 'Credisiman VISA', 'Pasivo', 'Tarjeta_Credito', -19.59, 1, NULL),
('CTA12', 'FENAFORE', 'Activo', 'Inversión', 0, 1, NULL),
('CTA13', 'Inversiones en Renta Fija', 'Activo', 'Inversión', 0, 1, NULL),
('CTA99', '(SIN CUENTA)', 'Activo', 'Control', NULL, 0, NULL),
('CTA14', 'BAC - Extrafinanciamiento', 'Pasivo', 'Prestamo', 0, 1, NULL),
('CTA15', 'Efectivo', 'Activo', 'Efectivo', 3800, 1, NULL),
('CTA16', 'Micoope - Credito 4592', 'Pasivo', 'Tarjeta_Credito', 0, 1, NULL),
('CTA17', 'Ferranta 12 Apartamento 1607', 'Activo',	'Inversión', 0,1, NULL);

INSERT INTO dim_tipo_flujo(
    tipo_flujo,
    definicion,
    afecta_patrimonio,
    en_fcf_operativo,
    en_fcf_disponible,
    es_transferencia_entre_cuentas
)
VALUES
('Ingreso', 'Entrada de dinero por trabajo, rendimientos u otros. Aumenta patrimonio.', 1, 1, 1, 0),
('Gasto_Fijo', 'Gasto recurrente comprometido (renta, servicios). Destruye patrimonio.', 1, 1, 1, 0),
('Impuesto', 'Impuestos y contribuciones sociales. Destruye patrimonio.', 1, 1, 1, 0),
('Interes_Deuda', 'Costo financiero de la deuda. Destruye patrimonio.', 1, 1, 1, 0),
('Comision_Bancaria', 'Comisiones y tarifas. Destruye patrimonio.', 1, 1, 1, 0),
('Amortizacion_Principal', 'Pago de capital de deuda. PATRIMONIO-NEUTRO (baja efectivo, baja pasivo) pero consume caja.', 0, 0, 1, 1),
('CapEx_Personal', 'Compra de activo durable con cuenta de activo contraparte. PATRIMONIO-NEUTRO, consume caja.', 0, 0, 1, 1),
('Inversion_Aporte', 'Aporte a instrumento de inversion o ahorro. PATRIMONIO-NEUTRO. Es un USO del FCF, no una merma.', 0, 0, 0, 1),
('Transferencia', 'Movimiento entre cuentas propias. Neutro en todo. Usar en la pierna contraparte de todo par.', 0, 0, 0, 1),
('Sin_Clasificar', 'CONTROL: fila sin Tipo_Flujo asignado. Debe llegar a cero. Excluida de toda medida.', 0, 0, 0, 0);

INSERT INTO dim_categorias(
    gran_categoria,
    subcategoria,
    tipo_flujo
)
VALUES
('Ingresos', 'Salario Neto', 'Ingreso'),
('Ingresos', 'Rendimientos financieros', 'Ingreso'),
('Ingresos', 'Otros ingresos', 'Ingreso'),
('Transferencias', 'Transferencia entre cuentas', 'Transferencia'),
('Alimentacion', 'Supermercado', 'Gasto_Variable'),
('Alimentacion', 'Restaurantes y comida rapida', 'Gasto_Variable'),
('Alimentacion', 'Cafe', 'Gasto_Variable'),
('Vivienda', 'Renta', 'Gasto_Fijo'),
('Vivienda', 'Hipoteca - Intereses', 'Interes_Deuda'),
('Vivienda', 'Hipoteca - Capital', 'Amortizacion_Principal'),
('Vivienda', 'Agua', 'Gasto_Fijo'),
('Vivienda', 'Electricidad', 'Gasto_Fijo'),
('Vivienda', 'Mantenimiento y reparaciones', 'Gasto_Variable'),
('Vivienda', 'Menaje y equipamiento', 'Gasto_Variable'),
('Servicios, y Suscripciones', 'Internet', 'Gasto_Fijo'),
('Servicios, y Suscripciones', 'Telefono', 'Gasto_Fijo'),
('Servicios, y Suscripciones', 'Streaming y aplicaciones', 'Gasto_Fijo'),
('Transporte', 'Combustible', 'Gasto_Variable'),
('Transporte', 'Mantenimiento vehicular', 'Gasto_Variable'),
('Transporte', 'Parqueo y peajes', 'Gasto_Variable'),
('Transporte', 'Movilidad (Uber)', 'Gasto_Variable'),
('Transporte', 'Viaticos', 'Gasto_Variable'),
('Salud y Bienestar', 'Consultas medicas', 'Gasto_Variable'),
('Salud y Bienestar', 'Medicamentos', 'Gasto_Variable'),
('Salud y Bienestar', 'Suplementos', 'Gasto_Variable'),
('Salud y Bienestar', 'Gimnasio y deportes', 'Gasto_Fijo'),
('Salud y Bienestar', 'Cuidado personal', 'Gasto_Variable'),
('Compras Personales', 'Ropa y calzado', 'Gasto_Variable'),
('Compras Personales', 'Accesorios y joyeria', 'Gasto_Variable'),
('Compras Personales', 'Electronica y accesorios', 'Gasto_Variable'),
('Compras Personales', 'Regalos', 'Gasto_Variable'),
('Compras Personales', 'Mascotas', 'Gasto_Variable'),
('Ocio y Entretenimiento', 'Salidas y eventos', 'Gasto_Variable'),
('Ocio y Entretenimiento', 'Bar y vida nocturna', 'Gasto_Variable'),
('Ocio y Entretenimiento', 'Entretenimiento en pareja', 'Gasto_Variable'),
('Obligaciones Financieras', 'Prestamos - Intereses', 'Interes_Deuda'),
('Obligaciones Financieras', 'Prestamos - Capital', 'Amortizacion_Principal'),
('Obligaciones Financieras', 'Tarjetas - Intereses', 'Interes_Deuda'),
('Obligaciones Financieras', 'Tarjetas - Pago capital', 'Amortizacion_Principal'),
('Obligaciones Financieras', 'Comisiones y tarifas', 'Comision_Bancaria'),
('Obligaciones Financieras', 'Fianzas', 'Gasto_Fijo'),
('Obligaciones Financieras', 'Seguros', 'Gasto_Fijo'),
('Obligaciones Financieras', 'Impuestos y contribuciones', 'Impuesto'),
('Ahorro e Inversion', 'Ahorro general', 'Inversion_Aporte'),
('Ahorro e Inversion', 'Fondo de emergencia', 'Inversion_Aporte'),
('Ahorro e Inversion', 'Inversiones bursatiles', 'Inversion_Aporte'),
('Ahorro e Inversion', 'Provision para vehiculo', 'Inversion_Aporte'),
('Ahorro e Inversion', 'Fondo de Retiro', 'Inversion_Aporte'),
('Educacion', 'Universidad Rafael Landivar', 'Gasto_Fijo'),
('Educacion', 'Certificaciones y cursos', 'Gasto_Variable'),
('Donaciones', 'Donaciones', 'Gasto_Variable'),
('(CONTROL)', '(SIN CLASIFICAR)', 'Sin_Clasificar');

INSERT INTO dim_objetivos(
id_objetivo,
nombre_objetivo,
id_cuenta,
monto_meta,
fecha_inicio,
fecha_meta,
saldo_actual,
progreso,
meses_restantes,
aporte_mensual
)
VALUES
('OBJ01','Enganche apartamento Ferranta 12', 'Inversión','CT017','36600','2026-10-01','2028-06-01',3000,NULL,NULL,NULL)
    
