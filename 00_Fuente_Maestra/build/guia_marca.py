"""
Oryzz · Guía de marca v2.0 (PDF 16:9, 1920×1080 px por página)
=================================================================

Genera `01_Guia_de_Marca/Oryzz_Guia_de_Marca_v2.pdf` a partir de los archivos
ya producidos en el kit (logos, color, elementos gráficos, plantillas…).
No redibuja nada: incrusta los SVG maestros y las previsualizaciones reales.

    python guia_marca.py               # genera el PDF y las vistas previas
    python guia_marca.py --html        # solo el HTML (para revisar en el navegador)
    python guia_marca.py --png         # además, exporta cada página a PNG (revisión)

Requisitos: Python 3.9+, PyMuPDF (`pip install pymupdf`), Pillow, Chrome o Edge.
Si cambias algo en otra carpeta (logo, paleta, plantillas), vuelve a ejecutar
este script y la guía se actualiza sola.
"""
import argparse, html, json, os, pathlib, re, shutil, sys, tempfile

AQUI = pathlib.Path(__file__).resolve().parent
MAESTRA = AQUI.parent
RAIZ = MAESTRA.parent                       # Identidad_Visual
SALIDA = RAIZ / '01_Guia_de_Marca'
PDF = SALIDA / 'Oryzz_Guia_de_Marca_v2.pdf'
TMP = pathlib.Path(tempfile.gettempdir()) / 'oryzz_guia_marca'

sys.path.insert(0, str(AQUI))
from render import html_to_pdf, _run, _url  # noqa: E402
from orbitas import orbitas_group  # noqa: E402

TOK = json.loads((MAESTRA / 'tokens.json').read_text(encoding='utf8'))
C = TOK['color']
G = C['grafito']

VERSION = 'v2.0'
FECHA = 'Octubre 2026'

# ----------------------------------------------------------------- utilidades

def uri(rel):
    return (RAIZ / rel).resolve().as_uri()


def esc(s):
    return html.escape(s, quote=False)


def svg_inline(rel, style=''):
    s = (RAIZ / rel).read_text(encoding='utf8')
    s = re.sub(r'<\?xml[^>]*>', '', s)
    s = re.sub(r'<title>.*?</title>', '', s, flags=re.S)
    if style:
        s = s.replace('<svg ', f'<svg style="{style}" ', 1)
    return s


def prep(rel, max_w=1600, max_h=None, fmt='png', crop=None, name=None):
    """Copia una imagen al temporal, reducida al tamaño útil. crop=(w, h) recorta desde arriba a esa proporción."""
    from PIL import Image
    src = RAIZ / rel
    im = Image.open(src)
    if im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGBA')
    if crop:
        cw, ch = crop
        w, h = im.size
        th = round(w * ch / cw)
        if th < h:
            im = im.crop((0, 0, w, th))
        else:
            tw = round(h * cw / ch)
            x0 = (w - tw) // 2
            im = im.crop((x0, 0, x0 + tw, h))
    w, h = im.size
    k = min(1, max_w / w, (max_h / h) if max_h else 1)
    if k < 1:
        im = im.resize((round(w * k), round(h * k)), Image.LANCZOS)
    TMP.mkdir(parents=True, exist_ok=True)
    stem = name or re.sub(r'[^a-zA-Z0-9]+', '_', rel)[-80:]
    out = TMP / f'{stem}.{fmt}'
    if fmt == 'jpg':
        im.convert('RGB').save(out, quality=88, optimize=True)
    else:
        im.save(out, optimize=True)
    return out.as_uri()


def pdf_page(rel, page=0, width=900, name=None):
    """Renderiza una página de un PDF del kit a PNG (para miniaturas de documentos)."""
    import fitz
    doc = fitz.open(RAIZ / rel)
    p = doc[page]
    zoom = width / p.rect.width
    pix = p.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    TMP.mkdir(parents=True, exist_ok=True)
    out = TMP / f'{name or re.sub(r"[^a-zA-Z0-9]+", "_", rel)[-70:]}_p{page}.png'
    pix.save(out)
    return out.as_uri()


def lum(hexc):
    hexc = hexc.lstrip('#')
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def num(x, d=1):
    return f'{x:.{d}f}'.replace('.', ',')


def hex_rgb(h):
    h = h.lstrip('#')
    return ', '.join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


PALETA = {}
for row in (RAIZ / '03_Color' / 'paleta.csv').read_text(encoding='utf-8-sig').splitlines()[1:]:
    f = row.split(';')
    PALETA[f[3].upper()] = {'nombre': f[1], 'cmyk': f'{f[10]}/{f[11]}/{f[12]}/{f[13]}', 'pantone': f[15]}

# ----------------------------------------------------------------- iconos inline

def icono(nombre, size=48, color='currentColor', acento=None):
    s = svg_inline(f'05_Elementos_Graficos/01_Iconos/SVG/oz-icono_{nombre}.svg')
    st = f'width:{size}px;height:{size}px;color:{color};' + (f'--oz-acento:{acento};' if acento else '')
    s = re.sub(r'width="24" height="24"', '', s, count=1)
    return s.replace('<svg ', f'<svg style="{st}" class="ico" ', 1)


SI = '<svg class="mk" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
NO = '<svg class="mk" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/></svg>'

# ----------------------------------------------------------------- órbitas de fondo

def orbitas_fondo(cx, cy, radios, tema='oscuro', nodo=True, nodo_en=2, opacidad=1.0, w=1920, h=1080, nodo_ang=None):
    trazo = G['700'] if tema == 'oscuro' else G['200']
    color_nodo = (C['lima']['500'] if tema == 'oscuro' else C['lima']['600']) if nodo else None
    g = orbitas_group(cx, cy, radios, trazo=trazo, grosor=1.5, nodo=color_nodo, nodo_en=nodo_en,
                      nodo_r=9, opacidad=opacidad, nodo_ang=nodo_ang)
    return f'<svg class="bgsvg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">{g}</svg>'


# ----------------------------------------------------------------- páginas

PAGES = []          # (html, tema)
TOC = []            # (nivel, título, página)
CAP = {'n': '', 't': ''}


def pg(body, tema='oscuro', cls='', fondo='', pie=True, toc=None, nivel=2):
    n = len(PAGES) + 1
    if toc:
        TOC.append((nivel, toc, n))
    foot = ''
    if pie:
        iso = 'oryzz-isotipo_mono-blanco' if tema == 'oscuro' else 'oryzz-isotipo_mono-grafito'
        cap = CAP['t'] if CAP['t'] else 'Oryzz · Guía de marca'
        foot = (f'<footer><img class="fiso" src="{uri("02_Logos/04_Isotipo/SVG_tamano_pequeno/" + iso.replace("isotipo", "isotipo-small") + ".svg")}">'
                f'<span>Guía de marca {VERSION}</span><span class="fcap">{esc(cap)}</span><span class="fnum">{n}</span></footer>')
    PAGES.append(f'<section class="page {tema} {cls}">{fondo}<div class="in">{body}</div>{foot}</section>')
    return n


def head(eyebrow, titulo, lead=None, cls=''):
    l = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<header class="hd {cls}"><div class="eyebrow">{eyebrow}</div><h2 class="t">{titulo}</h2>{l}</header>'


def capitulo(n, titulo, intro, contenidos, tema='oscuro', fondo=None):
    CAP['n'], CAP['t'] = n, titulo
    items = ''.join(f'<li><span>{esc(c)}</span></li>' for c in contenidos)
    fondo = fondo if fondo is not None else orbitas_fondo(1560, 640, [180, 300, 430, 570, 720], tema, nodo_ang=-120)
    body = (f'<div class="cap-b"><h1 class="cap-t">{titulo}</h1>'
            f'<p class="lead">{intro}</p><ul class="cap-l">{items}</ul></div>')
    return pg(body, tema, 'opener', fondo, toc=titulo, nivel=1)


# ----------------------------------------------------------------- CSS

CSS = f"""
@page {{ size: 1920px 1080px; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: {G['950']}; }}
body {{ font-family: var(--font-texto); -webkit-font-smoothing: antialiased; text-rendering: geometricPrecision; font-kerning: normal; }}
.page {{ width: 1920px; height: 1080px; position: relative; overflow: hidden; page-break-after: always; break-after: page; }}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
.page.oscuro {{ --bg:{G['950']}; --bg2:{G['900']}; --sup:{G['850']}; --sup2:{G['800']}; --borde:{G['700']}; --tx:#FFFFFF; --tx2:{G['200']}; --tx3:{G['400']}; --az:{C['azul']['400']}; --nodo:{C['lima']['500']}; --grad:var(--grad-ia-oscuro); --cta-bg:var(--grad-ia-oscuro); --cta-tx:{G['950']}; background: var(--bg); color: var(--tx); }}
.page.claro {{ --bg:#FFFFFF; --bg2:{G['50']}; --sup:{G['50']}; --sup2:{G['100']}; --borde:{G['200']}; --tx:{G['950']}; --tx2:{G['600']}; --tx3:{G['500']}; --az:{C['azul']['500']}; --nodo:{C['lima']['600']}; --grad:var(--grad-ia-claro); --cta-bg:{C['azul']['600']}; --cta-tx:#FFFFFF; background: var(--bg); color: var(--tx); }}
.page.papel {{ --bg:{G['50']}; background: {G['50']}; }}
.bgsvg {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.bgimg {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.in {{ position: absolute; inset: 96px 120px 120px 120px; display: flex; flex-direction: column; }}
footer {{ position: absolute; left: 120px; right: 120px; bottom: 44px; display: flex; align-items: center; gap: 18px;
  font-family: var(--font-texto); font-weight: 500; font-size: 20px; color: var(--tx3); }}
footer .fiso {{ width: 22px; height: 22px; opacity: .8; }}
footer .fcap {{ margin-left: auto; }}
footer .fnum {{ min-width: 64px; text-align: right; color: var(--tx2); }}

.eyebrow {{ font-family: var(--font-texto); font-weight: 600; font-size: 24px; line-height: 1.3; color: var(--tx3); }}
.eyebrow b {{ color: var(--az); font-weight: 600; }}
.hd {{ max-width: 1240px; }}
.hd .t {{ font-family: var(--font-display); font-weight: 700; font-size: 66px; line-height: 1.04; letter-spacing: -.035em; margin-top: 22px; }}
.hd .lead {{ margin-top: 26px; max-width: 1080px; }}
.az {{ color: var(--az); }}
.lead {{ font-size: 30px; line-height: 1.45; color: var(--tx2); font-weight: 400; }}
p, li {{ font-size: 25px; line-height: 1.55; color: var(--tx2); }}
p + p {{ margin-top: 16px; }}
strong {{ color: var(--tx); font-weight: 700; }}
code, .mono {{ font-family: var(--font-mono); font-size: .86em; letter-spacing: 0; }}
h3 {{ font-family: var(--font-display); font-weight: 600; font-size: 34px; line-height: 1.15; letter-spacing: -.02em; color: var(--tx); }}
h4 {{ font-family: var(--font-display); font-weight: 600; font-size: 27px; line-height: 1.2; letter-spacing: -.01em; color: var(--tx); }}
.grow {{ flex: 1; min-height: 0; }}
.g {{ display: grid; grid-template-columns: repeat(12, 1fr); column-gap: 32px; row-gap: 32px; }}
.s2{{grid-column:span 2}} .s3{{grid-column:span 3}} .s4{{grid-column:span 4}} .s5{{grid-column:span 5}} .s6{{grid-column:span 6}} .s7{{grid-column:span 7}} .s8{{grid-column:span 8}} .s9{{grid-column:span 9}} .s12{{grid-column:span 12}}
.mt1{{margin-top:16px}} .mt2{{margin-top:32px}} .mt3{{margin-top:48px}} .mt4{{margin-top:64px}} .mta{{margin-top:auto}}
.card {{ background: var(--sup); border: 1px solid var(--borde); border-radius: 14px; padding: 32px 34px; }}
.rule {{ border-top: 1px solid var(--borde); padding-top: 22px; }}
.kick {{ font-family: var(--font-texto); font-weight: 600; font-size: 24px; line-height: 1.3; color: var(--az); margin-bottom: 12px; }}
.kick.g3 {{ color: var(--tx3); }}
.nodo {{ display: inline-block; width: 16px; height: 16px; border-radius: 50%; background: var(--nodo); vertical-align: middle; }}
.fig {{ border-radius: 14px; overflow: hidden; border: 1px solid var(--borde); background: var(--sup); }}
.fig img {{ display: block; width: 100%; height: 100%; object-fit: cover; }}
.fig.contain img {{ object-fit: contain; }}
.cap {{ font-family: var(--font-texto); font-weight: 500; font-size: 21px; color: var(--tx3); margin-top: 14px; }}
ul.l {{ list-style: none; }}
ul.l li {{ position: relative; padding-left: 30px; margin-top: 10px; }}
ul.l li::before {{ content: ''; position: absolute; left: 2px; top: 17px; width: 12px; height: 2px; background: var(--tx3); }}
ol.n {{ list-style: none; counter-reset: n; }}
ol.n li {{ position: relative; padding-left: 44px; margin-top: 16px; }}
ol.n li::before {{ content: ''; position: absolute; left: 4px; top: 13px; width: 12px; height: 12px; border: 2px solid var(--az); border-radius: 50%; }}
.mk {{ width: 28px; height: 28px; flex: none; }}
.yes, .nope {{ display: flex; gap: 16px; align-items: flex-start; padding: 16px 0; border-bottom: 1px solid var(--borde); font-size: 25px; line-height: 1.45; color: var(--tx2); }}
.yes .mk {{ color: var(--tx); margin-top: 3px; }}
.nope .mk {{ color: var(--tx3); margin-top: 3px; }}
.nope {{ color: var(--tx3); }}
table.t {{ width: 100%; border-collapse: collapse; }}
table.t th {{ text-align: left; font-family: var(--font-texto); font-weight: 600; font-size: 21px; color: var(--tx3); padding: 0 20px 14px 0; border-bottom: 1px solid var(--borde); }}
table.t td {{ font-size: 23px; line-height: 1.4; color: var(--tx2); padding: 15px 20px 15px 0; border-bottom: 1px solid var(--borde); vertical-align: top; }}
table.t td:first-child {{ color: var(--tx); font-weight: 600; }}
table.t td.m {{ font-family: var(--font-mono); font-size: 20px; }}
table.t.compact td {{ padding-top: 7px; padding-bottom: 7px; font-size: 20px; }}
.big {{ font-family: var(--font-display); font-weight: 700; letter-spacing: -.045em; line-height: .95; }}

/* portada y capítulos */
.cover .in {{ inset: 96px 120px 96px 120px; }}
.opener .in {{ flex-direction: row; align-items: stretch; }}
.cap-n {{ font-family: var(--font-display); font-weight: 500; font-size: 300px; line-height: .8; letter-spacing: -.06em; color: var(--tx); width: 520px; flex: none; }}
.cap-b {{ display: flex; flex-direction: column; justify-content: flex-end; max-width: 980px; padding-bottom: 8px; }}
.cap-t {{ font-family: var(--font-display); font-weight: 700; font-size: 112px; line-height: .98; letter-spacing: -.045em; margin: 22px 0 30px; }}
.cap-l {{ list-style: none; margin-top: 44px; display: grid; grid-template-columns: 1fr 1fr; column-gap: 40px; border-top: 1px solid var(--borde); }}
.cap-l li {{ font-family: var(--font-texto); font-weight: 500; font-size: 22px; color: var(--tx3); padding: 14px 0; border-bottom: 1px solid var(--borde); }}

/* swatches */
.sw {{ border-radius: 14px; padding: 26px 28px; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid var(--borde); }}
.sw .nm {{ font-family: var(--font-display); font-weight: 600; font-size: 30px; letter-spacing: -.02em; }}
.sw .dt {{ font-family: var(--font-mono); font-size: 17px; letter-spacing: .02em; line-height: 1.65; white-space: nowrap; }}
.chip {{ display: inline-flex; align-items: center; gap: 10px; height: 44px; padding: 0 20px; border-radius: 999px; border: 1px solid var(--borde); font-family: var(--font-texto); font-weight: 600; font-size: 20px; color: var(--tx2); }}
.btn {{ display: inline-flex; align-items: center; gap: 14px; height: 72px; padding: 0 36px; border-radius: 14px; font-weight: 700; font-size: 25px; }}
.tile {{ border-radius: 14px; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }}
.tile .lbl {{ position: absolute; left: 20px; bottom: 16px; font-family: var(--font-texto); font-weight: 600; font-size: 20px; }}
.ico {{ display: block; }}
"""

# ----------------------------------------------------------------- contenido

def portada():
    fondo = f'<img class="bgimg" src="{uri("05_Elementos_Graficos/03_Fondos/SVG/oryzz-fondo-01_orbita_oscuro_16x9.svg")}">'
    body = f"""
    <img src="{uri('02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg')}" style="height:74px;align-self:flex-start;margin-left:-8px">
    <div class="mta" style="max-width:1000px">
      <div class="eyebrow">Identidad visual {VERSION} · {FECHA}</div>
      <h1 class="big" style="font-size:168px;margin-top:28px">Guía de<br><span class="az">marca</span>.</h1>
      <p class="lead" style="margin-top:36px;max-width:780px">Todo lo necesario para que cualquier pieza de Oryzz y Oryzz Tap —un anuncio, un correo, una propuesta o una placa— parezca hecha por el mismo equipo.</p>
    </div>
    <div class="eyebrow" style="position:absolute;right:0;bottom:0;text-align:right">Uso interno y de proveedores<br>oryzz.com</div>
    """
    pg(body, 'oscuro', 'cover', fondo, pie=False, toc='Portada', nivel=1)


def como_usar():
    body = head('Antes de empezar', 'Cómo usar <span class="az">este manual</span>',
                'Este documento es la referencia visual y verbal de Oryzz. Si algo no aparece aquí, se decide a favor de: <strong>menos elementos, más aire, un solo acento.</strong>')
    body += f"""
    <div class="g mta">
      <div class="s4 rule"><div class="kick">Lee</div><h4>De la marca a la voz</h4><p class="mt1">La marca, el logo, el color, la tipografía, el sistema gráfico, la fotografía, el motion y la voz. Las reglas, con su porqué.</p></div>
      <div class="s4 rule"><div class="kick">Produce</div><h4>Aplicaciones y Oryzz Tap</h4><p class="mt1">Cómo se aplica en web, redes, email, presentaciones, documentos, papelería y Oryzz Tap. Cada pieza remite a su plantilla.</p></div>
      <div class="s4 rule"><div class="kick">Comprueba</div><h4>Checklists y archivos del kit</h4><p class="mt1">Checklist antes de publicar, plan de migración y el mapa de archivos del kit: dónde está cada cosa.</p></div>
    </div>
    <div class="card mt3" style="display:flex;gap:28px;align-items:center">
      {icono('documento', 44, 'var(--tx2)')}
      <p style="margin:0">Fuente de verdad: <code>00_Fuente_Maestra/BRAND_SPEC.md</code> y <code>tokens.json</code>. Si este PDF y esos archivos no coinciden, mandan ellos: regenera la guía con <code>python 00_Fuente_Maestra/build/guia_marca.py</code>.</p>
    </div>
    """
    pg(body, 'oscuro', toc='Cómo usar este manual')


INDICE = [
    ('01', 'La marca'), ('02', 'Órbita y nodo'), ('03', 'Logo'), ('04', 'Color'), ('05', 'Tipografía'),
    ('06', 'Sistema gráfico'), ('07', 'Fotografía'), ('08', 'Motion'), ('09', 'Voz y tono'),
    ('10', 'Aplicaciones'), ('11', 'Oryzz Tap'), ('12', 'Checklists'), ('13', 'Archivos del kit'),
]


def indice(paginas):
    filas = ''
    for n, t in INDICE:
        p = paginas.get(n, 0)
        filas += (f'<div style="display:flex;align-items:baseline;gap:28px;padding:11px 0;border-bottom:1px solid var(--borde)">'
                  f'<span style="font-family:var(--font-display);font-weight:600;font-size:32px;letter-spacing:-.02em">{t}</span>'
                  f'<span class="eyebrow" style="margin-left:auto">{p}</span></div>')
    body = f"""
    <div class="g grow">
      <div class="s4" style="display:flex;flex-direction:column">
        <div class="eyebrow">Índice</div>
        <h2 class="big" style="font-size:96px;margin-top:22px">Trece<br>capítulos.<br><span class="az">Un sistema.</span></h2>
        <p class="mta">El PDF tiene marcadores: ábrelos en el panel lateral de tu lector para saltar a cualquier capítulo.</p>
      </div>
      <div class="s2"></div>
      <div class="s6" style="border-top:1px solid var(--borde)">{filas}</div>
    </div>"""
    return body


def resumen_sistema():
    sw = ''
    for hexc, nm, tx in [(G['950'], 'Grafito 950', '#fff'), ('#FFFFFF', 'Blanco', G['950']), (C['azul']['500'], 'Azul IA', '#fff'),
                         (C['cyan']['500'], 'Cyan', G['950']), (C['lima']['500'], 'Lima', G['950'])]:
        sw += f'<div style="flex:1;background:{hexc};color:{tx};border-radius:12px;border:1px solid var(--borde);padding:16px;display:flex;flex-direction:column;justify-content:flex-end;height:130px"><div style="font-weight:700;font-size:22px">{nm}</div><div class="mono" style="font-size:17px;opacity:.85">{hexc}</div></div>'
    body = head('El sistema en una página', 'Si solo vas a leer <span class="az">una página</span>, que sea esta')
    body += f"""
    <div class="g mt3 grow" style="grid-template-rows:100%">
      <div class="s5 card" style="display:flex;flex-direction:column">
        <div class="kick g3">Logo</div>
        <div style="flex:1;display:flex;align-items:center"><img src="{uri('02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg')}" style="width:100%"></div>
        <p>Siempre el SVG maestro. Nunca texto vivo ni redibujos. «ory» sólido, «zz» en gradiente.</p>
      </div>
      <div class="s7" style="display:flex;flex-direction:column;gap:24px">
        <div class="card"><div class="kick g3">Color · 60 / 25 / 10 / ≤ 5</div><div style="display:flex;gap:12px;margin-top:8px">{sw}</div></div>
        <div class="card" style="display:flex;gap:40px;align-items:flex-end">
          <div><div class="kick g3">Tipografía</div><div style="font-family:var(--font-display);font-weight:700;font-size:54px;letter-spacing:-.04em;line-height:1">Space Grotesk</div></div>
          <div><div style="font-family:var(--font-texto);font-size:34px;color:var(--tx2)">Manrope</div></div>
          <div><div style="font-family:var(--font-mono);font-size:26px;color:var(--tx3)">JetBrains Mono</div></div>
        </div>
        <div class="card" style="flex:1;padding:26px 34px"><div class="kick g3">Cinco reglas de oro</div>
          <ol class="n" style="columns:2;column-gap:40px">
            <li style="margin-top:4px;break-inside:avoid;font-size:22px">Un solo acento lima por pieza.</li>
            <li style="margin-top:4px;break-inside:avoid;font-size:22px">Un fragmento en azul por titular.</li>
            <li style="margin-top:4px;break-inside:avoid;font-size:22px">Un único CTA por pieza.</li>
            <li style="margin-top:4px;break-inside:avoid;font-size:22px">Cifras reales o marcadas «Ejemplo».</li>
            <li style="margin-top:4px;break-inside:avoid;font-size:22px">Nada de violeta, neón, emojis ni robots.</li>
          </ol></div>
      </div>
    </div>"""
    pg(body, 'oscuro', toc='El sistema en una página')


# ---------------------------------------------------------------- 01 La marca

def cap_marca():
    capitulo('01', 'La marca', 'Qué es Oryzz, para quién trabaja y cómo se comporta. Todo lo visual sale de aquí.',
             ['Plataforma', 'Arquitectura', 'A quién servimos', 'Personalidad', 'Claims'])

    body = f"""
    <div class="eyebrow">Plataforma de marca</div>
    <h2 class="big" style="font-size:150px;margin-top:40px;max-width:1500px">Sistemas que<br>captan <span class="az">clientes</span>.</h2>
    <div class="g mta">
      <div class="s5"><p class="lead">Oryzz no hace acciones sueltas. Monta un sistema que gira solo —anuncios, respuesta inmediata, seguimiento— y se mide en clientes y en euros.</p></div>
      <div class="s1"></div>
      <div class="s3 rule"><div class="kick g3">Propósito</div><p>Que una PYME deje de depender de la suerte para llenar la agenda.</p></div>
      <div class="s3 rule"><div class="kick g3">Promesa</div><p>Más clientes. No más likes. Y si no encajamos, te lo decimos.</p></div>
    </div>"""
    pg(body, 'oscuro', fondo=orbitas_fondo(1700, 260, [140, 240, 350], 'oscuro', nodo_en=1), toc='Plataforma')

    srv = [('ads-meta', 'Meta Ads', 'Campañas en Instagram y Facebook orientadas a mensajes y citas.'),
           ('ads-google', 'Google Ads', 'Presencia cuando te buscan con intención, en búsqueda y en Maps.'),
           ('ads-tiktok', 'TikTok Ads', 'Vídeo corto con segmentación local para crear demanda nueva.'),
           ('automatizacion', 'Automatización con IA', 'Respuesta, cualificación y agenda en WhatsApp las 24 horas.'),
           ('seo-local', 'SEO local y reseñas', 'Ficha de Google optimizada y un flujo constante de reseñas.'),
           ('geo-ia', 'GEO', 'Que ChatGPT, Gemini y Perplexity te recomienden en tu sector.')]
    tiles = ''.join(f'<div class="s4 rule" style="display:flex;gap:22px">{icono(i, 40, "var(--tx2)")}<div><h4>{t}</h4><p style="margin-top:6px;font-size:22px">{d}</p></div></div>' for i, t, d in srv)
    body = head('Arquitectura', 'Una marca, <span class="az">dos líneas</span>')
    body += f"""
    <div class="g mt3">
      <div class="s7">
        <div style="display:flex;align-items:center;gap:24px"><img src="{uri('02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg')}" style="height:52px"><span class="chip">Agencia · España · EUR</span></div>
        <p class="mt2">Agencia de captación de clientes con IA para PYMES. 100 % remota. Socios: <strong>Juan Salazar</strong> (Estrategia y Ads) y <strong>David Morales</strong> (Automatización e IA).</p>
      </div>
      <div class="s5">
        <div style="display:flex;align-items:center;gap:24px"><img src="{uri('02_Logos/07_Submarca_Tap/SVG/oryzz-tap-horizontal_color-sobre-oscuro.svg')}" style="height:52px"><span class="chip">Producto · Colombia · COP</span></div>
        <p class="mt2">Placas y stands NFC + QR (Reseñas Google, Oryzz Pro). Checkout en <code>shop.oryzz.com</code>.</p>
      </div>
    </div>
    <div class="g mt3">{tiles}</div>"""
    pg(body, 'oscuro', toc='Arquitectura de marca')

    sect = [('Clínicas dentales y de fisioterapia', 'Agenda que depende del boca a boca; recepción saturada; leads que llegan por WhatsApp de noche.'),
            ('Centros estéticos', 'Mucha competencia local, precio visible, decisiones rápidas desde Instagram.'),
            ('Gimnasios y estudios', 'Picos de demanda (enero, septiembre) y bajas silenciosas el resto del año.'),
            ('Hostelería y comercio local', 'Reseñas de Google como escaparate; Oryzz Tap es su puerta de entrada.')]
    filas = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in sect)
    body = head('A quién servimos', 'Negocios con agenda, <span class="az">no con «audiencia»</span>',
                'Hablamos con dueños y gerentes de PYMES que miden su mes en citas, mesas y clientes nuevos. No son marketers: quieren saber qué entra y cuánto cuesta.')
    body += f"""<div class="g mt3"><div class="s8"><table class="t"><tr><th style="width:38%">Sector</th><th>Lo que les duele</th></tr>{filas}</table></div>
    <div class="s4"><div class="card" style="height:100%"><div class="kick">Lo que esperan de nosotros</div>
    <ul class="l"><li>Que les hablemos en euros y en citas.</li><li>Que les digamos que no si no encajan.</li><li>Ver datos sin pedirlos.</li><li>Un único interlocutor.</li></ul></div></div></div>"""
    pg(body, 'claro', toc='A quién servimos')

    es = ['Clara: una idea por frase.', 'Directa: el dato antes que el adjetivo.', 'Segura: sin promesas que no podemos medir.', 'Cercana: tuteo, sin jerga.', 'Técnica cuando hace falta, nunca para impresionar.']
    noes = ['Grandilocuente: «revoluciona», «siguiente nivel».', 'Agresiva: urgencias falsas, mayúsculas, «¡¡».', 'Mística con la IA: cerebros, robots, magia.', 'Corporativa: «soluciones 360», «sinergias».', 'Fría: tablas sin contexto ni conclusión.']
    body = head('Personalidad', 'Cómo es Oryzz <span class="az">y cómo no</span>')
    body += f"""<div class="g mt3">
      <div class="s6"><div class="kick">Es</div>{''.join(f'<div class="yes">{SI}<span>{x}</span></div>' for x in es)}</div>
      <div class="s6"><div class="kick g3">No es</div>{''.join(f'<div class="nope">{NO}<span>{x}</span></div>' for x in noes)}</div>
    </div>
    <p class="mta" style="max-width:1200px">Si Oryzz fuera una persona, sería la socia que te enseña el panel de resultados el lunes a las nueve, te dice qué ha funcionado, qué no y qué va a cambiar. Sin teatro.</p>"""
    pg(body, 'oscuro', toc='Personalidad')

    claims = [('Más clientes. No más likes.', 'Claim principal'),
              ('Un sistema de captación, no acciones sueltas.', 'Posicionamiento'),
              ('El problema no es que no te vean. Es que no te contactan.', 'Problema'),
              ('30 minutos. Sales con un diagnóstico, no con un presupuesto.', 'Oferta de entrada'),
              ('Te traemos clientes, no likes.', 'Variante corta'),
              ('Tu negocio. A un toque.', 'Oryzz Tap'),
              ('Conecta lo que eres. Acerca lo que sigue.', 'Oryzz Tap · manifiesto')]
    filas = ''.join(f'<div style="display:flex;align-items:baseline;gap:32px;padding:18px 0;border-bottom:1px solid var(--borde)"><span style="font-family:var(--font-display);font-weight:600;font-size:{40 if i == 0 else 32}px;letter-spacing:-.025em;color:var(--tx)">«{c}»</span><span class="eyebrow" style="margin-left:auto;white-space:nowrap">{d}</span></div>' for i, (c, d) in enumerate(claims))
    body = head('Claims', 'Frases <span class="az">reales</span> de la marca', 'Salen de la web y se usan tal cual. No se inventan claims nuevos para cada pieza: se combinan estos con datos concretos.')
    body += f'<div class="mt3" style="border-top:1px solid var(--borde)">{filas}</div>'
    pg(body, 'oscuro', toc='Claims')


# ---------------------------------------------------------------- 02 Concepto

def cap_concepto():
    capitulo('02', 'Órbita y nodo', 'La idea visual que une todo el sistema, y qué cambió entre la marca anterior y la v2.',
             ['El concepto', 'Del símbolo al sistema', 'Evolución v1 → v2', 'Qué cambió y por qué'])

    body = f"""
    <div class="g grow" style="align-items:center">
      <div class="s6" style="display:flex;justify-content:center"><img src="{uri('02_Logos/04_Isotipo/SVG/oryzz-isotipo_color-sobre-oscuro.svg')}" style="width:600px"></div>
      <div class="s6">
        <div class="eyebrow">Concepto visual</div>
        <h2 class="big" style="font-size:96px;margin-top:22px">Órbita<br>y <span class="az">nodo</span>.</h2>
        <div class="mt3 rule"><div class="kick">La órbita</div><p>La O de Oryzz es una órbita abierta: el sistema en marcha, la automatización, el ciclo que no se detiene.</p></div>
        <div class="mt2 rule"><div class="kick" style="display:flex;align-items:center;gap:12px"><span class="nodo"></span> El nodo</div><p>El punto lima es el resultado medible: el lead, la cita, el cliente. Siempre separado del trazo.</p></div>
      </div>
    </div>"""
    pg(body, 'oscuro', toc='El concepto')

    import math, random
    ln, nd = G['600'], C['lima']['500']
    W, H = 400, 330
    orb = f'<svg viewBox="0 0 {W} {H}">{orbitas_group(200, 175, [40, 75, 110, 145], trazo=ln, grosor=2, nodo=nd, nodo_en=2, nodo_r=7, nodo_ang=-40)}</svg>'
    rut = (f'<svg viewBox="0 0 {W} {H}" fill="none" stroke="{ln}" stroke-width="2" stroke-linecap="round">'
           '<path d="M40 70H150Q170 70 170 90V150Q170 165 185 165H280"/><path d="M40 165H280"/><path d="M40 260H150Q170 260 170 240V180Q170 165 185 165"/>'
           + ''.join(f'<circle cx="40" cy="{y}" r="6" fill="{G["400"]}" stroke="none"/>' for y in (70, 165, 260))
           + f'<circle cx="300" cy="165" r="9" fill="{nd}" stroke="none"/></svg>')
    ret = (f'<svg viewBox="0 0 {W} {H}"><defs><radialGradient id="rf" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
           f'<mask id="rm"><rect width="{W}" height="{H}" fill="url(#rf)"/></mask></defs><g mask="url(#rm)" stroke="{ln}" stroke-width="1">'
           + ''.join(f'<path d="M{x} 0V{H}"/>' for x in range(8, W, 32)) + ''.join(f'<path d="M0 {y}H{W}"/>' for y in range(5, H, 32))
           + '</g>' + ''.join(f'<path d="M{x - 6} {y}h12M{x} {y - 6}v12" stroke="{G["400"]}" stroke-width="1.5"/>' for x in (136, 264) for y in (101, 229)) + '</svg>')
    random.seed(7)
    pts = []
    while len(pts) < 150:
        x, y = random.uniform(10, W - 10), random.uniform(10, H - 10)
        if random.random() < math.exp(-math.hypot(x - 300, y - 110) / 120):
            pts.append((x, y))
    dat = (f'<svg viewBox="0 0 {W} {H}">' + ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{G["400"]}"/>' for x, y in pts)
           + f'<circle cx="300" cy="110" r="8" fill="{nd}"/></svg>')
    pat = [(orb, 'Órbitas', 'Arcos abiertos concéntricos. Fondo y portada.'),
           (rut, 'Rutas y nodos', 'Líneas ortogonales que conectan canal → sistema → cliente.'),
           (ret, 'Retícula técnica', 'Cuadrícula de 64 px al 3,5 %. Solo textura.'),
           (dat, 'Datos', 'Campo de nodos: la densidad que cae desde un foco.')]
    tiles = ''.join(f'<div class="s3"><div class="fig" style="height:330px;display:flex">{f.replace("<svg ", "<svg style=\"width:100%;height:100%\" ", 1)}</div><h4 class="mt2">{t}</h4><p class="mt1" style="font-size:22px">{d}</p></div>' for f, t, d in pat)
    body = head('Del símbolo al sistema', 'Todo sale de <span class="az">la O</span>',
                'Las órbitas, las rutas, la retícula y los datos son piezas del mismo mecanismo. Por eso una slide, un post y una tarjeta de visita se reconocen sin necesidad de logo.')
    body += f'<div class="g mt4">{tiles}</div>'
    pg(body, 'oscuro', toc='Del símbolo al sistema')

    ev = '12_Auditoria_y_Mejoras/evidencias/'
    body = head('Evolución', 'De tres marcas a <span class="az">una</span>')
    body += f"""
    <div class="g mt3 grow">
      <div class="s6" style="display:flex;flex-direction:column">
        <div class="kick g3">Antes · v1 (hasta septiembre de 2026)</div>
        <div class="g" style="row-gap:20px;column-gap:20px">
          <div class="s6"><div class="fig" style="height:270px"><img src="{prep(ev + 'ev15_tap_hero.png', 900, fmt='jpg')}" style="object-position:left top"></div><div class="cap">/tap · Syne + Outfit, azul #0075FF</div></div>
          <div class="s6"><div class="fig" style="height:270px"><img src="{prep(ev + 'ev03_home_hero.png', 900, fmt='jpg')}"></div><div class="cap">oryzz.com · logo en texto vivo</div></div>
          <div class="s6"><div class="fig" style="height:230px;background:#fff"><img src="{prep(ev + 'ev09_tap_producto_logo_antiguo.png', 900, fmt='jpg')}" style="object-fit:contain"></div><div class="cap">Placas con estrellas</div></div>
          <div class="s6"><div class="fig" style="height:230px;background:#fff;display:flex;align-items:center;justify-content:center"><img src="{prep(ev + 'ev21_logo_tap_antiguo.png', 900)}" style="object-fit:contain;width:86%;height:auto"></div><div class="cap">Logo Tap antiguo</div></div>
        </div>
      </div>
      <div class="s6" style="display:flex;flex-direction:column">
        <div class="kick">Ahora · v2</div>
        <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:72px;padding:56px;border:1px solid var(--borde);border-radius:14px;background:var(--sup)">
          <img src="{uri('02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg')}" style="width:74%">
          <img src="{uri('02_Logos/07_Submarca_Tap/SVG/oryzz-tap-horizontal_color-sobre-oscuro.svg')}" style="width:74%">
        </div>
        <div class="cap">Un solo logo maestro, una submarca, un sistema</div>
      </div>
    </div>"""
    pg(body, 'oscuro', toc='Evolución v1 → v2')

    cambios = [('Nodo separado del trazo', 'Antes el nodo tocaba la órbita y se empastaba en una tinta, en bordado y a tamaño favicon. Ahora un corte lo separa.'),
               ('Wordmark vectorizado', 'La web escribía el logo con texto vivo: dependía de que cargara la fuente. Ahora es un SVG con kerning óptico.'),
               ('Un sistema, no tres', 'Web, tienda y documentos usaban 7 familias tipográficas, 4 azules y 2 limas. Ahora: 3 familias y una paleta.'),
               ('Botón legible', 'El CTA principal tenía texto blanco sobre cyan: 1,88:1. Ahora texto Grafito 950 sobre el gradiente: de 6,1 a 10,3:1.'),
               ('Sin estrellas en Tap', 'Las cinco estrellas ataban la marca a «reseñas». Tap usa ahora el mismo isotipo que Oryzz.'),
               ('JetBrains Mono para datos', 'Una tercera voz tipográfica que da el tono «sistema» sin recurrir a iconos de IA.')]
    filas = ''.join(f'<tr><td style="width:30%">{a}</td><td>{b}</td></tr>' for a, b in cambios)
    body = head('Qué cambió y por qué', 'Seis decisiones <span class="az">de la v2</span>')
    body += f'<table class="t mt3">{filas}</table><p class="mt2" style="font-size:21px;color:var(--tx3)">Detalle completo, con evidencias y cifras, en <code>12_Auditoria_y_Mejoras/Oryzz_Auditoria_de_Marca.pdf</code>.</p>'
    pg(body, 'claro', toc='Qué cambió y por qué')


# ---------------------------------------------------------------- 03 Logo

def cap_logo():
    L = '02_Logos/'
    capitulo('03', 'Logo', 'Versiones, construcción, espacios, tamaños y usos. El logo nunca se redibuja: siempre los SVG maestros.',
             ['Logo principal', 'Anatomía', 'Construcción', 'Área de respeto', 'Tamaños mínimos', 'Versiones', 'Colorways', 'Sobre fondos y fotos',
              'Favicon y avatares', 'Logo animado', 'Usos incorrectos', 'El nombre', 'Co-branding'])

    body = f"""
    <div class="eyebrow">Logo principal · horizontal · color sobre oscuro</div>
    <div class="grow" style="display:flex;align-items:center;justify-content:center"><img src="{uri(L + '01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg')}" style="width:1200px"></div>
    <div class="g"><div class="s4 rule"><div class="kick g3">Archivo</div><p><code>02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg</code></p></div>
    <div class="s4 rule"><div class="kick g3">Cuándo</div><p>Por defecto, en cualquier pieza oscura: web, slides, redes, firmas.</p></div>
    <div class="s4 rule"><div class="kick g3">Nunca</div><p>Escrito con texto vivo, redibujado o exportado desde una captura.</p></div></div>"""
    pg(body, 'oscuro', toc='Logo principal')

    body = head('Anatomía', 'Dos piezas, <span class="az">una firma</span>')
    body += f"""
    <div class="grow" style="position:relative;margin-top:40px">
      <img src="{uri(L + '01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-claro.svg')}" style="position:absolute;left:120px;top:60px;width:1440px">
      <div style="position:absolute;left:150px;top:450px;width:360px" class="rule"><div class="kick">Isotipo</div><p style="font-size:22px">Órbita abierta de 283,4° (≈ 302° visibles con las puntas redondas), hueco superior de 76,6°, trazo = 11 % de la caja, más el nodo.</p></div>
      <div style="position:absolute;left:600px;top:450px;width:420px" class="rule"><div class="kick">«ory» sólido</div><p style="font-size:22px">Space Grotesk Bold vectorizada, tracking −0,038 em con kerning óptico. Grafito 950 en claro, blanco en oscuro.</p></div>
      <div style="position:absolute;left:1140px;top:450px;width:420px" class="rule"><div class="kick">«zz» en gradiente</div><p style="font-size:22px">La firma de la marca: gradiente IA a 135°. Nunca se reordena ni se cambia de color fuera de los colorways.</p></div>
    </div>"""
    pg(body, 'claro', toc='Anatomía')

    for f, t, sub, lead in [
        ('oryzz-01_construccion-isotipo', 'Construcción del isotipo', 'Construcción', 'Arco de 283,4° sobre la línea central del trazo, puntas redondas y un nodo separado por un corte de 2,5 unidades. El corte crece en el isotipo pequeño y el favicon para que no se cierre.'),
        ('oryzz-02_area-de-respeto', 'Área de respeto', 'Área de respeto', 'En los cuatro lados, como mínimo x = la altura de la «z» del wordmark (≈ 60 % del diámetro del isotipo en el horizontal). En el isotipo solo: 25 % de su ancho.'),
        ('oryzz-03_tamanos-minimos', 'Tamaños mínimos', 'Tamaños mínimos', 'Horizontal: 88 px / 22 mm. Isotipo: 16 px / 5 mm (por debajo de 24 px, el isotipo pequeño). Por debajo de 120 px de ancho, la versión sólida: el gradiente se ensucia.')]:
        body = f"""
        <div class="g grow">
          <div class="s3" style="display:flex;flex-direction:column"><div class="eyebrow">{sub}</div><h2 class="t" style="font-family:var(--font-display);font-weight:700;font-size:56px;line-height:1.05;letter-spacing:-.035em;margin-top:22px">{t}</h2><p class="mt3" style="font-size:23px">{lead}</p></div>
          <div class="s9"><div class="fig contain" style="height:864px;border:none;background:transparent"><img src="{uri(L + '09_Construccion_y_Uso/SVG/' + f + '_oscuro.svg')}"></div></div>
        </div>"""
        pg(body, 'oscuro', toc=t)

    vers = [('01_Horizontal/SVG/oryzz-logo-horizontal', 'Horizontal', 'Principal. Cabeceras, firmas, slides.', 'width:86%'),
            ('02_Logos_v', 'Vertical', 'Formatos cuadrados o verticales, portadas centradas.', ''),
            ('03_Wordmark/SVG/oryzz-wordmark', 'Wordmark', 'Cuando el isotipo ya aparece en la pieza.', 'width:70%'),
            ('04_Isotipo/SVG/oryzz-isotipo', 'Isotipo', 'Avatares, favicons, sellos, motion.', 'height:62%'),
            ('04_Isotipo/SVG_tamano_pequeno/oryzz-isotipo-small', 'Isotipo pequeño', 'Trazo reforzado al 14 %. Para ≤ 24 px.', 'height:40%'),
            ('07_Submarca_Tap/SVG/oryzz-tap-horizontal', 'Submarca Tap', '«oryzz tap»: producto físico.', 'width:86%')]
    tiles = ''
    for f, t, d, st in vers:
        src = uri(L + '02_Vertical/SVG/oryzz-logo-vertical_color-sobre-claro.svg') if f == '02_Logos_v' else uri(L + f + '_color-sobre-claro.svg')
        st = st or 'height:74%'
        tiles += f'<div class="s4"><div class="tile" style="height:250px;background:var(--sup);border:1px solid var(--borde)"><img src="{src}" style="{st}"></div><h4 class="mt1" style="margin-top:18px">{t}</h4><p style="font-size:21px">{d}</p></div>'
    body = head('Versiones', 'Seis versiones, <span class="az">un mismo dibujo</span>')
    body += f'<div class="g mt3" style="row-gap:28px">{tiles}</div>'
    pg(body, 'claro', toc='Versiones')

    cw = [('color-sobre-oscuro', G['950'], G['400'], 'Principal'), ('color-sobre-claro', '#FFFFFF', G['500'], 'Fondos claros'),
          ('solido-sobre-oscuro', G['900'], G['400'], '< 120 px, bordado, vinilo'), ('solido-sobre-claro', G['50'], G['500'], 'Impresión barata, email'),
          ('sobre-azul', C['azul']['500'], '#FFFFFF', 'Piezas sobre azul'), ('sobre-lima', C['lima']['500'], G['950'], 'Solo campaña puntual'),
          ('mono-blanco', G['800'], G['400'], 'Sobre foto con velo'), ('mono-grafito', G['100'], G['500'], 'Una tinta en claro'),
          ('mono-negro', '#FFFFFF', G['500'], 'Fax, sellos, grabado'), ('mono-azul', '#FFFFFF', G['500'], 'Una tinta azul')]
    tiles = ''.join(f'<div style="grid-column:span 12;"></div>' if False else
                    f'<div class="tile" style="height:196px;background:{bg};border:1px solid var(--borde)"><img src="{uri(L + "01_Horizontal/SVG/oryzz-logo-horizontal_" + n + ".svg")}" style="width:70%;margin-top:-22px"><div class="lbl" style="color:{lc}">{n} · {u}</div></div>'
                    for n, bg, lc, u in cw)
    body = head('Colorways', 'Diez colorways. <span class="az">Ni uno más.</span>', 'El nombre indica el fondo para el que está hecho: <code>mono-blanco</code> va sobre oscuro. Cualquier otra combinación de colores está prohibida.')
    body += f'<div class="mt3" style="display:grid;grid-template-columns:repeat(5,1fr);gap:20px">{tiles}</div>'
    pg(body, 'oscuro', toc='Colorways')

    body = head('Sobre fondos y fotos', 'El logo necesita <span class="az">contraste y calma</span>')
    body += f"""
    <div class="g mt3 grow">
      <div class="s7"><div class="fig" style="aspect-ratio:16/9"><img src="{prep('05_Elementos_Graficos/06_Fotografia/PNG/tratamiento-01_clinica_16x9.png', 1400, fmt='jpg')}"></div><div class="cap">Ejemplo de tratamiento · 06_Fotografia</div></div>
      <div class="s5">
        <table class="t"><tr><th>Fondo</th><th>Versión</th></tr>
        <tr><td>Grafito 950 / 900</td><td><code>color-sobre-oscuro</code></td></tr>
        <tr><td>Blanco / Grafito 50</td><td><code>color-sobre-claro</code></td></tr>
        <tr><td>Foto con velo 55–70 %</td><td><code>color-sobre-oscuro</code> o <code>mono-blanco</code></td></tr>
        <tr><td>Foto sin velo</td><td><code>mono-blanco</code>, nunca el gradiente</td></tr>
        <tr><td>Azul IA</td><td><code>sobre-azul</code></td></tr>
        <tr><td>Lima (campaña)</td><td><code>sobre-lima</code></td></tr>
        </table>
        <p class="mt2">Sobre fondos de marca (<code>03_Fondos</code>) el logo va dentro de la zona de texto de <code>fondos.json</code>, nunca encima de la órbita ni del nodo.</p>
      </div>
    </div>"""
    pg(body, 'oscuro', toc='Sobre fondos y fotos')

    av = L + '05_Avatar_Perfil/SVG/'
    favs = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:14px"><img src="{uri(L + "06_Favicon/favicon.svg")}" style="width:{s}px;height:{s}px"><span class="cap" style="margin:0">{s} px</span></div>' for s in (16, 24, 32, 48, 96))
    body = head('Favicon y avatares', 'El isotipo <span class="az">a tamaño sello</span>')
    body += f"""
    <div class="g mt3 grow">
      <div class="s5 card" style="display:flex;flex-direction:column">
        <div class="kick g3">Favicon</div>
        <div style="flex:1;display:flex;align-items:center;justify-content:space-between;padding:20px 10px">{favs}</div>
        <p style="font-size:21px">Pack completo en <code>06_Favicon/</code> (SVG, ICO, 16/32, Apple 180, Android 192/512, maskable) con el <code>snippet-head.html</code> listo para pegar.</p>
      </div>
      <div class="s7" style="display:flex;flex-direction:column">
        <div style="display:flex;gap:28px;align-items:flex-end">
          <div><img src="{uri(av + 'oryzz-avatar-circulo_color-sobre-oscuro.svg')}" style="width:220px;display:block"><div class="cap">Redes · círculo</div></div>
          <div><img src="{uri(av + 'oryzz-avatar-cuadrado_color-sobre-oscuro.svg')}" style="width:220px;display:block"><div class="cap">App · cuadrado</div></div>
          <div><img src="{uri(av + 'oryzz-avatar-cuadrado_sobre-azul.svg')}" style="width:160px;display:block"><div class="cap">Sobre azul</div></div>
          <div><img src="{uri(L + '05_Avatar_Perfil/SVG_redes/oryzz-tap-avatar-redes_color-sobre-claro.svg')}" style="width:160px;display:block;border-radius:50%;border:1px solid var(--borde)"><div class="cap">Oryzz Tap</div></div>
        </div>
        <p class="mt3">Perfiles de Oryzz (@oryzzai, LinkedIn, WhatsApp, TikTok): <code>oryzz-avatar-redes_color-sobre-oscuro_1080.png</code>. Perfiles de Tap (@oryzztap, @oryzz.tap): la versión clara de Tap.</p>
        <p>El avatar no lleva texto, ni marco, ni el wordmark: solo el isotipo con su nodo.</p>
      </div>
    </div>"""
    pg(body, 'oscuro', toc='Favicon y avatares')

    # Logo animado: fotogramas clave del SVG oficial pausados en el tiempo
    intro = (RAIZ / L / '08_Animado/oryzz-logo-intro.svg').read_text(encoding='utf8')
    intro = re.sub(r'<title>.*?</title>', '', intro, flags=re.S)
    frames = ''
    for i, t in enumerate([0.15, 0.55, 0.95, 1.35, 1.75, 3.0]):
        frames += (f'<div class="s4"><div class="fig anim" data-t="{t}" style="height:200px;display:flex;align-items:center;justify-content:center;padding:0 40px">'
                   f'{intro.replace("<svg ", "<svg style=\"width:100%;height:auto\" ", 1)}</div><div class="cap">{num(t, 2)} s</div></div>')
    body = head('Logo animado', 'La órbita gira, <span class="az">las «zz» saltan</span>')
    body += f"""<div class="g mt3" style="row-gap:20px">{frames}</div>
    <div class="g mta"><div class="s4 rule"><div class="kick g3">Intro · 3 s</div><p style="font-size:22px">La órbita entra girando, «ory» se desliza, las «zz» caen con resorte (desfase 0,17 s) y el nodo respira.</p></div>
    <div class="s4 rule"><div class="kick g3">Loader</div><p style="font-size:22px">Órbita en giro continuo, 4,4 s lineal. Solo mientras algo carga.</p></div>
    <div class="s4 rule"><div class="kick g3">Archivos</div><p style="font-size:22px"><code>08_Animado/</code>: SVG animado, HTML, GIF 800×300 y póster.</p></div></div>"""
    pg(body, 'oscuro', toc='Logo animado')

    body = f"""
    <div class="g grow">
      <div class="s3" style="display:flex;flex-direction:column"><div class="eyebrow">Usos incorrectos</div><h2 style="font-family:var(--font-display);font-weight:700;font-size:56px;line-height:1.05;letter-spacing:-.035em;margin-top:22px">Lo que <span class="az">nunca</span> se hace</h2>
      <ul class="l mt3" style="font-size:23px"><li>Estirar, rotar o inclinar.</li><li>Recolorear fuera de los diez colorways.</li><li>Sombras, contornos, brillos o biseles.</li><li>Gradiente sobre foto sin velo.</li><li>Reordenar «ory» y «zz» o mover el nodo.</li><li>Recuperar las estrellas del logo antiguo de Tap.</li><li>Escribir «OryzzTAP» u «ORYZZ».</li></ul></div>
      <div class="s9"><div class="fig contain" style="height:864px;border:none;background:transparent"><img src="{uri(L + '09_Construccion_y_Uso/SVG/oryzz-04_usos-incorrectos_oscuro.svg')}"></div></div>
    </div>"""
    pg(body, 'oscuro', toc='Usos incorrectos')

    bien = [('Oryzz', 'En texto corrido, con O mayúscula.'), ('Oryzz Tap', 'Dos palabras, T mayúscula.'), ('oryzz', 'Solo dentro del logo (siempre SVG).'), ('@oryzzai · @oryzztap', 'Usuarios de redes, tal cual.')]
    mal = [('ORYZZ', 'Mayúsculas enteras'), ('OryzzTAP / OryzzTap', 'Pegado o en mayúsculas'), ('oryzz', 'En minúscula en una frase'), ('Oryz, Orizz, Oryzz.ai', 'Variantes'), ('MyOryzz', 'Hasta que se defina como producto')]
    body = head('El nombre', 'Cómo se escribe <span class="az">Oryzz</span>', 'Los buscadores y los asistentes de IA consolidan mejor una entidad con un nombre estable. Para una agencia que vende GEO, esto no es un detalle.')
    body += f"""<div class="g mt3">
      <div class="s6"><div class="kick">Así</div>{''.join(f'<div class="yes">{SI}<span><strong style="font-family:var(--font-display);font-size:30px">{a}</strong> &nbsp;{b}</span></div>' for a, b in bien)}</div>
      <div class="s6"><div class="kick g3">Así no</div>{''.join(f'<div class="nope">{NO}<span><span style="font-family:var(--font-display);font-size:30px;text-decoration:line-through">{a}</span> &nbsp;{b}</span></div>' for a, b in mal)}</div>
    </div>"""
    pg(body, 'claro', toc='El nombre')

    cliente = ('<div style="display:flex;align-items:center;gap:16px"><svg width="64" height="64" viewBox="0 0 64 64"><rect x="2" y="2" width="60" height="60" rx="14" fill="none" stroke="var(--tx3)" stroke-width="2" stroke-dasharray="6 6"/></svg>'
               '<span style="font-family:var(--font-texto);font-weight:700;font-size:34px;color:var(--tx2)">Logo del cliente</span></div>')
    body = head('Co-branding', 'Junto a otra marca, <span class="az">el mismo peso</span>', 'En propuestas, casos de estudio y piezas para clientes. El logo del cliente y el de Oryzz se separan con un filete y nunca se fusionan.')
    body += f"""
    <div class="g mt3 grow">
      <div class="s7 card" style="display:flex;flex-direction:column;justify-content:center;gap:56px">
        <div style="display:flex;align-items:center;gap:48px;justify-content:center">
          <img src="{uri(L + '01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-claro.svg')}" style="height:64px">
          <span style="width:2px;height:90px;background:var(--borde)"></span>{cliente}
        </div>
        <div style="display:flex;align-items:center;gap:20px;justify-content:center">
          <span class="eyebrow">Preparado para</span><span style="font-family:var(--font-display);font-weight:600;font-size:30px">Clínica Dental Arenal</span><span class="eyebrow">· por</span>
          <img src="{uri(L + '03_Wordmark/SVG/oryzz-wordmark_solido-sobre-claro.svg')}" style="height:30px">
        </div>
      </div>
      <div class="s5"><ol class="n">
        <li style="margin-top:0">Misma altura óptica: el logo del cliente no supera la altura del isotipo de Oryzz.</li>
        <li>Separación: filete de 1–2 px en Grafito 200 (claro) o 700 (oscuro), con el área de respeto a cada lado.</li>
        <li>Orden: Oryzz primero cuando el documento es nuestro (propuestas, informes); el cliente primero cuando la pieza es suya (anuncios, reseñas).</li>
        <li>El logo del cliente se usa en sus colores oficiales; si choca con el fondo, en su versión monocroma.</li>
        <li>Nunca se mete el logo del cliente dentro de la órbita ni se le añade el nodo.</li>
      </ol></div>
    </div>"""
    pg(body, 'claro', toc='Co-branding')


# ---------------------------------------------------------------- 04 Color

def sw_card(hexc, extra='', h=260, big=False):
    p = PALETA.get(hexc.upper(), {})
    tx = '#FFFFFF' if contraste(hexc, '#FFFFFF') >= contraste(hexc, G['950']) else G['950']
    nm = p.get('nombre', hexc)
    return (f'<div class="sw" style="background:{hexc};color:{tx};height:{h}px;{extra}"><div class="nm" style="{"font-size:38px" if big else ""}">{nm}</div>'
            f'<div class="dt">{hexc}<br>RGB {hex_rgb(hexc)}<br>CMYK {p.get("cmyk", "—")}<br>Pantone {p.get("pantone", "—")}</div></div>')


def cap_color():
    capitulo('04', 'Color', 'Una paleta corta y disciplinada: mucho grafito, un azul de marca y un único acento lima.',
             ['Paleta principal', 'Proporción', 'Escalas', 'Gradiente IA', 'El acento lima', 'Contraste', 'Botones', 'Oscuro y claro', 'Impresión'], tema='claro')

    body = head('Paleta principal', 'Cinco colores <span class="az">hacen la marca</span>')
    body += f"""<div class="mt3 grow" style="display:grid;grid-template-columns:1.9fr 1.35fr 1.25fr 1.05fr 1.05fr;gap:16px">
    {sw_card(G['950'], h=560, big=True)}{sw_card('#FFFFFF', h=560, big=True)}{sw_card(C['azul']['500'], h=560, big=True)}{sw_card(C['cyan']['500'], h=560)}{sw_card(C['lima']['500'], h=560)}</div>
    <p class="mt2" style="font-size:20px;color:var(--tx3)">CMYK aproximado: pide prueba de color a la imprenta. Pantone: referencia a validar con guía física. Valores completos en <code>03_Color/paleta.csv</code> y <code>.ase</code>.</p>"""
    pg(body, 'claro', toc='Paleta principal')

    body = head('Proporción', '60 · 25 · 10 · <span class="az">≤ 5</span>', 'La marca es oscura y tranquila. El color de marca aparece poco y el lima casi nunca: por eso, cuando aparece, se ve.')
    body += f"""
    <div class="mt4" style="display:flex;height:300px;border-radius:14px;overflow:hidden;border:1px solid var(--borde)">
      <div style="flex:60;background:{G['950']};padding:28px;display:flex;flex-direction:column;justify-content:flex-end"><div class="big" style="font-size:80px">60 %</div><div class="eyebrow">Grafito</div></div>
      <div style="flex:25;background:{G['50']};color:{G['950']};padding:28px;display:flex;flex-direction:column;justify-content:flex-end"><div class="big" style="font-size:64px">25 %</div><div class="eyebrow" style="color:{G['500']}">Blanco / Grafito 50</div></div>
      <div style="flex:10;background:linear-gradient(135deg,{C['azul']['400']},{C['cyan']['500']});color:{G['950']};padding:22px 18px;display:flex;flex-direction:column;justify-content:flex-end"><div class="big" style="font-size:44px">10 %</div><div class="eyebrow" style="color:{G['950']};font-size:15px">Azul / Cyan</div></div>
      <div style="flex:5;background:{C['lima']['500']};color:{G['950']};padding:22px 10px;display:flex;flex-direction:column;justify-content:flex-end"><div class="big" style="font-size:32px">5</div></div>
    </div>
    <div class="g mt4">
      <div class="s4 rule"><div class="kick g3">Grafito</div><p>Fondos, superficies, texto. Es la marca en reposo.</p></div>
      <div class="s4 rule"><div class="kick g3">Azul IA y gradiente</div><p>Color de marca: logo, un fragmento del titular, gráficos, botones. No cuenta como acento.</p></div>
      <div class="s4 rule"><div class="kick g3" style="display:flex;gap:12px;align-items:center"><span class="nodo"></span>Lima</div><p>El acento. Un dato, una acción, un punto. Como máximo un elemento por pieza.</p></div>
    </div>"""
    pg(body, 'oscuro', toc='Proporción 60/25/10/5')

    esc_g = ''.join(f'<div style="flex:1;background:{v};height:200px;border-radius:10px;border:1px solid var(--borde);padding:14px;display:flex;flex-direction:column;justify-content:flex-end;color:{"#fff" if contraste(v, "#FFFFFF") > 4 else G["950"]}"><div style="font-weight:700;font-size:20px">{k}</div><div class="mono" style="font-size:15px;opacity:.85">{v}</div></div>'
                    for k, v in G.items())
    def fila(grupo, nombre):
        return ''.join(f'<div style="flex:1;background:{v};height:150px;border-radius:10px;border:1px solid var(--borde);padding:14px;display:flex;flex-direction:column;justify-content:flex-end;color:{"#fff" if contraste(v, "#FFFFFF") > 3.6 else G["950"]}"><div style="font-weight:700;font-size:20px">{nombre} {k}</div><div class="mono" style="font-size:15px;opacity:.85">{v}</div></div>' for k, v in C[grupo].items())
    est = ''.join(f'<div style="flex:1;background:{v};height:150px;border-radius:10px;padding:14px;display:flex;flex-direction:column;justify-content:flex-end;color:{"#fff" if k != "aviso" else G["950"]}"><div style="font-weight:700;font-size:20px">{k.capitalize()}</div><div class="mono" style="font-size:15px;opacity:.85">{v}</div></div>' for k, v in C['estado'].items())
    body = head('Escalas', 'La paleta <span class="az">completa</span>')
    body += f"""<div class="mt3"><div class="kick g3">Grafito · 13 pasos (400 = «Titanio»)</div><div style="display:flex;gap:8px">{esc_g}</div></div>
    <div style="display:flex;gap:32px" class="mt2">
      <div style="flex:7"><div class="kick g3">Azul</div><div style="display:flex;gap:8px">{fila('azul', 'Azul')}</div></div>
      <div style="flex:4"><div class="kick g3">Cyan</div><div style="display:flex;gap:8px">{fila('cyan', 'Cyan')}</div></div>
    </div>
    <div style="display:flex;gap:32px" class="mt2">
      <div style="flex:5"><div class="kick g3">Lima</div><div style="display:flex;gap:8px">{fila('lima', 'Lima')}</div></div>
      <div style="flex:3"><div class="kick g3">Estado</div><div style="display:flex;gap:8px">{est}</div></div>
      <div style="flex:3"></div>
    </div>"""
    pg(body, 'claro', toc='Escalas de color')

    body = head('Gradiente IA', 'Dos colores, <span class="az">135°</span>, poco y bien')
    body += f"""
    <div class="g mt3 grow">
      <div class="s6" style="display:flex;flex-direction:column;gap:20px">
        <div style="flex:1;border-radius:14px;background:linear-gradient(135deg,#5C8BFF,#36CFE0);padding:28px;display:flex;flex-direction:column;justify-content:flex-end;color:{G['950']}"><div style="font-weight:700;font-size:30px">Sobre oscuro</div><div class="mono" style="font-size:19px">135° · #5C8BFF → #36CFE0</div></div>
        <div style="flex:1;border-radius:14px;background:linear-gradient(135deg,#3B72FF,#17A9C2);padding:28px;display:flex;flex-direction:column;justify-content:flex-end;color:#fff"><div style="font-weight:700;font-size:30px">Sobre claro</div><div class="mono" style="font-size:19px">135° · #3B72FF → #17A9C2</div></div>
      </div>
      <div class="s6">
        <div class="kick">Sí</div>
        <div class="yes">{SI}<span>En el logo (las «zz»).</span></div>
        <div class="yes">{SI}<span>Botón principal sobre oscuro, con texto Grafito 950.</span></div>
        <div class="yes">{SI}<span>Una línea, un arco o un dato por pieza.</span></div>
        <div class="kick g3 mt3">No</div>
        <div class="nope">{NO}<span>En párrafos o frases enteras de un titular.</span></div>
        <div class="nope">{NO}<span>Como fondo completo de una pieza.</span></div>
        <div class="nope">{NO}<span>Con un tercer color, violeta, magenta o neón.</span></div>
      </div>
    </div>"""
    pg(body, 'oscuro', toc='Gradiente IA')

    body = head('El acento lima', 'Un nodo. <span class="az">Uno.</span>', 'El lima es el nodo del logo llevado a la pieza: el dato que importa, el estado «en marcha», la acción. Si ya hay un elemento lima, no hay otro.')
    body += f"""
    <div class="g mt3 grow">
      <div class="s4"><div class="card" style="height:330px;display:flex;flex-direction:column;justify-content:space-between">
        <div class="eyebrow">Citas este mes · Ejemplo</div>
        <div><div style="font-family:var(--font-display);font-weight:500;font-size:96px;letter-spacing:-.03em;line-height:1">61</div><div class="mono" style="color:{C['lima']['500']};font-size:22px;margin-top:10px">▲ +18 vs. agosto</div></div></div>
        <div class="kick mt2" style="display:flex;gap:10px">{SI} Sobre oscuro</div><p style="font-size:22px">Lima 500 para el delta o el nodo. Un único elemento.</p></div>
      <div class="s4"><div class="card" style="height:330px;display:flex;flex-direction:column;justify-content:space-between;background:#fff;border-color:{G['200']}">
        <div class="eyebrow" style="color:{G['500']}">Citas este mes · Ejemplo</div>
        <div><div style="font-family:var(--font-display);font-weight:500;font-size:96px;letter-spacing:-.03em;line-height:1;color:{G['950']}">61</div><div class="mono" style="color:{G['950']};font-size:22px;margin-top:10px;display:flex;align-items:center;gap:10px"><span style="width:14px;height:14px;border-radius:50%;background:{C['lima']['600']}"></span>+18 vs. agosto</div></div></div>
        <div class="kick mt2" style="display:flex;gap:10px">{SI} Sobre claro</div><p style="font-size:22px">El dato en Grafito 950 y un nodo Lima 600 al lado. Nunca texto lima sobre claro.</p></div>
      <div class="s4"><div class="card" style="height:330px;display:flex;flex-direction:column;justify-content:space-between;opacity:.9">
        <div class="eyebrow" style="color:{C['lima']['500']}">Citas este mes</div>
        <div><div style="font-family:var(--font-display);font-weight:500;font-size:96px;letter-spacing:-.03em;line-height:1;color:{C['lima']['500']}">61</div><div class="mono" style="color:{C['lima']['500']};font-size:22px;margin-top:10px">▲ +18 · ● activo</div></div></div>
        <div class="kick g3 mt2" style="display:flex;gap:10px">{NO} Lima por todas partes</div><p style="font-size:22px">Tres elementos lima: ninguno destaca. Tampoco fondos grandes de lima.</p></div>
    </div>"""
    pg(body, 'oscuro', toc='El acento lima')

    fondos = [('Grafito 950', G['950']), ('Grafito 850', G['850']), ('Blanco', '#FFFFFF'), ('Grafito 50', G['50']), ('Azul IA 500', C['azul']['500'])]
    textos = [('Blanco', '#FFFFFF'), ('Grafito 200', G['200']), ('Titanio 400', G['400']), ('Grafito 500', G['500']), ('Grafito 950', G['950']),
              ('Azul 300', C['azul']['300']), ('Azul 400', C['azul']['400']), ('Azul 600', C['azul']['600']), ('Lima 500', C['lima']['500'])]
    th = ''.join(f'<th>{n}</th>' for n, _ in fondos)
    rows = ''
    for tn, tv in textos:
        cells = ''
        for fn, fv in fondos:
            r = contraste(tv, fv)
            if tv.upper() == fv.upper():
                cells += '<td style="padding:12px 6px;color:var(--tx3)">—</td>'
                continue
            ok = 'AA' if r >= 4.5 else ('AA grande' if r >= 3 else 'No')
            col = 'var(--tx)' if r >= 4.5 else ('var(--tx2)' if r >= 3 else 'var(--tx3)')
            cells += (f'<td style="padding:12px 6px"><div style="display:flex;align-items:center;gap:12px"><span style="background:{fv};color:{tv};border:1px solid var(--borde);border-radius:7px;padding:2px 12px;font-weight:700;font-size:19px">Aa</span>'
                      f'<span class="mono" style="font-size:16px;color:{col}">{num(r, 1)} · {ok}</span></div></td>')
        rows += f'<tr><td style="font-size:19px;padding:12px 12px 12px 0;white-space:nowrap">{tn} <span class="mono" style="font-weight:400;color:var(--tx3);font-size:15px">{tv}</span></td>{cells}</tr>'
    body = head('Contraste', 'Combinaciones <span class="az">accesibles</span>', None)
    body += f'<table class="t mt2" style="table-layout:fixed"><tr><th style="width:18%">Texto \\ Fondo</th>{th}</tr>{rows}</table>'
    body += '<p class="mt1" style="font-size:19px;color:var(--tx3)">WCAG 2.2: AA = 4,5:1 para texto normal; «AA grande» = 3:1, solo para texto ≥ 24 px o ≥ 19 px en negrita. Titanio 400 nunca sobre blanco; Azul IA 500 como texto, solo ≥ 24 px.</p>'
    pg(body, 'claro', toc='Matriz de contraste')

    r_mal = contraste('#FFFFFF', C['cyan']['500'])
    body = head('Botones', 'El botón que vende <span class="az">tiene que leerse</span>', 'Es la corrección más importante de la v2: el CTA principal de la web tenía texto blanco sobre el extremo cyan del gradiente.')
    body += f"""
    <div class="g mt4">
      <div class="s4 card" style="display:flex;flex-direction:column;gap:24px;align-items:flex-start">
        <div class="kick g3" style="display:flex;gap:10px">{NO} Antes</div>
        <span class="btn" style="background:linear-gradient(105deg,#3B72FF,#36CFE0);color:#fff;box-shadow:0 12px 36px -10px rgba(59,114,255,.6)">Agendar valoración →</span>
        <p style="font-size:22px">Blanco sobre gradiente: de 4,2 a <strong>{num(r_mal, 2)}:1</strong>. Suspende WCAG. Sombra de color.</p>
      </div>
      <div class="s4 card" style="display:flex;flex-direction:column;gap:24px;align-items:flex-start">
        <div class="kick" style="display:flex;gap:10px">{SI} Sobre oscuro</div>
        <span class="btn" style="background:var(--grad-ia-oscuro);color:{G['950']}">Agendar valoración →</span>
        <p style="font-size:22px">Gradiente IA + texto Grafito 950: <strong>{num(contraste(G['950'], '#5C8BFF'), 1)} a {num(contraste(G['950'], '#36CFE0'), 1)}:1</strong>. Sin sombra.</p>
      </div>
      <div class="s4 card" style="display:flex;flex-direction:column;gap:24px;align-items:flex-start;background:#fff;border-color:{G['200']}">
        <div class="kick" style="display:flex;gap:10px;color:{C['azul']['600']}">{SI} Sobre claro</div>
        <span class="btn" style="background:{C['azul']['600']};color:#fff">Elegir el mío →</span>
        <p style="font-size:22px;color:{G['600']}">Azul 600 + blanco: <strong style="color:{G['950']}">{num(contraste('#FFFFFF', C['azul']['600']), 1)}:1</strong>. Hover Azul 700 ({num(contraste('#FFFFFF', C['azul']['700']), 1)}:1).</p>
      </div>
    </div>
    <div class="g mt4"><div class="s4 rule"><div class="kick g3">Radio</div><p>14 px (<code>radius m</code>), el mismo que las tarjetas. Píldora solo en chips.</p></div>
    <div class="s4 rule"><div class="kick g3">Secundario</div><p>Contorno 1 px Grafito 700 (oscuro) o 300 (claro), texto blanco o Grafito 950.</p></div>
    <div class="s4 rule"><div class="kick g3">Texto</div><p>Verbo + resultado: «Agendar 30 minutos». Nunca «Saber más».</p></div></div>"""
    pg(body, 'oscuro', toc='Botones y contraste')

    so, sc = TOK['semantic']['oscuro'], TOK['semantic']['claro']
    filas = ''.join(f'<tr><td class="m" style="font-weight:400">{k}</td><td><span style="display:inline-block;width:22px;height:22px;border-radius:5px;vertical-align:-4px;margin-right:10px;border:1px solid var(--borde);background:{so[k] if so[k].startswith("#") else "linear-gradient(135deg,#5C8BFF,#36CFE0)"}"></span><span class="mono">{so[k] if so[k].startswith("#") else "gradiente IA"}</span></td>'
                    f'<td><span style="display:inline-block;width:22px;height:22px;border-radius:5px;vertical-align:-4px;margin-right:10px;border:1px solid var(--borde);background:{sc[k]}"></span><span class="mono">{sc[k]}</span></td></tr>' for k in so)
    body = head('Oscuro y claro', 'Mismo sistema, <span class="az">dos temas</span>')
    body += f"""<div class="g mt3">
      <div class="s7"><table class="t compact"><tr><th>Token semántico</th><th>Oscuro · Oryzz</th><th>Claro · Oryzz Tap y documentos</th></tr>{filas}</table></div>
      <div class="s5"><div class="card"><div class="kick">Cuándo cada uno</div>
      <ul class="l"><li><strong>Oscuro</strong>: expresión principal de Oryzz. Web, slides, redes, anuncios.</li><li><strong>Claro</strong>: Oryzz Tap, documentos A4, facturas, correos transaccionales y todo lo que se imprime.</li><li>En código: <code>data-tema="oscuro"</code> / <code>"claro"</code> con <code>11_Web_y_Codigo/tokens</code>.</li></ul></div></div>
    </div>"""
    pg(body, 'claro', toc='Modo oscuro y claro')

    body = head('Impresión', 'Del píxel <span class="az">al papel</span>')
    body += f"""<div class="g mt3">
      <div class="s7"><table class="t"><tr><th>Color</th><th>CMYK aprox.</th><th>Pantone ref.</th><th>Nota</th></tr>
      {''.join(f'<tr><td>{PALETA[h]["nombre"]}</td><td class="m">{PALETA[h]["cmyk"]}</td><td class="m">{PALETA[h]["pantone"]}</td><td style="font-size:20px">{n}</td></tr>' for h, n in [(G['950'], 'Negro enriquecido, no 100 K'), (C['azul']['500'], 'Pide prueba: el azul RGB pierde viveza'), (C['cyan']['500'], 'Solo en gradientes y datos'), (C['lima']['500'], 'Fluorescente no: usa 374 C'), (C['lima']['600'], 'Nodo sobre papel blanco'), (G['50'], 'Papel; sin tinta')])}
      </table></div>
      <div class="s5"><div class="card"><div class="kick">Reglas de imprenta</div><ul class="l">
        <li>Gradiente: solo en impresión digital o cuatricromía; en serigrafía, bordado o vinilo usa la versión <code>solido</code>.</li>
        <li>Sangrado 3 mm y marcas de corte: ya incluidos en los PDF de imprenta de <code>10_Papeleria_e_Impresion</code>.</li>
        <li>Texto mínimo 9 pt; nada de texto blanco fino sobre negro enriquecido por debajo de 8 pt.</li>
        <li>Pide siempre prueba de color física antes de una tirada.</li></ul></div></div>
    </div>"""
    pg(body, 'oscuro', toc='Color en impresión')


# ---------------------------------------------------------------- 05 Tipografía

def cap_tipo():
    capitulo('05', 'Tipografía', 'Tres familias libres (licencia OFL) con un papel cada una: titular, leer y medir.',
             ['Las tres familias', 'Escala', 'Jerarquía', 'Titulares', 'Tamaños mínimos', 'Instalación'])

    fam = [('Space Grotesk', 'display', 'Display', 'Titulares, cifras grandes y el logo. 500 / 600 / 700, tracking negativo.', 'Más clientes.', 700, '-.045em'),
           ('Manrope', 'texto', 'Texto', 'Párrafos, interfaz y documentos. 400 / 500 / 600 / 700.', 'Validamos con datos si tu negocio puede captar.', 400, '0'),
           ('JetBrains Mono', 'mono', 'Datos', 'Solo dato técnico: cifras tabulares, códigos y URL. Nunca etiquetas ni mayúsculas.', 'CPL 11,40 € · CTR 2,8 %', 500, '0')]
    cols = ''
    for n, v, rol, d, ej, w, tr in fam:
        cols += (f'<div class="s4" style="display:flex;flex-direction:column"><div class="kick">{rol}</div>'
                 f'<div style="font-family:var(--font-{v});font-weight:{w if v != "texto" else 600};font-size:230px;line-height:.9;letter-spacing:{"-.05em" if v == "display" else "-.02em" if v == "texto" else "0"}">Aa</div>'
                 f'<h3 class="mt2" style="font-family:var(--font-{v})">{n}</h3><p class="mt1">{d}</p>'
                 f'<div class="mta rule" style="font-family:var(--font-{v});font-weight:{w};letter-spacing:{tr};font-size:{38 if v == "display" else 28 if v == "texto" else 24}px;color:var(--tx)">{ej}</div></div>')
    body = head('Las tres familias', 'Titular, leer, <span class="az">medir</span>')
    body += f'<div class="g mt3 grow">{cols}</div>'
    pg(body, 'oscuro', toc='Las tres familias')

    chars = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ<br>abcdefghijklmnñopqrstuvwxyz<br>0123456789 €%+−×→ ¿?¡! áéíóúü'
    pesos = ''.join(f'<div style="display:flex;align-items:baseline;gap:30px;border-bottom:1px solid var(--borde);padding:12px 0"><span class="eyebrow" style="width:120px">{w}</span><span style="font-family:var(--font-display);font-weight:{w};font-size:56px;letter-spacing:-.035em">Sistemas que captan clientes</span></div>' for w in (700, 600, 500))
    body = head('Space Grotesk', 'La voz <span class="az">de los titulares</span>')
    body += f"""<div class="g mt3"><div class="s7">{pesos}</div>
    <div class="s5"><div style="font-family:var(--font-display);font-weight:500;font-size:34px;line-height:1.35;letter-spacing:-.01em;color:var(--tx2)">{chars}</div>
    <p class="mt2" style="font-size:22px">Tracking: −0,045 em en display XL, −0,035 em en H1, −0,02 em en H3. Interlineado 0,95–1,2. Nunca en párrafos largos.</p></div></div>"""
    pg(body, 'claro', toc='Space Grotesk')

    body = head('Manrope y JetBrains Mono', 'Para leer <span class="az">y para medir</span>')
    body += f"""<div class="g mt3 grow">
    <div class="s6" style="display:flex;flex-direction:column">
      <div class="kick">Manrope · texto</div>
      <p style="font-size:30px;line-height:1.55;color:var(--tx)">Tu negocio ya recibe visitas, mensajes y llamadas. Lo que falla es lo que pasa después: mensajes que se responden tarde, llamadas que nadie devuelve y anuncios medidos en clics, no en citas.</p>
      <div class="mt2" style="font-family:var(--font-texto);font-size:30px;line-height:1.7;color:var(--tx2)"><span style="font-weight:400">Regular 400</span> · <span style="font-weight:500">Medium 500</span> · <span style="font-weight:600">SemiBold 600</span> · <span style="font-weight:700">Bold 700</span></div>
      <p class="mta" style="font-size:22px">Cuerpo 16 px en web (interlineado 1,6), 9,5 pt en A4 (1,35) y ≥ 36 px en slides.</p>
    </div>
    <div class="s6" style="display:flex;flex-direction:column">
      <div class="kick">JetBrains Mono · datos</div>
      <div style="font-family:var(--font-mono);font-size:30px;color:var(--tx3)">Ref. OZ-2026-0142</div>
      <div style="font-family:var(--font-mono);font-size:44px;color:var(--tx);margin-top:24px">CPL 11,40 €</div>
      <div style="font-family:var(--font-mono);font-size:44px;color:var(--tx)">CTR 2,8 %</div>
      <div style="font-family:var(--font-mono);font-size:30px;color:var(--tx2);margin-top:18px">cal.com/oryzz/30min</div>
      <p class="mta" style="font-size:22px">Nunca para etiquetas: las etiquetas van en Manrope 600, en tipo frase y sin tracking. Cifras tabulares en tablas.</p>
    </div></div>"""
    pg(body, 'oscuro', toc='Manrope y JetBrains Mono')

    filas = ''
    for k, v in TOK['type-scale-px'].items():
        fam = {'display': 'display', 'texto': 'texto', 'mono': 'mono'}[v['font']]
        sz = min(v['size'], 96)
        txt = 'Más clientes.' if v['font'] == 'display' else ('Validamos con datos antes de que gastes.' if v['font'] == 'texto' else 'cal.com/oryzz/30min')
        if k == 'eyebrow':
            txt = 'Qué no necesita tu cliente'
        if k == 'dato':
            txt = '61 citas'
        style = f"font-family:var(--font-{fam});font-weight:{v['weight']};font-size:{sz}px;letter-spacing:{v['tracking']};line-height:1.05;{'text-transform:uppercase;' if v.get('case') == 'upper' else ''}white-space:nowrap"
        filas += (f'<div style="display:flex;align-items:baseline;gap:28px;border-bottom:1px solid var(--borde);padding:{8 if sz < 40 else 6}px 0">'
                  f'<span class="mono" style="width:150px;flex:none;font-size:17px;color:var(--az)">{k}</span>'
                  f'<span class="mono" style="width:270px;flex:none;font-size:17px;color:var(--tx3)">{v["size"]} px · {str(v["line"]).replace(".", ",")} · {v["tracking"]}</span>'
                  f'<span style="{style}">{txt}</span></div>')
    body = f'<div class="eyebrow">Escala tipográfica · web (px)</div><div class="mt2" style="border-top:1px solid var(--borde)">{filas}</div>'
    body += '<p class="mt1" style="font-size:19px;color:var(--tx3)">Valores de <code>tokens.json</code> → <code>type-scale-px</code>. Slides 1920×1080: titulares 64–120 px y lectura ≥ 36 px. A4: titular 22 pt, cuerpo 9,5 pt.</p>'
    pg(body, 'claro', toc='Escala tipográfica')

    body = head('Jerarquía', 'Una página <span class="az">bien jerarquizada</span>')
    body += f"""<div class="g mt3 grow">
      <div class="s7 card" style="padding:56px;display:flex;flex-direction:column;position:relative">
        <div class="eyebrow">El problema</div>
        <div style="font-family:var(--font-display);font-weight:700;font-size:62px;line-height:1.05;letter-spacing:-.035em;margin-top:18px">El problema no es que no te vean. <span class="az">Es que no te contactan.</span></div>
        <p style="margin-top:28px;font-size:26px">Mensajes que se responden tarde, llamadas que nadie devuelve y anuncios medidos en clics, no en citas.</p>
        <div class="mta" style="display:flex;gap:28px;align-items:flex-end"><span class="btn" style="background:var(--cta-bg);color:var(--cta-tx)">Agendar 30 minutos →</span><span class="mono" style="color:var(--tx3);font-size:20px">cal.com/oryzz/30min</span></div>
      </div>
      <div class="s5"><ol class="n">
        <li style="margin-top:0"><strong>Etiqueta</strong> en tipo frase (Manrope 600): sitúa (sección, dato, fecha).</li>
        <li><strong>Titular</strong> en Space Grotesk: 2–3 líneas, un solo fragmento en azul.</li>
        <li><strong>Bajada</strong> en Manrope, Grafito 200 / 600: una idea que amplía el titular.</li>
        <li><strong>Un CTA</strong> y, como mucho, una URL en mono.</li>
        <li>Aire: el espacio vacío es parte del diseño; nunca se rellena.</li>
      </ol></div>
    </div>"""
    pg(body, 'oscuro', toc='Jerarquía')

    body = head('Titulares y tamaños mínimos', 'Frases cortas, <span class="az">un solo resaltado</span>')
    body += f"""<div class="g mt3">
      <div class="s6">
        <div class="yes">{SI}<span style="font-family:var(--font-display);font-weight:700;font-size:40px;letter-spacing:-.03em;color:var(--tx)">Más <span class="az">clientes</span>. No más likes.</span></div>
        <div class="yes">{SI}<span style="font-family:var(--font-display);font-weight:700;font-size:40px;letter-spacing:-.03em;color:var(--tx)">Seis palancas. <span class="az">Un solo sistema.</span></span></div>
        <div class="nope">{NO}<span style="font-family:var(--font-display);font-weight:700;font-size:40px;letter-spacing:-.03em;background:var(--grad);-webkit-background-clip:text;color:transparent">Lleva tu negocio al siguiente nivel</span></div>
        <div class="nope">{NO}<span style="font-family:var(--font-display);font-weight:700;font-size:40px;letter-spacing:-.03em;text-transform:uppercase">MULTIPLICA TUS <span class="az">VENTAS</span> YA</span></div>
      </div>
      <div class="s6"><table class="t"><tr><th>Soporte</th><th>Mínimo</th><th>Lectura</th></tr>
        <tr><td>Pantalla (web, app)</td><td class="m">14 px</td><td class="m">16 px</td></tr>
        <tr><td>Etiqueta (eyebrow)</td><td class="m">14 px</td><td class="m">—</td></tr>
        <tr><td>Impreso</td><td class="m">9 pt</td><td class="m">9,5–11 pt</td></tr>
        <tr><td>Slides 1920×1080</td><td class="m">24 px</td><td class="m">≥ 36 px</td></tr>
        <tr><td>Redes 1080 px</td><td class="m">24 px</td><td class="m">32 px</td></tr>
        <tr><td>Diagramas exportados</td><td class="m">18 px</td><td class="m">—</td></tr>
      </table></div>
    </div>"""
    pg(body, 'claro', toc='Titulares y tamaños mínimos')

    body = head('Instalación', 'Dónde están <span class="az">y cómo se usan</span>')
    body += f"""<div class="g mt3">
      <div class="s4 rule"><div class="kick">Instalar</div><p>Las TTF están en <code>04_Tipografia/TTF_estaticas</code> (y variables en <code>Variables/</code>). Windows: clic derecho › Instalar para todos los usuarios. Mac: doble clic › Instalar.</p><p>También en Google Fonts, gratis.</p></div>
      <div class="s4 rule"><div class="kick">Office y Google</div><p>Las plantillas Word y PowerPoint llevan las fuentes incrustadas. Si alguien no las tiene: <strong>Arial</strong> como alternativa (Consolas para la mono). Google Slides y Docs: las tres están en el menú de fuentes.</p></div>
      <div class="s4 rule"><div class="kick">Canva y Figma</div><p>Canva Pro: sube las TTF a «Brand Kit». Figma: instala las fuentes en el equipo o usa las de Google Fonts. Web: <code>11_Web_y_Codigo/fonts</code> con <code>@font-face</code>.</p></div>
    </div>
    <div class="card mt4"><p style="margin:0">Licencia <strong>SIL Open Font License 1.1</strong> (<code>04_Tipografia/Licencias</code>): se pueden instalar, incrustar y compartir con proveedores sin coste. Retiradas en la v2: Syne, Outfit, Montserrat, DM Sans y Poppins.</p></div>
    <div class="cap mt2">Espécimen completo: 04_Tipografia/Oryzz_Especimen_Tipografico.pdf</div>"""
    pg(body, 'oscuro', toc='Instalación de fuentes')


# ---------------------------------------------------------------- 06 Sistema gráfico

def cap_sistema():
    E = '05_Elementos_Graficos/'
    capitulo('06', 'Sistema gráfico', 'Órbitas, rutas, nodos y datos: los recursos que hacen reconocible una pieza sin necesidad del logo.',
             ['Órbitas', 'Rutas y nodos', 'Retícula y datos', 'Fondos', 'Diagramas', 'Tarjetas dato', 'Iconografía', 'Componentes UI', 'Retícula de maquetación'])

    for f, t, sub, reglas in [
        ('patron-orbitas', 'Órbitas', 'Recurso 01', ['Arcos abiertos concéntricos, espaciado creciente.', 'Trazo 1–2 px en Grafito 700 (oscuro) o 200 (claro).', 'Un solo nodo lima o azul, separado del trazo.', 'Uso: fondos, portadas, aperturas de sección.']),
        ('patron-rutas', 'Rutas y nodos', 'Recurso 02', ['Líneas ortogonales con esquinas redondeadas.', 'Conectan nodos: canal → sistema → cliente.', 'Explican procesos; no decoran.', 'Retícula técnica (64 px al 3,5 %) y campo de nodos: solo textura, nunca más de dos patrones por pieza.'])]:
        body = f"""<div class="g grow">
        <div class="s4" style="display:flex;flex-direction:column"><div class="eyebrow">{sub}</div><h2 style="font-family:var(--font-display);font-weight:700;font-size:72px;letter-spacing:-.035em;line-height:1.02;margin-top:22px">{t}</h2>
        <ul class="l mt3">{''.join(f'<li>{r}</li>' for r in reglas)}</ul></div>
        <div class="s8" style="display:flex;flex-direction:column;gap:20px"><div class="fig" style="height:472px;flex:none"><img src="{uri(E + '02_Patrones/SVG/' + f + '_oscuro_1920x1080.svg')}"></div>
        <div class="fig" style="height:372px;flex:none"><img src="{uri(E + '02_Patrones/SVG/' + f + '_claro_1920x1080.svg')}"></div></div></div>"""
        pg(body, 'oscuro', toc=t)

    fs = ['oryzz-fondo-01_orbita_oscuro_16x9', 'oryzz-fondo-02_orbita_claro_16x9', 'oryzz-fondo-03_rutas_oscuro_16x9', 'oryzz-fondo-04_reticula_claro_16x9']
    v = ['oryzz-fondo-05_orbita_oscuro_4x5', 'oryzz-fondo-07_nodos_oscuro_4x5', 'oryzz-fondo-08_orbita_oscuro_9x16', 'oryzz-fondo-09_orbita_claro_9x16']
    body = head('Fondos', 'Doce fondos <span class="az">listos para usar</span>', 'Cada fondo trae su zona de texto en <code>fondos.json</code>. El titular y el logo van dentro; el nodo queda siempre fuera. No se añade otro halo, órbita ni nodo encima.')
    body += f"""<div class="mt3" style="display:flex;gap:18px;height:460px">
      <div style="flex:3.6;display:grid;grid-template-columns:1fr 1fr;gap:18px">{''.join(f'<div class="fig"><img src="{uri(E + "03_Fondos/SVG/" + f + ".svg")}"></div>' for f in fs)}</div>
      {''.join(f'<div class="fig" style="flex:{0.8 if "4x5" in f else 0.56}"><img src="{uri(E + "03_Fondos/SVG/" + f + ".svg")}"></div>' for f in v)}
    </div><div class="cap">16:9 · 4:5 · 9:16 · A4 — SVG, PNG a tamaño final y PDF a sangre en 05_Elementos_Graficos/03_Fondos</div>"""
    pg(body, 'oscuro', toc='Fondos')

    D = E + '04_Diagramas/SVG_contornos/'
    body = head('Diagramas', 'El método, <span class="az">dibujado</span>')
    body += f"""<div class="g mt3" style="row-gap:20px">
      <div class="s8"><div class="fig" style="height:520px"><img src="{uri(D + 'oryzz-diagrama-01_canales-sistema-cliente_oscuro_contornos.svg')}"></div><div class="cap">Canales → sistema → cliente</div></div>
      <div class="s4" style="display:flex;flex-direction:column;gap:20px">
        <div><div class="fig" style="height:220px"><img src="{uri(D + 'oryzz-diagrama-03_valoracion-30min_oscuro_contornos.svg')}"></div><div class="cap">Valoración de 30 min</div></div>
        <div><div class="fig" style="height:220px"><img src="{uri(D + 'oryzz-diagrama-06_geo-ia_oscuro_contornos.svg')}"></div><div class="cap">GEO</div></div>
      </div>
    </div><p class="mt2" style="font-size:21px">Seis diagramas en oscuro y claro (canales, embudo-órbita, valoración, prueba inicial, flujo Tap, GEO). Las cifras son de ejemplo y lo dicen. Usa <code>SVG_contornos</code> para incrustar sin depender de fuentes.</p>"""
    pg(body, 'oscuro', toc='Diagramas')

    K = E + '05_Componentes_Dato/SVG_contornos/'
    body = head('Tarjetas dato', 'Cifras que <span class="az">se leen de un vistazo</span>')
    body += f"""<div class="g mt3">
      {''.join(f'<div class="s3"><img src="{uri(K + "kpi/oryzz-kpi_" + k + "_oscuro_contornos.svg")}" style="width:100%;display:block"></div>' for k in ('citas', 'coste-por-lead', 'ctr', 'resenas'))}
    </div>
    <div class="g mt2">
      <div class="s6"><img src="{uri(K + 'graficos/oryzz-grafico-barras_oscuro_contornos.svg')}" style="width:100%;display:block;max-height:300px;object-fit:contain;object-position:left"></div>
      <div class="s6"><div style="display:flex;flex-wrap:wrap;gap:14px">{''.join(f'<img src="{uri(K + "chips/oryzz-chip_" + c + "_oscuro_contornos.svg")}" style="height:52px">' for c in ('en-marcha', 'nuevo-lead', 'ejemplo', 'pausado', 'meta-ads', 'google-ads', 'geo'))}</div>
      <p class="mt2" style="font-size:22px">Superficie Grafito 850, borde 1 px Grafito 700, radio 14 px. Etiqueta en Manrope 600 y tipo frase, cifra Space Grotesk 500, delta en lima. Chip «Ejemplo» cuando el dato no es real.</p></div>
    </div>"""
    pg(body, 'oscuro', toc='Tarjetas dato')

    nombres = [p.stem.replace('oz-icono_', '') for p in sorted((RAIZ / E / '01_Iconos/SVG').glob('*.svg'))]
    grid = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:16px;padding:34px 0 22px;border:1px solid var(--borde);border-radius:12px">{icono(n, 64, G["950"], C["lima"]["600"] if n == "calendario" else None)}<span class="mono" style="font-size:15px;color:var(--tx3)">{n}</span></div>' for n in nombres)
    body = f'<div style="display:flex;align-items:baseline;gap:40px"><div class="eyebrow">Iconografía · {len(nombres)} iconos propios</div><div class="eyebrow" style="margin-left:auto">Retícula 24 · trazo 1,75 · puntas redondas</div></div>'
    body += f'<div class="mt3" style="display:grid;grid-template-columns:repeat(11,1fr);gap:14px">{grid}</div>'
    pg(body, 'claro', toc='Iconografía')

    big = icono('calendario', 300, '#FFFFFF', C['lima']['500'])
    body = head('Iconos · reglas', 'Monocromos, <span class="az">un acento</span>')
    body += f"""<div class="g mt3 grow">
      <div class="s5 card" style="display:flex;align-items:center;justify-content:center;position:relative;background-image:linear-gradient(var(--borde) 1px,transparent 1px),linear-gradient(90deg,var(--borde) 1px,transparent 1px);background-size:12.5px 12.5px;background-position:center">
        {big}</div>
      <div class="s7">
        <div class="yes">{SI}<span>Grafito 200 sobre oscuro, Grafito 950 sobre claro. El acento (<code>.oz-acento</code>) solo en un elemento.</span></div>
        <div class="yes">{SI}<span>Tamaños 16, 20, 24, 32, 48. El trazo escala con el icono.</span></div>
        <div class="yes">{SI}<span>Canales (Meta, Google, TikTok) con iconos genéricos; el logo oficial, solo en monocromo.</span></div>
        <div class="nope">{NO}<span>Iconos rellenos de stock, emojis, cohetes, bombillas, cerebros o robots.</span></div>
        <div class="nope">{NO}<span>Iconos de colores mezclados o con los colores de cada plataforma.</span></div>
        <p class="mt2" style="font-size:21px">Sprite web: <code>iconos-sprite.svg</code> · PNG en 4 variantes · lámina en <code>01_Iconos/iconos-lamina.pdf</code>.</p>
      </div>
    </div>"""
    pg(body, 'oscuro', toc='Iconos · reglas')

    body = head('Componentes UI', 'La web, <span class="az">en piezas</span>')
    body += f"""<div class="g mt3 grow">
      <div class="s8"><div class="fig" style="height:680px"><img src="{prep('11_Web_y_Codigo/componentes/componentes_preview.png', 1440, crop=(1440, 1000), name='componentes_top')}" style="object-position:top"></div></div>
      <div class="s4"><ul class="l"><li>Botones primario y secundario en los dos temas.</li><li>Tarjetas, chips, etiquetas y formularios con el contraste corregido.</li><li>Tokens en CSS, SCSS, JSON y Tailwind v4.</li></ul>
      <p class="mt2" style="font-size:22px"><code>11_Web_y_Codigo/componentes/componentes.html</code> y <code>oryzz-ui.css</code>.</p></div>
    </div>"""
    pg(body, 'oscuro', toc='Componentes UI')

    cols = ''.join(f'<div style="background:rgba(59,114,255,.09);border-left:1px solid rgba(59,114,255,.35);border-right:1px solid rgba(59,114,255,.35)"></div>' for _ in range(12))
    body = head('Retícula de maquetación', 'Doce columnas, <span class="az">márgenes generosos</span>')
    body += f"""<div class="g mt3 grow">
      <div class="s8 card" style="position:relative;padding:0;overflow:hidden">
        <div style="position:absolute;inset:36px 64px;display:grid;grid-template-columns:repeat(12,1fr);column-gap:14px">{cols}</div>
        <div style="position:absolute;left:64px;top:70px;width:46%"><div class="eyebrow">Slide 1920×1080</div><div style="font-family:var(--font-display);font-weight:700;font-size:52px;letter-spacing:-.035em;line-height:1.05;margin-top:12px">Texto en 5 columnas; aire en el resto.</div></div>
      </div>
      <div class="s4"><table class="t"><tr><th>Soporte</th><th>Retícula</th></tr>
        <tr><td>Slides 16:9</td><td>12 col · margen 120 px · gutter 32 px</td></tr>
        <tr><td>Web</td><td>12 col · gutter 24 px · máx. 1200 px</td></tr>
        <tr><td>A4</td><td>6 col · margen 20 mm · gutter 5 mm</td></tr>
        <tr><td>Redes 1080</td><td>margen 88–96 px</td></tr></table>
        <p class="mt2" style="font-size:22px">Composición asimétrica: el recurso gráfico en un lado, el texto en el otro. No todo centrado, no todo en tarjetas iguales de tres en tres.</p></div>
    </div>"""
    pg(body, 'oscuro', toc='Retícula de maquetación')


# ---------------------------------------------------------------- 07 Fotografía

def cap_foto():
    F = '05_Elementos_Graficos/06_Fotografia/PNG/'
    capitulo('07', 'Fotografía', 'Personas reales en negocios reales, luz natural y un tratamiento que deja hablar al texto.',
             ['Dirección', 'Sí / No', 'Tratamiento con velo', 'Oryzz Tap en claro'])

    filas = [('Personas reales en clínicas, estética, fisio, gimnasios, hostelería', 'Apretones de manos, equipos riendo ante un portátil'),
             ('Manos, mostradores, móviles, agendas, recepciones', 'Cerebros, robots, hologramas, circuitos, cohetes'),
             ('Luz natural de ventana, lateral y suave', 'Flash frontal, neones, luces de colores'),
             ('Plano medio o detalle, con un tercio libre para texto', 'Planos generales vacíos, simetría centrada, collages'),
             ('Graduación fría y neutra, piel natural', 'Filtros cálidos, HDR, virados violetas o magenta'),
             ('Pantallas desenfocadas o genéricas', 'Capturas legibles de apps o logos de plataformas en color')]
    rows = ''.join(f'<tr><td style="font-weight:400;color:var(--tx2)"><span style="display:inline-flex;gap:12px;align-items:flex-start;color:var(--tx)">{SI}</span> {a}</td><td><span style="color:var(--tx3)">{NO}</span> {b}</td></tr>' for a, b in filas)
    body = head('Dirección', 'Enseñamos el momento <span class="az">en que llega el cliente</span>', 'No enseñamos «marketing». Enseñamos a alguien que llega al mostrador, una mano que confirma una cita, una recepción con gente. Si una foto no cumple esto, mejor un fondo de marca.')
    body += f'<table class="t mt3"><tr><th style="width:50%">Sí</th><th>No</th></tr>{rows}</table>'
    pg(body, 'claro', toc='Dirección fotográfica')

    body = head('Tratamiento con velo', 'Seis pasos <span class="az">obligatorios con texto</span>')
    body += f"""<div class="g mt3 grow">
      <div class="s6"><ol class="n">
        <li style="margin-top:0;font-size:23px"><strong>Velo Grafito 950 al 55–70 %</strong>: más denso del lado del texto. Un solo color en opacidad, no un degradado de colores.</li>
        <li style="font-size:23px"><strong>Texto</strong> blanco (titular) y Grafito 200 (bajada). Etiqueta en Manrope 600, tipo frase.</li>
        <li style="font-size:23px"><strong>Órbita</strong> blanca al 30–40 %, trazo 2 px, que abraza al sujeto sin tocar cara ni manos, con un nodo lima.</li>
        <li style="font-size:23px"><strong>Logo</strong> <code>color-sobre-oscuro</code> solo con velo; si no, <code>mono-blanco</code>.</li>
        <li style="font-size:23px"><strong>CTA</strong> primario oscuro (gradiente + texto grafito).</li>
        <li style="font-size:23px"><strong>Resolución</strong>: 2400 px (redes), 3000 px (web), 300 ppp impreso.</li>
      </ol></div>
      <div class="s3"><div class="fig" style="aspect-ratio:4/5"><img src="{prep(F + 'tratamiento-02_post_4x5.png', 900, fmt='jpg')}"></div><div class="cap">Post 4:5 · velo superior</div></div>
      <div class="s3"><div class="fig" style="aspect-ratio:4/5"><img src="{prep(F + 'tratamiento-03_tap-producto_4x5.png', 900, fmt='jpg')}"></div><div class="cap">Tap · claro, sin velo</div></div>
    </div>
    <p class="mt2" style="font-size:21px;color:var(--tx3)">Plantilla HTML: <code>06_Fotografia/plantilla-foto-velo_16x9.html</code> (cambia <code>--foto</code>). Graduación ≈ 5200–5600 K, saturación −10 a −20.</p>"""
    pg(body, 'oscuro', toc='Tratamiento con velo')


# ---------------------------------------------------------------- 08 Motion

def cap_motion():
    capitulo('08', 'Motion', 'El movimiento sale del logo: la órbita gira, el nodo respira, las «zz» saltan. Y casi nunca más.',
             ['Principios', 'Curvas y duraciones', 'Dónde sí y dónde no'])

    def curva(x1, y1, x2, y2, label, sub):
        W, H = 360, 260
        p = lambda x, y: (40 + x * (W - 80), H - 40 - y * (H - 80))
        a, b, c, d = p(0, 0), p(x1, y1), p(x2, y2), p(1, 1)
        return (f'<div class="card" style="padding:20px 24px"><svg viewBox="0 0 {W} {H}" style="width:100%;height:220px;display:block">'
                f'<rect x="40" y="40" width="{W - 80}" height="{H - 80}" fill="none" stroke="var(--borde)"/>'
                f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="var(--tx3)" stroke-dasharray="4 5"/><line x1="{d[0]}" y1="{d[1]}" x2="{c[0]}" y2="{c[1]}" stroke="var(--tx3)" stroke-dasharray="4 5"/>'
                f'<path d="M{a[0]} {a[1]} C{b[0]} {b[1]} {c[0]} {c[1]} {d[0]} {d[1]}" fill="none" stroke="var(--az)" stroke-width="3" stroke-linecap="round"/>'
                f'<circle cx="{b[0]}" cy="{b[1]}" r="6" fill="var(--tx2)"/><circle cx="{c[0]}" cy="{c[1]}" r="6" fill="var(--tx2)"/></svg>'
                f'<h4 class="mt1">{label}</h4><div class="mono" style="font-size:17px;color:var(--tx3);margin-top:6px">{sub}</div></div>')
    m = TOK['motion']
    body = head('Motion', 'Movimiento <span class="az">con intención</span>')
    body += f"""<div class="g mt3">
      <div class="s4">{curva(.2, .8, .2, 1, 'ease-marca', m['ease-marca'])}</div>
      <div class="s4">{curva(.34, 1.4, .5, 1, 'ease-salto', m['ease-salto'])}</div>
      <div class="s4"><table class="t"><tr><th>Token</th><th>Valor</th></tr>
        <tr><td>rápido</td><td class="m">{m['rapido']}</td></tr><tr><td>base</td><td class="m">{m['base']}</td></tr><tr><td>lento</td><td class="m">{m['lento']}</td></tr><tr><td>órbita</td><td class="m">4,4 s lineal</td></tr><tr><td>«zz»</td><td class="m">1,95 s · desfase 0,17 s</td></tr></table></div>
    </div>
    <div class="g mt2">
      <div class="s6"><div class="kick">Sí</div><div class="yes">{SI}<span>Intros de vídeo, loaders, cierres de reel y de presentación.</span></div><div class="yes">{SI}<span>Transiciones de interfaz de 160–280 ms con <code>ease-marca</code>.</span></div><div class="yes">{SI}<span>Respetar <code>prefers-reduced-motion</code>.</span></div></div>
      <div class="s6"><div class="kick g3">No</div><div class="nope">{NO}<span>Órbitas girando en bucle dentro de la interfaz.</span></div><div class="nope">{NO}<span>Halos que laten, brillos, partículas o glitch.</span></div><div class="nope">{NO}<span>Rotar el logo fuera de la animación oficial.</span></div></div>
    </div>"""
    pg(body, 'oscuro', toc='Principios de motion')

    body = head('Vídeo y edición', 'Reels, anuncios <span class="az">y presentaciones en vídeo</span>', 'Las mismas reglas del sistema, llevadas a la línea de tiempo.')
    body += f"""<div class="g mt2">
      <div class="s4 rule"><div class="kick">Apertura y cierre</div><p>Intro oficial del logo (≤ 3 s) solo al principio o al final. En reels de menos de 20 s, solo al cierre.</p></div>
      <div class="s4 rule"><div class="kick">Rótulos</div><p>Etiqueta en tipo frase (Manrope 600) + titular en Space Grotesk, alineados a la izquierda dentro de la zona segura. Un fragmento en azul.</p></div>
      <div class="s4 rule"><div class="kick">Subtítulos</div><p>Sin caja: Manrope Bold blanco con sombra difusa Grafito 950 (contorno o velo, solo si el fondo lo exige). Destacado en Azul 400. Máx. 2 líneas, ≥ 48 px.</p></div>
      <div class="s4 rule"><div class="kick">Cortes</div><p>Cortes secos o fundidos de 160–280 ms. Nada de transiciones de plantilla (cubos, zoom-blur, destellos).</p></div>
      <div class="s4 rule"><div class="kick">Color</div><p>Graduación fría y neutra (como la fotografía). Ningún LUT cálido ni teal-orange.</p></div>
      <div class="s4 rule"><div class="kick">Datos en pantalla</div><p>Tarjetas dato de <code>05_Componentes_Dato</code>, con «Ejemplo» si no son reales. Un solo lima.</p></div>
    </div>
    <p class="mt2" style="font-size:22px">Zonas seguras para 9:16: <code>09_Redes_Sociales/Stories/_guia_zonas_seguras.png</code> y <code>Otros/_guias/reel_tiktok_portada_GUIA_zonas_seguras.png</code>.</p>
    <p style="font-size:22px;margin-top:6px">Dirección completa de edición (hooks, subtítulos, animaciones de datos, sonido y control de calidad): skill <code>editor-oryzz</code> del repo <code>Oryzz-COL/Editor</code>.</p>"""
    pg(body, 'oscuro', toc='Vídeo y edición')


# ---------------------------------------------------------------- 09 Voz

def cap_voz():
    capitulo('09', 'Voz y tono', 'Clara, directa, segura, sin humo. Hablamos de clientes, citas, mensajes y euros.',
             ['Principios', 'Sí / No', 'Glosario', 'Titulares y CTA', 'Correos'], tema='claro')

    pr = [('Concreta', 'Cifras con unidades: «30 minutos», «50–100 €», «3–7 días».'), ('Honesta', '«Si no encajamos, te lo decimos.» Nada de garantías de resultados.'),
          ('Cercana', 'Tuteo. Frases cortas. Una persona hablando con otra.'), ('Útil', 'Cada pieza deja una idea aplicable o un siguiente paso claro.')]
    body = head('Principios', 'Cuatro reglas <span class="az">para escribir como Oryzz</span>')
    body += '<div class="g mt4">' + ''.join(f'<div class="s3 rule"><div class="kick">0{i + 1}</div><h3>{a}</h3><p class="mt1">{b}</p></div>' for i, (a, b) in enumerate(pr)) + '</div>'
    body += f"""<div class="card mt4"><div class="kick g3">Oryzz Tap</div><p style="font-size:28px;color:var(--tx)">Más cálido y de producto —«Acerca el teléfono y ocurre»—, con las mismas reglas.</p></div>"""
    pg(body, 'claro', toc='Principios de voz')

    pares = [('Validamos con datos si tu negocio puede captar antes de que gastes de más.', 'Lleva tu negocio al siguiente nivel.'),
             ('Primeros datos en 3–7 días.', 'Multiplica tus ventas en 7 días.'),
             ('Si no encajamos, te lo decimos.', 'Resultados garantizados.'),
             ('61 citas en septiembre, a 11,40 € cada una. (Ejemplo)', 'Hemos disparado tu engagement un 300 %.'),
             ('Te contestamos en WhatsApp en menos de 2 minutos.', 'Soluciones de marketing 360 impulsadas por IA.')]
    rows = ''.join(f'<tr><td style="font-weight:400;color:var(--tx)">«{a}»</td><td style="color:var(--tx3)">«{b}»</td></tr>' for a, b in pares)
    body = head('Sí / No', 'La diferencia <span class="az">en una frase</span>')
    body += f'<table class="t mt3"><tr><th style="width:55%">Decimos</th><th>No decimos</th></tr>{rows}</table>'
    body += '<p class="mt2">Sin emojis en titulares, sin exclamaciones dobles, sin MAYÚSCULAS enteras. Un único CTA por pieza.</p>'
    pg(body, 'oscuro', toc='Sí / No')

    glos = [('clientes, citas, leads', 'audiencia, impresiones, engagement'), ('mensajes, llamadas, reservas', 'interacciones, touchpoints'),
            ('coste por cita, coste por lead', 'ROI garantizado, «x10»'), ('sistema de captación', 'estrategia 360, ecosistema digital'),
            ('IA que responde en WhatsApp', 'IA revolucionaria, magia, disruptivo'), ('valoración de 30 minutos', 'auditoría GRATIS'),
            ('negocio, clínica, centro, gimnasio', 'marca personal, comunidad (salvo que lo sea)')]
    rows = ''.join(f'<tr><td>{a}</td><td style="text-decoration:line-through;color:var(--tx3)">{b}</td></tr>' for a, b in glos)
    proh = ['siguiente nivel', 'revoluciona', 'descubre', 'potencia', 'sinergia', 'disruptivo', 'garantizado', 'GRATIS', 'haz clic aquí', 'saber más', 'game changer', 'top']
    body = head('Glosario', 'Palabras que usamos <span class="az">y palabras que no</span>')
    body += f"""<div class="g mt3"><div class="s8"><table class="t"><tr><th>Sí</th><th>No</th></tr>{rows}</table></div>
    <div class="s4"><div class="kick g3">Prohibidas en cualquier pieza</div><div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:8px">{''.join(f'<span class="chip" style="text-transform:none;letter-spacing:.02em;font-size:19px">{p}</span>' for p in proh)}</div></div></div>"""
    pg(body, 'claro', toc='Glosario')

    body = head('Titulares y CTA', 'Escribir <span class="az">para que contesten</span>')
    body += f"""<div class="g mt3">
      <div class="s6"><div class="kick">Titulares</div><ol class="n">
        <li style="margin-top:0">Empieza por el problema o el resultado del cliente, no por Oryzz.</li>
        <li>Máximo 2–3 líneas. Un fragmento en azul, nunca la frase entera.</li>
        <li>Una cifra concreta vale más que tres adjetivos.</li>
        <li>Prueba de la recepción: ¿lo entendería la recepcionista de una clínica en 3 segundos?</li></ol></div>
      <div class="s6"><div class="kick">CTA</div>
        <div style="display:flex;flex-direction:column;gap:16px;align-items:flex-start;margin-top:8px">
          <span class="btn" style="background:var(--cta-bg);color:var(--cta-tx)">Agendar 30 minutos →</span>
          <span class="btn" style="background:var(--cta-bg);color:var(--cta-tx)">Ver el panel completo →</span>
          <span class="btn" style="background:var(--cta-bg);color:var(--cta-tx)">Activar mi Oryzz Tap →</span></div>
        <p class="mt2">Verbo + resultado. Uno por pieza. Prohibidos: «Haz clic aquí», «Saber más», «Descubre», «¡Empieza ya!».</p></div>
    </div>"""
    pg(body, 'oscuro', toc='Titulares y CTA')

    lon = [('Prospección (primer contacto)', '70–120', 'Una observación real de su negocio, qué hacemos, una pregunta.'), ('Seguimiento 1', '30–60', 'Mismo hilo, recordatorio en una frase.'),
           ('Seguimiento 2 (último)', '60–100', 'Aporta una idea útil aunque no conteste.'), ('Transaccional', '80–180', 'Datos arriba, instrucciones después.'),
           ('Bienvenida / informe', '200–400', 'Escaneable: titulares, tarjetas, listas.'), ('Newsletter', '300–500', '2–3 bloques, 5 minutos de lectura.')]
    rows = ''.join(f'<tr><td>{a}</td><td class="m">{b}</td><td>{c}</td></tr>' for a, b, c in lon)
    body = head('Correos', 'Asunto concreto, <span class="az">una sola acción</span>')
    body += f"""<div class="g mt3">
      <div class="s7"><table class="t"><tr><th>Tipo</th><th>Palabras</th><th>Clave</th></tr>{rows}</table></div>
      <div class="s5"><div class="card"><div class="kick">Asunto · 30–50 caracteres</div>
        <div class="yes" style="font-size:22px">{SI}<span>Septiembre en Arrieta: 61 citas y el coste por lead a la baja</span></div>
        <div class="yes" style="font-size:22px">{SI}<span>¿Te nombra ChatGPT cuando buscan fisio en Valencia?</span></div>
        <div class="nope" style="font-size:22px">{NO}<span>¡¡Lleva tu clínica al siguiente nivel!!</span></div>
        <div class="nope" style="font-size:22px;border:none">{NO}<span>RE: nuestra conversación</span></div></div>
        <p class="mt2" style="font-size:21px">Saludo «Hola, {{{{nombre}}}}:». Nunca «Estimado/a cliente». Guía completa: <code>08_Email/Guia_de_redaccion_email.md</code>.</p></div>
    </div>"""
    pg(body, 'oscuro', toc='Correos')


# ---------------------------------------------------------------- 10 Aplicaciones

def cap_aplicaciones():
    capitulo('10', 'Aplicaciones', 'El sistema aplicado. Cada pieza de este capítulo existe como plantilla editable en el kit.',
             ['Web', 'Instagram', 'Carrusel y stories', 'LinkedIn y otros', 'Email y firmas', 'Presentaciones', 'Documentos', 'Papelería', 'Gran formato y merchandising'])

    ev = '12_Auditoria_y_Mejoras/evidencias/'
    body = head('Web', 'oryzz.com, <span class="az">con el sistema v2</span>', None)
    body += f"""<div class="g mt3 grow">
      <div class="s7"><div class="fig" style="height:660px"><img src="{prep('11_Web_y_Codigo/componentes/componentes_preview.png', 1440, crop=(1440, 1100), name='web_comp')}" style="object-position:top"></div></div>
      <div class="s5"><ol class="n">
        <li style="margin-top:0">Enlaza <code>tokens.css</code> antes de los estilos y marca el tema: <code>data-tema="oscuro"</code> (Oryzz) o <code>"claro"</code> (Tap).</li>
        <li>Logo y favicon siempre desde <code>02_Logos</code> (SVG). Nunca texto vivo.</li>
        <li>Botón principal: gradiente + texto grafito, sin sombra. Un CTA por bloque.</li>
        <li>Texto mínimo 14 px; etiquetas en Manrope 600, tipo frase.</li>
        <li>Iconos monocromos del set propio; fuera halos animados.</li></ol>
        <p class="mt2" style="font-size:21px">Plan completo de migración en el capítulo «Checklists» y en <code>12_Auditoria_y_Mejoras</code>.</p></div>
    </div>"""
    pg(body, 'oscuro', toc='Web')

    I = '09_Redes_Sociales/Instagram_Oryzz/'
    osc = ['01_titular', '02_cifra', '05_cita', '08_cta_valoracion']
    cla = ['03_mito', '06_checklist']
    tiles = ''.join(f'<div><div class="fig" style="aspect-ratio:4/5"><img src="{prep(I + "oscuro/" + f + ".png", 640, fmt="jpg")}"></div></div>' for f in osc)
    tiles += ''.join(f'<div><div class="fig" style="aspect-ratio:4/5"><img src="{prep(I + "claro/" + f + ".png", 640, fmt="jpg")}"></div></div>' for f in cla)
    body = f"""<div style="display:flex;align-items:baseline"><div class="eyebrow">Instagram · @oryzzai · 4:5</div><div class="eyebrow" style="margin-left:auto">8 tipos de post · oscuro y claro · 09_Redes_Sociales</div></div>
    <h2 style="font-family:var(--font-display);font-weight:700;font-size:56px;letter-spacing:-.035em;margin-top:16px">Un post, <span class="az">una idea</span>, un dato.</h2>
    <div class="mt3" style="display:grid;grid-template-columns:repeat(6,1fr);gap:16px">{tiles}</div>
    <p class="mt2" style="font-size:22px">Las piezas se generan desde texto: escribe el copy en <code>_generador/contenido/*.json</code> o en una hoja de cálculo y ejecuta <code>python generar.py</code>. El generador avisa si un titular no cabe.</p>"""
    pg(body, 'oscuro', toc='Instagram')

    car = '09_Redes_Sociales/Instagram_Oryzz/carrusel_geo_clinicas/'
    st = '09_Redes_Sociales/Stories/Oryzz/'
    body = f"""<div class="eyebrow">Carrusel · stories · destacados</div>
    <div class="fig mt2" style="height:300px;background:transparent;border:none"><img src="{prep(car + '_vista_continua_carrusel_geo.png', 1700, fmt='jpg', name='carrusel_cont')}" style="object-fit:contain;object-position:left"></div>
    <div class="cap">Carrusel de 8 slides · una línea continua atraviesa todas</div>
    <div class="mt2" style="display:flex;gap:16px;height:440px">
      {''.join(f'<div class="fig" style="aspect-ratio:9/16;height:100%"><img src="{prep(st + f + ".png", 420, fmt="jpg")}"></div>' for f in ('01_pregunta', '03_dato', '05_testimonio', '06_cta'))}
      <div style="flex:1;padding-left:20px"><ul class="l"><li>Stories con zona segura: nada importante en los 250 px superiores e inferiores.</li><li>Portadas de destacados con iconos del set propio.</li><li>Carruseles: portada con promesa, desarrollo de una idea por slide, cierre con un CTA.</li></ul></div>
    </div>"""
    pg(body, 'oscuro', toc='Carrusel y stories')

    LI = '09_Redes_Sociales/LinkedIn/'
    O = '09_Redes_Sociales/Otros/'
    body = f"""<div class="eyebrow">LinkedIn · YouTube · Open Graph · Google Business</div>
    <div class="g mt2" style="row-gap:18px">
      <div class="s12"><div class="fig" style="height:260px"><img src="{prep(LI + 'banner_empresa_1128x191.png', 1680, fmt='jpg')}"></div><div class="cap">Banner de empresa · 1128×191</div></div>
      <div class="s6"><div class="fig"><img src="{prep(LI + 'banner_personal_juan_salazar_1584x396.png', 900, fmt='jpg')}" style="height:auto"></div><div class="cap">Banner personal · socios</div></div>
      <div class="s6"><div class="fig"><img src="{prep(O + 'og_oryzz_1200x630.png', 900, fmt='jpg')}" style="height:auto;aspect-ratio:1200/630"></div><div class="cap">Imagen para compartir la web (OG) · 1200×630</div></div>
    </div>"""
    pg(body, 'oscuro', toc='LinkedIn y otros formatos')

    E = '08_Email/_previews/'
    body = f"""<div style="display:flex;align-items:baseline"><div class="eyebrow">Email · 10 plantillas · firmas</div><div class="eyebrow" style="margin-left:auto">08_Email</div></div>
    <div class="g mt2 grow">
      {''.join(f'<div class="s3" style="display:flex;flex-direction:column"><div class="fig" style="flex:1"><img src="{prep(E + f + ".png", 700, crop=(600, 840), name="em_" + f)}" style="object-position:top"></div><div class="cap">{t}</div></div>' for f, t in (('04_confirmacion_valoracion_escritorio-600', 'Confirmación de valoración'), ('06_informe_mensual_oscuro-600', 'Informe mensual · oscuro'), ('08_tap_pedido_confirmado_escritorio-600', 'Tap · pedido confirmado')))}
      <div class="s3" style="display:flex;flex-direction:column"><div class="fig" style="flex:1;background:#fff"><img src="{prep(E + 'firmas_escritorio.png', 900, name='firmas')}" style="object-fit:contain;object-position:top"></div><div class="cap">Firmas Juan y David</div></div>
    </div>
    <p class="mt2" style="font-size:21px">HTML con tablas y CSS en línea, 600 px que se adaptan a 375 px, botón compatible con Outlook y Arial como alternativa. Logo en PNG sólido. Listas para enviar en <code>_listo_para_enviar</code>.</p>"""
    pg(body, 'claro', toc='Email y firmas')

    P = '06_Presentaciones/_previews/'
    sl = [('Oryzz_Plantilla_Presentacion_Oscura', 's01'), ('Oryzz_Plantilla_Presentacion_Oscura', 's08'), ('Oryzz_Plantilla_Presentacion_Oscura', 's06'),
          ('Oryzz_Plantilla_Presentacion_Clara', 's02'), ('Oryzz_Deck_Comercial_Ejemplo', 's01'), ('OryzzTap_Plantilla_Presentacion', 's01')]
    tiles = ''.join(f'<div class="s4"><div class="fig" style="aspect-ratio:16/9"><img src="{prep(P + d + "/" + s + ".png", 760, fmt="jpg", name=d + s)}"></div></div>' for d, s in sl)
    body = f"""<div style="display:flex;align-items:baseline"><div class="eyebrow">Presentaciones · PowerPoint</div><div class="eyebrow" style="margin-left:auto">06_Presentaciones</div></div>
    <div class="g mt2" style="row-gap:20px">{tiles}</div>
    <div class="g mt2"><div class="s4 rule"><div class="kick g3">Plantillas</div><p style="font-size:22px">Oscura y clara: 28 diseños en el patrón y 25 diapositivas de ejemplo cada una.</p></div>
    <div class="s4 rule"><div class="kick g3">Deck comercial</div><p style="font-size:22px">15 diapositivas para una clínica ficticia. Precios y plazos de ejemplo: revísalos.</p></div>
    <div class="s4 rule"><div class="kick g3">Oryzz Tap</div><p style="font-size:22px">11 diapositivas con placa y stand dibujados como planos.</p></div></div>"""
    pg(body, 'oscuro', toc='Presentaciones')

    D = '07_Documentos/'
    docs = [('01_Propuesta_Comercial/Oryzz_Propuesta-Comercial_EJEMPLO.pdf', 'Propuesta'), ('02_Informe_Diagnostico/Oryzz_Informe-Diagnostico_EJEMPLO.pdf', 'Diagnóstico'),
            ('03_Informe_Mensual/Oryzz_Informe-Mensual_EJEMPLO.pdf', 'Informe mensual'), ('04_Caso_de_Estudio/Oryzz_Caso-de-Estudio_EJEMPLO.pdf', 'Caso de estudio'),
            ('05_Presupuesto_y_Factura/Oryzz_Factura_EJEMPLO.pdf', 'Factura'), ('08_One_Pagers/Oryzz-Tap_One-Pager.pdf', 'One-pager Tap')]
    tiles = ''.join(f'<div><div class="fig" style="aspect-ratio:210/297;background:#fff"><img src="{pdf_page(D + f, 0, 560)}"></div><div class="cap">{t}</div></div>' for f, t in docs)
    body = f"""<div style="display:flex;align-items:baseline"><div class="eyebrow">Documentos A4 · Word + PDF</div><div class="eyebrow" style="margin-left:auto">07_Documentos</div></div>
    <div class="mt2" style="display:grid;grid-template-columns:repeat(6,1fr);gap:20px">{tiles}</div>
    <div class="g mt3"><div class="s6"><p style="font-size:22px">Doce plantillas Word con estilos propios (Título, Eyebrow, Dato, Campo…), tema de Office «Oryzz» y fuentes incrustadas. Rellena los <code>{{{{campos}}}}</code>, borra las líneas «Guía ·» y exporta a PDF.</p></div>
    <div class="s6"><p style="font-size:22px">Los clientes y cifras de los ejemplos son ficticios y van marcados como tales. El contrato es una maqueta: cada cláusula, a revisar por asesor legal.</p></div></div>"""
    pg(body, 'claro', toc='Documentos')

    PP = '10_Papeleria_e_Impresion/'
    body = f"""<div style="display:flex;align-items:baseline"><div class="eyebrow">Papelería</div><div class="eyebrow" style="margin-left:auto">10_Papeleria_e_Impresion</div></div>
    <div class="g mt2 grow" style="row-gap:20px">
      <div class="s3"><div class="fig" style="aspect-ratio:85/55"><img src="{pdf_page(PP + '01_Tarjetas_de_Visita/PDF_sin_marcas/oryzz_tarjeta_juan-salazar_oscura.pdf', 0, 700)}"></div><div class="cap">Tarjeta · anverso oscuro</div></div>
      <div class="s3"><div class="fig" style="aspect-ratio:85/55"><img src="{pdf_page(PP + '01_Tarjetas_de_Visita/PDF_sin_marcas/oryzz_tarjeta_juan-salazar_oscura.pdf', 1, 700)}"></div><div class="cap">Tarjeta · reverso</div></div>
      <div class="s3"><div class="fig" style="aspect-ratio:85/55"><img src="{pdf_page(PP + '01_Tarjetas_de_Visita/PDF_sin_marcas/oryzz_tarjeta_david-morales_clara.pdf', 0, 700)}"></div><div class="cap">Tarjeta · versión clara</div></div>
      <div class="s3" style="grid-row:span 2"><div class="fig" style="aspect-ratio:210/297;background:#fff"><img src="{pdf_page(PP + '02_Membrete_Sobre_Carpeta/PDF_sin_marcas/oryzz_membrete_A4.pdf', 0, 600)}"></div><div class="cap">Membrete A4</div></div>
      <div class="s5"><div class="fig" style="aspect-ratio:220/110;background:#fff"><img src="{pdf_page(PP + '02_Membrete_Sobre_Carpeta/PDF_sin_marcas/oryzz_sobre_DL.pdf', 0, 900)}"></div><div class="cap">Sobre DL</div></div>
      <div class="s4"><p style="font-size:22px">Cada pieza en tres formatos: <strong>PDF de imprenta</strong> (sangrado 3 mm y marcas), PDF sin marcas y SVG editable. Datos personales en campos fáciles de cambiar.</p></div>
    </div>"""
    pg(body, 'oscuro', toc='Papelería')

    body = f"""<div class="eyebrow">Gran formato · producto · merchandising</div>
    <div class="g mt2 grow">
      <div class="s2"><div class="fig" style="height:100%;background:transparent;border:none"><img src="{pdf_page(PP + '05_Rollup_y_Cartel/PDF_sin_marcas/oryzz_rollup_85x200cm.pdf', 0, 500)}" style="object-fit:contain"></div><div class="cap">Roll-up 85×200</div></div>
      <div class="s3"><div class="fig" style="height:100%;background:transparent;border:none"><img src="{pdf_page(PP + '05_Rollup_y_Cartel/PDF_sin_marcas/oryzz-tap_cartel_A3.pdf', 0, 700)}" style="object-fit:contain"></div><div class="cap">Cartel Tap A3</div></div>
      <div class="s7"><div class="fig" style="height:100%"><img src="{prep(PP + '06_Merchandising/Vista_previa_PNG/oryzz_merchandising_mockup.png', 1300, fmt='jpg')}" style="object-fit:contain;background:#fff"></div><div class="cap">Merchandising · camiseta, taza, tote, pegatinas</div></div>
    </div>
    <p class="mt2" style="font-size:21px">En bordado, serigrafía y vinilo, siempre el logo <code>solido</code> o <code>mono</code>: el gradiente no se reproduce bien. Pegatinas y etiquetas de envío Tap con troquel incluido.</p>"""
    pg(body, 'oscuro', toc='Gran formato y merchandising')


# ---------------------------------------------------------------- 11 Tap

def cap_tap():
    capitulo('11', 'Oryzz Tap', 'La línea de producto físico. Mismo sistema que Oryzz, expresión en claro y más producto.',
             ['Expresión', 'Producto y piezas', 'Reglas propias y migración'], tema='claro',
             fondo=orbitas_fondo(1560, 640, [180, 300, 430, 570, 720], 'claro', nodo_ang=-120))

    body = f"""<div class="g grow">
      <div class="s6" style="display:flex;flex-direction:column">
        <div class="eyebrow">Expresión</div>
        <h2 class="big" style="font-size:96px;margin-top:22px">Tu negocio.<br><span class="az">A un toque.</span></h2>
        <p class="lead mt3">Oryzz Tap usa el mismo logo, la misma paleta y las mismas tipografías. Lo que cambia es el tono visual: fondo claro, fotografía de producto y más blanco.</p>
        <div class="mta" style="display:flex;gap:40px;align-items:center"><img src="{uri('02_Logos/07_Submarca_Tap/SVG/oryzz-tap-horizontal_color-sobre-claro.svg')}" style="height:70px"><span class="btn" style="background:var(--cta-bg);color:var(--cta-tx)">Elegir el mío →</span></div>
      </div>
      <div class="s6" style="display:flex;justify-content:flex-end"><div class="fig" style="height:864px;aspect-ratio:4/5"><img src="{prep('05_Elementos_Graficos/06_Fotografia/PNG/tratamiento-03_tap-producto_4x5.png', 1000, fmt='jpg', name='tap_prod')}"></div></div>
    </div>"""
    pg(body, 'claro', toc='Expresión Oryzz Tap')

    T = '09_Redes_Sociales/Instagram_Tap/'
    tiles = ''.join(f'<div><div class="fig" style="aspect-ratio:4/5"><img src="{prep(T + f + ".png", 640, fmt="jpg")}"></div></div>' for f in ('01_producto', '02_como_funciona', '03_resenas_vs_pro', '04_placa_vs_stand', '05_activacion'))
    body = f"""<div style="display:flex;align-items:baseline"><div class="eyebrow">Producto y piezas · @oryzztap</div><div class="eyebrow" style="margin-left:auto">Instagram · tarjeta de producto · one-pager</div></div>
    <div class="mt2" style="display:grid;grid-template-columns:repeat(5,1fr);gap:16px">{tiles}</div>
    <div class="g mt2"><div class="s3"><div class="fig" style="aspect-ratio:148/105;background:#fff"><img src="{pdf_page('10_Papeleria_e_Impresion/04_Tarjeta_Producto_Tap/PDF_sin_marcas/oryzz-tap_tarjeta-producto_A6.pdf', 0, 700)}"></div><div class="cap">Tarjeta de producto A6 (en la caja)</div></div>
    <div class="s9"><ul class="l"><li>Nombres de producto: <strong>Oryzz Tap Reseñas Google</strong> y <strong>Oryzz Tap Pro</strong>. Precios en COP.</li><li>El gesto del toque (mano + móvil + placa) es la imagen central.</li><li>Instrucciones en tres pasos, con iconos <code>nfc</code>, <code>qr</code> y <code>resenas</code>.</li></ul></div></div>"""
    pg(body, 'claro', toc='Producto y piezas Tap')

    mig = [('Tipografías', 'Syne + Outfit', 'Space Grotesk + Manrope'), ('Azul', '#0075FF', 'Azul 600 #2C5BD0 (botones) · Azul IA #3B72FF'),
           ('Lima', '#C5F500', 'Lima 600 #7FB02E (nodo sobre claro)'), ('Logo', 'Órbita + 5 estrellas, «Tap»', 'oryzz tap v2, sin estrellas'),
           ('Fondo', '#EEF2F6', 'Blanco / Grafito 50 #F6F7F9'), ('Barra de anuncios', 'Emojis y marquesina', 'Texto fijo, sin emojis'),
           ('Nombre', 'OryzzTAP, MyOryzz', 'Oryzz Tap')]
    rows = ''.join(f'<tr><td>{a}</td><td style="text-decoration:line-through;color:var(--tx3)">{b}</td><td style="color:var(--tx)">{c}</td></tr>' for a, b, c in mig)
    body = head('Reglas propias y migración', 'Lo que queda <span class="az">obsoleto en Tap</span>')
    body += f"""<div class="g mt3"><div class="s8"><table class="t"><tr><th>Elemento</th><th>Antes</th><th>v2</th></tr>{rows}</table></div>
    <div class="s4"><div class="card"><div class="kick">Reglas de Tap</div><ul class="l"><li>Expresión principal en claro.</li><li>Foto de producto luminosa, sin velo; el texto va en un bloque contiguo.</li><li>Tono más cálido: «Acerca el teléfono y ocurre».</li><li>Placas y stands físicos: reimprimir con el lockup v2 al agotar stock.</li></ul></div></div></div>"""
    pg(body, 'claro', toc='Reglas propias y migración Tap')


# ---------------------------------------------------------------- 12 Checklists

def cap_check():
    capitulo('12', 'Checklists', 'Dos listas: la que se pasa antes de publicar cualquier pieza y la que ordena la migración a la v2.',
             ['Antes de publicar', 'Plan de migración'])

    items = [('Logo', 'SVG maestro, colorway correcto para el fondo, área de respeto y tamaño mínimo.'),
             ('Acento', 'Un solo elemento lima. Un solo fragmento azul en el titular.'),
             ('Color', 'Nada de violeta, magenta, neón ni gradientes de tres colores.'),
             ('Luz', 'Sin manchas difusas, esferas brillantes, auroras ni glassmorphism. Máximo un halo ≤ 20 %.'),
             ('Iconos', 'Del set propio, monocromos. Sin emojis, cohetes, bombillas, cerebros ni robots.'),
             ('Texto', 'Copy real, sin lorem ipsum. Tuteo, frases cortas, sin palabras prohibidas. Etiquetas en tipo frase, sin numeraciones.'),
             ('Datos', 'Cifras con unidad y fuente; si no son reales, «Ejemplo» o {{dato}}.'),
             ('Composición', 'Asimétrica, alineada a la retícula, con aire. No todo centrado ni en tarjetas iguales.'),
             ('Tamaños', '≥ 14 px pantalla · ≥ 9 pt impreso · ≥ 36 px lectura en slides.'),
             ('CTA', 'Uno. Verbo + resultado. Con contraste AA.')]
    rows = ''.join(f'<div style="display:flex;gap:24px;align-items:flex-start;padding:15px 0;border-bottom:1px solid var(--borde)"><span style="width:30px;height:30px;border:2px solid var(--tx3);border-radius:7px;flex:none;margin-top:2px"></span><span style="width:200px;flex:none;font-family:var(--font-display);font-weight:600;font-size:27px;color:var(--tx)">{a}</span><span style="font-size:24px;color:var(--tx2)">{b}</span></div>' for a, b in items)
    body = head('Antes de publicar', 'Diez comprobaciones <span class="az">anti «AI slop»</span>')
    body += f'<div class="mt2" style="border-top:1px solid var(--borde)">{rows}</div>'
    pg(body, 'oscuro', toc='Checklist antes de publicar')

    fases = [('Fase 0', 'Semana 0–1', 'Gobernanza', ['Localizar y versionar el repositorio real de /tap.', 'Aprobar tokens.json v2 como fuente única.', 'Correo de dominio (hola@oryzz.com).']),
             ('Fase 1', 'Semana 1', 'Correcciones críticas', ['CTA con texto grafito (oscuro) / Azul 600 (claro).', 'Grises legibles; «Oryzz Tap» bien escrito.', 'Logos y favicon SVG v2; Tap sin emojis.']),
             ('Fase 2', 'Semanas 2–3', 'Migración del sistema', ['tokens.css y fuentes en ambas webs.', '91 HEX sueltos de Tap → tokens.', 'Iconos monocromos; fuera halos y bucles.']),
             ('Fase 3', 'Semanas 3–4', 'Contenido y metadatos', ['og-images, JSON-LD con logo cuadrado.', 'CTA único, «Primeros datos en 3–7 días».', 'Composición asimétrica.']),
             ('Fase 4', 'Semanas 4–6', 'Fuera de la web', ['Documentos, redes y email con el kit v2.', 'Retirar la plantilla navy/Montserrat.', 'Reimprimir placas y stands Tap.'])]
    cols = ''.join(f'<div class="card" style="display:flex;flex-direction:column"><div class="kick">{b}</div><h4>{c}</h4><ul class="l mt1">{"".join(f"<li style=font-size:21px>{x}</li>" for x in xs)}</ul></div>' for a, b, c, xs in fases)
    body = head('Plan de migración', 'De la v1 a la v2 <span class="az">en 4–6 semanas</span>', 'Resumen de la auditoría de marca (nota de partida 4,3/10). Checklist detallado por canal en <code>12_Auditoria_y_Mejoras/Auditoria_de_Marca.md</code>.')
    body += f'<div class="mt3" style="display:grid;grid-template-columns:repeat(5,1fr);gap:18px">{cols}</div>'
    pg(body, 'claro', toc='Plan de migración')


# ---------------------------------------------------------------- 13 Archivos

def cap_archivos():
    capitulo('13', 'Archivos del kit', 'Qué hay en cada carpeta y cómo se regenera. Todo el kit sale de una sola fuente.',
             ['Mapa de carpetas', 'Fuente de verdad', 'Contacto y versión'])

    car = [('00_Fuente_Maestra', 'BRAND_SPEC.md, tokens.json, brand.css, fuentes y los scripts que generan todo el kit.'),
           ('01_Guia_de_Marca', 'Este manual, el resumen de una página y su LEEME.'),
           ('02_Logos', '91 SVG + PNG y PDF: horizontal, vertical, wordmark, isotipo, avatares, favicon, Tap, animado, láminas de uso.'),
           ('03_Color', 'Paleta en ASE, GPL, JSON y CSV; PDF de paleta y contraste; láminas.'),
           ('04_Tipografia', 'TTF estáticas y variables, licencias OFL, espécimen y guía de instalación.'),
           ('05_Elementos_Graficos', '43 iconos, patrones, 12 fondos, 6 diagramas, componentes dato, dirección fotográfica.'),
           ('06_Presentaciones', 'Plantillas PowerPoint oscura, clara y Tap, deck comercial de ejemplo y previsualizaciones.'),
           ('07_Documentos', 'Plantillas Word A4 (propuesta, informes, factura, contrato…) y PDF de ejemplo.'),
           ('08_Email', '10 plantillas HTML, firmas, guía de redacción y previsualizaciones.'),
           ('09_Redes_Sociales', 'Plantillas y generador de piezas, 71 ejemplos y guía de contenido.'),
           ('10_Papeleria_e_Impresion', 'Tarjetas, membrete, sobre, carpeta, pegatinas, roll-up, cartel, merchandising.'),
           ('11_Web_y_Codigo', 'Tokens CSS/SCSS/JSON/Tailwind, fuentes web y componentes UI.'),
           ('12_Auditoria_y_Mejoras', 'Auditoría de la marca anterior, evidencias y checklist de migración.')]
    rows = ''.join(f'<tr><td class="m" style="font-weight:500;color:var(--tx);width:30%">{a}/</td><td style="font-size:21px">{b}</td></tr>' for a, b in car)
    body = f'<div class="eyebrow">Mapa de carpetas · Identidad_Visual/</div><table class="t mt2">{rows}</table>'
    pg(body, 'claro', toc='Mapa de carpetas')

    body = head('Fuente de verdad', 'Cambia una vez, <span class="az">se actualiza todo</span>')
    body += f"""<div class="g mt3">
      <div class="s6"><ol class="n">
        <li style="margin-top:0"><code>BRAND_SPEC.md</code> y <code>tokens.json</code> definen la marca. Cualquier cambio de color, tipo o regla empieza ahí.</li>
        <li>Los scripts de <code>00_Fuente_Maestra/build/</code> regeneran logos, paleta, fondos, iconos, plantillas y esta guía.</li>
        <li>Nadie edita a mano un PNG o un PDF exportado: se cambia la fuente y se vuelve a exportar.</li>
        <li>Cada cambio se versiona en el repositorio con un commit que explique qué y por qué.</li></ol></div>
      <div class="s6"><div class="card"><div class="kick">Comandos útiles</div>
        <div class="mono" style="font-size:20px;line-height:2;color:var(--tx2)">python build/oryzz_logo.py &nbsp;<span style="color:var(--tx3)"># logos</span><br>python build/export_logos.py<br>python build/paleta_archivos.py<br>python build/pres_build_all.py<br>python build/guia_marca.py &nbsp;<span style="color:var(--tx3)"># esta guía</span><br>python 09_Redes_Sociales/_generador/generar.py</div></div></div>
    </div>"""
    pg(body, 'oscuro', toc='Fuente de verdad')

    fondo = orbitas_fondo(1620, 330, [120, 210, 310, 420], 'oscuro', nodo_en=1, nodo_ang=150)
    body = f"""
    <img src="{uri('02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg')}" style="height:64px;align-self:flex-start;margin-left:-8px">
    <h2 class="big" style="font-size:120px;margin-top:80px">Más clientes.<br><span class="az">No más likes.</span></h2>
    <div class="g mta">
      <div class="s3 rule"><div class="kick g3">Web</div><p>oryzz.com<br>oryzz.com/tap</p></div>
      <div class="s3 rule"><div class="kick g3">Agenda</div><p>cal.com/oryzz/30min</p></div>
      <div class="s3 rule"><div class="kick g3">Redes</div><p>@oryzzai · @oryzztap<br>linkedin.com/company/oryzz</p></div>
      <div class="s3 rule"><div class="kick g3">Versión</div><p>Guía de marca {VERSION}<br>{FECHA}</p></div>
    </div>"""
    pg(body, 'oscuro', 'cover', fondo, pie=False, toc='Contacto y versión')


# ----------------------------------------------------------------- montaje

SCRIPT = """
<script>
// Fotogramas clave del logo animado: congela cada copia en su instante.
document.querySelectorAll('.anim').forEach(function (el) {
  var t = parseFloat(el.dataset.t) * 1000;
  el.getAnimations({subtree: true}).forEach(function (a) { a.pause(); a.currentTime = t; });
});
</script>"""


def construir():
    PAGES.clear(); TOC.clear(); CAP['n'] = ''; CAP['t'] = ''
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    portada()
    como_usar()
    PAGES.append('__INDICE__'); TOC.append((2, 'Índice', len(PAGES)))
    resumen_sistema()
    starts = {}
    for n, fn in [('01', cap_marca), ('02', cap_concepto), ('03', cap_logo), ('04', cap_color), ('05', cap_tipo), ('06', cap_sistema),
                  ('07', cap_foto), ('08', cap_motion), ('09', cap_voz), ('10', cap_aplicaciones), ('11', cap_tap), ('12', cap_check), ('13', cap_archivos)]:
        starts[n] = len(PAGES) + 1
        fn()
    i = PAGES.index('__INDICE__')
    CAP['n'] = ''
    PAGES[i] = (f'<section class="page oscuro"><div class="in">{indice(starts)}</div>'
                f'<footer><img class="fiso" src="{uri("02_Logos/04_Isotipo/SVG_tamano_pequeno/oryzz-isotipo-small_mono-blanco.svg")}"><span>Guía de marca {VERSION}</span><span class="fcap">Oryzz · Guía de marca</span><span class="fnum">{i + 1}</span></footer></section>')
    brand = (MAESTRA / 'brand.css').resolve().as_uri()
    doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Oryzz · Guía de marca {VERSION}</title>'
           f'<link rel="stylesheet" href="{brand}"><style>{CSS}</style></head><body>{"".join(PAGES)}{SCRIPT}</body></html>')
    out = TMP / 'guia.html'
    out.write_text(doc, encoding='utf8')
    return out


CHECK = """
<script>
// Control de calidad: marca las páginas cuyo contenido se sale del área útil (.in) o del lienzo.
window.addEventListener('load', function () { setTimeout(function () {
  var out = [];
  document.querySelectorAll('section.page').forEach(function (pg, i) {
    var inn = pg.querySelector('.in'); if (!inn) return;
    var b = inn.getBoundingClientRect(), worst = 0, culprit = '';
    inn.querySelectorAll('*').forEach(function (el) {
      if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
      var r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
      var d = Math.max(r.bottom - b.bottom, r.right - b.right);
      if (d > worst) { worst = d; culprit = el.tagName + '.' + el.className + ' ' + (el.textContent || '').trim().slice(0, 40); }
    });
    if (worst > 2) out.push((i + 1) + ': +' + Math.round(worst) + 'px · ' + culprit);
  });
  var d = document.createElement('pre'); d.id = 'qa-desbordes'; d.textContent = out.join('\\n') || 'OK';
  document.body.appendChild(d);
}, 300); });
</script>"""


def comprobar_desbordes(html_path):
    """Abre el HTML en Chrome headless y devuelve las páginas con contenido fuera del área útil."""
    import subprocess
    from render import CHROME
    doc = pathlib.Path(html_path).read_text(encoding='utf8').replace('</body>', CHECK + '</body>')
    qa = pathlib.Path(html_path).with_name('guia_qa.html')
    qa.write_text(doc, encoding='utf8')
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--window-size=1920,1080',
                        '--virtual-time-budget=6000', '--dump-dom', _url(str(qa))], capture_output=True, timeout=180)
    m = re.search(r'<pre id="qa-desbordes">(.*?)</pre>', r.stdout.decode('utf8', 'replace'), re.S)
    return html.unescape(m.group(1)) if m else 'sin resultado'


def poner_marcadores(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    toc = [[lvl, t, p] for lvl, t, p in TOC if p <= doc.page_count]
    # el primer nivel debe empezar en 1 y no saltar niveles
    doc.set_toc(toc)
    doc.set_metadata({'title': f'Oryzz · Guía de marca {VERSION}', 'author': 'Oryzz', 'subject': 'Identidad visual y verbal de Oryzz y Oryzz Tap',
                      'keywords': 'Oryzz, Oryzz Tap, guía de marca, identidad visual', 'creator': 'guia_marca.py', 'producer': 'Oryzz'})
    tmp = str(pdf_path) + '.tmp'
    doc.save(tmp, garbage=4, deflate=True)
    doc.close()
    os.replace(tmp, pdf_path)


def exportar_png(pdf_path, carpeta, ancho=1280):
    import fitz
    carpeta.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    for i, p in enumerate(doc):
        z = ancho / p.rect.width
        p.get_pixmap(matrix=fitz.Matrix(z, z)).save(carpeta / f'p{i + 1:03d}.png')
    return doc.page_count


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--html', action='store_true', help='solo genera el HTML')
    ap.add_argument('--png', metavar='CARPETA', help='exporta cada página a PNG en CARPETA (revisión)')
    a = ap.parse_args()
    h = construir()
    print('HTML:', h, '·', len(PAGES), 'páginas')
    print('Desbordes:', comprobar_desbordes(h))
    if a.html:
        sys.exit()
    SALIDA.mkdir(exist_ok=True)
    html_to_pdf(str(h), str(PDF))
    poner_marcadores(PDF)
    print('PDF:', PDF, f'({PDF.stat().st_size / 1e6:.1f} MB)')
    if a.png:
        print('PNG:', exportar_png(PDF, pathlib.Path(a.png)))
