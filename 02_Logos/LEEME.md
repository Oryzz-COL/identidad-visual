# Oryzz · Logos v2.0 — LÉEME

Todo lo que necesitas para usar el logo de Oryzz y de Oryzz Tap. **Nunca redibujes el logo ni lo escribas con texto**: usa siempre estos archivos.
Para ver todas las versiones de un vistazo, abre `Oryzz_Logos_Hoja_de_Contacto.pdf`.

---

## 1. ¿Qué archivo uso?

| Caso | Archivo recomendado | Notas |
|---|---|---|
| **Web, cabecera sobre oscuro** (principal) | `01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg` | SVG siempre que se pueda. Si no, PNG `_1600`. |
| Web sobre fondo claro | `01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-claro.svg` | |
| Web, logo a menos de 120 px de ancho | `…horizontal_solido-sobre-oscuro.svg` / `_solido-sobre-claro.svg` | El gradiente se ensucia por debajo de 120 px. |
| Favicon e icono de app | `06_Favicon/` completo + `snippet-head.html` | Sube los archivos a la raíz del dominio y pega el snippet en `<head>`. |
| Foto de perfil **Oryzz** (Instagram, LinkedIn, WhatsApp, TikTok) | `05_Avatar_Perfil/PNG_redes/oryzz-avatar-redes_color-sobre-oscuro_1080.png` | Fondo a sangre y recorte circular seguro. `_400` para subidas ligeras. |
| Foto de perfil **Oryzz Tap** | `05_Avatar_Perfil/PNG_redes/oryzz-tap-avatar-redes_color-sobre-claro_1080.png` | Tap se expresa en claro. Alternativa: `_color-sobre-blanco`. |
| Marca de agua en posts, stories y vídeo | `04_Isotipo/PNG/oryzz-isotipo_mono-blanco_512.png` o `01_Horizontal/PNG/…_mono-blanco_1600.png` | Sobre foto, siempre con velo Grafito 950 al 55–70 %. |
| Firma de email | `01_Horizontal/PNG/oryzz-logo-horizontal_solido-sobre-claro_800.png` | Muéstralo a 160–200 px de ancho. Los clientes de correo no leen SVG. |
| Word, Google Docs, PowerPoint | PNG `_1600` en `color-sobre-claro` (fondo blanco) o `color-sobre-oscuro` (diapositiva oscura) | |
| Imprenta (papelería, flyers, lonas) | `…/PDF/…_color-sobre-claro.pdf` o `_color-sobre-oscuro.pdf` | PDF vectorial en RGB: la imprenta lo convierte con los CMYK de `03_Color` y entrega prueba de color (ver §2). |
| Impresión a una tinta / barata | `…/PDF/…_mono-negro.pdf` o `_mono-grafito.pdf` | |
| **Bordado** (polos, gorras) | `…/SVG/…_solido-sobre-oscuro.svg` / `_solido-sobre-claro.svg` o `mono-blanco` / `mono-grafito` | Sin gradiente. El corte del nodo (2,5 u) está pensado para que no se empaste. |
| **Vinilo de corte** (escaparate, coche) | `…/SVG/…_mono-blanco.svg` o `_mono-grafito.svg` | El vinilo de corte no admite gradientes. `solido` si se monta en varias capas. |
| **Grabado láser** (placas Tap, metacrilato, madera) | `…/SVG/…_mono-negro.svg` (o PDF) | Lo negro es lo que se graba. |
| Fondo de foto | `mono-blanco` sobre velo Grafito 950 al 55–70 % | Nunca el gradiente sobre foto sin velo. |
| Pieza sobre azul de marca | `…_sobre-azul` | |
| Campaña puntual sobre lima | `…_sobre-lima` | Solo piezas puntuales: el lima es acento (≤ 5 %). |
| Formatos cuadrados o verticales | `02_Vertical/` | |
| El isotipo ya aparece en la pieza | `03_Wordmark/` | |
| Tamaños ≤ 24 px | `04_Isotipo/SVG_tamano_pequeno/` o `PNG_tamano_pequeno/` | Trazo reforzado al 14 % y corte del nodo ampliado para que se vea a 16 px. |
| Producto y web de Oryzz Tap | `07_Submarca_Tap/…_color-sobre-claro` | Expresión principal en claro. |
| Intro de web o de vídeo | `08_Animado/oryzz-logo-intro.svg` (web) · `oryzz-logo-intro_800x300.gif` (donde no hay SVG) | Una sola vez; termina en el logo en reposo. |
| Estado de carga | `08_Animado/oryzz-loader.svg` | 32–96 px. |
| Guía de marca | `09_Construccion_y_Uso/` | Láminas en SVG (texto vectorizado) y PNG a 2×, en tema oscuro y claro. |

## 2. Estructura de carpetas

```
02_Logos/
├── 01_Horizontal/      SVG · PNG (800 / 1600 / 3200 px de ancho) · PDF      ← versión principal
├── 02_Vertical/        SVG · PNG (500 / 1000 / 2000) · PDF
├── 03_Wordmark/        SVG · PNG (800 / 1600 / 3200) · PDF
├── 04_Isotipo/         SVG · PNG (256 / 512 / 1024 / 2048) · PDF
│                       SVG_tamano_pequeno · PNG_tamano_pequeno (16 / 24 / 32 / 48 / 64)
├── 05_Avatar_Perfil/   SVG · PNG (256–2048, cuadrado y círculo)
│                       SVG_redes · PNG_redes (1080 y 400 px, a sangre) + vista previa del recorte circular
├── 06_Favicon/         favicon.svg · favicon.ico (16/32/48) · favicon-16/32.png · apple-touch-icon-180.png
│                       android-chrome-192/512.png · maskable-512.png · site.webmanifest · snippet-head.html · fuentes_svg/
├── 07_Submarca_Tap/    SVG · PNG (800 / 1600 / 3200) · PDF                  ← «oryzz tap»
├── 08_Animado/         intro, bucle y loader (SVG con CSS, claro y oscuro) · GIF · póster · oryzz-logo-animado.html
├── 09_Construccion_y_Uso/  construcción, área de respeto, tamaños mínimos, usos incorrectos (SVG + PNG, oscuro y claro)
└── Oryzz_Logos_Hoja_de_Contacto.pdf
```

**Nombres:** `oryzz-<pieza>_<colorway>[_<ancho en px>].<ext>` — p. ej. `oryzz-logo-horizontal_color-sobre-oscuro_1600.png`.

**Los diez colorways:** `color-sobre-oscuro` (principal) · `color-sobre-claro` · `solido-sobre-oscuro` · `solido-sobre-claro` · `sobre-azul` · `sobre-lima` · `mono-blanco` · `mono-grafito` · `mono-negro` · `mono-azul`. El nombre indica el fondo para el que está hecho: `mono-blanco` va sobre oscuro.

**Formatos:**
- **SVG**: maestro vectorial. Para web, Figma e Illustrator.
- **PNG**: fondo transparente, con el mismo encuadre que el SVG maestro. Los lockups llevan un margen uniforme de 32 u en los cuatro lados (nada toca el borde); isotipo y avatares mantienen su caja cuadrada.
- **PDF**: vectorial (sin imágenes incrustadas, sin fuentes: todo son trazados), página del tamaño del logo. **Van en RGB a propósito.** Instrucción para la imprenta: convertir a CMYK usando los valores CMYK de `03_Color` (no una conversión automática de perfil) y entregar **prueba de color** antes de tirar la producción.

## 3. Reglas rápidas

1. **Área de respeto**: como mínimo **x** (la altura de la «z» del wordmark) en los cuatro lados. Isotipo solo: 25 % de su ancho.
2. **Tamaño mínimo**: horizontal 88 px / 22 mm; isotipo 16 px / 5 mm. Por debajo de 120 px, `solido`; por debajo de 24 px, `isotipo-small`.
3. **No** estirar, rotar (salvo la animación oficial), recolorear fuera de los diez colorways, añadir sombras, contornos o brillos, ni ponerlo sobre fondos que lo apaguen.
4. **No** mover el nodo, reordenar «ory» y «zz» ni usar las estrellas del logo antiguo de Tap.
5. El logo va siempre en minúscula. En texto corrido: **Oryzz** y **Oryzz Tap** (nunca «ORYZZ» ni «OryzzTAP»).
6. El movimiento del logo solo en intros, loaders y cierres; nunca en bucle dentro de una interfaz.
7. Los `id` de los gradientes son únicos por familia y colorway (`oryzz-h-color-sobre-oscuro-r`…): puedes incrustar varios SVG en línea en la misma página. Solo evita repetir en línea el mismo archivo dos veces (usa `<img>`).

## 4. Regenerar

Todo sale de los scripts de `00_Fuente_Maestra/build/` (Python 3 + Chrome):

| Script | Genera |
|---|---|
| `oryzz_logo.py` | SVG maestros (geometría del logo) |
| `export_logos.py` | PNG, PDF, pack favicon y avatares de redes |
| `logo_animado.py` | `08_Animado` (SVG con CSS + GIF fotograma a fotograma) |
| `diagramas_uso.py` | `09_Construccion_y_Uso` |
| `hoja_contacto.py` | `Oryzz_Logos_Hoja_de_Contacto.pdf` |
| `render_fast.py` · `svg_text.py` | Utilidades: render rápido por CDP y texto vectorizado con las fuentes de marca |

Si cambian los SVG maestros, ejecuta en orden: `oryzz_logo.py 02_Logos` → `export_logos.py` → `logo_animado.py` → `diagramas_uso.py` → `hoja_contacto.py`.
