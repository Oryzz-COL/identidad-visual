# ORYZZ · Especificación maestra de marca v2.0 (2026-09-29)

> Documento fuente para cualquier persona o agente que produzca piezas de Oryzz.
> Si algo no está aquí, se decide a favor de: **menos elementos, más aire, un solo acento.**

---

## 0. Contexto

- **Oryzz** (oryzz.com) es una agencia de captación de clientes con IA para PYMES: Meta Ads, Google Ads, TikTok Ads, automatizaciones con IA, SEO local y reseñas, y **GEO** (posicionamiento en ChatGPT, Gemini y Perplexity). Es 100 % remota. Socios: **Juan Salazar** (Estrategia & Ads) y **David Morales** (Automatización & IA). Opera en España (EUR).
- **Oryzz Tap** (oryzz.com/tap) es la línea de producto físico: placas y stands NFC + QR (Reseñas Google, Oryzz Pro). Se vende en Colombia (COP) con checkout en Shopify (shop.oryzz.com).
- Contacto real conocido: `pedidos@oryzz.com` (Tap) · `cal.com/oryzz/30min` (agenda) · Instagram `@oryzzai` y `@oryzztap` · TikTok `@oryzz.tap` · LinkedIn `linkedin.com/company/oryzz`.
- Los correos personales (`juan@oryzz.com`, `david@oryzz.com`) y los teléfonos son **marcadores editables**: márcalos como `{{...}}` o déjalos en un campo fácil de cambiar.

## 1. Idea de marca

**Plataforma:** *Sistemas que captan clientes.* Oryzz no hace acciones sueltas; monta un sistema que gira solo y se mide en clientes y en euros.

**Concepto visual: «Órbita y nodo».** La O de Oryzz es una órbita abierta (el sistema en marcha, automatización, el ciclo que no se detiene). El **nodo** lima es el resultado medible: el lead, la cita, el cliente. Todo el sistema gráfico sale de ahí: órbitas, rutas, nodos y datos.

**Frases de marca (reales, de la web):**
- «Más clientes. No más likes.» (claim principal)
- «Un sistema de captación, no acciones sueltas.»
- «El problema no es que no te vean. Es que no te contactan.»
- «30 minutos. Sales con un diagnóstico, no con un presupuesto.»
- «Te traemos clientes, no likes.»
- Tap: «Tu negocio. A un toque.» · «Conecta lo que eres. Acerca lo que sigue.»

## 2. Logo (v2)

Los archivos maestros están en `02_Logos/` y se generan con `00_Fuente_Maestra/build/oryzz_logo.py`. **Nunca redibujes el logo ni lo escribas con texto vivo.** Usa siempre los SVG.

- **Wordmark:** «oryzz» en minúscula, Space Grotesk Bold vectorizada, tracking −0,038 em con kerning óptico. «ory» en sólido, «zz» en gradiente IA (la firma).
- **Isotipo:** órbita abierta (arco de 283,4° medido en el eje entre los centros de las puntas, ≈ 302° visibles con las puntas redondas; hueco superior de 76,6°; trazo = 11 % de la caja, puntas redondas) + nodo. **Novedad v2:** el nodo está *separado* del trazo por un corte de 2,5 unidades. Así se reproduce limpio en una tinta, en bordado, en grabado láser y a tamaños pequeños.
- **Versiones:** horizontal (principal), vertical, wordmark solo, isotipo, isotipo pequeño (trazo reforzado 14 %, para ≤ 24 px), avatar cuadrado y circular, favicon, submarca «oryzz tap».
- **Colorways:** `color-sobre-oscuro` (principal), `color-sobre-claro`, `solido-sobre-oscuro/claro` (sin gradiente, para bordado, vinilo, impresión barata, email), `sobre-azul`, `sobre-lima`, `mono-blanco`, `mono-grafito`, `mono-negro`, `mono-azul`.
- **Área de respeto:** en los cuatro lados del logo, como mínimo **x = la altura de la «z» del wordmark** (en el lockup horizontal, ≈ 60 % del diámetro exterior del isotipo). En el isotipo solo: 25 % de su ancho.
- **Tamaño mínimo:** horizontal 88 px de ancho en pantalla / 22 mm impreso. Isotipo 16 px / 5 mm (por debajo de 24 px usa `isotipo-small`). Por debajo de 120 px de ancho usa la versión `solido` (el gradiente se ensucia).
- **Prohibido:** estirar, rotar (salvo la animación oficial), cambiar colores fuera de los colorways, añadir sombras, contornos o brillos, poner el gradiente sobre fondos con foto sin velo, reordenar ory/zz, poner el nodo en otro sitio, usar las estrellas del logo antiguo de Tap, escribir «OryzzTAP» o «ORYZZ».
- **Nombre en texto corrido:** «Oryzz» (O mayúscula) y «Oryzz Tap» (dos palabras, T mayúscula). El logo siempre va en minúscula.

## 3. Color

Proporción de uso: **60 % Grafito · 25 % Blanco / Grafito 50 · 10 % Azul IA / Cyan · ≤ 5 % Lima.** El lima es el nodo: *un dato, una acción, un punto*. Nunca fondos grandes de lima salvo piezas puntuales de campaña.

**Acento:** el Azul IA y el gradiente IA son el color de marca y no cuentan como acento. El acento es el lima: como máximo **un elemento lima por pieza**.

**Lima sobre claro:** el lima nunca va como texto sobre fondo claro. En claro, los deltas y datos van en Grafito 950 con un nodo Lima 600 al lado.

| Token | HEX | Uso |
|---|---|---|
| Grafito 950 | `#0B0D12` | Fondo principal oscuro, texto sobre claro |
| Grafito 900 | `#0E1118` | Fondo oscuro alternativo (secciones alternas) |
| Grafito 850 | `#12151D` | Superficie / tarjetas en oscuro |
| Grafito 800 | `#171B25` | Superficie elevada |
| Grafito 700 | `#232836` | Bordes en oscuro |
| Grafito 600 | `#3A4152` | Texto secundario en claro |
| Grafito 500 | `#5A6172` | Texto terciario en claro (6,2:1 sobre blanco) |
| Titanio 400 (token `grafito-400`) | `#8A90A0` | Texto terciario en oscuro (6,1:1). **No usar para texto sobre blanco** (3,2:1) |
| Grafito 300 | `#C7CBD6` | Bordes y líneas de énfasis en claro, estados desactivados |
| Grafito 200 | `#D5D9E0` | Bordes en claro, texto secundario en oscuro |
| Grafito 100 | `#E5E8EE` | Separadores, superficies claras |
| Grafito 50 | `#F6F7F9` | Fondo claro alternativo |
| Azul IA 500 | `#3B72FF` | Color de marca. Acento, gráficos, logo. Texto solo ≥ 24 px |
| Azul 400 | `#5C8BFF` | Azul sobre fondo oscuro |
| Azul 600 | `#2C5BD0` | **Botones y enlaces sobre claro** (6,0:1 con blanco) |
| Azul 300 | `#9FB8FF` | Enlaces sobre oscuro |
| Cyan 500 | `#36CFE0` | Final del gradiente en oscuro, datos |
| Cyan 600 | `#17A9C2` | Final del gradiente en claro |
| Lima 500 | `#BFF24A` | Nodo, dato destacado, estado «en marcha» (solo sobre oscuro) |
| Lima 600 | `#7FB02E` | Nodo sobre fondo claro |

**Gradiente IA:** oscuro `135° #5C8BFF → #36CFE0`; claro `135° #3B72FF → #17A9C2`. Solo en: logo, botones principales en oscuro, una línea o un dato por pieza. **Nunca** en párrafos, fondos completos ni degradados de más de dos colores. Nada de violeta ni de neón.

**Botones (corrige la web actual):**
- Sobre oscuro: fondo gradiente IA + **texto Grafito 950** (6,1–10,3:1). El texto blanco actual sobre el gradiente baja a 1,9:1 en el extremo cyan.
- Sobre claro: fondo Azul 600 `#2C5BD0` + texto blanco (6,0:1).

## 4. Tipografía

- **Space Grotesk** (display): titulares, cifras grandes, logo. 500/600/700. Tracking negativo (ver `tokens.json`).
- **Manrope** (texto): párrafos, interfaz, documentos. 400/500/600/700.
- **JetBrains Mono** (datos): solo códigos, URLs técnicas y cifras tabulares. **Nunca** para etiquetas ni en mayúsculas.
- **Etiquetas (*eyebrow*):** tipo frase («Qué no necesita tu cliente»), Manrope 600, mismo tamaño que el texto o un punto menos, Grafito 500 (o Azul 600 para la etiqueta de sección), **sin mayúsculas ni tracking extra**. Sin números de sección («01 · Contexto» no).
- **Regla dura (2026-10-14):** prohibidas las etiquetas en MAYÚSCULAS espaciadas y las numeraciones de sección o de pasos («01», «Paso 02», «02 / 07» con ceros). Es el sello más reconocible de un documento hecho con IA. El folio de página se permite sin ceros a la izquierda: «2 / 9».
- Office sin fuentes instaladas: Arial como alternativa. Las TTF están en `04_Tipografia/` (licencia OFL, se pueden instalar y compartir libremente).
- Titulares: frases cortas, máximo 2–3 líneas, con un solo fragmento resaltado en Azul (en la web se usa «Más **clientes**.»). Nunca frases enteras en gradiente.

## 5. Sistema gráfico

1. **Órbitas:** arcos abiertos concéntricos, trazo 1–2 px en Grafito 700 (oscuro) o Grafito 200 (claro), con un solo nodo lima o azul. Recurso de fondo y de portada.
2. **Rutas y nodos:** líneas ortogonales con esquinas redondeadas que conectan nodos (canal → sistema → cliente). Explican procesos.
3. **Retícula técnica:** cuadrícula de 64 px al 3,5 % de opacidad en oscuro y al 5 % en claro, desvanecida en los bordes. Solo como textura, nunca protagonista.
4. **Tarjetas dato:** superficie Grafito 850, borde 1 px Grafito 700, radio 14 px (`radius m`, el mismo que los botones), etiqueta en tipo frase (Manrope 600), cifra en Space Grotesk 500 y delta en lima.
5. **Iconografía:** retícula 24 px, trazo 1,75 px, puntas y uniones redondeadas, monocromo (Grafito 200 en oscuro / Grafito 950 en claro); el acento solo en un elemento. Se prohíben iconos rellenos de stock, emojis e iconos de colores mezclados. Los logos de plataformas (Meta, Google, TikTok) se usan solo en su versión monocroma.
6. **Fotografía:** personas reales de negocios reales (clínicas, estética, fitness, hostelería), luz natural, encuadres cercanos a manos, mostradores o pantallas; graduación fría y neutra. Nada de stock de apretón de manos, cerebros, robots ni hologramas. Sobre foto: velo Grafito 950 al 55–70 %.
7. **Motion:** la órbita gira (4,4 s lineal), el nodo respira y las «zz» saltan (1,95 s, resorte, desfase 0,17 s). Solo en intros, loaders y cierres; nunca en bucle dentro de la interfaz.

## 6. Voz

Clara, directa, segura, sin humo. Habla de clientes, citas, mensajes y euros, no de «impresiones» ni de «engagement».
- **Sí:** «Validamos con datos si tu negocio puede captar antes de que gastes de más.» «Si no encajamos, te lo decimos.»
- **No:** «Lleva tu negocio al siguiente nivel», «Multiplica tus ventas en 7 días», «Resultados garantizados», «Marketing 360», emojis en titulares, exclamaciones dobles.
- Tuteo. Frases cortas. Cifras concretas («30 minutos», «50–100 €», «3–7 días»). Un único CTA por pieza.
- Tap: más cálido y de producto («Acerca el teléfono y ocurre»), mismas reglas.

## 7. Submarca Oryzz Tap

Oryzz Tap **usa el mismo sistema** que Oryzz (paleta, tipografías y logo). Diferencias permitidas: expresión principal en **claro** (fondo Grafito 50 / blanco), fotografía de producto, más uso de blanco. El lockup es «[isotipo] oryzz tap», con «tap» en Space Grotesk Medium, color Titanio (o el color mono del colorway).
**Migración:** la web de Tap usa hoy Syne + Outfit, azul `#0075FF`, lima `#C5F500` y un logo con estrellas. Todo eso queda obsoleto (ver `12_Auditoria_y_Mejoras`).

## 8. Reglas anti «AI slop» (obligatorias en todas las piezas)

1. Nada de manchas de luz difusas, esferas brillantes, auroras ni *glassmorphism* como protagonistas. Como máximo un halo radial muy sutil (≤ 20 % de opacidad) por composición.
2. Nada de violeta, magenta ni gradientes de tres colores. Nada de neón.
3. Nada de emojis, ni de iconos genéricos de cohete, bombilla, cerebro o robot.
4. Nada de *lorem ipsum*: se escribe con copy real de Oryzz (sección 1) o con ejemplos verosímiles de PYMES (clínica dental, centro estético, gimnasio).
5. Composiciones asimétricas con jerarquía clara; no todo centrado ni todo en tarjetas idénticas en rejilla de tres.
6. Un solo acento por pieza. Si ya hay lima, no hay más colores de acento.
7. Cifras con unidades y fuente reales; no se inventan resultados de clientes como si fueran reales: se marcan como «Ejemplo» o como `{{dato}}`.
8. Nada de etiquetas en MAYÚSCULAS espaciadas ni numeraciones de sección o pasos (ver sección 4). Ni en documentos, ni en slides, ni en redes, ni en vídeo.
9. Alineación a la retícula, márgenes generosos, y tamaño mínimo de texto:
   - Pantalla: 14 px.
   - Impreso: 9 pt.
   - Slides a 1920×1080: texto de lectura ≥ 36 px (18 pt); etiquetas, eyebrows y notas de fuente ≥ 24 px (12 pt).
   - Diagramas incrustados: etiquetas ≥ 18 px al tamaño de exportación.
