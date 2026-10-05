"""
oryzz_svg.py · utilidades comunes para generar piezas gráficas Oryzz v2.0 en SVG.

- Paleta leída de tokens.json (C['grafito-950'], C['lima-500'], ...).
- Texto: T(...) devuelve <text> editable o, con contornos=True, <path> vectorizado
  con las TTF de marca (métricas + kerning GPOS reales) → los SVG se ven igual en
  cualquier sitio aunque no estén instaladas las fuentes.
- Geometría del sistema «Órbita y nodo»: arc(), orbita(), nodo(), ruta().
- Render: png_from_svg() (Chrome headless vía render.py) con paralelismo.

    from oryzz_svg import C, T, text_width, arc, orbita, nodo, ruta, doc, write, png_from_svg
"""
import json, math, os, sys, re
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.normpath(os.path.join(HERE, '..'))
ROOT = os.path.normpath(os.path.join(MASTER, '..'))
FONTDIR = os.path.join(MASTER, 'fonts', 'static')
sys.path.insert(0, HERE)

# ------------------------------------------------------------------ color
_tok = json.load(open(os.path.join(MASTER, 'tokens.json'), encoding='utf8'))
C = {}
for fam, vals in _tok['color'].items():
    for k, v in vals.items():
        C[f'{fam}-{k}'] = v
C['blanco'] = '#FFFFFF'

# Temas semánticos para piezas del sistema gráfico
THEME = {
    'oscuro': dict(
        fondo=C['grafito-950'], superficie=C['grafito-850'], superficie2=C['grafito-800'],
        borde=C['grafito-700'], linea=C['grafito-700'], linea_suave=C['grafito-800'],
        texto=C['blanco'], texto2=C['grafito-200'], texto3=C['grafito-400'],
        acento=C['azul-400'], nodo=C['lima-500'], grad=(C['azul-400'], C['cyan-500']),
        reticula='#FFFFFF', halo=C['azul-500'], icono=C['grafito-200'],
    ),
    'claro': dict(
        fondo=C['blanco'], superficie=C['grafito-50'], superficie2=C['grafito-100'],
        borde=C['grafito-200'], linea=C['grafito-200'], linea_suave=C['grafito-100'],
        texto=C['grafito-950'], texto2=C['grafito-600'], texto3=C['grafito-500'],
        acento=C['azul-500'], nodo=C['lima-600'], grad=(C['azul-500'], C['cyan-600']),
        reticula=C['grafito-950'], halo=C['azul-500'], icono=C['grafito-950'],
    ),
}

# ------------------------------------------------------------------ fuentes
FONTS = {
    ('display', 500): 'SpaceGrotesk-Medium.ttf', ('display', 600): 'SpaceGrotesk-SemiBold.ttf',
    ('display', 700): 'SpaceGrotesk-Bold.ttf', ('display', 400): 'SpaceGrotesk-Regular.ttf',
    ('texto', 400): 'Manrope-Regular.ttf', ('texto', 500): 'Manrope-Medium.ttf',
    ('texto', 600): 'Manrope-SemiBold.ttf', ('texto', 700): 'Manrope-Bold.ttf',
    ('texto', 800): 'Manrope-ExtraBold.ttf',
    ('mono', 400): 'JetBrainsMono-Regular.ttf', ('mono', 500): 'JetBrainsMono-Medium.ttf',
    ('mono', 700): 'JetBrainsMono-Bold.ttf',
}
FAMILY = {
    'display': "'Space Grotesk', Arial, Helvetica, sans-serif",
    'texto': "Manrope, Arial, Helvetica, sans-serif",
    'mono': "'JetBrains Mono', Consolas, 'Courier New', monospace",
}


@lru_cache(None)
def _font(fam, wt):
    f = TTFont(os.path.join(FONTDIR, FONTS[(fam, wt)]))
    return f


@lru_cache(None)
def _kern(fam, wt):
    """Pares de kerning (glifo, glifo) -> unidades, desde GPOS PairPos."""
    f = _font(fam, wt)
    out = {}
    if 'GPOS' not in f:
        return out
    gpos = f['GPOS'].table
    for lk in gpos.LookupList.Lookup:
        subs = lk.SubTable
        for st in subs:
            if lk.LookupType == 9:
                st = st.ExtSubTable
                if st.LookupType != 2:
                    continue
            elif lk.LookupType != 2:
                continue
            if st.Format == 1:
                cov = st.Coverage.glyphs
                for i, ps in enumerate(st.PairSet):
                    for pvr in ps.PairValueRecord:
                        v = getattr(pvr.Value1, 'XAdvance', 0) if pvr.Value1 else 0
                        if v:
                            out.setdefault((cov[i], pvr.SecondGlyph), v)
            elif st.Format == 2:
                cov = st.Coverage.glyphs
                cd1 = st.ClassDef1.classDefs; cd2 = st.ClassDef2.classDefs
                cls2 = {}
                for g, c in cd2.items():
                    cls2.setdefault(c, []).append(g)
                for g1 in cov:
                    c1 = cd1.get(g1, 0)
                    rec = st.Class1Record[c1]
                    for c2, r2 in enumerate(rec.Class2Record):
                        v = getattr(r2.Value1, 'XAdvance', 0) if r2.Value1 else 0
                        if v and c2 in cls2:
                            for g2 in cls2[c2]:
                                out.setdefault((g1, g2), v)
    return out


def _layout(s, fam, wt, size, tracking):
    f = _font(fam, wt); cmap = f.getBestCmap(); hmtx = f['hmtx']
    upm = f['head'].unitsPerEm; sc = size / upm
    kern = _kern(fam, wt)
    x = 0.0; out = []; prev = None
    for ch in s:
        g = cmap.get(ord(ch)) or cmap.get(ord('?'))
        if prev is not None:
            x += kern.get((prev, g), 0) * sc
        out.append((g, x))
        x += hmtx[g][0] * sc + tracking * size
        prev = g
    width = x - (tracking * size if s else 0)
    return out, width, sc


def text_width(s, fam='texto', wt=400, size=16, tracking=0.0):
    return _layout(s, fam, wt, size, tracking)[1]


def cap_height(fam, wt, size):
    f = _font(fam, wt)
    return f['OS/2'].sCapHeight / f['head'].unitsPerEm * size


def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def T(x, y, s, fam='texto', wt=400, size=16, fill='#000', tracking=0.0, anchor='start',
      contornos=False, opacity=None, upper=False, extra=''):
    """Texto en baseline y. tracking en em. Devuelve <text> o <path>."""
    if upper:
        s = s.upper()
    items, width, sc = _layout(s, fam, wt, size, tracking)
    if anchor == 'middle':
        x0 = x - width / 2
    elif anchor == 'end':
        x0 = x - width
    else:
        x0 = x
    op = f' opacity="{opacity}"' if opacity is not None else ''
    if not contornos:
        ta = {'start': '', 'middle': ' text-anchor="middle"', 'end': ' text-anchor="end"'}[anchor]
        ls = f' letter-spacing="{tracking * size:.2f}"' if tracking else ''
        # Chrome añade el letter-spacing también tras el último glifo: compensamos en middle/end
        dx = ''
        if tracking and anchor == 'middle':
            dx = f' dx="{tracking * size / 2:.2f}"'
        elif tracking and anchor == 'end':
            dx = f' dx="{tracking * size:.2f}"'
        return (f'<text x="{x:.2f}" y="{y:.2f}"{dx} font-family="{FAMILY[fam]}" font-weight="{wt}" '
                f'font-size="{size:g}"{ls}{ta} fill="{fill}"{op}{extra}>{_esc(s)}</text>')
    f = _font(fam, wt); gs = f.getGlyphSet()
    pen = SVGPathPen(gs)
    for g, gx in items:
        tp = TransformPen(pen, (sc, 0, 0, -sc, x0 + gx, y))
        gs[g].draw(tp)
    d = pen.getCommands()
    if not d:
        return ''
    return f'<path d="{d}" fill="{fill}"{op}{extra}><title>{_esc(s)}</title></path>'


def wrap(s, fam, wt, size, maxw, tracking=0.0):
    words = s.split(); lines = []; cur = ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if text_width(t, fam, wt, size, tracking) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ geometría
def pol(cx, cy, r, a):
    """Punto en círculo; ángulo en grados, 0 = derecha, positivo = horario (y hacia abajo)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def arc(cx, cy, r, a0, a1):
    """Arco horario de a0 a a1 (grados). Admite > 180°."""
    span = (a1 - a0) % 360 or 360
    if span >= 359.99:
        x0, y0 = pol(cx, cy, r, a0); xm, ym = pol(cx, cy, r, a0 + 180)
        return (f'M{x0:.2f} {y0:.2f}A{r:g} {r:g} 0 1 1 {xm:.2f} {ym:.2f}'
                f'A{r:g} {r:g} 0 1 1 {x0:.2f} {y0:.2f}')
    x0, y0 = pol(cx, cy, r, a0); x1, y1 = pol(cx, cy, r, a0 + span)
    large = 1 if span > 180 else 0
    return f'M{x0:.2f} {y0:.2f}A{r:g} {r:g} 0 {large} 1 {x1:.2f} {y1:.2f}'


def gap_deg(r, dist):
    """Ángulo que ocupa una cuerda de longitud dist en un círculo de radio r."""
    return math.degrees(2 * math.asin(min(1, dist / (2 * r))))


def orbita(cx, cy, r, a_nodo, stroke, sw=1.5, nodo_r=None, nodo_fill=None, abertura=None,
           gap=None, opacity=None, extra=''):
    """Órbita abierta con nodo opcional, como el isotipo: el trazo se corta antes del nodo.
    a_nodo: ángulo del nodo. abertura: grados abiertos en sentido antihorario desde el nodo.
    Si nodo_r es None, sólo se dibuja el arco abierto (abertura por defecto 40°)."""
    ab = abertura if abertura is not None else 40
    if nodo_r:
        g = gap if gap is not None else max(sw * 2.2, 3)
        cut = gap_deg(r, nodo_r + sw / 2 + g)
    else:
        cut = 0
    a_start = a_nodo + cut           # el trazo arranca pasado el nodo (horario)
    a_end = a_nodo - ab              # y termina antes de la abertura
    op = f' opacity="{opacity}"' if opacity is not None else ''
    s = (f'<path d="{arc(cx, cy, r, a_start, a_end)}" fill="none" stroke="{stroke}" '
         f'stroke-width="{sw:g}" stroke-linecap="round"{op}{extra}/>')
    if nodo_r:
        nx, ny = pol(cx, cy, r, a_nodo)
        s += f'<circle cx="{nx:.2f}" cy="{ny:.2f}" r="{nodo_r:g}" fill="{nodo_fill or stroke}"/>'
    return s


def nodo(x, y, r, fill, halo=None, halo_r=None, halo_op=0.14):
    s = ''
    if halo:
        s += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{halo_r or r * 2.6:.2f}" fill="{halo}" opacity="{halo_op}"/>'
    return s + f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:g}" fill="{fill}"/>'


def ruta(pts, rad=12):
    """Polilínea ortogonal con esquinas redondeadas (radio rad)."""
    if len(pts) < 2:
        return ''
    d = f'M{pts[0][0]:.2f} {pts[0][1]:.2f}'
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        l1 = math.hypot(x1 - x0, y1 - y0); l2 = math.hypot(x2 - x1, y2 - y1)
        r = min(rad, l1 / 2, l2 / 2)
        ax = x1 - (x1 - x0) / l1 * r; ay = y1 - (y1 - y0) / l1 * r
        bx = x1 + (x2 - x1) / l2 * r; by = y1 + (y2 - y1) / l2 * r
        cross = (x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1)
        sweep = 1 if cross > 0 else 0
        d += f'L{ax:.2f} {ay:.2f}A{r:g} {r:g} 0 0 {sweep} {bx:.2f} {by:.2f}'
    d += f'L{pts[-1][0]:.2f} {pts[-1][1]:.2f}'
    return d


def grad_lineal(uid, a, b, x1=0, y1=0, x2=1, y2=1, units=None):
    u = f' gradientUnits="{units}"' if units else ''
    return (f'<linearGradient id="{uid}"{u} x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')


def halo(uid, cx, cy, r, color, op=0.16):
    """Halo radial muy sutil (≤ 20 % según BRAND_SPEC §8)."""
    op = min(op, 0.20)
    return (f'<defs><radialGradient id="{uid}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset="0.55" stop-color="{color}" stop-opacity="{op * 0.35:.3f}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{uid})"/>')


def reticula(uid, w, h, paso=64, color='#FFFFFF', op=0.035, fade=True, fx=None, fy=None, fr=None,
             x0=0, y0=0, cruces=0, cruz_op=None):
    """Retícula técnica de `paso` px, desvanecida con máscara radial. cruces: cada n celdas, marca +."""
    fx = w * 0.5 if fx is None else fx; fy = h * 0.5 if fy is None else fy
    fr = fr or max(w, h) * 0.62
    d = []
    x = x0 % paso
    while x <= w:
        d.append(f'M{x:.1f} 0V{h}'); x += paso
    y = y0 % paso
    while y <= h:
        d.append(f'M0 {y:.1f}H{w}'); y += paso
    s = ''
    m = ''
    if fade:
        s += (f'<defs><radialGradient id="{uid}g" cx="{fx}" cy="{fy}" r="{fr}" gradientUnits="userSpaceOnUse">'
              f'<stop offset="0" stop-color="#fff"/><stop offset="0.55" stop-color="#fff" stop-opacity=".75"/>'
              f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
              f'<mask id="{uid}m" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">'
              f'<rect width="{w}" height="{h}" fill="url(#{uid}g)"/></mask></defs>')
        m = f' mask="url(#{uid}m)"'
    s += f'<g{m}><path d="{"".join(d)}" stroke="{color}" stroke-opacity="{op}" stroke-width="1" fill="none"/>'
    if cruces:
        cd = []
        step = paso * cruces
        xs = [x for x in range(int(x0 % paso), int(w) + 1, paso)]
        ys = [y for y in range(int(y0 % paso), int(h) + 1, paso)]
        for i, xx in enumerate(xs):
            for j, yy in enumerate(ys):
                if i % cruces == 0 and j % cruces == 0:
                    cd.append(f'M{xx - 5} {yy}h10M{xx} {yy - 5}v10')
        s += f'<path d="{"".join(cd)}" stroke="{color}" stroke-opacity="{cruz_op or op * 3:.3f}" stroke-width="1" fill="none"/>'
    return s + '</g>'


# ------------------------------------------------------------------ documento
def doc(w, h, body, title='', bg=None, defs='', desc=''):
    t = f'<title>{_esc(title)}</title>' if title else ''
    ds = f'<desc>{_esc(desc)}</desc>' if desc else ''
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    dd = f'<defs>{defs}</defs>' if defs else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'role="img" aria-label="{_esc(title)}">{t}{ds}{dd}{b}{body}</svg>\n')


def write(path, txt):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8', newline='\n') as f:
        f.write(txt)


def png_from_svg(jobs, workers=4):
    """jobs: lista de (svg_path, png_path, width). Render en paralelo con Chrome headless."""
    from render import svg_to_png

    def one(j):
        svg_to_png(j[0], j[1], width=j[2])
        return j[1]
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(one, jobs))


def isotipo_group(x, y, size, ring, node, uid='iso', ko=True, grad=None):
    """Isotipo oficial (geometría de oryzz_logo.py) colocado en x,y con ancho `size`
    (caja visible 80 u). ring: color o None si grad=(a,b)."""
    import oryzz_logo as L
    s = size / 80.0
    tx = x - 10 * s; ty = y - 10 * s
    d = L.ring_path(knockout=ko); nx, ny = L.NODE
    defs = ''
    stroke = ring
    if grad:
        defs = (f'<defs><linearGradient id="{uid}" gradientUnits="userSpaceOnUse" x1="10" y1="10" x2="90" y2="90">'
                f'<stop offset="0" stop-color="{grad[0]}"/><stop offset="1" stop-color="{grad[1]}"/></linearGradient></defs>')
        stroke = f'url(#{uid})'
    return (defs + f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">'
            f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{L.SW}" stroke-linecap="round"/>'
            f'<circle cx="{nx:.2f}" cy="{ny:.2f}" r="{L.NR}" fill="{node}"/></g>')


def logo_file(kind='horizontal', way='color-sobre-oscuro'):
    sub = {'horizontal': ('01_Horizontal', 'oryzz-logo-horizontal'), 'isotipo': ('04_Isotipo', 'oryzz-isotipo'),
           'wordmark': ('03_Wordmark', 'oryzz-wordmark'), 'tap': ('07_Submarca_Tap', 'oryzz-tap-horizontal')}[kind]
    return os.path.join(ROOT, '02_Logos', sub[0], 'SVG', f'{sub[1]}_{way}.svg')


def embed_logo(x, y, width, kind='horizontal', way='color-sobre-oscuro', uid='lg'):
    """Incrusta el SVG maestro del logo (sin redibujar) como <svg> anidado. IDs renombrados."""
    s = open(logo_file(kind, way), encoding='utf8').read()
    m = re.search(r'viewBox="([-\d.\s]+)"', s)
    vx, vy, vw, vh = [float(v) for v in m.group(1).split()]
    h = width * vh / vw
    inner = re.sub(r'^<svg[^>]*>', '', s.strip()); inner = re.sub(r'</svg>\s*$', '', inner)
    inner = re.sub(r'<title>.*?</title>', '', inner)
    inner = re.sub(r'id="([^"]+)"', lambda mm: f'id="{uid}{mm.group(1)}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda mm: f'url(#{uid}{mm.group(1)})', inner)
    return (f'<svg x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{h:.2f}" viewBox="{m.group(1)}" '
            f'aria-label="oryzz">{inner}</svg>'), h
