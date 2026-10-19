"""
Oryzz · utilidades para piezas impresas (SVG en mm, sangrado, marcas de corte, PDF).

Convención: cada cara se dibuja en coordenadas de corte (0,0)-(W,H) en mm.
El sangrado se extiende a (-b,-b)-(W+b,H+b). Los fondos deben llegar al sangrado.
"""
import os, re, sys, tempfile, pathlib, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render import _run, _url

ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
LOGOS = os.path.join(ROOT, '02_Logos')
BRAND_CSS = os.path.join(ROOT, '00_Fuente_Maestra', 'brand.css')
PT = 0.3528  # mm por punto

C = dict(g950='#0B0D12', g850='#12151D', g800='#171B25', g700='#232836', g600='#3A4152', g500='#5A6172',
         g400='#8A90A0', g300='#C7CBD6', g200='#D5D9E0', g100='#E5E8EE', g50='#F6F7F9', w='#FFFFFF',
         az500='#3B72FF', az600='#2C5BD0', az400='#5C8BFF', cy500='#36CFE0', cy600='#17A9C2',
         li500='#BFF24A', li600='#7FB02E')

FONT = {'display': "'Space Grotesk', Arial, sans-serif", 'texto': "Manrope, Arial, sans-serif",
        'mono': "'JetBrains Mono', Consolas, monospace"}

_uid = itertools.count(1)

LOGO_FILES = {
    'h': '01_Horizontal/SVG/oryzz-logo-horizontal_{}.svg',
    'v': '02_Vertical/SVG/oryzz-logo-vertical_{}.svg',
    'w': '03_Wordmark/SVG/oryzz-wordmark_{}.svg',
    'i': '04_Isotipo/SVG/oryzz-isotipo_{}.svg',
    'is': '04_Isotipo/SVG_tamano_pequeno/oryzz-isotipo-small_{}.svg',
    't': '07_Submarca_Tap/SVG/oryzz-tap-horizontal_{}.svg',
}


def logo(kind, way, x, y, w=None, h=None):
    """Inserta un logo maestro como <svg> anidado (vectorial, sin redibujar). Devuelve (svg, w, h)."""
    src = open(os.path.join(LOGOS, LOGO_FILES[kind].format(way)), encoding='utf8').read()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    vx, vy, vw, vh = [float(v) for v in vb.split()]
    if w and not h:
        h = w * vh / vw
    elif h and not w:
        w = h * vw / vh
    inner = re.sub(r'^.*?<svg[^>]*>', '', src, count=1, flags=re.S)
    inner = re.sub(r'</svg>\s*$', '', inner.strip())
    inner = re.sub(r'<title>.*?</title>', '', inner)
    p = f'L{next(_uid)}_'
    inner = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m.group(1)})', inner)
    s = (f'<svg x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" viewBox="{vb}" '
         f'preserveAspectRatio="xMinYMin meet" data-logo="{kind}-{way}">{inner}</svg>')
    return s, w, h


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def text(x, y, s, pt=9, font='texto', weight=400, fill='#0B0D12', anchor='start', track=0.0, caps=False, extra=''):
    size = pt * PT
    if caps:
        s = s.upper()
    ls = f' letter-spacing="{size * track:.3f}"' if track else ''
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT[font]}" font-size="{size:.3f}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{ls}{extra}>{esc(s)}</text>')


def lines(x, y, rows, pt=9, lh=1.45, **kw):
    out = []
    for i, r in enumerate(rows):
        out.append(text(x, y + i * pt * PT * lh, r, pt, **kw))
    return ''.join(out)


def rect(x, y, w, h, fill, rx=0, extra=''):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}"{extra}/>'


def fondo(W, H, fill, b=3):
    return rect(-b, -b, W + 2 * b, H + 2 * b, fill)


def nfc_icon(x, y, s, color, sw=None):
    """Icono lineal NFC (retícula 24, trazo 1,75): teléfono + ondas. s = lado en mm."""
    k = s / 24
    sw = sw or 1.75
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f})" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">'
            f'<rect x="4" y="5" width="9" height="15" rx="2"/><path d="M7.5 17h2"/>'
            f'<path d="M16 9.5a4 4 0 0 1 0 5"/><path d="M18.6 7a7.5 7.5 0 0 1 0 10"/></g>')


# ---------------------------------------------------------------- composición de SVG
def svg_cara(W, H, body, b=3, guias=True, troquel=None, titulo='Oryzz'):
    """SVG editable de una cara con sangrado; guías (corte, seguridad) ocultas y troquel opcional."""
    g = ''
    if guias:
        g = (f'<g id="guias-no-imprimir" display="none" fill="none" stroke-width="0.2">'
             f'<rect x="0" y="0" width="{W}" height="{H}" stroke="#00A0E3"/>'
             f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" stroke="#00A0E3" stroke-dasharray="1 1"/></g>')
    t = ''
    if troquel:
        t = f'<g id="troquel-no-imprimir" display="none" fill="none" stroke="#E6007E" stroke-width="0.25">{troquel}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-b} {-b} {W + 2 * b} {H + 2 * b}" '
            f'width="{W + 2 * b}mm" height="{H + 2 * b}mm"><title>{esc(titulo)}</title>'
            f'<g id="arte">{body}</g>{g}{t}</svg>\n')


def _marcas(W, H, b=3, largo=5, info=''):
    o = []
    for (x, y) in ((0, 0), (W, 0), (0, H), (W, H)):
        sx = -1 if x == 0 else 1
        sy = -1 if y == 0 else 1
        o.append(f'<line x1="{x + sx * b:.2f}" y1="{y}" x2="{x + sx * (b + largo):.2f}" y2="{y}"/>')
        o.append(f'<line x1="{x}" y1="{y + sy * b:.2f}" x2="{x}" y2="{y + sy * (b + largo):.2f}"/>')
    m = f'<g stroke="#000000" stroke-width="0.25" fill="none">{"".join(o)}</g>'
    if info:
        fs = 2.1 if W >= 110 else 1.35
        m += (f'<text x="{-b - largo + 0.5 if W < 110 else 0:.2f}" y="{H + b + largo + 2.6:.2f}" font-family="{FONT["mono"]}" font-size="{fs}" fill="#000000">{esc(info)}</text>')
    return m


def svg_con_marcas(W, H, body, b=3, slug=10, info=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-b - slug} {-b - slug} {W + 2 * (b + slug)} {H + 2 * (b + slug)}" '
            f'width="{W + 2 * (b + slug)}mm" height="{H + 2 * (b + slug)}mm">'
            f'<defs><clipPath id="sangrado"><rect x="{-b}" y="{-b}" width="{W + 2 * b}" height="{H + 2 * b}"/></clipPath></defs>'
            f'<g clip-path="url(#sangrado)">{body}</g>{_marcas(W, H, b, 5, info)}</svg>')


def _html(pages, pw, ph):
    css = pathlib.Path(BRAND_CSS).as_uri()
    svgs = ''.join(f'<div class="p">{s}</div>' for s in pages)
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{css}">'
            f'<style>@page{{size:{pw}mm {ph}mm;margin:0}}html,body{{margin:0;padding:0}}'
            f'.p{{width:{pw}mm;height:{ph}mm;overflow:hidden;page-break-after:always;break-after:page}}'
            f'.p:last-child{{page-break-after:auto;break-after:auto}}.p svg{{display:block;width:{pw}mm;height:{ph}mm}}</style>'
            f'</head><body>{svgs}</body></html>')


def pdf(pages, pw, ph, out, trim=None):
    """pages: lista de SVG (string) del mismo tamaño pw×ph mm. trim=(W,H,offset) fija TrimBox/BleedBox."""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf8') as t:
        t.write(_html(pages, pw, ph)); tmp = t.name
    try:
        _run(['--no-pdf-header-footer', f'--print-to-pdf={os.path.abspath(out)}', _url(tmp)])
    finally:
        os.unlink(tmp)
    if trim:
        import fitz
        W, H, off, boff = trim
        k = 72 / 25.4
        d = fitz.open(out)
        for p in d:
            mb = p.mediabox  # Chrome redondea el tamaño de página a píxeles: se recorta a la MediaBox
            bb = fitz.Rect(boff * k, boff * k, (off * 2 + W - boff) * k, (off * 2 + H - boff) * k) & mb
            tb = fitz.Rect(off * k, off * k, (off + W) * k, (off + H) * k) & bb
            p.set_bleedbox(bb)
            p.set_trimbox(tb)
        tmp2 = out + '.tmp.pdf'
        d.save(tmp2, garbage=3, deflate=True); d.close()
        os.replace(tmp2, out)


def png_preview(pdf_path, out_png, dpi=150, page=0):
    import fitz
    d = fitz.open(pdf_path)
    pix = d[page].get_pixmap(dpi=dpi)
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    pix.save(out_png)


def exportar(pieza, carpeta, W, H, caras, b=3, troquel=None, info='', preview_dpi=150):
    """
    caras: [(sufijo, body_svg)]  ·  genera:
      SVG_editable/<pieza>_<cara>.svg
      PDF_sin_marcas/<pieza>.pdf        (con sangrado; TrimBox/BleedBox definidos)
      PDF_imprenta_con_marcas/<pieza>.pdf  (sangrado + marcas de corte + información)
      Vista_previa_PNG/<pieza>_<cara>.png
      (troquel) SVG_editable/<pieza>_troquel.svg y PDF_imprenta_con_marcas/<pieza>_troquel.pdf
    """
    out = {}
    for suf, body in caras:
        fn = os.path.join(carpeta, 'SVG_editable', f'{pieza}_{suf}.svg' if suf else f'{pieza}.svg')
        os.makedirs(os.path.dirname(fn), exist_ok=True)
        open(fn, 'w', encoding='utf8').write(svg_cara(W, H, body, b, troquel=troquel, titulo=f'Oryzz · {pieza} {suf}'))
    sin = [svg_cara(W, H, body, b, guias=False) for _, body in caras]
    p_sin = os.path.join(carpeta, 'PDF_sin_marcas', f'{pieza}.pdf')
    pdf(sin, W + 2 * b, H + 2 * b, p_sin, trim=(W, H, b, 0))
    slug = 10
    con = [svg_con_marcas(W, H, body, b, slug, f'{info} · {W:g} × {H:g} mm · sangrado {b} mm · {suf or "cara única"}') for suf, body in caras]
    p_con = os.path.join(carpeta, 'PDF_imprenta_con_marcas', f'{pieza}.pdf')
    pdf(con, W + 2 * (b + slug), H + 2 * (b + slug), p_con, trim=(W, H, b + slug, slug))
    for i, (suf, _) in enumerate(caras):
        png_preview(p_sin, os.path.join(carpeta, 'Vista_previa_PNG', f'{pieza}_{suf}.png' if suf else f'{pieza}.png'), preview_dpi, i)
    if troquel:
        tsvg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-b - slug} {-b - slug} {W + 2 * (b + slug)} {H + 2 * (b + slug)}" '
                f'width="{W + 2 * (b + slug)}mm" height="{H + 2 * (b + slug)}mm"><g id="troquel" fill="none" stroke="#E6007E" stroke-width="0.25">{troquel}</g>'
                f'{_marcas(W, H, b, 5, f"{info} · troquel (línea de corte, no imprimir) · {W:g} × {H:g} mm")}</svg>')
        open(os.path.join(carpeta, 'SVG_editable', f'{pieza}_troquel.svg'), 'w', encoding='utf8').write(tsvg)
        pdf([tsvg], W + 2 * (b + slug), H + 2 * (b + slug), os.path.join(carpeta, 'PDF_imprenta_con_marcas', f'{pieza}_troquel.pdf'))
    return p_sin, p_con
