"""
Genera 11_Web_y_Codigo/componentes/componentes.html (librería de referencia, oscuro + claro,
con el CSS de cada componente listo para copiar) y su captura PNG de revisión.
Fuente del CSS: 11_Web_y_Codigo/componentes/oryzz-ui.css (bloques /* @comp x */ … /* @end */).

Uso:  python componentes_web.py
"""
import html, os, re
from render import html_to_png

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
DIR = os.path.join(ROOT, '11_Web_y_Codigo', 'componentes')
CSS = open(os.path.join(DIR, 'oryzz-ui.css'), encoding='utf8').read()
BLOQUES = dict(re.findall(r'/\* @comp (\w+) \*/\n(.*?)/\* @end \*/', CSS, flags=re.S))

L = '../../02_Logos'
FLECHA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def logo(tema, kind='horizontal'):
    way = 'color-sobre-oscuro' if tema == 'oscuro' else 'color-sobre-claro'
    if kind == 'tap':
        return f'{L}/07_Submarca_Tap/SVG/oryzz-tap-horizontal_{way}.svg'
    return f'{L}/01_Horizontal/SVG/oryzz-logo-horizontal_{way}.svg'


def demo(nombre, tema):
    if nombre == 'boton':
        return f'''<div class="fila"><a class="ox-btn ox-btn--primario ox-btn--lg" href="#">Agendar valoración {FLECHA}</a>
          <a class="ox-btn ox-btn--secundario ox-btn--lg" href="#">Ver qué hacemos</a></div>
          <div class="fila"><button class="ox-btn ox-btn--primario">Reservar 30 min</button><button class="ox-btn ox-btn--secundario">Cancelar</button>
          <button class="ox-btn ox-btn--primario ox-btn--sm">Enviar</button><button class="ox-btn ox-btn--primario ox-btn--sm" disabled>No disponible</button></div>
          <p class="ox-small">{'Gradiente IA + texto Grafito 950: 6,10:1 → 10,33:1' if tema == 'oscuro' else 'Azul 600 + texto blanco: 5,98:1 · hover Azul 700: 8,87:1'}</p>'''
    if nombre == 'enlace':
        return '''<p>Si no encajamos, te lo decimos. Lee la <a class="ox-link" href="#">política de privacidad</a> antes de reservar.</p>
          <p style="margin-top:12px"><a class="ox-link ox-link--flecha" href="#">Ver casos de clínicas</a></p>'''
    if nombre == 'eyebrow':
        return '''<div class="pila"><span class="ox-eyebrow">Qué hacemos</span><span class="ox-eyebrow ox-eyebrow--nodo">Valoración gratuita</span>
          <h3 class="ox-h3" style="margin-top:4px">Un sistema de captación, <span class="ox-resalte">no acciones sueltas</span>.</h3></div>'''
    if nombre == 'dato':
        return '''<div class="fila"><div class="ox-dato"><span class="ox-eyebrow">Coste por cita · Ejemplo</span>
          <span class="ox-dato__cifra">14,20<small>€</small></span><span class="ox-dato__delta">▼ 32 % vs. mes anterior</span>
          <span class="ox-dato__nota">Clínica dental · Meta Ads · {{dato}}</span></div>
          <div class="ox-dato"><span class="ox-eyebrow">Mensajes nuevos · Ejemplo</span>
          <span class="ox-dato__cifra">86</span><span class="ox-dato__delta">▲ 21 en 7 días</span><span class="ox-dato__nota">Centro estético · WhatsApp</span></div></div>'''
    if nombre == 'badge':
        return '''<div class="fila"><span class="ox-badge ox-badge--marcha">En marcha</span><span class="ox-badge ox-badge--info">Prueba inicial</span>
          <span class="ox-badge ox-badge--aviso">Pendiente</span><span class="ox-badge ox-badge--error">Pausada</span></div>'''
    if nombre == 'input':
        return '''<div class="fila" style="align-items:flex-start"><div class="ox-campo"><label for="n-%s">Nombre del negocio</label>
          <input class="ox-input" id="n-%s" placeholder="Clínica Dental Sonrisa"><span class="ox-ayuda">Lo usamos para preparar el diagnóstico.</span></div>
          <div class="ox-campo ox-campo--error"><label for="e-%s">Correo</label><input class="ox-input" id="e-%s" value="clinica@"><span class="ox-ayuda">Falta el dominio del correo.</span></div></div>''' % ((tema,) * 4)
    if nombre == 'navbar':
        tap = tema == 'claro'
        links = ['Productos', 'Líneas', 'Activación', 'Preguntas'] if tap else ['Qué hacemos', 'Agenda', 'Nosotros', 'Oryzz Tap']
        cta = 'Elegir el mío' if tap else 'Agendar valoración'
        return f'''<nav class="ox-nav" style="position:relative" aria-label="Principal"><a class="ox-nav__logo" href="#"><img src="{logo(tema, 'tap' if tap else 'horizontal')}" alt="{'Oryzz Tap' if tap else 'Oryzz'}"></a>
          <ul class="ox-nav__links">{''.join(f'<li><a href="#"{" aria-current=page" if i == 0 else ""}>{x}</a></li>' for i, x in enumerate(links))}</ul>
          <a class="ox-btn ox-btn--primario ox-btn--sm" href="#">{cta}</a></nav>
          <p class="ox-small" style="margin-top:10px">{'Oryzz Tap: mismo sistema en claro. Lockup «oryzz tap» en SVG.' if tap else 'Oryzz: logo horizontal SVG, 26 px de alto (≥ 88 px de ancho).'}</p>'''
    if nombre == 'footer':
        return f'''<footer class="ox-footer" style="padding:36px 24px 20px"><div class="ox-footer__grid"><div><img src="{logo(tema)}" alt="Oryzz">
          <p>Sistemas que captan clientes para PYMES. 100&nbsp;% en remoto.</p></div>
          <div><h4>Empresa</h4><ul><li><a href="#">Qué hacemos</a></li><li><a href="#">Oryzz Tap</a></li><li><a href="#">Contacto</a></li></ul></div>
          <div><h4>Síguenos</h4><ul><li><a href="#">Instagram · @oryzzai</a></li><li><a href="#">LinkedIn</a></li></ul></div></div>
          <div class="ox-footer__legal"><span>© 2026 Oryzz</span><span>Aviso legal · Privacidad · Cookies</span></div></footer>'''
    return ''


COMPS = [('boton', 'Botones', 'Un único primario por vista. Oscuro: gradiente IA con texto Grafito 950. Claro: Azul 600 con texto blanco. Corrige el texto blanco sobre gradiente de la web actual (1,88:1).'),
         ('enlace', 'Enlaces', 'Subrayados siempre en texto corrido. Azul 300 en oscuro (9,97:1) y Azul 600 en claro (5,98:1).'),
         ('eyebrow', 'Etiqueta y titular', 'Manrope 600 a 14 px, en tipo frase, sin tracking ni números. Un solo fragmento del titular en azul.'),
         ('dato', 'Tarjeta dato', 'Superficie, borde 1 px, radio 20 px. Cifra en Space Grotesk 500 y delta en color dato. Datos ficticios marcados como «Ejemplo».'),
         ('badge', 'Badge de estado', 'El color va en el punto; el texto se mantiene en gris legible. Nada de fondos saturados.'),
         ('input', 'Campo de formulario', 'Borde ≥ 3:1 respecto al fondo (WCAG 1.4.11), foco de 2 px y error comunicado con texto, no solo con color.'),
         ('navbar', 'Barra de navegación', 'Logo siempre en SVG (nunca texto vivo). Nombre del enlace: «Oryzz Tap», nunca «OryzzTAP».'),
         ('footer', 'Pie de página', 'Texto mínimo 14 px y gris Titanio 400 / Grafito 500 según tema (nunca #5A6172 sobre oscuro).')]

PAGE_CSS = """
body{margin:0;background:#0B0D12;font-family:'Manrope',Arial,sans-serif}
.doc{max-width:1360px;margin:0 auto;padding:72px 48px 96px}
.doc>header{display:grid;grid-template-columns:1.1fr 1fr;gap:48px;align-items:end;padding-bottom:40px;border-bottom:1px solid #232836}
.doc>header p{color:#D5D9E0;max-width:60ch;margin:16px 0 0}
.doc>header code{font-family:'JetBrains Mono',monospace;font-size:13px;color:#9FB8FF}
.comp{padding:56px 0;border-bottom:1px solid #232836}
.comp__head{display:grid;grid-template-columns:260px 1fr;gap:40px}
.comp__head h2{font-family:'Space Grotesk';font-size:28px;letter-spacing:-.02em;color:#fff;margin:10px 0 0}
.comp__head p{color:#8A90A0;font-size:15px;margin:10px 0 0;max-width:34ch}
.duo{display:grid;grid-template-columns:1fr 1fr;border:1px solid #232836;border-radius:20px;overflow:hidden}
.duo>div{padding:32px;min-height:120px}
.duo--pila{grid-template-columns:1fr}
.duo .t{font-family:'Manrope',sans-serif;font-size:14px;font-weight:600;letter-spacing:0;color:var(--color-texto-3);margin-bottom:20px;display:block}
.fila{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.fila+.fila,.fila+.ox-small{margin-top:16px}
.pila{display:flex;flex-direction:column;gap:14px;align-items:flex-start}
details{margin-top:18px;grid-column:2}
summary{cursor:pointer;font-family:'Manrope',sans-serif;font-size:14px;font-weight:600;letter-spacing:0;color:#9FB8FF}
pre{margin:12px 0 0;padding:20px;background:#12151D;border:1px solid #232836;border-radius:14px;overflow:auto;max-height:420px}
pre code{font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.6;color:#D5D9E0;white-space:pre}
@media (max-width:980px){.duo,.comp__head,.doc>header{grid-template-columns:1fr}details{grid-column:1}}
"""


def build(open_code=False):
    secciones = []
    for i, (k, titulo, desc) in enumerate(COMPS, 1):
        code = html.escape(BLOQUES[k].strip())
        secciones.append(f'''<section class="comp" id="{k}"><div class="comp__head">
          <div><span class="ox-eyebrow">Componente</span><h2>{titulo}</h2><p>{desc}</p></div>
          <div class="duo{' duo--pila' if k in ('navbar', 'footer') else ''}"><div class="ox" data-tema="oscuro"><span class="t">Oscuro · oryzz.com</span>{demo(k, 'oscuro')}</div>
          <div class="ox" data-tema="claro"><span class="t">Claro · oryzz.com/tap</span>{demo(k, 'claro')}</div></div>
          <details{' open' if open_code else ''}><summary>CSS para copiar · {k}</summary><pre><code>{code}</code></pre></details></div></section>''')
    base = html.escape(BLOQUES['base'].strip())
    page = f'''<!doctype html><html lang="es" data-tema="oscuro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Oryzz · Componentes web v2.0</title>
<link rel="stylesheet" href="../tokens/tokens.css">
<!-- Solo para la vista local (file://): tokens.css apunta a /fonts/ en producción -->
<style>
{open(os.path.join(ROOT, '11_Web_y_Codigo', 'fonts', 'fonts.css'), encoding='utf8').read().replace("url('/fonts/", "url('../fonts/")}
</style>
<link rel="stylesheet" href="oryzz-ui.css">
<style>{PAGE_CSS}</style></head>
<body class="ox" data-tema="oscuro"><div class="doc">
<header><div><span class="ox-eyebrow">Sistema web de Oryzz v2.0</span><h1 class="ox-h1" style="margin-top:18px">Componentes<br><span class="ox-resalte">de referencia</span>.</h1></div>
<div><p>Cada componente se muestra en los dos temas con el mismo HTML: solo cambia <code>data-tema="oscuro|claro"</code> en un contenedor. Enlaza <code>tokens/tokens.css</code> y <code>componentes/oryzz-ui.css</code>, o copia el bloque CSS de cada componente.</p>
<details style="grid-column:1"><summary>CSS base (tipografía)</summary><pre><code>{base}</code></pre></details></div></header>
{''.join(secciones)}
</div></body></html>'''
    return page


if __name__ == '__main__':
    out = os.path.join(DIR, 'componentes.html')
    open(out, 'w', encoding='utf8').write(build())
    prev = os.path.join(DIR, '_preview_tmp.html')
    open(prev, 'w', encoding='utf8').write(build(open_code=False))
    html_to_png(prev, os.path.join(DIR, 'componentes_preview.png'), 1440, 4900)
    os.remove(prev)
    print('ok')
