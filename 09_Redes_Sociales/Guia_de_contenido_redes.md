# Guía de contenido para redes · Oryzz y Oryzz Tap

> Complementa a `BRAND_SPEC.md` (§6 Voz, §8 anti «AI slop») y a `LEEME.md` (cómo usar el generador).
> Regla madre: **una idea, un dato, una acción por pieza.** Si una pieza necesita dos CTA, son dos piezas.

---

## 1. Cuentas y papel de cada una

| Cuenta | Papel | Expresión | Público |
|---|---|---|---|
| Instagram **@oryzzai** | Autoridad y captación de la agencia | Oscura principal, clara para alternar en la cuadrícula | Dueños de PYMES de servicios en España: clínicas, estética, fisioterapia, fitness, hostelería |
| Instagram **@oryzztap** | Producto y venta directa | Clara (Grafito 50 / blanco), más cálida | Negocios con mostrador en Colombia: cafeterías, restaurantes, clínicas, peluquerías |
| TikTok **@oryzz.tap** | Demostración de producto en vídeo corto | Clara, portadas con la plantilla `reel_portada` | Mismo que @oryzztap |
| LinkedIn **company/oryzz** + perfiles de Juan Salazar y David Morales | Criterio profesional, método, casos | Oscura; datos en claro | Dueños y gerentes, socios potenciales |
| YouTube | Explicaciones largas (GEO, captación) | Oscura, miniatura con foto real | Quien ya busca aprender |
| WhatsApp Business / Google Business Profile | Confianza en el punto de contacto | Avatar e isotipo; portada con claim | Quien ya te está evaluando |

## 2. Pilares de contenido

| Pilar | Qué cuenta | Peso @oryzzai | Formatos preferidos |
|---|---|---|---|
| **1. Captación que se mide** | Anuncios que generan mensajes, citas y clientes, no impresiones. Presupuestos, pruebas, métricas que importan | 30 % | Cifra, mito vs realidad, carrusel |
| **2. Respuesta y seguimiento** | Velocidad de respuesta, automatización con IA, recordatorios, no perder leads | 25 % | Antes/después, checklist, story pregunta |
| **3. Visibilidad local y GEO** | Ficha de Google, reseñas, que ChatGPT, Gemini y Perplexity te entiendan y te nombren | 25 % | Carrusel, servicio, story dato |
| **4. Método y confianza** | Cómo trabajamos (valoración 30 min → prueba 3–7 días → escalado), límites honestos, equipo | 20 % | Proceso, CTA, cita (solo con testimonio real) |

**Oryzz Tap:** 40 % producto y uso (cómo funciona, dónde ponerlo), 30 % prueba social y resultados de reseñas (solo reales y autorizados), 20 % educación sobre reseñas de Google, 10 % oferta.

## 3. Formatos y cuándo usarlos

| Formato | Tamaño | Úsalo para | Plantilla |
|---|---|---|---|
| Post feed | 1080×1350 (4:5) | Una idea con impacto, un dato | `post_*` |
| Carrusel | 1080×1350 × 5–10 | Explicar un problema y su solución; guardados y compartidos | `carrusel` |
| Story | 1080×1920 | Conversación: preguntas, encuestas, avisos, CTA con enlace | `story`, `post_cta`, `post_cita` |
| Reel / TikTok | 1080×1920 vídeo + portada | Demostraciones de 15–45 s; la portada con `reel_portada`. Subtítulos sin caja (BRAND_SPEC §5.8): Manrope Bold blanco con sombra difusa Grafito 950, máx. 2 líneas, ≥ 48 px; edición con la skill `editor-oryzz` | `reel_portada` |
| Post LinkedIn | 1200×1200 o 1200×1500 | Criterio, método, datos | `post_titular`, `post_cifra`, `post_proceso` |
| Documento LinkedIn | PDF 1080×1350 | Guías de 6–10 páginas | `li_documento` + slides `carrusel` |
| Miniatura YouTube | 1280×720 | Vídeos largos, siempre con foto real | `yt_miniatura` |

## 4. Jerarquía y reglas de texto en imagen

Orden de lectura en todas las piezas: **etiqueta (contexto) → titular (la idea) → apoyo (1–2 frases) → acción o fuente**. El logo arriba a la izquierda; handle y web en el pie.

| Elemento | Máximo | Tamaño en 1080 px | Notas |
|---|---|---|---|
| Etiqueta (eyebrow) | 5 palabras | 28 px Manrope 600, tipo frase, sin tracking | Contexto o categoría, nunca el mensaje. Sin mayúsculas espaciadas ni numeraciones («01 ·», «Razón 1 de 4», «Episodio 01») |
| Titular | **12 palabras** (post), **9** (story), **6** (miniatura YouTube, portada Reel) | 70–118 px | Máx. 3–4 líneas. Un solo fragmento en `**azul**` |
| Texto de apoyo | **30 palabras** | 30–34 px | Nunca un segundo titular |
| Ítems de lista | 5 ítems × **10 palabras** | 28–32 px | Empiezan con verbo o sustantivo, sin punto final |
| Nota / fuente | 20 palabras | 22 px Manrope 500 | Obligatoria si hay un dato externo |
| Slide de carrusel | **45 palabras** en total | — | Una idea por slide |
| Total story | **30 palabras** | — | Se lee en 3 segundos |

Reglas:
- Tuteo, frases cortas, cifras concretas con unidad («30 minutos», «50–100 €», «3–7 días»).
- Un solo acento por pieza: si hay lima (dato o nodo), no hay otro color de acento.
- Nada de emojis, exclamaciones dobles, «siguiente nivel», «resultados garantizados», «multiplica tus ventas».
- Nunca inventar resultados de clientes. Si es ilustrativo: etiqueta «Ejemplo». Si falta el dato: `{{dato}}` hasta tenerlo.
- Nombres: «Oryzz» y «Oryzz Tap» en texto; el logo siempre es el SVG (nunca texto vivo).
- Texto mínimo: 20 px sobre 1080 px de ancho (se ve a ~7 px en móvil: por debajo es ilegible); etiquetas y pies, 24 px o más.
- JetBrains Mono solo para dato técnico (URL como `cal.com/oryzz/30min`, códigos). Chips, rótulos, pies y contadores van en Manrope. El folio de carrusel va sin ceros: «2 / 8».
- Los pasos se distinguen por su título o por un nodo, nunca por un número.

## 5. Zonas seguras por red

| Red / formato | Zona segura para texto | Qué tapa la interfaz |
|---|---|---|
| Instagram post 4:5 | Todo el lienzo; margen de 88 px | La cuadrícula del perfil recorta a 3:4 (1080×1440 de un 4:5 se ve completo; los 1:1 antiguos se recortan). Mantén el titular en el 80 % central |
| Instagram Stories | y 210–1620 px, x 88–992 px | Arriba 0–210: barra de progreso y perfil. Abajo 1620–1920: respuesta y enlaces |
| Instagram Reels | y 220–1500 px, x 88–940 px | Arriba 0–220: cabecera y audio. Abajo 1500–1920: descripción y botones. Derecha 140 px: botones |
| TikTok | y 160–1440 px, x 88–900 px | Abajo 480 px: descripción. Derecha 180 px: botones |
| Portada de Reel en perfil | Recorte central 3:4 (y 240–1680) | Todo lo que quede fuera no se ve en la cuadrícula |
| Portada de destacado | Círculo central | Instagram recorta un círculo; el icono va en el centro |
| LinkedIn empresa 1128×191 | x 250–1090 | Logo de empresa abajo a la izquierda (escritorio); en móvil se recortan los lados |
| LinkedIn perfil 1584×396 | x 600–1500 | La foto de perfil tapa la zona inferior izquierda (0–520 × 150–396) |
| YouTube 1280×720 | Evita la esquina inferior derecha | Duración del vídeo |
| OG 1200×630 | 80 % central | WhatsApp, Slack y LinkedIn recortan a 1,91:1 o cuadrado |
| WhatsApp 640×640 | Círculo inscrito | Isotipo al 46 % del lado |
| Google Business Profile | 80 % central | Google recorta según dispositivo |

Guías visuales: `Stories/_guia_zonas_seguras.png`, `Otros/_guias/`, `LinkedIn/_guias/`.

## 6. Cómo usar el generador (resumen)

1. Escribe el copy en `_generador/contenido/*.json` (o en una hoja de cálculo exportada a CSV).
2. `python generar.py <archivo> --solo <id>` para una pieza; `python generar.py --hojas` para todo con hojas de contacto.
3. Atiende los `aviso` (demasiadas palabras) y los `DESBORDA` (no cabe): recorta el copy, no bajes el tamaño a mano.
4. Revisa la pieza a tamaño móvil (al 33 %) antes de publicar: si el titular no se lee en 2 segundos, sobra texto.
Detalle completo en `LEEME.md`.

## 7. Calendario tipo semanal

| Día | @oryzzai (feed) | @oryzzai (stories) | @oryzztap | LinkedIn |
|---|---|---|---|---|
| Lunes | Carrusel educativo (pilar 1 o 3) | Pregunta de la semana | Post producto o uso | Post de Juan: criterio de captación |
| Martes | — | Encuesta + resultado al día siguiente | Reel/TikTok demostración | — |
| Miércoles | Cifra o mito vs realidad | Dato + enlace al carrusel del lunes | Story cómo funciona | Post de empresa: dato 4:5 |
| Jueves | Antes/después o checklist (pilar 2) | Detrás de cámaras del equipo | Reel/TikTok: dónde ponerlo | Post de David: automatización |
| Viernes | CTA valoración 30 min (1 de cada 2 semanas) o servicio | CTA con enlace a cal.com/oryzz/30min | Promoción (máx. 2 al mes) | Documento PDF (1 al mes) |
| Sáb–Dom | — | Repost de reseñas reales (si hay) | Story de cliente real (si hay) | — |

Ritmo mínimo sostenible: 3 posts + 5 stories por semana en @oryzzai; 3 piezas + 2 vídeos en Tap; 2 posts en LinkedIn. Mejor constante que intenso.

## 8. Veinte ideas de posts (titulares en la voz de Oryzz)

| # | Pilar | Formato | Titular | Apoyo |
|---|---|---|---|---|
| 1 | Captación | Titular | Tu mejor anuncio no sirve si nadie **contesta**. | Casi todo el trabajo empieza después del clic: responder, agendar y recordar la cita. |
| 2 | Captación | Mito vs realidad | Mito: «Necesito más seguidores». Realidad: necesitas más **citas**. | Los seguidores no pagan facturas. Las citas sí. |
| 3 | Captación | Cifra | Con **50–100 €** ya sabes si tu negocio puede captar. | Una prueba de 3–7 días antes de comprometer más presupuesto. |
| 4 | Captación | Carrusel | 5 señales de que tus anuncios traen **curiosos**, no clientes. | Mensajes que no responden, citas que no llegan, formularios a medias… |
| 5 | Captación | Titular | Antes de gastar más, **valida** con datos. | Una prueba corta dice más que tres meses de suposiciones. |
| 6 | Respuesta | Checklist | ¿Pierdes clientes por **contestar tarde**? 5 comprobaciones. | Tiempo de respuesta, horario, mensaje de bienvenida, seguimiento, recordatorio. |
| 7 | Respuesta | Antes/después | El mismo WhatsApp. Otra **respuesta**. | Antes: «Te escribo mañana». Después: cita propuesta en un minuto. |
| 8 | Respuesta | Titular | Un lead que espera un día ya está hablando con **otro**. | La primera respuesta la automatizamos; la conversación sigue siendo tuya. |
| 9 | Respuesta | Carrusel | Qué automatizar primero en una clínica (y qué **no**). | Confirmaciones y recordatorios sí; el diagnóstico, nunca. |
| 10 | Respuesta | Story encuesta | ¿Cuántas citas se te caen cada semana por **no confirmar**? | Vota y te contamos cómo recuperarlas. |
| 11 | Local y GEO | Carrusel | Por qué tu clínica no aparece cuando alguien pregunta a **ChatGPT**. | Cuatro razones y qué hacer con cada una. |
| 12 | Local y GEO | Titular | Tus clientes ya no buscan. **Preguntan**. | Y la respuesta son dos o tres nombres, no diez enlaces. |
| 13 | Local y GEO | Checklist | Tu ficha de Google, revisada en **5 minutos**. | Horario, fotos, categoría, respuestas, enlace de cita. |
| 14 | Local y GEO | Titular | Las reseñas no se piden al final. Se piden **en el momento**. | Justo cuando el cliente sale contento. |
| 15 | Local y GEO | Mito vs realidad | Mito: «Con la web ya basta». Realidad: la IA lee **todo lo que dicen de ti**. | Directorios, reseñas, prensa local y tu ficha cuentan. |
| 16 | Método | Proceso | Así pasamos de la idea a **clientes** medibles. | Valoración 30 min → prueba 3–7 días → escalado de lo que funciona. |
| 17 | Método | Titular | Si no encajamos, **te lo decimos**. | En la valoración sales con un diagnóstico, no con un presupuesto. |
| 18 | Método | Titular | No garantizamos ventas. Medimos **potencial real**. | Y solo escalamos lo que los datos confirman. |
| 19 | Tap | Producto | Tu negocio. A un **toque**. | Acerca el móvil y tu cliente está en tu página de reseñas. |
| 20 | Tap | Cómo funciona | De cliente contento a reseña publicada en **30 segundos**. | Sin app, sin pilas, sin cuotas. |

Las ideas 1, 5, 13 y 14 ya están montadas como ejemplo en `_generador/contenido/lote_ideas.csv`.

## 9. Antes de publicar (control de 30 segundos)

- [ ] ¿Se entiende la idea en 2 segundos a tamaño móvil?
- [ ] ¿Un solo resaltado azul y, como mucho, un dato en lima?
- [ ] ¿Cifras con unidad y fuente, o marcadas como «Ejemplo»?
- [ ] ¿Un único CTA?
- [ ] ¿Texto dentro de la zona segura de esa red?
- [ ] ¿Tildes, «¿» y «¡» de apertura, «Oryzz Tap» bien escrito?
- [ ] ¿El precio de Tap está confirmado (o conserva la etiqueta de ejemplo)?
