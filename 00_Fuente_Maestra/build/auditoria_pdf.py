"""
Genera 12_Auditoria_y_Mejoras/Oryzz_Auditoria_de_Marca.pdf (A4 apaisado) y Auditoria_de_Marca.md
a partir de auditoria_datos.py. Evidencias en 12_Auditoria_y_Mejoras/evidencias/.

Uso:  python auditoria_pdf.py
"""
import html, os, pathlib, re, tempfile
from auditoria_datos import FECHA, RESUMEN, CIFRAS, PUNTUACION, HALLAZGOS, FASES, CANALES, MATRIZ_PLAN, CHECKLIST
from doc_base import html_doc, folio, logo, ROOT
from render import html_to_pdf

OUT = os.path.join(ROOT, '12_Auditoria_y_Mejoras')
EV = os.path.join(OUT, 'evidencias')
EVU = pathlib.Path(EV).resolve().as_uri()
TMP = os.path.join(tempfile.gettempdir(), 'oryzz_auditoria'); os.makedirs(TMP, exist_ok=True)
H = {h['id']: h for h in HALLAZGOS}
PRIO_COLOR = {'Crítico': '#E5484D', 'Alto': '#F2A33A', 'Medio': '#3B72FF', 'Bajo': '#8A90A0'}
TXT = 'Auditoría de marca · 2026'


def md(s):
    """Markdown mínimo (`code`, **negrita**) → HTML."""
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    return s


def tag(prio):
    return f'<span class="prio"><i style="background:{PRIO_COLOR[prio]}"></i>{prio}</span>'


CSS = """
code{font-family:var(--fm);font-size:.86em;background:var(--g100);padding:.1mm 1mm;border-radius:1mm;color:var(--g950);word-break:break-word}
.dark code{background:var(--g800);color:var(--g200)}
.prio{display:inline-flex;align-items:center;gap:1.6mm;font-family:var(--ft);font-size:9pt;font-weight:600;border:1px solid var(--g300);border-radius:999px;padding:.8mm 2.6mm .8mm 2mm;color:var(--g950)}
.dark .prio{color:#fff;border-color:var(--g600)}
.prio i{width:2.2mm;height:2.2mm;border-radius:50%;display:inline-block}
.hid{font-family:var(--ft);font-size:9pt;font-weight:600;color:var(--g500)}
.ev li,.fx li{font-size:9pt;line-height:1.45;margin:0 0 1.6mm 3.6mm}
.ev li::marker{color:var(--g400)}
.lbl{font-family:var(--ft);font-size:9pt;font-weight:600;color:var(--g500);margin:4mm 0 1.6mm}
.imp{font-size:9pt;line-height:1.45;color:var(--g950);border-left:2px solid var(--a600);padding-left:3mm}
.fx{background:var(--g950);color:#E5E8EE;border-radius:3mm;padding:4mm 5mm 2.4mm}
.fx .lbl{color:var(--l500);margin-top:0}
.fx code{background:#232836;color:#fff}
.fx li::marker{color:var(--l500)}
.shot{border-radius:2.5mm;overflow:hidden;border:1px solid var(--g200);background:var(--g50);display:flex;align-items:center;justify-content:center}
.shot img{display:block;max-width:100%;max-height:100%;object-fit:contain}
.cap{font-family:var(--ft);font-size:9pt;font-weight:500;color:var(--g500);margin-top:1.2mm}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:9mm;margin-top:5mm}
.pair>div{min-width:0}
.pair h3{margin-top:2.2mm}
.kpi{border-top:1px solid var(--g700);padding-top:3mm}
.kpi b{display:block;font-family:var(--fd);font-weight:500;font-size:26pt;letter-spacing:-.03em;color:#fff;line-height:1}
.kpi span{display:block;font-size:9pt;color:var(--g400);margin-top:2mm;line-height:1.35}
.bar{height:3.2mm;background:var(--g100);border-radius:999px;overflow:hidden}
.bar i{display:block;height:100%;border-radius:999px}
table.t{font-size:9pt}
table.t th{font-family:var(--ft);font-size:9pt;font-weight:600;color:var(--g500);text-align:left;border-bottom:1px solid var(--g300);padding:1.4mm 2mm}
table.t td{border-bottom:1px solid var(--g100);padding:1.5mm 2mm;vertical-align:top;line-height:1.35}
table.compacta td{padding:1.05mm 2mm;line-height:1.3}
.fase{border:1px solid var(--g200);border-radius:3mm;padding:3.5mm;background:#fff}
.fase h4{margin-top:1.5mm}
.fase ul{margin-top:2mm}
.fase li{font-size:9pt;line-height:1.4;margin:0 0 1.3mm 3mm}
.chk{columns:3;column-gap:8mm;margin-top:5mm}
.chk section{break-inside:avoid;margin-bottom:4mm}
.chk h4{font-size:9pt;margin-bottom:1.8mm}
.chk label{display:flex;gap:2mm;font-size:9pt;line-height:1.35;margin-bottom:1.5mm}
.chk label i{flex:0 0 3.2mm;height:3.2mm;border:1px solid var(--g500);border-radius:.8mm;margin-top:.3mm}
"""


def lista(items, cls='ev'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{md(x)}</li>' for x in items) + '</ul>'


def shot(name, h, cap=None):
    c = f'<div class="cap">{cap}</div>' if cap else ''
    return f'<div><div class="shot" style="height:{h}mm"><img src="{EVU}/{name}"></div>{c}</div>'


def pagina(body, n, cls=''):
    return f'<section class="page {cls}">{body}{folio(TXT, n, cls == "dark")}</section>'


def cabecera(h):
    return (f'<div style="display:flex;align-items:center;gap:4mm"><span class="hid">Hallazgo · {h["id"]} · {h["area"]}</span>{tag(h["prio"])}</div>'
            f'<h2 style="margin-top:3mm;max-width:200mm">{md(h["titulo"])}</h2>')


def cuerpo(h):
    return (f'<div class="lbl">Evidencia</div>{lista(h["evidencia"])}'
            f'<div class="lbl">Impacto</div><p class="imp">{md(h["impacto"])}</p>')


def fix(h):
    return f'<div class="fx"><div class="lbl">Corrección</div>{lista(h["correccion"], "")}</div>'


CAPS = {
    'ev01_home_cabecera.png': 'oryzz.com · cabecera publicada (29-09-2026)',
    'ev02_tap_cabecera.png': 'oryzz.com/tap · barra de anuncios y cabecera',
    'ev03_home_hero.png': 'oryzz.com · hero: dos halos difusos animados y retícula',
    'ev04_home_cta.png': 'CTA actual: blanco sobre #3B72FF → #36CFE0 (4,17 → 1,88:1)',
    'ev05_home_problema_iconos.png': 'Tarjetas «El problema»: icono de Instagram a color y fondo rojo',
    'ev06_home_servicios_iconos.png': 'Servicios: Meta, Google y TikTok con sus colores',
    'ev08_tap_iconos_color.png': '/tap: iconografía multicolor y «MyOryzz»',
    'ev09_tap_producto_logo_antiguo.png': 'Placas y stands con el lockup antiguo',
    'ev10_tap_banner_cookies.png': 'Banner de cookies de la home dentro de /tap',
    'ev11_home_titular_gradiente.png': 'FAQ: línea entera en gradiente',
    'ev12_home_footer.png': 'Footer: «Empresa», «Síguenos» y © en #5A6172 (3,14:1)',
    'ev14_home_nosotros.png': '«Resultados en 3–7 días» frente a «sin promesas»',
    'ev18_home_pagina_completa.png': 'Home completa: 5 de 7 secciones centradas',
    'ev19_og_image_actual.png': 'og-image.png actual (1200×630)',
    'ev20_nodo_una_tinta.png': 'Una tinta · actual (grande y 20 px) frente a v2 (grande y 20 px)',
    'ev21_logo_tap_antiguo.png': 'Logo actual de /tap: órbita dibujada + 5 estrellas',
}


def build():
    pages = []; n = 1
    # 1 · Portada
    pages.append(f'''<section class="page dark" style="padding:18mm">
      <img src="{logo('horizontal','color-sobre-oscuro')}" style="height:9mm">
      <div style="position:absolute;left:18mm;bottom:34mm;width:170mm">
        <div class="eyebrow">Auditoría y mejoras · {FECHA}</div>
        <h1 style="margin-top:6mm;font-size:52pt">Auditoría<br>de marca.</h1>
        <p class="lead" style="margin-top:6mm;max-width:130mm">Estado de la identidad de Oryzz en oryzz.com, oryzz.com/tap, documentos y producto. Hallazgos priorizados con evidencia, impacto y corrección exacta, y el plan para migrar al sistema v2.</p>
      </div>
      <svg style="position:absolute;right:-40mm;top:-30mm;width:190mm;height:190mm" viewBox="0 0 100 100" fill="none">
        <path d="M35.58 19.2A34 34 0 1 0 72.1 24.4" stroke="#232836" stroke-width=".35"/>
        <path d="M31.4 9.6A44 44 0 1 0 78.5 16.3" stroke="#171B25" stroke-width=".35"/>
        <circle cx="64.4" cy="19.2" r="1.6" fill="#BFF24A"/></svg>
      <div class="folio" style="color:#5A6172"><span>Confidencial · uso interno</span><span>oryzz.com</span><span>1</span></div></section>''')
    n += 1
    # 2 · Resumen
    kpis = ''.join(f'<div class="kpi"><b>{v}</b><span>{t}</span></div>' for v, t in CIFRAS)
    pages.append(pagina(f'''<div class="grid"><div style="grid-column:1/5"><div class="eyebrow">Resumen ejecutivo</div>
      <h2 style="margin-top:4mm">Una buena idea<br>con tres caras.</h2>
      <p class="lead" style="margin-top:4mm">Nota global <b style="color:#fff">4,3 / 10</b>. La plataforma es sólida; la ejecución visual está fragmentada y suspende en accesibilidad justo en el botón que convierte.</p></div>
      <div style="grid-column:6/13">{''.join(f'<p style="font-size:9pt;line-height:1.5;color:#D5D9E0;margin-bottom:3mm;max-width:none">{md(p)}</p>' for p in RESUMEN)}</div></div>
      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6mm;position:absolute;left:18mm;right:18mm;bottom:20mm">{kpis}</div>''', n, 'dark')); n += 1
    # 3 · Puntuación
    filas = ''.join(f'''<tr><td style="width:48mm;font-weight:600">{a}</td><td style="width:70mm"><div class="bar"><i style="width:{s * 10}%;background:{'#2C5BD0' if s >= 6 else ('#F2A33A' if s >= 4 else '#E5484D')}"></i></div></td>
      <td style="width:14mm;font-family:var(--fd);font-weight:600;font-size:10pt">{s}</td><td class="muted">{d}</td></tr>''' for a, s, d in PUNTUACION)
    pages.append(pagina(f'''<div class="grid"><div style="grid-column:1/4"><div class="eyebrow">Puntuación</div><h2 style="margin-top:4mm">Diez áreas,<br>de 0 a 10.</h2>
      <p class="muted" style="margin-top:3mm">Criterio de estudio: 10 = sistema coherente, accesible y reconocible en todos los canales. 5 = funciona pero no escala. &lt; 4 = daña la marca.</p>
      <div style="margin-top:8mm;display:flex;flex-direction:column;gap:2mm;font-size:9pt">
        <span><i style="display:inline-block;width:3mm;height:3mm;border-radius:50%;background:#2C5BD0;vertical-align:-.4mm;margin-right:2mm"></i>≥ 6 · mantener</span>
        <span><i style="display:inline-block;width:3mm;height:3mm;border-radius:50%;background:#F2A33A;vertical-align:-.4mm;margin-right:2mm"></i>4–5 · corregir</span>
        <span><i style="display:inline-block;width:3mm;height:3mm;border-radius:50%;background:#E5484D;vertical-align:-.4mm;margin-right:2mm"></i>≤ 3 · rehacer</span></div></div>
      <div style="grid-column:4/13"><table class="t"><tr><th>Área</th><th>Estado</th><th>Nota</th><th>Por qué</th></tr>{filas}
      <tr><td style="font-weight:700;border-bottom:0;padding-top:3mm">Media</td><td style="border-bottom:0"></td><td style="font-family:var(--fd);font-weight:700;font-size:12pt;border-bottom:0;padding-top:2.4mm">4,3</td><td style="border-bottom:0"></td></tr></table></div></div>''', n)); n += 1
    # 4 · Mapa de hallazgos
    def fila(h):
        return (f'<tr><td style="width:10mm;font-family:var(--fm);font-weight:700">{h["id"]}</td><td style="width:22mm">{tag(h["prio"])}</td>'
                f'<td><b style="font-weight:600">{md(h["titulo"])}</b><br><span class="muted">{h["area"]}</span></td></tr>')
    mitad = (len(HALLAZGOS) + 1) // 2
    tabla = lambda hs: '<table class="t"><tr><th>ID</th><th>Prioridad</th><th>Hallazgo · área</th></tr>' + ''.join(fila(h) for h in hs) + '</table>'
    filas = f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm">{tabla(HALLAZGOS[:mitad])}{tabla(HALLAZGOS[mitad:])}</div>'
    cnt = {p: sum(1 for h in HALLAZGOS if h['prio'] == p) for p in PRIO_COLOR}
    pages.append(pagina(f'''<div class="grid"><div style="grid-column:1/4"><div class="eyebrow">Hallazgos priorizados</div><h2 style="margin-top:4mm">{len(HALLAZGOS)} hallazgos.</h2>
      <p class="muted" style="margin-top:3mm">{cnt['Crítico']} críticos, {cnt['Alto']} altos, {cnt['Medio']} medios y {cnt['Bajo']} bajos. Crítico: daña conversión o reconocimiento hoy. Alto: afecta a todos los canales. Medio: percepción y credibilidad. Bajo: mantenimiento.</p>
      <p class="muted" style="margin-top:3mm">Evidencia recogida el 29-09-2026 sobre la web publicada (estilos computados en Chrome) y el código de <code>TAP/OryzzTAP/oryzz/</code>.</p></div>
      <div style="grid-column:4/13">{filas}</div></div>''', n)); n += 1

    # --- páginas de hallazgo
    def full(hid, imgs, heights=None, layout='derecha'):
        h = H[hid]
        heights = heights or [60] * len(imgs)
        ims = ''.join(shot(i, hh, CAPS.get(i)) for i, hh in zip(imgs, heights))
        return f'''{cabecera(h)}<div class="grid" style="margin-top:4mm"><div style="grid-column:1/6">{cuerpo(h)}</div>
          <div style="grid-column:6/13;display:flex;flex-direction:column;gap:4mm">{ims}{fix(h)}</div></div>'''

    def pair(a, b, ia=None, ib=None, hh=38):
        def col(hid, img):
            h = H[hid]
            im = shot(img, hh, CAPS.get(img)) if img else ''
            return f'''<div><div style="display:flex;align-items:center;gap:3mm"><span class="hid">{h["id"]} · {h["area"]}</span>{tag(h["prio"])}</div>
              <h3>{md(h["titulo"])}</h3>{('<div style="margin-top:3mm">' + im + '</div>') if im else ''}{cuerpo(h)}<div style="margin-top:3mm">{fix(h)}</div></div>'''
        return f'<div class="eyebrow">Hallazgos · {a} y {b}</div><div class="pair">{col(a, ia)}{col(b, ib)}</div>'

    # C1 con tabla comparativa
    h = H['C1']
    comp = '''<table class="t" style="margin-top:1mm"><tr><th></th><th>oryzz.com</th><th>oryzz.com/tap</th><th>Documentos</th><th>v2</th></tr>
      <tr><td class="muted">Titulares</td><td>Space Grotesk</td><td>Syne</td><td>Montserrat</td><td><b>Space Grotesk</b></td></tr>
      <tr><td class="muted">Texto</td><td>Manrope</td><td>Outfit</td><td>Montserrat</td><td><b>Manrope</b></td></tr>
      <tr><td class="muted">Azul</td><td><code>#3B72FF</code></td><td><code>#0075FF</code></td><td><code>#5C8BFF</code></td><td><b><code>#3B72FF</code> · <code>#2C5BD0</code></b></td></tr>
      <tr><td class="muted">Lima</td><td><code>#BFF24A</code></td><td><code>#C5F500</code></td><td><code>#BFF24A</code></td><td><b><code>#BFF24A</code></b></td></tr>
      <tr><td class="muted">Fondo</td><td><code>#0B0D12</code></td><td><code>#EEF2F6</code></td><td><code>#0A0E1A</code></td><td><b><code>#0B0D12</code> · <code>#FFFFFF</code></b></td></tr>
      <tr><td class="muted">Logo</td><td>texto vivo</td><td>órbita + estrellas</td><td>PNG</td><td><b>SVG v2</b></td></tr></table>'''
    pages.append(pagina(f'''{cabecera(h)}<div class="grid" style="margin-top:4mm"><div style="grid-column:1/6">{cuerpo(h)}</div>
      <div style="grid-column:6/13;display:flex;flex-direction:column;gap:3mm">{shot('ev01_home_cabecera.png', 11, CAPS['ev01_home_cabecera.png'])}{shot('ev02_tap_cabecera.png', 14, CAPS['ev02_tap_cabecera.png'])}{comp}{fix(h)}</div></div>''', n)); n += 1
    pages.append(pagina(full('C2', ['ev04_home_cta.png'], [34]) + '''<div style="position:absolute;right:18mm;bottom:16mm;display:flex;gap:4mm">
      <div style="background:#0B0D12;border-radius:2.5mm;padding:3.5mm 4mm;display:flex;align-items:center;gap:3mm"><span style="display:inline-flex;height:9mm;align-items:center;padding:0 5mm;border-radius:2.5mm;background:linear-gradient(135deg,#5C8BFF,#36CFE0);color:#0B0D12;font:600 9.5pt 'Space Grotesk'">Agendar valoración</span><span class="mono" style="font-size:9pt;color:#D5D9E0">6,10–10,33:1</span></div>
      <div style="background:#fff;border:1px solid #E5E8EE;border-radius:2.5mm;padding:3.5mm 4mm;display:flex;align-items:center;gap:3mm"><span style="display:inline-flex;height:9mm;align-items:center;padding:0 5mm;border-radius:2.5mm;background:#2C5BD0;color:#fff;font:600 9.5pt 'Space Grotesk'">Elegir el mío</span><span class="mono" style="font-size:9pt;color:#3A4152">5,98:1</span></div></div>''', n)); n += 1
    # C3: logo antiguo vs v2
    h = H['C3']
    pages.append(pagina(f'''{cabecera(h)}<div class="grid" style="margin-top:4mm"><div style="grid-column:1/6">{cuerpo(h)}</div>
      <div style="grid-column:6/13;display:flex;flex-direction:column;gap:3mm">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm">
          <div><div class="shot" style="height:30mm;background:#fff;padding:5mm"><img src="{EVU}/ev21_logo_tap_antiguo.png"></div><div class="cap">Actual · /tap (órbita redibujada + estrellas)</div></div>
          <div><div class="shot" style="height:30mm;background:#fff;padding:6mm"><img src="{logo('tap','color-sobre-claro')}"></div><div class="cap">v2 · oryzz-tap-horizontal_color-sobre-claro.svg</div></div>
          <div><div class="shot" style="height:22mm;background:#0B0D12;padding:3mm"><img src="{EVU}/ev23_home_logo_actual.png"></div><div class="cap">Actual · oryzz.com (texto vivo)</div></div>
          <div><div class="shot" style="height:22mm;background:#0B0D12;padding:5mm"><img src="{logo('horizontal','color-sobre-oscuro')}"></div><div class="cap">v2 · oryzz-logo-horizontal_color-sobre-oscuro.svg</div></div>
        </div>{fix(h)}</div></div>''', n)); n += 1
    pages.append(pagina(pair('A1', 'A2', 'ev12_home_footer.png', None, 26), n)); n += 1
    pages.append(pagina(pair('A3', 'A6'), n)); n += 1
    pages.append(pagina(full('A4', ['ev06_home_servicios_iconos.png', 'ev08_tap_iconos_color.png'], [28, 56]), n)); n += 1
    pages.append(pagina(full('A5', ['ev20_nodo_una_tinta.png'], [34]), n)); n += 1
    pages.append(pagina(full('M1', ['ev03_home_hero.png'], [86]), n)); n += 1
    pages.append(pagina(pair('M2', 'M3', 'ev02_tap_cabecera.png', 'ev11_home_titular_gradiente.png', 20), n)); n += 1
    # M4 con miniatura vertical
    h = H['M4']
    pages.append(pagina(f'''{cabecera(h)}<div class="grid" style="margin-top:4mm"><div style="grid-column:1/7">{cuerpo(h)}<div style="margin-top:5mm">{fix(h)}</div>
      <div style="margin-top:5mm">{shot('ev05_home_problema_iconos.png', 44, CAPS['ev05_home_problema_iconos.png'])}</div></div>
      <div style="grid-column:8/13"><div class="shot" style="height:150mm;background:#0B0D12"><img src="{EVU}/ev18_home_pagina_completa.png"></div><div class="cap">{CAPS['ev18_home_pagina_completa.png']}</div></div></div>''', n)); n += 1
    pages.append(pagina(pair('M5', 'M6', None, 'ev14_home_nosotros.png', 44), n)); n += 1
    pages.append(pagina(pair('M7', 'M8', 'ev19_og_image_actual.png', None, 50), n)); n += 1
    pages.append(pagina(pair('M9', 'M10', 'ev10_tap_banner_cookies.png', 'ev09_tap_producto_logo_antiguo.png', 50), n)); n += 1
    # Bajos
    bajos = [h for h in HALLAZGOS if h['prio'] == 'Bajo']
    filas = ''.join(f'<tr><td style="font-family:var(--fm);font-weight:700;width:10mm">{h["id"]}</td><td style="width:44mm;font-weight:600">{md(h["titulo"])}</td><td>{md(" ".join(h["evidencia"]))}</td><td class="muted" style="width:52mm">{md(h["impacto"])}</td><td style="width:62mm">{md(" ".join(h["correccion"]))}</td></tr>' for h in bajos)
    pages.append(pagina(f'''<div style="display:flex;align-items:center;gap:4mm"><span class="hid">Hallazgos · B1–B{len(bajos)}</span>{tag("Bajo")}</div><h2 style="margin-top:3mm">Mantenimiento y confianza</h2>
      <table class="t" style="margin-top:6mm"><tr><th>ID</th><th>Hallazgo</th><th>Evidencia</th><th>Impacto</th><th>Corrección</th></tr>{filas}</table>''', n)); n += 1
    # Plan
    nombre_fase = {f: t for f, t, s, items in FASES}
    fases = ''.join(f'<div class="fase"><span class="hid">{s}</span><h4>{t}</h4><ul>' + ''.join(f'<li>{md(x)}</li>' for x in items) + '</ul></div>' for f, t, s, items in FASES)
    head = '<tr><th style="width:22mm"></th>' + ''.join(f'<th>{c}</th>' for c in CANALES) + '</tr>'
    rows = ''.join(f'<tr><td style="font-weight:700">{nombre_fase[f]}</td>' + ''.join(f'<td>{md(x)}</td>' for x in MATRIZ_PLAN[f]) + '</tr>' for f in MATRIZ_PLAN)
    pages.append(pagina(f'''<div class="grid"><div style="grid-column:1/5"><div class="eyebrow">Plan de migración</div><h2 style="margin-top:4mm">Cinco fases,<br>seis semanas.</h2></div>
      <p class="muted" style="grid-column:6/13;margin-top:8mm;max-width:none">Primero lo que cuesta clientes (CTA y contraste), después el sistema (tokens y fuentes) y al final lo que vive fuera de la web. Cada fase se puede publicar sola.</p></div>
      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;margin-top:4mm">{fases}</div>
      <table class="t compacta" style="margin-top:3mm">{head}{rows}</table>''', n, 'soft')); n += 1
    # Checklist
    chk = ''.join(f'<section><h4>{g}</h4>' + ''.join(f'<label><i></i><span>{md(x)}</span></label>' for x in items) + '</section>' for g, items in CHECKLIST)
    total = sum(len(i) for _, i in CHECKLIST)
    pages.append(pagina(f'''<div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eyebrow">Checklist de migración</div><h2 style="margin-top:4mm">{total} comprobaciones.</h2></div>
      <p class="muted" style="max-width:110mm">Imprímela o cópiala en el gestor de tareas. Una casilla = una tarea verificable con captura antes / después.</p></div>
      <div class="chk">{chk}</div>''', n)); n += 1

    src = os.path.join(TMP, 'auditoria.html')
    open(src, 'w', encoding='utf8').write(html_doc('Oryzz · Auditoría de marca', ''.join(pages), CSS))
    html_to_pdf(src, os.path.join(OUT, 'Oryzz_Auditoria_de_Marca.pdf'))
    return n - 1


def build_md():
    L = [f'# Oryzz · Auditoría de marca', '', f'*{FECHA} · Identidad visual v2.0 · uso interno*', '',
         'Fuente del PDF `Oryzz_Auditoria_de_Marca.pdf`. Evidencias en `evidencias/`. Generado con `00_Fuente_Maestra/build/auditoria_pdf.py` desde `auditoria_datos.py`.', '',
         '## Resumen ejecutivo', '', 'Nota global: **4,3 / 10**.', '']
    L += [f'- {p}' for p in RESUMEN] + ['', '| Cifra | Qué mide |', '|---|---|'] + [f'| {v} | {t} |' for v, t in CIFRAS]
    L += ['', '## Puntuación por área', '', '| Área | Nota | Por qué |', '|---|---|---|'] + [f'| {a} | {s}/10 | {d} |' for a, s, d in PUNTUACION] + ['| **Media** | **4,3** | |']
    L += ['', '## Hallazgos priorizados', '', '| ID | Prioridad | Área | Hallazgo |', '|---|---|---|---|'] + [f'| {h["id"]} | {h["prio"]} | {h["area"]} | {h["titulo"]} |' for h in HALLAZGOS]
    for h in HALLAZGOS:
        L += ['', f'### {h["id"]} · {h["titulo"]}', '', f'**Prioridad:** {h["prio"]} · **Área:** {h["area"]}', '']
        L += [f'![{CAPS.get(i, i)}](evidencias/{i})' for i in h['img']]
        L += ['', '**Evidencia**', ''] + [f'- {x}' for x in h['evidencia']]
        L += ['', f'**Impacto.** {h["impacto"]}', '', '**Corrección**', ''] + [f'- {x}' for x in h['correccion']]
    L += ['', '## Plan de migración por fases', '']
    for f, t, s, items in FASES:
        L += [f'### {t} ({s})', ''] + [f'- {x}' for x in items] + ['']
    L += ['| Fase | ' + ' | '.join(CANALES) + ' |', '|---|' + '---|' * len(CANALES)] + [f'| {dict((a, b) for a, b, _, _ in FASES)[f]} | ' + ' | '.join(v) + ' |' for f, v in MATRIZ_PLAN.items()]
    L += ['', '## Checklist de migración', '']
    for g, items in CHECKLIST:
        L += [f'### {g}', ''] + [f'- [ ] {x}' for x in items] + ['']
    L += ['## Método', '', '- Capturas y estilos computados de https://oryzz.com/ y https://oryzz.com/tap/ con Chrome headless (`00_Fuente_Maestra/build/web_capture.py`), 1440×900 y 390×844.',
          '- Contraste WCAG 2.2 (luminancia relativa) calculado para cada nodo de texto visible; en gradientes se toma el punto más débil.',
          '- Revisión del código local `TAP/OryzzTAP/oryzz/` (solo lectura) y de la skill `plantilla-documentos-oryzz`.', '']
    open(os.path.join(OUT, 'Auditoria_de_Marca.md'), 'w', encoding='utf8').write('\n'.join(L))


if __name__ == '__main__':
    print('páginas', build()); build_md(); print('ok')
