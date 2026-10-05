"""
Generador maestro del sistema de logos Oryzz (v2.0 · 2026).
Todas las piezas salen de esta geometría: nadie redibuja el logo a mano.

Uso:  python oryzz_logo.py <carpeta_salida>
"""
import math, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '..', 'fonts', 'static', 'SpaceGrotesk-Bold.ttf')
FONT_MED = os.path.join(HERE, '..', 'fonts', 'static', 'SpaceGrotesk-Medium.ttf')

# ------------------------------------------------------------------ color
C = dict(
    graphite='#0B0D12', white='#FFFFFF', black='#000000',
    blue='#3B72FF', blue_l='#5C8BFF', blue_d='#2C5BD0',
    cyan='#36CFE0', cyan_d='#17A9C2',
    lime='#BFF24A', lime_d='#7FB02E',
    titanium='#8A90A0',
)

# ------------------------------------------------------------------ isotipo (caja 100x100)
R, CX, CY, SW, NR = 34.0, 50.0, 50.0, 11.0, 7.5
A_LEFT, A_NODE = -115.1, -64.9  # grados (y hacia abajo)

def pt(a, r=R):
    return (CX + r * math.cos(math.radians(a)), CY + r * math.sin(math.radians(a)))

# Corte nodo-trazo (unidades de la caja 100). Se calcula con el trazo y el nodo REALES de cada versión.
GAP = 2.5          # isotipo normal y lockups
GAP_SMALL = 5.5    # isotipo pequeño (trazo 14, nodo 18): ≈ 1 px de separación a 16 px
GAP_FAV = 8.5      # favicon (isotipo pequeño al 74 % en la baldosa): ≈ 1 px de separación a 16 px
SW_SMALL, NR_SMALL = 14.0, 9.0

def ring_end_angle(knockout=True, gap=GAP, sw=SW, nr=NR):
    if not knockout:
        return A_NODE
    d = nr + sw / 2 + gap          # distancia centro del nodo -> centro de la punta
    return A_NODE + math.degrees(2 * math.asin(d / (2 * R)))

def ring_path(knockout=False, gap=GAP, sw=SW, nr=NR):
    x0, y0 = pt(A_LEFT)
    if not knockout:
        x1, y1 = pt(A_NODE)
    else:
        d = nr + sw / 2 + gap
        delta = math.degrees(2 * math.asin(d / (2 * R)))
        x1, y1 = pt(A_NODE + delta)
    return f'M{x0:.2f} {y0:.2f}A{R:g} {R:g} 0 1 0 {x1:.2f} {y1:.2f}'

NODE = pt(A_NODE)

# ------------------------------------------------------------------ wordmark
_font = TTFont(FONT)
_gs = _font.getGlyphSet()
_cmap = _font.getBestCmap()
_hmtx = _font['hmtx']
TRACK = -38          # unidades /1000 (≈ -0.038 em)
KERN = {('o', 'r'): -6, ('r', 'y'): -10, ('y', 'z'): -22}  # ajustes ópticos

def glyph_d(ch, x, baseline, scale=1.0, font=None):
    f = font or _font
    gs = f.getGlyphSet(); cmap = f.getBestCmap()
    pen = SVGPathPen(gs)
    tp = TransformPen(pen, (scale, 0, 0, -scale, x, baseline))
    gs[cmap[ord(ch)]].draw(tp)
    return pen.getCommands(), f['hmtx'][cmap[ord(ch)]][0] * scale

def word(text, x, baseline, scale=1.0, track=TRACK, font=None):
    """Devuelve lista de (char, d) y ancho total."""
    out = []; cx = x; prev = None
    for ch in text:
        if prev and (prev, ch) in KERN and font is None:
            cx += KERN[(prev, ch)] * scale
        d, adv = glyph_d(ch, cx, baseline, scale, font)
        out.append((ch, d)); cx += adv + track * scale; prev = ch
    return out, cx - x - track * scale

# ------------------------------------------------------------------ colorways
# ring: ('grad', a, b) | color ; node ; ory ; zz: ('grad',a,b) | color ; knockout
WAYS = {
    'color-sobre-oscuro': dict(bg=C['graphite'], ring=('grad', C['blue_l'], C['cyan']), node=C['lime'], ory=C['white'], zz=('grad', C['blue_l'], C['cyan']), ko=True),
    'color-sobre-claro':  dict(bg=C['white'],    ring=('grad', C['blue'], C['cyan_d']), node=C['lime_d'], ory=C['graphite'], zz=('grad', C['blue'], C['cyan_d']), ko=True),
    'solido-sobre-oscuro': dict(bg=C['graphite'], ring=C['blue_l'], node=C['lime'], ory=C['white'], zz=C['blue_l'], ko=True),
    'solido-sobre-claro':  dict(bg=C['white'],    ring=C['blue'], node=C['lime_d'], ory=C['graphite'], zz=C['blue'], ko=True),
    'sobre-azul':         dict(bg=C['blue'],     ring=C['white'], node=C['lime'], ory=C['white'], zz=C['white'], ko=True),
    'sobre-lima':         dict(bg=C['lime'],     ring=C['graphite'], node=C['graphite'], ory=C['graphite'], zz=C['graphite'], ko=True),
    'mono-blanco':        dict(bg=C['graphite'], ring=C['white'], node=C['white'], ory=C['white'], zz=C['white'], ko=True),
    'mono-grafito':       dict(bg=C['white'],    ring=C['graphite'], node=C['graphite'], ory=C['graphite'], zz=C['graphite'], ko=True),
    'mono-negro':         dict(bg=C['white'],    ring=C['black'], node=C['black'], ory=C['black'], zz=C['black'], ko=True),
    'mono-azul':          dict(bg=C['white'],    ring=C['blue'], node=C['blue'], ory=C['blue'], zz=C['blue'], ko=True),
}

def _defs(way, uid, ring_box, zz_box):
    s = []
    if isinstance(way['ring'], tuple):
        x1, y1, x2, y2 = ring_box
        s.append(f'<linearGradient id="{uid}r" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"><stop offset="0" stop-color="{way["ring"][1]}"/><stop offset="1" stop-color="{way["ring"][2]}"/></linearGradient>')
    if zz_box and isinstance(way['zz'], tuple):
        x1, y1, x2, y2 = zz_box
        s.append(f'<linearGradient id="{uid}z" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"><stop offset="0" stop-color="{way["zz"][1]}"/><stop offset="1" stop-color="{way["zz"][2]}"/></linearGradient>')
    return f'<defs>{"".join(s)}</defs>' if s else ''

def _paint(v, uid, key):
    return f'url(#{uid}{key})' if isinstance(v, tuple) else v

def mark_group(way, uid, tx=0, ty=0, s=1.0, sw=SW, nr=NR, gap=GAP):
    """Isotipo como <g>; coordenadas locales 0..100."""
    ring = way['ring']; stroke = _paint(ring, uid, 'r')
    d = ring_path(knockout=way['ko'], gap=gap, sw=sw, nr=nr)
    nx, ny = NODE
    return (f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">'
            f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<circle cx="{nx:.2f}" cy="{ny:.2f}" r="{nr}" fill="{way["node"]}"/></g>')

def uid_for(family, wayname):
    """Prefijo de ids único por familia + colorway completo (seguro al incrustar varios SVG en línea)."""
    return f'oryzz-{family}-{wayname}-'

def mark_bbox(sw=SW, nr=NR, gap=GAP, knockout=True):
    """bbox del isotipo en coordenadas locales 0..100 (el arco siempre pasa por 180°, 90° y 0°)."""
    a1 = ring_end_angle(knockout, gap, sw, nr)
    ys = [pt(A_LEFT)[1] - sw / 2, pt(a1)[1] - sw / 2, NODE[1] - nr]
    return (CX - R - sw / 2, min(ys), CX + R + sw / 2, CY + R + sw / 2)

def glyphs_bbox(text, x, baseline, scale=1.0, track=TRACK, font=None):
    """bbox real de los trazados de una palabra (misma maquetación que word())."""
    from fontTools.pens.boundsPen import BoundsPen
    f = font or _font; gs = f.getGlyphSet(); cmap = f.getBestCmap()
    cx = x; prev = None; bb = None
    for ch in text:
        if prev and (prev, ch) in KERN and font is None:
            cx += KERN[(prev, ch)] * scale
        bp = BoundsPen(gs)
        gs[cmap[ord(ch)]].draw(TransformPen(bp, (scale, 0, 0, -scale, cx, baseline)))
        if bp.bounds:
            b = bp.bounds
            bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
        cx += f['hmtx'][cmap[ord(ch)]][0] * scale + track * scale; prev = ch
    return bb

def union(*bbs):
    return (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))

def vb_margin(bb, m):
    """viewBox con margen uniforme m en los cuatro lados."""
    return f'{bb[0] - m:.2f} {bb[1] - m:.2f} {bb[2] - bb[0] + 2 * m:.2f} {bb[3] - bb[1] + 2 * m:.2f}'

def svg(w, h, body, title, vb=None):
    vb = vb or f'0 0 {w:.0f} {h:.0f}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

# ------------------------------------------------------------------ piezas
XH = 486
MARGIN = 32  # margen uniforme (u) en los cuatro lados del viewBox de todos los lockups (≈ 0,065 x)

def _mark_bb_scaled(tx, ty, s):
    x0, y0, x1, y1 = mark_bbox()
    return (tx + x0 * s, ty + y0 * s, tx + x1 * s, ty + y1 * s)

def lockup_h(wayname, sub=None):
    """Horizontal: isotipo + oryzz (+ submarca opcional)."""
    way = WAYS[wayname]; uid = uid_for('h' + ('-' + sub if sub else ''), wayname)
    ring_outer = 2 * (R + SW / 2)          # 79 en caja 100
    D = 1.70 * XH; s = D / ring_outer       # escala del isotipo
    B = 0.5 * XH + D / 2 + 4                # baseline
    cy = B - XH / 2
    tx = -(CX - R - SW / 2) * s; ty = cy - CY * s
    mark = mark_group(way, uid, tx, ty, s)
    x0 = D + 0.40 * XH - 46
    glyphs, wid = word('oryzz', x0, B)
    ory = ''.join(d for _, d in glyphs[:3]); zz = ''.join(d for _, d in glyphs[3:])
    zx1 = x0 + wid * 0.60; zx2 = x0 + wid
    ring_box = (10, 10, 90, 90)  # coordenadas locales del isotipo
    zz_box = (zx1, B - XH, zx2, B)
    body = _defs(way, uid, ring_box, zz_box) + mark
    body += f'<path d="{ory}" fill="{way["ory"]}"/><path d="{zz}" fill="{_paint(way["zz"], uid, "z")}"/>'
    bb = union(_mark_bb_scaled(tx, ty, s), glyphs_bbox('oryzz', x0, B))
    W = x0 + wid
    if sub:
        fm = TTFont(FONT_MED)
        sc = 0.62
        sx = W + 0.30 * XH
        sg, sw_ = word(sub, sx, B, sc, track=-10, font=fm)
        subc = C['titanium'] if wayname.startswith(('color', 'solido')) else way['ory']
        body += f'<path d="{"".join(d for _, d in sg)}" fill="{subc}"/>'
        bb = union(bb, glyphs_bbox(sub, sx, B, sc, track=-10, font=fm))
    return svg(0, 0, body, 'oryzz' + (' ' + sub if sub else ''), vb=vb_margin(bb, MARGIN))

def lockup_v(wayname):
    way = WAYS[wayname]; uid = uid_for('v', wayname)
    glyphs, wid = word('oryzz', 0, 0)
    D = 2.1 * XH; s = D / 79
    cxm = wid / 2
    tx = cxm - 50 * s; ty = -(10.5 * s)
    mark = mark_group(way, uid, tx, ty, s)
    B = D + 0.62 * XH + XH
    glyphs, wid = word('oryzz', 0, B)
    ory = ''.join(d for _, d in glyphs[:3]); zz = ''.join(d for _, d in glyphs[3:])
    ring_box = (10, 10, 90, 90)  # coordenadas locales del isotipo
    zz_box = (wid * 0.6, B - XH, wid, B)
    body = _defs(way, uid, ring_box, zz_box) + mark + f'<path d="{ory}" fill="{way["ory"]}"/><path d="{zz}" fill="{_paint(way["zz"], uid, "z")}"/>'
    bb = union(_mark_bb_scaled(tx, ty, s), glyphs_bbox('oryzz', 0, B))
    return svg(0, 0, body, 'oryzz', vb=vb_margin(bb, MARGIN))

def wordmark(wayname):
    way = WAYS[wayname]; uid = uid_for('w', wayname)
    B = 520
    glyphs, wid = word('oryzz', 0, B)
    ory = ''.join(d for _, d in glyphs[:3]); zz = ''.join(d for _, d in glyphs[3:])
    zz_box = (wid * 0.6, B - XH, wid, B)
    body = _defs({**way, 'ring': None}, uid, None, zz_box)
    body += f'<path d="{ory}" fill="{way["ory"]}"/><path d="{zz}" fill="{_paint(way["zz"], uid, "z")}"/>'
    return svg(0, 0, body, 'oryzz', vb=vb_margin(glyphs_bbox('oryzz', 0, B), MARGIN))

def isotipo(wayname, small=False):
    way = WAYS[wayname]; uid = uid_for('is' if small else 'i', wayname)
    sw, nr, gap = (SW_SMALL, NR_SMALL, GAP_SMALL) if small else (SW, NR, GAP)
    body = _defs(way, uid, (10, 10, 90, 90), None) + mark_group(way, uid, 0, 0, 1, sw, nr, gap)
    m = sw / 2 + 0.5
    return svg(100, 100, body, 'oryzz', vb=f'{CX - R - m:.2f} {CY - R - m:.2f} {2 * (R + m):.2f} {2 * (R + m):.2f}')

def avatar(wayname, shape='square', size=1024):
    """Contenedor para perfiles / app icon. shape: square | circle."""
    way = WAYS[wayname]; uid = uid_for('avatar-' + ('cuadrado' if shape == 'square' else 'circulo'), wayname)
    bg = way['bg']
    if shape == 'square':
        base = f'<rect width="100" height="100" rx="22.5" fill="{bg}"/>'
    else:
        base = f'<circle cx="50" cy="50" r="50" fill="{bg}"/>'
    s = 0.60
    body = base + _defs(way, uid, (10, 10, 90, 90), None) + mark_group(way, uid, 50 - 50 * s, 50 - 50 * s + 1, s)
    return svg(100, 100, body, 'oryzz')

def favicon():
    way = WAYS['color-sobre-oscuro']; uid = uid_for('favicon', 'color-sobre-oscuro')
    s = 0.74
    body = (f'<rect width="100" height="100" rx="22.5" fill="{C["graphite"]}"/>' + _defs(way, uid, (10, 10, 90, 90), None)
            + mark_group(way, uid, 50 - 50 * s, 50 - 50 * s + 1, s, SW_SMALL, NR_SMALL, GAP_FAV))
    return svg(100, 100, body, 'oryzz')

# ------------------------------------------------------------------ main
def build(out):
    def w(rel, txt):
        p = os.path.join(out, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf8').write(txt)
    for wn in WAYS:
        w(f'01_Horizontal/SVG/oryzz-logo-horizontal_{wn}.svg', lockup_h(wn))
        w(f'02_Vertical/SVG/oryzz-logo-vertical_{wn}.svg', lockup_v(wn))
        w(f'03_Wordmark/SVG/oryzz-wordmark_{wn}.svg', wordmark(wn))
        w(f'04_Isotipo/SVG/oryzz-isotipo_{wn}.svg', isotipo(wn))
        w(f'04_Isotipo/SVG_tamano_pequeno/oryzz-isotipo-small_{wn}.svg', isotipo(wn, small=True))
        w(f'07_Submarca_Tap/SVG/oryzz-tap-horizontal_{wn}.svg', lockup_h(wn, sub='tap'))
    for wn in ['color-sobre-oscuro', 'color-sobre-claro', 'sobre-azul', 'sobre-lima', 'mono-blanco']:
        w(f'05_Avatar_Perfil/SVG/oryzz-avatar-cuadrado_{wn}.svg', avatar(wn, 'square'))
        w(f'05_Avatar_Perfil/SVG/oryzz-avatar-circulo_{wn}.svg', avatar(wn, 'circle'))
    w('06_Favicon/favicon.svg', favicon())

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out_logos'))
    print('ok')
