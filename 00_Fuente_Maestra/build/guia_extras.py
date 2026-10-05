"""
Oryzz · piezas compañeras de la guía de marca
==============================================

    python guia_extras.py             # genera las dos piezas
    python guia_extras.py --png DIR   # además, PNG de cada página (revisión)

- `01_Guia_de_Marca/Oryzz_Guia_de_Marca_Resumen_1_pagina.pdf`  (A4 apaisado, referencia rápida)
- `04_Tipografia/Oryzz_Especimen_Tipografico.pdf`              (16:9, 8 páginas)

Reutiliza el CSS, los helpers y los datos de `guia_marca.py`.
"""
import argparse, pathlib, sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import guia_marca as gm  # noqa: E402
from guia_marca import uri, icono, SI, NO, head, pg, G, C, TOK, contraste, num  # noqa: E402
from render import html_to_pdf  # noqa: E402

RESUMEN = gm.SALIDA / 'Oryzz_Guia_de_Marca_Resumen_1_pagina.pdf'
ESPECIMEN = gm.RAIZ / '04_Tipografia' / 'Oryzz_Especimen_Tipografico.pdf'


def documento(cuerpo, titulo, css_extra=''):
    brand = (gm.MAESTRA / 'brand.css').resolve().as_uri()
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title>'
            f'<link rel="stylesheet" href="{brand}"><style>{gm.CSS}{css_extra}</style></head><body>{cuerpo}</body></html>')


def escribir_pdf(doc, nombre, destino, titulo):
    gm.TMP.mkdir(parents=True, exist_ok=True)
    h = gm.TMP / nombre
    h.write_text(doc, encoding='utf8')
    print('Desbordes', nombre, ':', gm.comprobar_desbordes(h))
    html_to_pdf(str(h), str(destino))
    import fitz
    d = fitz.open(destino)
    d.set_metadata({'title': titulo, 'author': 'Oryzz', 'creator': 'guia_extras.py', 'producer': 'Oryzz'})
    tmp = str(destino) + '.tmp'
    d.save(tmp, garbage=4, deflate=True)
    d.close()
    pathlib.Path(tmp).replace(destino)
    print('PDF:', destino, f'({destino.stat().st_size / 1e6:.1f} MB)')


# ----------------------------------------------------------------- resumen de una página (A4 apaisado)

def resumen():
    css = """
@page { size: 297mm 210mm; margin: 0; }
.r { width: 297mm; height: 210mm; position: relative; overflow: hidden; background: #0B0D12; color: #fff; }
.r .in { inset: 13mm 14mm 12mm 14mm; }
.r .eyebrow { font-size: 9.5px; }
.r p, .r li { font-size: 11.5px; line-height: 1.5; }
.r h4 { font-size: 14px; }
.r .card { padding: 4mm 4.5mm; border-radius: 8px; }
.r .kick { font-size: 9px; margin-bottom: 2.2mm; }
.r .g { column-gap: 5mm; row-gap: 5mm; }
.r code { font-size: 10px; }
.r .yes, .r .nope { font-size: 11px; padding: 1.6mm 0; gap: 2mm; }
.r .mk { width: 13px; height: 13px; }
.r ol.n li::before { font-size: 9px; top: 2px; }
"""
    sw = ''
    for hexc, nm, uso in [(G['950'], 'Grafito 950', '60 % · fondo'), ('#FFFFFF', 'Blanco', '25 % · superficie'), (C['azul']['500'], 'Azul IA', '10 % · marca'),
                          (C['azul']['600'], 'Azul 600', 'botón en claro'), (C['cyan']['500'], 'Cyan', 'gradiente, datos'), (C['lima']['500'], 'Lima', '≤ 5 % · acento')]:
        tx = '#FFFFFF' if contraste(hexc, '#FFFFFF') >= contraste(hexc, G['950']) else G['950']
        sw += (f'<div style="background:{hexc};color:{tx};border:1px solid var(--borde);border-radius:7px;height:26mm;padding:2.5mm;display:flex;flex-direction:column;justify-content:flex-end">'
               f'<div style="font-weight:700;font-size:11.5px">{nm}</div><div class="mono" style="font-size:9px;opacity:.85">{hexc}</div><div class="mono" style="font-size:8.5px;opacity:.75">{uso}</div></div>')
    reglas = ['Un solo acento lima por pieza; lima nunca como texto sobre claro.', 'Un fragmento en azul por titular; nunca la frase entera en gradiente.',
              'Un único CTA, verbo + resultado, con contraste AA.', 'Cifras reales con unidad; si no lo son, «Ejemplo» o {{dato}}.',
              'Nada de violeta, neón, emojis, robots, cerebros ni halos difusos.']
    L = '02_Logos/'
    cuerpo = f"""<section class="r page oscuro"><div class="in">
      <div style="display:flex;align-items:center;gap:6mm">
        <img src="{uri(L + '01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg')}" style="height:11mm;margin-left:-2mm">
        <div class="eyebrow" style="margin-left:auto;text-align:right">Guía de marca {gm.VERSION} · resumen de una página<br>{gm.FECHA}</div>
      </div>
      <div class="g" style="margin-top:7mm">
        <div class="s5">
          <div style="font-family:var(--font-display);font-weight:700;font-size:40px;line-height:1;letter-spacing:-.04em">Sistemas que<br>captan <span class="az">clientes</span>.</div>
          <p style="margin-top:4mm;color:var(--tx2)">Oryzz monta sistemas de captación con IA para PYMES y los mide en clientes y euros. Oryzz Tap es su línea de producto NFC + QR. Mismo sistema visual para las dos.</p>
          <div class="card" style="margin-top:5mm">
            <div class="kick">Logo</div>
            <div style="display:flex;gap:5mm;align-items:center">
              <img src="{uri(L + '04_Isotipo/SVG/oryzz-isotipo_color-sobre-oscuro.svg')}" style="height:15mm">
              <img src="{uri(L + '07_Submarca_Tap/SVG/oryzz-tap-horizontal_color-sobre-oscuro.svg')}" style="height:9mm">
            </div>
            <p style="margin-top:2.5mm">Siempre el SVG de <code>02_Logos</code>. Área de respeto = altura de la «z». Mínimo 88 px / 22 mm; por debajo de 120 px, versión <code>solido</code>. En texto: «Oryzz» y «Oryzz Tap».</p>
          </div>
        </div>
        <div class="s7">
          <div class="kick">Color · 60 / 25 / 10 / ≤ 5</div>
          <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:2mm">{sw}</div>
          <div style="display:flex;gap:2mm;margin-top:2mm">
            <div style="flex:1;height:8mm;border-radius:6px;background:var(--grad-ia-oscuro);display:flex;align-items:center;padding:0 3mm;color:#0B0D12;font-size:10px;font-weight:700">Gradiente IA oscuro · 135° #5C8BFF → #36CFE0</div>
            <div style="flex:1;height:8mm;border-radius:6px;background:var(--grad-ia-claro);display:flex;align-items:center;padding:0 3mm;color:#fff;font-size:10px;font-weight:700">Gradiente IA claro · 135° #3B72FF → #17A9C2</div>
          </div>
          <div class="card" style="margin-top:4mm;display:flex;align-items:flex-end;gap:7mm">
            <div><div class="kick">Tipografía</div><div style="font-family:var(--font-display);font-weight:700;font-size:26px;letter-spacing:-.035em;line-height:1">Space Grotesk</div><div class="mono" style="font-size:9px;color:var(--tx3);margin-top:1mm">TITULARES · CIFRAS</div></div>
            <div><div style="font-size:19px;color:var(--tx2)">Manrope</div><div class="mono" style="font-size:9px;color:var(--tx3);margin-top:1mm">TEXTO · INTERFAZ</div></div>
            <div><div class="mono" style="font-size:16px;color:var(--tx2)">JetBrains Mono</div><div class="mono" style="font-size:9px;color:var(--tx3);margin-top:1mm">EYEBROWS · DATOS</div></div>
          </div>
        </div>
      </div>
      <div class="g" style="margin-top:5mm">
        <div class="s5 card"><div class="kick">Cinco reglas de oro</div><ol class="n">{''.join(f'<li style="margin-top:1.2mm;padding-left:8mm;font-size:11px">{r}</li>' for r in reglas)}</ol></div>
        <div class="s4 card"><div class="kick">Voz</div>
          <div class="yes">{SI}<span>«Validamos con datos si tu negocio puede captar antes de que gastes de más.»</span></div>
          <div class="yes">{SI}<span>«Si no encajamos, te lo decimos.»</span></div>
          <div class="nope">{NO}<span>«Lleva tu negocio al siguiente nivel.»</span></div>
          <div class="nope" style="border:none">{NO}<span>«Resultados garantizados.»</span></div></div>
        <div class="s3 card"><div class="kick">Botones</div>
          <div style="display:flex;flex-direction:column;gap:2.5mm;align-items:flex-start">
            <span style="background:var(--grad-ia-oscuro);color:#0B0D12;font-weight:700;font-size:11px;padding:2.2mm 4mm;border-radius:7px">Agendar 30 minutos →</span>
            <span style="background:#2C5BD0;color:#fff;font-weight:700;font-size:11px;padding:2.2mm 4mm;border-radius:7px">Elegir el mío →</span></div>
          <p style="margin-top:2.5mm;font-size:10.5px">Oscuro: gradiente + texto grafito. Claro: Azul 600 + blanco. Sin sombras.</p></div>
      </div>
      <div class="mono" style="margin-top:auto;font-size:9px;letter-spacing:.08em;color:var(--tx3);display:flex;justify-content:space-between">
        <span>Manual completo: 01_Guia_de_Marca/Oryzz_Guia_de_Marca_v2.pdf · Fuente de verdad: 00_Fuente_Maestra/BRAND_SPEC.md</span><span>oryzz.com</span></div>
    </div></section>"""
    escribir_pdf(documento(cuerpo, f'Oryzz · Guía de marca {gm.VERSION} · Resumen', css), 'resumen.html', RESUMEN, f'Oryzz · Guía de marca {gm.VERSION} · Resumen de una página')


# ----------------------------------------------------------------- espécimen tipográfico (16:9)

def especimen():
    gm.PAGES.clear(); gm.TOC.clear()
    gm.CAP['n'], gm.CAP['t'] = '04', 'Espécimen tipográfico'
    juego = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ<br>abcdefghijklmnñopqrstuvwxyz<br>0123456789 ¿?¡!()[]{}@#&amp;%€$+−×÷=→<br>ÁÉÍÓÚÜ áéíóúü ç «» “” ‘’ … · — –'

    fondo = gm.orbitas_fondo(1560, 560, [160, 280, 410, 550], 'oscuro', nodo_ang=-120)
    body = f"""<img src="{uri('02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg')}" style="height:56px;align-self:flex-start;margin-left:-6px">
    <div class="mta"><div class="eyebrow">Espécimen tipográfico · {gm.VERSION}</div>
      <div style="font-family:var(--font-display);font-weight:700;font-size:150px;line-height:.95;letter-spacing:-.05em;margin-top:24px">Space Grotesk</div>
      <div style="font-family:var(--font-texto);font-weight:400;font-size:96px;line-height:1.05;letter-spacing:-.02em;color:var(--tx2)">Manrope</div>
      <div style="font-family:var(--font-mono);font-weight:400;font-size:64px;line-height:1.3;color:var(--az)">JetBrains Mono</div>
      <p class="mt3" style="max-width:900px">Tres familias libres (SIL OFL 1.1) con un papel cada una: titular, leer y medir.</p></div>"""
    pg(body, 'oscuro', 'cover', fondo, pie=False)

    pesos = ''.join(f'<div style="display:flex;align-items:baseline;gap:28px;border-bottom:1px solid var(--borde);padding:10px 0"><span class="mono" style="width:150px;font-size:17px;color:var(--tx3)">{n} {w}</span>'
                    f'<span style="font-family:var(--font-display);font-weight:{w};font-size:58px;letter-spacing:-.035em;line-height:1.05">Más clientes. No más likes.</span></div>'
                    for w, n in [(300, 'Light'), (400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold')])
    body = f"""<div class="g grow"><div class="s4" style="display:flex;flex-direction:column"><div class="eyebrow">Display · titulares y cifras</div>
      <div style="font-family:var(--font-display);font-weight:700;font-size:300px;line-height:.85;letter-spacing:-.06em;margin-top:30px">Ag</div>
      <h3 class="mt3">Space Grotesk</h3><p class="mt1" style="font-size:22px">Florian Karsten · OFL. En la marca: 500, 600 y 700. 300 y 400 solo en cifras muy grandes.</p></div>
      <div class="s8">{pesos}<div class="mt3" style="font-family:var(--font-display);font-weight:500;font-size:30px;line-height:1.45;color:var(--tx2)">{juego}</div></div></div>"""
    pg(body, 'oscuro')

    esc = [(96, -.045, .95, 'Más clientes.'), (72, -.04, 1, 'Un sistema, no acciones sueltas.'), (56, -.035, 1.05, 'El problema no es que no te vean.'),
           (40, -.03, 1.1, 'Es que no te contactan.'), (28, -.02, 1.2, '30 minutos. Sales con un diagnóstico, no con un presupuesto.'), (20, -.01, 1.3, 'Validamos con datos si tu negocio puede captar antes de que gastes de más.')]
    filas = ''.join(f'<div style="display:flex;align-items:baseline;gap:30px;border-bottom:1px solid var(--borde);padding:10px 0"><span class="mono" style="width:120px;flex:none;font-size:17px;color:var(--az)">{s} px</span>'
                    f'<span style="font-family:var(--font-display);font-weight:{700 if s >= 40 else 600};font-size:{s}px;letter-spacing:{t}em;line-height:{lh};white-space:nowrap;overflow:hidden;text-overflow:clip">{txt}</span></div>'
                    for s, t, lh, txt in esc)
    body = head('Space Grotesk · en uso', 'Tracking negativo, <span class="az">frases cortas</span>') + f'<div class="mt3" style="border-top:1px solid var(--borde)">{filas}</div>'
    body += '<p class="mt2" style="font-size:20px;color:var(--tx3)">Cuanto más grande, más cerrado: −0,045 em a 96 px, −0,02 em a 28 px. Nunca en párrafos de más de dos líneas.</p>'
    pg(body, 'claro')

    pesos = ''.join(f'<div style="display:flex;align-items:baseline;gap:28px;border-bottom:1px solid var(--borde);padding:9px 0"><span class="mono" style="width:150px;font-size:17px;color:var(--tx3)">{n} {w}</span>'
                    f'<span style="font-family:var(--font-texto);font-weight:{w};font-size:40px;letter-spacing:-.01em">Te traemos clientes, no likes.</span></div>'
                    for w, n in [(400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold')])
    body = f"""<div class="g grow"><div class="s4" style="display:flex;flex-direction:column"><div class="eyebrow">Texto · párrafos e interfaz</div>
      <div style="font-family:var(--font-texto);font-weight:600;font-size:300px;line-height:.85;letter-spacing:-.04em;margin-top:30px">Ag</div>
      <h3 class="mt3" style="font-family:var(--font-texto)">Manrope</h3><p class="mt1" style="font-size:22px">Mikhail Sharanda · OFL. Cuerpo en 400; destacados en 600–700; 800 solo en botones grandes.</p></div>
      <div class="s8">{pesos}
        <div class="g mt3">
          <div class="s4"><div class="kick g3">16 px · web</div><p style="font-size:16px;line-height:1.6">Tu negocio ya recibe visitas, mensajes y llamadas. Lo que falla es lo que pasa después: mensajes que se responden tarde y llamadas que nadie devuelve.</p></div>
          <div class="s4"><div class="kick g3">20 px · entradilla</div><p style="font-size:20px;line-height:1.55">Un sistema conecta cada canal con una respuesta inmediata y un seguimiento medible.</p></div>
          <div class="s4"><div class="kick g3">36 px · slides</div><p style="font-size:36px;line-height:1.35">Activamos solo lo que tiene sentido.</p></div>
        </div></div></div>"""
    pg(body, 'oscuro')

    cifras = ''.join(f'<tr><td class="m" style="font-weight:400">{a}</td><td class="m" style="text-align:right;color:var(--tx)">{b}</td><td class="m" style="text-align:right">{c}</td></tr>'
                     for a, b, c in [('Citas agendadas', '61', '+18'), ('Coste por lead', '11,40 €', '−1,90 €'), ('CTR anuncios', '2,8 %', '+0,6 pp'), ('Reseñas nuevas', '31', '+12')])
    body = f"""<div class="g grow"><div class="s4" style="display:flex;flex-direction:column"><div class="eyebrow">Datos · eyebrows, métricas, código</div>
      <div style="font-family:var(--font-mono);font-weight:500;font-size:240px;line-height:.9;margin-top:30px">Ag</div>
      <h3 class="mt3" style="font-family:var(--font-mono);letter-spacing:0">JetBrains Mono</h3><p class="mt1" style="font-size:22px">JetBrains · OFL. 400 y 500; 700 solo para resaltar un dato en una tabla.</p></div>
      <div class="s8">
        <div class="kick g3">Eyebrow · 12 px web / 20 px slides · MAYÚSCULAS · +0,16 em</div>
        <div style="font-family:var(--font-mono);font-weight:500;font-size:24px;letter-spacing:.16em;text-transform:uppercase;color:var(--tx3);margin-top:8px">01 · Diagnóstico — 30 min</div>
        <div style="font-family:var(--font-mono);font-weight:500;font-size:24px;letter-spacing:.16em;text-transform:uppercase;color:var(--az);margin-top:8px">Sistema Oryzz · en marcha</div>
        <div class="kick g3 mt3">Cifras tabulares · Ejemplo</div>
        <table class="t"><tr><th>Métrica</th><th style="text-align:right">Septiembre</th><th style="text-align:right">vs. agosto</th></tr>{cifras}</table>
        <div class="kick g3 mt3">Código y URLs</div>
        <div style="font-family:var(--font-mono);font-size:26px;color:var(--tx2);line-height:1.6">cal.com/oryzz/30min · --color-cta-texto: #0B0D12;</div>
      </div></div>"""
    pg(body, 'oscuro')

    body = head('Pares de ejemplo', 'Las tres familias, <span class="az">juntas</span>')
    body += f"""<div class="g mt3 grow">
      <div class="s7 card" style="padding:52px;display:flex;flex-direction:column">
        <div class="eyebrow">Propuesta de captación · Ejemplo</div>
        <div style="font-family:var(--font-display);font-weight:700;font-size:72px;line-height:1;letter-spacing:-.04em;margin-top:20px">Más <span class="az">pacientes</span>.<br>Menos huecos.</div>
        <p style="margin-top:26px;font-size:26px">Anuncios, respuesta con IA y reseñas para llenar la agenda de primeras visitas.</p>
        <div class="mta" style="display:flex;gap:40px;border-top:1px solid var(--borde);padding-top:20px">
          <div><div class="eyebrow">Plazo</div><div style="font-family:var(--font-display);font-weight:500;font-size:44px;letter-spacing:-.03em">3–7 días</div></div>
          <div><div class="eyebrow">Coste por cita</div><div style="font-family:var(--font-display);font-weight:500;font-size:44px;letter-spacing:-.03em">11,40 €</div></div>
        </div>
      </div>
      <div class="s5" style="display:flex;flex-direction:column;gap:32px">
        <div class="card" style="background:#fff;border-color:{G['200']};color:{G['950']}">
          <div class="eyebrow" style="color:{G['500']}">02 · Contexto</div>
          <div style="font-family:var(--font-display);font-weight:700;font-size:40px;letter-spacing:-.03em;line-height:1.1;margin-top:12px">Dónde se pierden hoy tus clientes</div>
          <p style="color:{G['600']};font-size:22px;margin-top:12px">Antes de invertir un euro más en anuncios, miramos qué pasa con los que ya te escriben.</p></div>
        <div class="card"><div class="eyebrow">Citas este mes · Ejemplo</div>
          <div style="font-family:var(--font-display);font-weight:500;font-size:88px;letter-spacing:-.03em;line-height:1;margin-top:10px">61</div>
          <div class="mono" style="color:{C['lima']['500']};font-size:22px;margin-top:6px">▲ +18 vs. agosto</div></div>
      </div></div>"""
    pg(body, 'oscuro')

    filas = ''
    for k, v in TOK['type-scale-px'].items():
        fam = {'display': 'Space Grotesk', 'texto': 'Manrope', 'mono': 'JetBrains Mono'}[v['font']]
        filas += (f'<tr><td class="m" style="color:var(--az);font-weight:500">{k}</td><td>{fam}</td><td class="m">{v["weight"]}</td><td class="m">{v["size"]} px</td>'
                  f'<td class="m">{str(v["line"]).replace(".", ",")}</td><td class="m">{v["tracking"]}</td></tr>')
    body = head('Escala y tokens', 'Una escala <span class="az">para todos los soportes</span>')
    body += f'<table class="t compact mt3"><tr><th>Token</th><th>Familia</th><th>Peso</th><th>Web</th><th>Interl.</th><th>Tracking</th></tr>{filas}</table>'
    body += '<div class="g mt3"><div class="s4 rule"><div class="kick g3">Web</div><p style="font-size:22px">La escala de arriba, tal cual (<code>tokens.json</code> → <code>type-scale-px</code>). Mínimo 14 px.</p></div><div class="s4 rule"><div class="kick g3">Slides 1920×1080</div><p style="font-size:22px">Titulares 64–120 px · lectura ≥ 36 px · eyebrows y notas ≥ 24 px.</p></div><div class="s4 rule"><div class="kick g3">A4</div><p style="font-size:22px">Titular 22 pt · cuerpo 9,5 pt · mínimo 9 pt. Ya definidos en las plantillas Word.</p></div></div>'
    pg(body, 'claro')

    body = head('Instalación y licencia', 'Instalar, usar <span class="az">y compartir</span>')
    body += f"""<div class="g mt3">
      <div class="s4 rule"><div class="kick">Windows</div><p>Abre <code>04_Tipografia/TTF_estaticas</code>, selecciona todas las TTF › clic derecho › <strong>Instalar para todos los usuarios</strong>. Reinicia Office.</p></div>
      <div class="s4 rule"><div class="kick">Mac</div><p>Selecciona las TTF › doble clic › <strong>Instalar</strong> en Catálogo Tipográfico. También están gratis en Google Fonts.</p></div>
      <div class="s4 rule"><div class="kick">Web</div><p><code>11_Web_y_Codigo/fonts</code> con <code>@font-face</code> (WOFF2) o Google Fonts con <code>display=swap</code>. Alternativas: Arial y Consolas.</p></div>
      <div class="s4 rule"><div class="kick">Office · Google</div><p>Las plantillas Word y PowerPoint llevan las fuentes incrustadas. Google Docs y Slides: las tres están en «Más fuentes».</p></div>
      <div class="s4 rule"><div class="kick">Canva · Figma</div><p>Canva Pro: súbelas al Brand Kit. Figma: instaladas en el equipo o desde Google Fonts.</p></div>
      <div class="s4 rule"><div class="kick">Licencia</div><p>SIL Open Font License 1.1: uso comercial, incrustación y redistribución libres. No se venden por separado. Textos en <code>Licencias/</code>.</p></div>
    </div>
    <div class="card mt4"><p style="margin:0">Retiradas en la v2: <span style="text-decoration:line-through;color:var(--tx3)">Syne · Outfit · Montserrat · DM Sans · Poppins</span>. Si aparecen en una pieza, es una pieza antigua.</p></div>"""
    pg(body, 'oscuro')

    brand = (gm.MAESTRA / 'brand.css').resolve().as_uri()
    doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Oryzz · Espécimen tipográfico</title>'
           f'<link rel="stylesheet" href="{brand}"><style>{gm.CSS}</style></head><body>{"".join(gm.PAGES)}</body></html>')
    escribir_pdf(doc, 'especimen.html', ESPECIMEN, f'Oryzz · Espécimen tipográfico {gm.VERSION}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--png', metavar='CARPETA')
    a = ap.parse_args()
    resumen()
    especimen()
    if a.png:
        d = pathlib.Path(a.png)
        gm.exportar_png(RESUMEN, d / 'resumen', 1600)
        gm.exportar_png(ESPECIMEN, d / 'especimen', 1280)
