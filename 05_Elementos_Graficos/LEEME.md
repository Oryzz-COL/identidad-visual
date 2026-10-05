# 05 · Elementos gráficos · «Órbita y nodo»

Lenguaje visual de Oryzz v2.0: **órbitas, rutas, nodos y datos**. Todo sale de la O del logo (órbita abierta = el sistema en marcha) y de su nodo lima (el resultado medible: el lead, la cita, el cliente).

Fuente obligatoria: `00_Fuente_Maestra/BRAND_SPEC.md` y `tokens.json`. Todo lo de esta carpeta se **regenera con scripts** (no se edita a mano): ver §8.

---

## Reglas que valen para todo

1. **Un solo acento por pieza: el nodo lima.** Lima 500 `#BFF24A` sobre oscuro, Lima 600 `#7FB02E` sobre claro. Si ya hay un nodo lima, no se añade otro color de acento.
2. **El nodo siempre va separado del trazo** (como en el isotipo v2): la línea se corta antes de llegar a él.
3. **Líneas finas**: 1–2 px en Grafito 700 (oscuro) / Grafito 200–300 (claro). Nada de brillos, sombras, glassmorphism ni manchas de luz. Como máximo un halo radial ≤ 20 % por composición (los fondos ya lo llevan, no añadas otro).
4. **Composición asimétrica**: el elemento gráfico vive en un lado; el texto, en el otro. Respeta las zonas de texto de `03_Fondos/fondos.json`.
5. **Texto mínimo**: 14 px en pantalla, 9 pt impreso, 18 pt en slides.
6. **Datos**: las cifras de los componentes y diagramas son de **ejemplo** y lo dicen (chip «Ejemplo»). Nunca se presentan como resultados reales de un cliente.
7. **El logo no se redibuja**: en las piezas se incrusta el SVG maestro de `02_Logos`.

---

## 01_Iconos · 43 iconos propios

| Recurso | Uso |
|---|---|
| `SVG/oz-icono_<nombre>.svg` | Icono suelto, 24 × 24, `stroke="currentColor"`, trazo 1,75, puntas redondas |
| `iconos-sprite.svg` | Sprite con `<symbol id="oz-<nombre>">` para web |
| `PNG_64/`, `PNG_256/` | PNG transparentes en 4 variantes: `grafito`, `blanco`, `grafito_acento-lima`, `blanco_acento-lima` |
| `iconos-lamina.png/pdf` | Lámina con todo el set, la construcción y la escala |

**Nombres:** `ads-meta` · `ads-google` · `ads-tiktok` · `geo-ia` · `seo-local` · `resenas` · `automatizacion` · `ia-sistema` · `estrategia` · `embudo` · `mensaje` · `email` · `calendario` · `llamada` · `lead` · `cliente` · `etiqueta` · `enviar` · `crecimiento` · `grafico` · `dashboard` · `objetivo` · `reloj` · `euro` · `ubicacion` · `mapa` · `nfc` · `qr` · `tienda` · `pago` · `menu-carta` · `check` · `check-orbita` · `flecha` · `flecha-diagonal` · `mas` · `cerrar` · `documento` · `ajustes` · `enlace` · `usuario` · `equipo` · `busqueda`.

**Acento:** el elemento con `class="oz-acento"` (casi siempre un nodo) toma el color de la variable CSS `--oz-acento`; si no se define, hereda el color del icono (monocromo).

```html
<svg class="oz-icon" width="24" height="24" style="color:#D5D9E0;--oz-acento:#BFF24A">
  <use href="05_Elementos_Graficos/01_Iconos/iconos-sprite.svg#oz-calendario"/>
</svg>
```

- Color del trazo: **Grafito 200 sobre oscuro**, **Grafito 950 sobre claro**.
- Tamaños: 16, 20, 24, 32, 48 (múltiplos de la retícula). No escales el trazo: a 48 px el trazo mide 3,5 px, es correcto.
- Los iconos de canal (`ads-meta`, `ads-google`, `ads-tiktok`) son **genéricos** (feed, buscador, vídeo vertical): no son los logos de las plataformas. Si hace falta el logo oficial, solo en su versión monocroma.
- Prohibido: rellenar, mezclar colores en un icono, poner iconos de stock al lado, emojis.

## 02_Patrones · 4 texturas × 2 temas

| Patrón | Tile enlosable (`SVG_tiles/`) | Composición (`SVG/`, `PNG/`, 1920×1080 y 1080×1350) |
|---|---|---|
| a) **Órbitas** concéntricas abiertas, espaciado creciente, un nodo | — (no tiene sentido repetir una órbita) | `patron-orbitas_<tema>_<tamaño>` |
| b) **Retícula** técnica 64 px, cruces cada 256 px, desvanecida | `patron-reticula_tile_<tema>.svg` (256 px) | `patron-reticula_<tema>_<tamaño>` |
| c) **Rutas y nodos** ortogonales con esquinas redondeadas | `patron-rutas_tile_<tema>.svg` (512 px) | `patron-rutas_…` (rutas que convergen en un nodo) |
| d) **Campo de nodos** / puntos de datos | `patron-nodos_tile_<tema>.svg` (512 px) | `patron-nodos_…` (densidad que cae desde un foco) |

- Los tiles **no llevan nodo lima** (al repetirse lo multiplicarían): añade uno solo por pieza.
- CSS: `background: #0B0D12 url(patron-rutas_tile_oscuro.svg) 0 0 / 512px;`
- Opacidad: retícula 3,5 % sobre oscuro y 5 % sobre claro. Siempre textura, nunca protagonista. No combines más de dos patrones en una pieza.

## 03_Fondos · 12 fondos listos

| # | Receta | Tema | Formato |
|---|---|---|---|
| 01 | órbita a la derecha | oscuro | 16:9 |
| 02 | órbita desde la esquina | claro | 16:9 |
| 03 | rutas que convergen | oscuro | 16:9 |
| 04 | retícula + órbita superior | claro | 16:9 |
| 05 | órbita abajo | oscuro | 4:5 |
| 06 | órbita arriba | claro | 4:5 |
| 07 | campo de nodos + órbita | oscuro | 4:5 |
| 08 | órbita abajo | oscuro | 9:16 |
| 09 | órbita arriba | claro | 9:16 |
| 10 | rutas | oscuro | 9:16 |
| 11 | portada documento | oscuro | A4 |
| 12 | portada documento | claro | A4 |

- `PNG/` a tamaño final (A4 a 2480 × 3508, 300 ppp), `SVG/` editable y `PDF/` A4 a sangre.
- **`fondos.json`**: zona de texto recomendada de cada fondo (px y %). Coloca titulares y logo dentro; el nodo lima queda siempre fuera.
- `fondos-lamina.png/pdf`: muestra de uso con copy real (la línea discontinua no forma parte del fondo).
- No añadas otro halo, otra órbita ni otro nodo encima. Sobre los fondos claros el logo va en `color-sobre-claro`.

## 04_Diagramas · 6 diagramas del método (oscuro y claro)

| # | Diagrama | Qué explica |
|---|---|---|
| 01 | `canales-sistema-cliente` | Meta, Google, TikTok y GEO convergen en el sistema Oryzz → cliente |
| 02 | `embudo-orbita` | Captar → responder → clasificar → seguir → medir, en ciclo alrededor del cliente |
| 03 | `valoracion-30min` | Valoración de 30 min en 3 pasos (media esfera de reloj) |
| 04 | `prueba-inicial` | Prueba inicial: 50–100 € · 3–7 días (montamos, medimos, decidimos) |
| 05 | `oryzz-tap-flujo` | Toque → reseña en Google, WhatsApp, menú o pago |
| 06 | `geo-ia` | Pregunta → asistente de IA → fuentes → respuesta que cita al negocio |

- `SVG/`: texto vivo, **editable** (necesita instaladas Space Grotesk, Manrope y JetBrains Mono de `04_Tipografia`).
- `SVG_contornos/`: texto convertido a trazados. **Usa este en web, email, `<img>` y documentos**: se ve igual en cualquier equipo.
- `PNG/`: 1920 × 1080 y `@2x` 3840 × 2160. En slides, a sangre en una diapositiva 16:9.
- Estilo: líneas finas, nodos huecos, etiquetas en JetBrains Mono y **un solo acento lima** (el resultado). Sin gradiente ni azul de acento dentro del diagrama.

## 05_Componentes_Dato

| Carpeta | Contenido |
|---|---|
| `kpi/` | Tarjetas KPI 400 × 232: `coste-por-lead`, `citas`, `ctr`, `resenas` (oscuro y claro) |
| `graficos/` | Mini gráfico de `linea` y de `barras` 640 × 340 (oscuro y claro) |
| `chips/` | `en-marcha`, `ejemplo`, `meta-ads`, `google-ads`, `tiktok-ads`, `geo`, `nuevo-lead`, `pausado` |
| `eyebrows/` | `linea` (— MÉTODO ORYZZ), `nodo` (● EN MARCHA), `numero` (01 / CAPTACIÓN) |
| `botones/` | `primario-oscuro` (gradiente IA + texto Grafito 950), `primario-claro` (Azul 600 + blanco), `secundario-oscuro/claro` (contorno), tallas M (48) y L (60) |

- Cada uno en `SVG/` (texto vivo), `SVG_contornos/` y `PNG/@2x`. Lámina: `componentes-lamina.png/pdf`.
- Tarjeta dato: superficie Grafito 850, borde 1 px Grafito 700, radio 20, eyebrow mono, cifra Space Grotesk 500, delta con nodo lima.
- **Sobre claro el delta va en Grafito 950 con nodo Lima 600** (el texto en lima 600 sobre blanco no llega a contraste).
- Las cifras son de ejemplo. Para cambiarlas: edita `KPIS`, `LEADS` y `CITAS` en `oryzz_componentes.py` y regenera. El chip «Ejemplo» solo se quita con datos reales y fuente.
- En web, reproduce los componentes en HTML/CSS con `brand.css`; los SVG son referencia exacta y material para slides/documentos.

## 06_Fotografia

- `direccion-fotografica.md`: qué sí / qué no, temas, luz, encuadres, graduación, velo y prompts.
- `PNG/` y `SVG/`: 3 tratamientos de ejemplo (clínica 16:9, post 4:5, producto Tap en claro).
- `plantilla-foto-velo_16x9.html`: plantilla con la variable `--foto` para cambiar la imagen.
- El rectángulo gris con grano es un **marcador de foto**: no se publica tal cual.

---

## Cómo regenerar

Desde `00_Fuente_Maestra/build/`:

```
python oryzz_iconos.py        # 01_Iconos (SVG, sprite, PNG, lámina)
python oryzz_patrones.py      # 02_Patrones
python oryzz_fondos.py        # 03_Fondos (+ fondos.json, PDF A4, lámina)
python oryzz_diagramas.py     # 04_Diagramas (o: python oryzz_diagramas.py 01 03)
python oryzz_componentes.py   # 05_Componentes_Dato
python oryzz_fotografia.py    # 06_Fotografia (tratamientos y plantilla)
```

Utilidades comunes en `oryzz_svg.py`: paleta desde `tokens.json`, texto a trazados con las TTF de marca (kerning real), `arc()`, `orbita()`, `ruta()`, `reticula()`, `halo()`, `embed_logo()` e `isotipo_group()` (geometría oficial de `oryzz_logo.py`). Render con Chrome headless (`render.py`).
