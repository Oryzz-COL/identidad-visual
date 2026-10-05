"""
Oryzz · recursos gráficos para presentaciones (PNG 2x generados desde SVG/HTML con Chrome).
Se regeneran solo si cambia su definición (caché por hash).
"""
import os, math, json, hashlib, tempfile
from render import svg_to_png, html_to_png

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
LOGOS = os.path.join(ROOT, '02_Logos')
BRAND_CSS = os.path.join(ROOT, '00_Fuente_Maestra', 'brand.css')
CACHE = os.path.join(tempfile.gettempdir(), 'oryzz_pres_assets_cache.json')

_cache = None


def _load():
    global _cache
    if _cache is None:
        try:
            _cache = json.load(open(CACHE, encoding='utf8'))
        except Exception:
            _cache = {}
    return _cache


def _save():
    json.dump(_cache, open(CACHE, 'w', encoding='utf8'))


def _fresh(out, key):
    c = _load()
    h = hashlib.md5(key.encode('utf8')).hexdigest()
    if os.path.exists(out) and c.get(os.path.abspath(out)) == h:
        return True, h
    return False, h


def _mark(out, h):
    _load()[os.path.abspath(out)] = h
    _save()


def svg_png(out, svg, w=1920, h=1080, scale=2):
    """Rasteriza un SVG (string) a PNG transparente a `scale`x."""
    ok, hsh = _fresh(out, svg + f'{w}{h}{scale}')
    if ok:
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = os.path.join(tempfile.gettempdir(), 'oryzz_' + hsh + '.svg')
    open(tmp, 'w', encoding='utf8').write(svg)
    svg_to_png(tmp, out, width=int(w * scale), height=int(h * scale))
    os.unlink(tmp)
    _mark(out, hsh)
    return out


def html_png(out, body_html, w, h, scale=2, transparent=True, extra_css=''):
    """Rasteriza HTML (con las fuentes de marca) a PNG a `scale`x."""
    css_url = 'file:///' + BRAND_CSS.replace('\\', '/')
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{css_url}">'
           f'<style>html,body{{margin:0;padding:0;background:transparent;overflow:hidden}}'
           f'.stage{{width:{w}px;height:{h}px;position:relative;zoom:{scale}}}{extra_css}</style></head>'
           f'<body><div class="stage">{body_html}</div></body></html>')
    ok, hsh = _fresh(out, doc + str(transparent))
    if ok:
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = os.path.join(tempfile.gettempdir(), 'oryzz_' + hsh + '.html')
    open(tmp, 'w', encoding='utf8').write(doc)
    html_to_png(tmp, out, int(w * scale), int(h * scale), transparent=transparent)
    os.unlink(tmp)
    _mark(out, hsh)
    return out


def logo_png(rel_svg, out, width):
    src = os.path.join(LOGOS, rel_svg)
    key = open(src, encoding='utf8').read() + str(width)
    ok, hsh = _fresh(out, key)
    if ok:
        return out
    svg_to_png(src, out, width=width)
    _mark(out, hsh)
    return out


# ---------------------------------------------------------------- primitivas SVG
def pt(cx, cy, r, a):
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def arc(cx, cy, r, a0, a1):
    """Arco en sentido horario (y hacia abajo) de a0 a a1 grados."""
    x0, y0 = pt(cx, cy, r, a0)
    x1, y1 = pt(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f'M{x0:.2f} {y0:.2f}A{r:.2f} {r:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}'


def orbit_system(cx, cy, radii, gap_start=-30, gap_step=53, gap=62, color='#232836', sw=1.5,
                 accent_i=None, accent_color='#5C8BFF', accent_span=64, accent_sw=2, node_color='#BFF24A',
                 node_r=9, knock=6, extra_nodes=()):
    """Órbitas abiertas concéntricas. Devuelve el cuerpo SVG.
    Cada órbita i tiene su hueco centrado en gap_start + i*gap_step.
    En la órbita accent_i, los últimos `accent_span` grados antes del hueco van en azul y el nodo cierra el trazo."""
    out = []
    for i, r in enumerate(radii):
        g = gap_start + i * gap_step
        a0, a1 = g + gap / 2, g - gap / 2 + 360   # empieza tras el hueco, termina antes
        if i == accent_i:
            kd = math.degrees((node_r + knock) / r)
            end = a1
            out.append(f'<path d="{arc(cx, cy, r, a0, end - accent_span)}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
            out.append(f'<path d="{arc(cx, cy, r, end - accent_span, end)}" fill="none" stroke="{accent_color}" stroke-width="{accent_sw}" stroke-linecap="round"/>')
            nx, ny = pt(cx, cy, r, end + kd)
            out.append(f'<circle cx="{nx:.2f}" cy="{ny:.2f}" r="{node_r}" fill="{node_color}"/>')
        else:
            out.append(f'<path d="{arc(cx, cy, r, a0, a1)}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    for (r, a, col, nr) in extra_nodes:
        x, y = pt(cx, cy, r, a)
        out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{nr}" fill="{col}"/>')
    return ''.join(out)


def svg_doc(body, w=1920, h=1080, defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{defs}</defs>{body}</svg>'


def grid_svg(color, opacity=0.035, step=64, w=1920, h=1080, fade=True, cx=0.5, cy=0.5, rx=0.62, ry=0.75):
    lines = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w + 1, step))
    lines += ''.join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h + 1, step))
    defs = ''
    mask = ''
    if fade:
        defs = (f'<radialGradient id="f" cx="{cx}" cy="{cy}" r="0.5" gradientTransform="translate({cx} {cy}) scale({rx * 2} {ry * 2}) translate({-cx} {-cy})">'
                f'<stop offset="0" stop-color="#fff"/><stop offset="0.55" stop-color="#fff" stop-opacity="0.85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
                f'<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="url(#f)"/></mask>')
        mask = ' mask="url(#m)"'
    body = f'<g{mask}><g stroke="{color}" stroke-opacity="{opacity}" stroke-width="1">{lines}</g></g>'
    return svg_doc(body, w, h, defs)


def halo_svg(cx, cy, r, color, opacity=0.16, w=1920, h=1080):
    defs = (f'<radialGradient id="h" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{r}">'
            f'<stop offset="0" stop-color="{color}" stop-opacity="{opacity}"/><stop offset="0.6" stop-color="{color}" stop-opacity="{opacity * 0.35}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')
    return svg_doc(f'<rect width="{w}" height="{h}" fill="url(#h)"/>', w, h, defs)


def rounded_route(points, r=24):
    """Polilínea ortogonal con esquinas redondeadas."""
    d = f'M{points[0][0]:.1f} {points[0][1]:.1f}'
    for i in range(1, len(points) - 1):
        (x0, y0), (x1, y1), (x2, y2) = points[i - 1], points[i], points[i + 1]
        v1 = (x1 - x0, y1 - y0); v2 = (x2 - x1, y2 - y1)
        l1 = math.hypot(*v1); l2 = math.hypot(*v2)
        rr = min(r, l1 / 2, l2 / 2)
        if rr < 0.5:
            d += f'L{x1:.1f} {y1:.1f}'
            continue
        p1 = (x1 - v1[0] / l1 * rr, y1 - v1[1] / l1 * rr)
        p2 = (x1 + v2[0] / l2 * rr, y1 + v2[1] / l2 * rr)
        d += f'L{p1[0]:.1f} {p1[1]:.1f}Q{x1:.1f} {y1:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    d += f'L{points[-1][0]:.1f} {points[-1][1]:.1f}'
    return d
