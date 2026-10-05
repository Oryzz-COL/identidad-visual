"""
oryzz_patrones.py · Patrones y texturas del sistema «Órbita y nodo» (Oryzz v2.0).

  a) órbitas   · arcos concéntricos abiertos (paso 64 px) con un solo nodo
  b) reticula  · cuadrícula técnica 64 px al 3,5 %, cruces cada 4 celdas, desvanecida
  c) rutas     · rutas ortogonales con esquinas redondeadas que conectan nodos (tile 512 enlosable)
  d) nodos     · campo de puntos de datos sobre retícula de 32 px (tile 512 enlosable)

Cada función devuelve el cuerpo SVG para (w, h, tema) y se reutiliza en 03_Fondos.
Uso:  python oryzz_patrones.py   → 05_Elementos_Graficos/02_Patrones
"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oryzz_svg import C, THEME, ROOT, write, doc, arc, pol, gap_deg, ruta, reticula, halo, png_from_svg

OUT = os.path.join(ROOT, '05_Elementos_Graficos', '02_Patrones')
TILE = 512


def _fade(uid, w, h, fx, fy, fr, inner=0.35):
    return (f'<radialGradient id="{uid}g" cx="{fx:.1f}" cy="{fy:.1f}" r="{fr:.1f}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#fff"/><stop offset="{inner}" stop-color="#fff" stop-opacity=".85"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="{uid}m" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="url(#{uid}g)"/></mask>')


# ------------------------------------------------------------------ a) órbitas
RADIOS = [96, 160, 256, 384, 544, 736, 960, 1216, 1500]
ABERTURAS = [58, 36, 44, 72, 40, 64, 48, 80, 52]
GIROS = [-62, 18, -38, 96, 150, -12, 60, -100, 20]


def orbitas(w, h, tema, cx=None, cy=None, uid='orb', nodo_en=2, sw=1.25, fade=True, nodo_r=7,
            radios=None, escala=1.0, op_out=0.35, mostrar_nodo=True, satelites=True, rot=0, nodo_hacia=None):
    """Órbitas concéntricas abiertas con espaciado creciente (sistema orbital, no diana).
    nodo_en: índice del anillo que lleva el único nodo lima, situado en el extremo de su abertura."""
    t = THEME[tema]
    cx = w * 0.70 if cx is None else cx; cy = h * 0.52 if cy is None else cy
    rmax = max(math.hypot(cx - x, cy - y) for x in (0, w) for y in (0, h))
    radios = [r * escala for r in (radios or RADIOS)]
    radios = [r for r in radios if r < rmax + 40]
    n = len(radios)
    s = []; node = ''
    for i, r in enumerate(radios):
        ab = ABERTURAS[i % len(ABERTURAS)]
        a_n = GIROS[i % len(GIROS)] + rot
        k = i / max(1, n - 1)
        op = 1 - (1 - op_out) * k
        wdt = sw * (1.4 if i < 2 else 1)
        if i == nodo_en and nodo_hacia:
            a_n = math.degrees(math.atan2(nodo_hacia[1] - cy, nodo_hacia[0] - cx))
        if i == nodo_en and mostrar_nodo:
            cut = gap_deg(r, nodo_r + wdt / 2 + 8)
            s.append(f'<path d="{arc(cx, cy, r, a_n + cut, a_n - ab)}" stroke="{t["linea"]}" stroke-width="{wdt * 1.2:g}" '
                     f'fill="none" stroke-linecap="round" opacity="{min(1, op + .15):.2f}"/>')
            nx, ny = pol(cx, cy, r, a_n)
            node = (f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{nodo_r * 3.4:.1f}" fill="{t["nodo"]}" opacity=".07"/>'
                    f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{nodo_r}" fill="{t["nodo"]}"/>')
        else:
            s.append(f'<path d="{arc(cx, cy, r, a_n, a_n - ab)}" stroke="{t["linea"]}" stroke-width="{wdt:g}" '
                     f'fill="none" stroke-linecap="round" opacity="{op:.2f}"/>')
            if satelites and i in (3, 5):
                sx, sy = pol(cx, cy, r, a_n + 120 + i * 9)
                s.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="3.5" fill="{t["fondo"]}" stroke="{C["grafito-600"] if tema == "oscuro" else C["grafito-300"]}" stroke-width="1.25" opacity="{op:.2f}"/>')
    body = ''.join(s)
    defs = ''
    if fade:
        defs = _fade(uid, w, h, cx, cy, rmax * 1.02, 0.5)
        body = f'<g mask="url(#{uid}m)">{body}</g>'
    return f'<defs>{defs}</defs>{body}{node}'


# ------------------------------------------------------------------ c) rutas (tile)
ROUTES = [
    # (puntos, extremo_inicio, extremo_fin)   extremos: None | 'hueco' | 'punto'
    ([(0, 96), (192, 96), (192, 288), (512, 288)], None, None),
    ([(0, 288), (96, 288), (96, 416), (288, 416)], None, 'hueco'),
    ([(384, 0), (384, 96), (512, 96)], None, None),
    ([(384, 512), (384, 416)], None, 'punto'),
]
PUNTOS = [(192, 192), (320, 288), (96, 352)]


def rutas_tile(tema, uid='rt', sw=1.5, rad=24, lin=None, op=1):
    t = THEME[tema]; col = lin or t['linea']
    s = []
    for pts, a, b in ROUTES:
        s.append(f'<path d="{ruta(pts, rad)}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
        for end, p, q in ((a, pts[0], pts[1]), (b, pts[-1], pts[-2])):
            if end == 'hueco':
                # el trazo se detiene antes del nodo (como el isotipo)
                s.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="6" fill="{t["fondo"]}" stroke="{col}" stroke-width="{sw}"/>')
            elif end == 'punto':
                s.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="4" fill="{col}"/>')
    # uniones: puntos pequeños en algunos giros
    for x, y in PUNTOS:
        s.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{col}"/>')
    return f'<g opacity="{op}">{"".join(s)}</g>'


def rutas(w, h, tema, uid='rut', ox=0, oy=0, fade=True, fx=None, fy=None, fr=None, nodo=(None, None), sw=1.5):
    """Composición a partir del tile de rutas. nodo=(x,y) en coordenadas de lienzo para el nodo lima."""
    t = THEME[tema]
    fx = w * 0.72 if fx is None else fx; fy = h * 0.5 if fy is None else fy
    fr = fr or max(w, h) * 0.75
    tile = rutas_tile(tema, sw=sw)
    defs = (f'<pattern id="{uid}p" width="{TILE}" height="{TILE}" patternUnits="userSpaceOnUse" x="{ox}" y="{oy}">{tile}</pattern>')
    body = f'<rect width="{w}" height="{h}" fill="url(#{uid}p)"/>'
    if fade:
        defs += _fade(uid, w, h, fx, fy, fr, 0.3)
        body = f'<g mask="url(#{uid}m)">{body}</g>'
    if nodo[0] is not None:
        nx, ny = nodo
        body += (f'<circle cx="{nx}" cy="{ny}" r="22" fill="{t["nodo"]}" opacity=".08"/>'
                 f'<circle cx="{nx}" cy="{ny}" r="7" fill="{t["nodo"]}"/>')
    return f'<defs>{defs}</defs>{body}'


def convergencia(w, h, tema, hub, fuentes, uid='cv', sw=1.5, rad=32, salida=None, fade=True, op=1,
                 col=None, nodo=True):
    """Rutas que nacen en nodos huecos y convergen en un nodo (sistema). fuentes: [(x, y)] ordenadas
    de la más cercana a la más lejana de hub_y; giran antes las más cercanas para no cruzarse."""
    t = THEME[tema]; col = col or (C['grafito-600'] if tema == 'oscuro' else C['grafito-300'])
    HX, HY = hub
    s = []
    fs = sorted(fuentes, key=lambda p: abs(p[1] - HY))
    turn0 = HX - 64 * (len(fs) + 2)
    for k, (x, y) in enumerate(fs):
        xt = turn0 + 64 * k
        pts = [(x + 10, y), (xt, y), (xt, HY), (HX - 30, HY)] if abs(y - HY) > 1 else [(x + 10, y), (HX - 30, HY)]
        s.append(f'<path d="{ruta(pts, rad)}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>')
        s.append(f'<circle cx="{x}" cy="{y}" r="6" fill="none" stroke="{col}" stroke-width="{sw}"/>')
    if salida:
        s.append(f'<path d="{ruta([(HX + 30, HY)] + salida, rad)}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>')
        ex, ey = salida[-1]
        s.append(f'<circle cx="{ex}" cy="{ey}" r="4" fill="{col}"/>')
    # anillo abierto alrededor del hub (eco del isotipo) + nodo
    s.append(f'<path d="{arc(HX, HY, 20, 20, -40)}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>')
    body = f'<g opacity="{op}">{"".join(s)}</g>'
    if nodo:
        body += (f'<circle cx="{HX}" cy="{HY}" r="30" fill="{t["nodo"]}" opacity=".06"/>'
                 f'<circle cx="{HX}" cy="{HY}" r="7" fill="{t["nodo"]}"/>')
    return body


# ------------------------------------------------------------------ d) campo de nodos (tile)
def nodos_tile(tema, seed=7, paso=32, op=1):
    t = THEME[tema]
    col = C['grafito-400'] if tema == 'oscuro' else C['grafito-500']
    rnd = random.Random(seed)
    s = []
    n = TILE // paso
    for i in range(n):
        for j in range(n):
            x = i * paso + paso / 2; y = j * paso + paso / 2
            v = rnd.random()
            if v < 0.50:
                continue
            elif v < 0.86:
                s.append(f'<circle cx="{x:g}" cy="{y:g}" r="1" fill="{col}" opacity=".45"/>')
            elif v < 0.985:
                s.append(f'<circle cx="{x:g}" cy="{y:g}" r="1.75" fill="{col}" opacity=".7"/>')
            else:
                s.append(f'<circle cx="{x:g}" cy="{y:g}" r="4" fill="none" stroke="{col}" stroke-width="1.25" opacity=".8"/>')
    return f'<g opacity="{op}">{"".join(s)}</g>'


def nodos(w, h, tema, uid='nod', fx=None, fy=None, fr=None, nodo=(None, None), op=1, seed=11, paso=32,
          densidad=0.62):
    """Campo de nodos no repetitivo para composiciones: densidad y opacidad caen con la distancia al foco."""
    t = THEME[tema]
    col = C['grafito-400'] if tema == 'oscuro' else C['grafito-500']
    fx = w * 0.7 if fx is None else fx; fy = h * 0.45 if fy is None else fy
    fr = fr or max(w, h) * 0.7
    rnd = random.Random(seed)
    s = []
    for i in range(int(w // paso) + 1):
        for j in range(int(h // paso) + 1):
            x = i * paso + paso / 2; y = j * paso + paso / 2
            d = math.hypot(x - fx, y - fy) / fr
            k = max(0.0, 1 - d) ** 1.4
            if rnd.random() > densidad * (0.25 + 0.75 * k):
                continue
            v = rnd.random(); o = (0.25 + 0.75 * k) * op
            if v < 0.80:
                s.append(f'<circle cx="{x:g}" cy="{y:g}" r="1" fill="{col}" opacity="{o * .55:.2f}"/>')
            elif v < 0.975:
                s.append(f'<circle cx="{x:g}" cy="{y:g}" r="1.75" fill="{col}" opacity="{o * .8:.2f}"/>')
            else:
                s.append(f'<circle cx="{x:g}" cy="{y:g}" r="4" fill="none" stroke="{col}" stroke-width="1.25" opacity="{o:.2f}"/>')
    body = ''.join(s)
    if nodo[0] is not None:
        nx, ny = nodo
        body += (f'<circle cx="{nx}" cy="{ny}" r="7" fill="{t["fondo"]}"/>'
                 f'<circle cx="{nx}" cy="{ny}" r="16" fill="none" stroke="{t["nodo"]}" stroke-width="1.25" opacity=".45"/>'
                 f'<circle cx="{nx}" cy="{ny}" r="6" fill="{t["nodo"]}"/>')
    return body


# ------------------------------------------------------------------ b) retícula
def reticula_comp(w, h, tema, uid='ret', fx=None, fy=None, fr=None, nodo=(None, None)):
    t = THEME[tema]
    op = 0.035 if tema == 'oscuro' else 0.05
    body = reticula(uid, w, h, 64, t['reticula'], op, True, fx if fx is not None else w * 0.6,
                    fy if fy is not None else h * 0.45, fr or max(w, h) * 0.62, cruces=4,
                    cruz_op=0.14 if tema == 'oscuro' else 0.16)
    if nodo[0] is not None:
        nx, ny = nodo
        body += f'<circle cx="{nx}" cy="{ny}" r="6" fill="{t["nodo"]}"/>'
    return body


# ------------------------------------------------------------------ tiles sueltos
def tile_svg(kind, tema):
    t = THEME[tema]
    if kind == 'reticula':
        op = 0.035 if tema == 'oscuro' else 0.05
        cop = 0.14 if tema == 'oscuro' else 0.16
        body = (f'<path d="M0 0.5H256M0 64.5H256M0 128.5H256M0 192.5H256M0.5 0V256M64.5 0V256M128.5 0V256M192.5 0V256" '
                f'stroke="{t["reticula"]}" stroke-opacity="{op}" fill="none"/>'
                f'<path d="M-5 0.5H5M0.5 -5V5M251 0.5H261M256.5 -5V5M-5 256.5H5M0.5 251V261" stroke="{t["reticula"]}" stroke-opacity="{cop}" fill="none"/>'
                f'<path d="M0.5 0V5M0 0.5H5" stroke="{t["reticula"]}" stroke-opacity="{cop}" fill="none"/>'
                f'<path d="M251 0.5H256M0.5 251V256" stroke="{t["reticula"]}" stroke-opacity="{cop}" fill="none"/>')
        return doc(256, 256, body, f'Oryzz · patrón retícula 64 px · tile 256 · {tema}', bg=t['fondo'],
                   desc='Enlosable. Líneas cada 64 px al 3,5 % (oscuro) / 5 % (claro), cruces cada 256 px.')
    if kind == 'rutas':
        return doc(TILE, TILE, rutas_tile(tema), f'Oryzz · patrón rutas y nodos · tile 512 · {tema}', bg=t['fondo'],
                   desc='Enlosable en ambas direcciones. Sin nodo lima: se añade uno solo por composición.')
    if kind == 'nodos':
        return doc(TILE, TILE, nodos_tile(tema), f'Oryzz · patrón campo de nodos · tile 512 · {tema}', bg=t['fondo'],
                   desc='Enlosable. Puntos sobre retícula de 32 px. Sin nodo lima: se añade uno solo por composición.')


SIZES = [(1920, 1080), (1080, 1350)]


def composicion(kind, w, h, tema):
    t = THEME[tema]
    vert = h > w
    if kind == 'orbitas':
        body = orbitas(w, h, tema, cx=w * (0.78 if not vert else 0.82), cy=h * (0.60 if not vert else 0.66),
                       nodo_en=2, rot=0 if not vert else -100)
        title = 'órbitas concéntricas abiertas'
    elif kind == 'reticula':
        nx = 64 * (21 if not vert else 12); ny = 64 * (5 if not vert else 6)
        body = reticula_comp(w, h, tema, fx=w * 0.62, fy=h * 0.42, nodo=(nx, ny))
        title = 'retícula técnica 64 px'
    elif kind == 'rutas':
        tex = rutas(w, h, tema, ox=-32, oy=32, fx=w * 0.25, fy=h * 0.5, fr=max(w, h) * 0.55)
        if not vert:
            hub = (1344, 544); fu = [(192, 544), (320, 224), (448, 864), (128, 352), (256, 736)]
            sal = [(1600, 544), (1600, 352), (1920 + 20, 352)]
        else:
            hub = (736, 864); fu = [(128, 864), (256, 480), (192, 1120), (320, 672)]
            sal = [(864, 864), (864, 1120), (1080 + 20, 1120)]
        body = (reticula_comp(w, h, tema, uid='rtr', fx=hub[0], fy=hub[1], fr=max(w, h) * 0.5)
                + convergencia(w, h, tema, hub, fu, salida=sal))
        title = 'rutas y nodos'
    elif kind == 'nodos':
        body = nodos(w, h, tema, fx=w * 0.72, fy=h * 0.4, nodo=(16 + 32 * (44 if not vert else 24), 16 + 32 * (9 if not vert else 12)))
        title = 'campo de nodos'
    return doc(w, h, body, f'Oryzz · patrón {title} · {tema} · {w}×{h}', bg=t['fondo'])


def build():
    jobs = []
    for tema in ('oscuro', 'claro'):
        for kind in ('reticula', 'rutas', 'nodos'):
            write(os.path.join(OUT, 'SVG_tiles', f'patron-{kind}_tile_{tema}.svg'), tile_svg(kind, tema))
        for kind in ('orbitas', 'reticula', 'rutas', 'nodos'):
            for (w, h) in SIZES:
                name = f'patron-{kind}_{tema}_{w}x{h}'
                sp = os.path.join(OUT, 'SVG', name + '.svg')
                write(sp, composicion(kind, w, h, tema))
                jobs.append((sp, os.path.join(OUT, 'PNG', name + '.png'), w))
    png_from_svg(jobs)
    return jobs


if __name__ == '__main__':
    j = build()
    print(len(j), 'composiciones')
