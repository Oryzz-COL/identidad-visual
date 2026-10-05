# 07 · Documentos Oryzz

Plantillas editables de Word y versiones PDF de ejemplo (A4) del sistema editorial Oryzz v2.0.
Fuente de verdad: `00_Fuente_Maestra/BRAND_SPEC.md` y `tokens.json`.

## Qué hay en cada carpeta

| Carpeta | Plantilla Word (`_PLANTILLA.docx`) | PDF de ejemplo |
|---|---|---|
| 01_Propuesta_Comercial | Portada, contexto, diagnóstico, estrategia, plan 30-60-90, inversión, próximos pasos, condiciones | `_EJEMPLO.pdf` (7 págs., Clínica Dental Arenal, ficticia) |
| 02_Informe_Diagnostico | Resumen con semáforo, hallazgos por canal (Meta, Google, SEO local, reseñas, web, GEO), prioridades | `_EJEMPLO.pdf` (6 págs., Forja Training Club, ficticio) |
| 03_Informe_Mensual | KPIs, gráficos, resultados por canal, qué funcionó / qué cambiamos, siguiente mes | `_EJEMPLO.pdf` (4 págs., Centro Estético Lumen, datos de ejemplo) |
| 04_Caso_de_Estudio | 2 páginas, etiqueta «EJEMPLO» | `_EJEMPLO.pdf` |
| 05_Presupuesto_y_Factura | Presupuesto y factura con datos fiscales en `{{campos}}`, IVA 21 % e IRPF opcional | `Presupuesto_EJEMPLO.pdf`, `Factura_EJEMPLO.pdf` |
| 06_Carta_y_Membrete | Carta con membrete + documento en blanco con membrete | `Carta_EJEMPLO.pdf`, `Documento-en-blanco.pdf` |
| 07_Brief_Onboarding | Cuestionario de arranque con líneas de respuesta y casillas | `Brief-Onboarding.pdf` (imprimible) |
| 08_One_Pagers | Servicios Oryzz (oscuro) y Oryzz Tap (claro) | `One-Pager-Servicios.pdf`, `Oryzz-Tap_One-Pager.pdf` |
| 09_Contrato_de_Servicios | Maqueta con cada cláusula marcada «Texto a revisar por asesor legal» | `_MAQUETA.pdf` |

Los clientes, cifras y testimonios de los PDF son **ficticios** y van marcados como «Documento de ejemplo», «Datos de ejemplo» o «Ejemplo». No los envíes como casos reales.

## Cómo usar las plantillas Word

1. Duplica el `.docx` y renómbralo (`Oryzz_Propuesta_NombreCliente_v1.docx`).
2. Sustituye todo lo que va entre `{{llaves}}` (se ve en azul: estilo de carácter **Campo**). Busca `{{` con Ctrl+B para no dejarte ninguno.
3. Borra las líneas que empiezan por «Guía ·» (instrucciones internas en azul).
4. No cambies colores ni fuentes a mano: usa los estilos de la galería.
5. Exporta a PDF desde Word (Archivo › Exportar › PDF). Revisa que no quede ningún `{{`.

### Estilos incluidos (galería de estilos de Word)

| Estilo | Uso | Especificación |
|---|---|---|
| **Título** | Titular de portada | Space Grotesk Bold 34 pt, tracking −1,2 pt |
| **Subtítulo** | Entradilla de portada | Manrope 12,5 pt, Grafito 600 |
| **Título 1 / 2 / 3** (alias **Encabezado 1 / 2 / 3**) | Titular de sección, subsección y bloque | Space Grotesk Bold 22 / 14 / 11 pt |
| **Cuerpo** (y Normal) | Texto corrido | Manrope 9,5 pt, interlineado 1,35, 6 pt después |
| **Entradilla** | Primer párrafo de sección | Manrope 12 pt, Grafito 600 |
| **Cita** (Quote) | Testimonios y frases | Space Grotesk Medium 14 pt, filete izquierdo Azul IA |
| **Eyebrow** | Etiqueta sobre titulares (`01 · CONTEXTO`) | JetBrains Mono 9 pt, mayúsculas, +1,45 pt |
| **Nota** | Fuentes, letra pequeña | Manrope 9 pt, Grafito 500 |
| **Dato** | Cifra grande en tarjetas | Space Grotesk Medium 26 pt |
| **Aviso legal** | «Texto a revisar por asesor legal» | JetBrains Mono 9 pt sobre ámbar claro |
| **Línea de respuesta** | Huecos para rellenar (brief) | Filete inferior Grafito 200 |
| **Lista Oryzz** / **Lista numerada Oryzz** | Viñetas y pasos | Manrope 9,5 pt |
| **Campo** (carácter) | `{{dato editable}}` | Azul IA |
| **Acento** (carácter) | La palabra resaltada del titular | Azul IA #3B72FF |
| **Tabla Oryzz** (tabla) | Todas las tablas de datos | Ver «Tablas» |
| **Maqueta Oryzz (sin bordes)** (tabla) | Columnas y bloques de maquetación | Sin bordes |

- **Tema de Office «Oryzz»**: colores del tema (Grafito, Azul IA, Cyan, Lima…) y fuentes del tema (Space Grotesk / Manrope). En Diseño › Colores aparecen como primera paleta.
- **Fuentes incrustadas**: cada `.docx` lleva incrustadas Space Grotesk (Regular, Medium, Bold), Manrope (Regular, Bold) y JetBrains Mono (Regular), licencia OFL. Se ven bien aunque el ordenador no las tenga instaladas. La tabla de fuentes declara **Arial** como alternativa (Consolas para la mono) si alguien abre el archivo con un programa que ignora las fuentes incrustadas (Google Docs, Pages). Para editar con comodidad, instala las TTF de `04_Tipografia/TTF_estaticas`.
- Encabezado: logo horizontal + etiqueta del documento. Pie: texto del documento + folio `02 / 07` (campos PAGE y NUMPAGES, se actualizan solos).
- Portadas: la imagen de fondo está anclada detrás del texto (Formato de imagen › Detrás del texto). La ficha inferior es una tabla flotante anclada a la página.
- Verificadas abriéndolas en Microsoft Word 365 y exportando a PDF.

## Reglas del sistema editorial A4

**Márgenes y retícula**
- Márgenes de 20 mm a izquierda y derecha. Arriba 30 mm (el encabezado vive entre 11 y 19 mm), abajo 24 mm (pie a 11 mm). Portadas y one-pagers: 18–20 mm.
- Retícula de **6 columnas** con **medianil de 5 mm** sobre 170 mm útiles (columna = 24,2 mm). Los bloques ocupan 2, 3, 4 o 6 columnas; los titulares, 4 (≈ 111 mm) para que no pasen de 2–3 líneas.
- Composición asimétrica: texto en 3–4 columnas y datos o tablas al lado. Nada de tres tarjetas idénticas como único recurso.

**Jerarquía (siempre en este orden)**
1. Eyebrow mono con número de sección en Azul 600 (`01  CONTEXTO`).
2. Titular (Título 1): una frase, máximo 2–3 líneas, un único fragmento en Azul IA (estilo Acento).
3. Entradilla (12 pt) con la idea de la página.
4. Cuerpo 9,5 pt. **Nunca por debajo de 9 pt** impreso (incluye pies, tablas y notas).

**Tablas («Tabla Oryzz»)**
- Cabecera en JetBrains Mono 9 pt mayúsculas, Grafito 500, con filete inferior de 1 pt en Grafito 950.
- Filas separadas por filete de 0,5 pt en Grafito 100. Sin rellenos alternos ni bordes verticales.
- Cifras alineadas a la derecha, formato español: `1.470,00 €`, `21 %`, `4,8 ★`.
- Fila de total (activa «Fila de totales» en Diseño de tabla): Space Grotesk Bold 11 pt con filete superior de 1 pt.
- Una idea por columna; detalles en gris debajo del concepto, no en columnas nuevas.

**Color en documentos**
- Fondo blanco, texto Grafito 950, secundarios Grafito 600 / 500. Azul IA solo en el acento del titular, números de sección y datos de gráfico. Lima solo como **nodo** (un punto), nunca como texto sobre blanco.
- Semáforo sobrio: solo el punto `●` lleva color (Crítico #E5484D, Mejorable #F2A33A, Correcto #1F9D55) y siempre con su palabra al lado.
- Gráficos: un tono (Azul IA) y el resto en Grafito 200; un solo eje Y; etiqueta solo el primer y el último valor; fuente debajo.

**Contenido**
- Inversión: honorarios de Oryzz separados del presupuesto de anuncios (que el cliente paga directamente a Meta y Google). Importes sin IVA salvo que se indique.
- Condiciones fijas: sin permanencia (30 días de preaviso) y sin resultados garantizados.
- Datos de clientes: con fuente y periodo. Si no están aprobados, se marcan «Ejemplo» o `{{dato}}`.
- Contrato: el texto jurídico es orientativo; no se firma sin revisión de un asesor legal.

## Fuentes y regeneración

- HTML de las versiones PDF: `07_Documentos/_fuente/html/` (CSS en `_fuente/css/oryzz-docs.css`, retícula y componentes documentados en el propio CSS).
- Recursos para Word (logos PNG, fondos de portada, gráficos): `_fuente/recursos_docx/`.
- Regenerar PDF de ejemplo: `python 00_Fuente_Maestra/build/build_documentos_pdf.py`
- Regenerar plantillas Word: `python 00_Fuente_Maestra/build/build_documentos_docx.py` (librería `oryzz_docx.py`).
- Comprobar las plantillas en Word: `powershell -File 00_Fuente_Maestra/build/docx_a_pdf.ps1 -Entrada 07_Documentos -Salida <carpeta>`.
- La antigua skill de documentos (portada navy + Montserrat) queda obsoleta: no se usa para piezas nuevas.
