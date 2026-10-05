import pdfplumber

ruta = "data/raw/ComprobanteCuenta - Agosto - 2026.pdf"

with pdfplumber.open(ruta) as pdf:
    primera_pagina = pdf.pages[0]
    texto = primera_pagina.extract_text()

print(texto)
texto_completo = ""

with pdfplumber.open(ruta) as pdf:
    for pagina in pdf.pages:
        texto_pagina = pagina.extract_text()
        texto_completo = texto_completo + texto_pagina + "\n"

print(texto_completo)
