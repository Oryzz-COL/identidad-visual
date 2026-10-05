# 10 · Papelería e impresión Oryzz

Piezas impresas de Oryzz y Oryzz Tap, listas para enviar a imprenta. Se generan con `00_Fuente_Maestra/build/build_papeleria.py` a partir de los logos maestros y los tokens: no se redibuja nada a mano.

## Formatos de cada pieza

Cada pieza existe en cuatro formatos, en subcarpetas con el mismo nombre en todas las secciones:

| Subcarpeta | Qué contiene | Para quién |
|---|---|---|
| `PDF_imprenta_con_marcas/` | PDF con **sangrado de 3 mm**, marcas de corte e información de la pieza en el margen. Las piezas troqueladas incluyen un `_troquel.pdf` con la línea de corte | La imprenta |
| `PDF_sin_marcas/` | PDF con sangrado, sin marcas. TrimBox y BleedBox definidos | Imprentas online que piden el archivo «limpio» |
| `SVG_editable/` | Una cara por archivo, en milímetros, editable en Illustrator, Inkscape o Figma | Para cambiar datos o adaptar |
| `Vista_previa_PNG/` | Vista previa para pantalla | Para revisar o enseñar |

## Contenido

| Carpeta | Pieza | Medida |
|---|---|---|
| `01_Tarjetas_de_Visita` | Juan Salazar y David Morales, versión oscura y clara, anverso y reverso con QR a oryzz.com | 85 × 55 mm |
| `02_Membrete_Sobre_Carpeta` | Membrete A4 · Sobre DL (frente y dorso) · Carpeta A4 con bolsillo (exterior, interior y troquel) | A4 · 220 × 110 mm · pliego 445 × 410 mm |
| `03_Pegatinas_y_Etiquetas` | Sticker del isotipo · Sticker Tap «Acerca tu teléfono» · Etiqueta de caja de envío Tap (todos con troquel) | Ø 50 mm · 70 × 35 mm · 100 × 60 mm |
| `04_Tarjeta_Producto_Tap` | Tarjeta que va en la caja de Oryzz Tap (frente y dorso, con instrucciones de activación) | A6 |
| `05_Rollup_y_Cartel` | Roll-up de Oryzz (los 100 mm inferiores quedan ocultos en el cassette) · Cartel A3 de Oryzz Tap | 850 × 2000 mm · A3 |
| `06_Merchandising` | Plano de aplicación en camiseta, taza y tote, con indicaciones de técnica | — |

## Antes de imprimir

1. **Datos personales:** correos y teléfonos de las tarjetas son marcadores (`{{juan@oryzz.com}}`, `{{+34 600 000 000}}`). Cámbialos en el SVG o en `PERSONAS` dentro de `build_papeleria.py` y vuelve a generar: `python build_papeleria.py tarjetas`.
2. **QR de Tap:** apunta a `https://oryzz.com/tap`. Sustitúyelo por la URL de activación definitiva en `URL_QR_TAP` antes de imprimir tarjetas de producto y etiquetas.
3. **Color:** los PDF están en RGB. Pide a la imprenta la conversión a su perfil y una **prueba de color física**; los valores CMYK y Pantone de `03_Color/paleta.csv` son aproximados. Negro de fondo: negro enriquecido, nunca 100 K solo.
4. **Texto:** nada por debajo de 9 pt (ya respetado en todas las piezas).
5. **Gradiente:** solo en impresión digital o cuatricromía. En serigrafía, bordado, vinilo o tampografía usa el logo `solido` o `mono` de `02_Logos`.

## Merchandising: técnica y logo

| Soporte | Técnica | Versión del logo |
|---|---|---|
| Camiseta oscura | Serigrafía 2 tintas | `solido-sobre-oscuro`, ancho de pecho 80–100 mm |
| Bordado (gorra, polo) | Bordado 1 hilo | `mono-blanco` o `mono-grafito`. Isotipo ≥ 15 mm; horizontal ≥ 40 mm |
| Taza blanca | Sublimación a color | `color-sobre-claro`, 55–65 mm centrado |
| Taza / tote 1 tinta | Tampografía o serigrafía | `mono-grafito` |

## Regenerar

```bash
cd Identidad_Visual/00_Fuente_Maestra/build
python build_papeleria.py                # todo
python build_papeleria.py tarjetas       # grupos: tarjetas papeleria pegatinas tap gran_formato merch
```
