# 08_Email · Sistema de email de Oryzz (v2.0)

Plantillas HTML de producción, versiones en texto plano, firmas y guía de redacción. Es la base para **todos** los correos de Oryzz y Oryzz Tap.

- Antes de escribir un correo, lee **`Guia_de_redaccion_email.md`**.
- Para ver todas las plantillas de un vistazo, abre **`Oryzz_Email_Catalogo.pdf`**.

---

## 1. Índice

| Archivo | Tipo | Para qué | Se envía desde |
|---|---|---|---|
| `01_newsletter.html` | Marca | Novedades y aprendizajes del mes: 3 bloques + CTA | Brevo / Mailchimp |
| `02_prospeccion_primer_contacto.html` | 1 a 1 | Primer contacto en frío, casi texto plano | Gmail de Juan |
| `03_seguimiento_1.html` | 1 a 1 | Seguimiento a los 3 días hábiles (mismo hilo) | Gmail de Juan |
| `03_seguimiento_2.html` | 1 a 1 | Último seguimiento a los 7 días, con idea útil + agenda | Gmail de Juan |
| `04_confirmacion_valoracion.html` | Transaccional | Confirmación de la videollamada de 30 min y qué preparar | Resend / Brevo (webhook de cal.com) o a mano |
| `05_bienvenida_onboarding.html` | Cliente | Bienvenida: próximos pasos, accesos, equipo | Gmail / Brevo |
| `06_informe_mensual.html` | Cliente | Informe con tarjetas dato (**cifras de ejemplo**) | Gmail / Brevo |
| `07_propuesta_enviada.html` | Comercial | Envío de propuesta con resumen y CTA | Gmail / Brevo |
| `08_tap_pedido_confirmado.html` | Oryzz Tap | Confirmación de pedido (COP) | Shopify (notificaciones) |
| `09_tap_activacion.html` | Oryzz Tap | Activación: NFC/QR → 8 dígitos → cuenta → perfil | Shopify Flow / Brevo |
| `10_base_en_blanco.html` | Base | Esqueleto modular documentado con **todos** los bloques | — |

Cada `.html` tiene su `.txt` (texto plano) con el mismo nombre. Arriba del `.txt` van el asunto y el preheader, separados por una línea `====`: **no** los pegues en el cuerpo.

**Carpetas**

| Carpeta | Contenido |
|---|---|
| `assets/` | PNG a 2×: logos sólidos (fondo horneado), órbita del hero, diagrama, iconos de pasos (versión clara y oscura), avatares de firma. **Hay que subirla a un servidor** (ver §3). |
| `_listo_para_enviar/` | Las mismas plantillas con URL absolutas (`https://oryzz.com/brand/email/…`). **Son las que se importan** en Brevo, Mailchimp, Resend o Shopify. |
| `_previews/` | PNG de cada plantilla: `_escritorio-600`, `_movil-375` y `_oscuro-600` (modo oscuro de Apple Mail; los 1 a 1 no lo llevan porque dependen del cliente). |
| `firmas/` | Firmas de Juan, David y Oryzz Tap (completa y compacta) + `_copiar_firmas.html` + `como-instalar-en-gmail.md`. |

---

## 2. Qué incluye cada plantilla (técnica)

- Maquetación con tablas y CSS en línea, 600 px, fluida hasta 375 px (breakpoint 640 px).
- Condicionales MSO: tabla fija de 600 px, Arial forzada y botón VML (`v:roundrect`) en Outlook para Windows.
- Botón «bulletproof», **uno por correo**.
- `color-scheme: light dark` + CSS de modo oscuro para Apple Mail, iOS y Outlook macOS (`prefers-color-scheme`) y para Outlook.com (`[data-ogsc]`, `[data-ogsb]`). En oscuro, el botón pasa al gradiente IA con texto Grafito 950 y el logo de Tap cambia de versión. Gmail no permite controlar el modo oscuro: la cabecera Grafito 950 y los logos con fondo horneado garantizan que el logo se lea siempre.
- Fuentes web (Space Grotesk, Manrope, JetBrains Mono) por Google Fonts, con alternativa Arial / Consolas. **Gmail y Outlook muestran Arial**: es lo previsto.
- Preheader oculto, `alt` en todas las imágenes, `lang="es"`, `role="presentation"` en las tablas.
- Enlace de baja `{{baja_url}}` + `{{direccion_postal}}` en la newsletter (y disponibles en la base).
- Peso: 18–34 KB por plantilla (Gmail recorta a partir de 102 KB).

---

## 3. Primera vez: subir las imágenes

1. Sube **todo** el contenido de `assets/` a `https://oryzz.com/brand/email/`. En Vercel u otro hosting estático basta con meterlo en `public/brand/email/`.
2. Comprueba una URL en el navegador: `https://oryzz.com/brand/email/oryzz-logo_sobre-oscuro.png`.
3. **Si usas otra URL** (p. ej. un CDN o la biblioteca de imágenes de Brevo), regenera las copias:
   ```
   cd 00_Fuente_Maestra/build
   python email_publicar.py https://tu-url/email
   ```
   Así se reescribe `_listo_para_enviar/` con la nueva base. En las firmas, cambia la constante `BASE_URL` al principio de `firmas/_copiar_firmas.html` (y, en los `.html` sueltos, busca y reemplaza la URL).

---

## 4. Cómo editar

### Opción A · a mano (lo normal)

1. Duplica la plantilla más parecida (o `10_base_en_blanco.html`) y ábrela en VS Code.
2. Cada bloque va entre `<!-- ▸ BLOQUE · NOMBRE -->` y `<!-- ◂ FIN · NOMBRE -->`. Para añadir uno, **copia desde ▸ hasta ◂** de la base y pégalo dentro de la tarjeta. Para quitarlo, borra ese tramo.
3. Cambia solo textos, URL y `alt`. No toques los atributos `class` (`o-t1`, `o-bd`, `o-px`…): de ellos dependen el móvil y el modo oscuro.
4. **Botón:** URL y texto aparecen **dos veces** (VML para Outlook y `<a>` para el resto). Si el texto es largo, sube el `width` del `v:roundrect` (≈ 9,4 px por carácter + 60).
5. **Resaltado del titular:** `<span class="o-hl" style="color:#3B72FF;">palabra</span>`, uno por titular.
6. Abre el archivo en Chrome para revisarlo y, con las herramientas de desarrollo (Ctrl+Mayús+M), míralo a 375 px.
7. Actualiza el `.txt` si cambias el texto.
8. Genera las copias con URL absolutas: `python 00_Fuente_Maestra/build/email_publicar.py`.

### Opción B · desde el generador (cambios de sistema)

Todo el sistema sale de `00_Fuente_Maestra/build/`:

| Script | Hace |
|---|---|
| `email_lib.py` | Librería de bloques (cabecera, hero, titular, párrafo, botón, tarjetas dato, lista, cita, imagen, detalles, pasos, sección, personas, despedida, pie) y ensamblado HTML + TXT. |
| `email_build.py` | Contenido de las 11 plantillas y las firmas, assets, previsualizaciones y catálogo. |
| `email_publicar.py` | Copia a `_listo_para_enviar/` con URL absolutas. |
| `email_catalogo.py` | PDF del catálogo. |

```
python email_build.py             # todo (≈ 3–4 min)
python email_build.py plantillas  # solo HTML, TXT, firmas y _listo_para_enviar
python email_build.py previews    # solo PNG + PDF
```

> **Aviso:** `email_build.py` **sobrescribe** los HTML de `08_Email/`. Si has editado alguno a mano, no lo ejecutes entero (pierdes los cambios) o traslada antes tus cambios al script.

---

## 5. Marcadores

Todos los datos variables van como `{{marcador}}` en minúsculas. La lista exacta de cada plantilla está en su comentario de cabecera (línea `Marcadores:`).

| Marcador | Qué es | Ejemplo |
|---|---|---|
| `{{nombre}}` | Nombre de pila | Laura |
| `{{negocio}}` | Nombre comercial (sin «S.L.») | Clínica Dental Arrieta |
| `{{ciudad}}`, `{{servicio}}` | Para prospección | Valencia · implantes dentales |
| `{{observacion_concreta}}` | **Escrito a mano** por cada contacto | la ficha no tiene botón de reserva… |
| `{{fecha}}`, `{{hora}}` | Cita | jueves 8 de octubre · 10:30 |
| `{{enlace_videollamada}}`, `{{enlace_reprogramar}}` | Enlaces de cal.com | — |
| `{{email_juan}}`, `{{email_david}}`, `{{telefono_*}}` | Contacto del equipo | juan@oryzz.com |
| `{{id_business_oryzz}}`, `{{id_mcc_oryzz}}`, `{{email_accesos}}` | Accesos (onboarding) | — |
| `{{url_*}}` | Enlaces de panel, propuesta, pedido, activación, formulario | — |
| `{{numero_pedido}}`, `{{producto}}`, `{{total}}`, `{{plazo_entrega}}`… | Pedido Tap | #1047 · $ 89.900 COP |
| `{{baja_url}}` | Enlace de baja | lo pone la plataforma |
| `{{direccion_postal}}` | Dirección fiscal de Oryzz | — |

### Equivalencias por plataforma

| Oryzz | Brevo | Mailchimp | Shopify (Liquid) | Resend |
|---|---|---|---|---|
| `{{nombre}}` | `{{ contact.FIRSTNAME }}` | `*\|FNAME\|*` | `{{ customer.first_name }}` | variable de tu código |
| `{{negocio}}` | `{{ contact.EMPRESA }}` (atributo propio) | `*\|COMPANY\|*` o `*\|MMERGE3\|*` | — | ídem |
| `{{baja_url}}` | `{{ unsubscribe }}` | `*\|UNSUB\|*` | — | enlace propio + cabecera `List-Unsubscribe` |
| `{{direccion_postal}}` | texto fijo (escribe la dirección) | `*\|HTML:LIST_ADDRESS_HTML\|*` | `{{ shop.address.summary }}` | texto fijo |
| `{{numero_pedido}}` | — | — | `{{ order.name }}` | — |
| `{{url_pedido}}` | — | — | `{{ order_status_url }}` | — |
| `{{total}}` | — | — | `{{ total_price \| money_with_currency }}` | — |

Busca y reemplaza con cuidado: `{{nombre}}` → `{{ contact.FIRSTNAME }}` en todo el archivo. Después busca `{{` para asegurarte de que no queda ninguno sin sustituir.

---

## 6. Cómo usarlas en cada herramienta

### Gmail (correos 1 a 1, bienvenida, informe, propuesta)
- **Prospección y seguimientos (02, 03):** no pegues el HTML. Copia el texto del `.txt` (sin la cabecera `ASUNTO/====`), pégalo en un correo nuevo, sustituye los marcadores y envía. La firma compacta se añade sola. Los seguimientos se envían **respondiendo** al hilo.
- **Plantillas de marca en Gmail:** abre la versión de `_listo_para_enviar/` en Chrome, selecciona todo (Ctrl+A), copia y pega en un correo nuevo. Gmail conserva la mayoría del diseño (la tipografía pasa a Arial). Para no repetir el proceso: Configuración → Avanzado → activa **Plantillas** y guarda el correo como plantilla.
- Si pegas una plantilla de marca, **quita la firma** de Gmail de ese correo: la plantilla ya lleva despedida y pie.

### Brevo (newsletter, transaccionales)
1. Campañas → Crear → Correo → **Editor de código** (o Plantillas → Nueva → «Pegar tu código»).
2. Pega el HTML de `_listo_para_enviar/`.
3. Sustituye los marcadores por las variables de Brevo (tabla §5). Brevo añade su pie legal si falta el enlace de baja: con `{{ unsubscribe }}` no lo añade.
4. Asunto y preheader: cópialos del comentario de cabecera (Brevo tiene un campo «Texto de previsualización»; si lo rellenas, puedes dejar vacío el `div.o-preheader`).
5. Envía la prueba a Gmail, Outlook e iPhone.

### Mailchimp
1. Campaigns → Create → Email → **Code your own → Paste in code**.
2. Pega el HTML de `_listo_para_enviar/`, sustituye `{{baja_url}}` por `*|UNSUB|*`, `{{nombre}}` por `*|FNAME|*` y `{{direccion_postal}}` por `*|HTML:LIST_ADDRESS_HTML|*`.
3. En «Preview text» pega el preheader. Pestaña **Plain-text**: pega el `.txt` (sin cabecera).

### Resend (transaccionales desde código: 04, 08, 09)
```js
import { Resend } from 'resend';
import fs from 'node:fs';
const resend = new Resend(process.env.RESEND_API_KEY);
const fill = (s, d) => s.replace(/\{\{\s*(\w+)\s*\}\}/g, (_, k) => d[k] ?? '');
const html = fs.readFileSync('08_Email/_listo_para_enviar/04_confirmacion_valoracion.html', 'utf8');
const text = fs.readFileSync('08_Email/04_confirmacion_valoracion.txt', 'utf8').split('====\n\n').pop();
const d = { nombre: 'Laura', negocio: 'Clínica Dental Arrieta', fecha: 'jueves 8 de octubre', hora: '10:30' /* … */ };
await resend.emails.send({
  from: 'Juan de Oryzz <juan@mail.oryzz.com>',
  to: 'laura@clinicaarrieta.es',
  subject: fill('Confirmada tu valoración: {{fecha}}, {{hora}}', d),
  html: fill(html, d), text: fill(text, d),
});
```
Escapa los valores que vengan de formularios antes de meterlos en el HTML. Si tu proyecto usa React Email, estas plantillas sirven de referencia visual y de copy.

### Shopify (Oryzz Tap: 08)
Configuración → Notificaciones → **Confirmación de pedido** → Editar código → pega el HTML de `_listo_para_enviar/08_tap_pedido_confirmado.html` y cambia los marcadores por Liquid (tabla §5). Si el pedido tiene varios productos, sustituye la fila «Producto» por un bucle `{% for line in subtotal_line_items %}…{% endfor %}`. Guarda y usa «Enviar correo de prueba».

---

## 7. Reglas que no se negocian

- Un solo botón por correo. Un solo fragmento azul por titular. Lima solo como nodo o como dato que mejora.
- Nada de emojis en asuntos ni titulares; nada de «¡Lleva tu negocio al siguiente nivel!».
- Cifras de clientes reales solo con permiso; si no, «Datos de ejemplo» (BRAND_SPEC §8.7).
- Texto mínimo 14 px (los rótulos mono en MAYÚSCULAS, 12 px).
- Logos: siempre los PNG de `assets/` (versiones sólidas). Nunca el logo escrito con texto.

---

## 8. Limitaciones conocidas

- **Gmail** ignora las fuentes web y el CSS de modo oscuro: muestra Arial y aplica su propia inversión en la app. Las piezas críticas (cabecera oscura, logos con fondo horneado, iconos con losa) están pensadas para aguantarlo.
- **Outlook para Windows** no redondea esquinas (tarjetas, botón fuera de VML, avatar de firma) ni muestra las imágenes de modo oscuro. Es el comportamiento esperado.
- Las previsualizaciones se han generado con Chrome (motor similar a Apple Mail) y fuentes locales. Antes de un envío importante, prueba en clientes reales (o con Litmus / Email on Acid).
- `09_tap_activacion`: comprueba con producto **dónde viene impreso el código de 8 dígitos** y la URL real de activación antes de usarla.
- `08_tap_pedido_confirmado`: el plazo de entrega es un marcador (`{{plazo_entrega}}`); confirma el plazo real con logística.
