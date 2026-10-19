# Guía de marca Oryzz v2.0

El manual de identidad de Oryzz y Oryzz Tap. Es la referencia para crear cualquier pieza: anuncios, posts, reels, correos, propuestas, presentaciones, documentos, papelería o producto.

| Archivo | Qué es | Cuándo usarlo |
|---|---|---|
| `Oryzz_Guia_de_Marca_v2.pdf` | Manual completo: 90 páginas en 16:9, con marcadores PDF por capítulo | Para entender una regla y su porqué, o para entregarlo a un proveedor (diseñador, editor de vídeo, imprenta, agencia) |
| `Oryzz_Guia_de_Marca_Resumen_1_pagina.pdf` | Referencia rápida en A4 apaisado: logo, color, tipografía, voz, botones y las seis reglas de oro | Para tenerla a mano mientras produces, imprimirla o fijarla en un canal del equipo |

## Capítulos del manual

| Capítulo | Incluye |
|---|---|
| Inicio | Portada, cómo usar el manual, índice y el sistema en una página |
| La marca | Plataforma «Sistemas que captan clientes», arquitectura (Oryzz y Oryzz Tap), a quién servimos, personalidad y claims reales |
| Órbita y nodo | El concepto, del símbolo al sistema y la evolución v1 → v2 |
| Logo | Anatomía, construcción, área de respeto, tamaños mínimos, versiones, colorways, fondos y fotos, favicon y avatares, logo animado, usos incorrectos, cómo se escribe el nombre y co-branding |
| Color | Paleta con HEX, RGB, CMYK y Pantone, proporción 60/25/10/5, escalas, gradiente IA, acento lima, matriz de contraste WCAG, botones, temas oscuro y claro, impresión |
| Tipografía | Space Grotesk, Manrope y JetBrains Mono (solo dato técnico), etiquetas en tipo frase, escala, jerarquía, titulares, tamaños mínimos e instalación |
| Sistema gráfico | Órbitas, rutas y nodos, fondos, diagramas, tarjetas dato, iconografía, componentes UI y retícula de maquetación |
| Fotografía | Dirección, sí / no y tratamiento con velo |
| Motion | Curvas, duraciones y reglas para vídeo y edición: rótulos con etiqueta en tipo frase, subtítulos sin caja (BRAND_SPEC §5.8) y la referencia a la skill `editor-oryzz` (repo `Oryzz-COL/Editor`) |
| Voz y tono | Principios, sí / no, glosario, palabras prohibidas, titulares, CTA y correos |
| Aplicaciones | Web, Instagram, carrusel y stories, LinkedIn, email, presentaciones, documentos, papelería, gran formato y merchandising |
| Oryzz Tap | Expresión en claro, producto y piezas, reglas propias y migración |
| Checklists | Diez comprobaciones antes de publicar y plan de migración en cinco fases |
| Archivos del kit | Mapa de carpetas, fuente de verdad y comandos para regenerar |

## Cómo se actualiza

El PDF no se edita a mano. Se genera a partir de los archivos del kit (logos, paleta, tokens, plantillas), así que siempre refleja lo que hay en las carpetas.

```bash
cd Identidad_Visual/00_Fuente_Maestra/build
python guia_marca.py          # manual completo → 01_Guia_de_Marca/Oryzz_Guia_de_Marca_v2.pdf
python guia_extras.py         # resumen de 1 página + espécimen tipográfico (04_Tipografia)
python guia_marca.py --png DIR   # además, PNG de cada página para revisarlas
```

Requisitos: Python 3.9+, `pip install pymupdf pillow`, y Google Chrome o Microsoft Edge instalados (se usan en modo headless para renderizar).

Cada ejecución comprueba que ningún contenido se salga del área útil de la página e informa en consola (`Desbordes: OK`).

**Orden de prioridad si algo no coincide:** `00_Fuente_Maestra/BRAND_SPEC.md` y `tokens.json` → archivos maestros de cada carpeta → este PDF. Si cambias la especificación, regenera la guía.

## Notas

- El manual no usa etiquetas en mayúsculas espaciadas ni numeraciones de capítulo: los capítulos se distinguen por su nombre y el folio va sin ceros (BRAND_SPEC §4).
- Todas las cifras de clientes que aparecen en el manual son **de ejemplo** y van marcadas como tales.
- Las fotografías de `05_Elementos_Graficos/06_Fotografia` son marcadores de posición con el tratamiento aplicado: hay que sustituirlas por fotos reales que cumplan la dirección fotográfica.
- Los correos personales y los teléfonos (`{{juan@oryzz.com}}`, `{{+34 600 000 000}}`) son marcadores editables.
