"""
Láminas de construcción y uso del logo (02_Logos/09_Construccion_y_Uso).
SVG con todo el texto vectorizado (portables a Figma / Illustrator / guía) + PNG a 2x.

Uso:  python diagramas_uso.py
"""
import math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oryzz_logo as L
from svg_text import text, measure, MISSING
from render_fast import Chrome

LOGOS = os.path.abspath(os.path.join(HERE, '..', '..', '02_Logos'))
OUT = os.path.join(LOGOS, '09_Construccion_y_Uso')
W, H = 1600, 1000
MX = 96

THEMES = {
    'oscuro': dict(bg='#0B0D12', card='#12151D', card2='#171B25', line='#232836', grid='#171B25', txt='#FFFFFF', txt2='#D5D9E0',
                   txt3='#8A90A0', acc='#5C8BFF', lime='#BFF24A', err='#E5484D', way='color-sobre-oscuro', solid='solido-sobre-oscuro',
                   construct='#FFFFFF'),
    'claro': dict(bg='#FFFFFF', card='#F6F7F9', card2='#E5E8EE', line='#D5D9E0', grid='#EEF0F4', txt='#0B0D12', txt2='#3A4152',
                  txt3='#5A6172', acc='#2C5BD0', lime='#7FB02E', err='#E5484D', way='color-sobre-claro', solid='solido-sobre-claro',
                  construct='#0B0D12'),
}

A_END = L.A_NODE + math.degrees(2 * math.asin((L.NR + L.SW / 2 + 2.5) / (2 * L.R)))
ARC = 360 - (A_END - L.A_LEFT)
GAP = A_END - L.A_LEFT


def es(v, nd=1):
    return (f'{v:.{nd}f}').replace('.', ',')


# ------------------------------------------------------------------ utilidades
_uid = [0]


def embed(path_or_svg, x, y, w=None, h=None, vb=None, extra='', par='xMidYMid meet', repl=None):
    """Inserta un SVG maestro como <svg> anidado con ids únicos."""
    s = open(path_or_svg, encoding='utf8').read() if path_or_svg.endswith('.svg') else path_or_svg
    for a, b in (repl or {}).items():
        s = s.replace(a, b)
    _uid[0] += 1; p = f'e{_uid[0]}_'
    s = re.sub(r'<title>.*?</title>', '', s)
    s = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', s)
    s = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m.group(1)})', s)
    ovb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    vb = vb or ovb
    if w and not h: h = w * vb[3] / vb[2]
    if h and not w: w = h * vb[2] / vb[3]
    inner = s[s.index('>', s.index('<svg')) + 1: s.rindex('</svg>')]
    return (f'<svg x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" viewBox="{" ".join(f"{v:.2f}" for v in vb)}" '
            f'preserveAspectRatio="{par}" overflow="visible"{extra}>{inner}</svg>'), w, h


def logo(rel):
    return os.path.join(LOGOS, rel)


def frame(T, n, total, eyebrow, title, note=''):
    s = f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>'
    s += text(eyebrow, 'texto-semibold', 15, MX, 104, T['txt3'])
    s += text(title, 'display-bold', 46, MX, 164, T['txt'], tracking=-0.03)
    if note:
        s += text(note, 'texto-medium', 15, W - MX, 104, T['txt3'], anchor='end')
    s += f'<line x1="{MX}" y1="198" x2="{W - MX}" y2="198" stroke="{T["line"]}" stroke-width="1"/>'
    s += f'<line x1="{MX}" y1="{H - 88}" x2="{W - MX}" y2="{H - 88}" stroke="{T["line"]}" stroke-width="1"/>'
    s += text('Sistema de logo de Oryzz v2.0', 'texto-medium', 14, MX, H - 52, T['txt3'])
    s += text(f'{n} / {total}', 'texto-medium', 14, W - MX, H - 52, T['txt3'], anchor='end')
    return s


def doc(body, title):
    # tamaño intrínseco = tamaño de exportación (2x): etiquetas mínimas de 12 u -> 24 px (BRAND_SPEC §8.8, ≥ 18 px)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W * 2}" height="{H * 2}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def callout(T, n, x, y, lx=None, ly=None):
    s = ''
    if lx is not None:
        s += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="{T["acc"]}" stroke-width="1.25"/>'
        s += f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="2.6" fill="{T["acc"]}"/>'
    s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="{T["bg"]}" stroke="{T["acc"]}" stroke-width="1.25"/>'
    s += text(str(n), 'mono-medium', 12, x, y + 4.3, T['acc'], anchor='middle')
    return s


# ------------------------------------------------------------------ 01 construcción
def construccion(T):
    u = 6.2; bx, by = 190, 250
    P = lambda ux, uy: (bx + ux * u, by + uy * u)
    pol = lambda a, r: P(L.CX + r * math.cos(math.radians(a)), L.CY + r * math.sin(math.radians(a)))
    s = frame(T, 1, 4, 'Logo', 'Construcción del isotipo', 'Geometría exacta, generada con oryzz_logo.py')
    # retícula 10 u
    g = ''
    for i in range(11):
        x, _ = P(i * 10, 0); _, y = P(0, i * 10)
        g += f'<line x1="{x:.1f}" y1="{by}" x2="{x:.1f}" y2="{by + 100 * u:.1f}"/><line x1="{bx}" y1="{y:.1f}" x2="{bx + 100 * u:.1f}" y2="{y:.1f}"/>'
    s += f'<g stroke="{T["line"]}" stroke-width="1">{g}</g>'
    s += f'<rect x="{bx}" y="{by}" width="{100 * u}" height="{100 * u}" fill="none" stroke="{T["txt3"]}" stroke-opacity=".5" stroke-width="1"/>'
    s += text('100 u', 'mono', 12, bx + 50 * u, by - 12, T['txt3'], anchor='middle')
    s += text('0', 'mono', 12, bx - 10, by + 4, T['txt3'], anchor='end')
    # isotipo maestro (misma función que genera los SVG)
    way = L.WAYS[T['way']]
    cu = L.uid_for('lamina-construccion', T['way'])
    s += L._defs(way, cu, (10, 10, 90, 90), None) + L.mark_group(way, cu, bx, by, u)
    c = T['construct']
    cx, cy = P(50, 50)
    # círculos: eje, interior, exterior
    s += f'<circle cx="{cx}" cy="{cy}" r="{L.R * u:.2f}" fill="none" stroke="{c}" stroke-opacity=".7" stroke-width="1" stroke-dasharray="5 4"/>'
    for r in (L.R - L.SW / 2, L.R + L.SW / 2):
        s += f'<circle cx="{cx}" cy="{cy}" r="{r * u:.2f}" fill="none" stroke="{c}" stroke-opacity=".28" stroke-width="1"/>'
    # ejes
    s += f'<line x1="{cx}" y1="{by}" x2="{cx}" y2="{by + 100 * u}" stroke="{c}" stroke-opacity=".3" stroke-width="1" stroke-dasharray="2 4"/>'
    s += f'<line x1="{bx}" y1="{cy}" x2="{bx + 100 * u}" y2="{cy}" stroke="{c}" stroke-opacity=".3" stroke-width="1" stroke-dasharray="2 4"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="3" fill="{c}"/>'
    # radios a inicio, nodo y fin
    for a in (L.A_LEFT, L.A_NODE, A_END):
        x2, y2 = pol(a, L.R)
        s += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{T["acc"]}" stroke-width="1"/>'
        s += f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="2.6" fill="{T["acc"]}"/>'
    # arcos de ángulo
    def arc(a0, a1, r, **kw):
        x0, y0 = pol(a0, r); x1, y1 = pol(a1, r)
        large = 1 if abs(a1 - a0) > 180 else 0; sweep = 1 if a1 > a0 else 0
        return f'<path d="M{x0:.1f} {y0:.1f}A{r * u:.1f} {r * u:.1f} 0 {large} {sweep} {x1:.1f} {y1:.1f}" fill="none" stroke="{T["acc"]}" stroke-width="1.25" {" ".join(f"{k.replace("_", "-")}={chr(34)}{v}{chr(34)}" for k, v in kw.items())}/>'
    s += arc(-90, L.A_LEFT, 12) + arc(-90, L.A_NODE, 12) + arc(-90, A_END, 19)
    lx, ly = pol(-103, 16.5); s += text('25,1°', 'mono', 12, lx, ly + 4, T['txt2'], anchor='middle')
    lx, ly = pol(-77, 16.5); s += text('25,1°', 'mono', 12, lx, ly + 4, T['txt2'], anchor='middle')
    lx, ly = pol(-52, 23.5); s += text(es(90 + A_END) + '°', 'mono', 12, lx + 4, ly + 4, T['txt2'], anchor='start')
    # hueco (arco exterior discontinuo)
    s += arc(A_END, L.A_LEFT, 45, stroke_dasharray='3 4')
    # corte: holgura alrededor del nodo
    nx, ny = P(*L.NODE)
    s += f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{(L.NR + 2.5) * u:.1f}" fill="none" stroke="{c}" stroke-opacity=".7" stroke-width="1" stroke-dasharray="3 3"/>'
    # cota del radio (0°)
    x1, y1 = P(50, 50); x2, y2 = P(84, 50)
    s += f'<line x1="{x1}" y1="{y1 - 0}" x2="{x2}" y2="{y2}" stroke="{T["acc"]}" stroke-width="1.25"/>'
    s += f'<line x1="{x2}" y1="{y2 - 6}" x2="{x2}" y2="{y2 + 6}" stroke="{T["acc"]}" stroke-width="1.25"/>'
    # cota del trazo (180°)
    xa, ya = P(L.CX - L.R - L.SW / 2, 50); xb, yb = P(L.CX - L.R + L.SW / 2, 50)
    s += f'<g stroke="{c}" stroke-width="1.5"><line x1="{xa}" y1="{ya - 9}" x2="{xa}" y2="{ya + 9}"/><line x1="{xb}" y1="{yb - 9}" x2="{xb}" y2="{yb + 9}"/><line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}"/></g>'
    # llamadas numeradas
    s += callout(T, 1, *P(66, 44), *P(66, 50))
    s += callout(T, 2, *P(3.5, 50), *P(L.CX - L.R - L.SW / 2, 50))
    s += callout(T, 3, *P(20, 8), *pol(L.A_LEFT - 12, L.R + L.SW / 2))
    s += callout(T, 4, *P(52, 13.5), *P(L.NODE[0] - L.NR, L.NODE[1]))
    ex, ey = L.pt(A_END); k = (L.NR + 1.25) / 15.5
    mid = (L.NODE[0] + (ex - L.NODE[0]) * k, L.NODE[1] + (ey - L.NODE[1]) * k)
    s += callout(T, 5, *P(90, 12), *P(*mid))
    s += callout(T, 6, *pol(-90, 45))
    # columna derecha: especificaciones
    rows = [
        ('Radio de la órbita', '34 u', 'Medido al eje del trazo · caja de 100 × 100 u'),
        ('Grosor del trazo', '11 u · 11 %', 'Isotipo pequeño (≤ 24 px): 14 u'),
        ('Puntas', 'Redondas · r 5,5 u', 'Radio igual a medio trazo'),
        ('Nodo', 'Diámetro 15 u', 'Centro sobre el eje, a 25,1° de la vertical'),
        ('Corte entre nodo y trazo', '2,5 u', 'Una tinta, bordado y láser sin empastes'),
        ('Arco', f'{es(ARC)}° · hueco {es(GAP)}°', f'Entre centros de puntas · ≈ {es(ARC + 2 * math.degrees(L.SW / 2 / L.R), 0)}° visibles'),
    ]
    x0 = 928; y = 262
    for i, (k, v, n) in enumerate(rows, 1):
        s += callout(T, i, x0 + 12, y + 2)
        s += text(k, 'texto-semibold', 14, x0 + 44, y + 6, T['txt3'])
        s += text(v, 'display-medium', 26, x0 + 44, y + 44, T['txt'], tracking=-0.02)
        s += text(n, 'texto', 15, x0 + 44, y + 70, T['txt3'])
        if i < len(rows):
            s += f'<line x1="{x0 + 44}" y1="{y + 90}" x2="{W - MX}" y2="{y + 90}" stroke="{T["line"]}"/>'
        y += 104
    return doc(s, 'Oryzz · Construcción del isotipo')


# ------------------------------------------------------------------ 02 área de respeto
def respeto(T, c):
    s = frame(T, 2, 4, 'Logo', 'Área de respeto', 'Mínimo alrededor del logo')
    hp = logo(f'01_Horizontal/SVG/oryzz-logo-horizontal_{T["way"]}.svg')
    x0, y0, x1, y1 = c.bbox(hp)
    zx = 496.0                                        # altura de la «z» (x del wordmark)
    B = 0.5 * L.XH + 1.7 * L.XH / 2 + 4               # línea base del lockup maestro
    sc = 700 / (x1 - x0); X = zx * sc
    zw = (x1 - x0) * sc + 2 * X; zh = (y1 - y0) * sc + 2 * X
    ox, oy = MX + 24, 300
    # zona de respeto
    s += f'<rect x="{ox}" y="{oy}" width="{zw:.1f}" height="{zh:.1f}" fill="{T["acc"]}" fill-opacity=".07" stroke="{T["acc"]}" stroke-width="1.25" stroke-dasharray="6 5"/>'
    lx, ly = ox + X, oy + X
    s += f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{(x1 - x0) * sc:.1f}" height="{(y1 - y0) * sc:.1f}" fill="none" stroke="{T["txt3"]}" stroke-opacity=".6" stroke-width="1"/>'
    el, _, _ = embed(hp, lx, ly, (x1 - x0) * sc, vb=(x0, y0, x1 - x0, y1 - y0))
    s += el
    # guías de altura de la «z» hasta la zona derecha
    ztop = ly + (B - zx - y0) * sc; zbase = ly + (B - y0) * sc
    for yy in (ztop, zbase):
        s += f'<line x1="{lx + (x1 - x0) * sc * 0.62:.1f}" y1="{yy:.1f}" x2="{ox + zw:.1f}" y2="{yy:.1f}" stroke="{T["acc"]}" stroke-width="1" stroke-dasharray="2 3"/>'
    # módulos x en los cuatro lados
    def mod(x, y):
        return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{X:.1f}" height="{X:.1f}" fill="{T["acc"]}" fill-opacity=".14" stroke="{T["acc"]}" stroke-width="1.25"/>'
                + text('x', 'display-medium', 22, x + X / 2, y + X / 2 + 7, T['acc'], anchor='middle'))
    s += mod(ox + zw - X, ztop)                              # derecha, alineado con la «z»
    s += mod(ox, oy + zh / 2 - X / 2)                        # izquierda
    s += mod(lx + (x1 - x0) * sc * 0.42, oy)                 # arriba
    s += mod(lx + (x1 - x0) * sc * 0.42, oy + zh - X)        # abajo
    # pie de la zona
    s += text('Logo horizontal y vertical', 'display-semibold', 22, ox, oy + zh + 48, T['txt'], tracking=-0.01)
    s += text('x = altura de la «z» del wordmark, en los cuatro lados.', 'texto', 16, ox, oy + zh + 76, T['txt3'])
    s += text('También en la submarca «oryzz tap» y en el wordmark solo.', 'texto', 16, ox, oy + zh + 100, T['txt3'])
    # isotipo: 25 % de su ancho
    ip = logo(f'04_Isotipo/SVG/oryzz-isotipo_{T["way"]}.svg')
    iw = 176; m = iw * 0.25
    ix = W - MX - 24 - (iw + 2 * m); iy = oy + (zh - (iw + 2 * m)) / 2
    s += f'<rect x="{ix:.1f}" y="{iy:.1f}" width="{iw + 2 * m:.1f}" height="{iw + 2 * m:.1f}" fill="{T["acc"]}" fill-opacity=".07" stroke="{T["acc"]}" stroke-width="1.25" stroke-dasharray="6 5"/>'
    s += f'<rect x="{ix + m:.1f}" y="{iy + m:.1f}" width="{iw}" height="{iw}" fill="none" stroke="{T["txt3"]}" stroke-opacity=".6"/>'
    # el isotipo maestro tiene 0,5 u de aire en su caja de 80 u: ancho del arte = caja
    el, _, _ = embed(ip, ix + m, iy + m, iw)
    s += el
    # cota 25 %
    yy = iy + iw + 2 * m + 22
    s += f'<g stroke="{T["acc"]}" stroke-width="1.25"><line x1="{ix:.1f}" y1="{yy}" x2="{ix + m:.1f}" y2="{yy}"/><line x1="{ix:.1f}" y1="{yy - 5}" x2="{ix:.1f}" y2="{yy + 5}"/><line x1="{ix + m:.1f}" y1="{yy - 5}" x2="{ix + m:.1f}" y2="{yy + 5}"/></g>'
    s += text('25 %', 'mono-medium', 12, ix + m + 10, yy + 4, T['acc'])
    s += text('Isotipo solo', 'display-semibold', 22, ix, oy + zh + 48, T['txt'], tracking=-0.01)
    s += text('25 % de su ancho por cada lado.', 'texto', 16, ix, oy + zh + 76, T['txt3'])
    s += text('En avatares y app ya va incluido.', 'texto', 16, ix, oy + zh + 100, T['txt3'])
    return doc(s, 'Oryzz · Área de respeto')


# ------------------------------------------------------------------ 03 tamaños mínimos
def minimos(T, c):
    s = frame(T, 3, 4, 'Logo', 'Tamaños mínimos', 'Mostrado a tamaño real (1×)')
    # tarjeta horizontal
    cx0, cy0, cw, ch = MX, 236, 684, 560
    s += f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="20" fill="{T["card"]}" stroke="{T["line"]}"/>'
    s += text('Logo horizontal', 'texto-semibold', 15, cx0 + 32, cy0 + 44, T['txt3'])
    rows = [(88, T['solid'], 'Mínimo en pantalla', '88 px · 22 mm impreso · versión sólida'),
            (120, T['way'], 'Desde 120 px', 'A partir de aquí, versión con gradiente'),
            (240, T['way'], 'Uso habitual', 'Cabeceras web, firmas de documento')]
    y = cy0 + 104
    for w, way, k, n in rows:
        p = logo(f'01_Horizontal/SVG/oryzz-logo-horizontal_{way}.svg')
        x0, y0, x1, y1 = c.bbox(p)
        h = w * (y1 - y0) / (x1 - x0)
        lx = cx0 + 32
        # cota
        s += f'<g stroke="{T["acc"]}" stroke-width="1"><line x1="{lx}" y1="{y}" x2="{lx + w}" y2="{y}"/><line x1="{lx}" y1="{y - 5}" x2="{lx}" y2="{y + 5}"/><line x1="{lx + w}" y1="{y - 5}" x2="{lx + w}" y2="{y + 5}"/></g>'
        s += text(f'{w} px', 'mono-medium', 12, lx + w + 12, y + 4, T['acc'])
        el, _, _ = embed(p, lx, y + 16, w, vb=(x0, y0, x1 - x0, y1 - y0)); s += el
        s += text(k, 'display-semibold', 20, cx0 + 360, y + 14, T['txt'], tracking=-0.01)
        s += text(n, 'texto', 15, cx0 + 360, y + 40, T['txt3'])
        y += max(h, 40) + 92
    # tarjeta isotipo
    ix0 = MX + cw + 32; iw_ = W - MX - ix0
    s += f'<rect x="{ix0}" y="{cy0}" width="{iw_}" height="{ch}" rx="20" fill="{T["card"]}" stroke="{T["line"]}"/>'
    s += text('Isotipo', 'texto-semibold', 15, ix0 + 32, cy0 + 44, T['txt3'])
    x = ix0 + 32; base = cy0 + 210
    for sz, small in ((16, True), (24, True), (32, False), (48, False), (96, False)):
        p = logo(f'04_Isotipo/SVG_tamano_pequeno/oryzz-isotipo-small_{T["way"]}.svg' if small else f'04_Isotipo/SVG/oryzz-isotipo_{T["way"]}.svg')
        el, _, _ = embed(p, x, base - sz, sz); s += el
        s += f'<g stroke="{T["acc"]}" stroke-width="1"><line x1="{x}" y1="{base + 18}" x2="{x + sz}" y2="{base + 18}"/><line x1="{x}" y1="{base + 13}" x2="{x}" y2="{base + 23}"/><line x1="{x + sz}" y1="{base + 13}" x2="{x + sz}" y2="{base + 23}"/></g>'
        s += text(f'{sz}', 'mono-medium', 12, x, base + 44, T['acc'])
        s += text('small' if small else 'normal', 'mono', 12, x, base + 62, T['txt3'])
        x += sz + 44
    s += f'<line x1="{ix0 + 32}" y1="{base + 100}" x2="{ix0 + iw_ - 32}" y2="{base + 100}" stroke="{T["line"]}"/>'
    s += text('Mínimo: 16 px · 5 mm impreso', 'display-semibold', 20, ix0 + 32, base + 144, T['txt'], tracking=-0.01)
    s += text('Hasta 24 px usa «isotipo-small»: trazo reforzado al 14 %', 'texto', 15, ix0 + 32, base + 172, T['txt3'])
    s += text('y nodo de 18 u, para que se lea a tamaño favicon.', 'texto', 15, ix0 + 32, base + 194, T['txt3'])
    # reglas
    ry = cy0 + ch + 44
    rules = ['Menos de 120 px: versión sólida', 'Hasta 24 px: isotipo-small', 'Impreso: 22 mm y 5 mm']
    x = MX
    for r in rules:
        s += f'<circle cx="{x + 4}" cy="{ry - 4}" r="4" fill="{T["lime"]}"/>'
        s += text(r, 'texto-semibold', 15, x + 18, ry, T['txt2'])
        x += measure(r, 'texto-semibold', 15) + 64
    return doc(s, 'Oryzz · Tamaños mínimos')


# ------------------------------------------------------------------ 04 usos incorrectos
def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36); rr = r if i % 2 == 0 else r * 0.45
        pts.append(f'{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}')
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def incorrectos(T, c):
    s = frame(T, 4, 4, 'Logo', 'Usos incorrectos', 'Esto no se hace')
    dark = T['way'] == 'color-sobre-oscuro'
    hp = logo(f'01_Horizontal/SVG/oryzz-logo-horizontal_{T["way"]}.svg')
    x0, y0, x1, y1 = c.bbox(hp); vbh = (x0, y0, x1 - x0, y1 - y0)
    tp = logo(f'07_Submarca_Tap/SVG/oryzz-tap-horizontal_{T["way"]}.svg')
    tb = c.bbox(tp); vbt = (tb[0], tb[1], tb[2] - tb[0], tb[3] - tb[1])
    cols, gap = 4, 24
    tw = (W - 2 * MX - (cols - 1) * gap) / cols; th = 236
    lw = 224; lh = lw * vbh[3] / vbh[2]
    grad = ('#5C8BFF', '#36CFE0', '#BFF24A') if dark else ('#3B72FF', '#17A9C2', '#7FB02E')

    def tile(i, title, note, content, bg=None):
        col, row = i % cols, i // cols
        x = MX + col * (tw + gap); y = 232 + row * (th + 104)
        t = f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{th}" rx="16" fill="{bg or T["card"]}" stroke="{T["line"]}"/>'
        t += f'<svg x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{th}" overflow="hidden">{content(tw, th)}</svg>'
        # tachado
        t += f'<line x1="{x + 28:.1f}" y1="{y + th - 28}" x2="{x + tw - 28:.1f}" y2="{y + 28}" stroke="{T["err"]}" stroke-width="2.5" stroke-linecap="round"/>'
        t += f'<circle cx="{x + 26:.1f}" cy="{y + 26}" r="12" fill="{T["err"]}"/>'
        t += f'<g stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"><line x1="{x + 21.5:.1f}" y1="{y + 21.5}" x2="{x + 30.5:.1f}" y2="{y + 30.5}"/><line x1="{x + 30.5:.1f}" y1="{y + 21.5}" x2="{x + 21.5:.1f}" y2="{y + 30.5}"/></g>'
        t += text(title, 'texto-semibold', 16, x, y + th + 32, T['txt'])
        t += text(note, 'texto', 15, x, y + th + 56, T['txt3'])
        return t

    def centered(el_fn, w, h):
        return lambda TW, TH: el_fn((TW - w) / 2, (TH - h) / 2)

    # 1 estirado
    s += tile(0, 'No estirar', 'Escala siempre en proporción.',
              lambda TW, TH: embed(hp, (TW - 290) / 2, (TH - 38) / 2, 290, 38, vb=vbh, par='none')[0])
    # 2 rotado
    s += tile(1, 'No rotar', 'Solo gira en la animación oficial.',
              lambda TW, TH: f'<g transform="rotate(-14 {TW / 2} {TH / 2})">{embed(hp, (TW - lw) / 2, (TH - lh) / 2, lw, vb=vbh)[0]}</g>')
    # 3 colores
    repl = {grad[0]: '#F2A33A', grad[1]: '#E5484D', grad[2]: '#1F9D55'}
    s += tile(2, 'No cambiar colores', 'Solo los diez colorways oficiales.',
              lambda TW, TH: embed(hp, (TW - lw) / 2, (TH - lh) / 2, lw, vb=vbh, repl=repl)[0])
    # 4 sombra
    def sombra(TW, TH):
        f = (f'<defs><filter id="oryzz-lamina-sombra-{T["way"]}" x="-30%" y="-60%" width="160%" height="220%">'
             '<feDropShadow dx="5" dy="7" stdDeviation="4" flood-color="#000" flood-opacity=".75"/>'
             f'<feDropShadow dx="0" dy="0" stdDeviation="9" flood-color="{grad[1]}" flood-opacity=".9"/></filter></defs>')
        return f + f'<g filter="url(#oryzz-lamina-sombra-{T["way"]})">{embed(hp, (TW - lw) / 2, (TH - lh) / 2, lw, vb=vbh)[0]}</g>'
    s += tile(3, 'Sin sombras ni brillos', 'Nada de sombras, contornos ni glow.', sombra)
    # 5 contraste
    mb = logo('01_Horizontal/SVG/oryzz-logo-horizontal_mono-blanco.svg')
    s += tile(4, 'Contraste suficiente', 'Nunca sobre fondos que lo apaguen.',
              lambda TW, TH: embed(mb, (TW - lw) / 2, (TH - lh) / 2, lw, vb=vbh)[0], bg='#D5D9E0')
    # 6 estrellas Tap
    def estrellas(TW, TH):
        tw_ = 250; th_ = tw_ * vbt[3] / vbt[2]
        x = (TW - tw_) / 2; y = (TH - th_) / 2 + 14
        st = ''.join(star(x + tw_ - 64 + k * 13, y - 12, 6, '#F2A33A') for k in range(5))
        return embed(tp, x, y, tw_, vb=vbt)[0] + st
    s += tile(5, 'Sin las estrellas de Tap', 'El logo antiguo de Tap queda obsoleto.', estrellas)
    # 7 mayúsculas
    def mayus(TW, TH):
        iso = logo(f'04_Isotipo/SVG/oryzz-isotipo_{T["way"]}.svg')
        size = 52
        wtxt = measure('ORYZZ', 'display-bold', size, -0.03)
        total = 56 + 14 + wtxt; x = (TW - total) / 2; yb = TH / 2 + size * 0.36
        el = embed(iso, x, TH / 2 - 28, 56)[0]
        return (el + text('ORY', 'display-bold', size, x + 70, yb, '#FFFFFF' if dark else '#0B0D12', tracking=-0.03)
                + text('ZZ', 'display-bold', size, x + 70 + measure('ORY', 'display-bold', size, -0.03) + size * -0.03, yb, grad[0], tracking=-0.03))
    s += tile(6, 'Siempre en minúscula', '«ORYZZ» y «OryzzTAP» no existen.', mayus)
    # 8 nodo fuera de sitio
    nx, ny = L.CX, L.CY; onx, ony = L.NODE
    moved = {f'cx="{onx:.2f}" cy="{ony:.2f}"': f'cx="{nx:.2f}" cy="{ny:.2f}"'}
    s += tile(7, 'No mover el nodo', 'Vive en el hueco superior de la órbita.',
              lambda TW, TH: embed(hp, (TW - lw) / 2, (TH - lh) / 2, lw, vb=vbh, repl=moved)[0])
    return doc(s, 'Oryzz · Usos incorrectos')


# ------------------------------------------------------------------ main
class _C:
    def __init__(self, chrome):
        self.c = chrome; self.cache = {}

    def bbox(self, p):
        if p not in self.cache:
            from export_logos import content_bbox
            self.cache[p] = content_bbox(self.c, p)
        return self.cache[p]


def main():
    os.makedirs(os.path.join(OUT, 'SVG'), exist_ok=True); os.makedirs(os.path.join(OUT, 'PNG'), exist_ok=True)
    with Chrome() as ch:
        c = _C(ch)
        for tname, T in THEMES.items():
            docs = {
                '01_construccion-isotipo': construccion(T),
                '02_area-de-respeto': respeto(T, c),
                '03_tamanos-minimos': minimos(T, c),
                '04_usos-incorrectos': incorrectos(T, c),
            }
            for name, svg in docs.items():
                fn = f'oryzz-{name}_{tname}'
                sp = os.path.join(OUT, 'SVG', fn + '.svg')
                open(sp, 'w', encoding='utf8').write(svg)
                ch.svg_to_png(sp, os.path.join(OUT, 'PNG', fn + '.png'), W * 2)
    if MISSING:
        print('glifos no disponibles:', MISSING)
    print('ok')


if __name__ == '__main__':
    main()
