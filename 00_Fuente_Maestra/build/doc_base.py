"""
Base común para documentos A4 apaisados de Oryzz generados en HTML → PDF (Chrome).
Proporciona el CSS de marca (@font-face con rutas absolutas), la retícula y helpers.

    from doc_base import CSS_BASE, page, logo, fmt
"""
import os, pathlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
FONTS = pathlib.Path(os.path.join(HERE, '..', 'fonts', 'static')).resolve().as_uri()
LOGOS = pathlib.Path(os.path.join(ROOT, '02_Logos')).resolve().as_uri()


def logo(kind='horizontal', way='color-sobre-oscuro'):
    m = {
        'horizontal': f'01_Horizontal/SVG/oryzz-logo-horizontal_{way}.svg',
        'vertical': f'02_Vertical/SVG/oryzz-logo-vertical_{way}.svg',
        'wordmark': f'03_Wordmark/SVG/oryzz-wordmark_{way}.svg',
        'isotipo': f'04_Isotipo/SVG/oryzz-isotipo_{way}.svg',
        'tap': f'07_Submarca_Tap/SVG/oryzz-tap-horizontal_{way}.svg',
        'favicon': '06_Favicon/favicon.svg',
    }
    return f'{LOGOS}/{m[kind]}'


def fmt(x, d=2):
    """Número con coma decimal española."""
    return f'{x:.{d}f}'.replace('.', ',')


_FF = [('Space Grotesk', w, f) for w, f in [(400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold')]] + \
      [('Manrope', w, f) for w, f in [(400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold')]] + \
      [('JetBrains Mono', w, f) for w, f in [(400, 'Regular'), (500, 'Medium'), (700, 'Bold')]]
_FILE = {'Space Grotesk': 'SpaceGrotesk', 'Manrope': 'Manrope', 'JetBrains Mono': 'JetBrainsMono'}
FONT_FACES = '\n'.join(
    f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;src:url('{FONTS}/{_FILE[fam]}-{f}.ttf') format('truetype')}}"
    for fam, w, f in _FF)

CSS_BASE = FONT_FACES + """
:root{
 --g950:#0B0D12;--g900:#0E1118;--g850:#12151D;--g800:#171B25;--g700:#232836;--g600:#3A4152;--g500:#5A6172;
 --g400:#8A90A0;--g300:#C7CBD6;--g200:#D5D9E0;--g100:#E5E8EE;--g50:#F6F7F9;--w:#FFFFFF;
 --a300:#9FB8FF;--a400:#5C8BFF;--a500:#3B72FF;--a600:#2C5BD0;--a50:#EEF3FF;
 --c500:#36CFE0;--c600:#17A9C2;--l500:#BFF24A;--l600:#7FB02E;--l900:#3A4A12;
 --ok:#1F9D55;--warn:#F2A33A;--err:#E5484D;
 --grad-d:linear-gradient(135deg,#5C8BFF 0%,#36CFE0 100%);--grad-l:linear-gradient(135deg,#3B72FF 0%,#17A9C2 100%);
 --fd:'Space Grotesk',Arial,sans-serif;--ft:'Manrope',Arial,sans-serif;--fm:'JetBrains Mono',Consolas,monospace;
}
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:var(--ft);color:var(--g950);-webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:9.5pt;line-height:1.5}
.page{width:297mm;height:210mm;position:relative;overflow:hidden;page-break-after:always;break-after:page;padding:16mm 18mm 16mm 18mm;background:#fff}
.page:last-child{page-break-after:auto;break-after:auto}
.dark{background:var(--g950);color:#fff}
.soft{background:var(--g50)}
.eyebrow{font-family:var(--fm);font-size:7.5pt;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--g500)}
.dark .eyebrow{color:var(--g400)}
.eyebrow .n{color:var(--a600)} .dark .eyebrow .n{color:var(--l500)}
h1,h2,h3,h4{font-family:var(--fd);font-weight:700;letter-spacing:-.03em;line-height:1.05}
h1{font-size:44pt;letter-spacing:-.045em;line-height:.98}
h2{font-size:24pt}
h3{font-size:13pt;font-weight:600;letter-spacing:-.015em;line-height:1.2}
h4{font-size:10pt;font-weight:600;letter-spacing:-.01em}
p{max-width:120mm}
.lead{font-size:11.5pt;line-height:1.5;color:var(--g600)} .dark .lead{color:var(--g200)}
.muted{color:var(--g500)} .dark .muted{color:var(--g400)}
.mono{font-family:var(--fm)}
.hl{color:var(--a600)} .dark .hl{color:var(--a400)}
.folio{position:absolute;left:18mm;right:18mm;bottom:8mm;display:flex;justify-content:space-between;font-family:var(--fm);font-size:6.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--g400)}
.dark .folio{color:var(--g500)}
.folio img{height:3.4mm}
.grid{display:grid;grid-template-columns:repeat(12,1fr);column-gap:5mm}
.rule{height:1px;background:var(--g200);margin:5mm 0} .dark .rule{background:var(--g700)}
table{border-collapse:collapse;width:100%}
.tag{display:inline-block;font-family:var(--fm);font-size:6.5pt;font-weight:500;letter-spacing:.08em;text-transform:uppercase;padding:.6mm 1.8mm;border-radius:999px;border:1px solid currentColor;white-space:nowrap}
"""


def folio(texto, n, dark=False):
    way = 'mono-blanco' if dark else 'mono-grafito'
    return (f'<div class="folio"><span><img src="{logo("wordmark", way)}" alt="oryzz" style="vertical-align:middle;opacity:.8"></span>'
            f'<span>{texto}</span><span>{n:02d}</span></div>')


def html_doc(title, body, extra_css=''):
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{title}</title><style>{CSS_BASE}{extra_css}</style></head><body>{body}</body></html>'
