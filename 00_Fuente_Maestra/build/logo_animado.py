"""
Logo animado de Oryzz (BRAND_SPEC §5.7) — SVG con CSS, GIF fotograma a fotograma y loader.

Uso:  python logo_animado.py            -> escribe en 02_Logos/08_Animado/

Una sola fuente de verdad: las pistas de animación (TRACKS) se usan para
  a) escribir los @keyframes CSS de los SVG, y
  b) calcular cada fotograma estático del GIF (misma curva, mismo instante).

Geometría idéntica a oryzz_logo.lockup_h(): el fotograma final del intro es el logo maestro.
Técnica de pivote robusta: <g translate(pivote)><g class=anim><g translate(-pivote)>…  (sin transform-box).
"""
import math, os, sys, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oryzz_logo as L
from render_fast import Chrome

OUT = os.path.abspath(os.path.join(HERE, '..', '..', '02_Logos', '08_Animado'))
GRAFITO = '#0B0D12'

EASE = {
    'linear': (0, 0, 1, 1),
    'marca': (.2, .8, .2, 1),          # tokens.motion.ease-marca
    'salto': (.34, 1.4, .5, 1),        # tokens.motion.ease-salto (resorte)
    'inout': (.42, 0, .58, 1),
    'caida': (.55, 0, .85, .4),        # aceleración de caída
    'subida': (.2, .7, .4, 1),
}


def bezier(p, e):
    x1, y1, x2, y2 = EASE[e]
    if (x1, y1, x2, y2) == (0, 0, 1, 1):
        return p
    cx = lambda t: 3 * x1 * t * (1 - t) ** 2 + 3 * x2 * t * t * (1 - t) + t ** 3
    cy = lambda t: 3 * y1 * t * (1 - t) ** 2 + 3 * y2 * t * t * (1 - t) + t ** 3
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if cx(mid) < p: lo = mid
        else: hi = mid
    return cy((lo + hi) / 2)


class Track:
    """kf: [(offset 0..1, valores(tuple), easing_hasta_el_siguiente)]"""
    def __init__(self, name, props, dur, kf, delay=0.0, iters='infinite', ease='linear'):
        self.name, self.props, self.dur, self.kf, self.delay, self.iters, self.ease = name, props, dur, kf, delay, iters, ease

    def value(self, t):
        lt = t - self.delay
        if lt < 0:
            return self.kf[0][1]
        if self.iters == 'infinite':
            lt = lt % self.dur
        elif lt >= self.dur * self.iters:
            return self.kf[-1][1]
        p = (lt % self.dur) / self.dur
        for (o0, v0, e), (o1, v1, _) in zip(self.kf, self.kf[1:]):
            if o0 <= p <= o1:
                q = 0 if o1 == o0 else (p - o0) / (o1 - o0)
                k = bezier(q, e)
                return tuple(a + (b - a) * k for a, b in zip(v0, v1))
        return self.kf[-1][1]

    def css_decl(self, v):
        out = []
        tr = []
        for prop, x in zip(self.props, v):
            if prop == 'rotate': tr.append(f'rotate({x:.3f}deg)')
            elif prop == 'scale': tr.append(f'scale({x:.4f})')
            elif prop == 'tx': tr.append(f'translateX({x:.2f}px)')
            elif prop == 'ty': tr.append(f'translateY({x:.2f}px)')
            elif prop == 'sy': tr.append(f'scaleY({x:.4f})')
            elif prop == 'opacity': out.append(f'opacity:{x:.3f}')
            elif prop == 'dash': out.append(f'stroke-dashoffset:{x - 100:.3f}')
        if tr: out.append('transform:' + ' '.join(tr))
        return ';'.join(out)

    def css(self):
        rows = []
        for o, v, e in self.kf:
            x1, y1, x2, y2 = EASE[e]
            rows.append(f'{o * 100:.2f}%{{{self.css_decl(v)};animation-timing-function:cubic-bezier({x1},{y1},{x2},{y2})}}')
        return f'@keyframes {self.name}{{{"".join(rows)}}}'

    def anim(self):
        it = 'infinite' if self.iters == 'infinite' else str(self.iters)
        fill = 'both' if self.iters != 'infinite' else 'none'
        return f'animation:{self.name} {self.dur}s linear {self.delay}s {it} {fill}'

    def attrs(self, t):
        """Transform/estilo estático del instante t (para fotogramas)."""
        v = self.value(t)
        tr, st = [], {}
        for prop, x in zip(self.props, v):
            if prop == 'rotate': tr.append(f'rotate({x:.4f})')
            elif prop == 'scale': tr.append(f'scale({max(x, 0.0001):.5f})')
            elif prop == 'tx': tr.append(f'translate({x:.3f} 0)')
            elif prop == 'ty': tr.append(f'translate(0 {x:.3f})')
            elif prop == 'sy': tr.append(f'scale(1 {max(x, 0.0001):.5f})')
            elif prop == 'opacity': st['opacity'] = f'{min(max(x, 0), 1):.4f}'
            elif prop == 'dash': st['stroke-dashoffset'] = f'{x - 100:.4f}'
        return ' '.join(tr), st


# ------------------------------------------------------------------ pistas
ZHOP = [(0, (0, 1), 'salto'), (.10, (0, .84), 'salto'), (.40, (-262, 1.07), 'salto'), (.62, (0, .90), 'salto'),
        (.74, (-46, 1.02), 'salto'), (.84, (0, 1), 'salto'), (1, (0, 1), 'linear')]   # 34px/130px del original = 0,26 em


def tracks_loop(prefix):
    return {
        'orb': Track(prefix + 'Orb', ('rotate',), 4.4, [(0, (0,), 'linear'), (1, (360,), 'linear')]),
        'nodo': Track(prefix + 'Nodo', ('opacity', 'scale'), 4.4, [(0, (1, 1), 'inout'), (.5, (.92, .80), 'inout'), (1, (1, 1), 'linear')]),
        'z1': Track(prefix + 'Z', ('ty', 'sy'), 1.95, ZHOP),
        'z2': Track(prefix + 'Z', ('ty', 'sy'), 1.95, ZHOP, delay=.17),
    }


INTRO_T = 3.0


def tracks_intro(prefix):
    zin = [(0, (-260, 1.06), 'caida'), (.38, (0, .84), 'subida'), (.58, (-52, 1.03), 'caida'),
           (.74, (0, .95), 'salto'), (1, (0, 1), 'linear')]
    T = INTRO_T
    return {
        'ringop': Track(prefix + 'RingOp', ('opacity',), .14, [(0, (0,), 'linear'), (1, (1,), 'linear')], iters=1),
        'dash': Track(prefix + 'Dash', ('dash',), 1.25, [(0, (0,), 'marca'), (1, (100,), 'linear')], iters=1),
        'orb': Track(prefix + 'Orb', ('rotate',), 1.5, [(0, (-150,), 'marca'), (1, (0,), 'linear')], iters=1),
        'nodo': Track(prefix + 'Nodo', ('opacity', 'scale'), T, [
            (0, (0, 0), 'linear'), (.95 / T, (0, 0), 'salto'), (1.45 / T, (1, 1), 'linear'),
            (1.9 / T, (1, 1), 'inout'), (2.4 / T, (.92, .82), 'inout'), (2.9 / T, (1, 1), 'linear'), (1, (1, 1), 'linear')], iters=1),
        'ory': Track(prefix + 'Ory', ('opacity', 'tx'), .7, [(0, (0, -110), 'marca'), (1, (1, 0), 'linear')], delay=.5, iters=1),
        'z1op': Track(prefix + 'ZOp', ('opacity',), .16, [(0, (0,), 'linear'), (1, (1,), 'linear')], delay=.95, iters=1),
        'z2op': Track(prefix + 'ZOp', ('opacity',), .16, [(0, (0,), 'linear'), (1, (1,), 'linear')], delay=1.12, iters=1),
        'z1': Track(prefix + 'ZIn', ('ty', 'sy'), 1.1, zin, delay=.95, iters=1),
        'z2': Track(prefix + 'ZIn', ('ty', 'sy'), 1.1, zin, delay=1.12, iters=1),
    }


# ------------------------------------------------------------------ geometría (idéntica a lockup_h)
def geometry():
    XH = L.XH
    D = 1.70 * XH; s = D / (2 * (L.R + L.SW / 2))
    B = 0.5 * XH + D / 2 + 4
    cy = B - XH / 2
    tx = -(L.CX - L.R - L.SW / 2) * s; ty = cy - L.CY * s
    x0 = D + 0.40 * XH - 46
    glyphs, wid = L.word('oryzz', x0, B)
    # posiciones de cada letra (réplica de L.word)
    xs = []; cx = x0; prev = None
    for ch in 'oryzz':
        if prev and (prev, ch) in L.KERN: cx += L.KERN[(prev, ch)]
        xs.append(cx); _, adv = L.glyph_d(ch, cx, B); cx += adv + L.TRACK; prev = ch
    W = x0 + wid
    top = cy - D / 2; bottom = max(cy + D / 2, B + 200)
    return dict(s=s, tx=tx, ty=ty, B=B, x0=x0, wid=wid, W=W, top=top, bottom=bottom, glyphs=glyphs, xs=xs,
                ring_c=(tx + L.CX * s, ty + L.CY * s), node_c=(tx + L.NODE[0] * s, ty + L.NODE[1] * s),
                zz_box=(x0 + wid * 0.6, B - XH, x0 + wid, B))


G = geometry()


def _check_against_master():
    master = L.lockup_h('color-sobre-oscuro')
    ory = ''.join(d for _, d in G['glyphs'][:3]); zz = ''.join(d for _, d in G['glyphs'][3:])
    assert f'd="{ory}"' in master and f'd="{zz}"' in master, 'geometría distinta del maestro'


def _paint(v, uid, k):
    return f'url(#{uid}{k})' if isinstance(v, tuple) else v


def _grad(uid, k, v, box):
    x1, y1, x2, y2 = box
    return (f'<linearGradient id="{uid}{k}" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">'
            f'<stop offset="0" stop-color="{v[1]}"/><stop offset="1" stop-color="{v[2]}"/></linearGradient>')


def _pivot(center, inner, cls=None, tr=None, style=None):
    """<g translate(c)><g class|transform><g translate(-c)>inner</g></g></g>"""
    cx, cy = center
    a = []
    if cls: a.append(f'class="{cls}"')
    if tr: a.append(f'transform="{tr}"')
    if style: a.append('style="' + ';'.join(f'{k}:{v}' for k, v in style.items()) + '"')
    return (f'<g transform="translate({cx:.3f} {cy:.3f})"><g {" ".join(a)}>'
            f'<g transform="translate({-cx:.3f} {-cy:.3f})">{inner}</g></g></g>')


def _el_style(st):
    return (' style="' + ';'.join(f'{k}:{v}' for k, v in st.items()) + '"') if st else ''


def build(wayname, tracks, t=None, mark_only=False, bg=None, vb=None, uid='an', css_extra=''):
    """SVG animado (t=None, CSS) o fotograma estático del instante t."""
    way = L.WAYS[wayname]
    s, tx, ty = G['s'], G['tx'], G['ty']
    live = t is None

    def fx(key):
        """(clase CSS, transform, estilo) para una pista."""
        tr_ = tracks.get(key)
        if tr_ is None: return None, None, {}
        if live: return key, None, {}
        a, st = tr_.attrs(t); return None, a or None, st

    defs = []
    if isinstance(way['ring'], tuple): defs.append(_grad(uid, 'r', way['ring'], (10, 10, 90, 90)))
    if not mark_only and isinstance(way['zz'], tuple): defs.append(_grad(uid, 'z', way['zz'], G['zz_box']))

    # anillo (en coordenadas locales 0..100 del isotipo)
    ring_d = L.ring_path(knockout=way['ko'])
    ring_attrs = f'd="{ring_d}" fill="none" stroke="{_paint(way["ring"], uid, "r")}" stroke-width="{L.SW}" stroke-linecap="round"'
    ring_style, wrap_style, cls_attr, wrap_cls = {}, {}, '', ''
    if 'dash' in tracks:
        ring_attrs += ' pathLength="100" stroke-dasharray="100 200"'
        c_, a_, ring_style = fx('dash'); cls_attr = ' class="dash"' if live else ''
    if 'ringop' in tracks:
        c_, a_, wrap_style = fx('ringop'); wrap_cls = ' class="ringop"' if live else ''
    ring = (f'<g{wrap_cls} transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})"{_el_style(wrap_style)}>'
            f'<path {ring_attrs}{cls_attr}{_el_style(ring_style)}/></g>')
    # nodo en coordenadas del lienzo (para que su pivote sea su centro)
    nx, ny = G['node_c']
    node = f'<circle cx="{nx:.3f}" cy="{ny:.3f}" r="{L.NR * s:.3f}" fill="{way["node"]}"/>'
    c_, a_, st = fx('nodo')
    node = _pivot(G['node_c'], node, cls=c_, tr=a_, style=st)
    c_, a_, st = fx('orb')
    orb = _pivot(G['ring_c'], ring + node, cls=c_, tr=a_, style=st)
    body = orb

    if not mark_only:
        ory = ''.join(d for _, d in G['glyphs'][:3])
        c_, a_, st = fx('ory')
        ory_el = f'<path d="{ory}" fill="{way["ory"]}"/>'
        if 'ory' in tracks:
            a = []
            if c_: a.append(f'class="{c_}"')
            if a_: a.append(f'transform="{a_}"')
            ory_el = f'<g {" ".join(a)}{_el_style(st)}>{ory_el}</g>'
        body += ory_el
        for i, key in ((3, 'z1'), (4, 'z2')):
            d = G['glyphs'][i][1]
            zx = G['xs'][i] + (52 + 470) / 2  # centro inferior del glifo «z»
            el = f'<path d="{d}" fill="{_paint(way["zz"], uid, "z")}"/>'
            c_, a_, st = fx(key)
            el = _pivot((zx, G['B']), el, cls=c_, tr=a_, style=st)
            opk = key + 'op'
            if opk in tracks:
                c2, a2, st2 = fx(opk)
                el = f'<g{f" class={chr(34)}{c2}{chr(34)}" if c2 else ""}{_el_style(st2)}>{el}</g>'
            body += el

    style = ''
    if live:
        seen = set(); kfs = []; rules = []
        for key, tr_ in tracks.items():
            if tr_.name not in seen:
                kfs.append(tr_.css()); seen.add(tr_.name)
            rules.append(f'.{key}{{{tr_.anim()}}}')
        style = ('<style>' + ''.join(kfs) + ''.join(rules) + css_extra +
                 '@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>')
    if bg:
        x, y, w, h = vb
        body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' + body
    vbs = ' '.join(f'{v:.1f}' for v in vb)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vbs}" role="img" aria-label="oryzz">'
            f'<title>oryzz</title>{style}<defs>{"".join(defs)}</defs>{body}</svg>\n')


# viewBox del lockup con aire para el salto de las «zz» (simétrico arriba/abajo)
HEAD = 170
HX = 40   # el nodo sobresale 2 u del anillo: al girar necesita aire lateral
VB_LOCKUP = (-HX, G['top'] - HEAD, G['W'] + 12 + 2 * HX, (G['bottom'] - G['top']) + 2 * HEAD)
# viewBox del isotipo (loader): círculo completo centrado en el anillo + margen
_rc = G['ring_c']; _rr = (L.R + L.SW / 2) * G['s']
VB_MARK = (_rc[0] - _rr * 1.18, _rc[1] - _rr * 1.18, 2 * _rr * 1.18, 2 * _rr * 1.18)


def gif(frames_png, out, durations, colors=255):
    ims = [Image.open(f).convert('RGB') for f in frames_png]
    # paleta global a partir del fotograma final (contiene todos los colores) + uno intermedio
    ref = Image.new('RGB', (ims[0].width, ims[0].height * 2))
    ref.paste(ims[-1], (0, 0)); ref.paste(ims[len(ims) // 2], (0, ims[0].height))
    pal = ref.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [im.quantize(palette=pal, dither=Image.Dither.NONE) for im in ims]
    q[0].save(out, save_all=True, append_images=q[1:], duration=durations, loop=0, optimize=False, disposal=1)


def main():
    _check_against_master()
    os.makedirs(OUT, exist_ok=True)
    import tempfile, shutil
    fr_dir = tempfile.mkdtemp(prefix='oryzz_frames_')
    loop_css = ''
    files = {
        'oryzz-logo-animado.svg': build('color-sobre-oscuro', tracks_loop('oy'), vb=VB_LOCKUP, uid='oryzz-animado-color-sobre-oscuro-'),
        'oryzz-logo-animado_sobre-claro.svg': build('color-sobre-claro', tracks_loop('oy'), vb=VB_LOCKUP, uid='oryzz-animado-color-sobre-claro-'),
        'oryzz-logo-intro.svg': build('color-sobre-oscuro', tracks_intro('oi'), vb=VB_LOCKUP, uid='oryzz-intro-color-sobre-oscuro-'),
        'oryzz-logo-intro_sobre-claro.svg': build('color-sobre-claro', tracks_intro('oi'), vb=VB_LOCKUP, uid='oryzz-intro-color-sobre-claro-'),
        'oryzz-loader.svg': build('color-sobre-oscuro', {k: v for k, v in tracks_loop('ol').items() if k in ('orb', 'nodo')}, mark_only=True, vb=VB_MARK, uid='oryzz-loader-color-sobre-oscuro-'),
        'oryzz-loader_sobre-claro.svg': build('color-sobre-claro', {k: v for k, v in tracks_loop('ol').items() if k in ('orb', 'nodo')}, mark_only=True, vb=VB_MARK, uid='oryzz-loader-color-sobre-claro-'),
    }
    for n, txt in files.items():
        open(os.path.join(OUT, n), 'w', encoding='utf8').write(txt)

    fps = 30
    with Chrome() as c:
        # ---- GIF intro 800x300 sobre grafito
        W, H = 800, 300
        lw = 3456.6 * 1.0
        scale = 560 / lw                           # el lockup ocupa 560 px de ancho
        vw, vh = W / scale, H / scale
        _bb = L.union(L.glyphs_bbox('oryzz', G['x0'], G['B']), (0, G['ty'] + L.mark_bbox()[1] * G['s'], 0, G['ty'] + L.mark_bbox()[3] * G['s']))
        cxm = (_bb[0] + _bb[2]) / 2; cym = (_bb[1] + _bb[3]) / 2
        vb = (cxm - vw / 2, cym - vh / 2, vw, vh)
        tr = tracks_intro('x')
        n = int(INTRO_T * fps) + 1
        pngs = []
        for i in range(n):
            t = i / fps
            svg = build('color-sobre-oscuro', tr, t=t, bg=GRAFITO, vb=vb, uid='f')
            p = os.path.join(fr_dir, f'intro_{i:03d}.png'); pngs.append(p)
            c.svg_string_to_png(svg, p, W, H)
        dur = [33 if i % 3 else 34 for i in range(n)]
        dur[-1] = 1400                            # pausa con el logo en reposo antes de repetir
        gif(pngs, os.path.join(OUT, 'oryzz-logo-intro_800x300.gif'), dur)
        # ---- loaders 256x256 (una vuelta = 4,4 s = 132 fotogramas; bucle perfecto)
        trl = {k: v for k, v in tracks_loop('x').items() if k in ('orb', 'nodo')}
        for way, bg, tag in (('color-sobre-oscuro', GRAFITO, 'sobre-oscuro'), ('color-sobre-claro', '#FFFFFF', 'sobre-claro')):
            pngs = []
            for i in range(int(4.4 * fps)):
                t = i / fps
                svg = build(way, trl, t=t, mark_only=True, bg=bg, vb=VB_MARK, uid='l')
                p = os.path.join(fr_dir, f'loader_{tag}_{i:03d}.png'); pngs.append(p)
                c.svg_string_to_png(svg, p, 256, 256)
            gif(pngs, os.path.join(OUT, f'oryzz-loader_{tag}_256.gif'), [33 if i % 3 else 34 for i in range(len(pngs))], colors=96)
        # ---- póster (último fotograma) para usar como fallback estático
        c.svg_string_to_png(build('color-sobre-oscuro', tr, t=INTRO_T, bg=GRAFITO, vb=vb, uid='f'),
                            os.path.join(OUT, 'oryzz-logo-intro_poster_800x300.png'), W, H)
    shutil.rmtree(fr_dir, ignore_errors=True)
    print('ok', n, 'fotogramas intro')


if __name__ == '__main__':
    main()
