# Oryzz · Identidad visual v2.0

Kit completo de marca de **Oryzz** (agencia de captación de clientes con IA para PYMES) y **Oryzz Tap** (placas y stands NFC + QR). Es la base para crear todo: contenido para redes, edición de vídeo, anuncios, correos, propuestas, presentaciones, documentos, papelería y producto.

> **Empieza aquí:** [`01_Guia_de_Marca/Oryzz_Guia_de_Marca_v2.pdf`](01_Guia_de_Marca/Oryzz_Guia_de_Marca_v2.pdf) (manual de 90 páginas) o, si tienes prisa, el [resumen de una página](01_Guia_de_Marca/Oryzz_Guia_de_Marca_Resumen_1_pagina.pdf).
>
> **Fuente de verdad:** [`00_Fuente_Maestra/BRAND_SPEC.md`](00_Fuente_Maestra/BRAND_SPEC.md) y [`tokens.json`](00_Fuente_Maestra/tokens.json). Si algo no coincide, mandan ellos.

## La marca en 30 segundos

- **Plataforma:** *Sistemas que captan clientes.* Claim: «Más clientes. No más likes.»
- **Concepto visual:** *Órbita y nodo.* La O es una órbita abierta (el sistema en marcha); el nodo lima es el resultado medible (el lead, la cita, el cliente).
- **Color:** 60 % Grafito `#0B0D12` · 25 % Blanco / Grafito 50 · 10 % Azul IA `#3B72FF` / Cyan `#36CFE0` · ≤ 5 % Lima `#BFF24A` (un solo acento por pieza).
- **Tipografía:** Space Grotesk (titulares) · Manrope (texto) · JetBrains Mono (solo datos técnicos). Sin etiquetas en mayúsculas espaciadas ni numeraciones de sección.
- **Voz:** clara, directa, segura, sin humo. Hablamos de clientes, citas, mensajes y euros.

## Mapa del kit

| Carpeta | Contenido |
|---|---|
| [`00_Fuente_Maestra`](00_Fuente_Maestra) | `BRAND_SPEC.md`, `tokens.json`, `brand.css`, fuentes y los scripts de `build/` que generan todo el kit |
| [`01_Guia_de_Marca`](01_Guia_de_Marca) | Manual de marca (PDF 16:9, 90 páginas) y resumen de una página |
| [`02_Logos`](02_Logos) | 91 SVG + PNG y PDF: horizontal, vertical, wordmark, isotipo, avatares, favicon, submarca Tap, animado, láminas de construcción y uso |
| [`03_Color`](03_Color) | Paleta en ASE, GPL, JSON y CSV (HEX, RGB, CMYK, Pantone, contraste), PDF de paleta y contraste |
| [`04_Tipografia`](04_Tipografia) | TTF estáticas y variables, licencias OFL, espécimen tipográfico e instrucciones de instalación |
| [`05_Elementos_Graficos`](05_Elementos_Graficos) | 43 iconos, patrones, 12 fondos, 6 diagramas, componentes de dato y dirección fotográfica |
| [`06_Presentaciones`](06_Presentaciones) | Plantillas PowerPoint (oscura, clara, Oryzz Tap) y deck comercial de ejemplo |
| [`07_Documentos`](07_Documentos) | Plantillas Word A4: propuesta, diagnóstico, informe mensual, caso de estudio, presupuesto, factura, carta, brief, one-pagers y contrato |
| [`08_Email`](08_Email) | 10 plantillas HTML, firmas y guía de redacción |
| [`09_Redes_Sociales`](09_Redes_Sociales) | Generador de piezas desde texto, 71 piezas de ejemplo y guía de contenido |
| [`10_Papeleria_e_Impresion`](10_Papeleria_e_Impresion) | Tarjetas, membrete, sobre, carpeta, pegatinas, tarjeta de producto Tap, roll-up, cartel y merchandising, listos para imprenta |
| [`11_Web_y_Codigo`](11_Web_y_Codigo) | Tokens CSS / SCSS / JSON / Tailwind v4, fuentes web y componentes UI |
| [`12_Auditoria_y_Mejoras`](12_Auditoria_y_Mejoras) | Auditoría de la marca anterior, evidencias y plan de migración |
| [`99_Archivo`](99_Archivo) | Material de la marca anterior, solo como referencia |

Cada carpeta tiene su `LEEME.md` con el detalle de archivos y cómo usarlos.

## Uso rápido según la tarea

| Voy a… | Usa |
|---|---|
| Publicar en Instagram / LinkedIn | `09_Redes_Sociales` (generador) + `Guia_de_contenido_redes.md` |
| Editar un reel o un anuncio en vídeo | Guía cap. 08 (Motion · vídeo y edición), `02_Logos/08_Animado`, zonas seguras en `09_Redes_Sociales/Stories` |
| Escribir un correo | `08_Email/Guia_de_redaccion_email.md` + plantillas |
| Preparar una propuesta o informe | `07_Documentos` (Word) o `06_Presentaciones` (PowerPoint) |
| Tocar la web | `11_Web_y_Codigo` + plan de `12_Auditoria_y_Mejoras` |
| Imprimir | `10_Papeleria_e_Impresion` (PDF de imprenta con sangrado y marcas) |

Antes de publicar cualquier pieza, pasa el **checklist anti «AI slop»** (guía, cap. 12).

## Regenerar el kit

Todo se genera con scripts a partir de la fuente maestra. Requisitos: Python 3.9+, `pip install pymupdf pillow jinja2 qrcode`, y Chrome o Edge.

```bash
cd 00_Fuente_Maestra/build
python oryzz_logo.py && python export_logos.py   # logos
python paleta_archivos.py                        # paleta
python pres_build_all.py                         # presentaciones
python build_papeleria.py                        # papelería
python guia_marca.py                             # manual de marca
python guia_extras.py                            # resumen de 1 página + espécimen tipográfico
python ../../09_Redes_Sociales/_generador/generar.py   # piezas de redes
```

Nadie edita a mano un PNG o un PDF exportado: se cambia la fuente y se vuelve a generar.

---

Uso interno de Oryzz y de sus proveedores. Fuentes bajo SIL Open Font License 1.1. Cifras y clientes de los ejemplos: ficticios y marcados como tales.
