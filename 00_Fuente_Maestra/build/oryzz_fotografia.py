"""
oryzz_fotografia.py · Tratamientos fotográficos de ejemplo (velo grafito + texto + órbita).

El rectángulo con gradiente neutro es un MARCADOR DE FOTO: sustitúyelo por la imagen real
(en el SVG, el grupo id="foto"; en la plantilla HTML, la variable --foto).
Uso:  python oryzz_fotografia.py → 05_Elementos_Graficos/06_Fotografia
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oryzz_svg import C, THEME, ROOT, write, doc, T, text_width, arc, pol, gap_deg, embed_logo, png_from_svg, wrap

OUT = os.path.join(ROOT, '05_Elementos_Graficos', '06_Fotografia')


def foto(uid, w, h, tono='oscuro', nota=''):
    """Marcador de foto: gradiente neutro frío + grano sutil + etiqueta de dirección."""
    a, b = ('#6B7384', '#1A1E28') if tono == 'oscuro' else ('#E9ECF1', '#C9CED8')
    s = (f'<defs><linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="1">'
         f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
         f'<filter id="{uid}n" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>'
         f'<feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 .09 0"/></filter></defs>'
         f'<g id="foto"><rect width="{w}" height="{h}" fill="url(#{uid}g)"/>'
         f'<rect width="{w}" height="{h}" filter="url(#{uid}n)"/></g>')
    return s


def veil(uid, w, h, lado='izq', op_min=0.55, op_max=0.70):
    """Velo Grafito 950 al 55–70 % (BRAND_SPEC §5.6), más denso del lado del texto."""
    x1, x2 = ('0', '1') if lado == 'izq' else ('1', '0')
    y1 = y2 = '0'
    if lado == 'arriba':
        x1 = x2 = '0'; y1, y2 = '0', '1'
    return (f'<defs><linearGradient id="{uid}v" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{C["grafito-950"]}" stop-opacity="{op_max}"/>'
            f'<stop offset="1" stop-color="{C["grafito-950"]}" stop-opacity="{op_min}"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#{uid}v)"/>')


def nota(x, y, s, k, col, anchor='end'):
    return T(x, y, s.upper(), 'mono', 500, 14, col, tracking=0.12, anchor=anchor, contornos=k)


def orbita_foto(cx, cy, r, a_nodo, col, nodo, sw=2, op=.35, ab=48):
    cut = gap_deg(r, 12 + 12)
    nx, ny = pol(cx, cy, r, a_nodo)
    return (f'<path d="{arc(cx, cy, r, a_nodo + cut, a_nodo - ab)}" fill="none" stroke="{col}" stroke-width="{sw}" '
            f'stroke-linecap="round" opacity="{op}"/>'
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="12" fill="{nodo}"/>')


def boton(x, y, lab, k, h=60, fs=18):
    tw = text_width(lab, 'texto', 700, fs)
    w = 28 + tw + 28
    return (f'<defs><linearGradient id="btg" gradientUnits="userSpaceOnUse" x1="{x}" y1="{y}" x2="{x + w}" y2="{y + w}">'
            f'<stop offset="0" stop-color="{C["azul-400"]}"/><stop offset="1" stop-color="{C["cyan-500"]}"/></linearGradient></defs>'
            f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="14" fill="url(#btg)"/>'
            + T(x + 28, y + h / 2 + fs * 0.36, lab, 'texto', 700, fs, C['grafito-950'], contornos=k))


def t1(k):
    """16:9 · clínica · velo lateral + órbita que abraza al sujeto + titular."""
    w, h = 1920, 1080
    s = foto('f1', w, h)
    s += veil('f1', w, h, 'izq', 0.55, 0.70)
    s += orbita_foto(1340, 560, 420, -140, C['blanco'], C['lima-500'])
    lg, _ = embed_logo(120, 108, 176, 'horizontal', 'color-sobre-oscuro', uid='t1l'); s += lg
    s += T(120, 470, 'CLÍNICAS · ESTÉTICA · FITNESS', 'mono', 500, 16, C['grafito-200'], tracking=0.16, contornos=k)
    s += T(120, 576, 'Más clientes.', 'display', 700, 96, C['blanco'], tracking=-0.045, contornos=k)
    s += T(120, 668, 'No más likes.', 'display', 700, 96, C['blanco'], tracking=-0.045, contornos=k)
    s += T(120, 740, 'Un sistema de captación, no acciones sueltas.', 'texto', 400, 24, C['grafito-200'], contornos=k)
    s += boton(120, 800, 'Reserva tu valoración', k)
    s += nota(w - 64, h - 48, 'Marcador de foto · recepción de clínica, manos en el mostrador, luz lateral', k, C['grafito-400'])
    return doc(w, h, s, 'Oryzz · tratamiento fotográfico 16:9 · velo grafito + órbita',
               desc='Sustituye el grupo #foto por la imagen. Velo Grafito 950 70 % → 55 %. Órbita blanca al 35 % con nodo lima.')


def t2(k):
    """4:5 · post · velo superior, sujeto abajo, órbita recortada."""
    w, h = 1080, 1350
    s = foto('f2', w, h)
    s += veil('f2', w, h, 'arriba', 0.55, 0.70)
    s += orbita_foto(720, 1010, 360, -118, C['blanco'], C['lima-500'], op=.4)
    s += T(96, 170, 'GIMNASIO · EJEMPLO', 'mono', 500, 16, C['grafito-200'], tracking=0.16, contornos=k)
    y = 250
    for l in ['El problema no', 'es que no te vean.', 'Es que no te', 'contactan.']:
        s += T(96, y, l, 'display', 700, 76, C['blanco'], tracking=-0.04, contornos=k); y += 80
    s += T(96, y + 20, 'Te traemos clientes, no likes.', 'texto', 500, 26, C['grafito-200'], contornos=k)
    lg, _ = embed_logo(96, h - 128, 150, 'horizontal', 'color-sobre-oscuro', uid='t2l'); s += lg
    s += nota(w - 48, 64, 'Marcador de foto · entrenadora con cliente', k, C['grafito-400'])
    return doc(w, h, s, 'Oryzz · tratamiento fotográfico 4:5 · post con velo superior',
               desc='Velo Grafito 950 de arriba (70 %) a abajo (55 %). El sujeto ocupa el tercio inferior derecho.')


def t3(k):
    """4:5 · Oryzz Tap en claro · foto de producto sin velo, órbita en grafito."""
    w, h = 1080, 1350
    s = foto('f3', w, h, 'claro')
    s += f'<rect y="{h - 430}" width="{w}" height="430" fill="{C["blanco"]}"/>'
    # placa de producto (silueta) como guía de encuadre
    s += (f'<rect x="560" y="360" width="340" height="340" rx="44" fill="{C["blanco"]}" stroke="{C["grafito-200"]}" stroke-width="2" opacity=".9"/>'
          f'<path d="{arc(730, 530, 262, -30, -96)}" fill="none" stroke="{C["grafito-950"]}" stroke-width="2" opacity=".35" stroke-linecap="round"/>')
    nx, ny = pol(730, 530, 262, -44)
    s += f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="11" fill="{C["lima-600"]}"/>'
    s += T(560 + 170, 540, 'PLACA NFC + QR', 'mono', 500, 16, C['grafito-500'], tracking=0.12, anchor='middle', contornos=k)
    s += T(96, h - 330, 'ORYZZ TAP · RESEÑAS GOOGLE', 'mono', 500, 16, C['grafito-500'], tracking=0.16, contornos=k)
    s += T(96, h - 240, 'Tu negocio.', 'display', 700, 76, C['grafito-950'], tracking=-0.04, contornos=k)
    s += T(96, h - 160, 'A un toque.', 'display', 700, 76, C['grafito-950'], tracking=-0.04, contornos=k)
    s += T(96, h - 100, 'Acerca el teléfono y ocurre.', 'texto', 500, 26, C['grafito-600'], contornos=k)
    lg, _ = embed_logo(w - 96 - 190, h - 118, 190, 'tap', 'color-sobre-claro', uid='t3l'); s += lg
    s += nota(w - 48, 64, 'Marcador de foto · placa sobre mostrador de madera clara, luz de ventana', k, C['grafito-600'])
    return doc(w, h, s, 'Oryzz Tap · tratamiento fotográfico 4:5 · producto en claro',
               desc='Expresión Tap en claro: foto de producto luminosa sin velo, bloque de texto sobre blanco.')


TRAT = [('tratamiento-01_clinica_16x9', t1, 1920), ('tratamiento-02_post_4x5', t2, 1080), ('tratamiento-03_tap-producto_4x5', t3, 1080)]

PLANTILLA = '''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Plantilla foto con velo</title>
<link rel="stylesheet" href="../../00_Fuente_Maestra/brand.css">
<!-- Oryzz · plantilla de tratamiento fotográfico. Cambia --foto por tu imagen (ruta relativa o URL).
     Velo Grafito 950 70 % → 55 %. Un solo acento: el nodo lima. -->
<style>
:root{--foto:linear-gradient(135deg,#6B7384,#1A1E28)}
*{box-sizing:border-box} html,body{margin:0;background:var(--grafito-950)}
.pieza{position:relative;width:1920px;height:1080px;overflow:hidden;background:var(--foto) center/cover;font-family:var(--font-texto);color:#fff}
.pieza::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,13,18,.70),rgba(11,13,18,.55))}
.orb{position:absolute;inset:0}
.txt{position:absolute;left:120px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;max-width:880px}
.eb{font-family:var(--font-mono);font-size:16px;letter-spacing:.16em;text-transform:uppercase;color:var(--grafito-200);margin:0 0 28px}
h1{font-family:var(--font-display);font-weight:700;font-size:96px;letter-spacing:-.045em;line-height:.95;margin:0 0 24px}
p{font-size:24px;color:var(--grafito-200);margin:0 0 36px}
a.btn{align-self:flex-start;background:var(--grad-ia-oscuro);color:var(--grafito-950);font-weight:700;font-size:18px;padding:19px 28px;border-radius:14px;text-decoration:none}
.logo{position:absolute;left:120px;top:108px;width:176px}
</style></head><body><div class="pieza">
<svg class="orb" viewBox="0 0 1920 1080"><path d="ORBIT" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".35"/><circle cx="NX" cy="NY" r="12" fill="#BFF24A"/></svg>
<img class="logo" src="../../02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg" alt="oryzz">
<div class="txt"><p class="eb">Clínicas · estética · fitness</p><h1>Más clientes.<br>No más likes.</h1>
<p>Un sistema de captación, no acciones sueltas.</p><a class="btn" href="https://cal.com/oryzz/30min">Reserva tu valoración</a></div>
</div></body></html>'''


def build():
    jobs = []
    for name, fn, w in TRAT:
        write(os.path.join(OUT, 'SVG', name + '.svg'), fn(False))
        sp = os.path.join(OUT, 'SVG_contornos', name + '_contornos.svg'); write(sp, fn(True))
        jobs.append((sp, os.path.join(OUT, 'PNG', name + '.png'), w))
    png_from_svg(jobs)
    cut = gap_deg(420, 24); nx, ny = pol(1340, 560, 420, -140)
    html = (PLANTILLA.replace('ORBIT', arc(1340, 560, 420, -140 + cut, -188))
            .replace('NX', f'{nx:.1f}').replace('NY', f'{ny:.1f}'))
    write(os.path.join(OUT, 'plantilla-foto-velo_16x9.html'), html)


if __name__ == '__main__':
    build(); print('ok')
