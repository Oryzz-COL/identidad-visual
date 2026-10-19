# -*- coding: utf-8 -*-
"""
Oryzz · librería de bloques para email HTML (v2.0)
==================================================

Genera HTML de email de producción: tablas, CSS en línea, 600 px, responsive,
condicionales MSO/VML para Outlook, modo oscuro (Apple Mail, iOS, Outlook.com)
y versión de texto plano en paralelo.

Cada bloque devuelve un dict {'html': ..., 'txt': ...}. Una plantilla es una
lista de bloques que se pasa a `documento()` (correos de marca) o a
`documento_1a1()` (correos personales casi en texto plano).

Uso desde otro script:
    import email_lib as E
    bloques = [E.cabecera('Notas'), E.titular('Hola'), E.parrafo('...'), E.pie()]
    html, txt = E.documento(asunto, preheader, bloques)

Colores y tipografías salen de 00_Fuente_Maestra/tokens.json (copiados aquí
para que el HTML resultante no dependa de nada externo).
"""
import html as _html
import re

# ---------------------------------------------------------------- tokens
C = dict(
    g950='#0B0D12', g900='#0E1118', g850='#12151D', g800='#171B25', g700='#232836',
    g600='#3A4152', g500='#5A6172', g400='#8A90A0', g300='#C7CBD6', g200='#D5D9E0',
    g100='#E5E8EE', g50='#F6F7F9', w='#FFFFFF',
    a50='#EEF3FF', a300='#9FB8FF', a400='#5C8BFF', a500='#3B72FF', a600='#2C5BD0',
    c500='#36CFE0', c600='#17A9C2', l500='#BFF24A', l600='#7FB02E',
)
F_DISPLAY = "'Space Grotesk',Arial,Helvetica,sans-serif"
F_TEXT = "'Manrope',Arial,Helvetica,sans-serif"
F_MONO = "'JetBrains Mono','SF Mono',Menlo,Consolas,'Courier New',monospace"
GOOGLE_FONTS = ('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500'
                '&family=Manrope:wght@400;600;700&family=Space+Grotesk:wght@500;600;700&display=swap')

ASSETS = 'assets/'          # ruta base de imágenes en las plantillas (ver LEEME)
PX = 40                     # margen lateral del contenido en escritorio
PX_M = 24                   # margen lateral en móvil

# ---------------------------------------------------------------- CSS
CSS_BASE = """
:root{color-scheme:light dark;supported-color-schemes:light dark}
html,body{margin:0!important;padding:0!important;width:100%!important;height:100%!important}
body{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;word-spacing:normal}
table,td{border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt}
img{border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic}
a{text-decoration:none}
a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}
u + .body a{color:inherit;text-decoration:none;font-size:inherit;font-family:inherit;font-weight:inherit;line-height:inherit}
#MessageViewBody a{color:inherit;text-decoration:none;font-size:inherit;font-family:inherit;font-weight:inherit;line-height:inherit}
.o-link-u{text-decoration:underline!important}
"""

CSS_MOVIL = """
@media only screen and (max-width:640px){
.o-outer{padding:0!important}
.o-card{border-radius:0!important;border-left:0!important;border-right:0!important}
.o-hdr{border-radius:0!important}
.o-px{padding-left:%(m)spx!important;padding-right:%(m)spx!important}
.o-h1{font-size:28px!important;line-height:32px!important}
.o-h1-hero{font-size:28px!important;line-height:32px!important}
.o-h2{font-size:20px!important;line-height:26px!important}
.o-lead{font-size:17px!important;line-height:27px!important}
.o-stack{display:block!important;width:100%%!important;max-width:100%%!important}
.o-stack-gap{padding:0 0 12px 0!important}
.o-hide-m{display:none!important;width:0!important;max-height:0!important;overflow:hidden!important;mso-hide:all}
.o-btn-tbl{width:100%%!important}
.o-btn{display:block!important;padding:0 16px!important}
.o-img{width:100%%!important;max-width:100%%!important;height:auto!important}
.o-kpi{font-size:28px!important;line-height:32px!important}
.o-kpi-td{padding:16px 14px!important}
.o-dl-k{width:112px!important}
}
""" % {'m': PX_M}

# Modo oscuro: clase -> declaraciones. Se genera para prefers-color-scheme
# (Apple Mail, iOS Mail, Outlook macOS/iOS) y para Outlook.com ([data-ogsc]/[data-ogsb]).
OSCURO_COLOR = {
    'o-t1': 'color:#FFFFFF', 'o-t2': 'color:#D5D9E0', 'o-t3': 'color:#8A90A0',
    'o-link': 'color:#9FB8FF', 'o-hl': 'color:#5C8BFF', 'o-num': 'color:#9FB8FF',
    'o-node': 'color:#BFF24A',
}
OSCURO_FONDO = {
    'o-bg-page': 'background-color:#0B0D12', 'o-card': 'background-color:#12151D;border-color:#232836',
    'o-bg-surface': 'background-color:#171B25', 'o-bd': 'border-color:#232836',
    'o-hdr-claro': 'background-color:#0B0D12;border-color:#232836', 'o-quote': 'border-color:#5C8BFF',
}


def _css_oscuro():
    out = ['@media (prefers-color-scheme:dark){']
    for k, v in {**OSCURO_COLOR, **OSCURO_FONDO}.items():
        out.append('.%s{%s}' % (k, ';'.join(d + '!important' for d in v.split(';'))))
    out.append('.o-btn{background-color:#5C8BFF!important;background-image:linear-gradient(135deg,#5C8BFF 0%,#36CFE0 100%)!important;color:#0B0D12!important}')
    out.append('.o-solo-claro{display:none!important}')
    out.append('.o-solo-oscuro{display:block!important;max-height:none!important;overflow:visible!important}')
    out.append('}')
    for k, v in OSCURO_COLOR.items():
        out.append('[data-ogsc] .%s{%s}' % (k, ';'.join(d + '!important' for d in v.split(';'))))
    for k, v in OSCURO_FONDO.items():
        out.append('[data-ogsb] .%s{%s}' % (k, ';'.join(d + '!important' for d in v.split(';'))))
    out.append('[data-ogsc] .o-btn{color:#FFFFFF!important}')
    return '\n'.join(out)


# ---------------------------------------------------------------- utilidades
def hl(texto):
    """Fragmento resaltado en Azul IA dentro de un titular sobre claro (uno por titular)."""
    return '<span class="o-hl" style="color:%s;">%s</span>' % (C['a500'], texto)


def hl_oscuro(texto):
    """Fragmento resaltado dentro de un titular sobre fondo oscuro."""
    return '<span style="color:%s;">%s</span>' % (C['a400'], texto)


def enlace(texto, url, oscuro=False):
    col = C['a300'] if oscuro else C['a600']
    cls = '' if oscuro else ' class="o-link o-link-u"'
    return '<a href="%s" target="_blank"%s style="color:%s;text-decoration:underline;">%s</a>' % (url, cls, col, texto)


def b(texto):
    return '<strong style="font-weight:700;">%s</strong>' % texto


def html_a_texto(s):
    """Convierte el HTML en línea de un bloque en texto plano legible."""
    s = re.sub(r'<br\s*/?>', '\n', s)

    def _a(m):
        url, txt = m.group(1), re.sub('<[^>]+>', '', m.group(2)).strip()
        clean = re.sub(r'^(https?://|mailto:)', '', url).rstrip('/')
        if txt.rstrip('/') in (url, clean) or clean.endswith(txt.rstrip('/')):
            return clean if url.startswith('mailto:') else url
        return '%s (%s)' % (txt, clean if url.startswith('mailto:') else url)
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', _a, s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = _html.unescape(s).replace(' ', ' ')
    return re.sub(r'[ \t]+', ' ', s).strip()


def _bloque(nombre, html, txt):
    tag = nombre.upper()
    return {'html': '\n<!-- ▸ BLOQUE · %s -->\n%s\n<!-- ◂ FIN · %s -->' % (tag, html.strip(), tag), 'txt': txt}


def _fila(inner, pad='0 %dpx 16px' % PX, extra='', cls='o-px'):
    return '<tr><td class="%s" style="padding:%s;%s">%s</td></tr>' % (cls, pad, extra, inner)


# Etiqueta (eyebrow, rótulos de tarjeta, claves): tipo frase, Manrope 600, 14 px, sin tracking ni mayúsculas.
ETIQUETA = 'font-family:%s;font-size:14px;line-height:20px;font-weight:600;' % F_TEXT


def _eyebrow_html(texto, oscuro=False, nodo=True, margen='0 0 16px'):
    col = C['g400'] if oscuro else C['g500']
    cls = '' if oscuro else ' class="o-t3"'
    node = ''
    if nodo:
        ncol = C['l500'] if oscuro else C['l600']
        ncls = '' if oscuro else ' class="o-node"'
        node = '<span%s style="color:%s;font-size:10px;">&#9679;</span>&nbsp;&nbsp;' % (ncls, ncol)
    return '<p%s style="margin:%s;%scolor:%s;">%s%s</p>' % (cls, margen, ETIQUETA, col, node, texto)


# ---------------------------------------------------------------- bloques de marca
def cabecera(etiqueta='', variante='oscuro', url='https://oryzz.com'):
    """Banda superior con el logo. variante: 'oscuro' (Oryzz) · 'tap' (Oryzz Tap, expresión clara)."""
    tag = ''
    if etiqueta:
        col = C['g400']
        tag = '<td align="right" valign="middle" style="%scolor:%s;">%s</td>' % (ETIQUETA, col, etiqueta)
    if variante == 'tap':
        logo = ('<a href="%s" target="_blank" style="text-decoration:none;">'
                '<img class="o-solo-claro" src="%soryzz-tap-logo_sobre-claro.png" width="150" height="28" alt="Oryzz Tap" '
                'style="display:block;width:150px;height:28px;border:0;font-family:Arial,sans-serif;font-size:18px;font-weight:700;color:#0B0D12;">'
                '<!--[if !mso]><!--><div class="o-solo-oscuro" style="display:none;max-height:0;overflow:hidden;mso-hide:all;">'
                '<img src="%soryzz-tap-logo_sobre-oscuro.png" width="150" height="28" alt="Oryzz Tap" '
                'style="display:block;width:150px;height:28px;border:0;"></div><!--<![endif]--></a>' % (url, ASSETS, ASSETS))
        td = ('<td class="o-px o-hdr o-hdr-claro" style="background-color:#FFFFFF;border-bottom:1px solid %s;'
              'border-radius:16px 16px 0 0;padding:26px %dpx 24px;">' % (C['g100'], PX))
    else:
        logo = ('<a href="%s" target="_blank" style="text-decoration:none;">'
                '<img src="%soryzz-logo_sobre-oscuro.png" width="112" height="28" alt="Oryzz" '
                'style="display:block;width:112px;height:28px;border:0;font-family:Arial,sans-serif;font-size:18px;font-weight:700;color:#FFFFFF;"></a>'
                % (url, ASSETS))
        td = ('<td class="o-px o-hdr" bgcolor="#0B0D12" style="background-color:#0B0D12;border-radius:16px 16px 0 0;'
              'padding:28px %dpx 26px;">' % PX)
    html = ('<tr>%s<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0"><tr>'
            '<td valign="middle">%s</td>%s</tr></table></td></tr>' % (td, logo, tag))
    marca = 'Oryzz Tap' if variante == 'tap' else 'Oryzz'
    return _bloque('cabecera', html, marca + (' · ' + etiqueta if etiqueta else '') + '\n')


def hero_oscuro(eyebrow, titulo, lead='', imagen='orbita-hero.png', alt=''):
    """Continúa la banda oscura de la cabecera con titular, entradilla y órbita decorativa (se oculta en móvil)."""
    txt_lead = ('<p style="margin:16px 0 0;font-family:%s;font-size:17px;line-height:27px;color:%s;">%s</p>'
                % (F_TEXT, C['g200'], lead)) if lead else ''
    img = ''
    if imagen:
        img = ('<td class="o-hide-m" width="168" valign="bottom" align="right" style="width:168px;">'
               '<img src="%s%s" width="168" height="168" alt="%s" style="display:block;width:168px;height:168px;border:0;"></td>'
               % (ASSETS, imagen, alt))
    html = ('<tr><td class="o-px" bgcolor="#0B0D12" style="background-color:#0B0D12;padding:12px %dpx 40px;">'
            '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0"><tr>'
            '<td class="o-stack" valign="bottom" style="padding-right:8px;">%s'
            '<h1 class="o-h1-hero" style="margin:0;font-family:%s;font-size:34px;line-height:38px;font-weight:700;letter-spacing:-1px;color:#FFFFFF;">%s</h1>'
            '%s</td>%s</tr></table></td></tr>'
            % (PX, _eyebrow_html(eyebrow, oscuro=True), F_DISPLAY, titulo, txt_lead, img))
    tt = html_a_texto(titulo)
    t = '%s\n\n%s\n%s\n' % (html_a_texto(eyebrow), tt, '=' * min(len(tt), 60))
    if lead:
        t += '\n' + html_a_texto(lead) + '\n'
    return _bloque('hero oscuro', html, t)


def espacio(alto=24):
    html = ('<tr><td aria-hidden="true" style="height:%dpx;font-size:0;line-height:0;mso-line-height-rule:exactly;">&nbsp;</td></tr>' % alto)
    return {'html': html, 'txt': ''}


def eyebrow(texto, nodo=True):
    return _bloque('eyebrow', _fila(_eyebrow_html(texto, nodo=nodo, margen='0')), html_a_texto(texto) + '\n')


def titular(texto, nivel=1, margen_inf=16):
    """nivel 1 = titular principal (34 px) · nivel 2 = subtítulo de sección (22 px)."""
    if nivel == 1:
        h = ('<h1 class="o-h1 o-t1" style="margin:0;font-family:%s;font-size:34px;line-height:38px;font-weight:700;'
             'letter-spacing:-1px;color:%s;">%s</h1>' % (F_DISPLAY, C['g950'], texto))
        tt = html_a_texto(texto)
        t = tt + '\n' + '=' * min(len(tt), 60) + '\n'
    else:
        h = ('<h2 class="o-h2 o-t1" style="margin:0;font-family:%s;font-size:22px;line-height:28px;font-weight:600;'
             'letter-spacing:-0.4px;color:%s;">%s</h2>' % (F_DISPLAY, C['g950'], texto))
        tt = html_a_texto(texto)
        t = tt + '\n' + '-' * min(len(tt), 60) + '\n'
    return _bloque('titular', _fila(h, pad='0 %dpx %dpx' % (PX, margen_inf)), t)


def parrafo(texto, lead=False, pequeno=False, margen_inf=16, alinear='left'):
    if lead:
        size, lh, cls = 18, 28, 'o-lead o-t2'
    elif pequeno:
        size, lh, cls = 14, 22, 'o-t3'
    else:
        size, lh, cls = 16, 26, 'o-t2'
    col = C['g500'] if pequeno else C['g600']
    p = ('<p class="%s" style="margin:0;font-family:%s;font-size:%dpx;line-height:%dpx;color:%s;text-align:%s;">%s</p>'
         % (cls, F_TEXT, size, lh, col, alinear, texto))
    return _bloque('párrafo', _fila(p, pad='0 %dpx %dpx' % (PX, margen_inf)), html_a_texto(texto) + '\n')


def boton(texto, url, ancho_vml=None, margen='8px %dpx 28px' % PX):
    """Botón «bulletproof»: VML en Outlook Windows, <a> con padding en el resto. Un solo botón por correo."""
    w = ancho_vml or int(len(texto) * 9.4 + 60)
    vml = ('<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" '
           'href="%s" style="height:50px;v-text-anchor:middle;width:%dpx;" arcsize="20%%" stroke="f" fillcolor="#2C5BD0">'
           '<w:anchorlock/><center style="color:#FFFFFF;font-family:Arial,sans-serif;font-size:16px;font-weight:bold;">%s</center>'
           '</v:roundrect><![endif]-->' % (url, w, texto))
    a = ('<!--[if !mso]><!--><a href="%s" target="_blank" class="o-btn" style="background-color:#2C5BD0;border-radius:10px;'
         'color:#FFFFFF;display:inline-block;font-family:%s;font-size:16px;font-weight:700;line-height:50px;'
         'text-align:center;text-decoration:none;padding:0 28px;-webkit-text-size-adjust:none;mso-hide:all;">%s</a><!--<![endif]-->'
         % (url, F_TEXT, texto))
    tbl = ('<table role="presentation" class="o-btn-tbl" cellspacing="0" cellpadding="0" border="0"><tr><td>%s%s</td></tr></table>'
           % (vml, a))
    return _bloque('botón', _fila(tbl, pad=margen), '%s: %s\n' % (html_a_texto(texto).rstrip(' →'), url))


def separador(margen='8px %dpx 24px' % PX):
    s = ('<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"><tr>'
         '<td class="o-bd" style="border-top:1px solid #E5E8EE;font-size:0;line-height:0;height:1px;">&nbsp;</td></tr></table>')
    return _bloque('separador', _fila(s, pad=margen), '―' * 24 + '\n')


def lista(items, estilo='nodo', margen_inf=16):
    """estilo 'nodo' (punto azul, por defecto) o 'guion' (– en azul). Sin números (BRAND_SPEC §4).
    'num' se acepta como alias de 'nodo'. Los items admiten <strong> y enlaces."""
    rows, txt = [], []
    for it in items:
        if estilo == 'guion':
            mark = '<span style="font-size:16px;line-height:26px;">&ndash;</span>'
        else:
            mark = '<span style="font-size:10px;line-height:26px;">&#9679;</span>'
        rows.append('<tr><td class="o-num" width="28" valign="top" style="width:28px;padding:0 0 12px;font-family:%s;'
                    'font-size:16px;line-height:26px;color:%s;">%s</td>'
                    '<td class="o-t2" valign="top" style="padding:0 0 12px;font-family:%s;font-size:16px;line-height:26px;color:%s;">%s</td></tr>'
                    % (F_TEXT, C['a600'], mark, F_TEXT, C['g600'], it))
        txt.append('- ' + html_a_texto(it))
    t = ('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0">%s</table>' % ''.join(rows))
    return _bloque('lista', _fila(t, pad='0 %dpx %dpx' % (PX, max(0, margen_inf - 12))), '\n'.join(txt) + '\n')


def cita(texto, autor=''):
    au = ('<p class="o-t3" style="margin:12px 0 0;%scolor:%s;">%s</p>' % (ETIQUETA, C['g500'], autor)) if autor else ''
    q = ('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0"><tr>'
         '<td class="o-quote" style="border-left:3px solid %s;padding:4px 0 4px 20px;">'
         '<p class="o-t1" style="margin:0;font-family:%s;font-size:20px;line-height:28px;font-weight:500;letter-spacing:-0.3px;color:%s;">%s</p>%s'
         '</td></tr></table>' % (C['a500'], F_DISPLAY, C['g950'], texto, au))
    t = '> «%s»' % html_a_texto(texto).strip('«»') + ('\n> — %s' % html_a_texto(autor) if autor else '')
    return _bloque('cita', _fila(q, pad='8px %dpx 24px' % PX), t + '\n')


def imagen(src, alt, ancho=518, alto=None, href=None, radio=12, margen='0 %dpx 24px' % PX):
    """Imagen a ancho de columna (518 px en escritorio, fluida en móvil). `alt` obligatorio y descriptivo."""
    h_attr = ' height="%d"' % alto if alto else ''
    img = ('<img class="o-img" src="%s%s" width="%d"%s alt="%s" style="display:block;width:%dpx;max-width:100%%;height:auto;'
           'border:0;border-radius:%dpx;font-family:%s;font-size:14px;color:%s;">'
           % (ASSETS, src, ancho, h_attr, alt, ancho, radio, F_TEXT, C['g500']))
    if href:
        img = '<a href="%s" target="_blank">%s</a>' % (href, img)
    return _bloque('imagen', _fila(img, pad=margen), '[Imagen: %s]\n' % alt)


def detalles(filas, margen='0 %dpx 24px' % PX):
    """Tarjeta de datos clave/valor (cita, pedido, propuesta). filas = [(clave, valor_html), ...]."""
    rows, txt = [], []
    for i, (k, v) in enumerate(filas):
        bt = '' if i == 0 else 'border-top:1px solid #E5E8EE;'
        rows.append('<tr><td class="o-bd o-t3 o-dl-k" width="150" valign="top" style="width:150px;%spadding:14px 12px 14px 20px;'
                    'font-family:%s;font-size:14px;line-height:22px;font-weight:600;color:%s;">%s</td>'
                    '<td class="o-bd o-t1" valign="top" style="%spadding:14px 20px 14px 0;font-family:%s;font-size:16px;line-height:22px;'
                    'font-weight:600;color:%s;">%s</td></tr>' % (bt, F_TEXT, C['g500'], k, bt, F_TEXT, C['g950'], v))
        txt.append('%s: %s' % (html_a_texto(k), html_a_texto(v)))
    t = ('<table role="presentation" class="o-bg-surface" width="100%%" cellspacing="0" cellpadding="0" border="0" '
         'style="background-color:%s;border-radius:14px;border-collapse:separate;">%s</table>' % (C['g50'], ''.join(rows)))
    return _bloque('detalles', _fila(t, pad=margen), '\n'.join(txt) + '\n')


def tarjetas_dato(items, eyebrow_txt='', margen='0 %dpx 28px' % PX):
    """Tarjetas dato sobre banda Grafito 950 (firma visual de marca). items = [dict(etiqueta, valor, delta, tono)].
    tono: 'bueno' (lima) o 'neutro' (titanio). Siempre 2 por fila, también en móvil."""
    cells, txt = [], []
    for it in items:
        dcol = C['l500'] if it.get('tono', 'bueno') == 'bueno' else C['g400']
        cells.append('<td class="o-kpi-td" width="50%%" valign="top" bgcolor="#12151D" style="width:50%%;background-color:#12151D;'
                     'border:1px solid #232836;border-radius:14px;padding:20px 20px 18px;">'
                     '<p style="margin:0 0 10px;%scolor:%s;">%s</p>'
                     '<p class="o-kpi" style="margin:0;font-family:%s;font-size:36px;line-height:40px;font-weight:500;letter-spacing:-1px;color:#FFFFFF;">%s</p>'
                     '<p style="margin:8px 0 0;font-family:%s;font-size:14px;line-height:20px;font-weight:600;color:%s;">%s</p></td>'
                     % (ETIQUETA, C['g400'], it['etiqueta'], F_DISPLAY, it['valor'], F_TEXT, dcol, it.get('delta', '&nbsp;')))
        txt.append('- %s: %s (%s)' % (html_a_texto(it['etiqueta']), html_a_texto(it['valor']), html_a_texto(it.get('delta', ''))))
    rows = ''.join('<tr>%s</tr>' % ''.join(cells[i:i + 2]) for i in range(0, len(cells), 2))
    eb = ''
    if eyebrow_txt:
        eb = '<tr><td style="padding:14px 14px 2px;">%s</td></tr>' % _eyebrow_html(eyebrow_txt, oscuro=True, margen='0')
    t = ('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" bgcolor="#0B0D12" '
         'style="background-color:#0B0D12;border-radius:18px;border-collapse:separate;">%s<tr><td style="padding:4px;">'
         '<table role="presentation" width="100%%" cellspacing="10" cellpadding="0" border="0" style="border-collapse:separate;">%s</table>'
         '</td></tr></table>' % (eb, rows))
    head = (html_a_texto(eyebrow_txt) + '\n') if eyebrow_txt else ''
    return _bloque('tarjetas dato', _fila(t, pad=margen), head + '\n'.join(txt) + '\n')


def pasos(items, iconos=None, margen_inf=12):
    """Pasos con icono PNG 48 px o con nodo azul; se distinguen por su título, nunca por un número (BRAND_SPEC §4).
    items = [dict(titulo, texto, cuando?, extra_html?)]. `cuando` es un rótulo temporal opcional («Hoy», «Días 2–3»).
    iconos = lista de nombres base: se usan assets/<nombre>_claro.png y _oscuro.png."""
    rows, txt = [], []
    for i, it in enumerate(items, 1):
        if iconos:
            n = iconos[i - 1]
            mark = ('<img class="o-solo-claro" src="%sicono-%s_claro.png" width="48" height="48" alt="" style="display:block;width:48px;height:48px;border:0;">'
                    '<!--[if !mso]><!--><div class="o-solo-oscuro" style="display:none;max-height:0;overflow:hidden;mso-hide:all;">'
                    '<img src="%sicono-%s_oscuro.png" width="48" height="48" alt="" style="display:block;width:48px;height:48px;border:0;"></div><!--<![endif]-->'
                    % (ASSETS, n, ASSETS, n))
            mtd = '<td width="64" valign="top" style="width:64px;padding:0 0 20px;">%s</td>' % mark
        else:
            mtd = ('<td class="o-num" width="28" valign="top" style="width:28px;padding:0 0 20px;font-family:%s;font-size:10px;'
                   'line-height:24px;color:%s;">&#9679;</td>' % (F_TEXT, C['a600']))
        etiqueta = _eyebrow_html(it['cuando'], nodo=False, margen='0 0 4px') if it.get('cuando') else ''
        extra = it.get('extra_html', '')
        rows.append('<tr>%s<td valign="top" style="padding:0 0 20px;">%s'
                    '<p class="o-t1" style="margin:0 0 4px;font-family:%s;font-size:18px;line-height:24px;font-weight:600;letter-spacing:-0.2px;color:%s;">%s</p>'
                    '<p class="o-t2" style="margin:0;font-family:%s;font-size:16px;line-height:25px;color:%s;">%s</p>%s</td></tr>'
                    % (mtd, etiqueta, F_DISPLAY, C['g950'], it['titulo'], F_TEXT, C['g600'], it['texto'], extra))
        pre = ('[%s] ' % html_a_texto(it['cuando'])) if it.get('cuando') else ''
        txt.append('- %s%s\n  %s' % (pre, html_a_texto(it['titulo']), html_a_texto(it['texto'])))
        if it.get('extra_txt'):
            txt.append('  ' + it['extra_txt'])
    t = '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0">%s</table>' % ''.join(rows)
    return _bloque('pasos', _fila(t, pad='4px %dpx %dpx' % (PX, margen_inf)), '\n'.join(txt) + '\n')


def seccion(titulo, parrafos, enlace_html=''):
    """Bloque editorial (newsletter): nodo azul a la izquierda, titular y texto a la derecha. Sin números."""
    ps = ''.join('<p class="o-t2" style="margin:0 0 14px;font-family:%s;font-size:16px;line-height:26px;color:%s;">%s</p>'
                 % (F_TEXT, C['g600'], p) for p in parrafos)
    if enlace_html:
        ps += '<p style="margin:0 0 14px;font-family:%s;font-size:16px;line-height:26px;font-weight:700;">%s</p>' % (F_TEXT, enlace_html)
    t = ('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0"><tr>'
         '<td class="o-bd" colspan="2" style="border-top:1px solid #E5E8EE;font-size:0;line-height:0;height:1px;">&nbsp;</td></tr><tr>'
         '<td class="o-num" width="28" valign="top" style="width:28px;padding:20px 0 0;font-family:%s;font-size:10px;line-height:28px;color:%s;">&#9679;</td>'
         '<td valign="top" style="padding:20px 0 0;">'
         '<h2 class="o-h2 o-t1" style="margin:0 0 12px;font-family:%s;font-size:22px;line-height:28px;font-weight:600;letter-spacing:-0.4px;color:%s;">%s</h2>%s</td>'
         '</tr></table>' % (F_TEXT, C['a600'], F_DISPLAY, C['g950'], titulo, ps))
    tt = html_a_texto(titulo)
    txt = tt + '\n' + '-' * min(len(tt), 60) + '\n' + '\n\n'.join(html_a_texto(p) for p in parrafos)
    if enlace_html:
        txt += '\n\n' + html_a_texto(enlace_html)
    return _bloque('sección', _fila(t, pad='0 %dpx 12px' % PX), txt + '\n')


def personas(lista_p, margen='0 %dpx 24px' % PX):
    """Tarjetas de contacto del equipo (2 columnas, se apilan en móvil). lista_p = [(nombre, rol, email)]."""
    cells = []
    for i, (n, r, e) in enumerate(lista_p):
        gap = 'padding:0 6px 0 0;' if i % 2 == 0 else 'padding:0 0 0 6px;'
        cells.append('<td class="o-stack o-stack-gap" width="50%%" valign="top" style="width:50%%;%s">'
                     '<table role="presentation" class="o-bg-surface" width="100%%" cellspacing="0" cellpadding="0" border="0" '
                     'style="background-color:%s;border-radius:14px;border-collapse:separate;"><tr><td style="padding:18px 20px;">'
                     '<p class="o-t1" style="margin:0;font-family:%s;font-size:18px;line-height:24px;font-weight:600;color:%s;">%s</p>'
                     '<p class="o-t3" style="margin:2px 0 8px;font-family:%s;font-size:14px;line-height:20px;color:%s;">%s</p>'
                     '<p style="margin:0;font-family:%s;font-size:14px;line-height:20px;">%s</p></td></tr></table></td>'
                     % (gap, C['g50'], F_DISPLAY, C['g950'], n, F_TEXT, C['g500'], r, F_TEXT, enlace(e, 'mailto:' + e)))
    t = ('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0"><tr>%s</tr></table>' % ''.join(cells))
    txt = '\n'.join('- %s (%s): %s' % (n, r, e) for n, r, e in lista_p)
    return _bloque('personas', _fila(t, pad=margen), txt + '\n')


def codigo(texto, etiqueta=''):
    """Caja para códigos o formatos (p. ej. código de activación): rótulo en Manrope, código en mono (dato técnico).
    Devuelve HTML en línea para `extra_html`."""
    et = ('<span class="o-t3" style="%scolor:%s;">%s&nbsp;&nbsp;</span>' % (ETIQUETA, C['g500'], etiqueta)) if etiqueta else ''
    return ('<table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin-top:12px;"><tr>'
            '<td class="o-bg-surface o-bd" style="background-color:%s;border:1px solid %s;border-radius:10px;padding:10px 16px;">%s'
            '<span class="o-t1" style="font-family:%s;font-size:18px;line-height:24px;font-weight:500;letter-spacing:3px;color:%s;">%s</span></td></tr></table>'
            % (C['g50'], C['g100'], et, F_MONO, C['g950'], texto))


def despedida(saludo='Un saludo,', nombre='Juan Salazar', rol='Estrategia &amp; Ads · Oryzz', margen='8px %dpx 36px' % PX):
    h = ('<p class="o-t2" style="margin:0 0 6px;font-family:%s;font-size:16px;line-height:26px;color:%s;">%s</p>'
         '<p class="o-t1" style="margin:0;font-family:%s;font-size:17px;line-height:24px;font-weight:600;color:%s;">%s</p>'
         '<p class="o-t3" style="margin:0;font-family:%s;font-size:14px;line-height:22px;color:%s;">%s</p>'
         % (F_TEXT, C['g600'], saludo, F_DISPLAY, C['g950'], nombre, F_TEXT, C['g500'], rol))
    return _bloque('despedida', _fila(h, pad=margen), '%s\n%s\n%s\n' % (html_a_texto(saludo), html_a_texto(nombre), html_a_texto(rol)))


def pie(marca='oryzz', motivo='', baja=False, direccion=False):
    """Pie fuera de la tarjeta. `baja=True` añade el enlace de baja {{baja_url}} (obligatorio en newsletter)."""
    if marca == 'tap':
        firma = 'Oryzz Tap · Tu negocio. A un toque.'
        links = [('oryzz.com/tap', 'https://oryzz.com/tap'), ('Instagram', 'https://instagram.com/oryzztap'),
                 ('TikTok', 'https://www.tiktok.com/@oryzz.tap'), ('pedidos@oryzz.com', 'mailto:pedidos@oryzz.com')]
    else:
        firma = 'Oryzz · Sistemas que captan clientes.'
        links = [('oryzz.com', 'https://oryzz.com'), ('Instagram', 'https://instagram.com/oryzzai'),
                 ('LinkedIn', 'https://www.linkedin.com/company/oryzz')]
    st = 'font-family:%s;font-size:14px;line-height:22px;color:%s;' % (F_TEXT, C['g500'])
    lk = ' &nbsp;·&nbsp; '.join('<a href="%s" target="_blank" class="o-t3" style="color:%s;text-decoration:underline;">%s</a>'
                                % (u, C['g600'], t) for t, u in links)
    partes = ['<p class="o-t1" style="margin:0 0 6px;font-family:%s;font-size:15px;line-height:22px;font-weight:600;color:%s;">%s</p>'
              % (F_DISPLAY, C['g950'], firma),
              '<p class="o-t3" style="margin:0 0 14px;%s">%s</p>' % (st, lk)]
    txt = [firma, ' · '.join('%s: %s' % (t, u.replace('mailto:', '')) if t != u.replace('mailto:', '').replace('https://', '') else t
                            for t, u in links)]
    if motivo:
        partes.append('<p class="o-t3" style="margin:0 0 6px;%s">%s</p>' % (st, motivo))
        txt.append(html_a_texto(motivo))
    if baja:
        partes.append('<p class="o-t3" style="margin:0 0 6px;%s">¿Prefieres no recibir más estas notas? '
                      '<a href="{{baja_url}}" target="_blank" class="o-t3" style="color:%s;text-decoration:underline;">Darte de baja</a> '
                      'es inmediato.</p>' % (st, C['g600']))
        txt.append('Darte de baja: {{baja_url}}')
    if direccion:
        partes.append('<p class="o-t3" style="margin:0;%s">{{direccion_postal}}</p>' % st)
        txt.append('{{direccion_postal}}')
    html = ('<tr><td class="o-px" style="padding:28px %dpx 12px;">%s</td></tr>' % (PX, ''.join(partes)))
    return _bloque('pie', html, '\n'.join(txt) + '\n')


# ---------------------------------------------------------------- documento
def _preheader(texto):
    if not texto:
        return ''
    relleno = '&#847;&zwnj;&nbsp;' * 90
    return ('<div class="o-preheader" style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;'
            'overflow:hidden;mso-hide:all;color:#F6F7F9;">%s%s</div>' % (texto, relleno))


def _cabecera_html(asunto, lang='es'):
    return ('<!DOCTYPE html>\n<html lang="%s" dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" '
            'xmlns:o="urn:schemas-microsoft-com:office:office">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta http-equiv="X-UA-Compatible" content="IE=edge">\n'
            '<meta name="x-apple-disable-message-reformatting">\n'
            '<meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no">\n'
            '<meta name="color-scheme" content="light dark">\n<meta name="supported-color-schemes" content="light dark">\n'
            '<title>%s</title>\n' % (lang, _html.escape(asunto)))


def documento(asunto, preheader, bloques, comentario='', idioma='es'):
    """Ensambla un correo de marca completo. Devuelve (html, txt)."""
    cuerpo = [bl for bl in bloques if bl.get('zona', 'tarjeta') == 'tarjeta']
    fuera = [bl for bl in bloques if bl.get('zona') == 'fuera']
    head = _cabecera_html(asunto, idioma)
    head += ('<!--[if mso]>\n<noscript><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch>'
             '</o:OfficeDocumentSettings></xml></noscript>\n'
             '<style>table,td,div,h1,h2,h3,p,a,span,li{font-family:Arial,Helvetica,sans-serif!important;}'
             'h1,h2,h3,p{mso-line-height-rule:exactly;}</style>\n<![endif]-->\n'
             '<!--[if !mso]><!-->\n<link rel="preconnect" href="https://fonts.gstatic.com">\n'
             '<link href="%s" rel="stylesheet" type="text/css">\n<!--<![endif]-->\n' % GOOGLE_FONTS.replace('&', '&amp;'))
    head += '<style type="text/css">%s</style>\n' % CSS_BASE
    head += '<style type="text/css">%s</style>\n' % CSS_MOVIL
    head += '<style type="text/css">\n%s\n</style>\n</head>\n' % _css_oscuro()
    card_rows = '\n'.join(bl['html'] for bl in cuerpo)
    fuera_rows = '\n'.join(bl['html'] for bl in fuera)
    body = ('<body class="body o-bg-page" style="margin:0;padding:0;background-color:%s;word-spacing:normal;">\n'
            '<div role="article" aria-roledescription="email" aria-label="%s" lang="%s" dir="ltr" class="o-bg-page" '
            'style="background-color:%s;-webkit-text-size-adjust:100%%;-ms-text-size-adjust:100%%;">\n%s\n'
            '<table role="presentation" class="o-bg-page" width="100%%" cellspacing="0" cellpadding="0" border="0" bgcolor="#F6F7F9" style="background-color:%s;">\n'
            '<tr><td class="o-outer" align="center" style="padding:32px 32px 24px;">\n'
            '<!--[if mso]><table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center"><tr><td><![endif]-->\n'
            '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" style="max-width:600px;width:100%%;">\n'
            '<tr><td>\n<table role="presentation" class="o-card" width="100%%" cellspacing="0" cellpadding="0" border="0" bgcolor="#FFFFFF" '
            'style="background-color:#FFFFFF;border:1px solid %s;border-radius:16px;border-collapse:separate;">\n%s\n</table>\n</td></tr>\n'
            '%s\n</table>\n<!--[if mso]></td></tr></table><![endif]-->\n</td></tr>\n</table>\n</div>\n</body>\n</html>\n'
            % (C['g50'], _html.escape(asunto), idioma, C['g50'], _preheader(preheader), C['g50'], C['g100'], card_rows, fuera_rows))
    html = head + body
    if comentario:
        html = html.replace('<head>\n', '<head>\n<!--\n%s\n-->\n' % comentario, 1)
    txt = '\n'.join(bl['txt'] for bl in bloques if bl['txt']).strip() + '\n'
    txt = re.sub(r'\n{3,}', '\n\n', txt)
    return html, txt


def fuera(bloque):
    """Marca un bloque para que vaya fuera de la tarjeta blanca (p. ej. el pie)."""
    bloque = dict(bloque)
    bloque['zona'] = 'fuera'
    return bloque


# ---------------------------------------------------------------- correos 1 a 1 (casi texto plano)
def documento_1a1(asunto, parrafos, firma_lineas, comentario=''):
    """Correo personal: sin imágenes, sin botones, sin preheader oculto, tipografía del sistema.
    Imita un correo escrito a mano en Gmail para que no parezca publicidad (entregabilidad)."""
    ps = []
    for p in parrafos:
        ps.append('<p style="margin:0 0 14px;">%s</p>' % p)
    firma = '<br>'.join(firma_lineas)
    html = _cabecera_html(asunto)
    html += ('<style type="text/css">body{margin:0;padding:0}a{color:#2C5BD0}'
             '@media (prefers-color-scheme:dark){a{color:#9FB8FF!important}}</style>\n</head>\n'
             '<body style="margin:0;padding:0;">\n'
             '<div dir="ltr" style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;max-width:600px;padding:16px 16px 24px;">\n'
             '%s\n<p style="margin:18px 0 0;">%s</p>\n</div>\n</body>\n</html>\n' % ('\n'.join(ps), firma))
    if comentario:
        html = html.replace('<head>\n', '<head>\n<!--\n%s\n-->\n' % comentario, 1)
    txt = '\n\n'.join(html_a_texto(p) for p in parrafos) + '\n\n' + '\n'.join(html_a_texto(l) for l in firma_lineas) + '\n'
    return html, txt


def marcadores(s):
    return sorted(set(re.findall(r'\{\{\s*([A-Za-z0-9_]+)\s*\}\}', s)))
