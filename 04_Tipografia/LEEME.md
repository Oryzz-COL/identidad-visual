# 04 · Tipografía Oryzz

Tres familias libres, cada una con un papel:

| Familia | Papel | Pesos en uso | Dónde |
|---|---|---|---|
| **Space Grotesk** | Display: titulares, cifras grandes y el logo | 500 · 600 · 700 (300 y 400 solo en cifras muy grandes) | Web, slides, redes, portadas |
| **Manrope** | Texto: párrafos, interfaz y documentos | 400 · 500 · 600 · 700 (800 solo en botones grandes) | Todo lo que se lee |
| **JetBrains Mono** | Datos: eyebrows en MAYÚSCULAS, métricas, códigos y URLs | 400 · 500 (700 solo para destacar un dato en una tabla) | Etiquetas, tablas, KPI |

Espécimen completo, con la escala y los pares de ejemplo: **`Oryzz_Especimen_Tipografico.pdf`** (8 páginas).

## Contenido de la carpeta

| Carpeta / archivo | Contenido |
|---|---|
| `TTF_estaticas/` | 13 TTF: Space Grotesk (Light, Regular, Medium, SemiBold, Bold), Manrope (Regular, Medium, SemiBold, Bold, ExtraBold), JetBrains Mono (Regular, Medium, Bold) |
| `Variables/` | Las tres familias en fuente variable (`*-VF.ttf`), para diseño y web |
| `Licencias/` | Texto de la SIL Open Font License 1.1 de cada familia |
| `Oryzz_Especimen_Tipografico.pdf` | Espécimen 16:9 |

## Instalación

**Windows**
1. Abre `TTF_estaticas/`, selecciona todas las fuentes (Ctrl+A).
2. Clic derecho › **Instalar para todos los usuarios** (o «Instalar» si no tienes permisos de administrador).
3. Cierra y vuelve a abrir Word, PowerPoint o el programa que estés usando.

**Mac**
1. Selecciona las TTF y haz doble clic.
2. Pulsa **Instalar** en Catálogo Tipográfico. Para varias a la vez, arrástralas a Catálogo Tipográfico.

**Google Fonts**
Las tres familias están en [fonts.google.com](https://fonts.google.com): Space Grotesk, Manrope y JetBrains Mono.

## Uso por herramienta

| Herramienta | Cómo |
|---|---|
| **Word y PowerPoint** | Las plantillas de `06_Presentaciones` y `07_Documentos` llevan las fuentes incrustadas y sus estilos. Instálalas igualmente para editar con comodidad. Si alguien abre un archivo sin ellas, se ve en **Arial** (y **Consolas** para la mono). |
| **Google Docs y Slides** | Menú de fuentes › **Más fuentes** › busca y añade las tres. Las fuentes incrustadas de un .docx o .pptx no viajan a Google: aplica las de Google tras importar. |
| **Canva** | Canva Pro › **Brand Kit** › Fuentes › Subir las TTF de `TTF_estaticas/`. Asigna Space Grotesk a «Título», Manrope a «Cuerpo». |
| **Figma** | Con las fuentes instaladas en el equipo (o el instalador de fuentes de Figma) aparecen en el selector. También están en el catálogo de Google Fonts de Figma. |
| **Editores de vídeo** (CapCut, Premiere, DaVinci, After Effects) | Instala las TTF en el sistema y reinicia el editor. Rótulos: eyebrow en JetBrains Mono + titular en Space Grotesk. Subtítulos: Manrope Bold. |
| **Web** | Usa `11_Web_y_Codigo/fonts/` con `@font-face` (WOFF2) o Google Fonts con `display=swap`. Alternativas de la pila: `Arial, Helvetica, sans-serif` y `Consolas, 'Courier New', monospace`. |

## Reglas rápidas

- Titulares: Space Grotesk 700, tracking negativo (−0,045 em a 96 px, −0,035 em a 56 px, −0,02 em a 28 px), 2–3 líneas como máximo, un solo fragmento en azul.
- Cuerpo: Manrope 400, 16 px en web (interlineado 1,6), 9,5 pt en A4, ≥ 36 px en slides 1920×1080.
- Eyebrow: JetBrains Mono 500, 12 px en web y 20 px en slides, MAYÚSCULAS, +0,16 em. Es la única excepción al mínimo de 14 px.
- Tamaños mínimos: 14 px en pantalla · 9 pt impreso · 24 px en slides (36 px para leer).
- Nunca frases enteras en gradiente ni en MAYÚSCULAS.

## Licencia

Las tres familias están bajo la **SIL Open Font License 1.1**: se pueden usar comercialmente, incrustar en documentos y compartir con proveedores sin coste. Lo único que no se permite es venderlas por separado. Textos completos en `Licencias/`.

## Retiradas en la v2

Syne, Outfit, Montserrat, DM Sans y Poppins ya no forman parte de la marca. Si aparecen en una pieza, es una pieza antigua y hay que migrarla (ver `12_Auditoria_y_Mejoras`).
