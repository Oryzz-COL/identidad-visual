# Oryzz · Dirección fotográfica v2.0

> Fuente: `00_Fuente_Maestra/BRAND_SPEC.md` §5.6 y §8. Si una foto no cumple esto, no se usa: mejor un fondo de marca (`03_Fondos`) que una foto genérica.

## 1. La idea

Oryzz habla de **clientes, citas, mensajes y euros**. La foto enseña el momento en el que eso pasa en un negocio real: alguien que llega al mostrador, una mano que confirma una cita en el móvil, una recepción con gente. No enseñamos «marketing», enseñamos **negocio funcionando**.

Oryzz Tap enseña **producto en uso**: la placa en el mostrador, el móvil que se acerca, la mano del cliente.

## 2. Qué sí / qué no

| Sí | No |
|---|---|
| Personas reales en negocios reales: clínica dental, centro estético, fisioterapia, gimnasio, restaurante, peluquería | Stock de apretón de manos, equipos riendo ante un portátil, trajes y oficinas de cristal |
| Manos, mostradores, pantallas de móvil, agendas, recepciones | Cerebros, robots, hologramas, circuitos, «IA» literal, cohetes, bombillas |
| Luz natural de ventana, lateral y suave | Flash frontal, neones, luces de colores, contraluces con destellos |
| Encuadres cercanos (plano medio, detalle) con aire en un lado para texto | Planos generales vacíos, simetría total centrada, collage de fotos |
| Graduación fría y neutra, negros densos, piel natural | Filtros cálidos de Instagram, HDR, saturación alta, virados violetas o magenta |
| Pantallas con interfaz desenfocada o genérica | Capturas legibles de apps de terceros, logos de Meta/Google/TikTok en color |
| Diversidad real de edades y tipos de negocio en España | Modelos de catálogo, sonrisas forzadas mirando a cámara |

## 3. Temas por línea

**Oryzz (captación)**
1. Recepción de clínica: la recepcionista atiende; en primer plano, un móvil con una conversación.
2. Manos que agendan: detalle de una mano en el móvil con un calendario desenfocado.
3. Centro estético o fisio: profesional con cliente, plano medio, luz de ventana.
4. Gimnasio de barrio: entrenadora con un cliente, poca gente, espacio ordenado.
5. Hostelería: sala a media tarde, camarero atendiendo, mesa en primer plano.
6. El dueño o la dueña del negocio mirando el móvil tras el mostrador (el «llega un lead»).

**Oryzz Tap (producto)**
1. Placa NFC sobre mostrador de madera clara o piedra, luz de ventana.
2. Mano de cliente acercando el móvil a la placa (el gesto del toque).
3. Stand en la mesa de un restaurante junto a la carta.
4. Detalle del móvil abriendo la reseña de Google (pantalla genérica, sin datos reales).

## 4. Luz, encuadre y graduación

- **Luz:** natural, lateral, de ventana. Sombras suaves. Nunca varias fuentes de color.
- **Encuadre:** plano medio o detalle. Deja **un tercio libre** (izquierda en 16:9, arriba en 4:5 y 9:16) para el titular. Sujeto hacia el tercio contrario, nunca centrado.
- **Profundidad:** f/2–f/4, fondo desenfocado pero reconocible (se entiende qué negocio es).
- **Graduación:** temperatura ligeramente fría (≈ 5200–5600 K), saturación −10 a −20, negros levantados lo mínimo, sin viñeta artificial. Verdes y rojos contenidos para que el lima del nodo sea el único acento.
- **Resolución mínima:** 2400 px en el lado largo (redes) · 3000 px (web a pantalla completa) · 300 ppp a tamaño final (impreso).

## 5. Tratamiento sobre foto (obligatorio con texto)

1. **Velo Grafito 950 `#0B0D12` al 55–70 %** sobre toda la foto. Más denso (70 %) del lado del texto, más ligero (55 %) del lado del sujeto. Es un degradado de **un solo color** en opacidad, no un degradado de colores.
2. **Texto** en blanco (titular) y Grafito 200 `#D5D9E0` (bajada). Eyebrow en JetBrains Mono.
3. **Órbita**: un arco abierto blanco al 30–40 %, trazo 2 px, que abraza al sujeto sin tocar su cara ni sus manos; con **un solo nodo lima** `#BFF24A` en su extremo, separado del trazo.
4. **Logo**: `color-sobre-oscuro` solo con velo; sin velo, usa `mono-blanco`.
5. **CTA**: botón primario oscuro (gradiente IA + texto Grafito 950).
6. En Oryzz Tap (claro) la foto va **luminosa y sin velo**; el texto se coloca en un bloque blanco o Grafito 50 contiguo, nunca sobre la foto.

Ejemplos en esta carpeta:
- `PNG/tratamiento-01_clinica_16x9.png` · velo lateral, órbita que abraza al sujeto, titular y CTA.
- `PNG/tratamiento-02_post_4x5.png` · post con velo superior, sujeto en el tercio inferior.
- `PNG/tratamiento-03_tap-producto_4x5.png` · producto Tap en claro, sin velo.
- `plantilla-foto-velo_16x9.html` · plantilla HTML: cambia `--foto` por `url('tu-foto.jpg')`.
- En los SVG, sustituye el grupo `<g id="foto">` por `<image href="tu-foto.jpg" width="…" height="…" preserveAspectRatio="xMidYMid slice"/>`.

> El rectángulo gris con grano es un **marcador de foto**, no una foto. No se publica tal cual.

## 6. Prompts sugeridos

Para generar con IA o buscar en bancos de imagen. Sustituye `[negocio]` y `[ciudad]`. Revisa siempre manos, texto en pantallas y logos antes de usar.

**Base (añádela a todos):**
> fotografía editorial documental, luz natural de ventana lateral y suave, graduación fría y neutra, saturación contenida, profundidad de campo reducida, 35 mm, plano medio, espacio libre en el tercio izquierdo para texto, sin texto, sin logos, sin neones, sin tonos violeta

1. **Recepción de clínica** · «recepcionista de una clínica dental en [ciudad] atendiendo a un paciente en el mostrador, en primer plano un móvil apoyado con una conversación de chat desenfocada, ambiente real y ordenado»
2. **Manos que agendan** · «detalle de las manos de una mujer de 40 años confirmando una cita en el móvil, calendario desenfocado en pantalla, mostrador de madera clara, luz de ventana»
3. **Centro estético** · «esteticista con clienta en cabina luminosa, plano medio desde el lateral, gesto de conversación, tonos neutros, sin mirar a cámara»
4. **Gimnasio de barrio** · «entrenadora personal corrigiendo la postura de un cliente de 50 años en un gimnasio pequeño y ordenado, luz natural, pocas personas al fondo»
5. **Dueño del negocio** · «dueño de una peluquería mirando el móvil tras el mostrador con media sonrisa, final del día, luz cálida muy suave compensada a neutra»
6. **Oryzz Tap · producto** · «placa cuadrada blanca con esquinas redondeadas sobre un mostrador de madera clara de una cafetería, luz de ventana, fondo desenfocado con clientes, fotografía de producto limpia»
7. **Oryzz Tap · gesto** · «mano de un cliente acercando un smartphone a una placa NFC blanca sobre el mostrador de un restaurante, detalle, pantalla sin contenido legible»

**Negativo (si la herramienta lo admite):**
> robot, cerebro, holograma, circuitos, neón, violeta, magenta, lens flare, apretón de manos, traje, oficina de cristal, texto, logotipos, marca de agua, HDR, piel plástica

**Búsqueda en bancos (palabras clave):** `dental reception candid`, `hands booking phone counter`, `small gym trainer candid natural light`, `salon owner phone counter`, `nfc tap phone counter`. Descarta cualquier resultado con sonrisa a cámara o fondo blanco infinito.

## 7. Checklist antes de publicar

- [ ] Negocio real y reconocible (o marcado como «Ejemplo» si es ilustrativo).
- [ ] Luz natural, graduación fría y neutra, sin colores ajenos a la paleta dominando.
- [ ] Hay aire para el texto; el sujeto no queda bajo el titular.
- [ ] Velo Grafito 950 55–70 % si hay texto encima.
- [ ] Un solo acento (nodo lima). Sin gradiente IA sobre la foto salvo en el logo o el CTA.
- [ ] Derechos de uso: foto propia, cedida por el cliente con permiso por escrito o con licencia comercial.
