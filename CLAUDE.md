# Instrucciones para agentes · Identidad visual Oryzz

Este repositorio es el sistema de marca de Oryzz y Oryzz Tap. Cualquier pieza que produzcas (post, carrusel, story, guion o edición de vídeo, anuncio, correo, propuesta, presentación, documento, web, impreso) debe seguirlo.

## Antes de producir

1. Lee `00_Fuente_Maestra/BRAND_SPEC.md` (reglas) y `00_Fuente_Maestra/tokens.json` (valores). Son la fuente de verdad.
2. Busca la plantilla de la carpeta correspondiente y su `LEEME.md` antes de crear algo desde cero (ver tabla «Uso rápido» del `README.md`).
3. Para el porqué de una regla, consulta `01_Guia_de_Marca/Oryzz_Guia_de_Marca_v2.pdf`.

## Reglas que no se negocian

- **Logo:** siempre los SVG de `02_Logos`. Nunca texto vivo, nunca redibujado. Colorway según el fondo. Por debajo de 120 px de ancho, versión `solido`.
- **Nombre en texto:** «Oryzz» y «Oryzz Tap». Nunca «ORYZZ», «OryzzTAP» ni «oryzz» en una frase.
- **Color:** 60 % Grafito · 25 % Blanco · 10 % Azul IA / Cyan · ≤ 5 % Lima. **Un solo elemento lima por pieza**; lima nunca como texto sobre fondo claro.
- **Gradiente IA:** solo en el logo, el botón principal sobre oscuro, o una línea / un dato. Nunca en párrafos ni fondos completos. Nada de violeta, magenta, neón ni gradientes de tres colores.
- **Botones:** sobre oscuro, gradiente + texto Grafito 950 `#0B0D12`. Sobre claro, Azul 600 `#2C5BD0` + blanco. Sin sombras de color.
- **Tipografía:** Space Grotesk (titulares, 2–3 líneas, un fragmento en azul), Manrope (texto), JetBrains Mono solo para códigos y cifras técnicas (nunca etiquetas). Mínimos: 14 px pantalla · 9 pt impreso · ≥ 36 px de lectura en slides 1920×1080.
- **Sin etiquetas en MAYÚSCULAS espaciadas ni numeraciones de sección** («QUÉ NO NECESITA TU CLIENTE», «01 · CONTEXTO», «PASO 02»): canta a plantilla de IA. Las etiquetas van en tipo frase (solo la primera letra en mayúscula), Manrope 600, sin tracking extra. Los pasos se distinguen por su título o por un nodo, no por un número. Vale para slides, documentos, redes, correos y vídeo.
- **Voz:** tuteo, frases cortas, cifras concretas, un único CTA (verbo + resultado). Prohibido: «siguiente nivel», «revoluciona», «garantizado», «engagement», «GRATIS», «haz clic aquí», emojis en titulares, exclamaciones dobles.
- **Datos:** nunca inventar resultados de clientes como reales. Si no son reales, marcarlos «Ejemplo» o como `{{dato}}`.
- **Anti «AI slop»:** sin manchas de luz, esferas brillantes, auroras ni glassmorphism; sin cohetes, bombillas, cerebros ni robots; sin lorem ipsum; composición asimétrica con aire.
- **Oryzz Tap:** mismo sistema, expresión en claro (blanco / Grafito 50), foto de producto, tono más cálido.

## Vídeo

Intro oficial del logo (`02_Logos/08_Animado`) solo al principio o al final. Rótulos: etiqueta en tipo frase + titular Space Grotesk alineados a la izquierda en zona segura. Subtítulos en Manrope Bold, blanco sobre caja Grafito 950 al 70 %, ≥ 48 px en 1080×1920. Cortes secos o fundidos de 160–280 ms. Graduación fría y neutra.

## Mantenimiento

- No edites a mano PNG ni PDF exportados: cambia la fuente o el script de `00_Fuente_Maestra/build/` y regenera.
- Si cambias `BRAND_SPEC.md` o `tokens.json`, regenera la guía: `python 00_Fuente_Maestra/build/guia_marca.py` y `guia_extras.py`.
- La plantilla antigua de documentos (navy + Montserrat) está obsoleta: usa `07_Documentos`.
