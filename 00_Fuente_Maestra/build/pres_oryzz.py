"""
Oryzz · plantillas de presentación (oscura / clara) + deck comercial de ejemplo.

    python pres_oryzz.py            -> genera .pptx (sin post-proceso) + HTML/PDF de previsualización
Post-proceso con PowerPoint (incrustar fuentes y exportar PNG): pres_powerpoint.ps1 (lo llama pres_build_all.py)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pres_engine import *          # noqa
from pres_assets import (svg_png, logo_png, orbit_system, svg_doc, grid_svg, halo_svg, rounded_route, html_png, ROOT)

OUT = os.path.join(ROOT, '06_Presentaciones')
RES = os.path.join(OUT, '_recursos')

# ---------------------------------------------------------------- retícula 12 col · 1920x1080 · margen 120 · gutter 32
M = 120
GUT = 32
COLW = (W - 2 * M - 11 * GUT) / 12      # 110,67 px


def col(i):
    return round(M + i * (COLW + GUT), 2)


def span(n):
    return round(n * COLW + (n - 1) * GUT, 2)


RIGHT = W - M

# ---------------------------------------------------------------- paletas
DARK = dict(bg='#0B0D12', surf='#12151D', surf2='#171B25', border='#232836', text='#FFFFFF', text2='#D5D9E0', text3='#8A90A0',
            hl='#5C8BFF', accent='#3B72FF', node='#BFF24A', delta='#BFF24A', grad=('#5C8BFF', '#36CFE0'),
            cta_fill=None, cta_text='#0B0D12', orbit='#262B3A', link='#9FB8FF', chart_main='#5C8BFF', chart_muted='#3A4152',
            ph_bg='#171B25', ph_label='#5A6172', on_photo='#FFFFFF', on_photo2='#D5D9E0')
LIGHT = dict(bg='#FFFFFF', surf='#F6F7F9', surf2='#E5E8EE', border='#D5D9E0', text='#0B0D12', text2='#3A4152', text3='#5A6172',
             hl='#3B72FF', accent='#2C5BD0', node='#7FB02E', delta='#3A4A12', grad=('#3B72FF', '#17A9C2'),
             cta_fill='#2C5BD0', cta_text='#FFFFFF', orbit='#D5D9E0', link='#2C5BD0', chart_main='#3B72FF', chart_muted='#D5D9E0',
             ph_bg='#E5E8EE', ph_label='#8A90A0', on_photo='#FFFFFF', on_photo2='#E5E8EE')

ACCENTS = dict(accent1='#3B72FF', accent2='#36CFE0', accent3='#BFF24A', accent4='#2C5BD0', accent5='#8A90A0', accent6='#7FB02E')


def make_theme(dark, footer_text='Oryzz · Sistemas que captan clientes', lang='es-ES', name=None):
    c = DARK if dark else LIGHT
    scheme = dict(dk1='#0B0D12', lt1='#FFFFFF', **ACCENTS)
    if dark:
        scheme.update(dk2='#12151D', lt2='#D5D9E0')
    else:
        scheme.update(dk2='#3A4152', lt2='#F6F7F9')
    fs = dict(font='text_med', size=12, color=c['text3'], lh=1.0, align='l')
    ns = dict(font='text_med', size=12, color=c['text3'], lh=1.0, align='r')
    return Theme('oscuro' if dark else 'claro', name or ('Oscuro' if dark else 'Claro'), dark, c, scheme,
                 hlink='#9FB8FF' if dark else '#2C5BD0', folhlink='#5C8BFF' if dark else '#1F43A0',
                 footer_style=fs, number_style=ns, footer_text=footer_text, lang=lang)


def styles(c):
    return dict(
        eyebrow=dict(font='text_semi', size=14, color=c['text3'], lh=1.0),  # tipo frase, sin tracking (BRAND_SPEC §4)
        title=dict(font='display', size=44, color=c['text'], spc=-0.035, lh=1.04, hl_color=c['hl']),
        title_l=dict(font='display', size=80, color=c['text'], spc=-0.042, lh=0.98, hl_color=c['hl']),
        cover=dict(font='display', size=96, color=c['text'], spc=-0.048, lh=0.94, hl_color=c['hl']),
        h3=dict(font='display', size=28, color=c['text'], spc=-0.02, lh=1.15, hl_color=c['hl']),
        h4=dict(font='display', size=24, color=c['text'], spc=-0.015, lh=1.2),
        lead=dict(font='text', size=24, color=c['text2'], lh=1.42),
        body=dict(font='text', size=20, color=c['text2'], lh=1.5),
        body18=dict(font='text', size=18, color=c['text2'], lh=1.5),
        small=dict(font='text', size=18, color=c['text3'], lh=1.45),
        num=dict(font='display_med', size=96, color=c['text'], spc=-0.04, lh=1.0),
        delta=dict(font='text_semi', size=15, color=c['delta'], lh=1.2),
        meta=dict(font='text_med', size=12, color=c['text3'], lh=1.0),
        list=dict(font='text', size=20, color=c['text2'], lh=1.4, bullet='–', indent=34, bullet_color=c['text3'], sa=10),
    )


# ---------------------------------------------------------------- recursos
CH_X, CH_W, CH_H, CH_Y0, CH_P = 120, 380, 84, 300, 110
CH_CY = [CH_Y0 + i * CH_P + CH_H / 2 for i in range(5)]
MID = (CH_CY[0] + CH_CY[-1]) / 2
BUS_X = 572
SYS_X, SYS_W, SYS_H = 640, 680, 548
SYS_Y = MID - SYS_H / 2
NODE_X = 1440
ROUTE_Y = 476


def make_assets(theme):
    c, k = theme.c, theme.key
    dark = theme.dark
    A = {}
    A['grid'] = svg_png(os.path.join(RES, f'reticula_{k}.png'),
                        grid_svg('#FFFFFF' if dark else '#0B0D12', opacity=0.035 if dark else 0.045))
    A['grid_r'] = svg_png(os.path.join(RES, f'reticula-derecha_{k}.png'),
                          grid_svg('#FFFFFF' if dark else '#0B0D12', opacity=0.035 if dark else 0.045, cx=0.78, cy=0.45, rx=0.42, ry=0.7))
    halo = halo_svg(1600, 500, 820, '#5C8BFF', 0.13) if dark else None
    orb = dict(color=c['orbit'], accent_color=c['hl'], node_color=c['node'], sw=1.5, accent_sw=2.25)
    cover = orbit_system(1600, 500, [140, 232, 330, 438, 556, 684, 822], gap_start=-236, gap_step=57, gap=58,
                         accent_i=2, accent_span=72, node_r=11, **orb)
    A['orb_cover'] = svg_png(os.path.join(RES, f'orbitas-portada_{k}.png'),
                             svg_doc((halo[halo.index('<rect'):halo.rindex('</svg>')] if halo else '') + cover,
                                     defs=halo[halo.index('<defs>') + 6:halo.index('</defs>')] if halo else ''))
    A['orb_section'] = svg_png(os.path.join(RES, f'orbitas-seccion_{k}.png'), svg_doc(
        orbit_system(1720, 1010, [170, 290, 420, 560, 710, 870], gap_start=-222, gap_step=50, gap=56, accent_i=3,
                     accent_span=46, node_r=11, **orb)))
    A['orb_cta'] = svg_png(os.path.join(RES, f'orbitas-cta_{k}.png'), svg_doc(
        orbit_system(1560, 560, [110, 196, 290, 392, 502, 620], gap_start=-152, gap_step=61, gap=60, accent_i=2,
                     accent_span=70, node_r=11, **orb)))
    A['orb_close'] = svg_png(os.path.join(RES, f'orbitas-cierre_{k}.png'), svg_doc(
        orbit_system(1560, 560, [150, 250, 360, 480, 610, 750], gap_start=-60, gap_step=-49, gap=58, accent_i=1,
                     accent_span=60, node_r=11, **orb)))
    A['orb_arc'] = svg_png(os.path.join(RES, f'orbitas-arco_{k}.png'), svg_doc(
        orbit_system(1880, -180, [380, 530, 690, 860], gap_start=40, gap_step=-8, gap=40, accent_i=2,
                     accent_span=30, node_r=11, **orb)))
    # rutas canales -> sistema -> cliente
    body = ''
    for cy in CH_CY:
        pts = [(CH_X + CH_W, cy), (BUS_X, cy), (BUS_X, MID), (SYS_X, MID)] if abs(cy - MID) > 1 else [(CH_X + CH_W, cy), (SYS_X, MID)]
        body += f'<path d="{rounded_route(pts, 30)}" fill="none" stroke="{c["text3"] if dark else "#8A90A0"}" stroke-opacity="0.55" stroke-width="2" stroke-linecap="round"/>'
        body += f'<circle cx="{CH_X + CH_W}" cy="{cy}" r="5" fill="{c["bg"]}" stroke="{c["text3"]}" stroke-width="2"/>'
    body += f'<path d="M{SYS_X + SYS_W} {MID}H{NODE_X - 26}" stroke="{c["hl"]}" stroke-width="2.5" stroke-linecap="round"/>'
    body += f'<circle cx="{SYS_X}" cy="{MID}" r="5" fill="{c["bg"]}" stroke="{c["text3"]}" stroke-width="2"/>'
    A['routes'] = svg_png(os.path.join(RES, f'rutas-canales-sistema-cliente_{k}.png'), svg_doc(body))
    way = 'color-sobre-oscuro' if dark else 'color-sobre-claro'
    A['logo'] = logo_png(f'01_Horizontal/SVG/oryzz-logo-horizontal_{way}.svg', os.path.join(RES, f'logo-horizontal_{way}.png'), 1800)
    solid = 'solido-sobre-oscuro' if dark else 'solido-sobre-claro'
    A['iso'] = logo_png(f'04_Isotipo/SVG_tamano_pequeno/oryzz-isotipo-small_{solid}.svg', os.path.join(RES, f'isotipo-pie_{solid}.png'), 160)
    A['logo_white'] = logo_png('01_Horizontal/SVG/oryzz-logo-horizontal_mono-blanco.svg', os.path.join(RES, 'logo-horizontal_mono-blanco.png'), 1800)
    return A


LOGO_RATIO = 3456.6 / 856.1


# ---------------------------------------------------------------- layouts
def make_layouts(theme, A):
    c = theme.c
    s = styles(c)
    L = {}
    iso_footer = Img(M, FOOTER_Y, 24, 24, A['iso'], name='Isotipo pie')
    eyebrow = lambda prompt='Etiqueta', idx=10, x=M, y=M, w=1000: PH(idx, 'body', x, y, w, 34, prompt, name='Etiqueta', **s['eyebrow'])
    title = lambda x=M, y=160, w=1300, h=210, prompt='Título de la diapositiva', st='title', **kw: PH(0, 'title', x, y, w, h, prompt, **merged(s[st], kw))
    logo = lambda y=M - 8, h=44: Img(M, y, h * A.get('logo_ratio', LOGO_RATIO), h, A['logo'], name='Logo', descr=A.get('logo_descr', 'oryzz'))

    def add(name, statics=(), phs=(), footer=True, number=True, bg=None):
        st = list(statics)
        if footer:
            st.append(iso_footer)
        L[name] = Layout(name, st, phs, footer=footer, number=number, bg=bg)

    # 01 · Portada órbita
    add('Portada · Órbita', [Img(0, 0, W, H, A['grid'], name='Retícula'), Img(0, 0, W, H, A['orb_cover'], name='Órbitas'), logo()], [
        eyebrow('Propuesta · mes y año', y=388),
        title(y=432, w=1240, h=380, prompt='Titular de portada', st='cover'),
        PH(11, 'body', M, 836, 940, 130, 'Subtítulo: qué resuelve esta presentación en una frase.', name='Subtítulo', **merged(s['lead'], dict(size=22))),
        PH(12, 'body', 1000, 968, 800, 30, 'Preparado para {{Cliente}} · oryzz.com', name='Meta', **merged(s['meta'], dict(align='r'))),
    ], footer=False, number=False)

    # 02 · Portada tipográfica
    add('Portada · Tipográfica', [Img(0, 0, W, H, A['grid_r'], name='Retícula'), Img(0, 0, W, H, A['orb_arc'], name='Órbitas'), logo(),
                                     Ln(M, 836, RIGHT, 836, c['border'], 1.5, name='Filete'),
                                     T(col(0), 868, span(4), 24, 'Preparado para', name='Etiqueta 1', **s['meta']),
                                     T(col(4), 868, span(4), 24, 'Fecha', name='Etiqueta 2', **s['meta']),
                                     T(col(8), 868, span(4), 24, 'Contacto', name='Etiqueta 3', **s['meta'])], [
        eyebrow('Tipo de documento · año', x=1100, y=M + 4, w=700) if False else PH(10, 'body', 1100, M + 4, 700, 28, 'Tipo de documento · año', name='Etiqueta', **merged(s['eyebrow'], dict(align='r'))),
        title(y=290, w=1560, h=515, prompt='Titular tipográfico en dos o tres líneas', st='title_l', size=88, lh=0.95, anchor='b'),
        PH(11, 'body', col(0), 904, span(4), 60, '{{Cliente}}', name='Preparado para', **s['body']),
        PH(12, 'body', col(4), 904, span(4), 60, 'Fecha', name='Fecha', **s['body']),
        PH(13, 'body', col(8), 904, span(4), 60, 'cal.com/oryzz/30min', name='Contacto', **s['body']),
    ], footer=False, number=False)

    # 03 · Agenda
    rows = []
    for i in range(5):
        y = 196 + i * 136
        rows.append(Ln(col(5), y, RIGHT, y, c['border'], 1.5, name=f'Filete {i + 1}'))
        rows.append(Dot(col(5) + 10, y + 68, 7, c['bg'], line=c['hl'], lw=2, name=f'Nodo {i + 1}'))  # sin numeración: nodo
    rows.append(Ln(col(5), 196 + 5 * 136, RIGHT, 196 + 5 * 136, c['border'], 1.5, name='Filete final'))
    add('Agenda', rows, [
        eyebrow('Agenda'),
        title(w=span(4), h=220, prompt='Agenda'),
        PH(11, 'body', M, 420, span(4), 160, 'Duración · formato', name='Nota', **s['small']),
    ] + [PH(12 + i, 'body', col(5) + 110, 196 + i * 136 + 38, 710, 64, f'Punto {i + 1} de la agenda', name=f'Punto {i + 1}',
            **merged(s['h3'], dict(size=26))) for i in range(5)]
      + [PH(17 + i, 'body', RIGHT - 140, 196 + i * 136 + 52, 140, 32, '10 min', name=f'Duración {i + 1}', **merged(s['meta'], dict(size=13, align='r')))
         for i in range(5)])

    # 04 · Separador de sección
    add('Separador de sección', [Img(0, 0, W, H, A['grid'], name='Retícula'), Img(0, 0, W, H, A['orb_section'], name='Órbitas')], [
        eyebrow('Nombre de la sección'),
        title(y=250, w=1300, h=510, prompt='Título de la sección', st='title_l', anchor='b'),
        PH(11, 'body', M, 792, 1180, 150, 'Una frase que explica qué se va a ver en esta sección.', name='Descripción', **s['lead']),
    ])

    # 05 · Título + texto
    add('Título + texto', [], [
        eyebrow(),
        title(w=span(9), h=290),
        PH(12, 'body', M, 520, span(5), 400, 'Mensaje principal en una o dos frases.', name='Entradilla', **s['lead']),
        PH(11, 'body', col(7), 520, span(5), 420, 'Texto de apoyo. Frases cortas, datos concretos, un único mensaje por diapositiva.', name='Texto', **s['body']),
    ])

    # 06 · Dos columnas
    cols2 = []
    for x in (col(0), col(6)):
        cols2.append(Ln(x, 468, x + span(5), 468, c['border'], 1.5, name='Filete columna'))
    add('Dos columnas', cols2, [
        eyebrow(), title(w=span(9), h=220),
        PH(11, 'body', col(0), 500, span(5), 28, 'Etiqueta A', name='Etiqueta A', **merged(s['eyebrow'], dict(color=c['hl']))),
        PH(12, 'body', col(0), 548, span(5), 130, 'Titular de la columna A', name='Titular A', **s['h3']),
        PH(13, 'body', col(0), 690, span(5), 250, 'Texto de la columna A.', name='Texto A', **s['body']),
        PH(14, 'body', col(6), 500, span(5), 28, 'Etiqueta B', name='Etiqueta B', **merged(s['eyebrow'], dict(color=c['hl']))),
        PH(15, 'body', col(6), 548, span(5), 130, 'Titular de la columna B', name='Titular B', **s['h3']),
        PH(16, 'body', col(6), 690, span(5), 250, 'Texto de la columna B.', name='Texto B', **s['body']),
    ])

    # 07 · Cita / manifiesto
    add('Cita / manifiesto', [Dot(col(1) - 60, 318, 10, c['node'], name='Nodo')], [
        eyebrow(),
        title(x=col(1), y=270, w=span(10), h=500, prompt='«Frase de manifiesto o cita en dos o tres líneas.»', st='title_l',
              font='display_med', size=64, lh=1.08, spc=-0.03),
        PH(11, 'body', col(1), 820, span(8), 32, 'Nombre · cargo', name='Autoría', **s['meta']),
    ])

    # 08 · Cifra gigante
    add('Cifra gigante', [Img(0, 0, W, H, A['grid'], name='Retícula')], [
        eyebrow(),
        PH(11, 'body', M - 12, 250, 1180, 600, '00', name='Cifra', **merged(s['num'], dict(size=300, lh=1.0, spc=-0.05, grad=c['grad'], grad_angle=0))),
        PH(12, 'body', col(8), 440, span(4), 100, 'unidad', name='Unidad', **merged(s['h3'], dict(size=40))),
        PH(13, 'body', col(8), 560, span(4), 310, 'Qué significa la cifra en una frase.', name='Descripción', **s['body']),
        PH(14, 'body', M, 912, 1300, 28, 'Fuente · fecha · ejemplo', name='Fuente', **s['meta']),
    ])

    # 09 · Tres KPIs
    add('Tres KPIs', [Box(M, 360, span(6), 560, fill=c['surf'], line=c['border'], lw=1, r=20, name='Tarjeta dato'),
                         Ln(col(7), 640, RIGHT, 640, c['border'], 1.5, name='Filete')], [
        eyebrow(), title(w=W - 2 * M, h=120),
        PH(11, 'body', M + 56, 412, span(6) - 112, 28, 'Métrica principal', name='Etiqueta 1', **s['eyebrow']),
        PH(12, 'body', M + 48, 468, span(6) - 96, 300, '000', name='Cifra 1', **merged(s['num'], dict(size=150))),
        PH(13, 'body', M + 56, 756, span(6) - 112, 36, '+00 % vs. periodo anterior', name='Variación 1', **s['delta']),
        PH(14, 'body', M + 56, 806, span(6) - 112, 110, 'Qué mide esta cifra.', name='Descripción 1', **s['body18']),
        PH(15, 'body', col(7), 372, span(5), 28, 'Segunda métrica', name='Etiqueta 2', **s['eyebrow']),
        PH(16, 'body', col(7) - 4, 414, span(5), 180, '00', name='Cifra 2', **merged(s['num'], dict(size=88))),
        PH(17, 'body', col(7), 592, span(5), 36, 'Variación', name='Variación 2', **s['delta']),
        PH(18, 'body', col(7), 680, span(5), 28, 'Tercera métrica', name='Etiqueta 3', **s['eyebrow']),
        PH(19, 'body', col(7) - 4, 722, span(5), 180, '00', name='Cifra 3', **merged(s['num'], dict(size=88))),
        PH(20, 'body', col(7), 900, span(5), 36, 'Variación', name='Variación 3', **s['delta']),
    ])

    # 10 · Gráfico
    add('Gráfico', [Ln(1388, 400, 1388, 920, c['border'], 1.5, name='Filete')], [
        eyebrow(), title(w=span(9), h=200),
        PH(11, 'chart', M, 390, span(8), 540, 'Inserta un gráfico', name='Gráfico'),
        PH(12, 'body', 1420, 396, RIGHT - 1420, 130, '+00 %', name='Dato clave', **merged(s['num'], dict(size=60, color=c['text']))),
        PH(13, 'body', 1420, 540, RIGHT - 1420, 310, 'Lectura del gráfico en una frase.', name='Lectura', **s['body18']),
        PH(14, 'body', 1420, 860, RIGHT - 1420, 64, 'Fuente · ejemplo', name='Fuente', **s['meta']),
    ])

    # 11 · Tabla
    add('Tabla', [], [
        eyebrow(), title(w=W - 2 * M, h=120),
        PH(11, 'tbl', M, 330, W - 2 * M, 560, 'Inserta una tabla', name='Tabla'),
        PH(12, 'body', M, 912, 1300, 28, 'Nota · fuente', name='Nota', **s['meta']),
    ])

    # 12 · Proceso en pasos
    xs = [col(0), col(3), col(6), col(9)]
    st12 = [Ln(M, ROUTE_Y, RIGHT, ROUTE_Y, c['border'], 2, name='Ruta')]
    for i, x in enumerate(xs):
        last = i == len(xs) - 1
        st12.append(Dot(x + 10, ROUTE_Y, 11 if last else 9, c['node'] if last else c['bg'], line=None if last else c['text3'], lw=2, name=f'Nodo {i + 1}'))
    add('Proceso en pasos', st12, [
        eyebrow(), title(w=span(10), h=200),
    ] + [PH(11 + i, 'body', x, 530, span(3) - 24, 76, f'Paso {i + 1}', name=f'Paso {i + 1} título', **s['h3']) for i, x in enumerate(xs)]
      + [PH(15 + i, 'body', x, 624, span(3) - 24, 260, 'Descripción breve del paso.', name=f'Paso {i + 1} texto', **s['body18']) for i, x in enumerate(xs)])

    # 13 · Canales -> sistema -> cliente
    st13 = [Img(0, 0, W, H, A['routes'], name='Rutas')]
    for i in range(5):
        st13.append(Box(CH_X, CH_Y0 + i * CH_P, CH_W, CH_H, fill=c['surf'], line=c['border'], lw=1, r=14, name=f'Canal {i + 1}'))
    st13 += [Box(SYS_X, SYS_Y, SYS_W, SYS_H, fill=c['surf'], line=c['hl'], lw=2, r=20, name='Sistema'),
             T(SYS_X + 48, SYS_Y + 44, SYS_W - 96, 30, 'Sistema Oryzz', name='Etiqueta sistema', **merged(s['eyebrow'], dict(color=c['hl']))),
             Dot(NODE_X, MID, 16, c['node'], name='Nodo cliente'),
             T(NODE_X + 44, MID - 100, 330, 30, 'Cliente', name='Etiqueta cliente', **s['eyebrow'])]
    add('Canales → sistema → cliente', st13, [
        eyebrow(), title(w=span(11), h=110),
    ] + [PH(11 + i, 'body', CH_X + 28, CH_Y0 + i * CH_P, CH_W - 56, CH_H, f'Canal {i + 1}', name=f'Canal {i + 1}',
            **merged(s['body'], dict(size=18, color=c['text'], anchor='m', lh=1.15))) for i in range(5)] + [
        PH(16, 'body', SYS_X + 48, SYS_Y + 84, SYS_W - 96, 132, 'Qué hace el sistema', name='Sistema título', **s['h3']),
        PH(17, 'body', SYS_X + 48, SYS_Y + 232, SYS_W - 96, 260, 'Función 1', name='Sistema funciones', **merged(s['list'], dict(size=18, sa=10))),
        PH(18, 'body', NODE_X + 44, MID - 60, RIGHT - NODE_X - 44, 150, 'Resultado', name='Cliente', **merged(s['h3'], dict(size=32))),
        PH(19, 'body', NODE_X + 44, MID + 100, RIGHT - NODE_X - 44, 170, 'Cómo se mide.', name='Cliente texto', **s['small']),
    ])

    # 14 · Antes / después
    add('Antes / después', [Box(M, 330, span(6), 600, fill=c['surf'], r=20, name='Panel antes'),
                               Box(col(6), 330, span(6), 600, fill=c['surf'], line=c['hl'], lw=2, r=20, name='Panel después'),
                               Dot(RIGHT - 52, 382, 10, c['node'], name='Nodo')], [
        eyebrow(), title(w=W - 2 * M, h=120),
        PH(11, 'body', M + 56, 378, span(6) - 112, 28, 'Antes', name='Etiqueta antes', **s['eyebrow']),
        PH(12, 'body', M + 56, 424, span(6) - 112, 70, 'Situación actual', name='Titular antes', **merged(s['h3'], dict(color=c['text2']))),
        PH(13, 'body', M + 56, 528, span(6) - 112, 380, 'Punto', name='Lista antes', **merged(s['list'], dict(color=c['text3']))),
        PH(14, 'body', col(6) + 56, 378, span(6) - 112, 28, 'Después', name='Etiqueta después', **merged(s['eyebrow'], dict(color=c['hl']))),
        PH(15, 'body', col(6) + 56, 424, span(6) - 112, 70, 'Con el sistema', name='Titular después', **s['h3']),
        PH(16, 'body', col(6) + 56, 528, span(6) - 112, 380, 'Punto', name='Lista después', **s['list']),
    ])

    # 15 · Caso de estudio
    st15 = [Box(col(8), 160, span(4), 760, fill=c['surf'], line=c['border'], lw=1, r=20, name='Tarjeta resultado'),
            Ln(col(8) + 48, 640, RIGHT - 48, 640, c['border'], 1.5, name='Filete tarjeta')]
    for i, lab in enumerate(['Reto', 'Qué hicimos', 'Resultado']):
        y = 384 + i * 184
        st15.append(Ln(M, y, col(7) + span(1), y, c['border'], 1.5, name=f'Filete {lab}'))
        st15.append(T(M, y + 28, span(2), 28, lab, name=f'Etiqueta {lab}', **merged(s['meta'], dict(size=13, color=c['hl'] if i == 2 else c['text3']))))
    add('Caso de estudio', st15, [
        eyebrow(), title(w=span(8) - 20, h=250),
        PH(11, 'body', col(2), 404, span(6) - 20, 160, 'El punto de partida.', name='Reto', **merged(s['body18'], dict(lh=1.4))),
        PH(12, 'body', col(2), 588, span(6) - 20, 160, 'Qué montamos.', name='Qué hicimos', **merged(s['body18'], dict(lh=1.4))),
        PH(13, 'body', col(2), 772, span(6) - 20, 160, 'Qué cambió, con cifras.', name='Resultado', **merged(s['body18'], dict(lh=1.4))),
        PH(14, 'body', col(8) + 48, 208, span(4) - 96, 34, 'Métrica', name='Etiqueta cifra', **s['eyebrow']),
        PH(15, 'body', col(8) + 40, 256, span(4) - 80, 200, '+000', name='Cifra', **merged(s['num'], dict(size=96, grad=c['grad'], grad_angle=0))),
        PH(16, 'body', col(8) + 48, 468, span(4) - 96, 140, 'unidad y periodo', name='Unidad', **merged(s['h3'], dict(size=30))),
        PH(17, 'body', col(8) + 48, 676, 210, 100, '00', name='Cifra 2', **merged(s['num'], dict(size=48))),
        PH(18, 'body', col(8) + 48, 782, 210, 64, 'Segunda métrica', name='Etiqueta 2', **s['meta']),
        PH(19, 'body', col(8) + 290, 676, 210, 100, '00', name='Cifra 3', **merged(s['num'], dict(size=48))),
        PH(20, 'body', col(8) + 290, 782, 210, 64, 'Tercera métrica', name='Etiqueta 3', **s['meta']),
    ])

    # 16 · Plan 30-60-90
    xs3 = [col(0), col(4), col(8)]
    st16 = [Ln(M, 448, RIGHT, 448, c['border'], 2, name='Línea de tiempo')]
    for i, x in enumerate(xs3):
        last = i == 2
        st16.append(Dot(x + 10, 448, 11 if last else 9, c['node'] if last else c['bg'], line=None if last else c['text3'], lw=2, name=f'Hito {i + 1}'))
    add('Plan 30-60-90', st16, [
        eyebrow(), title(w=W - 2 * M, h=120),
    ] + [PH(11 + i, 'body', x, 380, span(4), 28, 'Días 1–30', name=f'Fase {i + 1} etiqueta', **merged(s['eyebrow'], dict(color=c['hl'] if i < 2 else c['text']))) for i, x in enumerate(xs3)]
      + [PH(14 + i, 'body', x, 488, span(4) - 24, 88, 'Fase', name=f'Fase {i + 1} título', **merged(s['h3'], dict(size=36))) for i, x in enumerate(xs3)]
      + [PH(17 + i, 'body', x, 592, span(4) - 40, 360, 'Acción', name=f'Fase {i + 1} acciones', **merged(s['list'], dict(size=18))) for i, x in enumerate(xs3)])

    # 17 · Equipo (2 personas)
    st17 = []
    for x in (col(0), col(6)):
        st17.append(Box(x, 400, span(2), 316, fill=c['ph_bg'], r=14, name='Fondo foto'))
        st17.append(T(x + 20, 672, span(2) - 40, 28, 'Foto 4:5', name='Etiqueta foto', **merged(s['meta'], dict(size=10, color=c['ph_label']))))
    add('Equipo', st17, [
        PH(21, 'pic', col(0), 400, span(2), 316, 'Foto', name='Foto A', r=14),
        PH(22, 'pic', col(6), 400, span(2), 316, 'Foto', name='Foto B', r=14),
        eyebrow(), title(w=W - 2 * M, h=120),
    ] + sum([[PH(11 + k * 5, 'body', x + span(2) + GUT + 8, 396, span(3) + 100, 82, 'Nombre Apellido', name=f'Nombre {"AB"[k]}', **merged(s['h3'], dict(size=34))),
              PH(12 + k * 5, 'body', x + span(2) + GUT + 8, 476, span(3) + 100, 34, 'Rol', name=f'Rol {"AB"[k]}', **merged(s['eyebrow'], dict(color=c['hl']))),
              PH(13 + k * 5, 'body', x + span(2) + GUT + 8, 526, span(3) + 100, 220, 'Qué hace en una o dos frases.', name=f'Bio {"AB"[k]}', **s['body18']),
              PH(14 + k * 5, 'body', x + span(2) + GUT + 8, 790, span(3) + 100, 34, '{{correo}}', name=f'Contacto {"AB"[k]}', **merged(s['meta'], dict(size=13)))]
             for k, x in enumerate((col(0), col(6)))], []))

    # 18 · Precios / planes
    st18 = []
    px = [col(0), col(4), col(8)]
    PAD = 44
    for i, x in enumerate(px):
        st18.append(Box(x, 356, span(4), 580, fill=c['surf'], line=c['hl'] if i == 1 else c['border'], lw=2 if i == 1 else 1, r=20, name=f'Plan {i + 1}'))
        st18.append(Ln(x + PAD, 676, x + span(4) - PAD, 676, c['border'], 1.5, name='Filete plan'))
    add('Precios / planes', st18, [
        eyebrow(), title(w=W - 2 * M, h=100),
        PH(11, 'body', M, 262, 1680, 60, 'Qué incluye la inversión y qué va aparte.', name='Introducción', **s['body18']),
    ] + sum([[PH(12 + i * 5, 'body', x + PAD, 396, span(4) - 2 * PAD, 30, 'Plan', name=f'Plan {i + 1} etiqueta', **merged(s['eyebrow'], dict(size=13, color=c['hl'] if i == 1 else c['text3']))),
              PH(13 + i * 5, 'body', x + PAD, 438, span(4) - 2 * PAD, 70, 'Nombre', name=f'Plan {i + 1} nombre', **merged(s['h3'], dict(size=30))),
              PH(14 + i * 5, 'body', x + PAD - 4, 506, span(4) - 2 * PAD + 8, 110, '000 €', name=f'Plan {i + 1} precio', **merged(s['num'], dict(size=56))),
              PH(15 + i * 5, 'body', x + PAD, 618, span(4) - 2 * PAD, 40, '/ mes', name=f'Plan {i + 1} periodo', **merged(s['small'], dict(size=18, lh=1.1))),
              PH(16 + i * 5, 'body', x + PAD, 706, span(4) - 2 * PAD, 220, 'Incluye', name=f'Plan {i + 1} incluye', **merged(s['list'], dict(size=18, sa=8, indent=28)))]
             for i, x in enumerate(px)], []))

    # 19 · Imagen a sangre con velo
    add('Imagen a sangre', [Box(0, 0, W, H, fill=c['ph_bg'], name='Fondo foto'), Img(0, 0, W, H, A['grid'], name='Retícula'),
                               T(M, 120, 1200, 30, 'Foto a sangre · 1920 × 1080 px · velo Grafito 950 al 62 %', name='Etiqueta foto', **merged(s['meta'], dict(color=c['ph_label'])))], [
        PH(11, 'pic', 0, 0, W, H, 'Foto a sangre', name='Foto'),
        PH(10, 'body', M, 530, 1000, 34, 'Etiqueta', name='Etiqueta', **merged(s['eyebrow'], dict(color=c['on_photo2']))),
        title(y=580, w=1440, h=360, prompt='Titular sobre la foto', size=56, lh=1.04, color=c['on_photo'], anchor='t'),
        PH(12, 'body', M, 968, 1200, 30, 'Pie de foto', name='Pie de foto', **merged(s['meta'], dict(color=c['on_photo2']))),
    ], footer=False, number=False)

    # 20 · Imagen + texto
    add('Imagen + texto', [Box(0, 0, 960, H, fill=c['ph_bg'], name='Fondo foto'),
                              T(M, 1000, 700, 30, 'Foto 960 × 1080 px', name='Etiqueta foto', **merged(s['meta'], dict(size=10, color=c['ph_label'])))], [
        PH(11, 'pic', 0, 0, 960, H, 'Foto', name='Foto'),
        eyebrow(x=col(7)), title(x=col(7), w=span(5), h=380),
        PH(12, 'body', col(7), 580, span(5), 380, 'Texto de apoyo.', name='Texto', **s['body']),
    ], footer=False)

    # 21 · Comparativa
    add('Comparativa', [Box(1120, 316, 680, 600, fill=c['surf'], line=c['hl'], lw=2, r=20, name='Columna destacada'),
                           Dot(RIGHT - 44, 358, 10, c['node'], name='Nodo')], [
        eyebrow(), title(w=W - 2 * M, h=120),
        PH(11, 'tbl', M, 330, W - 2 * M, 560, 'Inserta una tabla de 3 columnas', name='Tabla'),
    ])

    # 22 · Preguntas frecuentes (4 filas a la derecha)
    FQ0, FQP = 150, 205
    st22 = [Ln(col(6), FQ0 + i * FQP, RIGHT, FQ0 + i * FQP, c['border'], 1.5, name=f'Filete {i + 1}') for i in range(4)]
    add('Preguntas frecuentes', st22, [
        eyebrow(), title(w=span(5), h=380),
        PH(11, 'body', M, 600, span(4), 200, 'Nota o contacto.', name='Nota', **s['small']),
    ] + sum([[PH(12 + i * 2, 'body', col(6), FQ0 + 28 + i * FQP, span(6), 60, '¿Pregunta?', name=f'Pregunta {i + 1}', **s['h4']),
              PH(13 + i * 2, 'body', col(6), FQ0 + 88 + i * FQP, span(6), 110, 'Respuesta breve.', name=f'Respuesta {i + 1}', **s['body18'])]
             for i in range(4)], []))

    # 23 · Lista de seis (3 x 2 a todo el ancho)
    st23 = []
    LY = [384, 676]
    for i in range(6):
        x, y = col((i % 3) * 4), LY[i // 3]
        st23.append(Ln(x, y, x + span(4), y, c['border'], 1.5, name=f'Filete {i + 1}'))
        st23.append(Dot(x + 10, y + 39, 7, c['bg'], line=c['hl'], lw=2, name=f'Nodo {i + 1}'))  # sin numeración: nodo
    add('Lista de seis', st23, [
        eyebrow(), title(w=span(7), h=190),
        PH(11, 'body', col(8), 172, span(4), 160, 'Nota.', name='Nota', **s['small']),
    ] + sum([[PH(12 + i * 2, 'body', col((i % 3) * 4), LY[i // 3] + 66, span(4) - 24, 60, 'Punto', name=f'Punto {i + 1}', **s['h4']),
              PH(13 + i * 2, 'body', col((i % 3) * 4), LY[i // 3] + 128, span(4) - 40, 120, 'Descripción breve.', name=f'Texto {i + 1}', **s['body18'])]
             for i in range(6)], []))

    # 24 · CTA
    btn = Box(M, 800, 700, 104, fill=c['cta_fill'], grad=None if c['cta_fill'] else c['grad'], r=52, name='Botón')
    add('Llamada a la acción', [Img(0, 0, W, H, A['grid'], name='Retícula'), Img(0, 0, W, H, A['orb_cta'], name='Órbitas'), btn], [
        eyebrow(y=140),
        title(y=190, w=1180, h=500, prompt='Llamada a la acción', st='title_l', size=84, anchor='b'),
        PH(11, 'body', M, 708, 1100, 72, 'Qué obtiene la persona.', name='Subtítulo', **s['lead']),
        PH(12, 'body', M + 52, 800, 620, 104, 'enlace', name='Texto del botón', **dict(font='text_bold', size=22, color=c['cta_text'], anchor='m', lh=1.2)),
        PH(13, 'body', M + 744, 834, 700, 36, 'Sin compromiso', name='Nota', **merged(s['meta'], dict(size=13))),
    ])

    # 25 · Cierre
    add('Cierre', [Img(0, 0, W, H, A['grid'], name='Retícula'), Img(0, 0, W, H, A['orb_close'], name='Órbitas'), logo()], [
        eyebrow(y=380),
        title(y=420, w=1100, h=300, prompt='Gracias.', st='cover', size=150, lh=0.92),
        PH(11, 'body', M, 744, 900, 220, 'web · agenda · redes', name='Contacto', **merged(s['body'], dict(size=22, color=c['text2'], lh=1.55))),
    ], footer=False, number=False)


    # utilidades
    add('Título y contenido', [], [eyebrow(), title(w=span(10), h=200),
                                       PH(11, 'body', M, 420, span(8), 500, 'Texto', name='Contenido', **s['body'])])
    add('Solo título', [], [eyebrow(), title(w=span(10), h=200)])
    add('En blanco', [], [])
    return L


# ---------------------------------------------------------------- contenido: plantilla
def template_slides(theme, L):
    c = theme.c
    s = styles(c)
    CAL = 'https://cal.com/oryzz/30min'
    S = []
    S.append(Slide(L['Portada · Órbita'], {
        10: 'Propuesta de captación · septiembre de 2026',
        0: 'Más **clientes.**\nNo más likes.',
        11: 'Anuncios, IA y reseñas conectados en un solo sistema que se mide en clientes y en euros.',
        12: 'Preparado para {{Cliente}} · oryzz.com'},
        notes='Portada principal. Sustituye el titular por el claim de la propuesta (máx. 2 líneas) y resalta en azul una sola palabra.'))
    S.append(Slide(L['Portada · Tipográfica'], {
        10: 'Presentación comercial · 2026',
        0: 'Un sistema de captación, **no acciones sueltas.**',
        11: '{{Nombre del cliente}}', 12: '29 de septiembre de 2026', 13: 'cal.com/oryzz/30min'},
        notes='Portada alternativa, solo tipográfica. Úsala para documentos internos o cuando la órbita compita con el titular.'))
    S.append(Slide(L['Agenda'], {
        10: 'Agenda', 0: 'Qué vamos\na ver',
        11: '45 minutos · Videollamada\nResolvemos dudas al final de cada bloque.',
        12: 'Dónde se pierden clientes', 13: 'Cómo funciona el sistema', 14: 'Plan de 30, 60 y 90 días',
        15: 'Inversión y planes', 16: 'Siguientes pasos',
        17: '5 min', 18: '10 min', 19: '10 min', 20: '10 min', 21: '10 min'}))
    S.append(Slide(L['Separador de sección'], {
        10: 'El diagnóstico', 0: 'Dónde se pierden\nhoy tus **clientes**',
        11: 'Antes de invertir un euro más en anuncios, miramos qué pasa con los que ya te escriben.'}))
    S.append(Slide(L['Título + texto'], {
        10: 'El problema', 0: 'El problema no es que no te vean. **Es que no te contactan.**',
        12: 'Tu negocio ya recibe visitas, mensajes y llamadas. Lo que falla es lo que pasa después.',
        11: 'Mensajes que se responden tarde, llamadas fuera de horario que nadie devuelve y anuncios que se miden en clics, no en citas.\n'
            'Un sistema de captación conecta cada canal con una respuesta inmediata y un seguimiento que se puede medir.'}))
    S[-1].fill[11] = [P('Mensajes que se responden tarde, llamadas que nadie devuelve y anuncios medidos en clics, no en citas.', sa=16),
                      P('Un sistema conecta cada canal con una respuesta inmediata y un seguimiento medible.')]
    S.append(Slide(L['Cifra gigante'], {
        10: 'Puesta en marcha', 11: '3–7', 12: 'días',
        13: 'Lo que tardamos en tener tu sistema captando: anuncios activos, respuesta automática y panel de resultados.',
        14: 'Plazo habitual de implantación · dato de ejemplo'},
        notes='Una sola cifra por diapositiva. La cifra lleva el gradiente IA: no añadas lima en esta diapositiva.'))
    S.append(Slide(L['Dos columnas'], {
        10: 'Cómo lo resolvemos', 0: 'Dos piezas que tienen que\nfuncionar juntas',
        11: 'Captar', 12: 'Anuncios que traen conversaciones',
        13: 'Meta Ads, Google Ads y TikTok Ads orientados a mensajes y llamadas reales, no a alcance. Cada euro se mide contra citas.',
        14: 'Convertir', 15: 'Automatización que las convierte en citas',
        16: 'Un asistente con IA responde en WhatsApp en menos de 2 minutos, cualifica, agenda y avisa a tu equipo.'}))
    S.append(Slide(L['Canales → sistema → cliente'], {
        10: 'El sistema', 0: 'Canales → sistema → **cliente**',
        11: 'Meta Ads', 12: 'Google Ads', 13: 'TikTok Ads', 14: 'Google Maps y reseñas', 15: 'ChatGPT · Gemini · Perplexity',
        16: 'Capta, responde y hace seguimiento',
        17: ['Respuesta con IA en WhatsApp', 'Agenda automática', 'CRM con el origen de cada lead', 'Panel de resultados semanal'],
        18: 'Cliente con cita', 19: 'Se mide en citas y en euros, no en likes.'},
        notes='Diagrama base del sistema. Cambia los nombres de los canales; las rutas son fijas (5 entradas).'))
    S.append(Slide(L['Lista de seis'], {
        10: 'Servicios', 0: 'Seis palancas.\n**Un solo sistema.**',
        11: 'Activamos solo las que tienen sentido para tu negocio. Si no encajamos, te lo decimos.',
        12: 'Meta Ads', 13: 'Campañas en Instagram y Facebook orientadas a mensajes y citas.',
        14: 'Google Ads', 15: 'Aparece cuando te buscan con intención, en búsqueda y en Maps.',
        16: 'TikTok Ads', 17: 'Vídeo corto con segmentación local para crear demanda nueva.',
        18: 'Automatización con IA', 19: 'Respuesta, cualificación y agenda en WhatsApp las 24 horas.',
        20: 'SEO local y reseñas', 21: 'Ficha de Google optimizada y un flujo constante de reseñas.',
        22: 'GEO', 23: 'Que ChatGPT, Gemini y Perplexity te recomienden en tu sector.'}))
    S.append(Slide(L['Proceso en pasos'], {
        10: 'Cómo trabajamos', 0: 'De la primera llamada a un sistema\nque gira solo',
        11: 'Diagnóstico', 12: 'Montaje', 13: 'Lanzamiento', 14: 'Optimización',
        15: '30 minutos. Sales con un diagnóstico, no con un presupuesto.',
        16: 'Anuncios, asistente de WhatsApp, CRM y medición conectados.',
        17: 'Primeras campañas activas y respuesta automática en marcha.',
        18: 'Cada semana: coste por cita, qué canal funciona y qué se ajusta.'}))
    S.append(Slide(L['Antes / después'], {
        10: 'Antes y después', 0: 'Lo que cambia cuando hay **un sistema**',
        11: 'Antes', 12: 'Captación a golpe de post',
        13: ['Mensajes sin responder en horas', 'Leads apuntados en una libreta', 'Anuncios medidos en likes', 'No sabes qué cita trajo cada euro'],
        14: 'Después', 15: 'Captación con sistema',
        16: ['Respuesta en menos de 2 minutos', 'Cada lead en el CRM con su origen', 'Campañas por coste por cita', 'Informe semanal en citas y euros']}))
    S.append(Slide(L['Gráfico'], {
        10: 'Resultados · ejemplo', 0: 'Leads cualificados por semana',
        11: Chart([f'S{i}' for i in range(1, 13)], [('Leads cualificados', [18, 17, 19, 20, 24, 26, 27, 29, 30, 31, 33, 34], c['chart_main'])],
                  y_max=40, y_unit=10, point_colors={(0, i): c['chart_muted'] for i in range(4)}, gap=55),
        12: {'text': '+73 %', 'grad': None},
        13: 'Últimas 4 semanas frente a las 4 primeras, tras activar el seguimiento por WhatsApp.',
        14: 'Datos de ejemplo'},
        notes='Gráfico nativo de PowerPoint: clic derecho > Modificar datos. Barras grises = antes; azul = con el sistema.'))
    S.append(Slide(L['Tres KPIs'], {
        10: 'Primer trimestre · ejemplo', 0: 'Lo que medimos cada semana',
        11: 'Citas agendadas', 12: '146', 13: '+41 % vs. trimestre anterior', 14: 'Citas confirmadas en agenda, no formularios ni clics.',
        15: 'Coste por lead', 16: '18 €', 17: '−32 % en 90 días',
        18: 'Tiempo de respuesta', 19: '2 min', 20: 'Antes: 5 horas'}))
    S.append(Slide(L['Caso de estudio'], {
        10: 'Caso · ejemplo', 0: 'La agenda llena **sin depender del teléfono**',
        11: 'Clínica dental. Los mensajes de Instagram y WhatsApp se respondían al día siguiente y los pacientes reservaban en otra clínica.',
        12: 'Meta Ads a mensajes, asistente con IA en WhatsApp que agenda en su software y flujo de reseñas tras cada visita.',
        13: 'Respuesta en menos de 2 minutos y agenda de primeras visitas completa desde la semana 6.',
        14: 'Primeras visitas', 15: '+146', 16: 'citas nuevas en 90 días',
        17: '18 €', 18: 'Coste por lead', 19: '4,8', 20: 'Valoración en Google'}))
    tbl_st = dict(cell=dict(font='text', size=18, color=c['text2'], lh=1.3, border_b=c['border'], border_w=1.5, pad=(0, 24, 0, 0)),
                  head=dict(font='text_semi', size=13, color=c['text3'], border_b=c['text3'], border_w=1.5),
                  first=dict(font='display', size=20, color=c['text'], spc=-0.01))
    S.append(Slide(L['Tabla'], {
        10: 'Canales', 0: 'Qué hace cada canal y cómo lo medimos',
        11: Table([['Canal', 'Para qué sirve', 'Métrica que manda', 'Primeros datos'],
                   ['Meta Ads', 'Generar conversaciones con público local', 'Coste por conversación', '3–7 días'],
                   ['Google Ads', 'Captar a quien ya te está buscando', 'Coste por llamada o cita', '1–2 semanas'],
                   ['TikTok Ads', 'Crear demanda nueva con vídeo corto', 'Coste por lead cualificado', '2–3 semanas'],
                   ['SEO local y reseñas', 'Ganar la búsqueda en Google Maps', 'Llamadas y rutas desde la ficha', '4–8 semanas'],
                   ['GEO', 'Aparecer en ChatGPT, Gemini y Perplexity', 'Menciones y visitas referidas', '6–12 semanas']],
                  col_w=[340, 560, 500, 280], row_h=[56] + [100] * 5, styles=tbl_st,
                  col_styles={3: dict(font='mono', size=16, color=c['text'], caps=False, spc=0)}),
        12: 'Plazos orientativos · ejemplo'}))
    S[-1].fill[11].col_styles[3]['head'] = dict(font='text_semi', size=13, color=c['text3'])
    cmp_st = dict(cell=dict(font='text', size=19, color=c['text3'], lh=1.3, border_b=c['border'], border_w=1.5, pad=(0, 32, 0, 0)),
                  head=dict(font='text_semi', size=13, color=c['text3'], border_b=None),
                  first=dict(font='text_semi', size=19, color=c['text2']))
    S.append(Slide(L['Comparativa'], {
        10: 'Por qué Oryzz', 0: 'Agencia tradicional frente a **un sistema**',
        11: Table([['', 'Agencia tradicional', 'Oryzz'],
                   ['Se mide en', 'Alcance, likes e impresiones', 'Citas, clientes y euros'],
                   ['Respuesta a leads', 'Tu equipo, cuando puede', 'IA en WhatsApp, al momento'],
                   ['Informes', 'PDF mensual difícil de leer', 'Panel semanal con coste por cita'],
                   ['Canales', 'Acciones sueltas por separado', 'Un sistema conectado'],
                   ['Si no encajamos', 'Te lo dicen tarde', 'Te lo decimos en la primera llamada']],
                  col_w=[400, 600, 680], row_h=[92] + [96] * 5, styles=cmp_st,
                  col_styles={2: dict(font='text_semi', color=c['text'], pad=(40, 32, 0, 0), border_b=c['border'],
                                      head=dict(font='display', size=26, color=c['text'], caps=False, spc=-0.02))})},
        notes='La columna destacada (panel azul) está en el layout: mantén Oryzz en la tercera columna.'))
    S[-1].fill[11].styles['last_b'] = None
    S.append(Slide(L['Plan 30-60-90'], {
        10: 'Plan de trabajo', 0: 'Plan 30 · 60 · 90',
        11: 'Días 1–30', 12: 'Días 31–60', 13: 'Días 61–90',
        14: 'Montar', 15: 'Medir', 16: 'Escalar',
        17: ['Diagnóstico y objetivos en euros', 'Campañas y asistente de WhatsApp', 'CRM y medición conectados'],
        18: ['Coste por cita en cada canal', 'Ajuste de mensajes y públicos', 'Primer flujo de reseñas'],
        19: ['Más presupuesto donde hay retorno', 'SEO local y GEO', 'Revisión trimestral de resultados']}))
    mono = lambda x, t: T(x, 400, span(2), 316, t, name='Monograma', **dict(font='display', size=72, color=c['text3'], spc=-0.04, align='c', anchor='m', lh=1))
    S.append(Slide(L['Equipo'], {
        21: None, 22: None,
        10: 'Equipo', 0: 'Dos socios. **Un solo sistema.**',
        11: 'Juan Salazar', 12: 'Estrategia y Ads',
        13: 'Diseña la estrategia y lleva las campañas de Meta, Google y TikTok. Mide cada euro contra citas.',
        14: '{{juan@oryzz.com}}',
        16: 'David Morales', 17: 'Automatización e IA',
        18: 'Construye los asistentes con IA, las automatizaciones y el CRM que convierten cada mensaje en una cita.',
        19: '{{david@oryzz.com}}'},
        under=[mono(col(0), 'JS'), mono(col(6), 'DM')],
        notes='Sustituye los monogramas por fotos reales 4:5 (clic en el icono de imagen del marcador). Correos: marcadores editables.'))
    S.append(Slide(L['Cita / manifiesto'], {
        11: 'Oryzz · valoración inicial', 10: 'Nuestra forma de trabajar',
        0: '«30 minutos. Sales con un diagnóstico, **no con un presupuesto.**»'}))
    S.append(Slide(L['Imagen a sangre'], {
        11: None, 10: 'Automatización con IA',
        0: 'Tu recepción no debería depender de que alguien mire el móvil.',
        12: 'Foto: {{recepción de la clínica, luz natural}}'},
        under=[Box(0, 0, W, H, fill='#0B0D12', alpha=0.62, name='Velo 62 %')],
        notes='Inserta una foto real en el marcador (clic en el icono). El velo Grafito 950 al 62 % queda por encima: no lo borres.'))
    S.append(Slide(L['Imagen + texto'], {
        11: None, 10: 'SEO local y reseñas', 0: 'Cuando te buscan en Google Maps, **ganas tú**',
        12: [P('Optimizamos tu ficha de Google y montamos un flujo que pide la reseña justo después de la visita.', sa=16),
             P('Más reseñas recientes, más llamadas y más rutas hacia tu negocio.')]}))
    S.append(Slide(L['Precios / planes'], {
        10: 'Inversión · ejemplo', 0: 'Elige el ritmo. **El sistema es el mismo.**',
        11: 'Precios de ejemplo sin IVA. La inversión en anuncios va aparte y se fija con datos.',
        12: 'Para empezar', 13: 'Arranque', 14: '490 €', 15: '/ mes · ejemplo', 16: ['1 canal de anuncios', 'Respuesta automática', 'Informe mensual'],
        17: 'Recomendado', 18: 'Sistema', 19: '890 €', 20: '/ mes · ejemplo', 21: ['2 canales de anuncios', 'Asistente IA que agenda', 'CRM y panel semanal'],
        22: 'Para crecer', 23: 'Completo', 24: '1.290 €', 25: '/ mes · ejemplo', 26: ['Todos los canales', 'SEO local y GEO', 'Revisión quincenal']}))
    S.append(Slide(L['Preguntas frecuentes'], {
        10: 'Preguntas frecuentes', 0: 'Lo que nos preguntan antes de empezar',
        11: '¿Otra duda? La resolvemos en la valoración de 30 minutos.',
        12: '¿Cuánto invierto en anuncios?', 13: 'Depende de tu zona y tu ticket. Lo calculamos con datos antes de que gastes de más.',
        14: '¿Cuándo llegan los primeros leads?', 15: 'Normalmente en la primera semana. Las citas estables llegan entre el día 30 y el 60.',
        16: '¿Tengo que cambiar mi web?', 17: 'No siempre. Si no convierte, montamos una página de citas conectada al sistema.',
        18: '¿Y si no encajamos?', 19: 'Te lo decimos en la primera llamada, sin rodeos y sin presupuesto sorpresa.'}))
    S.append(Slide(L['Llamada a la acción'], {
        10: 'Siguiente paso', 0: 'Agenda tu valoración\nde **30 minutos.**',
        11: 'Sales con un diagnóstico, no con un presupuesto.',
        12: [P([Rn('cal.com/oryzz/30min   →', link=CAL)])],
        13: 'Sin compromiso · por videollamada'},
        notes='Un único CTA por pieza. El enlace del botón ya apunta a cal.com/oryzz/30min.'))
    S.append(Slide(L['Cierre'], {
        10: 'Más clientes. No más likes.', 0: 'Gracias.',
        11: [P([Rn('oryzz.com', color=c['text'])]), P('cal.com/oryzz/30min'), P('@oryzzai · linkedin.com/company/oryzz')]}))
    return S


# ---------------------------------------------------------------- contenido: deck comercial (clínica dental ficticia)
def deck_slides(theme, L):
    c = theme.c
    CAL = 'https://cal.com/oryzz/30min'
    S = []
    S.append(Slide(L['Portada · Órbita'], {
        10: 'Propuesta de captación · octubre de 2026',
        0: {'text': 'Más **pacientes.**\nMenos huecos.', 'size': 86},
        11: 'Anuncios, respuesta con IA y reseñas para llenar la agenda de primeras visitas.',
        12: 'Clínica Dental Arce · cliente ficticio'}))
    S.append(Slide(L['Agenda'], {
        10: 'Agenda', 0: 'Qué vamos\na ver',
        11: '45 minutos · Videollamada con dirección y recepción.\nCaso ficticio: cifras de ejemplo.',
        12: 'Lo que vimos en tu clínica', 13: 'Dónde se pierden pacientes', 14: 'El sistema que proponemos',
        15: 'Objetivos, plan e inversión', 16: 'Siguientes pasos',
        17: '10 min', 18: '5 min', 19: '10 min', 20: '15 min', 21: '5 min'}))
    S.append(Slide(L['Título + texto'], {
        10: 'Lo que vimos · ejemplo', 0: 'Buena reputación, **agenda irregular**',
        12: 'Clínica Dental Arce tiene 4,6 estrellas en Google y un equipo muy valorado. Pero las primeras visitas dependen del boca a boca.',
        11: [P('Hoy la captación se apoya en publicaciones orgánicas y en un anuncio de Instagram que se activa y se para según el mes.', sa=16),
             P('Los mensajes de Instagram y WhatsApp los responde recepción entre paciente y paciente.')]}))
    S.append(Slide(L['Cifra gigante'], {
        10: 'Diagnóstico · ejemplo', 11: '41 %', 12: 'llega tarde',
        13: 'de los mensajes se responde al día siguiente. Para entonces, el paciente ya ha pedido cita en otra clínica.',
        14: 'Muestra de 212 mensajes · agosto de 2026 · datos de ejemplo'}))
    S.append(Slide(L['Separador de sección'], {
        10: 'La propuesta', 0: 'Responder\n**antes que nadie**',
        11: 'Anuncios para atraer, IA para responder y reseñas para que te elijan.'}))
    S.append(Slide(L['Canales → sistema → cliente'], {
        10: 'El sistema para Clínica Arce', 0: 'Canales → sistema → **paciente**',
        11: 'Meta Ads', 12: 'Google Ads · búsqueda', 13: 'Google Maps y reseñas', 14: 'Instagram orgánico', 15: 'Web de la clínica',
        16: 'Asistente de WhatsApp con IA',
        17: ['Responde en menos de 2 min', 'Resuelve dudas de precio', 'Agenda en tu software', 'Recuerda la cita 24 h antes'],
        18: 'Primera visita', 19: 'Confirmada, con su canal de origen y su coste.'}))
    S.append(Slide(L['Dos columnas'], {
        10: 'Qué montamos', 0: 'Dos piezas, un objetivo:\nprimeras visitas',
        11: 'Captar', 12: 'Anuncios de implantes, ortodoncia e higiene',
        13: 'Meta Ads a mensajes de WhatsApp en un radio de 8 km y Google Ads para quien busca «dentista cerca». Presupuesto por tratamiento.',
        14: 'Convertir', 15: 'Recepción que no se satura',
        16: 'El asistente responde, filtra y agenda. Recepción solo atiende lo que necesita una persona y ve cada conversación en el CRM.'}))
    S.append(Slide(L['Gráfico'], {
        10: 'Proyección · ejemplo', 0: 'Primeras visitas al mes',
        11: Chart(['Hoy', 'Oct', 'Nov', 'Dic', 'Ene', 'Feb', 'Mar'], [('Primeras visitas', [38, 44, 53, 58, 66, 71, 76], c['chart_main'])],
                  y_max=80, y_unit=20, point_colors={(0, 0): c['chart_muted']}, labels=True, gap=60),
        12: '×2',
        13: 'Primeras visitas al mes en seis meses, con 1.200 € al mes de inversión en anuncios.',
        14: 'Estimación, no garantía'}))
    S.append(Slide(L['Tres KPIs'], {
        10: 'Objetivos a 90 días · ejemplo', 0: 'Tres números que revisamos cada lunes',
        11: 'Primeras visitas al mes', 12: '66', 13: '+74 % vs. hoy (38)', 14: 'Citas confirmadas que acuden, contadas en tu software de gestión.',
        15: 'Coste por primera visita', 16: '25 €', 17: 'Objetivo máximo',
        18: 'Tiempo de respuesta', 19: '< 2 min', 20: 'Hoy: 9 horas de media'}))
    S.append(Slide(L['Plan 30-60-90'], {
        10: 'Plan de trabajo · Clínica Arce', 0: 'Plan 30 · 60 · 90',
        11: 'Días 1–30', 12: 'Días 31–60', 13: 'Días 61–90',
        14: 'Montar', 15: 'Medir', 16: 'Escalar',
        17: ['Asistente de WhatsApp conectado a la agenda', 'Campañas de Meta y Google activas', 'Formación a recepción (60 min)'],
        18: ['Coste por primera visita por tratamiento', 'Ajuste de anuncios y respuestas', 'Flujo de reseñas tras cada visita'],
        19: ['Más presupuesto a implantes si rinde', 'SEO local de la ficha de Google', 'Revisión de resultados con dirección']}))
    S.append(Slide(L['Precios / planes'], {
        10: 'Inversión · ejemplo', 0: 'Nuestra recomendación: **Sistema**',
        11: 'Precios de ejemplo sin IVA. Anuncios aparte: 1.200 € al mes recomendados, pagados a Meta y Google.',
        12: 'Para empezar', 13: 'Arranque', 14: '490 €', 15: '/ mes · ejemplo', 16: ['Meta Ads', 'Respuesta automática', 'Informe mensual'],
        17: 'Recomendado', 18: 'Sistema', 19: '890 €', 20: '/ mes · ejemplo', 21: ['Meta Ads + Google Ads', 'Asistente IA que agenda', 'CRM y panel semanal'],
        22: 'Para crecer', 23: 'Completo', 24: '1.290 €', 25: '/ mes · ejemplo', 26: ['Todo lo anterior', 'SEO local y GEO', 'Revisión quincenal']}))
    S.append(Slide(L['Preguntas frecuentes'], {
        10: 'Dudas habituales', 0: 'Lo que suele preguntar una clínica',
        11: '¿Otra duda? Escríbenos antes de la próxima llamada.',
        12: '¿Sustituye a recepción?', 13: 'No. Resuelve lo repetitivo (horarios, precios, huecos) y deja a recepción lo importante.',
        14: '¿Funciona con nuestro software?', 15: 'Con la mayoría de agendas online. Si no hay integración, reserva y avisa a recepción.',
        16: '¿Cuánto tiempo necesita el equipo?', 17: '60 minutos para el montaje y 15 minutos a la semana para revisar resultados.',
        18: '¿Y si no funciona?', 19: 'Revisamos el coste por visita cada semana. Si en 60 días no hay tracción, te lo decimos.'}))
    mono = lambda x, t: T(x, 400, span(2), 316, t, name='Monograma', **dict(font='display', size=72, color=c['text3'], spc=-0.04, align='c', anchor='m', lh=1))
    S.append(Slide(L['Equipo'], {
        21: None, 22: None, 10: 'Quién trabajará contigo', 0: 'Hablarás siempre con **los socios**',
        11: 'Juan Salazar', 12: 'Estrategia y Ads',
        13: 'Tu interlocutor para campañas, presupuesto y resultados. Revisa contigo el coste por primera visita.',
        14: '{{juan@oryzz.com}}',
        16: 'David Morales', 17: 'Automatización e IA',
        18: 'Monta el asistente de WhatsApp, la conexión con tu agenda y el CRM. Forma a recepción.',
        19: '{{david@oryzz.com}}'}, under=[mono(col(0), 'JS'), mono(col(6), 'DM')]))
    S.append(Slide(L['Llamada a la acción'], {
        10: 'Siguiente paso', 0: 'Reserva la sesión\nde **arranque.**',
        11: 'Objetivos, accesos y fecha de lanzamiento.',
        12: [P([Rn('cal.com/oryzz/30min   →', link=CAL)])],
        13: 'Respuesta en 24 h laborables'}))
    S.append(Slide(L['Cierre'], {
        10: 'Más pacientes. Menos huecos.', 0: 'Gracias.',
        11: [P([Rn('oryzz.com', color=c['text'])]), P('cal.com/oryzz/30min'), P('@oryzzai · linkedin.com/company/oryzz')]}))
    return S


# ---------------------------------------------------------------- build
def build(dark=True, which='template', out_pptx=None, out_html=None):
    footer = 'Oryzz · Sistemas que captan clientes' if which == 'template' else 'Oryzz · Propuesta para Clínica Dental Arce · Ejemplo'
    theme = make_theme(dark, footer_text=footer)
    A = make_assets(theme)
    L = make_layouts(theme, A)
    slides = template_slides(theme, L) if which == 'template' else deck_slides(theme, L)
    print(f'· {which} {theme.key}: {len(slides)} slides, {len(L)} layouts')
    qa_fit(slides, label=f'{which}-{theme.key}')
    b = PptxBuilder(theme, list(L.values()))
    for S in slides:
        b.add(S)
    if out_pptx:
        b.save(out_pptx)
    if out_html:
        html_deck(slides, theme, out_html, os.path.relpath(os.path.join(ROOT, '00_Fuente_Maestra', 'brand.css'), os.path.dirname(out_html)).replace('\\', '/'),
                  'Oryzz · Plantilla de presentación')
    return slides


if __name__ == '__main__':
    tmp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '_build')
    os.makedirs(tmp, exist_ok=True)
    build(True, 'template', os.path.join(tmp, 'Oryzz_Plantilla_Presentacion_Oscura.pptx'), os.path.join(OUT, 'Oryzz_Plantilla_Presentacion_Previsualizacion.html'))
    build(False, 'template', os.path.join(tmp, 'Oryzz_Plantilla_Presentacion_Clara.pptx'), os.path.join(OUT, 'Oryzz_Plantilla_Presentacion_Clara_Previsualizacion.html'))
    build(True, 'deck', os.path.join(tmp, 'Oryzz_Deck_Comercial_Ejemplo.pptx'), os.path.join(tmp, 'deck.html'))
