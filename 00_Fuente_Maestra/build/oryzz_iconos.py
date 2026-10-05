"""
oryzz_iconos.py · Iconografía propia Oryzz v2.0 («Órbita y nodo»).

Reglas de dibujo (comunes a todos):
  · Retícula 24 px, área viva 3–21 (margen 3 px; excepciones ópticas hasta 2,5).
  · Trazo 1,75 px, stroke-linecap/linejoin round, sin rellenos (salvo nodos).
  · Radios: contenedores 3–4 px, detalles 1,5–2,5 px.
  · Nodo = círculo relleno r 1,25–2,25. Siempre separado del trazo (≥ 1,5 px), como en el isotipo.
  · Un único elemento con class="oz-acento": se colorea con la variable CSS --oz-acento
    (por defecto hereda currentColor, así el icono es monocromo si no se define).

Uso:  python oryzz_iconos.py      → genera 05_Elementos_Graficos/01_Iconos
"""
import os, math, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oryzz_svg import C, ROOT, MASTER, write, pol, arc

OUT = os.path.join(ROOT, '05_Elementos_Graficos', '01_Iconos')

ACC = ' class="oz-acento" style="color:var(--oz-acento,currentColor)"'


def N(x, y, r=1.75, acc=True):
    """Nodo relleno (acento por defecto)."""
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="currentColor" stroke="none"{ACC if acc else ""}/>'


def P(d, acc=False):
    return f'<path d="{d}"{ACC if acc else ""}/>'


def R(x, y, w, h, rx, acc=False):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}"{ACC if acc else ""}/>'


def O(cx, cy, r, acc=False):
    return f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}"{ACC if acc else ""}/>'


def chevron(tip, direction, size=3.2, spread=42):
    """Punta de flecha abierta en `tip`, apuntando en `direction` (grados)."""
    a1 = math.radians(direction + 180 - spread); a2 = math.radians(direction + 180 + spread)
    x, y = tip
    return (f'M{x + size * math.cos(a1):.2f} {y + size * math.sin(a1):.2f}L{x:.2f} {y:.2f}'
            f'L{x + size * math.cos(a2):.2f} {y + size * math.sin(a2):.2f}')


def star(cx, cy, R_, r_, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        rr = R_ if i % 2 == 0 else r_
        a = math.radians(rot + i * 180 / n)
        pts.append(f'{cx + rr * math.cos(a):.2f} {cy + rr * math.sin(a):.2f}')
    return 'M' + 'L'.join(pts) + 'Z'


# ------------------------------------------------------------------ definiciones
# nombre: (título ES, categoría, cuerpo)
ICONS = {}


def icon(name, title, cat):
    def deco(fn):
        ICONS[name] = (title, cat, fn())
        return fn
    return deco


CAT = ['Canales y servicios', 'Captación y contacto', 'Datos y resultados', 'Negocio local y Tap', 'Interfaz']

# ---------- Canales y servicios
@icon('ads-meta', 'Anuncios en redes sociales (Meta Ads)', CAT[0])
def _():
    return R(3, 3, 18, 18, 4) + N(7.75, 7.5, 1.5) + P('M11 7.5H16.25') + R(6.75, 11.25, 10.5, 6.25, 1.75)


@icon('ads-google', 'Anuncios en buscador (Google Ads)', CAT[0])
def _():
    return R(3, 3.5, 18, 7, 3.5) + P('M6.75 7H13.5') + N(4.75, 15, 1.5) + P('M8.5 15H20.5') + P('M3.5 19H14.5')


@icon('ads-tiktok', 'Anuncios en vídeo corto (TikTok Ads)', CAT[0])
def _():
    return R(6, 2.5, 12, 19, 3) + P('M10.5 9.25V14.75L15 12Z', acc=True)


@icon('geo-ia', 'GEO · búsqueda con IA', CAT[0])
def _():
    bub = 'M7 3.5H17A4 4 0 0 1 21 7.5V12.5A4 4 0 0 1 17 16.5H11.5L7 20.5V16.5A4 4 0 0 1 3 12.5V7.5A4 4 0 0 1 7 3.5Z'
    return P(bub) + P('M7.5 8H16.5') + P('M7.5 12H11') + N(14.75, 12, 1.5)


@icon('seo-local', 'SEO local', CAT[0])
def _():
    pin = 'M12 16C12 16 7.25 12.1 7.25 8.25A4.75 4.75 0 0 1 16.75 8.25C16.75 12.1 12 16 12 16Z'
    # órbita elíptica bajo el pin, abierta donde apoya la punta
    rx, ry, cx, cy = 8.5, 3, 12, 17.25
    t0, t1 = -62, 242
    x0, y0 = cx + rx * math.cos(math.radians(t0)), cy + ry * math.sin(math.radians(t0))
    x1, y1 = cx + rx * math.cos(math.radians(t1)), cy + ry * math.sin(math.radians(t1))
    ell = f'M{x0:.2f} {y0:.2f}A{rx} {ry} 0 1 1 {x1:.2f} {y1:.2f}'
    return P(pin) + N(12, 8.25, 1.6) + P(ell)


@icon('resenas', 'Reseñas', CAT[0])
def _():
    return P(star(10.75, 13, 7.9, 3.35)) + N(19.5, 4.75, 1.75)


@icon('automatizacion', 'Automatización', CAT[0])
def _():
    cx = cy = 12; r = 8
    a_end = 240; a_start = -30
    tip = pol(cx, cy, r, a_end)
    tang = a_end + 90  # dirección de avance (horario)
    return (P(arc(cx, cy, r, a_start, a_end)) + P(chevron(tip, tang, 3.1, 45))
            + N(*pol(cx, cy, r, -75), 1.75))


@icon('ia-sistema', 'IA · sistema', CAT[0])
def _():
    return (R(6.5, 6.5, 11, 11, 2.75) + P('M10 3V6.5M14 3V6.5M10 17.5V21M14 17.5V21M3 10H6.5M3 14H6.5M17.5 10H21M17.5 14H21') + N(12, 12, 1.75))


@icon('estrategia', 'Estrategia', CAT[0])
def _():
    from oryzz_svg import ruta
    return (O(5, 18.5, 2) + P(ruta([(7, 18.5), (12, 18.5), (12, 6), (15.75, 6)], 3.5)) + N(19.25, 6, 1.75))


# ---------- Captación y contacto
@icon('embudo', 'Embudo de captación', CAT[1])
def _():
    return P('M3.5 3.5H20.5L14 10.5V15L10 17V10.5Z') + N(12, 20.25, 1.5)


@icon('mensaje', 'Mensaje · WhatsApp', CAT[1])
def _():
    cx, cy, r = 12, 11.5, 8.5
    a, b = pol(cx, cy, r, 150), pol(cx, cy, r, 112)
    d = (f'M{a[0]:.2f} {a[1]:.2f}A{r} {r} 0 1 1 {b[0]:.2f} {b[1]:.2f}L3.5 20.5Z')
    return P(d) + N(8.5, 11.5, 1.1, False) + N(12, 11.5, 1.1, False) + N(15.5, 11.5, 1.1)


@icon('email', 'Email', CAT[1])
def _():
    return R(3, 5, 18, 14, 3) + P('M3.75 7.75L12 13.25L20.25 7.75', acc=True)


@icon('calendario', 'Calendario · cita', CAT[1])
def _():
    return R(3, 4.5, 18, 16.5, 3) + P('M8 2.75V6.25M16 2.75V6.25M3 10H21') + N(15.5, 15.5, 1.75)


@icon('llamada', 'Llamada', CAT[1])
def _():
    h = ('M8.2 3.5H5.6A2.1 2.1 0 0 0 3.5 5.7C3.9 13.7 10.3 20.1 18.3 20.5A2.1 2.1 0 0 0 20.5 18.4V15.8'
         'L16.6 14.3L14.6 16.3C11.8 15 9 12.2 7.7 9.4L9.7 7.4Z')
    return P(h) + P('M14.25 3.5A6.25 6.25 0 0 1 20.5 9.75') + N(15.6, 8.4, 1.4)


@icon('lead', 'Lead · contacto nuevo', CAT[1])
def _():
    return (O(10, 8, 3.5) + P('M3 20.5C3 16.6 6.1 14 10 14S17 16.6 17 20.5')
            + P('M19 4V9M16.5 6.5H21.5', acc=True))


@icon('cliente', 'Cliente', CAT[1])
def _():
    return (O(10, 8, 3.5) + P('M3 20.5C3 16.6 6.1 14 10 14S17 16.6 17 20.5') + N(19, 6.5, 2))


@icon('etiqueta', 'Etiqueta · clasificar', CAT[1])
def _():
    d = ('M3 11.6V5A2 2 0 0 1 5 3H11.6A2 2 0 0 1 13 3.6L20.4 11A2 2 0 0 1 20.4 13.8L13.8 20.4'
         'A2 2 0 0 1 11 20.4L3.6 13A2 2 0 0 1 3 11.6Z')
    return P(d) + N(7.75, 7.75, 1.5)


@icon('enviar', 'Enviar · responder', CAT[1])
def _():
    return P('M20.5 3.5L3.5 10.25L10.5 13.5L13.75 20.5Z') + P('M20.5 3.5L10.5 13.5', acc=True)


# ---------- Datos y resultados
@icon('crecimiento', 'Crecimiento', CAT[2])
def _():
    return P('M3 17.5L8.5 12L12.5 16L17.5 11') + N(20.5, 8, 1.75)


@icon('grafico', 'Dato · gráfico de barras', CAT[2])
def _():
    return P('M3.5 20.5H20.5') + P('M6.5 16.5V12.5M17.5 16.5V9.5') + P('M12 16.5V5.5', acc=True)


@icon('dashboard', 'Dashboard · panel', CAT[2])
def _():
    return R(3, 3, 18, 18, 4) + P('M3 9H21M9.5 9V21') + P('M13 17L15.25 14.5L17.5 15.75') + N(6.25, 6, 1.15)


@icon('objetivo', 'Objetivo', CAT[2])
def _():
    return P(arc(12, 12, 8.75, -22, -68)) + P(arc(12, 12, 4.75, 110, 55)) + N(12, 12, 1.6)


@icon('reloj', 'Reloj · tiempo', CAT[2])
def _():
    return O(12, 12, 8.75) + P('M12 7.25V12L15.25 14', acc=True)


@icon('euro', 'Euro · coste', CAT[2])
def _():
    return P(arc(13.75, 12, 6.5, 42, 318)) + P('M4.75 10.25H13M4.75 13.75H12')


# ---------- Negocio local y Tap
@icon('ubicacion', 'Ubicación', CAT[3])
def _():
    return P('M12 21C12 21 5 15.2 5 9.75A7 7 0 0 1 19 9.75C19 15.2 12 21 12 21Z') + N(12, 9.75, 2.25)


@icon('mapa', 'Mapa', CAT[3])
def _():
    return P('M3 6.5L9 4L15 6.5L21 4V17.5L15 20L9 17.5L3 20Z') + P('M9 4V17.5') + P('M15 6.5V20')


@icon('nfc', 'NFC · toque', CAT[3])
def _():
    cx, cy = 5.25, 12
    return (N(cx, cy, 1.75) + P(arc(cx, cy, 5, -42, 42)) + P(arc(cx, cy, 9, -42, 42))
            + P(arc(cx, cy, 13, -42, 42)))


@icon('qr', 'Código QR', CAT[3])
def _():
    return (R(3, 3, 7, 7, 2) + R(14, 3, 7, 7, 2) + R(3, 14, 7, 7, 2)
            + N(6.5, 6.5, 1.1) + N(17.5, 6.5, 1.1, False) + N(6.5, 17.5, 1.1, False)
            + P('M14 14V17M17.5 14H20.5M20.5 17.5V20.5M14 20.5H17M17.5 17.5H17.51'))


@icon('tienda', 'Tienda · negocio', CAT[3])
def _():
    aw = ('M3.5 9.5A2.83 2.83 0 0 0 9.17 9.5A2.83 2.83 0 0 0 14.83 9.5A2.83 2.83 0 0 0 20.5 9.5'
          'L19 4H5Z')
    return P(aw) + P('M5 13V20.5H19V13') + P('M10 20.5V16.5A2 2 0 0 1 14 16.5V20.5', acc=True)


@icon('pago', 'Pago', CAT[3])
def _():
    return R(2.5, 5, 19, 14, 3) + P('M2.5 9.5H21.5M6 15H10') + N(17, 15, 1.5)


@icon('menu-carta', 'Carta · menú', CAT[3])
def _():
    return (P('M6 3V7.75A2.75 2.75 0 0 0 11.5 7.75V3M8.75 3V21')
            + P('M17.5 21V3C15.5 4 14.25 6.75 14.25 10.5C14.25 12.6 15.4 13.75 17.5 13.75'))


# ---------- Interfaz
@icon('check', 'Check', CAT[4])
def _():
    return P('M4.5 12.5L9.5 17.5L19.5 6.5')


@icon('check-orbita', 'Hecho · check en órbita', CAT[4])
def _():
    return P(arc(12, 12, 9, -18, -70)) + P('M7.5 12L11 15.5L20 6.5', acc=True)


@icon('flecha', 'Flecha', CAT[4])
def _():
    return P('M4 12H20M14 6L20 12L14 18')


@icon('flecha-diagonal', 'Flecha · enlace externo', CAT[4])
def _():
    return P('M7 17L17 7M9 7H17V15')


@icon('mas', 'Más', CAT[4])
def _():
    return P('M12 5V19M5 12H19')


@icon('cerrar', 'Cerrar', CAT[4])
def _():
    return P('M6.5 6.5L17.5 17.5M17.5 6.5L6.5 17.5')


@icon('documento', 'Documento', CAT[4])
def _():
    return (P('M14 3H7.5A2.5 2.5 0 0 0 5 5.5V18.5A2.5 2.5 0 0 0 7.5 21H16.5A2.5 2.5 0 0 0 19 18.5V8Z')
            + P('M14 3V6.5A1.5 1.5 0 0 0 15.5 8H19') + P('M9 13H15M9 16.5H12.5'))


@icon('ajustes', 'Ajustes', CAT[4])
def _():
    return (P('M3.5 7.5H6.75M11.25 7.5H20.5M3.5 16.5H12.75M17.25 16.5H20.5')
            + O(9, 7.5, 2.25) + O(15, 16.5, 2.25, acc=True))


@icon('enlace', 'Enlace', CAT[4])
def _():
    g = ('M11 8.75H7.25A3.25 3.25 0 0 0 7.25 15.25H11M13 8.75H16.75A3.25 3.25 0 0 1 16.75 15.25H13')
    return f'<g transform="rotate(-45 12 12)">{P(g)}{P("M9 12H15")}</g>'


@icon('usuario', 'Usuario', CAT[4])
def _():
    return O(12, 7.75, 3.75) + P('M4.75 20.5C4.75 16.6 8 14 12 14S19.25 16.6 19.25 20.5')


@icon('equipo', 'Equipo', CAT[4])
def _():
    return (O(9, 8.25, 3.25) + P('M2.75 20.25C2.75 16.8 5.5 14.5 9 14.5S15.25 16.8 15.25 20.25')
            + O(16.5, 7.25, 2.75) + P('M17.25 13.25C19.6 13.6 21.25 15.9 21.25 19'))


@icon('busqueda', 'Búsqueda', CAT[4])
def _():
    return O(10.5, 10.5, 6.75) + P('M15.5 15.5L20.5 20.5')


# ------------------------------------------------------------------ salida
HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" '
        'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"')


def svg_icon(name, color=None, acento=None):
    title, cat, body = ICONS[name]
    st = ''
    if color:
        st = f' style="color:{color}' + (f';--oz-acento:{acento}' if acento else '') + '"'
    return f'{HEAD} role="img" aria-label="{html.escape(title)}"{st}><title>{html.escape(title)}</title>{body}</svg>\n'


def sprite():
    syms = []
    for n, (t, c, b) in ICONS.items():
        syms.append(f'<symbol id="oz-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
                    f'stroke-linecap="round" stroke-linejoin="round"><title>{html.escape(t)}</title>{b}</symbol>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">\n'
            '<!-- Oryzz · sprite de iconos v2.0. Uso: <svg class="oz-icon"><use href="iconos-sprite.svg#oz-calendario"/></svg>\n'
            '     Color: CSS color (trazo) y --oz-acento (nodo o trazo de acento). -->\n'
            + '\n'.join(syms) + '\n</svg>\n')


VARIANTS = {
    # nombre: (color trazo, color acento)
    'grafito': (C['grafito-950'], None),
    'blanco': (C['blanco'], None),
    'grafito_acento-lima': (C['grafito-950'], C['lima-600']),
    'blanco_acento-lima': (C['blanco'], C['lima-500']),
}


def build_pngs(tmpdir):
    from PIL import Image
    from render import html_to_png
    names = list(ICONS)
    cols = 8; rows = math.ceil(len(names) / cols)
    for size in (64, 256):
        for vname, (col, acc) in VARIANTS.items():
            cells = ''.join(
                f'<div class="c">{svg_icon(n, col, acc)}</div>' for n in names)
            page = (f'<!doctype html><html><head><style>html,body{{margin:0;background:transparent}}'
                    f'.g{{display:grid;grid-template-columns:repeat({cols},{size}px);grid-auto-rows:{size}px}}'
                    f'.c svg{{width:{size}px;height:{size}px;display:block}}</style></head>'
                    f'<body><div class="g">{cells}</div></body></html>')
            hp = os.path.join(tmpdir, f'ic_{size}_{vname}.html')
            open(hp, 'w', encoding='utf8').write(page)
            sheet = os.path.join(tmpdir, f'ic_{size}_{vname}.png')
            html_to_png(hp, sheet, cols * size, rows * size, transparent=True)
            im = Image.open(sheet).convert('RGBA')
            od = os.path.join(OUT, f'PNG_{size}', vname)
            os.makedirs(od, exist_ok=True)
            for i, n in enumerate(names):
                x = (i % cols) * size; y = (i // cols) * size
                im.crop((x, y, x + size, y + size)).save(os.path.join(od, f'oz-icono_{n}_{vname}_{size}.png'), optimize=True)


def build_svgs():
    for n in ICONS:
        write(os.path.join(OUT, 'SVG', f'oz-icono_{n}.svg'), svg_icon(n))
    write(os.path.join(OUT, 'iconos-sprite.svg'), sprite())


# ------------------------------------------------------------------ lámina
def build_lamina():
    from render import html_to_png, html_to_pdf
    groups = ''
    for cat in CAT:
        items = [n for n, v in ICONS.items() if v[1] == cat]
        cells = ''.join(f'<figure>{svg_icon(n)}<figcaption>{n}</figcaption></figure>' for n in items)
        full = ' full' if cat == CAT[4] else ''
        groups += f'<section class="grp{full}"><h3 class="t-eyebrow">{cat}<span>{len(items):02d}</span></h3><div class="cells">{cells}</div></section>'
    # construcción: icono ampliado sobre retícula
    k = 'calendario'
    big = svg_icon(k)
    keyl = ('<svg class="key" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="4" />'
            '<circle cx="12" cy="12" r="9" /><rect x="0.5" y="0.5" width="23" height="23" class="edge"/></svg>')
    ramp = ''.join(f'<div class="rs"><div style="width:{s}px;height:{s}px">{svg_icon("automatizacion")}</div><span>{s}</span></div>' for s in (16, 20, 24, 32, 48))
    on_light = ''.join(svg_icon(n) for n in ('calendario', 'crecimiento', 'mensaje', 'resenas', 'nfc'))
    on_dark = on_light
    total = len(ICONS)
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Iconografía Oryzz</title>
<link rel="stylesheet" href="../../00_Fuente_Maestra/brand.css">
<style>
@page{{size:1920px 2060px;margin:0}}
*{{box-sizing:border-box}} html,body{{margin:0;background:var(--grafito-950);color:#fff}}
body{{width:1920px;height:2060px;position:relative;overflow:hidden;font-family:var(--font-texto)}}
.wrap{{padding:120px 120px 0}}
.t-eyebrow{{color:var(--grafito-400);margin:0}}
header{{display:grid;grid-template-columns:1fr 700px;gap:96px;align-items:end;border-bottom:1px solid var(--grafito-700);padding-bottom:64px}}
h1{{font-family:var(--font-display);font-weight:700;font-size:96px;letter-spacing:-.045em;line-height:.95;margin:28px 0 28px}}
h1 em{{font-style:normal;color:var(--azul-400)}}
.lead{{font-size:20px;line-height:1.55;color:var(--grafito-200);max-width:720px;margin:0}}
.spec{{display:grid;grid-template-columns:260px 1fr;gap:32px;align-items:center}}
.cons{{position:relative;width:260px;height:260px;background:var(--grafito-850);border:1px solid var(--grafito-700);border-radius:20px;
  background-image:linear-gradient(#ffffff0d 1px,transparent 1px),linear-gradient(90deg,#ffffff0d 1px,transparent 1px);background-size:10px 10px;background-position:10px 10px}}
.cons svg{{position:absolute;left:10px;top:10px;width:240px;height:240px}}
.cons svg.ic{{color:var(--grafito-200);--oz-acento:var(--lima-500)}}
.key{{fill:none;stroke:var(--azul-400);stroke-width:.08;stroke-dasharray:.3 .3}} .key .edge{{stroke:var(--grafito-600);stroke-dasharray:none}}
dl{{margin:0;font-family:var(--font-mono);font-size:14px;line-height:1.3;display:grid;grid-template-columns:auto 1fr;gap:12px 20px}}
dt{{color:var(--grafito-400);text-transform:uppercase;letter-spacing:.12em}} dd{{margin:0;color:#fff}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:56px 96px;margin-top:64px}}
.grp h3{{display:flex;justify-content:space-between;border-bottom:1px solid var(--grafito-700);padding-bottom:14px;margin-bottom:8px;font-weight:500;font-size:14px}}
.grp h3 span{{color:var(--grafito-600)}}
.cells{{display:grid;grid-template-columns:repeat(5,1fr)}} .grp.full{{grid-column:1/-1}} .full .cells{{grid-template-columns:repeat(10,1fr)}}
figure{{margin:0;height:132px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;border-bottom:1px solid var(--grafito-850)}}
figure svg{{width:40px;height:40px;color:var(--grafito-200);--oz-acento:var(--lima-500)}}
figcaption{{font-family:var(--font-mono);font-size:14px;color:var(--grafito-400)}}
.foot{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:32px;margin-top:64px}}
.box{{border:1px solid var(--grafito-700);border-radius:20px;padding:32px;height:220px;display:flex;flex-direction:column;justify-content:space-between}}
.box p{{margin:0;font-size:16px;color:var(--grafito-200);line-height:1.5}}
.ramp{{display:flex;align-items:flex-end;gap:36px}} .rs{{display:flex;flex-direction:column;align-items:center;gap:12px}}
.rs svg{{width:100%;height:100%;color:#fff;--oz-acento:var(--lima-500)}} .rs span{{font-family:var(--font-mono);font-size:14px;color:var(--grafito-400)}}
.row{{display:flex;gap:28px}} .row svg{{width:32px;height:32px}}
.box.l{{background:#fff;border-color:#fff}} .box.l p{{color:var(--grafito-600)}} .box.l .t-eyebrow{{color:var(--grafito-500)}}
.box.l .row svg{{color:var(--grafito-950);--oz-acento:var(--lima-600)}}
.box.d .row svg{{color:var(--grafito-200);--oz-acento:var(--lima-500)}}
.colophon{{position:absolute;left:120px;right:120px;bottom:56px;display:flex;justify-content:space-between;font-family:var(--font-mono);font-size:14px;color:var(--grafito-500);letter-spacing:.08em}}
</style></head><body><div class="wrap">
<header><div><p class="t-eyebrow">Oryzz · Sistema gráfico v2.0 · 05 · Elementos gráficos</p>
<h1>Iconografía<br><em>propia.</em></h1>
<p class="lead">{total} iconos dibujados sobre la misma retícula que la órbita del logo. Trazo fino, puntas redondas y un único acento: el nodo, que marca el resultado (la cita, el lead, el cliente).</p></div>
<div class="spec"><div class="cons">{keyl.replace('<svg class="key"', '<svg class="key"')}{big.replace('<svg ', '<svg class="ic" ', 1)}</div>
<dl><dt>Retícula</dt><dd>24 × 24 px · área viva 18</dd><dt>Trazo</dt><dd>1,75 px · round</dd><dt>Radios</dt><dd>3–4 contenedor · 1,5–2,5 detalle</dd>
<dt>Nodo</dt><dd>r 1,25–2,25 · separado ≥ 1,5</dd><dt>Acento</dt><dd>.oz-acento · --oz-acento</dd><dt>Color</dt><dd>currentColor</dd></dl></div></header>
<div class="grid">{groups}</div>
<div class="foot">
<div class="box"><p class="t-eyebrow">Escala · px</p><div class="ramp">{ramp}</div></div>
<div class="box d"><p class="t-eyebrow">Sobre oscuro · Grafito 200 + Lima 500</p><div class="row">{on_dark}</div><p>El acento es opcional. Si la pieza ya tiene otro dato en lima, los iconos van monocromos.</p></div>
<div class="box l"><p class="t-eyebrow">Sobre claro · Grafito 950 + Lima 600</p><div class="row">{on_light}</div><p>Nunca rellenos, nunca en varios colores, nunca logos de plataformas en color.</p></div>
</div></div>
<div class="colophon"><span>ORYZZ · ICONOS · 24 PX · 1,75</span><span>05_Elementos_Graficos/01_Iconos</span></div>
</body></html>'''
    hp = os.path.join(OUT, 'iconos-lamina.html')
    write(hp, page)
    html_to_png(hp, os.path.join(OUT, 'iconos-lamina.png'), 1920, 2060)
    html_to_pdf(hp, os.path.join(OUT, 'iconos-lamina.pdf'))


if __name__ == '__main__':
    tmp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get('TEMP', '.'), 'oz_iconos')
    os.makedirs(tmp, exist_ok=True)
    build_svgs()
    if '--sin-png' not in sys.argv:
        build_pngs(tmp)
    build_lamina()
    print(len(ICONS), 'iconos')
