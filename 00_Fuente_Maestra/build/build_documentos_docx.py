"""
Oryzz · genera las plantillas Word (.docx) de 07_Documentos.

    python build_documentos_docx.py          # todas
    python build_documentos_docx.py 01 05    # solo algunas
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from oryzz_docx import *  # noqa
from oryzz_docx import _set_fonts, _pborder, _tab_right, _tbl_look, _widths, _cell_shade
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUT = os.path.normpath(os.path.join(HERE, '..', '..', '07_Documentos'))
R = [2]  # columnas a la derecha (atajo)


def guia(doc, texto):
    """Instrucción para quien rellena la plantilla (borrar antes de enviar)."""
    p = P(doc, 'Guía · ' + texto, 'Nota')
    for r in p.runs:
        r.font.color.rgb = RGBColor.from_string(AZ600)
    return p


# ============================================================ 01 PROPUESTA
def propuesta():
    doc = new_doc()
    s = portada(doc, 'Propuesta comercial',
                'Un sistema que llena tu agenda de [[{{resultado}}]].',
                '{{Una frase: qué captamos, para quién y con qué piezas (anuncios, WhatsApp automatizado, seguimiento).}}',
                [('Preparado para', '{{Cliente · Ciudad}}'), ('Fecha', '{{dd mmm aaaa}}'), ('Versión', 'v1.0'), ('Contacto', 'Juan Salazar\n{{juan@oryzz.com}}')])
    running_header(s, 'Propuesta · {{Cliente}}', 'oryzz.com · Propuesta válida 30 días')

    eyebrow(doc, 'Contexto', '01')
    h(doc, '{{Titular de contexto: una idea, máximo 2 líneas.}}')
    P(doc, '{{Quién es el cliente, cuánto tiempo lleva, tamaño del equipo y cómo llegan hoy sus clientes.}}', 'Entradilla')
    P(doc, '{{Lo que nos contó en la reunión: qué funciona, qué no, qué ha probado ya.}}')
    P(doc, 'El objetivo de esta propuesta es montar un sistema que traiga solicitudes de forma constante, que las atienda en minutos y que te diga cada mes cuántas citas y cuántos euros ha generado.')
    h(doc, 'Lo que nos has contado', 3)
    tabla(doc, ['Tema', 'Situación actual'], [
        ['Origen de clientes', '{{≈ 70 % recomendación, 20 % Google Maps…}}'],
        ['Clientes nuevos / mes', '{{00–00}}'],
        ['Respuesta a mensajes', '{{Quién atiende y en qué horario}}'],
        ['Anuncios', '{{Qué se ha hecho y cómo se mide}}'],
        ['Capacidad', '{{Clientes nuevos que puede atender al mes}}'],
    ], [50, 120])
    datos(doc, [('Objetivo 90 días', '+{{00}}', 'clientes/mes', 'objetivo de referencia'),
                ('Respuesta', '< 5', 'min', '24/7, con WhatsApp automatizado'),
                ('Coste por cliente', '≤ {{00}}', '€', 'objetivo de referencia, no garantía')])
    page_break(doc)

    eyebrow(doc, 'Diagnóstico', '02')
    h(doc, 'El problema no es que no te vean. Es que no te [[contactan]].')
    P(doc, 'Revisamos tu presencia digital el {{fecha}}. Resumen por canal; el detalle está en el informe de diagnóstico.', 'Entradilla')
    tabla(doc, ['Canal', 'Qué encontramos', 'Estado'], [
        ['**Google Business Profile**', '{{Hallazgo concreto con cifra}}', '● Mejorable'],
        ['**Web**', '{{Hallazgo concreto con cifra}}', '● Crítico'],
        ['**Meta (Instagram y Facebook)**', '{{Hallazgo concreto con cifra}}', '● Crítico'],
        ['**Google Ads**', '{{Hallazgo concreto con cifra}}', '○ Sin actividad'],
        ['**Reseñas**', '{{Hallazgo concreto con cifra}}', '● Correcto'],
        ['**IA generativa (GEO)**', '{{Hallazgo concreto con cifra}}', '● Mejorable'],
    ], [45, 90, 35])
    guia(doc, 'semáforo: colorea el punto ● con Rojo #E5484D (Crítico), Ámbar #F2A33A (Mejorable) o Verde #1F9D55 (Correcto). El texto siempre acompaña al color.')
    nota(doc, 'Conclusión', '{{Dos frases: qué tiene el negocio a favor y qué falta para captar.}}')
    page_break(doc)

    eyebrow(doc, 'Estrategia', '03')
    h(doc, 'Un sistema de captación, no acciones sueltas.')
    P(doc, 'Tres piezas conectadas: la demanda entra por anuncios y Google, un asistente la atiende al momento y tu equipo solo recibe citas confirmadas.', 'Entradilla')
    t = maqueta(doc, 3)
    for i, (n, tit, txt) in enumerate([('A · Captar', 'Demanda con intención', '{{Google Ads para quien ya busca; Meta Ads para quien aún no busca pero lo necesita.}}'),
                                       ('B · Atender', 'Respuesta en minutos', '{{Asistente de WhatsApp entrenado con tus servicios, precios orientativos y horarios.}}'),
                                       ('C · Medir', 'Citas y euros, no clics', '{{Cada solicitud con su origen; informe mensual por canal.}}')]):
        c = t.rows[0].cells[i]
        c.paragraphs[0].style = doc.styles['Eyebrow']; add_text(c.paragraphs[0], n)
        P(c, tit, 'Heading 3'); P(c, txt)
    P(doc, '')
    P(doc, 'Lo que no haremos: {{acciones que quedan fuera del plan y por qué}}.', 'Nota')
    page_break(doc)

    eyebrow(doc, 'Plan 30-60-90', '04')
    h(doc, 'Primero validamos. Después escalamos lo que funciona.')
    t = maqueta(doc, 3)
    for i, (d, tit, items) in enumerate([('Días 1–30', 'Montar y validar', ['Medición: píxel, etiqueta de Google y conversiones.', 'Landing de {{servicio}}.', 'Asistente de WhatsApp revisado por tu equipo.', 'Campañas de prueba con presupuesto contenido.']),
                                         ('Días 31–60', 'Optimizar', ['Pausar lo que no trae clientes.', 'Ajustar el asistente con conversaciones reales.', 'Recordatorios automáticos.']),
                                         ('Días 61–90', 'Escalar', ['Subir presupuesto si el coste se mantiene.', 'Recaptación de quien no agendó.', 'Revisión trimestral: seguir, ajustar o parar.'])]):
        c = t.rows[0].cells[i]
        c.paragraphs[0].style = doc.styles['Eyebrow']; add_text(c.paragraphs[0], d)
        P(c, tit, 'Heading 3')
        for it in items:
            P(c, it, 'List Bullet')
    P(doc, '')
    tabla(doc, ['Hito', 'Cómo lo medimos', 'Revisión'], [
        ['Sistema en marcha', 'Primer mensaje atendido y registrado con su origen', 'Día 14'],
        ['Validación', 'Coste por cliente frente al objetivo', 'Día 30'],
        ['Decisión de escala', 'Clientes por canal, con informe mensual', 'Día 90'],
    ], [45, 95, 30], right_cols=(2,))
    page_break(doc)

    eyebrow(doc, 'Inversión', '05')
    h(doc, 'Honorarios claros. Los anuncios, aparte.')
    P(doc, 'Separamos lo que cobra Oryzz de lo que se invierte en anuncios. El presupuesto de anuncios lo pagas directamente a Meta y Google: nunca pasa por nosotros.', 'Entradilla')
    h(doc, 'Honorarios Oryzz', 2)
    tabla(doc, ['Concepto', 'Pago único', 'Mensual'], [
        ['**Puesta en marcha** | Medición, landings, asistente de WhatsApp, estructura de campañas', '{{000,00 €}}', '—'],
        ['**Gestión de campañas** | Meta Ads y Google Ads: creatividades y optimización semanal', '—', '{{000,00 €}}'],
        ['**Automatización e IA** | Asistente, recordatorios y sistema de reseñas', '—', '{{000,00 €}}'],
        ['**Informe mensual y reunión de 30 minutos**', '—', 'Incluido'],
        ['Total honorarios', '{{000,00 €}}', '{{000,00 €}}'],
    ], [110, 30, 30], total=True, right_cols=(1, 2))
    P(doc, 'Importes sin IVA (21 %). Facturación mensual por adelantado.', 'Nota')
    h(doc, 'Presupuesto de anuncios', 2)
    P(doc, 'Recomendado para validar: **{{000–000 €}} al mes**, repartido entre {{Google Ads (≈ 60 %) y Meta Ads (≈ 40 %)}}. Se paga directamente a las plataformas. Oryzz no aplica comisión sobre la inversión en anuncios.')
    page_break(doc)

    eyebrow(doc, 'Próximos pasos', '06')
    h(doc, 'Si encaja, empezamos la semana que viene.')
    bullets(doc, ['**Confirmación.** Respondes a este documento o lo firmas abajo.',
                  '**Brief de arranque (45 min).** Servicios, precios orientativos, horarios y tono.',
                  '**Accesos.** Meta, Google Ads, Google Business Profile y web.',
                  '**Día 14.** Sistema en marcha.', '**Día 30.** Reunión de validación con datos reales.'], numbered=True)
    nota(doc, 'Si no encajamos, te lo decimos', 'Si a los 30 días los datos dicen que tu caso no puede captar al coste objetivo, te lo diremos y te recomendaremos parar la inversión en anuncios.')
    eyebrow(doc, 'Condiciones', '07')
    h(doc, 'Sin permanencia', 3)
    P(doc, 'Servicio mensual sin compromiso de duración. Puedes cancelar con 30 días de preaviso por escrito. Las cuentas publicitarias, los píxeles y los datos son siempre tuyos.')
    h(doc, 'Sin resultados garantizados', 3)
    P(doc, 'Ninguna agencia seria puede garantizar clientes: dependen del mercado, del precio y de la atención. Nos comprometemos a trabajar con método, a medir cada euro y a contarte la verdad sobre los datos.')
    h(doc, 'Validez y pagos', 3)
    P(doc, 'Propuesta válida 30 días desde su fecha. Honorarios más IVA, facturados por adelantado y pagaderos por transferencia en 7 días.')
    firma(doc, [('Por Oryzz', 'Juan Salazar · Estrategia & Ads'), ('Por el cliente', 'Nombre, cargo y fecha')])
    P(doc, '¿Dudas? 30 minutos por videollamada: **cal.com/oryzz/30min**', 'Nota').paragraph_format.space_before = Pt(14)
    return save(doc, os.path.join(OUT, '01_Propuesta_Comercial', 'Oryzz_Propuesta-Comercial_PLANTILLA.docx'))


# ============================================================ 02 DIAGNÓSTICO
def diagnostico():
    doc = new_doc()
    s = portada(doc, 'Informe de diagnóstico · Auditoría digital',
                'Dónde se pierden hoy tus [[{{clientes nuevos}}]].',
                'Revisión de Meta, Google, SEO local, reseñas y visibilidad en asistentes de IA, con prioridades ordenadas por impacto.',
                [('Preparado para', '{{Cliente · Ciudad}}'), ('Fecha', '{{dd mmm aaaa}}'), ('Revisión', '{{fechas}}'), ('Responsable', 'Juan Salazar\nEstrategia & Ads')])
    running_header(s, 'Diagnóstico digital · {{Cliente}}', 'oryzz.com · Confidencial')
    eyebrow(doc, 'Resumen', '01')
    h(doc, '{{Titular: el cuello de botella en una frase.}}')
    P(doc, '{{Tres frases: qué tiene a favor el negocio, dónde se pierde la oportunidad y qué haríamos primero.}}', 'Entradilla')
    P(doc, 'Revisamos cada canal con el mismo criterio: **¿acerca este canal un cliente nuevo, y podemos medirlo?** Cada canal recibe una puntuación de 0 a 10 y un estado: ● Crítico · ● Mejorable · ● Correcto.')
    tabla(doc, ['Canal', 'Estado', 'Puntuación', 'Prioridad'], [
        ['**Meta Ads**', '● Crítico', '{{3}}/10', 'Alta'], ['**Google Ads**', '● Mejorable', '{{5}}/10', 'Media'],
        ['**SEO local (Google Maps)**', '● Mejorable', '{{6}}/10', 'Alta'], ['**Reseñas**', '● Correcto', '{{8}}/10', 'Baja'],
        ['**Web y conversión**', '● Crítico', '{{3}}/10', 'Alta'], ['**GEO (ChatGPT, Gemini, Perplexity)**', '● Mejorable', '{{2}}/10', 'Media'],
    ], [70, 35, 35, 30], right_cols=(3,))
    guia(doc, 'semáforo sobrio: solo el punto ● va en color (Rojo #E5484D, Ámbar #F2A33A, Verde #1F9D55); el texto queda en grafito.')
    datos(doc, [('Respuesta media', '{{00}}', 'h', 'a mensajes (muestra de {{00}})'), ('Formulario', '{{0}}', 'campos', 'para pedir cita'), ('Valoración Google', '{{4,8}}', '/ 5', '{{000}} reseñas')])
    page_break(doc)
    eyebrow(doc, 'Hallazgos por canal', '02')
    h(doc, '{{Titular de la sección de hallazgos.}}')
    for n, canal in enumerate(['Meta Ads', 'Google Ads', 'SEO local', 'Reseñas', 'Web y conversión', 'GEO'], start=1):
        p = eyebrow(doc, f'Canal {n:02d}')
        h(doc, f'{canal}  ·  ● {{{{Estado}}}}  ·  {{{{0}}}}/10', 2)
        h(doc, 'Qué encontramos', 3)
        bullets(doc, ['{{Hallazgo con cifra y fuente}}', '{{Hallazgo con cifra y fuente}}', '{{Hallazgo con cifra y fuente}}'])
        nota(doc, 'Recomendación', '{{Acción concreta, con plazo y cómo se medirá.}}')
        if canal in ('Google Ads', 'Reseñas'):
            page_break(doc)
        if canal == 'GEO':
            tabla(doc, ['Pregunta', 'ChatGPT', 'Gemini', 'Perplexity'], [
                ['«{{Mejor clínica de … en …}}»', 'No aparece', 'Mención', 'No aparece'],
                ['«{{Pregunta 2}}»', 'No aparece', 'No aparece', 'Mención']], [80, 30, 30, 30])
    page_break(doc)
    eyebrow(doc, 'Prioridades', '03')
    h(doc, 'Qué haríamos primero, y por qué.')
    P(doc, 'Ordenado por impacto en clientes nuevos y por el esfuerzo que requiere.', 'Entradilla')
    tabla(doc, ['#', 'Acción', 'Impacto', 'Esfuerzo', 'Plazo'], [
        ['01', '**{{Acción}}** | {{Por qué}}', 'Alto', 'Bajo', 'Semana 1'], ['02', '**{{Acción}}** | {{Por qué}}', 'Alto', 'Medio', 'Semana 2'],
        ['03', '**{{Acción}}** | {{Por qué}}', 'Alto', 'Medio', 'Semana 2–3'], ['04', '**{{Acción}}**', 'Medio', 'Bajo', 'Semana 3'],
        ['05', '**{{Acción}}**', 'Medio', 'Medio', 'Mes 2']], [12, 88, 22, 22, 26], right_cols=(4,))
    h(doc, 'Metodología', 3)
    P(doc, 'Revisión manual de cuentas con acceso de lectura (últimos 90 días), PageSpeed Insights, cuadrícula de posiciones en Google Maps y consultas a asistentes de IA desde sesión sin historial. Los datos son una foto del periodo indicado.', 'Nota')
    nota(doc, 'Siguiente paso', '30 minutos para repasar el informe. Sales con un plan, no con un presupuesto cerrado. **cal.com/oryzz/30min**')
    return save(doc, os.path.join(OUT, '02_Informe_Diagnostico', 'Oryzz_Informe-Diagnostico_PLANTILLA.docx'))


# ============================================================ 03 INFORME MENSUAL
def mensual():
    doc = new_doc()
    s = portada(doc, 'Informe mensual de resultados · {{Mes aaaa}}',
                '{{00}} citas. [[{{00,00 €}}]] por cita.',
                'Qué ha pasado este mes en la captación de {{Cliente}}, qué ha funcionado, qué hemos cambiado y qué haremos el mes que viene.',
                [('Cliente', '{{Cliente · Ciudad}}'), ('Periodo', '{{1–31 mmm}}'), ('Entrega', '{{dd mmm aaaa}}'), ('Equipo', 'Juan Salazar · Ads\nDavid Morales · Automatización')])
    running_header(s, 'Informe mensual · {{Mes aaaa}} · {{Cliente}}')
    eyebrow(doc, 'Resumen del mes', '01')
    h(doc, '{{Titular: el resultado del mes en una frase.}}')
    datos(doc, [('Citas', '{{00}}', '', '{{±0 %}} vs mes anterior'), ('€ por cita', '{{0,00}}', '€', '{{±0 %}} vs mes anterior'), ('Solicitudes', '{{000}}', '', '{{00 %}} acaban en cita'), ('Asistencia', '{{00}}', '%', '{{00 de 00}} acudieron')])
    h(doc, 'Citas agendadas por mes', 3)
    P(doc, 'Todas las fuentes medidas · {{periodo}}', 'Nota')
    doc.add_paragraph(style='Cuerpo').add_run().add_picture(res('grafico-citas-mes.png'), width=Mm(120))
    guia(doc, 'sustituye el gráfico (Insertar › Gráfico › Columnas). Barras en Grafito 200 #D5D9E0 y el mes actual en Azul IA #3B72FF; etiqueta solo el primero y el último.')
    P(doc, 'Fuente: {{CRM de Oryzz (citas con origen registrado)}}.', 'Nota')
    h(doc, 'Lectura', 3)
    P(doc, '{{Dos o tres frases que expliquen el porqué de los números, no solo el qué.}}')
    page_break(doc)
    eyebrow(doc, 'Resultados por canal', '02')
    h(doc, '{{Titular: qué canal hace qué.}}')
    tabla(doc, ['Canal', 'Inversión', 'Solicitudes', 'Citas', '€ / cita', 'vs mes ant.'], [
        ['**Meta Ads** | Instagram y Facebook', '{{000,00 €}}', '{{00}}', '{{00}}', '{{00,00 €}}', '{{−0 %}}'],
        ['**Google Ads** | Búsqueda', '{{000,00 €}}', '{{00}}', '{{00}}', '{{00,00 €}}', '{{−0 %}}'],
        ['**Google Maps** | Perfil de empresa', '—', '{{00}}', '{{00}}', '—', '{{+0}}'],
        ['**Otros**', '—', '{{00}}', '{{00}}', '—', '='],
        ['Total', '{{0.000,00 €}}', '{{000}}', '{{00}}', '{{00,00 €}}', '']], [52, 26, 24, 18, 26, 24], total=True, right_cols=(1, 2, 3, 4, 5))
    P(doc, 'Inversión pagada directamente a Meta y Google; no incluye honorarios de Oryzz.', 'Nota')
    t = maqueta(doc, 2, [82.5, 87.5])
    c = t.rows[0].cells[0]; P(c, 'Citas por canal', 'Heading 3'); c.paragraphs[0]._p.getparent().remove(c.paragraphs[0]._p)
    c.add_paragraph(style='Cuerpo').add_run().add_picture(res('grafico-citas-canal.png'), width=Mm(78))
    c = t.rows[0].cells[1]; P(c, 'Coste por cita', 'Heading 3'); c.paragraphs[0]._p.getparent().remove(c.paragraphs[0]._p)
    c.add_paragraph(style='Cuerpo').add_run().add_picture(res('grafico-coste-cita.png'), width=Mm(78))
    P(doc, '')
    guia(doc, 'barras horizontales en un solo tono (Azul IA). Línea de 2 pt en Azul IA y objetivo en discontinua Grafito 500. Nunca dos ejes Y.')
    page_break(doc)
    eyebrow(doc, 'Aprendizajes y cambios', '03')
    h(doc, 'Lo que funcionó, lo que cambiamos y lo que viene.')
    t = maqueta(doc, 2)
    for i, (ey, items) in enumerate([('Qué funcionó', ['{{Aprendizaje 1}}', '{{Aprendizaje 2}}', '{{Aprendizaje 3}}']), ('Qué cambiamos', ['{{Cambio 1}}', '{{Cambio 2}}', '{{Cambio 3}}'])]):
        c = t.rows[0].cells[i]; c.paragraphs[0].style = doc.styles['Eyebrow']; add_text(c.paragraphs[0], ey)
        for k, it in enumerate(items, 1):
            P(c, f'{k:02d}  {it}', 'Heading 3'); P(c, '{{Qué pasó, con cifra.}}')
    P(doc, '')
    eyebrow(doc, 'Siguiente mes', '04')
    tabla(doc, ['Acción', 'Responsable', 'Fecha'], [['{{Acción}}', '{{Oryzz / Cliente}}', '{{dd mmm}}'], ['{{Acción}}', '{{Oryzz}}', '{{dd mmm}}'], ['{{Acción}}', '{{Cliente + Oryzz}}', '{{dd mmm}}']], [100, 45, 25], right_cols=(2,))
    datos(doc, [('Presupuesto anuncios', '{{1.280}}', '€', 'Propuesto para {{mes}}. Pendiente de tu aprobación.')])
    return save(doc, os.path.join(OUT, '03_Informe_Mensual', 'Oryzz_Informe-Mensual_PLANTILLA.docx'))


# ============================================================ 04 CASO DE ESTUDIO
def caso():
    doc = new_doc()
    s = doc.sections[0]
    running_header(s, 'Caso de estudio · {{Cliente}}', 'oryzz.com · Caso con datos de {{ejemplo / cliente real aprobado}}')
    p = eyebrow(doc, 'Caso de estudio · {{Sector}} · {{Ciudad}}')
    p = P(doc, 'EJEMPLO', 'Aviso legal')
    guia(doc, 'mientras las cifras no estén aprobadas por el cliente, mantén la etiqueta «EJEMPLO» y el pie «datos de ejemplo».')
    h(doc, 'De {{11 horas}} a [[{{4 minutos}}]] para {{responder a una clase de prueba}}.')
    P(doc, '{{Una frase: qué negocio, qué problema y qué sistema montamos.}}', 'Entradilla')
    datos(doc, [('{{Métrica 1}}', '{{00 → 00}}', '', '{{en 90 días}}'), ('{{Métrica 2}}', '{{38}}', '€', '{{frente a 95 € al inicio}}'), ('{{Métrica 3}}', '+{{23}}', '/mes', '{{detalle}}')])
    t = maqueta(doc, 2, [50, 120])
    c = t.rows[0].cells[0]
    c.paragraphs[0].style = doc.styles['Eyebrow']; add_text(c.paragraphs[0], 'Cliente'); P(c, '{{Nombre}}\n{{Descripción breve}}')
    P(c, 'Servicios', 'Eyebrow'); P(c, '{{Meta Ads · Google Ads · Asistente de WhatsApp}}')
    P(c, 'Duración', 'Eyebrow'); P(c, '{{mmm–mmm aaaa}}')
    c = t.rows[0].cells[1]
    c.paragraphs[0].style = doc.styles['Heading 2']; add_text(c.paragraphs[0], 'Punto de partida')
    P(c, '{{Situación antes: cifras de partida y qué se había probado.}}')
    P(c, 'Qué hicimos', 'Heading 2')
    for it in ['**{{Pieza 1}}:** {{qué y por qué}}', '**{{Pieza 2}}:** {{qué y por qué}}', '**{{Pieza 3}}:** {{qué y por qué}}']:
        P(c, it, 'List Number')
    page_break(doc)
    eyebrow(doc, 'Resultados', '02')
    h(doc, '{{Titular del resultado.}}')
    tabla(doc, ['Métrica', 'Antes', 'Después', 'Cambio'], [['{{Métrica}}', '{{0}}', '{{0}}', '{{±0 %}}']] * 5, [80, 30, 30, 30], right_cols=(1, 2, 3))
    P(doc, 'Fuente de cada cifra: {{CRM, Meta Ads Manager, Google Ads}} · Periodo: {{fechas exactas}}.', 'Nota')
    cita(doc, '«{{Testimonio real, aprobado por el cliente, en sus palabras.}}»', '{{Nombre · Cargo}} · testimonio aprobado el {{fecha}}')
    t = maqueta(doc, 2)
    for i, (tit, txt) in enumerate([('Lo que marcó la diferencia', '{{Tres claves}}'), ('Lo que no funcionó', '{{Honestidad: qué se probó y se pausó.}}')]):
        c = t.rows[0].cells[i]; c.paragraphs[0].style = doc.styles['Heading 3']; add_text(c.paragraphs[0], tit); P(c, txt)
    P(doc, '')
    nota(doc, '¿Tu negocio se parece a este?', '**30 minutos. Sales con un diagnóstico, no con un presupuesto.**  cal.com/oryzz/30min')
    return save(doc, os.path.join(OUT, '04_Caso_de_Estudio', 'Oryzz_Caso-de-Estudio_PLANTILLA.docx'))


# ============================================================ 05 PRESUPUESTO / FACTURA
def _fiscal(tipo, numero, metas, filas, totales, notas, cliente_lbl, archivo):
    doc = new_doc()
    s = doc.sections[0]; s.top_margin = Mm(20)
    running_header(s, f'{tipo} {numero}', '{{Razón social}} · NIF {{B00000000}} · {{Dirección fiscal}}', folio=False)
    s.header.paragraphs[0].runs[-1].text = ''
    s.header_distance = Mm(8)
    t = maqueta(doc, 2, [100, 70])
    c = t.rows[0].cells[0]; c.paragraphs[0].style = doc.styles['Eyebrow']; add_text(c.paragraphs[0], tipo)
    P(c, numero, 'Heading 1')
    c = t.rows[0].cells[1]
    for k, v in metas:
        p = c.paragraphs[0] if not c.paragraphs[0].text else c.add_paragraph(style='Cuerpo')
        p.style = doc.styles['Cuerpo']; p.paragraph_format.space_after = Pt(2)
        _tab = p.paragraph_format.tab_stops
        from docx.enum.text import WD_TAB_ALIGNMENT
        _tab.add_tab_stop(Mm(68), WD_TAB_ALIGNMENT.RIGHT)
        r = p.add_run(k)
        _set_fonts(r._r.get_or_add_rPr(), MONO); r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string(G500)
        p.add_run('\t'); add_text(p, v)
    P(doc, '')
    t = maqueta(doc, 2)
    for i, (ey, txt) in enumerate([('Emisor', '**{{Razón social}}**\nNIF {{B00000000}}\n{{Dirección fiscal}}\n{{CP}} {{Ciudad}}\n{{facturacion@oryzz.com}}'),
                                   (cliente_lbl, '**{{Razón social del cliente}}**\nNIF {{00000000X}}\n{{Dirección fiscal}}\n{{CP}} {{Ciudad}}')]):
        c = t.rows[0].cells[i]; c.paragraphs[0].style = doc.styles['Eyebrow']; add_text(c.paragraphs[0], ey)
        P(c, txt)
    P(doc, '')
    tabla(doc, ['#', 'Concepto', 'Cant.', 'Precio', 'Importe'], filas, [10, 94, 16, 25, 25], right_cols=(2, 3, 4))
    t = maqueta(doc, 2, [80, 90])
    c = t.rows[0].cells[0]; c.paragraphs[0].style = doc.styles['Eyebrow']; add_text(c.paragraphs[0], notas[0]); P(c, notas[1], 'Nota')
    c = t.rows[0].cells[1]
    tt = c.add_table(rows=len(totales), cols=2)
    tt.style = doc.styles['Tabla Oryzz']; from oryzz_docx import _tbl_look, _widths
    _tbl_look(tt, False, True); _widths(tt, [55, 30])
    for i, (k, v) in enumerate(totales):
        a, b = tt.rows[i].cells
        a.paragraphs[0].style = doc.styles['Texto de tabla']; add_text(a.paragraphs[0], k)
        b.paragraphs[0].style = doc.styles['Texto de tabla']; add_text(b.paragraphs[0], v); b.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    c.paragraphs[0]._p.getparent().remove(c.paragraphs[0]._p)
    c.add_paragraph(style='Nota')
    P(doc, '')
    return doc


def presupuesto():
    doc = _fiscal('Presupuesto', '{{PRE-2026-000}}',
                  [('Fecha', '{{dd/mm/aaaa}}'), ('Válido hasta', '{{dd/mm/aaaa}}'), ('Referencia', '{{Propuesta v1.0}}'), ('Contacto', '{{juan@oryzz.com}}')],
                  [['01', '**Puesta en marcha del sistema** | Pago único', '1', '{{000,00 €}}', '{{000,00 €}}'],
                   ['02', '**Gestión de campañas Meta Ads y Google Ads** | Cuota mensual', '1', '{{000,00 €}}', '{{000,00 €}}'],
                   ['03', '**Automatización e IA** | Cuota mensual', '1', '{{000,00 €}}', '{{000,00 €}}'],
                   ['04', '**Informe mensual y reunión de seguimiento**', '1', '0,00 €', 'Incluido']],
                  [('Base imponible', '{{0.000,00 €}}'), ('IVA (21 %)', '{{000,00 €}}'), ('Total', '{{0.000,00 €}}')],
                  ('No incluido', 'Presupuesto de anuncios ({{000–000 €}}/mes), que se paga directamente a Meta y Google. Oryzz no aplica comisión sobre la inversión en anuncios.'),
                  'Cliente', None)
    t = maqueta(doc, 3)
    for i, (ey, txt) in enumerate([('Condiciones', 'Servicio mensual sin permanencia, con 30 días de preaviso. Sin resultados garantizados.'),
                                   ('Forma de pago', 'Transferencia a 7 días de la factura.\nIBAN {{ES00 0000 0000 0000 0000 0000}}'),
                                   ('Aceptación', '\n\nFirma, nombre y fecha')]):
        c = t.rows[0].cells[i]; c.paragraphs[0].style = doc.styles['Eyebrow']; add_text(c.paragraphs[0], ey); P(c, txt, 'Nota')
    return save(doc, os.path.join(OUT, '05_Presupuesto_y_Factura', 'Oryzz_Presupuesto_PLANTILLA.docx'))


def factura():
    doc = _fiscal('Factura', '{{2026-0000}}',
                  [('Emisión', '{{dd/mm/aaaa}}'), ('Vencimiento', '{{dd/mm/aaaa}}'), ('Periodo', '{{Mes aaaa}}'), ('Presupuesto', '{{PRE-2026-000}}')],
                  [['01', '**Gestión de campañas Meta Ads y Google Ads** | Cuota mensual · {{mes aaaa}}', '1', '{{000,00 €}}', '{{000,00 €}}'],
                   ['02', '**Automatización e IA** | Cuota mensual · {{mes aaaa}}', '1', '{{000,00 €}}', '{{000,00 €}}'],
                   ['03', '**Informe mensual y reunión de seguimiento**', '1', '0,00 €', 'Incluido']],
                  [('Base imponible', '{{000,00 €}}'), ('IVA (21 %)', '{{000,00 €}}'), ('Retención IRPF (solo si aplica)', '{{0,00 €}}'), ('Total a pagar', '{{000,00 €}}')],
                  ('Nota', 'La inversión en anuncios la facturan directamente Meta Platforms Ireland Ltd. y Google Ireland Ltd. y no forma parte de esta factura.'),
                  'Facturar a', None)
    t = maqueta(doc, 2)
    for i, (ey, txt) in enumerate([('Forma de pago', 'Transferencia antes del vencimiento.\nIBAN {{ES00 0000 0000 0000 0000 0000}} · BIC {{XXXXESXX}}\nConcepto: {{número de factura}}'),
                                   ('Protección de datos', '{{Texto informativo RGPD a revisar por asesor legal.}}')]):
        c = t.rows[0].cells[i]; c.paragraphs[0].style = doc.styles['Eyebrow']; add_text(c.paragraphs[0], ey); P(c, txt, 'Nota')
    return save(doc, os.path.join(OUT, '05_Presupuesto_y_Factura', 'Oryzz_Factura_PLANTILLA.docx'))


# ============================================================ 06 MEMBRETE
def _membrete(doc, correo='{{correo@oryzz.com}}'):
    s = doc.sections[0]
    s.top_margin = Mm(52); s.bottom_margin = Mm(34); s.header_distance = Mm(18); s.footer_distance = Mm(12)
    h_ = s.header; p = h_.paragraphs[0]; p.style = doc.styles['Pie Oryzz']
    from oryzz_docx import _tab_right
    _tab_right(p)
    p.add_run().add_picture(res('logo-horizontal-claro.png'), width=Mm(34))
    r = p.add_run('\toryzz.com'); r.font.color.rgb = RGBColor.from_string(G950)
    p2 = h_.add_paragraph(style='Pie Oryzz'); _tab_right(p2); p2.add_run('\t' + correo)
    p3 = h_.add_paragraph(style='Pie Oryzz'); _tab_right(p3); p3.add_run('\t{{+34 600 000 000}}')
    anchor_image(p3.add_run(), res('esquina-membrete.png'), 70, 70, 140, 227)
    for pp in (p, p2, p3):
        pp.paragraph_format.space_after = Pt(1)
    f = s.footer; fp = f.paragraphs[0]; fp.style = doc.styles['Pie Oryzz']
    from oryzz_docx import _pborder
    _pborder(fp._p.get_or_add_pPr(), 'top', 4, G100, 8)
    r = fp.add_run('Oryzz'); r.font.color.rgb = RGBColor.from_string(G950)
    fp.add_run('     Sistemas que captan clientes     {{Razón social}} · NIF {{B00000000}}')


def carta():
    doc = new_doc(); _membrete(doc, '{{juan@oryzz.com}}')
    for l in ['**{{Nombre del destinatario}}**', '{{Empresa}}', '{{Calle y número}}', '{{CP Ciudad}}']:
        P(doc, l).paragraph_format.space_after = Pt(0)
    p = P(doc, '{{dd de mmmm de aaaa}}', 'Pie Oryzz'); p.paragraph_format.space_before = Pt(36); p.paragraph_format.space_after = Pt(20)
    P(doc, '{{Asunto de la carta}}', 'Heading 3').paragraph_format.space_after = Pt(16)
    P(doc, 'Hola, {{nombre}}:')
    for t_ in ['{{Primer párrafo: por qué escribes, en una o dos frases.}}',
               '{{Segundo párrafo: qué va a pasar, con fechas concretas.}}',
               '{{Tercer párrafo: qué necesitas de la otra persona, si algo.}}',
               'Si en algún momento los datos dicen que algo no funciona, te lo diremos antes de gastar de más.']:
        P(doc, t_)
    p = P(doc, 'Un saludo,'); p.paragraph_format.space_before = Pt(18)
    p = P(doc, '**Juan Salazar**'); p.paragraph_format.space_before = Pt(30); p.paragraph_format.space_after = Pt(0)
    P(doc, 'Estrategia & Ads · Oryzz', 'Nota')
    return save(doc, os.path.join(OUT, '06_Carta_y_Membrete', 'Oryzz_Carta_PLANTILLA.docx'))


def blanco():
    doc = new_doc(); _membrete(doc)
    P(doc, '')
    return save(doc, os.path.join(OUT, '06_Carta_y_Membrete', 'Oryzz_Documento-en-blanco_PLANTILLA.docx'))


# ============================================================ 07 BRIEF
def brief():
    doc = new_doc()
    s = portada(doc, 'Brief de cliente · Onboarding', 'Cuéntanos tu [[negocio]].',
                'Rellénalo antes de la reunión de arranque. Son unos 20 minutos. Si alguna pregunta no aplica, déjala en blanco: la vemos juntos.',
                [('Negocio', '{{Nombre del negocio}}'), ('Fecha', '{{dd/mm/aaaa}}'), ('Rellena', '{{Nombre}}'), ('Devolver a', '{{juan@oryzz.com}}')], oscura=False)
    running_header(s, 'Brief de cliente · Onboarding', 'oryzz.com · Confidencial')

    def preg(n, q, ayuda=None, lineas=2, ops=None):
        p = P(doc, f'{n}   **{q}**'); p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.keep_with_next = True
        p.runs[0].font.color.rgb = RGBColor.from_string(AZ600); _set_fonts(p.runs[0]._r.get_or_add_rPr(), MONO); p.runs[0].font.size = Pt(9)
        if ayuda:
            a = P(doc, ayuda, 'Nota'); a.paragraph_format.left_indent = Mm(9); a.paragraph_format.keep_with_next = True
        if ops:
            o = P(doc, '    '.join('☐ ' + x for x in ops)); o.paragraph_format.left_indent = Mm(9)
        for _ in range(lineas):
            P(doc, '', 'Línea de respuesta')

    secciones = [
        ('Tu negocio', '01', [('1.1', 'Nombre comercial y razón social', None, 1, None), ('1.2', 'Dirección del local o locales', None, 2, None),
                              ('1.3', 'Web y redes sociales', 'Enlaces completos.', 2, None),
                              ('1.4', 'Sector', None, 0, ['Clínica / salud', 'Estética', 'Fitness', 'Hostelería', 'Servicios profesionales', 'Otro']),
                              ('1.5', 'Horario de atención', '¿Quién atiende teléfono y WhatsApp, y cuándo?', 1, None),
                              ('1.6', 'Capacidad libre', '¿Cuántos clientes nuevos al mes podrías atender sin contratar a nadie?', 1, None)]),
        ('Clientes y oferta', '02', [('2.1', 'Servicios que quieres vender más', 'Máximo tres, por orden de prioridad, con precio o precio «desde».', 3, None),
                                     ('2.2', 'Valor medio de un cliente nuevo', 'Primera compra y, si lo sabes, lo que gasta en un año.', 1, None),
                                     ('2.3', '¿Quién es tu cliente ideal?', 'Edad, zona, qué le preocupa, por qué te elige.', 2, None),
                                     ('2.4', 'Tres competidores que conozcas', None, 1, None)]),
        ('Captación actual', '03', [('3.1', '¿De dónde llegan hoy tus clientes nuevos?', 'Porcentaje aproximado: recomendación · Google · Instagram/Facebook · otros.', 2, None),
                                    ('3.2', '¿Has hecho publicidad antes?', None, 0, ['Meta Ads', 'Google Ads', 'TikTok Ads', 'Otra agencia', 'Nunca']),
                                    ('3.3', '¿Qué funcionó y qué no?', None, 2, None),
                                    ('3.4', '¿Cuántas solicitudes recibes al mes y cuántas se convierten en cliente?', None, 1, None)]),
        ('Objetivos y presupuesto', '04', [('4.1', '¿Qué resultado haría que esto mereciera la pena en 90 días?', 'En clientes, citas o euros; no en seguidores.', 2, None),
                                           ('4.2', 'Presupuesto mensual para anuncios', 'Se paga aparte, directamente a Meta y Google.', 0, ['< 500 €', '500–1.000 €', '1.000–2.500 €', '> 2.500 €']),
                                           ('4.3', '¿Hay temporadas fuertes o flojas?', None, 1, None)]),
    ]
    for i, (tit, n, qs) in enumerate(secciones):
        eyebrow(doc, tit, n)
        if i == 0:
            h(doc, 'Empecemos por lo básico.')
        for q in qs:
            preg(*q)
        if i in (1, 3):
            page_break(doc)
        else:
            P(doc, '')
    eyebrow(doc, 'Accesos', '05')
    h(doc, 'Las cuentas siempre son tuyas. Nosotros entramos como colaboradores.')
    tabla(doc, ['Plataforma', 'Qué necesitamos', 'Lo tengo', 'Ayuda'], [
        ['**Meta Business Suite**', 'Acceso de socio a la página, Instagram y cuenta publicitaria', '☐', '☐'],
        ['**Google Ads**', 'Acceso de administrador o crear cuenta nueva', '☐', '☐'],
        ['**Google Business Profile**', 'Acceso de administrador al perfil', '☐', '☐'],
        ['**Web**', 'Usuario de editor o contacto de quien la mantiene', '☐', '☐'],
        ['**WhatsApp Business**', 'Número que usarás para el asistente', '☐', '☐'],
        ['**Agenda / CRM**', 'Herramienta de citas que usáis hoy', '☐', '☐']], [45, 85, 20, 20])
    eyebrow(doc, 'Tono y marca', '06')
    preg('6.1', '¿Cómo habláis con los clientes?', None, 0, ['De tú', 'De usted', 'Depende'])
    preg('6.2', 'Cosas que nunca diríais en un anuncio', None, 2)
    preg('6.3', 'Material disponible', None, 0, ['Logo', 'Fotos del local', 'Fotos del equipo', 'Vídeos', 'Reseñas destacadas'])
    preg('6.4', '¿Algo más que debamos saber?', None, 2)
    return save(doc, os.path.join(OUT, '07_Brief_Onboarding', 'Oryzz_Brief-Onboarding_PLANTILLA.docx'))


# ============================================================ 08 ONE-PAGERS
def onepager_servicios():
    doc = new_doc()
    s = doc.sections[0]; s.top_margin = Mm(18); s.bottom_margin = Mm(14)
    p = P(doc, ''); p.paragraph_format.space_after = Pt(0)
    anchor_image(p.add_run(), res('fondo-onepager-oscuro.png'), 210, 297)
    p.add_run().add_picture(res('logo-horizontal-oscuro.png'), width=Mm(32))
    from oryzz_docx import _tab_right
    _tab_right(p); r = p.add_run('\toryzz.com'); _set_fonts(r._r.get_or_add_rPr(), MONO); r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string(G400)
    e = eyebrow(doc, 'Captación de clientes con IA para pymes'); e.paragraph_format.space_before = Pt(64)
    for r in e.runs: r.font.color.rgb = RGBColor.from_string(G400)
    t = P(doc, 'Más clientes.\n[[No más likes.]]', 'Title', color='FFFFFF'); t.paragraph_format.space_after = Pt(10)
    for r in t.runs:
        if r.style.name == 'Acento': r.font.color.rgb = RGBColor.from_string(AZ400)
    P(doc, 'Montamos un sistema de captación que gira solo: anuncios que traen demanda, IA que responde al momento y un informe que se mide en citas y en euros.', 'Subtitle', color=G200).paragraph_format.right_indent = Mm(50)
    e = eyebrow(doc, 'Qué hacemos'); e.paragraph_format.space_before = Pt(14)
    for r in e.runs: r.font.color.rgb = RGBColor.from_string(G400)
    tb = doc.add_table(rows=4, cols=3); tb.style = doc.styles['Tabla Oryzz']
    from oryzz_docx import _tbl_look, _widths
    _tbl_look(tb, False, False); _widths(tb, [20, 60, 90])
    tblpr = tb._tbl.tblPr
    tblpr.append(parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:color="{G700}"/><w:bottom w:val="single" w:sz="4" w:color="{G700}"/><w:insideH w:val="single" w:sz="4" w:color="{G700}"/></w:tblBorders>'))
    for i, (tit, txt) in enumerate([('Meta, Google y TikTok Ads', 'Campañas optimizadas a mensajes, llamadas y formularios. Creatividades con tu negocio real.'),
                                    ('Automatización con IA', 'Asistente de WhatsApp e Instagram que responde en minutos, filtra y agenda.'),
                                    ('SEO local y reseñas', 'Google Business Profile completo y un sistema que pide reseñas en el momento justo.'),
                                    ('GEO', 'Posicionamiento en ChatGPT, Gemini y Perplexity para cuando tu cliente pregunta a una IA.')]):
        a, b, c = tb.rows[i].cells
        for cc in (a, b, c): cc.paragraphs[0].style = doc.styles['Texto de tabla']
        add_text(a.paragraphs[0], f'{i + 1:02d}', color=G400, font=MONO, size=9)
        add_text(b.paragraphs[0], tit, color='FFFFFF', font=DISPLAY, bold=True, size=11.5)
        add_text(c.paragraphs[0], txt, color=G200)
    P(doc, '')
    e = eyebrow(doc, 'Cómo trabajamos')
    for r in e.runs: r.font.color.rgb = RGBColor.from_string(G400)
    datos(doc, [('Diagnóstico', '30', 'min', 'Sales con un diagnóstico, no con un presupuesto.'), ('En marcha', '14', 'días', 'Medición, anuncios y asistente activos y revisados por ti.'), ('Permanencia', '0', 'meses', 'Sin permanencia: 30 días de preaviso. Las cuentas y los datos son tuyos.')], dark=True)
    p = P(doc, 'Un sistema de captación, no acciones sueltas.', 'Heading 2', color='FFFFFF'); p.paragraph_format.space_before = Pt(10)
    P(doc, '**Agenda 30 min · cal.com/oryzz/30min**   ·   @oryzzai   ·   linkedin.com/company/oryzz', 'Cuerpo', color=G200)
    return save(doc, os.path.join(OUT, '08_One_Pagers', 'Oryzz_One-Pager-Servicios_PLANTILLA.docx'))


def onepager_tap():
    doc = new_doc()
    s = doc.sections[0]; s.top_margin = Mm(18); s.bottom_margin = Mm(14)
    p = P(doc, ''); p.paragraph_format.space_after = Pt(0)
    anchor_image(p.add_run(), res('fondo-onepager-tap.png'), 210, 297)
    anchor_image(p.add_run(), res('tap-stand.png'), 80, 110, 116, 42, behind=False)
    p.add_run().add_picture(res('logo-tap-claro.png'), width=Mm(44))
    from oryzz_docx import _tab_right
    _tab_right(p); r = p.add_run('\toryzz.com/tap'); _set_fonts(r._r.get_or_add_rPr(), MONO); r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string(G500)
    e = eyebrow(doc, 'Placas y stands NFC + QR'); e.paragraph_format.space_before = Pt(60)
    t = P(doc, 'Tu negocio.\n[[A un toque.]]', 'Title'); t.paragraph_format.right_indent = Mm(80)
    P(doc, 'Tus clientes acercan el teléfono y ocurre: dejan una reseña en Google, te escriben por WhatsApp o te siguen. Sin apps, sin buscarte.', 'Subtitle').paragraph_format.right_indent = Mm(82)
    P(doc, 'iPhone y Android  ·  Sin pilas  ·  QR de respaldo', 'Pie Oryzz').paragraph_format.space_after = Pt(70)
    eyebrow(doc, 'Cómo funciona')
    tt = maqueta(doc, 3)
    for i, (tit, txt) in enumerate([('Acerca el teléfono', 'El chip NFC abre tu enlace al instante. Si el móvil no tiene NFC, el QR hace lo mismo.'),
                                    ('Se abre tu página', 'Directo a dejar la reseña, a tu WhatsApp o a tu perfil.'),
                                    ('Lo cambias cuando quieras', 'El destino de la placa se edita sin reimprimir nada.')]):
        c = tt.rows[0].cells[i]
        c.paragraphs[0].style = doc.styles['Pie Oryzz']; add_text(c.paragraphs[0], f'{i + 1:02d}', color=AZ600)
        _pborder(c.paragraphs[0]._p.get_or_add_pPr(), 'top', 8, G950, 6)
        P(c, tit, 'Heading 3'); P(c, txt, color=G600)
    P(doc, '')
    eyebrow(doc, 'Gama')
    tt = maqueta(doc, 2)
    for i, (tit, txt) in enumerate([('Reseñas Google', 'Placa o stand que lleva directo a la ventana de reseña de tu ficha.'), ('Oryzz Pro', 'Tu placa conectada a una página con todos tus enlaces: reseñas, WhatsApp, redes y carta.')]):
        c = tt.rows[0].cells[i]
        c.paragraphs[0].style = doc.styles['Heading 3']; add_text(c.paragraphs[0], tit)
        P(c, txt, color=G600); P(c, 'Desde {{$ 000.000 COP}}', 'Pie Oryzz')
    P(doc, '')
    p = P(doc, 'Conecta lo que eres. Acerca lo que sigue.', 'Heading 2'); p.paragraph_format.space_before = Pt(10)
    P(doc, '**Pídela en shop.oryzz.com**   ·   pedidos@oryzz.com   ·   @oryzztap   ·   TikTok @oryzz.tap')
    return save(doc, os.path.join(OUT, '08_One_Pagers', 'Oryzz-Tap_One-Pager_PLANTILLA.docx'))


# ============================================================ 09 CONTRATO
CLAUSULAS = [
    ('Objeto', 'Oryzz prestará al Cliente los servicios de captación de clientes descritos en la propuesta {{referencia}}, que se adjunta como Anexo I y forma parte de este contrato.'),
    ('Servicios incluidos', 'Gestión de campañas en {{Meta Ads / Google Ads / TikTok Ads}}, configuración y mantenimiento de automatizaciones, optimización del perfil de empresa en Google e informe mensual de resultados. Cualquier servicio no descrito en el Anexo I se presupuestará aparte.'),
    ('Duración y sin permanencia', 'El contrato entra en vigor el {{fecha de inicio}} y tiene duración mensual prorrogable de forma automática. Cualquiera de las partes puede resolverlo sin penalización con un preaviso escrito de 30 días naturales.'),
    ('Honorarios y forma de pago', 'El Cliente abonará a Oryzz una cuota de puesta en marcha de {{000,00 €}} y una cuota mensual de {{000,00 €}}, más el IVA aplicable, facturadas por adelantado y pagaderas por transferencia en {{7}} días.'),
    ('Presupuesto publicitario', 'La inversión en anuncios no forma parte de los honorarios. El Cliente la abona directamente a las plataformas publicitarias. Oryzz no percibe comisión sobre dicha inversión y no modificará el presupuesto acordado sin autorización escrita del Cliente.'),
    ('Sin garantía de resultados', 'Oryzz asume una obligación de medios y no de resultados. Los resultados dependen de factores ajenos a Oryzz. Las cifras objetivo de la propuesta son referencias de trabajo y no constituyen garantía.'),
    ('Obligaciones del Cliente', 'Facilitar los accesos necesarios, aprobar anuncios y respuestas automatizadas en {{3}} días hábiles, atender las solicitudes generadas y garantizar la veracidad de la información facilitada.'),
    ('Titularidad de cuentas y datos', 'Las cuentas publicitarias, perfiles, píxeles, bases de datos y contenidos creados para el Cliente son de su titularidad. Al finalizar, Oryzz retirará sus accesos y entregará la documentación de configuración en {{15}} días.'),
    ('Protección de datos', 'Oryzz actuará como encargado del tratamiento conforme al Reglamento (UE) 2016/679 y a la Ley Orgánica 3/2018. Las partes firmarán el acuerdo de encargo del tratamiento del Anexo II.'),
    ('Confidencialidad', 'Ambas partes mantendrán la confidencialidad de la información a la que accedan durante la vigencia del contrato y {{2}} años después.'),
    ('Propiedad intelectual', 'Los materiales creativos elaborados para el Cliente se ceden a este una vez abonados. Oryzz conserva la titularidad de sus metodologías, plantillas y herramientas internas.'),
    ('Resolución anticipada', 'Cualquiera de las partes podrá resolver el contrato de forma inmediata en caso de incumplimiento grave no subsanado en {{15}} días desde su notificación.'),
    ('Ley aplicable y jurisdicción', 'El contrato se rige por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales de {{ciudad}}.'),
]


def contrato():
    doc = new_doc()
    s = portada(doc, 'Contrato de prestación de servicios', 'Servicios de captación de clientes y automatización.',
                'Maqueta de contrato. La estructura y la tipografía son definitivas; el texto jurídico es orientativo y debe validarlo un asesor legal antes de usarse.',
                [('Cliente', '{{Razón social del cliente}}'), ('Fecha', '{{dd/mm/aaaa}}'), ('Referencia', '{{CT-2026-000}}'), ('Prestador', '{{Razón social}} (Oryzz)')],
                oscura=False, etiqueta='Texto a revisar por asesor legal')
    running_header(s, 'Contrato de servicios · Maqueta', 'oryzz.com · Borrador · Texto a revisar por asesor legal')
    P(doc, 'BORRADOR · Todas las cláusulas están pendientes de revisión jurídica. No firmar sin validación.', 'Aviso legal')
    eyebrow(doc, 'Reunidos')
    P(doc, 'De una parte, **{{Razón social}}**, con NIF {{B00000000}} y domicilio en {{Dirección fiscal}}, representada por {{Nombre y cargo}} (en adelante, «Oryzz»).')
    P(doc, 'De otra parte, **{{Razón social del cliente}}**, con NIF {{00000000X}} y domicilio en {{Dirección fiscal}}, representada por {{Nombre y cargo}} (en adelante, «el Cliente»).')
    P(doc, 'Ambas partes se reconocen capacidad para contratar y acuerdan las siguientes cláusulas.')
    for i, (tit, txt) in enumerate(CLAUSULAS, 1):
        p = h(doc, f'{i:02d}   {tit}', 2)
        P(doc, 'Texto a revisar por asesor legal', 'Aviso legal')
        P(doc, txt)
    h(doc, 'Anexos', 3)
    P(doc, 'Anexo I · Propuesta comercial {{referencia}}\nAnexo II · Acuerdo de encargo del tratamiento de datos')
    P(doc, 'Y en prueba de conformidad, firman el presente contrato por duplicado en {{ciudad}}, a {{fecha}}.').paragraph_format.space_before = Pt(12)
    firma(doc, [('Por Oryzz', '{{Nombre y cargo}}'), ('Por el Cliente', '{{Nombre y cargo}}')])
    return save(doc, os.path.join(OUT, '09_Contrato_de_Servicios', 'Oryzz_Contrato-Servicios_PLANTILLA.docx'))


TODOS = [('01', propuesta), ('02', diagnostico), ('03', mensual), ('04', caso), ('05', presupuesto), ('05', factura),
         ('06', carta), ('06', blanco), ('07', brief), ('08', onepager_servicios), ('08', onepager_tap), ('09', contrato)]

if __name__ == '__main__':
    f = sys.argv[1:]
    for k, fn in TODOS:
        if not f or k in f:
            print('ok', fn())
