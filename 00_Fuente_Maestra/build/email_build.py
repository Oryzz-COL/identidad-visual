# -*- coding: utf-8 -*-
"""
Oryzz · generador del sistema de email (08_Email) v2.0
======================================================

    python email_build.py            # todo: assets, plantillas, .txt, firmas, previews, PDF, _listo_para_enviar
    python email_build.py plantillas # solo HTML + TXT + firmas (rápido)
    python email_build.py previews   # solo previsualizaciones + PDF

AVISO: sobrescribe los HTML de 08_Email. Si has editado a mano alguna plantilla,
no vuelvas a ejecutar este script entero; usa `email_publicar.py` para generar
las copias con URL absolutas.
"""
import os, re, sys, html as _html, pathlib, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import email_lib as E
from email_lib import hl, hl_oscuro, enlace, b
import render

ROOT = pathlib.Path(__file__).resolve().parents[2]            # Identidad_Visual
OUT = ROOT / '08_Email'
ASSETS = OUT / 'assets'
LOGOS = ROOT / '02_Logos'
ICONOS = ROOT / '05_Elementos_Graficos' / '01_Iconos' / 'SVG'
FONTS = ROOT / '00_Fuente_Maestra' / 'fonts' / 'static'
import tempfile
SCRATCH = pathlib.Path(os.environ.get('ORYZZ_SCRATCH', os.path.join(tempfile.gettempdir(), 'oryzz_email_build')))

# URL pública donde se suben los archivos de 08_Email/assets/ (ver LEEME).
BASE_URL = 'https://oryzz.com/brand/email'

CAL = 'https://cal.com/oryzz/30min'


# =====================================================================
# 1. ASSETS (PNG a 2×)
# =====================================================================
def _svg_tmp(name, svg):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    p = SCRATCH / name
    p.write_text(svg, encoding='utf8')
    return str(p)


def _icono_svg(nombre, trazo, acento):
    """Lee un icono oficial (05_Elementos_Graficos) o el propio de email y lo colorea."""
    propio = {
        # Código de 8 dígitos — mismo estilo que la familia oficial (24 px, trazo 1,75, un acento).
        'codigo': ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                   'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
                   '<rect x="2.75" y="6.5" width="18.5" height="11" rx="3"/>'
                   '<path d="M6.5 14.5H8.5M10.25 14.5H12.25M14 14.5H16"/>'
                   '<circle cx="18.25" cy="10.25" r="1.25" fill="currentColor" stroke="none" class="oz-acento" '
                   'style="color:var(--oz-acento,currentColor)"/></svg>'),
    }
    src = ICONOS / ('oz-icono_%s.svg' % nombre)
    svg = src.read_text(encoding='utf8') if src.exists() else propio[nombre]
    svg = re.sub(r'<title>.*?</title>', '', svg)
    svg = svg.replace('var(--oz-acento,currentColor)', acento)
    root = re.match(r'<svg[^>]*>', svg).group(0)
    nuevo = re.sub(r'\s(width|height|style|role|aria-label)="[^"]*"', '', root)
    nuevo = nuevo.replace('<svg ', '<svg x="12" y="12" width="24" height="24" style="color:%s" ' % trazo, 1)
    return svg.replace(root, nuevo, 1)


def build_assets():
    ASSETS.mkdir(parents=True, exist_ok=True)
    H = LOGOS / '01_Horizontal' / 'SVG'
    T = LOGOS / '07_Submarca_Tap' / 'SVG'
    # Logos (versiones sólidas, fondo horneado = color de la banda donde van)
    render.svg_to_png(str(H / 'oryzz-logo-horizontal_solido-sobre-oscuro.svg'), str(ASSETS / 'oryzz-logo_sobre-oscuro.png'),
                      width=224, background='#0B0D12')
    render.svg_to_png(str(H / 'oryzz-logo-horizontal_solido-sobre-claro.svg'), str(ASSETS / 'oryzz-logo_sobre-claro.png'),
                      width=224, background='#FFFFFF')
    render.svg_to_png(str(T / 'oryzz-tap-horizontal_solido-sobre-claro.svg'), str(ASSETS / 'oryzz-tap-logo_sobre-claro.png'),
                      width=300, background='#FFFFFF')
    render.svg_to_png(str(T / 'oryzz-tap-horizontal_solido-sobre-oscuro.svg'), str(ASSETS / 'oryzz-tap-logo_sobre-oscuro.png'),
                      width=300, background='#0B0D12')
    # Avatares para firma (esquinas transparentes): Oryzz = Grafito 950 + órbita sólida; Tap = sobre azul oficial.
    iso = (LOGOS / '04_Isotipo' / 'SVG' / 'oryzz-isotipo_solido-sobre-oscuro.svg').read_text(encoding='utf8')
    g = re.search(r'<g transform="[^"]*">(.*?)</g>', iso, re.S).group(1)
    av = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22.5" fill="#0B0D12"/>'
          '<g transform="translate(20.00 21.00) scale(0.6000)">%s</g></svg>' % g)
    render.svg_to_png(_svg_tmp('av.svg', av), str(ASSETS / 'firma-avatar-oryzz.png'), width=112)
    render.svg_to_png(str(LOGOS / '05_Avatar_Perfil' / 'SVG' / 'oryzz-avatar-cuadrado_sobre-azul.svg'),
                      str(ASSETS / 'firma-avatar-tap.png'), width=112)
    # Órbita decorativa del hero (sistema gráfico §5.1): arcos abiertos Grafito 700 + un nodo lima.
    orb = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 168 168">'
           '<g fill="none" stroke="#232836" stroke-width="1.5" stroke-linecap="round">'
           '<path d="M168 36 A132 132 0 0 0 43.6 124.5"/>'
           '<path d="M168 80 A88 88 0 0 0 84.4 140.6"/>'
           '<path d="M168 124 A44 44 0 0 0 125.3 157.4"/>'
           '<path d="M38.7 146.3 A132 132 0 0 0 36.6 168"/>'
           '</g>'
           '<circle cx="41.6" cy="134.2" r="5" fill="#BFF24A"/></svg>')
    render.svg_to_png(_svg_tmp('orb.svg', orb), str(ASSETS / 'orbita-hero.png'), width=336, background='#0B0D12')
    # Iconos de pasos (Tap): losa 48 px con esquinas horneadas al color de la tarjeta.
    for nombre in ['nfc', 'codigo', 'usuario', 'check-orbita']:
        for modo, losa, fondo, trazo, acento in [('claro', '#F6F7F9', '#FFFFFF', '#0B0D12', '#7FB02E'),
                                                 ('oscuro', '#171B25', '#12151D', '#D5D9E0', '#BFF24A')]:
            ic = _icono_svg(nombre, trazo, acento)
            tile = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="%s"/>%s</svg>'
                    % (losa, ic))
            render.svg_to_png(_svg_tmp('ic.svg', tile), str(ASSETS / ('icono-%s_%s.png' % (nombre, modo))), width=96, background=fondo)
    # Diagrama «canales → sistema → citas» (rutas y nodos §5.2), HTML con fuentes locales → PNG 2×.
    diagrama_html = DIAGRAMA.replace('%FONTS%', FONTS.as_uri())
    p = _svg_tmp('diagrama.html', diagrama_html)
    shot(p, str(ASSETS / 'diagrama-sistema.png'), 518, 196)
    print('assets ok')


DIAGRAMA = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:SG;src:url('%FONTS%/SpaceGrotesk-SemiBold.ttf')}
@font-face{font-family:MR;src:url('%FONTS%/Manrope-Medium.ttf')}
@font-face{font-family:JB;src:url('%FONTS%/JetBrainsMono-Medium.ttf')}
html,body{margin:0;width:518px;height:196px;background:#0B0D12;overflow:hidden}
.w{position:relative;width:518px;height:196px}
.c{position:absolute;top:44px;width:132px;height:104px;box-sizing:border-box;background:#12151D;border:1px solid #232836;border-radius:14px;padding:16px 16px 0}
.c.s{border-color:#3A4152;background:#171B25}
.e{font:500 11px/14px JB;letter-spacing:.14em;color:#8A90A0;text-transform:uppercase;margin:0 0 10px}
.t{font:600 22px/24px SG;letter-spacing:-.02em;color:#fff;margin:0 0 6px}
.d{font:500 12.5px/16px MR;color:#D5D9E0;margin:0}
.l{position:absolute;top:95px;height:0;border-top:1.5px solid #3A4152}
.n{position:absolute;width:8px;height:8px;border-radius:50%;background:#5C8BFF;top:91px}
.lima{background:#BFF24A;width:12px;height:12px;top:89px}
.cap{position:absolute;left:24px;top:14px;font:500 11px/14px JB;letter-spacing:.14em;color:#5A6172}
</style></head><body><div class="w">
<div class="cap">TU SISTEMA DE CAPTACIÓN</div>
<div class="c" style="left:24px"><p class="e">01 · Canales</p><p class="t">Anuncios</p><p class="d">Meta · Google · TikTok</p></div>
<div class="l" style="left:156px;width:37px"></div><div class="n" style="left:170px"></div>
<div class="c s" style="left:193px"><p class="e">02 · Sistema</p><p class="t">Respuesta</p><p class="d">En minutos, con seguimiento</p></div>
<div class="l" style="left:325px;width:37px"></div><div class="n" style="left:339px"></div>
<div class="c" style="left:362px"><p class="e">03 · Cliente</p><p class="t">Citas</p><p class="d">En tu agenda y medidas en €</p></div>
<div class="n lima" style="left:484px;top:38px"></div>
</div></body></html>"""


def shot(html_path, png_path, w, h, scale=2):
    render._run(['--force-device-scale-factor=%d' % scale, '--window-size=%d,%d' % (max(w, 500), h),
                 '--screenshot=%s' % os.path.abspath(png_path), pathlib.Path(html_path).resolve().as_uri()])
    from PIL import Image
    im = Image.open(png_path)
    im.crop((0, 0, w * scale, h * scale)).save(png_path, optimize=True)


# =====================================================================
# 2. PLANTILLAS
# =====================================================================
def comentario(nombre, asunto, preheader, alternativas, notas, cuerpo=''):
    alt = '\n'.join('    · ' + a for a in alternativas)
    return ('  ORYZZ · PLANTILLA DE EMAIL · %s\n'
            '  ─────────────────────────────────────────────────────────────\n'
            '  Asunto:      %s\n'
            '  Preheader:   %s\n'
            '  Alternativas de asunto:\n%s\n'
            '  Marcadores:  %%MARCADORES%%\n'
            '  Notas:\n%s\n'
            '  Imágenes:    rutas relativas «assets/…». Para enviar, usa la copia de _listo_para_enviar/\n'
            '               (URL absolutas a %s) o reemplaza «assets/» por esa URL.\n'
            '  Sistema:     00_Fuente_Maestra/build/email_lib.py · guía en 08_Email/Guia_de_redaccion_email.md'
            % (nombre, asunto, preheader or '(sin preheader: correo 1 a 1)', alt,
               '\n'.join('    · ' + n for n in notas), BASE_URL + '/'))


P = {}   # nombre de archivo -> dict(asunto, preheader, html, txt, tipo, descripcion)


def registrar(archivo, asunto, preheader, bloques, alternativas, notas, tipo, descripcion, uno_a_uno=None):
    com = comentario(archivo, asunto, preheader, alternativas, notas)
    if uno_a_uno:
        html, txt = E.documento_1a1(asunto, uno_a_uno['parrafos'], uno_a_uno['firma'], com)
    else:
        html, txt = E.documento(asunto, preheader, bloques, com)
    mk = E.marcadores(html.split('-->', 1)[1] + asunto)   # sin el comentario de cabecera
    html = html.replace('%MARCADORES%', ', '.join('{{%s}}' % m for m in mk) or '—')
    cab = 'ASUNTO: %s\n' % asunto
    if preheader:
        cab += 'PREHEADER: %s\n' % preheader
    cab += '=' * 64 + '\n\n'
    P[archivo] = dict(asunto=asunto, preheader=preheader, html=html, txt=cab + txt, tipo=tipo, descripcion=descripcion,
                      marcadores=mk)


def plantillas():
    P.clear()
    # ------------------------------------------------------------ 01 NEWSLETTER
    registrar(
        '01_newsletter', 'Lo que aprendimos en septiembre captando clientes',
        'Contestar en minutos, aparecer en ChatGPT y pedir la reseña en el momento justo.',
        [
            E.cabecera('Notas · Sep 2026'),
            E.hero_oscuro('Notas de captación',
                          'Tres ideas que este mes movieron %s.' % hl_oscuro('citas'),
                          'Sin teoría: lo que vimos funcionar (y fallar) en clínicas, gimnasios y centros de estética.',
                          alt=''),
            E.espacio(36),
            E.parrafo('Hola, {{nombre}}. Esta es la carta mensual de Oryzz: tres ideas, cinco minutos de lectura y ninguna promesa milagro.',
                      margen_inf=24),
            E.seccion('01', 'Contestar en 5 minutos vale más que otro anuncio', [
                'Quien escribe a las 21:40 y recibe respuesta a la mañana siguiente ya ha pedido precio en otros dos sitios. '
                'Lo vemos cada mes: casi nunca faltan contactos; lo que pasa es que se enfrían.',
                '%s mira cuánto tardaste en responder los últimos diez mensajes de WhatsApp o del formulario. '
                'Si pasa de una hora, un asistente puede hacer la primera pregunta y proponer hora por ti.' % b('Para esta semana:'),
            ]),
            E.seccion('02', 'ChatGPT ya recomienda negocios de tu zona. ¿Te nombra a ti?', [
                'Cada vez más gente pregunta a ChatGPT, Gemini o Perplexity «qué fisio me recomiendas en Valencia» en lugar de buscar en Google. '
                'Las respuestas salen de reseñas, fichas y webs que esos modelos pueden leer.',
                '%s hazle esa pregunta con tu servicio y tu ciudad. Si no sales, empieza por lo básico: ficha de Google completa, '
                'servicios con precio orientativo en tu web y reseñas que nombren el tratamiento concreto.' % b('Prueba rápida:'),
            ]),
            E.seccion('03', 'La reseña se pide en el mostrador, no una semana después', [
                'El mejor momento para pedir una reseña es justo cuando el cliente dice «qué bien ha ido». '
                'Un correo a los siete días llega tarde y compite con todo lo demás.',
                'En recepción funciona una placa NFC: el cliente acerca el móvil y se abre directamente la pantalla para valorar. '
                'Es lo que hace %s.' % enlace('Oryzz Tap', 'https://oryzz.com/tap'),
            ]),
            E.separador('12px 40px 28px'),
            E.titular('¿Miramos tu caso?', nivel=2, margen_inf=10),
            E.parrafo('En 30 minutos revisamos cómo te llegan hoy los clientes y dónde se pierden. '
                      'Sales con un diagnóstico, no con un presupuesto.'),
            E.boton('Agendar 30 minutos', CAL),
            E.despedida('Hasta el mes que viene,', 'Juan y David', 'Socios de Oryzz'),
            E.fuera(E.pie(motivo='Recibes estas notas porque te suscribiste en oryzz.com.', baja=True, direccion=True)),
        ],
        ['Tres cosas que movieron citas en septiembre', 'Tu próximo cliente ya está preguntando a ChatGPT',
         'Por qué el lead de las 21:40 no te llama mañana'],
        ['Envío mensual desde Brevo / Mailchimp. Sustituye {{baja_url}} por la etiqueta de baja de tu plataforma (ver LEEME).',
         '2–3 bloques de «sección numerada». Un único botón al final.',
         'La órbita del hero se oculta en móvil (clase o-hide-m).'],
        'Newsletter', 'Novedades y aprendizajes del mes: 3 bloques numerados + CTA de agenda.')

    # ------------------------------------------------------------ 02 PROSPECCIÓN
    registrar(
        '02_prospeccion_primer_contacto', 'Pregunta sobre las citas de {{negocio}}', '', None,
        ['{{nombre}}, una cosa que vi en la ficha de {{negocio}}', 'Citas de {{servicio}} en {{ciudad}}',
         '¿Quién responde los WhatsApp de {{negocio}}?'],
        ['CORREO 1 A 1: se envía desde Gmail de Juan (no desde una herramienta de newsletter), sin imágenes, sin botón ni píxel.',
         'Personaliza SIEMPRE {{observacion_concreta}}: algo real que viste en su ficha, web o anuncios. Ejemplo: «la ficha no tiene botón de reserva y varias reseñas recientes siguen sin respuesta».',
         'Máximo 120 palabras. Una sola pregunta al final. Nada de enlaces en el primer correo.',
         'Envía en pequeñas tandas (≤ 30/día por buzón) y solo a correos profesionales públicos. Revisa la LSSI en la guía.'],
        '1 a 1', 'Primer contacto en frío, estilo personal y casi texto plano (máxima entregabilidad).',
        uno_a_uno=dict(parrafos=[
            'Hola, {{nombre}}:',
            'Buscando «{{servicio}} en {{ciudad}}» he visto que {{negocio}} sale en el mapa de Google, pero {{observacion_concreta}}. '
            'Son detalles pequeños que suelen costar citas que ya estaban a punto de llegar.',
            'Soy Juan, de Oryzz. Montamos sistemas de captación para clínicas y negocios locales: anuncios en Meta y Google, '
            'respuesta por WhatsApp en minutos y la ficha de Google bien trabajada. Lo medimos en citas, no en likes.',
            '¿Te mando en tres líneas lo que cambiaría primero en tu caso? Sin llamada, por aquí mismo.',
            'Si no es buen momento, respóndeme «no» y no vuelvo a escribirte.',
            'Un saludo,',
        ], firma=['Juan Salazar', 'Oryzz · Estrategia &amp; Ads', '<a href="https://oryzz.com">oryzz.com</a>']))

    # ------------------------------------------------------------ 03 SEGUIMIENTOS
    registrar(
        '03_seguimiento_1', 'Re: Pregunta sobre las citas de {{negocio}}', '', None,
        ['(Responde en el mismo hilo: el asunto se mantiene con «Re:»)'],
        ['Seguimiento 1: 3 días hábiles después del primer correo, RESPONDIENDO en el mismo hilo.',
         'Más corto que el primero (≤ 60 palabras). Sin enlaces.'],
        '1 a 1', 'Seguimiento 1 (a los 3 días hábiles), en el mismo hilo.',
        uno_a_uno=dict(parrafos=[
            'Hola, {{nombre}}:',
            'Te escribo de nuevo por si mi correo del {{dia_primer_correo}} se quedó abajo en la bandeja.',
            'En una frase: creo que {{negocio}} está perdiendo citas entre el anuncio (o la búsqueda en Google) y la primera respuesta, '
            'y eso se arregla sin subir lo que inviertes.',
            '¿Te lo cuento en tres líneas?',
            'Gracias,',
        ], firma=['Juan', 'Oryzz · <a href="https://oryzz.com">oryzz.com</a>']))

    registrar(
        '03_seguimiento_2', 'Re: Pregunta sobre las citas de {{negocio}}', '', None,
        ['(Responde en el mismo hilo)'],
        ['Seguimiento 2 y último: 7 días después del seguimiento 1. Aporta algo útil aunque no conteste.',
         'Único enlace permitido: la agenda. Después de este correo, no se vuelve a escribir salvo que responda.'],
        '1 a 1', 'Seguimiento 2 (cierre a los 7 días) con una idea útil y la agenda.',
        uno_a_uno=dict(parrafos=[
            'Hola, {{nombre}}:',
            'Último correo sobre esto, prometido.',
            'Te dejo una idea que puedes aplicar hoy sin nosotros: responde a las reseñas de los últimos tres meses nombrando el servicio '
            '(«gracias por confiar en nosotros para tu {{servicio}}»). Google y los asistentes de IA leen esas respuestas, '
            'y quien te busca ve que hay alguien detrás.',
            'Si más adelante quieres que revisemos tu captación, tienes 30 minutos en mi agenda: '
            '<a href="https://cal.com/oryzz/30min">cal.com/oryzz/30min</a>. Sales con un diagnóstico, no con un presupuesto.',
            'Un saludo,',
        ], firma=['Juan Salazar', 'Oryzz · Estrategia &amp; Ads', '<a href="https://oryzz.com">oryzz.com</a>']))

    # ------------------------------------------------------------ 04 CONFIRMACIÓN VALORACIÓN
    registrar(
        '04_confirmacion_valoracion', 'Confirmada tu valoración: {{fecha}}, {{hora}}',
        '30 minutos por videollamada. Te contamos qué tener a mano para aprovecharlos.',
        [
            E.cabecera('Valoración · 30 min'),
            E.espacio(40),
            E.eyebrow('Cita confirmada'),
            E.espacio(14),
            E.titular('Nos vemos el %s.' % hl('{{fecha}}')),
            E.parrafo('Hola, {{nombre}}. Gracias por reservar. En 30 minutos revisamos cómo le llegan hoy los clientes a {{negocio}}, '
                      'dónde se pierden y qué haríamos primero. Sales con un diagnóstico, no con un presupuesto.', lead=True, margen_inf=24),
            E.detalles([('Cuándo', '{{fecha}} · {{hora}} (hora peninsular)'), ('Duración', '30 minutos'),
                        ('Dónde', 'Videollamada, con el enlace de abajo'), ('Con', '{{anfitrion}}')]),
            E.boton('Entrar a la videollamada', '{{enlace_videollamada}}', margen='0 40px 16px'),
            E.parrafo('¿No te va bien la hora? %s.' % enlace('Cámbiala o cancélala aquí', '{{enlace_reprogramar}}'),
                      pequeno=True, margen_inf=32),
            E.separador('0 40px 28px'),
            E.titular('Qué tener a mano (10 minutos)', nivel=2, margen_inf=16),
            E.lista([
                '%s Ticket medio o valor de un tratamiento; con una cifra aproximada basta.' % b('Cuánto vale un cliente para ti.'),
                '%s y por dónde: llamadas, WhatsApp, formulario, Instagram.' % b('Cuántos contactos te llegan al mes'),
                '%s Anuncios, agencias, promociones: qué pasó y qué no te convenció.' % b('Qué has probado ya.'),
                '%s aunque sea una intuición.' % b('Tu objetivo para los próximos tres meses,'),
            ]),
            E.parrafo('No hace falta preparar presentaciones ni darnos accesos todavía. Y si no encajamos, te lo decimos.', margen_inf=16),
            E.despedida('Hasta el {{fecha}},', 'Juan Salazar', 'Estrategia &amp; Ads · Oryzz'),
            E.fuera(E.pie(motivo='Te escribimos porque reservaste una valoración en cal.com/oryzz/30min.')),
        ],
        ['Tu diagnóstico del {{fecha}}: qué tener a mano', '{{nombre}}, nos vemos el {{fecha}} a las {{hora}}'],
        ['Transaccional. Se dispara al reservar en cal.com (webhook → Resend/Brevo) o se envía a mano.',
         'Cal.com ya envía su propia invitación: esta plantilla la complementa con el «qué preparar».'],
        'Transaccional', 'Confirmación de la videollamada de 30 minutos y qué preparar.')

    # ------------------------------------------------------------ 05 BIENVENIDA
    registrar(
        '05_bienvenida_onboarding', 'Empezamos, {{nombre}}: tus próximos 7 días',
        'Qué accesos necesitamos, cuándo es la llamada de arranque y quién lleva tu cuenta.',
        [
            E.cabecera('Alta de cliente'),
            E.espacio(40),
            E.eyebrow('Bienvenida'),
            E.espacio(14),
            E.titular('Empezamos. Esto es lo que pasa %s.' % hl('esta semana')),
            E.parrafo('Hola, {{nombre}}. Gracias por confiar en Oryzz para {{negocio}}. Desde hoy montamos tu sistema de captación: '
                      'primero los accesos, luego la llamada de arranque y, en 3–7 días, las primeras campañas listas para revisar.',
                      lead=True, margen_inf=28),
            E.imagen('diagrama-sistema.png', 'Tu sistema de captación: anuncios en Meta, Google y TikTok, respuesta en minutos con seguimiento y citas en tu agenda.',
                     ancho=518, alto=196, margen='0 40px 32px'),
            E.titular('Tus próximos pasos', nivel=2, margen_inf=20),
            E.pasos([
                dict(cuando='Hoy', titulo='Danos acceso a tus cuentas',
                     texto='La lista está justo debajo. Son unos 15 minutos y, si te atascas, lo hacemos contigo por videollamada.'),
                dict(cuando='Días 2–3', titulo='Llamada de arranque (45 min)',
                     texto='Repasamos objetivos, servicios, horarios y cómo quieres que se atiendan los mensajes. Fecha: {{fecha_arranque}}.'),
                dict(cuando='Días 3–7', titulo='Campañas y respuestas listas para revisar',
                     texto='Te enseñamos anuncios, textos y mensajes automáticos antes de publicar. Nada sale sin tu visto bueno.'),
                dict(cuando='Cada mes', titulo='Informe en euros, no en impresiones',
                     texto='Leads, citas, coste por lead y qué cambiamos. Y una llamada si quieres repasarlo.'),
            ]),
            E.separador('0 40px 28px'),
            E.titular('Accesos que necesitamos', nivel=2, margen_inf=16),
            E.detalles([
                ('Meta', 'Añade a Oryzz como socio en Business Suite con el ID {{id_business_oryzz}}: página, Instagram y cuenta publicitaria.'),
                ('Google Ads', 'Acepta la invitación de nuestra cuenta de administrador ({{id_mcc_oryzz}}).'),
                ('Perfil Google', 'Añade {{email_accesos}} como administrador de tu Perfil de Empresa.'),
                ('Web', 'Acceso a la web (o el contacto de quien la lleva) y a Analytics o Tag Manager si los tienes.'),
                ('WhatsApp', 'El número con el que atendéis a clientes y quién responde hoy.'),
            ], margen='0 40px 24px'),
            E.boton('Completar la lista de accesos', '{{url_formulario_accesos}}'),
            E.titular('Quién lleva tu cuenta', nivel=2, margen_inf=16),
            E.personas([('Juan Salazar', 'Estrategia &amp; Ads', '{{email_juan}}'),
                        ('David Morales', 'Automatización &amp; IA', '{{email_david}}')]),
            E.parrafo('Para cualquier duda, responde a este correo: lo leemos los dos.', margen_inf=16),
            E.despedida('Un abrazo y a por ello,', 'Juan y David', 'Socios de Oryzz'),
            E.fuera(E.pie(motivo='Te escribimos porque {{negocio}} acaba de empezar a trabajar con Oryzz.')),
        ],
        ['Bienvenida a Oryzz: accesos y llamada de arranque', '{{negocio}} + Oryzz: lo que pasa esta semana'],
        ['Se envía el mismo día de la firma. Rellena los ID de Meta/Google antes de enviar.',
         'El diagrama es una imagen con alt descriptivo; los pasos van en texto real.'],
        'Cliente', 'Bienvenida a cliente nuevo: próximos pasos, accesos a pedir y equipo.')

    # ------------------------------------------------------------ 06 INFORME MENSUAL
    registrar(
        '06_informe_mensual', 'Septiembre en {{negocio}}: 61 citas y el coste por lead a la baja',
        'El mes en cuatro cifras, qué funcionó, qué cambiamos y el plan para octubre.',
        [
            E.cabecera('Informe mensual'),
            E.hero_oscuro('Septiembre 2026',
                          '61 citas nuevas. Mismo presupuesto, menos coste por lead.',
                          'La versión corta: la respuesta automática por WhatsApp convirtió más contactos en citas.'),
            E.espacio(32),
            E.parrafo('Hola, {{nombre}}. Aquí tienes el resumen de septiembre. Las cifras salen del panel de campañas y de tu agenda.',
                      margen_inf=24),
            E.tarjetas_dato([
                dict(etiqueta='Leads', valor='184', delta='+22&nbsp;% vs. agosto'),
                dict(etiqueta='Citas', valor='61', delta='+14&nbsp;% vs. agosto'),
                dict(etiqueta='Coste por lead', valor='11,40&nbsp;€', delta='−9&nbsp;% vs. agosto'),
                dict(etiqueta='Inversión', valor='2.100&nbsp;€', delta='En presupuesto', tono='neutro'),
            ], eyebrow_txt='Resumen · Datos de ejemplo'),
            E.titular('Lo que funcionó', nivel=2, margen_inf=10),
            E.parrafo('La campaña de «primera revisión sin coste» en Meta trajo el 58&nbsp;% de los leads. El asistente de WhatsApp '
                      'respondió en menos de 5 minutos al 92&nbsp;% de los mensajes, también fuera de horario.', margen_inf=24),
            E.titular('Lo que cambiamos', nivel=2, margen_inf=10),
            E.parrafo('Pausamos Google Ads entre las 23:00 y las 7:00: se llevaba el 18&nbsp;% del presupuesto y no traía citas. '
                      'Ese dinero pasó a la campaña que mejor convierte.', margen_inf=24),
            E.titular('Plan para octubre', nivel=2, margen_inf=14),
            E.lista([
                'Probar un segundo anuncio en vídeo grabado con tu equipo en la clínica.',
                'Activar el recordatorio de cita 24 horas antes para bajar las ausencias.',
                'Pedir la reseña al terminar cada tratamiento, con la placa de recepción.',
            ]),
            E.boton('Ver el panel completo', '{{url_panel}}'),
            E.parrafo('Si quieres repasarlo por videollamada, responde a este correo y buscamos hueco.', margen_inf=24),
            E.despedida('Un saludo,', 'Juan Salazar', 'Estrategia &amp; Ads · Oryzz'),
            E.fuera(E.pie(motivo='Te escribimos porque {{negocio}} es cliente de Oryzz. Las cifras de esta plantilla son de ejemplo.')),
        ],
        ['{{mes}} en {{negocio}}: {{citas}} citas nuevas', 'Tu informe de {{mes}}, en cuatro cifras'],
        ['DATOS DE EJEMPLO: cambia cifras, deltas y textos, y quita «· Datos de ejemplo» del rótulo de las tarjetas.',
         'Tarjetas dato: Grafito 850 sobre banda Grafito 950, delta en lima (solo si es una mejora; si no, tono neutro).',
         'Primer día hábil de cada mes.'],
        'Cliente', 'Informe mensual con tarjetas dato (KPIs de ejemplo) y plan del mes siguiente.')

    # ------------------------------------------------------------ 07 PROPUESTA ENVIADA
    registrar(
        '07_propuesta_enviada', 'Tu propuesta de captación para {{negocio}}',
        'Qué haríamos, en cuánto tiempo y cuánto cuesta. En una página y sin letra pequeña.',
        [
            E.cabecera('Propuesta'),
            E.espacio(40),
            E.eyebrow('Propuesta · válida hasta el {{fecha_validez}}'),
            E.espacio(14),
            E.titular('Tu plan para conseguir más %s, en una página.' % hl('citas')),
            E.parrafo('Hola, {{nombre}}. Gracias por la llamada del {{fecha_llamada}}. Como quedamos, aquí tienes la propuesta para '
                      '{{negocio}}. Te resumo lo importante:', lead=True, margen_inf=24),
            E.detalles([
                ('Objetivo', '{{objetivo}}'),
                ('Canales', '{{canales}}'),
                ('Arranque', 'Primeras campañas listas para revisar en 3–7 días desde la firma'),
                ('Anuncios', '{{inversion_ads}} al mes, que pagas directamente a cada plataforma'),
                ('Honorarios', '{{honorarios}} al mes + IVA'),
                ('Compromiso', '{{permanencia}}'),
            ]),
            E.boton('Ver la propuesta completa', '{{url_propuesta}}'),
            E.parrafo('Si algo no te cuadra, dímelo tal cual: prefiero ajustar el alcance antes que inflar el precio. '
                      'Y si ves que no encajamos, también me sirve saberlo.'),
            E.parrafo('Para seguir adelante, basta con responder «adelante» a este correo. Te enviamos el contrato y la lista de accesos el mismo día.',
                      margen_inf=16),
            E.despedida('Un saludo,', 'Juan Salazar', 'Estrategia &amp; Ads · Oryzz'),
            E.fuera(E.pie(motivo='Te escribimos porque pediste una propuesta a Oryzz para {{negocio}}.')),
        ],
        ['{{nombre}}, tu propuesta en una página', 'Propuesta para {{negocio}}: plan, plazos y precio'],
        ['Adjunta el PDF de la propuesta o enlázalo en {{url_propuesta}} (mejor enlace: pesa menos y sabes si se abrió).',
         'Rellena la tarjeta con cifras concretas: «40 citas nuevas al mes en 90 días», «1.500 € al mes», etc.'],
        'Comercial', 'Envío de propuesta con resumen en tarjeta y CTA a la propuesta completa.')

    # ------------------------------------------------------------ 08 TAP PEDIDO CONFIRMADO
    registrar(
        '08_tap_pedido_confirmado', 'Pedido {{numero_pedido}} confirmado: ya preparamos tu Oryzz Tap',
        'Te avisamos cuando salga, con el número de seguimiento. Entrega estimada: {{plazo_entrega}}.',
        [
            E.cabecera('Pedido {{numero_pedido}}', variante='tap', url='https://oryzz.com/tap'),
            E.espacio(40),
            E.eyebrow('Pedido confirmado'),
            E.espacio(14),
            E.titular('Gracias, {{nombre}}. Ya estamos preparando tu %s.' % hl('Oryzz Tap')),
            E.parrafo('Hemos recibido tu pedido y el pago. Lo preparamos y te escribimos en cuanto salga, con el número de seguimiento.',
                      lead=True, margen_inf=24),
            E.detalles([
                ('Producto', '{{producto}}'), ('Cantidad', '{{cantidad}}'), ('Total', '{{total}}'),
                ('Envío a', '{{direccion_envio}}'), ('Entrega', '{{plazo_entrega}}'),
            ]),
            E.boton('Ver mi pedido', '{{url_pedido}}'),
            E.titular('Qué pasa ahora', nivel=2, margen_inf=14),
            E.lista([
                'Preparamos tu pedido y te enviamos el número de seguimiento.',
                'Llega a tu dirección en {{plazo_entrega}}.',
                'La activas en 2 minutos: ese mismo día te mandamos los pasos.',
            ]),
            E.parrafo('¿Algo del pedido no está bien? Responde a este correo o escríbenos a %s.'
                      % enlace('pedidos@oryzz.com', 'mailto:pedidos@oryzz.com'), margen_inf=16),
            E.despedida('Gracias por confiar en nosotros,', 'Equipo Oryzz Tap', 'Tu negocio. A un toque.'),
            E.fuera(E.pie(marca='tap', motivo='Te escribimos porque hiciste un pedido en shop.oryzz.com.')),
        ],
        ['Tu Oryzz Tap está en preparación (pedido {{numero_pedido}})', 'Recibido, {{nombre}}: pedido {{numero_pedido}}'],
        ['Transaccional de Shopify: pega este HTML en Configuración → Notificaciones → Confirmación de pedido y cambia los marcadores por '
         'variables Liquid ({{ order.name }}, {{ customer.first_name }}, {{ order_status_url }}…). Ver LEEME.',
         'Expresión clara de Oryzz Tap (BRAND_SPEC §7). Precios en COP: «$ 89.900 COP».'],
        'Oryzz Tap', 'Confirmación de pedido de Oryzz Tap (Shopify, COP).')

    # ------------------------------------------------------------ 09 TAP ACTIVACIÓN
    registrar(
        '09_tap_activacion', 'Activa tu Oryzz Tap en 2 minutos',
        'Acerca el teléfono, escribe tu código de 8 dígitos y elige qué se abre con cada toque.',
        [
            E.cabecera('Activación', variante='tap', url='https://oryzz.com/tap'),
            E.espacio(40),
            E.eyebrow('Tu Oryzz Tap ya llegó'),
            E.espacio(14),
            E.titular('Acerca el teléfono y %s.' % hl('ocurre')),
            E.parrafo('Hola, {{nombre}}. Antes de ponerla en el mostrador, actívala: son cuatro pasos y unos 2 minutos.',
                      lead=True, margen_inf=28),
            E.pasos([
                dict(titulo='Acerca el teléfono o escanea el QR',
                     texto='Acerca la parte de arriba del móvil a la placa. Si no reacciona, abre la cámara y escanea el código QR.'),
                dict(titulo='Escribe tu código de 8 dígitos',
                     texto='Viene con tu Oryzz Tap. Escríbelo sin espacios: así sabemos que la placa es tuya.',
                     extra_html=E.codigo('0000&nbsp;0000', 'FORMATO'), extra_txt='Formato: 8 dígitos (0000 0000)'),
                dict(titulo='Crea tu cuenta',
                     texto='Con tu correo y una contraseña. Desde ahí cambias a dónde lleva tu placa cuando quieras.'),
                dict(titulo='Configura tu perfil',
                     texto='Pega el enlace de reseñas de Google o elige tu perfil Oryzz Pro y guarda. Desde ese momento, cada toque abre esa pantalla.'),
            ], iconos=['nfc', 'codigo', 'usuario', 'check-orbita'], margen_inf=8),
            E.boton('Activar mi Oryzz Tap', '{{url_activacion}}'),
            E.separador('0 40px 28px'),
            E.titular('Dónde colocarla', nivel=2, margen_inf=10),
            E.parrafo('Donde el cliente ya tiene el móvil en la mano: junto a la caja o en recepción, a la altura de la mano. '
                      'Y pídelo en voz alta: «¿Nos dejas una reseña? Acerca el móvil aquí».'),
            E.parrafo('¿No se activa? Escríbenos a %s con tu número de pedido y lo resolvemos.'
                      % enlace('pedidos@oryzz.com', 'mailto:pedidos@oryzz.com'), margen_inf=16),
            E.despedida('Que la disfrutes,', 'Equipo Oryzz Tap', 'Tu negocio. A un toque.'),
            E.fuera(E.pie(marca='tap', motivo='Te escribimos porque tu pedido {{numero_pedido}} ya está entregado.')),
        ],
        ['{{nombre}}, tu placa está lista para activar', 'Cuatro pasos y tu Oryzz Tap empieza a funcionar'],
        ['Se envía al marcar el pedido como entregado (Shopify Flow o manual).',
         'Verifica con producto dónde viene impreso el código de 8 dígitos y ajusta el paso 2 si hace falta.',
         'Iconos oficiales de 05_Elementos_Graficos/01_Iconos (nfc, usuario, check-orbita) + «codigo» dibujado en el mismo estilo.'],
        'Oryzz Tap', 'Activación de Oryzz Tap: NFC/QR → 8 dígitos → cuenta → perfil.')

    # ------------------------------------------------------------ 10 BASE EN BLANCO
    base_blanco()


def doc(texto, bloque):
    """Antepone un comentario de documentación a un bloque (solo en la plantilla base)."""
    bloque = dict(bloque)
    lineas = '\n'.join('     ' + l for l in texto.strip().split('\n'))
    bloque['html'] = '\n<!-- ══════════════════════════════════════════════════════════════\n%s\n══════════════════════════════════════════════════════════════ -->%s' % (lineas, bloque['html'])
    return bloque


def base_blanco():
    bl = [
        doc('CABECERA · obligatoria, siempre la primera fila de la tarjeta.\n'
            'E.cabecera(etiqueta, variante): «oscuro» = Oryzz (banda Grafito 950 + logo sólido).\n'
            'Para Oryzz Tap copia la cabecera de 08_tap_pedido_confirmado.html (expresión clara, logo que cambia en modo oscuro).\n'
            'La etiqueta de la derecha: MAYÚSCULAS, máx. 18 caracteres, sin emojis.',
            E.cabecera('Tipo de correo')),
        doc('HERO OSCURO · opcional (newsletter, informes, anuncios importantes). Sustituye a EYEBROW + TITULAR.\n'
            'La órbita de la derecha es decorativa (alt vacío) y se oculta en móvil. Un solo fragmento en azul.',
            E.hero_oscuro('Rótulo del hero', 'Titular corto, con una sola %s en azul.' % hl_oscuro('palabra'),
                          'Entradilla opcional de una o dos frases que explica qué gana quien sigue leyendo.')),
        E.espacio(36),
        doc('EYEBROW · rótulo en JetBrains Mono, MAYÚSCULAS, 12 px, con el nodo lima delante.\n'
            'Dice qué es el correo en 2–4 palabras. Usa E.espacio(14) debajo antes del titular.',
            E.eyebrow('Rótulo del correo')),
        E.espacio(14),
        doc('TITULAR · Space Grotesk 700, 34 px (28 px en móvil). Máximo 2–3 líneas.\n'
            'Resalta UN solo fragmento con <span class="o-hl" style="color:#3B72FF;">…</span>. Nunca el titular entero.\n'
            'Subtítulo de sección: el mismo bloque con nivel 2 (22 px, <h2>).',
            E.titular('Un titular corto que dice %s.' % hl('una sola cosa'))),
        doc('PÁRRAFO DESTACADO (lead) · 18 px. Primer párrafo: saluda y di para qué es el correo en dos frases.',
            E.parrafo('Hola, {{nombre}}. Este es el párrafo destacado: la primera frase dice para qué escribimos y la segunda, '
                      'qué tiene que hacer la persona. Si no cabe en dos frases, el correo es demasiado largo.', lead=True, margen_inf=24)),
        doc('PÁRRAFO · Manrope 16/26 px, Grafito 600. Frases cortas, tuteo, cifras concretas.\n'
            'Enlaces dentro del texto: usa el patrón de abajo (azul 600 subrayado, clase o-link).',
            E.parrafo('Un párrafo normal tiene tres o cuatro líneas como mucho. Habla de clientes, citas y euros, no de impresiones. '
                      'Si enlazas algo en el texto, que sea %s y que el texto del enlace diga adónde lleva.' % enlace('algo concreto', 'https://oryzz.com'))),
        doc('BOTÓN · «bulletproof»: VML para Outlook Windows + <a> para el resto. UNO por correo.\n'
            'Cambia la URL en DOS sitios (href del v:roundrect y href del <a>) y el texto en DOS sitios (<center> y <a>).\n'
            'Si el texto es más largo, sube el width del v:roundrect (≈ 9,4 px por carácter + 60).\n'
            'En modo oscuro (Apple Mail) pasa solo a gradiente IA con texto Grafito 950, como pide BRAND_SPEC §3.',
            E.boton('Verbo + resultado', 'https://oryzz.com')),
        doc('TARJETAS DATO · KPIs sobre banda Grafito 950. Siempre en pares (2, 4 o 6 tarjetas).\n'
            'Delta en lima solo si es una mejora; tono «neutro» (titanio) si no lo es. Cifras con unidad y fuente.\n'
            'Si los datos no son reales, el rótulo DEBE decir «Datos de ejemplo» (BRAND_SPEC §8.7).',
            E.tarjetas_dato([dict(etiqueta='Métrica', valor='128', delta='+12&nbsp;% vs. mes anterior'),
                             dict(etiqueta='Otra métrica', valor='9,80&nbsp;€', delta='Sin cambios', tono='neutro')],
                            eyebrow_txt='Rótulo · Datos de ejemplo')),
        doc('LISTA · estilo «num» (01, 02… en mono azul) o «guion». Máx. 5 elementos, una idea por línea.\n'
            'Puedes empezar cada elemento con <strong> para que se lea en diagonal.',
            E.lista(['%s y después la explicación en la misma línea.' % b('Empieza por la acción,'),
                     'Un elemento, una idea. Si necesitas dos frases, probablemente son dos elementos.',
                     'Tres elementos se leen; siete, no.'])),
        doc('CITA · para una frase de cliente (real y con permiso) o una frase de marca. Borde azul a la izquierda.',
            E.cita('Sales con un diagnóstico, no con un presupuesto.', 'Oryzz · valoración de 30 minutos')),
        doc('IMAGEN · ancho de columna 518 px (fluida en móvil). PNG/JPG a 2× (1036 px de ancho).\n'
            'alt SIEMPRE descriptivo (lo que se ve y lo que significa). Nunca metas texto importante solo en la imagen.\n'
            'Fotografía: personas reales de negocios reales, velo Grafito 950 si lleva texto encima (BRAND_SPEC §5.6).',
            E.imagen('diagrama-sistema.png', 'Diagrama del sistema de captación de Oryzz: anuncios, respuesta en minutos y citas en agenda.',
                     ancho=518, alto=196)),
        doc('DETALLES · tarjeta clave/valor (fecha y hora, resumen de pedido, condiciones de una propuesta).\n'
            'Clave en mono MAYÚSCULAS (máx. 12 caracteres); valor en Manrope 600.',
            E.detalles([('Clave', 'Valor concreto'), ('Fecha', '{{fecha}} · {{hora}}'), ('Importe', '1.500&nbsp;€ al mes + IVA')])),
        doc('PASOS · proceso de 3–5 pasos. Con rótulo temporal («Hoy», «Días 2–3») o con iconos PNG 48 px\n'
            '(ver 09_tap_activacion.html: E.pasos(items, iconos=[...]) usa assets/icono-<nombre>_claro/_oscuro.png).',
            E.pasos([dict(cuando='Hoy', titulo='Primer paso', texto='Qué pasa y qué tiene que hacer la persona, en una frase.'),
                     dict(cuando='Mañana', titulo='Segundo paso', texto='Plazos en números: «3–7 días», «30 minutos».')])),
        doc('SEPARADOR · línea de 1 px Grafito 100. Úsalo entre partes del correo, no entre cada párrafo.',
            E.separador()),
        doc('SECCIÓN NUMERADA · bloque editorial de la newsletter (número mono + titular + texto + enlace opcional).',
            E.seccion('01', 'Titular de la sección en una línea', ['Texto de la sección: el aprendizaje, el dato y qué hacer con él.'],
                      enlace('Leer el caso completo →', 'https://oryzz.com'))),
        doc('PERSONAS · tarjetas de contacto del equipo (2 columnas; se apilan en móvil).',
            E.personas([('Juan Salazar', 'Estrategia &amp; Ads', '{{email_juan}}'), ('David Morales', 'Automatización &amp; IA', '{{email_david}}')])),
        doc('DESPEDIDA · cierre con nombre real. Nunca «El equipo de marketing».',
            E.despedida('Un saludo,', 'Juan Salazar', 'Estrategia &amp; Ads · Oryzz')),
        doc('PIE · va FUERA de la tarjeta (E.fuera). Oryzz o Tap (marca="tap").\n'
            'Motivo del envío siempre. En correos comerciales/newsletter: enlace de baja {{baja_url}} + {{direccion_postal}}.',
            E.fuera(E.pie(motivo='Te escribimos porque… (motivo real del envío).', baja=True, direccion=True))),
    ]
    registrar(
        '10_base_en_blanco', 'Asunto: 35–50 caracteres, concreto, sin emojis',
        'Preheader: completa el asunto en 40–90 caracteres; no lo repitas.',
        bl, ['Consulta la Guia_de_redaccion_email.md para ejemplos de asunto'],
        ['ESQUELETO MODULAR. Cada bloque va entre dos comentarios: «▸ BLOQUE · NOMBRE» y «◂ FIN · NOMBRE».',
         'Para crear un correo nuevo: duplica este archivo, borra los bloques que no uses y reescribe los textos.',
         'Para repetir un bloque, copia desde «▸ BLOQUE» hasta «◂ FIN» (ambos incluidos) y pégalo donde quieras dentro de la tarjeta.',
         'No cambies colores fuera de los tokens (00_Fuente_Maestra/tokens.json). Tamaño mínimo de texto: 14 px (rótulos mono: 12 px).',
         'Modo oscuro: conserva las clases o-t1/o-t2/o-t3/o-link/o-bd/o-bg-surface; son las que cambian el color en Apple Mail y Outlook.com.'],
        'Base', 'Esqueleto modular documentado con todos los bloques del sistema.')


# =====================================================================
# 3. FIRMAS
# =====================================================================
FIRMAS = {
    'juan-salazar': dict(nombre='Juan Salazar', rol='Socio · Estrategia &amp; Ads', email='{{email_juan}}', tel='{{telefono_juan}}',
                         avatar='firma-avatar-oryzz.png', marca='oryzz'),
    'david-morales': dict(nombre='David Morales', rol='Socio · Automatización &amp; IA', email='{{email_david}}', tel='{{telefono_david}}',
                          avatar='firma-avatar-oryzz.png', marca='oryzz'),
    'oryzz-tap': dict(nombre='Equipo Oryzz Tap', rol='Placas NFC + QR para reseñas y perfil', email='pedidos@oryzz.com', tel='{{telefono_tap}}',
                      avatar='firma-avatar-tap.png', marca='tap'),
}
FA = 'font-family:Arial,Helvetica,sans-serif;'


def _a(t, u, col='#3A4152', bold=False):
    return ('<a href="%s" target="_blank" style="%scolor:%s;text-decoration:none;%s">%s</a>'
            % (u, FA, col, 'font-weight:bold;' if bold else '', t))


def firma_completa(f, base):
    if f['marca'] == 'tap':
        l3 = '%s &nbsp;·&nbsp; %s' % (_a('pedidos@oryzz.com', 'mailto:pedidos@oryzz.com'), _a('shop.oryzz.com', 'https://shop.oryzz.com'))
        l4 = '%s &nbsp;·&nbsp; %s' % (_a('Ver Oryzz Tap →', 'https://oryzz.com/tap', '#2C5BD0', True), 'Tu negocio. A un toque.')
        redes = '%s &nbsp;·&nbsp; %s' % (_a('Instagram @oryzztap', 'https://instagram.com/oryzztap', '#5A6172'),
                                          _a('TikTok @oryzz.tap', 'https://www.tiktok.com/@oryzz.tap', '#5A6172'))
        home = 'https://oryzz.com/tap'
    else:
        l3 = '%s &nbsp;·&nbsp; %s' % (_a(f['email'], 'mailto:' + f['email']), _a(f['tel'], 'tel:' + f['tel']))
        l4 = '%s &nbsp;·&nbsp; %s' % (_a('Agenda 30 minutos →', CAL, '#2C5BD0', True), _a('oryzz.com', 'https://oryzz.com'))
        redes = '%s &nbsp;·&nbsp; %s' % (_a('Instagram', 'https://instagram.com/oryzzai', '#5A6172'),
                                          _a('LinkedIn', 'https://www.linkedin.com/company/oryzz', '#5A6172'))
        home = 'https://oryzz.com'
    return ('<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;%s">'
            '<tr><td valign="top" style="padding:2px 16px 0 0;">'
            '<a href="%s" target="_blank"><img src="%s/%s" width="56" height="56" alt="Oryzz" '
            'style="display:block;width:56px;height:56px;border:0;border-radius:12px;"></a></td>'
            '<td valign="top" style="border-left:1px solid #D5D9E0;padding:0 0 0 16px;%s">'
            '<div style="%sfont-size:16px;line-height:22px;font-weight:bold;color:#0B0D12;">%s</div>'
            '<div style="%sfont-size:14px;line-height:20px;color:#5A6172;padding:0 0 8px;">%s%s</div>'
            '<div style="%sfont-size:14px;line-height:21px;color:#3A4152;">%s</div>'
            '<div style="%sfont-size:14px;line-height:21px;color:#3A4152;">%s</div>'
            '<div style="%sfont-size:14px;line-height:21px;color:#5A6172;padding:6px 0 0;">%s</div>'
            '</td></tr></table>'
            % (FA, home, base, f['avatar'], FA, FA, f['nombre'], FA, f['rol'], '' if f['marca'] == 'tap' else ' · Oryzz',
               FA, l3, FA, l4, FA, redes))


def firma_compacta(f):
    if f['marca'] == 'tap':
        l2 = 'pedidos@oryzz.com &nbsp;·&nbsp; %s' % _a('oryzz.com/tap', 'https://oryzz.com/tap', '#2C5BD0')
        l1 = '<b style="color:#0B0D12;">Equipo Oryzz Tap</b>'
    else:
        l1 = '<b style="color:#0B0D12;">%s</b> · Oryzz' % f['nombre']
        l2 = '%s &nbsp;·&nbsp; %s &nbsp;·&nbsp; %s' % (f['rol'].replace('Socio · ', ''), f['tel'], _a('oryzz.com', 'https://oryzz.com', '#2C5BD0'))
    return ('<div style="%sfont-size:14px;line-height:21px;color:#3A4152;">%s</div>'
            '<div style="%sfont-size:14px;line-height:21px;color:#5A6172;">%s</div>' % (FA, l1, FA, l2))


def firma_txt(f, completa=True):
    if f['marca'] == 'tap':
        return ('Equipo Oryzz Tap\nPlacas NFC + QR para reseñas y perfil\npedidos@oryzz.com · shop.oryzz.com\n'
                'oryzz.com/tap · Instagram @oryzztap · TikTok @oryzz.tap' if completa else 'Equipo Oryzz Tap · pedidos@oryzz.com · oryzz.com/tap')
    rol = _html.unescape(f['rol'])
    if completa:
        return '%s\n%s · Oryzz\n%s · %s\nAgenda 30 minutos: cal.com/oryzz/30min\noryzz.com' % (f['nombre'], rol, f['email'], f['tel'])
    return '%s · Oryzz\n%s · %s · oryzz.com' % (f['nombre'], rol.replace('Socio · ', ''), f['tel'])


def firma_archivo(titulo, cuerpo):
    return ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n'
            '<!--\n  ORYZZ · FIRMA DE CORREO\n'
            '  BASE_URL = %s\n'
            '  (las imágenes se cargan desde BASE_URL. Si cambias el alojamiento, busca y reemplaza esa URL.)\n'
            '  Sustituye los {{marcadores}} (email, teléfono) antes de instalarla.\n'
            '  Instalación: firmas/como-instalar-en-gmail.md. Lo más cómodo: abrir _copiar_firmas.html y pulsar «Copiar».\n-->\n'
            '</head>\n<body style="margin:0;padding:24px;background:#FFFFFF;">\n'
            '<!-- ▸ FIRMA: copia desde aquí -->\n%s\n<!-- ◂ FIRMA: hasta aquí -->\n</body>\n</html>\n' % (titulo, BASE_URL, cuerpo))


COPIAR_HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Firmas de correo · Oryzz</title>
<script>
/* ══════════ CONFIGURACIÓN · edita solo esto ══════════ */
const BASE_URL = '%BASE%';          // donde has subido 08_Email/assets/ (sin barra final)
const DATOS = {
  email_juan:     '{{email_juan}}',     // p. ej. juan@oryzz.com
  telefono_juan:  '{{telefono_juan}}',  // p. ej. +34 600 000 000
  email_david:    '{{email_david}}',
  telefono_david: '{{telefono_david}}',
  telefono_tap:   '{{telefono_tap}}'
};
/* ═════════════════════════════════════════════════════ */
</script>
<style>
:root{--fondo:#F6F7F9;--superficie:#FFFFFF;--borde:#E5E8EE;--texto:#0B0D12;--texto-2:#3A4152;--texto-3:#5A6172;--azul:#2C5BD0;--nodo:#7FB02E}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--fondo:#0B0D12;--superficie:#12151D;--borde:#232836;--texto:#FFFFFF;--texto-2:#D5D9E0;--texto-3:#8A90A0;--azul:#9FB8FF;--nodo:#BFF24A}}
:root[data-theme="dark"]{--fondo:#0B0D12;--superficie:#12151D;--borde:#232836;--texto:#FFFFFF;--texto-2:#D5D9E0;--texto-3:#8A90A0;--azul:#9FB8FF;--nodo:#BFF24A}
body{margin:0;background:var(--fondo);color:var(--texto);font:16px/1.6 Manrope,Arial,sans-serif}
main{max-width:880px;margin:0 auto;padding:48px 16px 80px}
.eb{font:500 12px/16px 'JetBrains Mono',Consolas,monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--texto-3);margin:0 0 12px}
.eb b{color:var(--nodo);font-weight:500}
h1{font:700 40px/1.1 'Space Grotesk',Arial,sans-serif;letter-spacing:-.03em;margin:0 0 12px}
h2{font:600 20px/1.3 'Space Grotesk',Arial,sans-serif;margin:0 0 4px}
p.lead{color:var(--texto-2);margin:0 0 32px;max-width:640px}
.aviso{display:none;border:1px solid #F2A33A;border-radius:12px;padding:14px 18px;margin:0 0 32px;color:var(--texto-2)}
.f{background:var(--superficie);border:1px solid var(--borde);border-radius:16px;padding:24px;margin:0 0 20px}
.f header{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0 0 18px;flex-wrap:wrap}
.f small{color:var(--texto-3);font-size:14px}
.lienzo{background:#FFFFFF;border-radius:10px;padding:20px;overflow-x:auto}
button{font:700 15px Manrope,Arial,sans-serif;background:var(--azul);color:#fff;border:0;border-radius:10px;padding:10px 18px;cursor:pointer}
@media (prefers-color-scheme:dark){button{color:#0B0D12}}
button.ok{background:#1F9D55;color:#fff}
ol{color:var(--texto-2);padding-left:20px}
code{font-family:'JetBrains Mono',Consolas,monospace;font-size:14px}
</style>
</head>
<body>
<main>
<p class="eb"><b>●</b>&nbsp; 08_Email · firmas</p>
<h1>Firmas de correo</h1>
<p class="lead">Pulsa «Copiar firma» y pégala en Gmail (Configuración → Ver todos los ajustes → Firma) o en Outlook. Usa la completa para correos nuevos y la compacta para respuestas. Antes, edita la configuración al principio de este archivo (BASE_URL, correos y teléfonos).</p>
<div class="aviso" id="aviso"><strong>Las imágenes no están subidas todavía.</strong> Se muestran desde la carpeta local <code>assets/</code>. Súbelas a <code id="burl"></code> antes de copiar la firma completa, o Gmail la mostrará sin logo.</div>
%FIRMAS%
<ol>
<li>La firma compacta no lleva imágenes: se puede instalar ya.</li>
<li>Gmail en el móvil solo admite firma en texto: usa la versión de texto de <code>como-instalar-en-gmail.md</code>.</li>
</ol>
</main>
<script>
(function(){
  let local = false;
  document.querySelectorAll('.lienzo').forEach(function(c){
    let h = c.innerHTML;
    Object.keys(DATOS).forEach(function(k){ h = h.split('{{'+k+'}}').join(DATOS[k]); });
    h = h.split('%BASE_PLACEHOLDER%').join(BASE_URL);
    c.innerHTML = h;
  });
  document.querySelectorAll('.lienzo img').forEach(function(img){
    img.addEventListener('error', function(){
      if (img.dataset.fallback) return;
      img.dataset.fallback = '1'; local = true;
      img.src = '../assets/' + img.src.split('/').pop();
      document.getElementById('aviso').style.display = 'block';
      document.getElementById('burl').textContent = BASE_URL + '/';
    });
  });
  document.querySelectorAll('button[data-copiar]').forEach(function(btn){
    btn.addEventListener('click', function(){
      const el = document.getElementById(btn.dataset.copiar);
      const r = document.createRange(); r.selectNodeContents(el);
      const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      let ok = false; try { ok = document.execCommand('copy'); } catch(e) {}
      s.removeAllRanges();
      btn.textContent = ok ? 'Copiada. Pégala en Gmail' : 'Selecciona y copia a mano (Ctrl+C)';
      btn.classList.toggle('ok', ok);
      setTimeout(function(){ btn.textContent = 'Copiar firma'; btn.classList.remove('ok'); }, 2600);
    });
  });
})();
</script>
</body>
</html>
"""


def firmas():
    d = OUT / 'firmas'
    d.mkdir(parents=True, exist_ok=True)
    bloques, textos = [], []
    for slug, f in FIRMAS.items():
        for tipo in ('completa', 'compacta'):
            cuerpo = firma_completa(f, BASE_URL) if tipo == 'completa' else firma_compacta(f)
            titulo = 'Firma %s · %s' % (tipo, _html.unescape(f['nombre']))
            (d / ('firma_%s_%s.html' % (slug, tipo))).write_text(firma_archivo(titulo, cuerpo), encoding='utf8')
            (d / ('firma_%s_%s.txt' % (slug, tipo))).write_text(firma_txt(f, tipo == 'completa') + '\n', encoding='utf8')
            cid = '%s-%s' % (slug, tipo)
            cuerpo_p = firma_completa(f, '%BASE_PLACEHOLDER%') if tipo == 'completa' else cuerpo
            bloques.append('<section class="f"><header><div><h2>%s</h2><small>%s</small></div>'
                           '<button type="button" data-copiar="%s">Copiar firma</button></header>'
                           '<div class="lienzo" id="%s">%s</div></section>'
                           % (_html.unescape(f['nombre']), 'Completa · correos nuevos' if tipo == 'completa' else 'Compacta · respuestas y reenvíos',
                              cid, cid, cuerpo_p))
    page = COPIAR_HTML.replace('%BASE%', BASE_URL).replace('%FIRMAS%', '\n'.join(bloques))
    (d / '_copiar_firmas.html').write_text(page, encoding='utf8')
    print('firmas ok')


# =====================================================================
# 4. ESCRITURA + PUBLICACIÓN
# =====================================================================
def escribir():
    OUT.mkdir(parents=True, exist_ok=True)
    for k, v in P.items():
        (OUT / (k + '.html')).write_text(v['html'], encoding='utf8')
        (OUT / (k + '.txt')).write_text(v['txt'], encoding='utf8')
    print('plantillas ok:', len(P))


def publicar():
    import email_publicar
    email_publicar.publicar(OUT, BASE_URL)


# =====================================================================
# 5. PREVISUALIZACIONES
# =====================================================================
MUESTRA = {
    'nombre': 'Laura', 'negocio': 'Clínica Dental Arrieta', 'ciudad': 'Valencia', 'servicio': 'implantes dentales',
    'observacion_concreta': 'la ficha no tiene botón de reserva y varias reseñas recientes siguen sin respuesta',
    'dia_primer_correo': 'martes', 'fecha': 'jueves 8 de octubre', 'hora': '10:30', 'anfitrion': 'Juan Salazar, Estrategia &amp; Ads',
    'fecha_arranque': 'miércoles 14 de octubre, 10:00', 'id_business_oryzz': '1234 5678 9012', 'id_mcc_oryzz': '123-456-7890',
    'email_accesos': 'accesos@oryzz.com', 'email_juan': 'juan@oryzz.com', 'email_david': 'david@oryzz.com',
    'telefono_juan': '+34 600 000 000', 'telefono_david': '+34 600 000 001', 'telefono_tap': '+57 300 000 0000',
    'fecha_validez': '31 de octubre', 'fecha_llamada': 'lunes', 'objetivo': '40 citas nuevas al mes en 90 días',
    'canales': 'Meta Ads, Google Ads y asistente de WhatsApp', 'inversion_ads': '1.500&nbsp;€', 'honorarios': '890&nbsp;€',
    'permanencia': 'Mes a mes, sin permanencia', 'numero_pedido': '#1047', 'producto': 'Placa Reseñas Google · NFC + QR',
    'cantidad': '1', 'total': '$&nbsp;89.900 COP', 'direccion_envio': 'Cra. 43A #1-50, Medellín', 'plazo_entrega': '3–5 días hábiles',
    'direccion_postal': 'Oryzz · Dirección postal de la empresa',
}


def _local_fonts():
    f = FONTS.as_uri()
    faces = [('Space Grotesk', 500, 'SpaceGrotesk-Medium'), ('Space Grotesk', 600, 'SpaceGrotesk-SemiBold'),
             ('Space Grotesk', 700, 'SpaceGrotesk-Bold'), ('Manrope', 400, 'Manrope-Regular'), ('Manrope', 500, 'Manrope-Medium'),
             ('Manrope', 600, 'Manrope-SemiBold'), ('Manrope', 700, 'Manrope-Bold'), ('JetBrains Mono', 500, 'JetBrainsMono-Medium')]
    return '<style>%s</style>' % ''.join("@font-face{font-family:'%s';font-weight:%d;src:url('%s/%s.ttf')}" % (n, w, f, fn) for n, w, fn in faces)


def _muestra(s):
    for k, v in MUESTRA.items():
        s = s.replace('{{%s}}' % k, v)
    return s.replace('{{baja_url}}', '#').replace('{{', '').replace('}}', '')


def preview(html_path, png_path, ancho, oscuro=False):
    from PIL import Image
    s = pathlib.Path(html_path).read_text(encoding='utf8')
    s = _muestra(s)
    s = re.sub(r'<link href="https://fonts.googleapis[^>]+>', '', s)
    base = pathlib.Path(html_path).resolve().parent.as_uri() + '/'
    s = s.replace('<head>', '<head><base href="%s">%s' % (base, _local_fonts()), 1)
    # Esquema de color determinista (Chrome hereda el modo oscuro del sistema)
    s = s.replace('@media (prefers-color-scheme:dark)', '@media all' if oscuro else '@media (max-width:1px)')
    s = s.replace('</body>', '<div style="height:24px;background:#FF00FF;"></div></body>', 1)
    wrap = ('<!doctype html><html><head><meta charset="utf-8"><meta name="color-scheme" content="light"><style>html,body{margin:0;background:#FFFFFF}'
            'iframe{display:block;border:0;width:%dpx;height:9000px}</style></head><body>'
            '<iframe scrolling="no" srcdoc="%s"></iframe></body></html>'
            % (ancho, _html.escape(s, quote=True)))
    SCRATCH.mkdir(parents=True, exist_ok=True)
    wp = SCRATCH / 'wrap.html'
    wp.write_text(wrap, encoding='utf8')
    for intento in range(3):   # Chrome headless se cuelga de vez en cuando: reintenta
        try:
            render._run(['--force-device-scale-factor=2', '--window-size=%d,9000' % max(ancho, 500),
                         '--screenshot=%s' % os.path.abspath(png_path), wp.as_uri()])
            break
        except Exception as e:
            print('  reintento', intento + 1, type(e).__name__)
    im = Image.open(png_path).convert('RGB')
    W, H = im.size
    px = im.load()
    y = 0
    while y < H and px[3, y] != (255, 0, 255):
        y += 1
    im.crop((0, 0, ancho * 2, y)).save(png_path, optimize=True)
    return png_path


def preview_firmas(png):
    """Lámina estática con las 6 firmas (datos de muestra, imágenes locales)."""
    base = ASSETS.resolve().as_uri()
    filas = []
    for slug, f in FIRMAS.items():
        for tipo in ('completa', 'compacta'):
            cuerpo = firma_completa(f, base) if tipo == 'completa' else firma_compacta(f)
            filas.append('<tr><td style="padding:28px 32px;border-top:1px solid #E5E8EE;vertical-align:top;width:200px;'
                         'font:500 12px/16px JetBrains Mono,monospace;letter-spacing:.14em;color:#5A6172;text-transform:uppercase">'
                         '%s<br>%s</td><td style="padding:28px 32px;border-top:1px solid #E5E8EE">%s</td></tr>'
                         % (_html.unescape(f['nombre']), tipo, cuerpo))
    page = ('<!doctype html><html lang="es"><head><meta charset="utf-8"></head><body style="margin:0;background:#FFFFFF">'
            '<table style="border-collapse:collapse;width:100%%">%s</table></body></html>' % ''.join(filas))
    for k, v in MUESTRA.items():
        page = page.replace('{{%s}}' % k, v)
    tmp = SCRATCH / 'firmas_preview.html'
    SCRATCH.mkdir(parents=True, exist_ok=True)
    tmp.write_text(page, encoding='utf8')
    preview(tmp, png, 920)


def previews():
    pv = OUT / '_previews'
    pv.mkdir(parents=True, exist_ok=True)
    nombres = sorted(p.stem for p in OUT.glob('[0-9][0-9]_*.html'))
    for n in nombres:
        src = OUT / (n + '.html')
        preview(src, pv / ('%s_escritorio-600.png' % n), 664)
        preview(src, pv / ('%s_movil-375.png' % n), 375)
        if not n.startswith(('02_', '03_')):
            preview(src, pv / ('%s_oscuro-600.png' % n), 664, oscuro=True)
        print('preview', n)
    # Firmas
    preview_firmas(pv / 'firmas_escritorio.png')
    print('previews ok')


# =====================================================================
# 6. CATÁLOGO PDF
# =====================================================================
def catalogo():
    import email_catalogo
    email_catalogo.construir(OUT, P or leer_meta(), ROOT)


def leer_meta():
    meta = {}
    for p in sorted(OUT.glob('[0-9][0-9]_*.html')):
        s = p.read_text(encoding='utf8')
        asunto = re.search(r'Asunto:\s+(.*)', s).group(1).strip()
        pre = re.search(r'Preheader:\s+(.*)', s).group(1).strip()
        meta[p.stem] = dict(asunto=asunto, preheader=pre, tipo='', descripcion='')
    return meta


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'todo'
    if modo in ('todo', 'assets'):
        build_assets()
    if modo in ('todo', 'plantillas'):
        plantillas(); escribir(); firmas(); publicar()
    if modo in ('todo', 'previews'):
        if not P:
            plantillas()
        previews(); catalogo()
