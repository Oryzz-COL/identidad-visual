# Guía de redacción de correos · Oryzz

> Para cualquier persona o agente que escriba un correo en nombre de Oryzz u Oryzz Tap.
> Base: `00_Fuente_Maestra/BRAND_SPEC.md` (voz §6, anti AI-slop §8). Si dudas: **más corto, más concreto, un solo paso siguiente.**

---

## 1. La voz en una frase

Clara, directa, segura y sin humo. Hablamos de **clientes, citas, mensajes y euros**, no de «impresiones», «engagement» ni «soluciones». Tuteamos. Frases cortas. Cifras concretas («30 minutos», «3–7 días», «11,40 €»).

- **Sí:** «Validamos con datos si tu negocio puede captar antes de que gastes de más.» · «Si no encajamos, te lo decimos.»
- **No:** «¡Lleva tu negocio al siguiente nivel!» · «Multiplica tus ventas en 7 días» · «Resultados garantizados».

Oryzz Tap es algo más cálido y de producto («Acerca el teléfono y ocurre»), con las mismas reglas.

---

## 2. Asunto

**Longitud:** 30–50 caracteres (en el móvil se cortan hacia el carácter 40). Lo importante, al principio.

**Fórmula:** *dato concreto o pregunta real + su negocio o su nombre*. Nada de mayúsculas enteras, emojis, signos de exclamación ni «RE:» falsos.

| Mal | Por qué | Bien |
|---|---|---|
| ¡¡Lleva tu clínica al siguiente nivel!! + emoji de cohete | Promesa vacía, exclamaciones, emoji | Pregunta sobre las citas de Clínica Arrieta |
| Newsletter Oryzz – Septiembre | No dice qué gano leyéndolo | Lo que aprendimos en septiembre captando clientes |
| Oferta exclusiva solo hoy | Suena a spam y activa filtros | Tu propuesta de captación para Clínica Arrieta |
| RE: nuestra conversación | «Re:» falso: destruye la confianza | Laura, una cosa que vi en tu ficha de Google |
| Informe | Genérico | Septiembre en Arrieta: 61 citas y el coste por lead a la baja |
| Tu pedido | Poco útil en una bandeja llena | Pedido #1047 confirmado: ya preparamos tu Oryzz Tap |
| Descubre cómo la IA revoluciona tu marketing | Jerga, «revoluciona», «descubre» | ¿Te nombra ChatGPT cuando buscan fisio en Valencia? |
| GRATIS: auditoría de tu negocio | Mayúsculas y «gratis» en el asunto | 30 minutos para ver dónde se pierden tus clientes |

**Personalización:** `{{nombre}}` o `{{negocio}}` solo si el dato está limpio en la lista. «Hola, CLINICA DENTAL ARRIETA SL» es peor que no personalizar.

---

## 3. Preheader

El texto gris que aparece junto al asunto. **40–90 caracteres.** Completa el asunto, no lo repite. Si no lo escribes, el cliente mostrará «Ver en el navegador» o el texto alternativo del logo.

- Asunto: *Confirmada tu valoración: jueves 8, 10:30* → Preheader: *30 minutos por videollamada. Te contamos qué tener a mano.*
- Asunto: *Activa tu Oryzz Tap en 2 minutos* → Preheader: *Acerca el teléfono, escribe tu código de 8 dígitos y elige qué se abre con cada toque.*

En las plantillas va en el `<div class="o-preheader">`, justo después de `<body>`. **Los correos 1 a 1 no llevan preheader oculto**: la primera frase hace ese papel.

---

## 4. Apertura

- Saludo: **«Hola, {{nombre}}:»** en correos 1 a 1; **«Hola, {{nombre}}.»** dentro de una frase en los de marca. Nunca «Estimado/a cliente».
- La primera frase dice **por qué escribimos**, con algo concreto. Nada de «Espero que estés bien», «Me pongo en contacto contigo para…» ni «En Oryzz somos líderes en…».
- Si es prospección, la primera frase va de **su negocio**, no del nuestro.

---

## 5. Un solo CTA

Un correo, **una acción**. En los de marca, un solo botón (verbo + resultado: «Agendar 30 minutos», «Activar mi Oryzz Tap», «Ver el panel completo»). Puede haber enlaces secundarios en texto pequeño (cambiar la cita, contacto de soporte), nunca otro botón.

En los 1 a 1, el CTA es **una pregunta fácil de responder** («¿Te mando en tres líneas lo que cambiaría primero?»), no un enlace.

Textos de botón prohibidos: «Haz clic aquí», «Saber más», «Descubre», «¡Empieza ya!».

---

## 6. Longitud

| Tipo | Palabras | Notas |
|---|---|---|
| Prospección (primer contacto) | 70–120 | Una observación real, qué hacemos, una pregunta, salida fácil |
| Seguimiento 1 | 30–60 | Mismo hilo, recordatorio en una frase |
| Seguimiento 2 (último) | 60–100 | Aporta una idea útil aunque no conteste |
| Transaccional (cita, pedido) | 80–180 | Datos arriba, instrucciones después |
| Bienvenida / informe | 200–400 | Escaneable: titulares, tarjetas, listas |
| Newsletter | 300–500 | 2–3 bloques, 5 minutos de lectura como máximo |

Párrafos de 3–4 líneas como mucho. Si un párrafo necesita «además», probablemente son dos.

---

## 7. Tono por tipo de correo

| Plantilla | Tono | Firma |
|---|---|---|
| `01_newsletter` | Didáctico, de colega que ha visto muchas cuentas. Aprendizajes, no autobombo | Juan y David |
| `02_prospeccion_primer_contacto` | Personal, concreto, humilde. Una persona que escribe a otra | Juan Salazar |
| `03_seguimiento_1/2` | Breve, sin presión, sin culpa («¿viste mi correo?» no) | Juan |
| `04_confirmacion_valoracion` | Práctico y tranquilizador | Juan Salazar |
| `05_bienvenida_onboarding` | Cálido y organizado: qué pasa, cuándo y quién | Juan y David |
| `06_informe_mensual` | Honesto con los datos, también cuando no son buenos | Quien lleva la cuenta |
| `07_propuesta_enviada` | Seguro, transparente con el precio, sin presión | Juan Salazar |
| `08/09_tap_*` | Cálido, de producto, instrucciones clarísimas | Equipo Oryzz Tap |

**Cuando los datos son malos (informe):** dilo en la primera línea y di qué cambiamos. «Octubre fue peor: 38 citas (−22 %). Esto es lo que ya hemos cambiado.»

---

## 8. Palabras y fórmulas prohibidas

**De voz (BRAND_SPEC §6):** siguiente nivel · multiplica · garantizado / resultados garantizados · marketing 360 · revoluciona · potencia · impulsa tu negocio · soluciones integrales · sinergia · disruptivo · «en la era de la IA» · líderes del sector · a medida (sin decir qué) · engagement · impresiones (como logro) · «no te lo pierdas» · «última oportunidad».

**De entregabilidad (activan filtros):** GRATIS en mayúsculas · 100 % gratis · dinero fácil · oferta exclusiva · actúa ya · sin riesgo · clic aquí · «¡¡» / «!!» · $$$ · asuntos EN MAYÚSCULAS.

**De forma:** emojis en asunto y titulares · lorem ipsum · cifras de clientes inventadas sin marcar como «Ejemplo» (§8.7) · «Estimado/a» · «Quedo a la espera de sus noticias» · firmar como «El equipo de marketing».

---

## 9. Checklist antes de enviar

**Contenido**
- [ ] El asunto tiene 30–50 caracteres, sin emojis ni exclamaciones.
- [ ] El preheader completa el asunto (40–90 caracteres). En los 1 a 1, la primera frase hace de preheader.
- [ ] La primera frase dice por qué escribimos.
- [ ] Hay **un solo** botón o una sola pregunta.
- [ ] Cifras con unidad y, si son de ejemplo, marcadas como «Ejemplo».
- [ ] No queda ningún `{{marcador}}` sin sustituir (busca `{{` en el HTML final o en la vista previa de la herramienta).
- [ ] Nombre y negocio bien escritos (tildes, mayúsculas).
- [ ] Lo ha leído alguien más, o lo has leído en voz alta.

**Técnica**
- [ ] Las imágenes cargan desde una URL pública (usa `_listo_para_enviar/`).
- [ ] Todas las imágenes tienen `alt`; el correo se entiende con las imágenes desactivadas.
- [ ] Todos los enlaces funcionan y el botón lleva a donde dice (revisa los **dos** `href` del botón: VML y `<a>`).
- [ ] Newsletter/comercial: enlace de baja y dirección postal presentes.
- [ ] Prueba enviada a Gmail (web y app), Outlook y iPhone; revisada en modo oscuro.
- [ ] Remitente real (`Juan de Oryzz <juan@oryzz.com>`), nunca `noreply@`.
- [ ] Versión de texto plano (`.txt`) cargada si la herramienta lo permite.

---

## 10. Entregabilidad

**Autenticación del dominio (una vez, en el DNS de oryzz.com):**
- **SPF:** un único registro TXT que autoriza a los servidores que envían por ti (Google Workspace, Brevo, Resend…). Ej.: `v=spf1 include:_spf.google.com include:spf.brevo.com ~all`.
- **DKIM:** firma criptográfica; cada plataforma te da su registro (Google Workspace, Brevo, Resend, Mailchimp). Actívalo en todas.
- **DMARC:** empieza con `v=DMARC1; p=none; rua=mailto:dmarc@oryzz.com` para observar, y sube a `p=quarantine` cuando SPF y DKIM pasen en todos los envíos. Gmail y Yahoo lo exigen para envíos masivos desde 2024.

**Separa los tráficos:** los 1 a 1 salen del Gmail personal de cada socio; la newsletter y los transaccionales desde Brevo/Resend con un subdominio (p. ej. `mail.oryzz.com` o `news.oryzz.com`). Si la newsletter tiene un mal día, no arrastra a los correos de Juan.

**Prospección en frío:**
- Calienta los buzones nuevos durante 2–3 semanas antes de enviar en frío y **no superes 30–50 correos al día por buzón**.
- Sin imágenes, sin botones, sin píxel de apertura y **sin enlaces en el primer correo**. Máximo un enlace en el último seguimiento.
- Escribe cada `{{observacion_concreta}}` a mano. Un texto idéntico enviado a 200 personas es spam, aunque vaya personalizado con el nombre.
- Legalidad (España): la LSSI (art. 21) limita las comunicaciones comerciales por correo no solicitadas, también entre empresas, y el RGPD aplica a los correos de personas (`laura@clinica.com`). Usa solo direcciones profesionales publicadas por la empresa, ofrece siempre la salida («respóndeme "no" y no vuelvo a escribirte») y respeta cada baja al momento. Ante la duda, consulta con vuestra asesoría: esta guía no es asesoramiento legal.

**Texto e imagen:** al menos un 60 % de texto real; nunca un correo que sea solo una imagen. Todo el texto importante en HTML, no dentro de imágenes.

**Enlaces:** con dominios propios o conocidos (oryzz.com, cal.com, shop.oryzz.com). Nada de acortadores (bit.ly). El texto del enlace dice adónde lleva.

**Listas:** doble confirmación en la newsletter; borra rebotes duros al momento y a quien no abre en 6 meses. **Enlace de baja visible** (y cabecera `List-Unsubscribe` de un clic, que Brevo, Mailchimp y Resend añaden si la activas).

**Peso:** HTML por debajo de 100 KB (Gmail recorta a partir de 102 KB). Las plantillas pesan 18–34 KB.

---

## 11. Asuntos de ejemplo (20)

**Prospección y seguimiento**
1. Pregunta sobre las citas de {{negocio}}
2. {{nombre}}, una cosa que vi en la ficha de {{negocio}}
3. ¿Quién responde los WhatsApp de {{negocio}} a las 22:00?
4. Citas de {{servicio}} en {{ciudad}}
5. Re: Pregunta sobre las citas de {{negocio}} *(solo en el mismo hilo)*

**Newsletter**
6. Lo que aprendimos en septiembre captando clientes
7. Por qué el lead de las 21:40 no te llama mañana
8. ¿Te nombra ChatGPT cuando buscan fisio en tu ciudad?
9. Tres cosas que movieron citas este mes
10. La reseña se pide en el mostrador

**Transaccionales y clientes**
11. Confirmada tu valoración: {{fecha}}, {{hora}}
12. Empezamos, {{nombre}}: tus próximos 7 días
13. Septiembre en {{negocio}}: 61 citas y el coste por lead a la baja
14. Octubre fue más flojo: esto es lo que ya hemos cambiado
15. Tu propuesta de captación para {{negocio}}
16. Faltan dos accesos para lanzar tus campañas

**Oryzz Tap**
17. Pedido {{numero_pedido}} confirmado: ya preparamos tu Oryzz Tap
18. Tu Oryzz Tap va de camino (seguimiento dentro)
19. Activa tu Oryzz Tap en 2 minutos
20. ¿Dónde has puesto tu placa? Tres sitios que funcionan

---

## 12. Plantilla de prospección, desmontada

```
Hola, {{nombre}}:                                   ← saludo 1 a 1

Buscando «{{servicio}} en {{ciudad}}» he visto que   ← observación REAL y concreta
{{negocio}} sale en el mapa, pero {{observacion}}.     (esto es lo que hace que no sea spam)
Son detalles pequeños que suelen costar citas.       ← consecuencia, sin dramatizar

Soy Juan, de Oryzz. Montamos sistemas de captación…  ← quién soy, en una frase
Lo medimos en citas, no en likes.                    ← frase de marca

¿Te mando en tres líneas lo que cambiaría primero?   ← CTA = pregunta fácil
Si no es buen momento, respóndeme «no»…              ← salida fácil (y legal)
```
