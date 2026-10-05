# 09 · Redes sociales — Oryzz y Oryzz Tap

Sistema de plantillas para producir piezas de redes **cambiando solo el texto**. Las piezas de esta carpeta son ejemplos ya exportados; todas salen del mismo generador y se pueden rehacer o duplicar en segundos.

> Reglas de marca: `00_Fuente_Maestra/BRAND_SPEC.md`. Reglas de contenido (pilares, límites de palabras, zonas seguras, calendario, ideas): `Guia_de_contenido_redes.md`.

---

## 1. Qué hay en cada carpeta

| Carpeta | Contenido |
|---|---|
| `Instagram_Oryzz/oscuro/` y `/claro/` | 8 tipos de post 1080×1350 para @oryzzai, en las dos expresiones: titular, cifra, mito vs realidad, antes/después, cita (ejemplo), checklist, servicio GEO, CTA valoración 30 min |
| `Instagram_Oryzz/carrusel_geo_clinicas/` | Carrusel de 8 slides «Por qué tu clínica no aparece cuando alguien pregunta a ChatGPT». `_vista_continua_carrusel_geo.png` muestra la ruta que atraviesa las slides |
| `Instagram_Oryzz/lote_csv/` | 4 posts generados desde una hoja de cálculo (`_generador/contenido/lote_ideas.csv`) |
| `Instagram_Tap/` | 6 posts de Oryzz Tap (@oryzztap) en expresión clara: producto, cómo funciona, Reseñas Google vs Oryzz Pro, placa vs stand, activación, promoción con precio de ejemplo |
| `Instagram_Tap/stories/` | 3 stories de Tap: producto, cómo funciona, promoción |
| `Stories/Oryzz/` | 6 stories 1080×1920: pregunta, encuesta, dato, anuncio, testimonio, CTA |
| `Stories/Destacados/` | 8 portadas de destacados (Servicios, Casos, GEO, Tap, FAQ, Equipo, Reseñas, Contacto) + `00_vista_previa_perfil.png` |
| `Stories/_guia_zonas_seguras.png` | Story con las zonas de interfaz de Instagram marcadas (solo referencia) |
| `LinkedIn/` | Banner de empresa 1128×191 y banners personales 1584×396 (Juan Salazar, David Morales), exportados @2x · 3 posts (1:1 titular, 4:5 dato, 4:5 proceso) · portada de documento PDF · `_guias/` con la zona que tapa la foto/logo |
| `Otros/` | Miniatura YouTube 1280×720 · portada Reels/TikTok 1080×1920 · OG 1200×630 (Oryzz y Tap) · portada Google Business Profile 1200×675 · foto de perfil WhatsApp Business 640×640 (Oryzz y Tap) · `_guias/` con zonas seguras de Reels/TikTok y recorte circular |
| `_plantillas/` | Plantillas HTML (Jinja2) + `social.css`. **Aquí se toca el diseño**, no el copy |
| `_generador/` | `generar.py`, `graficos.py` (órbitas, rutas, nodos, iconos, QR), `contenido/*.json|csv` (**aquí se toca el copy**), `_html/` (HTML intermedio, se puede abrir en el navegador) y `_hojas/` (hojas de contacto para revisar) |

## 2. Cómo hacer una pieza nueva (5 minutos)

1. Instala una vez: Python 3.9+, Google Chrome y `pip install jinja2 qrcode pillow`.
2. Abre el archivo de contenido que corresponda en `_generador/contenido/` (por ejemplo `instagram_oryzz.json`).
3. Duplica un bloque de pieza, cambia su `id` y el texto. No hace falta tocar HTML.
4. Genera:

```bash
cd 09_Redes_Sociales/_generador
python generar.py instagram_oryzz --solo 09_mi_post     # solo esa pieza
python generar.py instagram_oryzz                        # todo el archivo
python generar.py                                        # todo el sistema
python generar.py --hojas                                # + hojas de contacto en _hojas/
python generar.py --lista                                # plantillas, formatos y piezas
python generar.py --html                                 # solo HTML, para ajustar en el navegador
```

5. Revisa la consola: `aviso` = el texto supera el máximo de palabras recomendado; `DESBORDA` = el texto no cabe ni reduciendo el cuerpo (la pieza sale con una franja roja: recorta el copy).

### Marcado del texto

| Escribes | Sale |
|---|---|
| `**clientes**` | resaltado en Azul IA (uno por titular) |
| `==+32 %==` | dato en lima (un dato por pieza) |
| `~~$ 118.000~~` | tachado |
| `__texto__` | negrita |
| `\n` en el JSON | salto de línea forzado |

Los espacios antes de `%`, `€`, `×`, `min`, `mm`, `COP` y los rangos (`3–7 días`, `50–100 €`) se vuelven no separables automáticamente.

### Campos comunes

`plantilla`, `formato` (`post`, `story`, `cuadrado`, `li`, `documento`, `li_banner_empresa`, `li_banner_personal`, `youtube`, `og`, `gbp`, `avatar`), `tema` (`oscuro`, `claro`, `tap`) o `temas` (lista → una salida por tema), `marca` (`oryzz` | `tap`), `handle`, `web`, `carpeta`, `eyebrow`, `eyebrow_der`, `titular`, `texto`, `guia` (`true` superpone zonas seguras), `foto` (ruta relativa a `09_Redes_Sociales/`; donde no hay foto la plantilla deja un marco rotulado).

### Catálogo de plantillas

| Plantilla | Para | Campos propios |
|---|---|---|
| `post_titular` | Idea, claim | `orbita` [cx, cy, escala] |
| `post_cifra` | Dato con fuente | `cifra`, `unidad`, `comparativa` [{etiqueta, valor, pct, on}], `cierre`, `fuente`, `tam_cifra` |
| `post_mito` | Mito vs realidad | `mito`, `realidad`, `nota` |
| `post_antes_despues` | Comparativa de proceso | `antes` [..], `despues` [..], `sector`, `nota` |
| `post_cita` | Testimonio (post o story) | `cita`, `autor`, `negocio`, `etiqueta` (false solo con testimonio real y autorizado), `foto` |
| `post_checklist` | Checklist | `items` [..], `cierre` |
| `post_servicio` | Anuncio de servicio | `chat` {pregunta, intro, opciones}, `plataformas`, `nota` |
| `post_cta` | CTA valoración (post o story) | `boton`, `url`, `minutos`, `reloj_etiqueta` |
| `post_proceso` | Pasos con ruta y nodos | `pasos` [{titulo, texto}], `nota` |
| `carrusel` | Carruseles con ruta continua | `estaciones` [..] + `slides` [{tipo: portada/desarrollo/pasos/cta, …, `accion`}] |
| `story` | Pregunta, encuesta, dato, anuncio | `tipo`, `pista`, `alto_sticker`, `cifra`, `unidad`, `fuente`, `etiqueta` |
| `destacado` / `destacados_vista` | Portadas de destacados | `icono_nombre` / `destacados` [{icono, nombre}] |
| `tap_producto` | Producto Tap (post/story) | `chips`, `color_placa`, `titulo_placa`, `foto` |
| `tap_pasos` | Cómo funciona / activación | `pasos` [..], `pantalla` (resena, activar, perfil), `negocio` |
| `tap_comparativa` | Reseñas Google vs Oryzz Pro | `columnas` [{linea, titulo, texto, destinos, puntos, on}] |
| `tap_formatos` | Placa vs stand | `placa` {…}, `stand` {…}, `colores` |
| `tap_promo` | Promoción con precio | `aviso_precio`, `precio`, `moneda`, `precio_antes`, `incluye`, `boton`, `url` |
| `li_banner` | Banners LinkedIn | `tipo` (empresa, personal), `servicios`, `pie` |
| `li_documento` | Portada PDF LinkedIn | `etiqueta` [..], `autores` [{iniciales, nombre, rol, foto}] |
| `yt_miniatura`, `reel_portada`, `horizontal`, `avatar` | YouTube, Reels/TikTok, OG y GBP, WhatsApp | `foto`, `episodio`, `producto`, `servicios`, `url` |

Iconos disponibles (`graficos.ICONOS`): check, cruz, flecha, flecha-abajo, chat, calendario, estrella, nfc, qr, movil, sobre, equipo, capas, casos, pregunta, geo, tap, reloj, enlace, buscar, ubicacion, mas, perfil, pantalla. Retícula 24 px, trazo 1,75 px, monocromo.

### Desde una hoja de cálculo

`contenido/*.csv` funciona igual que el JSON: una fila por pieza, columnas con el nombre del campo. Las listas van en columnas terminadas en `[]` separadas por `|` (ver `lote_ideas.csv`). Útil para preparar un mes de posts en Google Sheets y exportarlo como CSV.

## 3. Cómo cambiar el diseño

- Colores, tipografías y componentes: `_plantillas/social.css` (solo tokens de `tokens.json`).
- Maqueta de cada tipo: `_plantillas/<plantilla>.html`. Base común (cabecera, pie, ajuste automático): `_base.html` y `_macros.html`.
- Órbitas, rutas, iconos y QR: `_generador/graficos.py`.
- Formatos nuevos: diccionario `FORMATOS` de `generar.py`.

## 4. Limitaciones conocidas

- **No hay fotos reales.** Tap usa placa, stand y móvil dibujados en vector; YouTube deja un marco rotulado para la foto del presentador. Al tener fotos, añade `"foto": "ruta.jpg"`.
- **La cita es un ejemplo** (marcada como «Testimonio de ejemplo»). No se publica como real sin un testimonio autorizado.
- **El precio de Tap** ($ 99.900 COP pack x2, antes $ 118.000) sale de la web actual y lleva la etiqueta «Precio de ejemplo · confirmar antes de publicar». Bórrala (`"aviso_precio": ""`) solo con el precio confirmado.
- **El dato 21×** cita el *Lead Response Management Study* (MIT e InsideSales.com, 2007). Verifica la fuente antes de publicarlo en anuncios.
- El QR de las placas dibujadas apunta a `https://oryzz.com/tap` (se escanea de verdad).
- Las zonas seguras son las recomendadas a septiembre de 2026; las apps cambian su interfaz a menudo. Revísalas con las guías `_guias` cada trimestre.
- Los logos se leen desde `02_Logos/` (SVG). Si cambian allí, basta con regenerar.
