# Presentaciones · Oryzz y Oryzz Tap

Plantillas de presentación 16:9 (1920 × 1080 px / 33,867 × 19,05 cm) del sistema de marca Oryzz v2.0.
Todo sale de un único modelo en código (`00_Fuente_Maestra/build/pres_*.py`), así que el .pptx, la previsualización HTML/PDF y las miniaturas coinciden.

## Qué hay en esta carpeta

| Archivo | Qué es |
|---|---|
| `Oryzz_Plantilla_Presentacion_Oscura.pptx` | Plantilla principal (expresión oscura). 28 diseños en el patrón de diapositivas y 25 diapositivas de ejemplo ya maquetadas. |
| `Oryzz_Plantilla_Presentacion_Clara.pptx` | La misma plantilla en expresión clara (fondo blanco, azul 600 en botones, lima 600 en nodos). |
| `Oryzz_Deck_Comercial_Ejemplo.pptx` | Presentación comercial completa (15 diapositivas) para una clínica dental **ficticia**, «Clínica Dental Arce». Todas las cifras están marcadas como ejemplo. |
| `OryzzTap_Plantilla_Presentacion.pptx` | Plantilla de Oryzz Tap (expresión clara, 11 diapositivas): portada de producto, problema, toque/QR, líneas Reseñas Google y Oryzz Pro, formatos, activación, precios en COP de ejemplo, usos, pedidos y cierre. |
| `Oryzz_Plantilla_Presentacion_Previsualizacion.pdf` / `.html` | Plantilla oscura en HTML y PDF (una página por diapositiva, 1920 × 1080). Para compartir y para la guía de marca. |
| `*_Previsualizacion.pdf` | PDF de la versión clara, del deck comercial y de Oryzz Tap. |
| `_previews/<plantilla>/sNN.png` | Miniaturas 1280 × 720 exportadas por PowerPoint (render nativo) de cada diapositiva. |
| `_recursos/` | Recursos gráficos PNG 2x: retícula, órbitas, rutas del diagrama, logos rasterizados, ilustraciones de producto Tap. |

## Diseños incluidos (patrón de diapositivas)

Portada · Órbita, Portada · Tipográfica, Agenda, Separador de sección, Título + texto, Dos columnas, Cita / manifiesto, Cifra gigante, Tres KPIs, Gráfico, Tabla, Proceso en pasos, Canales → sistema → cliente, Antes / después, Caso de estudio, Plan 30-60-90, Equipo, Precios / planes, Imagen a sangre, Imagen + texto, Comparativa, Preguntas frecuentes, Lista de seis, Llamada a la acción, Cierre, Título y contenido, Solo título y En blanco.
Oryzz Tap añade: Tap · Portada producto y Tap · Dos columnas con imagen.

Los diseños no llevan número en el nombre, y los pasos, agendas y listas se distinguen por su título y por un nodo, nunca por «01», «Paso 02» o «02 / 07» (BRAND_SPEC §4).

Cada diseño tiene marcadores reales (título, textos, imagen, gráfico, tabla), pie y número de diapositiva. Las notas del orador de varias diapositivas explican cómo usarlas.

## Cómo usarlas

### PowerPoint (recomendado)
1. Instala las fuentes (ver abajo). Los .pptx ya llevan **las fuentes incrustadas**, así que se ven bien aunque no estén instaladas; para editar texto con ellas, instálalas.
2. Abre la plantilla, duplica la diapositiva de ejemplo que más se parezca a lo que necesitas (clic derecho > Duplicar) y cambia el texto. Para una diapositiva vacía: **Inicio > Nueva diapositiva** y elige el diseño.
3. Imágenes: clic en el icono del marcador de imagen. En «Imagen a sangre», el velo Grafito 950 al 62 % ya está encima del marcador: cambia la foto con clic derecho > **Cambiar imagen** para no perderlo.
4. Gráficos: son gráficos nativos. Clic derecho > **Modificar datos**. Barras grises = antes; azul = con el sistema.
5. Pie y numeración: **Insertar > Encabezado y pie de página**. El texto del pie se cambia ahí o en cada diapositiva.
6. Los colores de marca están en el tema (**Diseño > Variantes > Colores**): Texto/fondo oscuro 1 = Grafito 950, Claro 1 = blanco, Énfasis 1 Azul IA 500, 2 Cyan 500, 3 Lima 500, 4 Azul 600, 5 Titanio 400, 6 Lima 600. Las fuentes del tema son Space Grotesk (títulos) y Manrope (texto).
7. Para guardar tu propia plantilla: **Archivo > Guardar como > Plantilla de PowerPoint (.potx)**.

### Keynote (Mac)
1. Instala las fuentes con Catálogo Tipográfico **antes** de abrir el archivo.
2. **Archivo > Abrir** el .pptx. Keynote convierte los diseños en «maestros»; revisa que los marcadores de imagen sigan siéndolo (se mantienen en versiones recientes).
3. Keynote no lee algunos detalles de Office: el gradiente del texto de las cifras puede verse plano y el espaciado entre letras puede variar ligeramente. Revisa las portadas y las cifras gigantes.
4. Guarda como Keynote y, si quieres, **Archivo > Guardar como tema**.

### Google Slides
1. **Archivo > Importar diapositivas** (o sube el .pptx a Drive y ábrelo con Presentaciones).
2. Space Grotesk, Manrope y JetBrains Mono están en Google Fonts: ábrelas desde **Fuente > Más fuentes**. Las variantes Medium y SemiBold pueden importarse como Arial; selecciona el texto y vuelve a elegir «Space Grotesk» con el peso correspondiente.
3. Google Slides no incrusta fuentes, no aplica el gradiente al texto (queda un color sólido) y puede importar los gráficos nativos como imagen fija. Para gráficos editables, recréalos con Hojas de cálculo de Google usando los colores del tema.

## Fuentes que hay que instalar

En `04_Tipografia/TTF_estaticas/` (licencia OFL, gratuitas y redistribuibles):
- **Space Grotesk** — Bold (titulares), Medium (cifras), SemiBold.
- **Manrope** — Regular (texto), Medium, SemiBold, Bold.
- **JetBrains Mono** — Regular, solo para dato técnico: ejes de gráficos, cifras tabulares y códigos.

Windows: selecciona los .ttf > clic derecho > **Instalar para todos los usuarios**. Mac: doble clic > Instalar. Si una fuente falta y el archivo no la trae incrustada, Office la sustituye por Arial.

## Reglas de maquetación

- **Retícula:** 12 columnas en 1920 × 1080, **márgenes de 120 px** en los cuatro lados, medianil de 32 px (columna = 110,67 px). Todo el texto y los bloques arrancan en una columna. El pie y la numeración viven en el margen inferior (y = 1004 px).
- **Una idea por diapositiva.** Si necesitas dos mensajes, son dos diapositivas. El titular dice la conclusión, no el tema («Lo que cambia cuando hay un sistema», no «Antes y después»).
- **Tamaños mínimos:** texto de lectura **18 pt** como mínimo (cuerpo 20 pt, entradilla 24 pt, titulares 44 pt, portadas 80–96 pt). Las únicas excepciones son elementos de sistema que no se leen como contenido: etiquetas (14 pt), pie, número de diapositiva, fuentes de datos y ejes de gráfico (12–14 pt; nunca menos de 24 px en 1920 × 1080).
- **Jerarquía tipográfica:** Space Grotesk Bold con tracking negativo para titulares (máx. 2–3 líneas), Manrope para el texto y para las etiquetas (Manrope SemiBold, **tipo frase, sin mayúsculas ni tracking**: «Cómo trabajamos», no «CÓMO TRABAJAMOS»). JetBrains Mono solo para dato técnico (ejes, cifras tabulares). Resalta **un solo fragmento** del titular en azul.
- **Un acento por diapositiva:** el lima es el nodo (un dato, un punto, un resultado). Si la diapositiva lleva una cifra con gradiente IA, no lleva lima. Nunca fondos grandes de lima, ni violeta, ni gradientes de tres colores.
- **Composición asimétrica y aire:** no centres todo ni pongas tres tarjetas idénticas en fila. Deja vacío al menos un tercio de la diapositiva.
- **Datos honestos:** toda cifra lleva unidad y fuente. Si no es real, se marca como «Ejemplo» o como `{{dato}}`.
- **Fotografía:** personas y negocios reales, luz natural, graduación fría; sobre foto, velo Grafito 950 al 55–70 %. Nada de stock de apretones de manos, robots ni cerebros.
- **Un único CTA por presentación:** «Agenda tu valoración de 30 minutos» → `cal.com/oryzz/30min` (Oryzz) o `shop.oryzz.com` / `pedidos@oryzz.com` (Oryzz Tap).
- **Marcadores editables:** los correos personales y otros datos no confirmados van como `{{juan@oryzz.com}}`, `{{david@oryzz.com}}`, `{{Cliente}}`.

## Regenerar

```
cd 00_Fuente_Maestra/build
python pres_build_all.py
```
Necesita Python 3 con `python-pptx`, `Pillow`, `fontTools` y `qrcode`, y Chrome. Si hay PowerPoint para Windows instalado, el script incrusta las fuentes y exporta las miniaturas nativas (`pres_powerpoint.ps1`); sin PowerPoint genera los .pptx sin fuentes incrustadas.
Archivos: `pres_engine.py` (motor PPTX + HTML), `pres_assets.py` (recursos PNG), `pres_oryzz.py` (diseños y contenido Oryzz), `pres_tap.py` (Oryzz Tap), `pres_build_all.py` (todo).
