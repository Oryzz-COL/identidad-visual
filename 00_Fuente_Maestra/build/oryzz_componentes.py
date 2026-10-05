"""
oryzz_componentes.py · Componentes de dato Oryzz v2.0 (tarjetas KPI, gráficos, chips, eyebrows, botones).

Todos los datos son de EJEMPLO (se marcan con el chip «Ejemplo»). Cambia las cifras en DATA y regenera.
Salida en 05_Elementos_Graficos/05_Componentes_Dato:
  SVG/ (texto vivo) · SVG_contornos/ (texto en trazados) · PNG/ (@2x) · componentes-lamina.png/pdf
Uso:  python oryzz_componentes.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oryzz_svg import C, THEME, ROOT, write, doc, T, text_width, png_from_svg, ruta
import oryzz_iconos as IC

OUT = os.path.join(ROOT, '05_Elementos_Graficos', '05_Componentes_Dato')

KPIS = [
    ('coste-por-lead', 'Coste por lead', '12,40 €', '−18 %', 'vs. mes anterior', 'euro'),
    ('citas', 'Citas agendadas', '46', '+12', 'en 30 días', 'calendario'),
    ('ctr', 'CTR de anuncios', '2,8 %', '+0,6 pp', 'Meta + Google', 'crecimiento'),
    ('resenas', 'Reseñas en Google', '4,8', '+31', 'reseñas nuevas', 'resenas'),
]
LEADS = [18, 22, 19, 27, 31, 29, 36, 41]
CITAS = [6, 8, 7, 10, 12, 11, 14, 16]


def pal(tema):
    t = THEME[tema]
    return dict(t=t, card=t['superficie'] if tema == 'claro' else C['grafito-850'],
                borde=t['borde'] if tema == 'claro' else C['grafito-700'],
                barra=C['grafito-600'] if tema == 'oscuro' else C['grafito-300'],
                guia=C['grafito-800'] if tema == 'oscuro' else C['grafito-100'],
                delta=C['lima-500'] if tema == 'oscuro' else C['grafito-950'])


def icon(name, x, y, size, col, acc=None):
    body = IC.ICONS[name][2].replace('style="color:var(--oz-acento,currentColor)"', f'style="color:{acc or col}"')
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({size / 24:.4f})" style="color:{col}" fill="none" '
            f'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{body}</g>')


def chip(x, y, label, tema, k, kind='neutro', h=32, anchor='start'):
    """Chip/etiqueta. kind: neutro | ejemplo | marcha | canal. Devuelve (svg, ancho)."""
    p = pal(tema); t = p['t']
    size = 14; tr = 0.08
    tw = text_width(label.upper(), 'mono', 500, size, tr)
    dot = kind == 'marcha'
    pad = 14
    w = tw + pad * 2 + (18 if dot else 0)
    if anchor == 'end':
        x = x - w
    if kind == 'ejemplo':
        fill, stroke, col, dash = 'none', t['texto3'], t['texto3'], ' stroke-dasharray="3 3"'
    elif kind == 'marcha':
        fill = C['grafito-800'] if tema == 'oscuro' else C['blanco']
        stroke, col, dash = p['borde'], t['texto'], ''
    else:
        fill = C['grafito-800'] if tema == 'oscuro' else C['blanco']
        stroke, col, dash = p['borde'], t['texto2'], ''
    s = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{fill}" stroke="{stroke}" stroke-width="1"{dash}/>'
    tx = x + pad
    if dot:
        s += f'<circle cx="{x + pad + 4:.1f}" cy="{y + h / 2:.1f}" r="4" fill="{t["nodo"]}"/>'
        tx += 18
    s += T(tx, y + h / 2 + 5, label.upper(), 'mono', 500, size, col, tracking=tr, contornos=k)
    return s, w


# ------------------------------------------------------------------ KPI
def kpi(slug, tema, k):
    p = pal(tema); t = p['t']
    _, lab, val, delta, cap, ic = next(x for x in KPIS if x[0] == slug)
    W, H = 400, 232
    s = f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{p["card"]}" stroke="{p["borde"]}"/>'
    s += icon(ic, 28, 28, 22, t['texto3'])
    s += T(62, 45, lab.upper(), 'mono', 500, 14, t['texto3'], tracking=0.12, contornos=k)
    c, _ = chip(W - 24, 24, 'Ejemplo', tema, k, 'ejemplo', 28, anchor='end'); s += c
    # cifra
    if slug == 'resenas':
        s += T(28, 150, val, 'display', 500, 64, t['texto'], tracking=-0.03, contornos=k)
        vw = text_width(val, 'display', 500, 64, -0.03)
        s += T(28 + vw + 8, 150, '/ 5', 'display', 500, 28, t['texto3'], contornos=k)
    else:
        s += T(28, 150, val, 'display', 500, 64, t['texto'], tracking=-0.03, contornos=k)
    # delta: nodo + texto (en oscuro, texto lima; en claro, texto grafito y nodo lima 600 por contraste)
    s += f'<path d="M28 178H{W - 28}" stroke="{p["guia"]}"/>'
    s += f'<circle cx="34" cy="{202}" r="5" fill="{t["nodo"]}"/>'
    s += T(48, 208, delta, 'mono', 700, 16, p['delta'], contornos=k)
    dw = text_width(delta, 'mono', 700, 16)
    s += T(48 + dw + 10, 208, cap, 'texto', 500, 15, t['texto3'], contornos=k)
    return doc(W, H, s, f'Oryzz · tarjeta KPI · {lab} · {tema} · Ejemplo',
               desc='Datos de ejemplo. Superficie Grafito 850, borde 1 px, radio 20, eyebrow mono, cifra Space Grotesk 500, delta con nodo lima.')


# ------------------------------------------------------------------ gráficos
def grafico(tipo, tema, k):
    p = pal(tema); t = p['t']
    W, H = 640, 340
    s = f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{p["card"]}" stroke="{p["borde"]}"/>'
    datos = LEADS if tipo == 'linea' else CITAS
    tit = 'Leads por semana' if tipo == 'linea' else 'Citas por semana'
    s += T(28, 46, tit.upper(), 'mono', 500, 14, t['texto3'], tracking=0.12, contornos=k)
    c, _ = chip(W - 24, 24, 'Ejemplo', tema, k, 'ejemplo', 28, anchor='end'); s += c
    last = datos[-1]
    s += T(28, 104, str(last), 'display', 500, 44, t['texto'], tracking=-0.03, contornos=k)
    lw = text_width(str(last), 'display', 500, 44, -0.03)
    s += T(28 + lw + 12, 104, 'esta semana', 'texto', 500, 15, t['texto3'], contornos=k)
    X0, X1, Y0, Y1 = 40, W - 40, 140, 280
    vmax = max(datos) * 1.15
    for g in range(4):
        y = Y1 - (Y1 - Y0) * g / 3
        s += f'<path d="M{X0} {y:.1f}H{X1}" stroke="{p["guia"]}" stroke-width="1"/>'
    n = len(datos)
    xs = [X0 + 16 + (X1 - X0 - 32) * i / (n - 1) for i in range(n)]
    for i, x in enumerate(xs):
        s += T(x, Y1 + 30, f'S{i + 1}', 'mono', 500, 14, t['texto3'], anchor='middle', contornos=k)
    if tipo == 'linea':
        pts = [(x, Y1 - (Y1 - Y0) * v / vmax) for x, v in zip(xs, datos)]
        d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts[:-1])
        # el trazo se corta antes del último nodo (como el isotipo)
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        L = math.hypot(xb - xa, yb - ya); cut = 14
        xe, ye = xb - (xb - xa) / L * cut, yb - (yb - ya) / L * cut
        d += f'L{xe:.1f} {ye:.1f}'
        s += f'<path d="{d}" fill="none" stroke="{t["texto2"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        for x, y in pts[:-1]:
            s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{p["card"]}" stroke="{t["texto3"]}" stroke-width="1.5"/>'
        s += f'<circle cx="{xb:.1f}" cy="{yb:.1f}" r="16" fill="none" stroke="{t["nodo"]}" stroke-width="1.25" opacity=".5"/>'
        s += f'<circle cx="{xb:.1f}" cy="{yb:.1f}" r="6" fill="{t["nodo"]}"/>'
    else:
        bw = 28
        for i, (x, v) in enumerate(zip(xs, datos)):
            h = (Y1 - Y0) * v / vmax
            col = t['nodo'] if i == n - 1 else p['barra']
            s += (f'<path d="M{x - bw / 2:.1f} {Y1}V{Y1 - h + 6:.1f}A6 6 0 0 1 {x - bw / 2 + 6:.1f} {Y1 - h:.1f}'
                  f'H{x + bw / 2 - 6:.1f}A6 6 0 0 1 {x + bw / 2:.1f} {Y1 - h + 6:.1f}V{Y1}Z" fill="{col}"/>')
    return doc(W, H, s, f'Oryzz · gráfico de {"línea" if tipo == "linea" else "barras"} · {tit} · {tema} · Ejemplo',
               desc='Datos de ejemplo. Un solo acento: el último dato en lima.')


# ------------------------------------------------------------------ chips y eyebrows
CHIPS = [('en-marcha', 'En marcha', 'marcha'), ('ejemplo', 'Ejemplo', 'ejemplo'), ('meta-ads', 'Meta Ads', 'neutro'),
         ('google-ads', 'Google Ads', 'neutro'), ('tiktok-ads', 'TikTok Ads', 'neutro'), ('geo', 'GEO · IA', 'neutro'),
         ('nuevo-lead', 'Nuevo lead', 'neutro'), ('pausado', 'Pausado', 'neutro')]


def chip_svg(slug, tema, k):
    _, lab, kind = next(c for c in CHIPS if c[0] == slug)
    s, w = chip(1, 1, lab, tema, k, kind)
    return doc(math.ceil(w + 2), 34, s, f'Oryzz · chip · {lab} · {tema}')


EYEBROWS = [('linea', 'Método Oryzz'), ('nodo', 'En marcha'), ('numero', 'Captación')]


def eyebrow_svg(slug, tema, k, num='01'):
    t = THEME[tema]
    lab = dict(EYEBROWS)[slug].upper()
    size, tr = 14, 0.16
    tw = text_width(lab, 'mono', 500, size, tr)
    if slug == 'linea':
        s = f'<path d="M0 12H28" stroke="{t["texto3"]}" stroke-width="1.5"/>' + T(40, 17, lab, 'mono', 500, size, t['texto3'], tracking=tr, contornos=k)
        w = 40 + tw
    elif slug == 'nodo':
        s = f'<circle cx="5" cy="12" r="5" fill="{t["nodo"]}"/>' + T(20, 17, lab, 'mono', 500, size, t['texto2'], tracking=tr, contornos=k)
        w = 20 + tw
    else:
        nw = text_width(num + ' / ', 'mono', 500, size, tr)
        s = (T(0, 17, num + ' / ', 'mono', 500, size, t['texto'], tracking=tr, contornos=k)
             + T(nw, 17, lab, 'mono', 500, size, t['texto3'], tracking=tr, contornos=k))
        w = nw + tw
    return doc(math.ceil(w + 2), 24, s, f'Oryzz · eyebrow · {lab.lower()} · {tema}')


# ------------------------------------------------------------------ botones
BOTONES = [('primario-oscuro', 'oscuro', 'Reserva tu valoración'), ('primario-claro', 'claro', 'Reserva tu valoración'),
           ('secundario-oscuro', 'oscuro', 'Ver el método'), ('secundario-claro', 'claro', 'Ver el método')]


def boton(slug, k, talla='M'):
    tema = next(b[1] for b in BOTONES if b[0] == slug); lab = next(b[2] for b in BOTONES if b[0] == slug)
    t = THEME[tema]
    h, fs, pad, isz = (48, 16, 22, 18) if talla == 'M' else (60, 18, 28, 20)
    tw = text_width(lab, 'texto', 700, fs)
    w = pad + tw + 12 + isz + pad
    defs = ''
    if slug == 'primario-oscuro':
        defs = (f'<linearGradient id="bg{talla}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="{w}">'
                f'<stop offset="0" stop-color="{C["azul-400"]}"/><stop offset="1" stop-color="{C["cyan-500"]}"/></linearGradient>')
        bg, col, st = f'url(#bg{talla})', C['grafito-950'], ''
    elif slug == 'primario-claro':
        bg, col, st = C['azul-600'], C['blanco'], ''
    elif slug == 'secundario-oscuro':
        bg, col, st = 'none', C['blanco'], f' stroke="{C["grafito-600"]}" stroke-width="1.5"'
    else:
        bg, col, st = 'none', C['grafito-950'], f' stroke="{C["grafito-300"]}" stroke-width="1.5"'
    s = f'<rect x="1" y="1" width="{w:.1f}" height="{h}" rx="14" fill="{bg}"{st}/>'
    s += T(1 + pad, 1 + h / 2 + fs * 0.36, lab, 'texto', 700, fs, col, contornos=k)
    s += icon('flecha', 1 + pad + tw + 12, 1 + (h - isz) / 2, isz, col)
    return doc(math.ceil(w + 2), h + 2, s, f'Oryzz · botón {slug} · {talla} · «{lab}»', defs=defs,
               desc={'primario-oscuro': 'Gradiente IA oscuro 135° + texto Grafito 950 (contraste 6,1–10,3:1).',
                     'primario-claro': 'Azul 600 + texto blanco (6,0:1).'}.get(slug, 'Contorno 1,5 px.'))


# ------------------------------------------------------------------ build
def build():
    items = []  # (subcarpeta/nombre, fn(k) -> svg, ancho px del svg)
    for tema in ('oscuro', 'claro'):
        for slug, *_ in KPIS:
            items.append((f'kpi/oryzz-kpi_{slug}_{tema}', lambda k, s=slug, tm=tema: kpi(s, tm, k), 400))
        for tipo in ('linea', 'barras'):
            items.append((f'graficos/oryzz-grafico-{tipo}_{tema}', lambda k, ty=tipo, tm=tema: grafico(ty, tm, k), 640))
        for slug, *_ in CHIPS:
            items.append((f'chips/oryzz-chip_{slug}_{tema}', lambda k, s=slug, tm=tema: chip_svg(s, tm, k), None))
        for slug, _ in EYEBROWS:
            items.append((f'eyebrows/oryzz-eyebrow_{slug}_{tema}', lambda k, s=slug, tm=tema: eyebrow_svg(s, tm, k), None))
    for slug, *_ in BOTONES:
        for talla in ('M', 'L'):
            items.append((f'botones/oryzz-boton_{slug}_{talla}', lambda k, s=slug, ta=talla: boton(s, k, ta), None))
    jobs = []
    import re
    for rel, fn, w in items:
        write(os.path.join(OUT, 'SVG', rel + '.svg'), fn(False))
        sp = os.path.join(OUT, 'SVG_contornos', rel + '_contornos.svg')
        svg = fn(True); write(sp, svg)
        vw = float(re.search(r'viewBox="0 0 ([\d.]+)', svg).group(1))
        jobs.append((sp, os.path.join(OUT, 'PNG', rel + '@2x.png'), int(round(vw * 2))))
    png_from_svg(jobs)
    return items


def lamina():
    from render import html_to_png, html_to_pdf
    base = 'SVG_contornos'

    def img(rel, w=None):
        st = f' style="width:{w}px"' if w else ''
        return f'<img src="{base}/{rel}_contornos.svg"{st}>'
    halves = ''
    for tema in ('oscuro', 'claro'):
        kp = ''.join(img(f'kpi/oryzz-kpi_{s}_{tema}', 400) for s, *_ in KPIS)
        gr = img(f'graficos/oryzz-grafico-linea_{tema}', 560) + img(f'graficos/oryzz-grafico-barras_{tema}', 560)
        ch = ''.join(img(f'chips/oryzz-chip_{s}_{tema}') for s, *_ in CHIPS)
        ey = ''.join(img(f'eyebrows/oryzz-eyebrow_{s}_{tema}') for s, _ in EYEBROWS)
        bt = ''.join(img(f'botones/oryzz-boton_{s}_{ta}') for s, tm, _ in BOTONES if tm == tema for ta in ('L', 'M'))
        halves += (f'<section class="{tema}"><p class="t-eyebrow">Sobre {tema}</p>'
                   f'<div class="row kpi">{kp}</div><div class="row gr">{gr}<div class="col"><p class="t-eyebrow">Botones</p>'
                   f'<div class="bt">{bt}</div><p class="t-eyebrow">Chips</p><div class="ch">{ch}</div>'
                   f'<p class="t-eyebrow">Eyebrows</p><div class="ch ey">{ey}</div></div></div></section>')
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Componentes de dato Oryzz</title>
<link rel="stylesheet" href="../../00_Fuente_Maestra/brand.css"><style>
@page{{size:1920px 2250px;margin:0}} *{{box-sizing:border-box}} html,body{{margin:0}}
body{{width:1920px;height:2250px;font-family:var(--font-texto);background:var(--grafito-950)}}
header{{padding:104px 120px 48px;color:#fff}} header h1{{font-family:var(--font-display);font-size:72px;letter-spacing:-.04em;margin:18px 0 12px;line-height:1}}
header p{{color:var(--grafito-200);font-size:20px;margin:0;max-width:1000px}}
.t-eyebrow{{color:var(--grafito-400);margin:0 0 16px}}
section{{padding:48px 120px 56px}} section.claro{{background:#fff}} section.claro .t-eyebrow{{color:var(--grafito-500)}}
.row{{display:flex;gap:32px;align-items:flex-start}} .kpi{{margin-bottom:32px}} .gr .col{{display:flex;flex-direction:column;gap:0;margin-left:8px}}
.bt{{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin-bottom:28px;max-width:500px}} .ch{{display:flex;flex-wrap:wrap;gap:10px;max-width:460px;margin-bottom:28px}} .ey{{gap:28px}}
img{{display:block}}
</style></head><body><header><p class="t-eyebrow">Oryzz · 05 · Elementos gráficos · 05 Componentes de dato</p>
<h1>Componentes de dato</h1><p>Tarjetas KPI, gráficos, chips, eyebrows y botones. Todas las cifras son de ejemplo y lo dicen. Un acento por componente: el nodo lima.</p></header>
{halves}</body></html>'''
    hp = os.path.join(OUT, 'componentes-lamina.html'); write(hp, page)
    html_to_png(hp, os.path.join(OUT, 'componentes-lamina.png'), 1920, 2250)
    html_to_pdf(hp, os.path.join(OUT, 'componentes-lamina.pdf'))


if __name__ == '__main__':
    it = build(); lamina(); print(len(it), 'componentes')
