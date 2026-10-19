"""
Hoja de contacto de 02_Logos (A4 apaisado, varias páginas): todas las versiones sobre su fondo correcto
con su nombre de archivo.   Uso:  python hoja_contacto.py
"""
import os, sys, pathlib, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oryzz_logo as L
from render import html_to_pdf

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '02_Logos'))
CSS = pathlib.Path(os.path.join(HERE, '..', 'brand.css')).resolve().as_uri()
OUT = os.path.join(ROOT, 'Oryzz_Logos_Hoja_de_Contacto.pdf')
ORDER = ['color-sobre-oscuro', 'color-sobre-claro', 'solido-sobre-oscuro', 'solido-sobre-claro', 'sobre-azul',
         'sobre-lima', 'mono-blanco', 'mono-grafito', 'mono-negro', 'mono-azul']


def uri(rel):
    return pathlib.Path(os.path.join(ROOT, rel)).resolve().as_uri()


def wbr(name):
    return name.replace('_', '_<wbr>').replace('-', '-<wbr>')


def tile(rel, bg, label, img_style='', cls=''):
    border = ' bordered' if bg.upper() in ('#FFFFFF', '#F6F7F9') else ''
    fn = os.path.basename(rel)
    return (f'<figure class="tile{border} {cls}"><div class="plate" style="background:{bg}">'
            f'<img src="{uri(rel)}" style="{img_style}" alt=""></div>'
            f'<figcaption><span class="cw">{label}</span><span class="fn">{wbr(fn)}</span></figcaption></figure>')


def page(n, total, eyebrow, title, body, note=''):
    return (f'<section class="page"><header><div><div class="eyebrow">{eyebrow}</div><h1>{title}</h1></div>'
            f'<div class="note">{note}</div></header><div class="body">{body}</div>'
            f'<footer><span>Sistema de logo de Oryzz v2.0 · Hoja de contacto</span><span>{n} / {total}</span></footer></section>')


def family(folder, prefix, cols, img_style):
    t = ''
    for w in ORDER:
        t += tile(f'{folder}/{prefix}_{w}.svg', L.WAYS[w]['bg'], w, img_style)
    return f'<div class="grid" style="grid-template-columns:repeat({cols},1fr)">{t}</div>'


def build():
    pages = []
    # portada
    cover = (f'<div class="cover"><img class="cover-logo" src="{uri("01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg")}" alt="oryzz">'
             '<div class="cover-copy"><div class="eyebrow">Logos de Oryzz · v2.0 · 2026</div>'
             '<h1 class="big">Hoja de contacto</h1>'
             '<p>Todas las versiones del logo sobre su fondo correcto, con el nombre de archivo exacto. '
             'Los maestros están en <b>SVG</b>; cada carpeta incluye <b>PNG</b> transparentes y <b>PDF</b> vectoriales para imprenta.</p>'
             '<ol class="idx"><li>Horizontal <i>principal</i></li><li>Vertical</li><li>Wordmark</li><li>Isotipo e isotipo pequeño</li>'
             '<li>Submarca Oryzz Tap</li><li>Avatares, redes y favicon</li><li>Animado y láminas de uso</li></ol></div></div>')
    pages.append(('', '', cover, ''))
    pages.append(('Horizontal', 'Logo horizontal', family('01_Horizontal/SVG', 'oryzz-logo-horizontal', 3, 'width:74%'),
                  'Versión principal · <b>color-sobre-oscuro</b>'))
    pages.append(('Vertical', 'Logo vertical', family('02_Vertical/SVG', 'oryzz-logo-vertical', 5, 'width:58%'),
                  'Para formatos cuadrados y verticales'))
    pages.append(('Wordmark', 'Wordmark', family('03_Wordmark/SVG', 'oryzz-wordmark', 3, 'width:60%'),
                  'Solo cuando el isotipo ya está presente en la pieza'))
    iso = ''
    for w in ORDER:
        iso += tile(f'04_Isotipo/SVG/oryzz-isotipo_{w}.svg', L.WAYS[w]['bg'], w, 'width:38%', 'sq')
    for w in ORDER:
        iso += tile(f'04_Isotipo/SVG_tamano_pequeno/oryzz-isotipo-small_{w}.svg', L.WAYS[w]['bg'], w + ' · small', 'width:24%', 'sq small')
    pages.append(('Isotipo', 'Isotipo e isotipo pequeño', f'<div class="grid iso" style="grid-template-columns:repeat(10,1fr)">{iso}</div>',
                  'Fila inferior: <b>isotipo-small</b>, para ≤ 24 px'))
    pages.append(('Submarca', 'Oryzz Tap', family('07_Submarca_Tap/SVG', 'oryzz-tap-horizontal', 3, 'width:80%'),
                  'Expresión principal en claro · <b>color-sobre-claro</b>'))
    av = ''
    for shape in ('cuadrado', 'circulo'):
        for w in ['color-sobre-oscuro', 'color-sobre-claro', 'sobre-azul', 'sobre-lima', 'mono-blanco']:
            av += tile(f'05_Avatar_Perfil/SVG/oryzz-avatar-{shape}_{w}.svg', '#E5E8EE', f'{shape} · {w}', 'width:46%', 'sq')
    redes = ''
    for n in ['oryzz-avatar-redes_color-sobre-oscuro', 'oryzz-avatar-redes_sobre-azul', 'oryzz-tap-avatar-redes_color-sobre-claro', 'oryzz-tap-avatar-redes_color-sobre-blanco']:
        redes += tile(f'05_Avatar_Perfil/PNG_redes/{n}_1080.png', '#E5E8EE', 'redes · 1080 / 400 px', 'width:46%;border-radius:50%', 'sq')
    fav = ''
    for n, lab in [('favicon.svg', 'favicon.svg / .ico'), ('apple-touch-icon-180.png', 'iOS · 180 px'), ('android-chrome-512.png', 'Android · 192 / 512'),
                   ('maskable-512.png', 'PWA maskable · 512')]:
        fav += tile(f'06_Favicon/{n}', '#E5E8EE', lab, 'width:46%', 'sq')
    pages.append(('Avatares y favicon', 'Avatares, redes y favicon',
                  f'<div class="grid" style="grid-template-columns:repeat(10,1fr)">{av}</div>'
                  f'<div class="grid" style="grid-template-columns:repeat(8,1fr);margin-top:5mm">{redes}{fav}</div>',
                  'Redes: fondo a sangre, recorte circular seguro'))
    an = (f'<div class="grid" style="grid-template-columns:1.4fr 1fr 1fr">'
          + tile('08_Animado/oryzz-logo-intro_poster_800x300.png', '#0B0D12', 'intro · SVG + GIF 800×300', 'width:92%')
          + tile('08_Animado/oryzz-loader.svg', '#0B0D12', 'loader · sobre oscuro', 'width:30%')
          + tile('08_Animado/oryzz-loader_sobre-claro.svg', '#FFFFFF', 'loader · sobre claro', 'width:30%')
          + '</div><div class="grid" style="grid-template-columns:repeat(4,1fr);margin-top:5mm">')
    for n in ['01_construccion-isotipo', '02_area-de-respeto', '03_tamanos-minimos', '04_usos-incorrectos']:
        an += tile(f'09_Construccion_y_Uso/PNG/oryzz-{n}_oscuro.png', '#0B0D12', 'lámina · oscuro / claro', 'width:100%', 'sheet')
    an += '</div>'
    pages.append(('Animado y uso', 'Animado y láminas de uso', an, 'Movimiento: solo en intros, loaders y cierres'))

    total = len(pages)
    body = ''.join(page(i + 1, total, e, t, b, n) if e else f'<section class="page cover-page">{b}<footer><span>Sistema de logo de Oryzz v2.0</span><span>1 / {total}</span></footer></section>'
                   for i, (e, t, b, n) in enumerate(pages))
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Oryzz · Hoja de contacto de logos</title>
<link rel="stylesheet" href="{CSS}"><style>
@page{{size:297mm 210mm;margin:0}}
*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
html,body{{margin:0;padding:0;background:#F6F7F9;font-family:var(--font-texto);color:#0B0D12}}
.page{{width:297mm;height:210mm;padding:13mm 16mm 0;position:relative;overflow:hidden;break-after:page;display:flex;flex-direction:column;background:#F6F7F9}}
header{{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:5mm;border-bottom:.25mm solid #D5D9E0;margin-bottom:6mm}}
.eyebrow{{font-family:var(--font-texto);font-size:10pt;font-weight:600;letter-spacing:0;color:#5A6172}}
h1{{font-family:var(--font-display);font-weight:700;font-size:24pt;letter-spacing:-.03em;margin:2mm 0 0;line-height:1}}
.note{{font-family:var(--font-texto);font-size:9.5pt;color:#5A6172}} .note b{{color:#0B0D12;font-weight:600}}
.body{{flex:1}}
.grid{{display:grid;gap:3.5mm 4mm}}
.tile{{margin:0}}
.plate{{height:22mm;border-radius:2.5mm;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.grid[style*="repeat(5"] .plate{{height:52mm}}
.tile.sq .plate{{height:auto;aspect-ratio:1/1}}
.tile.sheet .plate{{height:auto;aspect-ratio:16/10}}
.tile.bordered .plate{{box-shadow:inset 0 0 0 .25mm #D5D9E0}}
.plate img{{display:block;max-height:78%}}
figcaption{{margin-top:1.6mm;display:flex;flex-direction:column;gap:.4mm}}
.cw{{font-family:var(--font-mono);font-size:9pt;font-weight:500;color:#0B0D12}}
.fn{{font-family:var(--font-mono);font-size:9pt;color:#5A6172;line-height:1.25}}
.grid.iso{{gap:3mm 2.6mm}} .grid.iso .fn, .grid[style*="repeat(10"] .fn, .grid[style*="repeat(8"] .fn{{display:none}}
.grid[style*="repeat(10"] .cw, .grid[style*="repeat(8"] .cw{{font-size:9pt;line-height:1.2;overflow-wrap:anywhere}}
footer{{position:absolute;left:16mm;right:16mm;bottom:8mm;display:flex;justify-content:space-between;font-family:var(--font-texto);font-weight:500;font-size:9pt;color:#5A6172;border-top:.25mm solid #D5D9E0;padding-top:3mm}}
.cover-page{{background:#0B0D12;color:#fff;padding:0}}
.cover-page footer{{color:#8A90A0;border-color:#232836}}
.cover{{display:grid;grid-template-columns:1.25fr 1fr;height:100%;align-items:center;padding:0 16mm 20mm}}
.cover-logo{{width:128mm;display:block}}
.cover-copy .eyebrow{{color:#8A90A0}}
h1.big{{font-size:40pt;margin:4mm 0 6mm}}
.cover-copy p{{font-size:11pt;line-height:1.55;color:#D5D9E0;max-width:92mm;margin:0 0 7mm}} .cover-copy b{{color:#fff;font-weight:600}}
.idx{{margin:0;padding:0;list-style:none;font-family:var(--font-texto);font-weight:600;font-size:10pt;color:#D5D9E0;border-top:.25mm solid #232836}}
.idx li{{display:flex;align-items:center;gap:2.5mm;padding:2mm 0;border-bottom:.25mm solid #232836}}
.idx li::before{{content:"";width:1.6mm;height:1.6mm;border-radius:50%;border:.3mm solid #5C8BFF;flex:none}}
.idx i{{font-style:normal;color:#BFF24A;margin-left:2mm}}
</style></head><body>{body}</body></html>"""
    tmp = os.path.join(tempfile.mkdtemp(prefix='oryzz_hc_'), 'hoja.html')
    open(tmp, 'w', encoding='utf8').write(html)
    html_to_pdf(tmp, OUT)
    print('ok', OUT)


if __name__ == '__main__':
    build()
