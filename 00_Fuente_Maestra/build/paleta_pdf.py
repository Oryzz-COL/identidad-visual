"""
Genera 03_Color/Oryzz_Paleta_y_Contraste.pdf (A4 apaisado) y las láminas PNG de la paleta.
Uso:  python paleta_pdf.py
"""
import os, sys, tempfile
from oryzz_color import PALETA, POR_NOMBRE, contraste, nivel, NOTA_CMYK, NOTA_PANTONE
from doc_base import html_doc, folio, logo, fmt, ROOT
from render import html_to_pdf, html_to_png

OUT = os.path.join(ROOT, '03_Color')
TMP = os.path.join(tempfile.gettempdir(), 'oryzz_paleta'); os.makedirs(TMP, exist_ok=True)
P = POR_NOMBRE
TITLE = 'Oryzz · Color y contraste v2.0'


def txt_on(hx):
    return '#0B0D12' if contraste(hx, '#0B0D12') >= contraste(hx, '#FFFFFF') else '#FFFFFF'


def ficha(p, big=False):
    c, m, y, k = p['cmyk']
    fg = txt_on(p['hex'])
    border = 'border:1px solid var(--g200);' if p['hex'] in ('#FFFFFF', '#F6F7F9', '#EEF3FF', '#E8FAFC', '#F4FCE0') else ''
    h = '46mm' if big else '26mm'
    return f'''<div class="ficha">
      <div class="chip" style="background:{p['hex']};color:{fg};height:{h};{border}"><span class="mono">{p['hex']}</span></div>
      <h4>{p['nombre']}</h4>
      <dl><div><dt>RGB</dt> <dd>{' '.join(str(v) for v in p['rgb'])}</dd></div>
      <div><dt>CMYK*</dt> <dd>{c} {m} {y} {k}</dd></div>
      <div><dt>PMS†</dt> <dd>{p['pantone'] or '—'}</dd></div></dl>
      <p class="uso">{p['uso']}</p></div>'''


CSS = """
.ficha h4{margin-top:2.5mm;font-size:9pt}
.chip{border-radius:3mm;display:flex;align-items:flex-end;padding:2.5mm 3mm;font-size:7pt}
.ficha dl{font-family:var(--fm);font-size:6.2pt;line-height:1.55;margin-top:1.2mm;color:var(--g600)}
.dark .ficha dl{color:var(--g200)}
.ficha dt,.ficha dd{display:inline}.ficha dt{color:var(--g500)} .dark .ficha dt{color:var(--g400)}
.ficha .uso{font-size:7pt;line-height:1.4;color:var(--g500);margin-top:1.4mm}
.dark .ficha .uso{color:var(--g400)}
.row{display:grid;gap:4mm}
.nota{font-size:6.8pt;color:var(--g500);line-height:1.45}
.dark .nota{color:var(--g400)}
/* matriz */
.mx{border-collapse:separate;border-spacing:1.2mm}
.mx th{font-family:var(--fm);font-size:6.3pt;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--g500);text-align:left;padding:0 1mm;vertical-align:bottom}
.mx th.fg{text-align:right;white-space:nowrap;padding-right:2mm;vertical-align:middle;text-transform:none;letter-spacing:0;font-family:var(--ft);font-size:7.5pt;color:var(--g950)}
.dark .mx th.fg{color:#fff}
.mx th .sw{display:inline-block;width:3mm;height:3mm;border-radius:1mm;vertical-align:-.4mm;margin-right:1.4mm;border:1px solid rgba(128,128,128,.35)}
.cell{border-radius:1.6mm;overflow:hidden;width:100%;border:1px solid rgba(128,128,128,.18)}
.cell .s{height:6.4mm;display:flex;align-items:center;padding:0 2mm;font-family:var(--fd);font-weight:600;font-size:9.5pt;justify-content:space-between}
.cell .s small{font-family:var(--ft);font-weight:500;font-size:6.2pt}
.cell .r{display:flex;justify-content:space-between;align-items:center;padding:.5mm 1.6mm;font-family:var(--fm);font-size:6.2pt;background:#fff;color:var(--g950)}
.dark .cell .r{background:var(--g850);color:#fff}
.lv{font-weight:700;letter-spacing:.04em}
.lv-AAA{color:#1F7A45} .lv-AA{color:#1F7A45} .lv-AAg{color:#9A5B00} .lv-No{color:#C0282D}
.dark .lv-AAA,.dark .lv-AA{color:var(--l500)} .dark .lv-AAg{color:var(--warn)} .dark .lv-No{color:#FF8A8E}
.leyenda{display:flex;gap:6mm;font-size:7pt;margin-top:3mm}
.leyenda b{font-family:var(--fm)}
/* barras */
.prop{display:flex;height:34mm;border-radius:3mm;overflow:hidden;margin-top:8mm}
.prop div{display:flex;flex-direction:column;justify-content:flex-end;padding:3mm;font-family:var(--fm);font-size:7pt;letter-spacing:.06em}
.prop b{font-family:var(--fd);font-size:20pt;letter-spacing:-.03em;font-weight:600}
.cta{display:inline-flex;align-items:center;gap:2.5mm;height:12mm;padding:0 6mm;border-radius:3mm;font-family:var(--fd);font-weight:600;font-size:11pt}
.reco li{margin:0 0 2.4mm 4mm;font-size:8.6pt;line-height:1.45}
.reco li b{font-weight:700}
"""


def pagina(cls, body, n, dark=False):
    return f'<section class="page {cls}">{body}{folio("Color y contraste · v2.0", n, dark)}</section>'


def matriz(fgs, bgs, dark=False):
    head = '<tr><th></th>' + ''.join(
        f'<th><span class="sw" style="background:{P[b]["hex"]}"></span>{b}<br><span style="opacity:.8">{P[b]["hex"]}</span></th>' for b in bgs) + '</tr>'
    rows = []
    for f in fgs:
        cells = []
        for b in bgs:
            r = contraste(P[f]['hex'], P[b]['hex']); lv = nivel(r)
            cls = {'AAA': 'AAA', 'AA': 'AA', 'AA grande': 'AAg', 'No apto': 'No'}[lv]
            cells.append(f'<td><div class="cell"><div class="s" style="background:{P[b]["hex"]};color:{P[f]["hex"]}">Aa<small>Texto</small></div>'
                         f'<div class="r"><span>{fmt(r)}:1</span><span class="lv lv-{cls}">{lv}</span></div></div></td>')
        rows.append(f'<tr><th class="fg"><span class="sw" style="background:{P[f]["hex"]}"></span>{f}</th>{"".join(cells)}</tr>')
    return f'<table class="mx">{head}{"".join(rows)}</table>'


LEYENDA = '''<div class="leyenda"><span><b class="lv lv-AAA">AAA</b> ≥ 7:1 · cualquier texto</span><span><b class="lv lv-AA">AA</b> ≥ 4,5:1 · texto normal</span>
<span><b class="lv lv-AAg">AA grande</b> ≥ 3:1 · solo ≥ 24 px (18 pt) o ≥ 18,7 px negrita, iconos y bordes</span><span><b class="lv lv-No">No apto</b> &lt; 3:1 · nunca para texto</span></div>'''


def build_pdf():
    pages = []
    n = 1
    # 1 · Portada
    pages.append(f'''<section class="page dark" style="padding:18mm">
      <img src="{logo('horizontal','color-sobre-oscuro')}" style="height:9mm">
      <div style="position:absolute;left:18mm;top:62mm;width:150mm">
        <div class="eyebrow"><span class="n">03</span> · Sistema de color · v2.0</div>
        <h1 style="margin-top:6mm">Color y<br>contraste.</h1>
        <p class="lead" style="margin-top:6mm;max-width:110mm">Paleta de marca, proporción de uso, gradientes y la matriz de contraste WCAG 2.2 calculada para cada combinación útil.</p>
      </div>
      <div style="position:absolute;right:18mm;top:18mm;bottom:18mm;width:88mm;display:flex;flex-direction:column;border-radius:4mm;overflow:hidden">
        <div style="flex:60;background:#12151D;border:1px solid #232836;border-bottom:0;padding:4mm;display:flex;align-items:flex-end" class="mono"><span style="font-size:7pt;color:#8A90A0">60 % GRAFITO</span></div>
        <div style="flex:25;background:#F6F7F9;padding:4mm;display:flex;align-items:flex-end" class="mono"><span style="font-size:7pt;color:#3A4152">25 % BLANCO / GRAFITO 50</span></div>
        <div style="flex:10;background:linear-gradient(135deg,#5C8BFF,#36CFE0);padding:0 4mm;display:flex;align-items:center" class="mono"><span style="font-size:7pt;color:#0B0D12">10 % AZUL IA / CYAN</span></div>
        <div style="flex:5;background:#BFF24A;padding:0 4mm;display:flex;align-items:center" class="mono"><span style="font-size:7pt;color:#0B0D12">≤ 5 % LIMA</span></div>
      </div>
      <div class="folio" style="color:#5A6172"><span>Identidad visual Oryzz · 2026</span><span>oryzz.com</span><span>01</span></div>
    </section>''')
    n += 1
    # 2 · Proporción
    pages.append(pagina('', f'''
      <div class="grid">
        <div style="grid-column:1/5"><div class="eyebrow"><span class="n">01</span> · Proporción</div>
          <h2 style="margin-top:4mm">Mucho grafito.<br>Un solo acento.</h2>
          <p class="lead" style="margin-top:4mm">El grafito es el espacio donde el sistema trabaja. El azul marca la tecnología; el lima es el nodo: el lead, la cita, el cliente. Si una pieza ya tiene lima, no lleva otro acento.</p></div>
        <div style="grid-column:6/13">
          <div class="prop">
            <div style="flex:60;background:#0B0D12;color:#8A90A0"><b style="color:#fff">60 %</b>GRAFITO 950 · 850 · 800</div>
            <div style="flex:25;background:#F6F7F9;color:#3A4152;border:1px solid #E5E8EE"><b style="color:#0B0D12">25 %</b>BLANCO · GRAFITO 50</div>
            <div style="flex:10;background:linear-gradient(135deg,#5C8BFF,#36CFE0);color:#0B0D12;padding:3mm 2mm"><b style="font-size:13pt">10 %</b>AZUL</div>
            <div style="flex:5;background:#BFF24A;color:#0B0D12;padding:3mm 1.5mm"><b style="font-size:10pt">5 %</b>LIMA</div>
          </div>
          <div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:9mm;column-gap:7mm">
            <div><h3>Fondos</h3><p class="muted" style="margin-top:2mm">Grafito 950 en digital y presentaciones; blanco o Grafito 50 en documentos, Tap y piezas de producto. Nunca fondos completos de azul, cyan o lima salvo piezas puntuales de campaña.</p></div>
            <div><h3>Acento azul</h3><p class="muted" style="margin-top:2mm">Una palabra del titular, un gráfico, un botón. En claro, el azul funcional es el <b>Azul 600</b>; el Azul IA 500 solo en logo, gráficos y texto ≥ 24 px.</p></div>
            <div><h3>El nodo lima</h3><p class="muted" style="margin-top:2mm">Un dato, una acción o un punto por pieza. Sobre oscuro, Lima 500. Sobre claro no funciona como texto: usa Lima 600 como punto gráfico y Lima 900 si necesitas texto.</p></div>
          </div>
        </div>
      </div>''', n)); n += 1
    # 3 · Grafito
    g1 = ['Grafito 950', 'Grafito 850', 'Grafito 800', 'Grafito 700', 'Grafito 600', 'Grafito 500', 'Titanio 400']
    g2 = ['Grafito 300', 'Grafito 200', 'Grafito 100', 'Grafito 50', 'Blanco', 'Grafito 900']
    pages.append(pagina('', f'''
      <div class="grid"><div style="grid-column:1/4"><div class="eyebrow"><span class="n">02</span> · Neutros</div><h2 style="margin-top:4mm">Grafito</h2>
      <p class="muted" style="margin-top:3mm">Neutros fríos (tono 220–224°). Sustituyen a los 40+ grises sueltos de las webs actuales.</p></div>
      <div style="grid-column:4/13"><div class="row" style="grid-template-columns:repeat(7,1fr)">{''.join(ficha(P[x], True) for x in g1)}</div>
      <div class="row" style="grid-template-columns:repeat(7,1fr);margin-top:6mm">{''.join(ficha(P[x]) for x in g2)}<div></div></div></div></div>
      <p class="nota" style="position:absolute;left:18mm;bottom:15mm;max-width:250mm">* CMYK {NOTA_CMYK}; en grafitos muy oscuros se propone negro enriquecido frío. † Pantone Solid Coated: {NOTA_PANTONE}. «—» = sin tinta directa (papel o tramado).</p>''', n)); n += 1
    # 4 · Azul y cyan
    az = ['Azul 300', 'Azul 400', 'Azul IA 500', 'Azul 600', 'Azul 700', 'Azul 900', 'Azul 50']
    cy = ['Cyan 300', 'Cyan 500', 'Cyan 600', 'Cyan 50']
    pages.append(pagina('', f'''
      <div class="grid"><div style="grid-column:1/4"><div class="eyebrow"><span class="n">03</span> · Acento tecnológico</div><h2 style="margin-top:4mm">Azul IA<br>y Cyan</h2>
      <p class="muted" style="margin-top:3mm">El Azul IA 500 <span class="mono">#3B72FF</span> es el color de marca. El 400 lo sustituye sobre oscuro y el 600 es el azul que funciona en botones y enlaces sobre claro. El cyan solo existe como final del gradiente y como color de dato.</p></div>
      <div style="grid-column:4/13"><div class="row" style="grid-template-columns:repeat(7,1fr)">{''.join(ficha(P[x], x == 'Azul IA 500') for x in az)}</div>
      <div class="row" style="grid-template-columns:repeat(7,1fr);margin-top:6mm">{''.join(ficha(P[x], x == 'Cyan 500') for x in cy)}</div></div></div>''', n)); n += 1
    # 5 · Lima y estado
    li = ['Lima 500', 'Lima 600', 'Lima 300', 'Lima 900', 'Lima 50']
    es = ['Éxito', 'Aviso', 'Error']
    pages.append(pagina('', f'''
      <div class="grid"><div style="grid-column:1/4"><div class="eyebrow"><span class="n">04</span> · El nodo y los estados</div><h2 style="margin-top:4mm">Lima<br>y Estado</h2>
      <p class="muted" style="margin-top:3mm">El lima es escaso a propósito: ≤ 5 % de la superficie. Los colores de estado son funcionales (formularios, alertas, informes) y nunca decorativos.</p></div>
      <div style="grid-column:4/13"><div class="row" style="grid-template-columns:repeat(7,1fr)">{''.join(ficha(P[x], x == 'Lima 500') for x in li)}</div>
      <div class="eyebrow" style="margin-top:8mm">Estado</div>
      <div class="row" style="grid-template-columns:repeat(7,1fr);margin-top:3mm">{''.join(ficha(P[x]) for x in es)}</div>
      <p class="nota" style="margin-top:5mm;max-width:200mm">Éxito y Error no alcanzan 4,5:1 con texto blanco (3,49 y 3,91:1). Úsalos como icono, borde o fondo suave con el mensaje en Grafito 950; sobre fondo oscuro sí sirven como texto (5,56 y 4,97:1).</p></div></div>''', n)); n += 1
    # 6 · Gradientes
    pages.append(pagina('dark', f'''
      <div class="grid"><div style="grid-column:1/5"><div class="eyebrow"><span class="n">05</span> · Gradiente IA</div><h2 style="margin-top:4mm">Dos colores.<br>135°. Nada más.</h2>
      <p class="lead" style="margin-top:4mm">El gradiente es la firma de las «zz». Se usa en el logo, en el botón principal sobre oscuro y en una línea o un dato por pieza.</p>
      <div style="margin-top:8mm" class="mono muted">
        <p style="font-size:7.5pt">OSCURO · linear-gradient(135deg, #5C8BFF, #36CFE0)</p>
        <p style="font-size:7.5pt;margin-top:1.5mm">CLARO · linear-gradient(135deg, #3B72FF, #17A9C2)</p></div></div>
      <div style="grid-column:6/13">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm">
          <div><div style="height:52mm;border-radius:4mm;background:var(--grad-d);display:flex;align-items:flex-end;padding:4mm"><span class="mono" style="font-size:7pt;color:#0B0D12">IA · OSCURO</span></div></div>
          <div><div style="height:52mm;border-radius:4mm;background:#fff;padding:4mm;display:flex;align-items:flex-end"><div style="height:100%;width:100%;border-radius:3mm;background:var(--grad-l);display:flex;align-items:flex-end;padding:3mm"><span class="mono" style="font-size:7pt;color:#fff">IA · CLARO</span></div></div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:8mm">
          <div><h4 style="color:var(--l500)">Sí</h4><ul class="reco" style="margin-top:2mm;color:#D5D9E0">
            <li>Logo y «zz» del wordmark.</li><li>Botón principal sobre oscuro, con texto Grafito 950.</li><li>Una palabra de un titular grande (≥ 40 px) o una línea de gráfico.</li></ul></div>
          <div><h4 style="color:#FF8A8E">No</h4><ul class="reco" style="margin-top:2mm;color:#D5D9E0">
            <li>Párrafos, frases enteras o titulares completos en gradiente.</li><li>Fondos de sección o de página.</li><li>Tres colores, violeta o neón; halos difusos de color.</li></ul></div>
        </div></div></div>''', n, True)); n += 1
    # 7 · Matriz oscuro
    fg_d = ['Blanco', 'Grafito 200', 'Grafito 300', 'Titanio 400', 'Grafito 500', 'Azul 300', 'Azul 400', 'Azul IA 500', 'Cyan 500', 'Lima 500', 'Éxito', 'Aviso', 'Error']
    bg_d = ['Grafito 950', 'Grafito 850', 'Grafito 800', 'Grafito 700', 'Azul 900']
    pages.append(pagina('dark', f'''
      <div class="grid"><div style="grid-column:1/4"><div class="eyebrow"><span class="n">06</span> · Contraste WCAG 2.2</div><h2 style="margin-top:4mm">Sobre<br>oscuro</h2>
      <p class="muted" style="margin-top:3mm">Relación de contraste calculada con la fórmula de luminancia relativa de WCAG 2.2 (criterios 1.4.3 y 1.4.6).</p>
      <div style="margin-top:6mm;font-size:8pt;line-height:1.5;color:#D5D9E0"><b style="color:#fff">Lectura rápida</b><br>Texto: Blanco, Grafito 200 y 300.<br>Texto terciario: Titanio 400 (nunca Grafito 500).<br>Enlaces: Azul 300.<br>Dato: Lima 500 o Cyan 500.</div></div>
      <div style="grid-column:4/13">{matriz(fg_d, bg_d, True)}{LEYENDA}</div></div>''', n, True)); n += 1
    # 8 · Matriz claro
    fg_l = ['Grafito 950', 'Grafito 600', 'Grafito 500', 'Titanio 400', 'Azul IA 500', 'Azul 600', 'Azul 700', 'Cyan 600', 'Lima 600', 'Lima 900', 'Éxito', 'Aviso', 'Error']
    bg_l = ['Blanco', 'Grafito 50', 'Grafito 100', 'Azul 50', 'Lima 50']
    pages.append(pagina('', f'''
      <div class="grid"><div style="grid-column:1/4"><div class="eyebrow"><span class="n">07</span> · Contraste WCAG 2.2</div><h2 style="margin-top:4mm">Sobre<br>claro</h2>
      <p class="muted" style="margin-top:3mm">El error más habitual en claro es usar el azul o el lima de la versión oscura. En claro manda el Azul 600.</p>
      <div style="margin-top:6mm;font-size:8pt;line-height:1.5;color:var(--g600)"><b style="color:var(--g950)">Lectura rápida</b><br>Texto: Grafito 950 y 600.<br>Texto terciario: Grafito 500 (nunca Titanio 400).<br>Enlaces y botones: Azul 600.<br>Dato: Lima 900 o Azul 600; Lima 600 solo como punto.</div></div>
      <div style="grid-column:4/13">{matriz(fg_l, bg_l)}{LEYENDA}</div></div>''', n)); n += 1
    # 9 · Sobre color + botones
    fg_c = ['Blanco', 'Grafito 950']
    bg_c = ['Azul 600', 'Azul IA 500', 'Azul 400', 'Cyan 500', 'Cyan 600', 'Lima 500']
    w = lambda a, b: fmt(contraste(a, b))
    pages.append(pagina('', f'''
      <div class="grid"><div style="grid-column:1/4"><div class="eyebrow"><span class="n">08</span> · Botones</div><h2 style="margin-top:4mm">Texto sobre<br>color</h2>
      <p class="muted" style="margin-top:3mm">Un botón con gradiente se evalúa en su punto más débil. El texto blanco sobre el gradiente actual de la web cae a 1,88:1 en el extremo cyan.</p></div>
      <div style="grid-column:4/13">{matriz(fg_c, bg_c)}
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm;margin-top:7mm">
        <div style="background:#0B0D12;border-radius:3mm;padding:6mm"><div class="eyebrow" style="color:#8A90A0">Oscuro · correcto</div>
          <div class="cta" style="margin-top:4mm;background:var(--grad-d);color:#0B0D12">Agendar valoración</div>
          <p class="mono" style="font-size:6.8pt;color:#D5D9E0;margin-top:3mm">Grafito 950 sobre gradiente<br>{w('#0B0D12','#5C8BFF')}:1 → {w('#0B0D12','#36CFE0')}:1 · AA en todo el botón</p></div>
        <div style="background:#fff;border:1px solid #E5E8EE;border-radius:3mm;padding:6mm"><div class="eyebrow">Claro · correcto</div>
          <div class="cta" style="margin-top:4mm;background:#2C5BD0;color:#fff">Agendar valoración</div>
          <p class="mono" style="font-size:6.8pt;color:#3A4152;margin-top:3mm">Blanco sobre Azul 600<br>{w('#FFFFFF','#2C5BD0')}:1 · AA</p></div>
        <div style="background:#0B0D12;border-radius:3mm;padding:6mm;position:relative"><div class="eyebrow" style="color:#FF8A8E">Web actual · incorrecto</div>
          <div class="cta" style="margin-top:4mm;background:linear-gradient(105deg,#3B72FF,#36CFE0);color:#fff">Agendar valoración</div>
          <p class="mono" style="font-size:6.8pt;color:#D5D9E0;margin-top:3mm">Blanco sobre gradiente<br>{w('#FFFFFF','#3B72FF')}:1 → {w('#FFFFFF','#36CFE0')}:1 · no apto</p></div>
      </div></div></div>''', n)); n += 1
    # 10 · Recomendaciones + impresión
    pages.append(pagina('soft', f'''
      <div class="grid"><div style="grid-column:1/5"><div class="eyebrow"><span class="n">09</span> · Reglas</div><h2 style="margin-top:4mm">Recomendaciones</h2>
      <p class="muted" style="margin-top:3mm">Diez reglas que resuelven el 95 % de las decisiones de color sin abrir esta guía.</p></div>
      <div style="grid-column:5/13;display:grid;grid-template-columns:1fr 1fr;gap:7mm">
      <ol class="reco" style="padding-left:2mm">
        <li><b>Botón principal en oscuro:</b> gradiente IA + texto Grafito 950 (6,10–10,33:1).</li>
        <li><b>Botón principal en claro:</b> Azul 600 + texto blanco (5,98:1). Hover: Azul 700 (8,87:1).</li>
        <li><b>Texto terciario:</b> Titanio 400 en oscuro (6,09:1), Grafito 500 en claro (6,20:1). No se intercambian: cruzados bajan a 3,14 y 3,19:1.</li>
        <li><b>Azul IA 500 como texto</b> solo ≥ 24 px (4,17:1 sobre blanco, 4,66:1 sobre Grafito 950).</li>
        <li><b>Enlaces:</b> Azul 300 en oscuro (9,97:1); Azul 600 subrayado en claro.</li>
      </ol><ol class="reco" start="6" style="padding-left:2mm">
        <li><b>Lima:</b> texto solo sobre oscuro (14,82:1). En claro, Lima 600 como punto (2,58:1, no apto para texto ni iconos informativos).</li>
        <li><b>Cyan:</b> dato y final del gradiente. Nunca texto sobre blanco (1,88:1; Cyan 600 2,80:1).</li>
        <li><b>Estados:</b> mensajes en Grafito 950 con icono o borde del color de estado.</li>
        <li><b>Tamaño mínimo:</b> 14 px en pantalla (eyebrow mono 12 px como única excepción), 9 pt impreso.</li>
        <li><b>Foco visible:</b> contorno 2 px Azul 400 en oscuro / Azul 600 en claro, desplazado 3 px.</li>
      </ol></div></div>
      <div class="rule" style="margin-top:9mm"></div>
      <div class="grid"><div style="grid-column:1/5"><h3>Impresión</h3></div>
      <div style="grid-column:5/13;display:grid;grid-template-columns:1fr 1fr;gap:7mm;font-size:8.2pt;color:var(--g600)">
        <p>Los valores CMYK son una conversión <b>aproximada</b> sin perfil ICC. Antes de imprimir tiradas, pide <b>prueba de color</b> contractual (FOGRA39 estucado / FOGRA47 no estucado). Grandes fondos de grafito: negro enriquecido frío, nunca solo K.</p>
        <p>Las referencias Pantone son la coincidencia visual más cercana en Solid Coated y deben <b>validarse con la guía Pantone física</b>. Azul IA 500 y Lima 500 son más saturados que la mayoría de tintas: en offset quedarán algo apagados; para vinilo, bordado y serigrafía usa los colorways «sólido» del logo.</p>
      </div></div>''', n)); n += 1
    html = html_doc(TITLE, ''.join(pages), CSS)
    src = os.path.join(TMP, 'paleta.html'); open(src, 'w', encoding='utf8').write(html)
    html_to_pdf(src, os.path.join(OUT, 'Oryzz_Paleta_y_Contraste.pdf'))
    return src


def build_laminas():
    """Láminas 1920×1080 para compartir (oscura y clara)."""
    def lam(dark):
        bg = '#0B0D12' if dark else '#FFFFFF'
        ink = '#FFFFFF' if dark else '#0B0D12'
        sub = '#8A90A0' if dark else '#5A6172'
        brd = '#232836' if dark else '#E5E8EE'
        cols = (['Grafito 950', 'Grafito 850', 'Grafito 700', 'Titanio 400', 'Grafito 200', 'Blanco'] if dark else
                ['Blanco', 'Grafito 50', 'Grafito 100', 'Grafito 500', 'Grafito 600', 'Grafito 950'])
        acc = (['Azul 400', 'Azul IA 500', 'Azul 300', 'Cyan 500', 'Lima 500'] if dark else
               ['Azul IA 500', 'Azul 600', 'Azul 700', 'Cyan 600', 'Lima 600'])
        grad = 'linear-gradient(135deg,#5C8BFF,#36CFE0)' if dark else 'linear-gradient(135deg,#3B72FF,#17A9C2)'
        way = 'color-sobre-oscuro' if dark else 'color-sobre-claro'

        def sw(nm, h):
            p = P[nm]; fg = txt_on(p['hex'])
            return (f'<div style="display:flex;flex-direction:column;gap:14px"><div style="height:{h}px;border-radius:18px;background:{p["hex"]};border:1px solid {brd};'
                    f'display:flex;align-items:flex-end;padding:18px;color:{fg};font:500 17px \'JetBrains Mono\'">{p["hex"]}</div>'
                    f'<div style="font:600 22px \'Space Grotesk\';letter-spacing:-.01em;color:{ink}">{nm}</div>'
                    f'<div style="font:400 15px \'JetBrains Mono\';color:{sub};line-height:1.5">RGB {" ".join(map(str, p["rgb"]))}<br>Pantone {p["pantone"] or "—"}</div></div>')
        body = f'''<div style="width:1920px;height:1080px;background:{bg};padding:96px 120px;position:relative;font-family:'Manrope'">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div><div style="font:500 16px 'JetBrains Mono';letter-spacing:.16em;text-transform:uppercase;color:{sub}">Oryzz · Paleta v2.0 · {'versión oscura' if dark else 'versión clara'}</div>
            <div style="font:700 88px 'Space Grotesk';letter-spacing:-.045em;line-height:.95;color:{ink};margin-top:26px">Grafito, azul<br>y un <span style="color:{'#BFF24A' if dark else '#2C5BD0'}">nodo</span>.</div></div>
            <img src="{logo('horizontal', way)}" style="height:52px">
          </div>
          <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:28px;margin-top:70px">{''.join(sw(c, 170) for c in cols)}</div>
          <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:28px;margin-top:40px">{''.join(sw(c, 110) for c in acc)}
            <div style="display:flex;flex-direction:column;gap:14px"><div style="height:110px;border-radius:18px;background:{grad};display:flex;align-items:flex-end;padding:18px;color:{'#0B0D12' if dark else '#fff'};font:500 17px 'JetBrains Mono'">135°</div>
            <div style="font:600 22px 'Space Grotesk';color:{ink}">Gradiente IA</div><div style="font:400 15px 'JetBrains Mono';color:{sub}">Solo logo, CTA y un dato</div></div>
          </div>
          <div style="position:absolute;left:120px;right:120px;bottom:60px;display:flex;justify-content:space-between;font:500 15px 'JetBrains Mono';letter-spacing:.12em;text-transform:uppercase;color:{sub}">
            <span>60 % grafito · 25 % {'blanco' if dark else 'blanco / grafito 50'} · 10 % azul / cyan · ≤ 5 % lima</span><span>oryzz.com</span></div></div>'''
        return html_doc('Oryzz paleta', body, 'html,body{background:%s}' % bg)
    for dark, name in [(True, 'Oryzz_Paleta_Lamina_Oscura.png'), (False, 'Oryzz_Paleta_Lamina_Clara.png')]:
        src = os.path.join(TMP, name + '.html'); open(src, 'w', encoding='utf8').write(lam(dark))
        html_to_png(src, os.path.join(OUT, name), 1920, 1080)


if __name__ == '__main__':
    build_pdf(); build_laminas(); print('ok')
