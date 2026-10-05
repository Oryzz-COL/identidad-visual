"""
Exportación de producción de 02_Logos (PNG, PDF vectorial, pack favicon/app, avatares de redes).
Parte SIEMPRE de los SVG maestros generados por oryzz_logo.py (no los modifica).

Uso:  python export_logos.py [png] [pdf] [favicon] [redes]      (sin argumentos: todo)

Encuadre de los PNG/PDF: el del SVG maestro (los lockups ya traen un margen uniforme de 32 u
en los cuatro lados; isotipo y avatares mantienen su caja cuadrada).
"""
import os, re, sys, json, math, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oryzz_logo as L
from render import html_to_pdf
from render_fast import Chrome

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '02_Logos'))

FAMILIES = [
    # carpeta, subcarpeta SVG, subcarpeta PNG, anchos, encuadre, ancho PDF (mm)
    ('01_Horizontal', 'SVG', 'PNG', [800, 1600, 3200], 'lockup', 100),
    ('02_Vertical', 'SVG', 'PNG', [500, 1000, 2000], 'lockup', 60),
    ('03_Wordmark', 'SVG', 'PNG', [800, 1600, 3200], 'lockup', 80),
    ('04_Isotipo', 'SVG', 'PNG', [256, 512, 1024, 2048], 'square', 40),
    ('04_Isotipo', 'SVG_tamano_pequeno', 'PNG_tamano_pequeno', [16, 24, 32, 48, 64], 'square', None),
    ('05_Avatar_Perfil', 'SVG', 'PNG', [256, 512, 1024, 2048], 'square', None),
    ('07_Submarca_Tap', 'SVG', 'PNG', [800, 1600, 3200], 'lockup', 120),
]

PAD = 0.035


def read(p):
    return open(p, encoding='utf8').read()


def viewbox(svg):
    m = re.search(r'viewBox="([-\d.\s]+)"', svg)
    return [float(v) for v in m.group(1).split()]


def set_viewbox(svg, vb):
    return re.sub(r'viewBox="[^"]*"', 'viewBox="%.2f %.2f %.2f %.2f"' % tuple(vb), svg, count=1)


def content_bbox(c, svg_path, probe_w=4000):
    """bbox del contenido (unidades SVG) a partir de un render de sondeo."""
    vx, vy, vw, vh = viewbox(read(svg_path))
    tmp = os.path.join(c.tmpdir, 'probe.png')
    w, h = c.svg_to_png(svg_path, tmp, probe_w)
    a = Image.open(tmp).getchannel('A')
    x0, y0, x1, y1 = a.getbbox()
    sx, sy = vw / w, vh / h
    return (vx + x0 * sx, vy + y0 * sy, vx + x1 * sx, vy + y1 * sy)


def framed_svg(c, svg_path, mode):
    """Texto SVG para exportar. Desde v2.0.1 los maestros ya traen margen uniforme: se usan tal cual."""
    return read(svg_path)


def iter_svgs():
    for fam, sub, pngsub, widths, mode, pdfw in FAMILIES:
        d = os.path.join(ROOT, fam, sub)
        for f in sorted(os.listdir(d)):
            if f.endswith('.svg'):
                yield fam, sub, pngsub, widths, mode, pdfw, os.path.join(d, f)


# ------------------------------------------------------------------ PNG
def export_png(c, framed_cache):
    n = 0
    for fam, sub, pngsub, widths, mode, pdfw, p in iter_svgs():
        svg = framed_cache.setdefault(p, framed_svg(c, p, mode))
        tmp = os.path.join(c.tmpdir, 'framed.svg')
        open(tmp, 'w', encoding='utf8').write(svg)
        base = os.path.basename(p)[:-4]
        outdir = os.path.join(ROOT, fam, pngsub)
        for w in widths:
            c.svg_to_png(tmp, os.path.join(outdir, f'{base}_{w}.png'), w)
            n += 1
    print('PNG:', n)


# ------------------------------------------------------------------ PDF
PDF_HTML = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>
@page{{size:{w:.3f}mm {h:.3f}mm;margin:0}}
html,body{{margin:0;padding:0;width:{w:.3f}mm;height:{h:.3f}mm;overflow:hidden;background:transparent}}
svg{{display:block;width:{w:.3f}mm;height:{hs:.3f}mm}}
</style></head><body>{svg}</body></html>"""


def export_pdf(c, framed_cache):
    n = 0
    tmpd = tempfile.mkdtemp(prefix='oryzz_pdf_')
    for fam, sub, pngsub, widths, mode, pdfw, p in iter_svgs():
        if not pdfw:
            continue
        svg = framed_cache.setdefault(p, framed_svg(c, p, mode))
        vx, vy, vw, vh = viewbox(svg)
        w = pdfw; h = pdfw * vh / vw
        svg_inline = re.sub(r'<title>.*?</title>', '', svg)
        base = os.path.basename(p)[:-4]
        html = PDF_HTML.format(title=base, w=w, h=h, hs=h - 0.01, svg=svg_inline)
        hp = os.path.join(tmpd, base + '.html')
        open(hp, 'w', encoding='utf8').write(html)
        html_to_pdf(hp, os.path.join(ROOT, fam, 'PDF', base + '.pdf'))
        n += 1
    print('PDF:', n)


# ------------------------------------------------------------------ favicon / app
def icon_svg(bg, way, s, shape='full', small=False, uid='ic'):
    """Icono cuadrado 100x100: fondo a sangre (full) o baldosa redondeada (tile)."""
    w = L.WAYS[way]
    base = (f'<rect width="100" height="100" fill="{bg}"/>' if shape == 'full'
            else f'<rect width="100" height="100" rx="22.5" fill="{bg}"/>')
    sw, nr = (14.0, 9.0) if small else (L.SW, L.NR)
    body = base + L._defs(w, uid, (10, 10, 90, 90), None) + L.mark_group(w, uid, 50 - 50 * s, 50 - 50 * s + 1, s, sw, nr)
    return L.svg(100, 100, body, 'oryzz')


def export_favicon(c):
    d = os.path.join(ROOT, '06_Favicon')
    src = os.path.join(d, 'fuentes_svg'); os.makedirs(src, exist_ok=True)
    fav = os.path.join(d, 'favicon.svg')
    # 16/32/48 directos (sin reescalar) desde favicon.svg
    ims = []
    for s in (16, 32, 48):
        out = os.path.join(d, f'favicon-{s}.png')
        c.svg_to_png(fav, out, s)
        ims.append(Image.open(out).convert('RGBA'))
    ims[2].save(os.path.join(d, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32), (48, 48)],
                append_images=[ims[0], ims[1]])
    os.remove(os.path.join(d, 'favicon-48.png'))  # solo vive dentro del .ico
    G = L.C['graphite']
    # apple-touch: a sangre (iOS aplica su propia máscara y rellena la transparencia en negro)
    apple = icon_svg(G, 'color-sobre-oscuro', 0.60, 'full', uid=L.uid_for('apple-touch-icon', 'color-sobre-oscuro'))
    open(os.path.join(src, 'apple-touch-icon.svg'), 'w', encoding='utf8').write(apple)
    # android "any": baldosa redondeada = avatar cuadrado maestro
    android = read(os.path.join(ROOT, '05_Avatar_Perfil', 'SVG', 'oryzz-avatar-cuadrado_color-sobre-oscuro.svg'))
    # maskable: a sangre, isotipo dentro de la zona segura (círculo del 80 %)
    mask = icon_svg(G, 'color-sobre-oscuro', 0.50, 'full', uid=L.uid_for('maskable', 'color-sobre-oscuro'))
    open(os.path.join(src, 'maskable.svg'), 'w', encoding='utf8').write(mask)
    for name, svg, size in [('apple-touch-icon-180.png', apple, 180), ('android-chrome-192.png', android, 192),
                            ('android-chrome-512.png', android, 512), ('maskable-512.png', mask, 512)]:
        c.svg_string_to_png(svg, os.path.join(d, name), size, size)
    manifest = {
        'name': 'Oryzz', 'short_name': 'Oryzz',
        'description': 'Sistemas que captan clientes.',
        'start_url': '/', 'scope': '/', 'display': 'standalone', 'lang': 'es',
        'theme_color': G, 'background_color': G,
        'icons': [
            {'src': '/android-chrome-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': '/android-chrome-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
            {'src': '/maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        ],
    }
    open(os.path.join(d, 'site.webmanifest'), 'w', encoding='utf8').write(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    snippet = """<!-- Oryzz · favicon y app — pegar dentro de <head>. Sube todos los archivos de 06_Favicon a la raíz del dominio. -->
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/favicon-16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0B0D12">
"""
    open(os.path.join(d, 'snippet-head.html'), 'w', encoding='utf8').write(snippet)
    print('Favicon: ok')


# ------------------------------------------------------------------ avatares de redes
REDES = [
    # nombre, fondo, colorway del isotipo
    ('oryzz-avatar-redes_color-sobre-oscuro', L.C['graphite'], 'color-sobre-oscuro'),
    ('oryzz-avatar-redes_sobre-azul', L.C['blue'], 'sobre-azul'),
    ('oryzz-tap-avatar-redes_color-sobre-claro', '#F6F7F9', 'color-sobre-claro'),
    ('oryzz-tap-avatar-redes_color-sobre-blanco', '#FFFFFF', 'color-sobre-claro'),
]


def export_redes(c):
    d = os.path.join(ROOT, '05_Avatar_Perfil')
    out = os.path.join(d, 'PNG_redes'); src = os.path.join(d, 'SVG_redes')
    os.makedirs(out, exist_ok=True); os.makedirs(src, exist_ok=True)
    for name, bg, way in REDES:
        svg = icon_svg(bg, way, 0.60, 'full', uid=name + '-')
        open(os.path.join(src, name + '.svg'), 'w', encoding='utf8').write(svg)
        for s in (1080, 400):
            c.svg_string_to_png(svg, os.path.join(out, f'{name}_{s}.png'), s, s)
    # vista previa del recorte circular (cómo se verá en Instagram / WhatsApp / TikTok / LinkedIn)
    tiles = []
    for name, bg, way in REDES:
        im = Image.open(os.path.join(out, f'{name}_400.png')).convert('RGBA')
        m = Image.new('L', (1600, 1600), 0)
        from PIL import ImageDraw
        ImageDraw.Draw(m).ellipse((0, 0, 1599, 1599), fill=255)
        m = m.resize((400, 400), Image.LANCZOS)
        t = Image.new('RGBA', (400, 400), (0, 0, 0, 0)); t.paste(im, (0, 0), m); tiles.append(t)
    sheet = Image.new('RGBA', (4 * 400 + 5 * 60, 520), (229, 232, 238, 255))
    for i, t in enumerate(tiles):
        sheet.alpha_composite(t, (60 + i * 460, 60))
    sheet.convert('RGB').save(os.path.join(out, '_vista-previa-recorte-circular.png'))
    print('Redes: ok')


if __name__ == '__main__':
    steps = sys.argv[1:] or ['png', 'pdf', 'favicon', 'redes']
    cache = {}
    with Chrome() as c:
        if 'png' in steps: export_png(c, cache)
        if 'pdf' in steps: export_pdf(c, cache)
        if 'favicon' in steps: export_favicon(c)
        if 'redes' in steps: export_redes(c)
