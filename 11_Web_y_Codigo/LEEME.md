# Oryzz · Web y código (sistema v2.0)

Esta carpeta es la implementación del sistema de marca v2.0 para las dos webs:
**oryzz.com** (HTML estático + `styles.css`, tema oscuro) y **oryzz.com/tap** (Next.js 16 + Tailwind v4, tema claro).
La fuente única de verdad es `00_Fuente_Maestra/tokens.json`. Todo lo de `tokens/` y `fonts/fonts.css` se **genera**:

```bash
cd Identidad_Visual/00_Fuente_Maestra/build
python web_tokens.py        # tokens.css, tokens.scss, tailwind.preset.js, tailwind-v4.css, tokens.json, figma-tokens.json
python componentes_web.py   # componentes/componentes.html + componentes_preview.png
```

## Contenido

| Carpeta / archivo | Qué es |
|---|---|
| `tokens/tokens.css` | Variables CSS: primitivos (`--grafito-950`, `--azul-600`…), escala tipográfica, espacios, radios, motion y **semántica por tema** (`--color-fondo`, `--color-texto-2`, `--color-cta-fondo`…) con `data-tema="oscuro"` (por defecto) y `data-tema="claro"`. Incluye los `@font-face` apuntando a `/fonts/`. |
| `tokens/tokens.scss` | Las mismas variables para Sass (`@use "tokens" as ox;`), mapas y mixins `ox.tema(claro)` y `ox.tipo("h1")`. Validado con Dart Sass 1.9x sin avisos. |
| `tokens/tailwind.preset.js` | Preset para **Tailwind v3** (`presets: [require('./tailwind.preset.js')]`). |
| `tokens/tailwind-v4.css` | Tema para **Tailwind v4** con `@theme` (lo que usa hoy /tap). Validado con Tailwind 4.3. |
| `tokens/tokens.json` | Formato **W3C Design Tokens (DTCG)**, con alias `{color.grafito.950}` en la semántica. |
| `tokens/figma-tokens.json` | Formato **Tokens Studio for Figma** con sets `global`, `oscuro`, `claro` y dos temas. |
| `componentes/oryzz-ui.css` | Botones, enlaces, eyebrow, tarjeta dato, badge, input, navbar y footer. Solo usa variables semánticas: el mismo HTML sirve en oscuro y en claro. |
| `componentes/componentes.html` | Librería de referencia navegable (oscuro + claro lado a lado, CSS para copiar). Ábrela en el navegador desde esta carpeta. |
| `fonts/` | Space Grotesk, Manrope y JetBrains Mono en **WOFF2** (estáticas + variables `*-VF.woff2`), `fonts.css` y licencias OFL. |

## Reglas que el código ya resuelve

- **Botón principal:** oscuro = gradiente IA `#5C8BFF → #36CFE0` + texto **Grafito 950** (6,10–10,33:1). Claro = **Azul 600** `#2C5BD0` + blanco (5,98:1). El botón actual (blanco sobre `#3B72FF → #36CFE0`) baja a **1,88:1**.
- **Grises de texto:** oscuro → `--color-texto-2` Grafito 200, `--color-texto-3` Titanio 400 (6,09:1). Claro → Grafito 600 y Grafito 500 (6,20:1). `#5A6172` **nunca** como texto sobre oscuro (3,14:1).
- **Bordes de controles** (inputs, botón secundario) ≥ 3:1: `--color-borde-fuerte` = Grafito 500 en oscuro / Titanio 400 en claro.
- **Dato en claro:** `--color-dato` (Lima 600) es solo un punto gráfico (2,58:1); para texto usa `--color-dato-texto` (Lima 900 en claro, Lima 500 en oscuro).
- **Sin** `box-shadow` de color en botones, sin halos animados, sin `filter:brightness` en hover.
- Texto mínimo **14 px** (el eyebrow mono de 12 px es la única excepción).
- `prefers-reduced-motion` desactiva animaciones.

## Aplicarlo en oryzz.com (sitio estático)

Código: `TAP/OryzzTAP/oryzz/` (`index.html`, `contacto.html`, `legal.html`, `styles.css`, `fonts.css`).

1. **Fuentes.** Copia `fonts/*.woff2` a `oryzz/fonts/` y sustituye `fonts.css` por `fonts/fonts.css` de aquí (añade JetBrains Mono, que hoy falta). Borra los 16 `*-latin*.woff2` actuales: son 2 archivos repetidos 4 veces cada familia. Preload: `SpaceGrotesk-Bold.woff2` y `Manrope-Regular.woff2`.
2. **Tokens.** Copia `tokens/tokens.css` a `oryzz/tokens.css`, enlázalo **antes** de `styles.css` y pon `<html lang="es" data-tema="oscuro">`.
3. **Mapea las variables de `styles.css`** (y borra su bloque `:root`):

   | Actual | Nuevo |
   |---|---|
   | `--bg` `--bg2` `--surface` `--surface2` | `--color-fondo` · `--grafito-900` · `--color-superficie` · `--color-superficie-2` |
   | `--bd` `--bd2` | `--color-borde` · `--color-borde-fuerte` |
   | `--t1` `--t2` `--t3` `--t4` | `--color-texto` · `--color-texto-2` · `--color-texto-2` · `--color-texto-3` |
   | `--t5` (#5A6172, usado como texto) | `--color-texto-3` (Titanio 400) |
   | `--grad` / `--grad-strong` (105°) | `--grad-ia-oscuro` (135°) |
   | `--blue` `--blue-l` `--cyan` `--lime` | `--azul-500` · `--azul-400` · `--cyan-500` · `--lima-500` |
   | `--ease` | `--motion-ease-marca` |

4. **Botón.** `.btn-grad{background:var(--color-cta-fondo);color:var(--color-cta-texto);box-shadow:none}` y hover `background:var(--color-cta-fondo-hover)` (o usa `.ox-btn--primario`). Aplica también a `.ck-accept` de `cookies.js`.
5. **Logo.** Sustituye el SVG dibujado a mano + `<span class="wordmark">` por `<img src="/brand/oryzz-logo-horizontal_color-sobre-oscuro.svg" alt="Oryzz" height="26">` (copia de `02_Logos/01_Horizontal/SVG/`). En el footer, lo mismo. `favicon.svg` → `02_Logos/06_Favicon/favicon.svg` y añade `apple-touch-icon` PNG 180 px.
6. **Eyebrow** en JetBrains Mono (`.ox-eyebrow`), no en Space Grotesk.
7. **Iconos.** Sustituye los `<symbol>` de colores (`kgMeta`, `kgGem`, `kgIg`, `ic-google` multicolor, `ic-wa`, `ic-pin` rojo/azul) por la iconografía monocroma de `05_Elementos_Graficos/01_Iconos` (trazo 1,75 px, `currentColor`). Elimina `background:rgba(255,90,90,.1);color:#FF7B7B` de las tarjetas «El problema».
8. **Escenografía.** Elimina `.aura` (dos manchas de 560–680 px con `blur` y animación en bucle) o deja **una** sola sin animar al ≤ 20 % de opacidad.
9. **Nombre.** «OryzzTAP» → «Oryzz Tap» (3 apariciones en `index.html`, 2 en `contacto.html`). En texto corrido, «Oryzz» con mayúscula (title, `og:site_name`, JSON-LD, `llms.txt`).
10. **Meta.** Nueva `og-image.png` 1200×630 con el logo v2 (`09_Redes_Sociales`), `"logo"` del JSON-LD apuntando a un PNG cuadrado del isotipo, `theme-color` se mantiene `#0B0D12`.

## Aplicarlo en oryzz.com/tap (Next.js + Tailwind v4)

> **Atención:** el código fuente local `oryzz/oryzz-tap-store/` **no es** el que está publicado (usa DM Sans + Poppins y el azul Google `#1A73E8`; la web publicada usa Syne + Outfit y `#0075FF`). Localiza el repositorio real antes de migrar y deja una sola fuente.

1. En `app/globals.css`:
   ```css
   @import "tailwindcss";
   @import "./tailwind-v4.css";   /* copia de tokens/tailwind-v4.css */
   @import "./tokens.css";        /* copia de tokens/tokens.css (semántica + @font-face) */
   ```
   y elimina `--color-accent #0075ff`, `--color-brand-lime #c5f500`, `--color-canvas #eef2f6`, los ~90 HEX sueltos y `--font-heading/--font-sans` de Syne/Outfit.
2. En `app/layout.tsx` quita `next/font/google` (Syne, Outfit) y pon `<html lang="es" data-tema="claro">`. Copia `fonts/*.woff2` a `public/fonts/` (con `basePath: '/tap'` la ruta pública será `/tap/fonts/`: ajusta la `url()` de `tokens.css` o sírvelas desde la raíz de oryzz.com, que ya las tendrá).
3. Clases: `bg-canvas` → `bg-grafito-50`; `text-ink` → `text-grafito-950`; `text-accent`/`bg-accent` → `text-azul-600`/`bg-azul-600`; `font-heading` → `font-display`; botones → `ox-btn ox-btn--primario` o `bg-azul-600 text-white rounded-md`.
4. Logo: `/tap/brand/oryzz-logo-light.svg` (órbita dibujada con 5 estrellas) → `02_Logos/07_Submarca_Tap/SVG/oryzz-tap-horizontal_color-sobre-claro.svg`. Favicon propio de Tap no hace falta: usa el de Oryzz.
5. Barra de anuncios: sin emojis (`💙`) y un solo mensaje fijo, sin marquesina (`components/announcement-bar.tsx`, `lib/config.ts`).
6. Banner de cookies: al compartir `cookies.js` con la home, en /tap sale oscuro y con el botón en gradiente; pásalo a variables semánticas para que herede `data-tema="claro"`.
7. Añade `<meta name="theme-color" content="#FFFFFF">` y `apple-touch-icon`.

## Tailwind v3 (proyectos nuevos)

```js
// tailwind.config.js
module.exports = { presets: [require('./tokens/tailwind.preset.js')], content: ['./src/**/*.{html,tsx}'] };
```
Clases disponibles: `bg-grafito-950`, `text-azul-600`, `font-display`, `font-mono`, `text-h1 … text-eyebrow`, `rounded-xs|sm|md|lg|xl|full|app`, `bg-grad-ia-oscuro`, `ease-marca`, y semánticas `bg-fondo`, `text-texto-2`, `border-borde`, `text-enlace` (requieren `tokens.css`).
Radios renombrados a la convención de Tailwind (`s/m/l` → `sm/md/lg`) porque `rounded-l` ya significa «esquinas izquierdas».

## Figma

Tokens Studio → *Load from file* → `tokens/figma-tokens.json`. Activa el tema «Oryzz · Oscuro» o «Oryzz · Claro (Tap)». Los gradientes se importan como color con valor CSS.
