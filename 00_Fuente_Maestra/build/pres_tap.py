"""
Oryzz Tap · plantilla de presentación (expresión clara) · placas y stands NFC + QR.
Mismo sistema que Oryzz (paleta, tipografías, retícula); lockup «oryzz tap»; es-CO; precios en COP (ejemplo).

    python pres_tap.py   -> 06_Presentaciones/_build/OryzzTap_Plantilla_Presentacion.pptx + HTML
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pres_engine import *          # noqa
from pres_assets import html_png, logo_png, ROOT, svg_png, svg_doc, orbit_system
from qr_svg import qr_group
import pres_oryzz as O

OUT, RES = O.OUT, O.RES
col, span, M, RIGHT = O.col, O.span, O.M, O.RIGHT
QR_URL = 'https://oryzz.com/tap'
C = O.LIGHT
TAP_RATIO = 4629.1 / 856.1


# ---------------------------------------------------------------- ilustraciones de producto (HTML -> PNG 2x)
def _qr(size, color='#0B0D12', fondo='#FFFFFF', pad=0):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="display:block">'
            f'{qr_group(QR_URL, 0, 0, size, color, fondo, radio=size * 0.06)}</svg>')


def _nfc(size, color):
    s = size
    arcs = ''.join(f'<path d="M{s * (0.30 + i * 0.16):.1f} {s * (0.28 - i * 0.06):.1f}a{s * (0.26 + i * 0.16):.1f} {s * (0.26 + i * 0.16):.1f} 0 0 1 0 {s * (0.44 + i * 0.12):.1f}" '
                   f'fill="none" stroke="{color}" stroke-width="{s * 0.07:.1f}" stroke-linecap="round"/>' for i in range(3))
    return f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block"><circle cx="{s * 0.16}" cy="{s * 0.5}" r="{s * 0.07}" fill="{color}"/>{arcs}</svg>'


def plate_html(w, h, kind='resenas', scale=1.0):
    """Frente de placa (10x10) o stand (10x16). w,h en px del lienzo."""
    dark = kind == 'pro'
    bg = '#0B0D12' if dark else '#FFFFFF'
    ink = '#FFFFFF' if dark else '#0B0D12'
    ink2 = '#8A90A0' if dark else '#5A6172'
    logo = os.path.join(RES, 'logo-tap_color-sobre-oscuro.png' if dark else 'logo-tap_color-sobre-claro.png').replace('\\', '/')
    pad = w * 0.09
    qr = w * 0.30
    if kind == 'pro':
        head, sub = 'Conecta<br>con nosotros', 'WhatsApp · Instagram · Web'
    else:
        head, sub = '¿Te gustó<br>tu visita?', 'Déjanos tu reseña en Google'
    return f'''
<div style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;border-radius:{w * 0.07}px;background:{bg};
     box-shadow:0 0 0 1px {'#232836' if dark else '#D5D9E0'}, 0 {w * 0.10}px {w * 0.16}px -{w * 0.10}px rgba(11,13,18,.28);overflow:hidden">
  <img src="file:///{logo}" style="position:absolute;left:{pad}px;top:{pad}px;height:{w * 0.075}px">
  <div style="position:absolute;left:{pad}px;top:{h * (0.30 if h > w else 0.27)}px;width:{w - 2 * pad}px;font:700 {w * 0.105}px/1.02 'Space Grotesk';letter-spacing:-.035em;color:{ink}">{head}</div>
  <div style="position:absolute;left:{pad}px;top:{h * (0.30 if h > w else 0.27) + w * 0.24}px;width:{w - 2 * pad}px;font:500 {w * 0.048}px/1.35 'Manrope';color:{ink2}">{sub}</div>
  <div style="position:absolute;left:{pad}px;bottom:{pad}px;display:flex;align-items:center;gap:{w * 0.03}px">
    {_nfc(w * 0.12, '#BFF24A' if dark else '#7FB02E')}
    <div style="font:500 {w * 0.034}px/1.3 'JetBrains Mono';letter-spacing:.12em;text-transform:uppercase;color:{ink2}">Acerca tu<br>teléfono</div>
  </div>
  <div style="position:absolute;right:{pad}px;bottom:{pad}px;padding:{w * 0.012}px;background:#FFFFFF;border-radius:{w * 0.03}px">{_qr(qr)}</div>
</div>'''


def make_tap_assets():
    A = {}
    A['tap_claro'] = logo_png('07_Submarca_Tap/SVG/oryzz-tap-horizontal_color-sobre-claro.svg', os.path.join(RES, 'logo-tap_color-sobre-claro.png'), 1800)
    A['tap_oscuro'] = logo_png('07_Submarca_Tap/SVG/oryzz-tap-horizontal_color-sobre-oscuro.svg', os.path.join(RES, 'logo-tap_color-sobre-oscuro.png'), 1800)
    surf = C['surf']
    orbit_bg = svg_doc(orbit_system(460, 540, [220, 330, 450, 580, 720], gap_start=-120, gap_step=57, gap=58, color='#D5D9E0',
                                    accent_i=None, sw=1.5), 920, 1080)
    orbit_url = 'file:///' + svg_png(os.path.join(RES, 'tap-orbitas-portada.png'), orbit_bg, 920, 1080).replace('\\', '/')
    # portada: placa + stand sobre Grafito 50 con órbitas
    A['cover'] = html_png(os.path.join(RES, 'tap-portada-producto.png'), f'''
<div style="position:absolute;inset:0;background:{surf}"></div>
<img src="{orbit_url}" style="position:absolute;left:0;top:0;width:920px;height:1080px">
<div style="position:absolute;left:150px;top:250px;transform:rotate(-6deg)">{plate_html(420, 420, 'resenas')}</div>
<div style="position:absolute;left:470px;top:470px;transform:rotate(5deg)">{plate_html(300, 480, 'pro')}</div>
<div style="position:absolute;left:64px;bottom:56px;font:500 20px/1 'JetBrains Mono';letter-spacing:.14em;color:#8A90A0">ILUSTRACIÓN DE PRODUCTO · SUSTITUIR POR FOTO</div>
''', 920, 1080, transparent=False)
    W2, H2 = 824, 420
    card = f'<div style="position:absolute;inset:0;background:{surf};border-radius:20px"></div>'
    # toque NFC
    phone = lambda x, y, w, rot=0, inner='': (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w * 2.05}px;border-radius:{w * 0.16}px;'
                                             f'border:3.5px solid #0B0D12;background:#FFFFFF;transform:rotate({rot}deg);overflow:hidden">'
                                             f'<div style="position:absolute;left:50%;top:{w * 0.06}px;width:{w * 0.28}px;height:{w * 0.07}px;margin-left:-{w * 0.14}px;border-radius:9px;background:#0B0D12"></div>{inner}</div>')
    arcs = ''.join(f'<div style="position:absolute;left:{360 - i * 34}px;top:{118 - i * 34}px;width:{80 + i * 68}px;height:{80 + i * 68}px;border-radius:50%;'
                   f'border:3px solid transparent;border-top-color:{"#7FB02E" if i == 0 else "#8A90A0"};transform:rotate(-20deg)"></div>' for i in range(3))
    A['tap_nfc'] = html_png(os.path.join(RES, 'tap-como-funciona-toque.png'), card + f'''
<div style="position:absolute;left:470px;top:150px">{plate_html(230, 230, 'resenas')}</div>
{phone(250, 40, 150, -18, '<div style="position:absolute;left:18px;right:18px;top:70px;height:10px;border-radius:5px;background:#E5E8EE"></div><div style="position:absolute;left:18px;width:70px;top:92px;height:10px;border-radius:5px;background:#E5E8EE"></div><div style="position:absolute;left:18px;right:18px;bottom:40px;height:44px;border-radius:22px;background:#2C5BD0"></div>')}
{arcs}
<div style="position:absolute;left:40px;bottom:32px;font:500 18px/1 'JetBrains Mono';letter-spacing:.14em;color:#5A6172">NFC · IPHONE Y ANDROID</div>''', W2, H2, transparent=True)
    # QR
    corners = ''.join(f'<div style="position:absolute;{v}:0;{hh}:0;width:34px;height:34px;border-{v}:4px solid #7FB02E;border-{hh}:4px solid #7FB02E;border-{v}-{hh}-radius:10px"></div>'
                      for v in ('top', 'bottom') for hh in ('left', 'right'))
    A['tap_qr'] = html_png(os.path.join(RES, 'tap-como-funciona-qr.png'), card + f'''
<div style="position:absolute;left:120px;top:110px">{plate_html(230, 230, 'resenas')}</div>
{phone(470, 40, 150, 0, f'<div style="position:absolute;left:22px;right:22px;top:92px;height:106px">{corners}<div style="position:absolute;left:14px;top:12px">{_qr(78)}</div></div><div style="position:absolute;left:18px;right:18px;bottom:40px;height:10px;border-radius:5px;background:#E5E8EE"></div>')}
<div style="position:absolute;left:40px;bottom:32px;font:500 18px/1 'JetBrains Mono';letter-spacing:.14em;color:#5A6172">QR · CUALQUIER CÁMARA</div>''', W2, H2, transparent=True)
    # líneas de producto
    A['linea_resenas'] = html_png(os.path.join(RES, 'tap-linea-resenas-google.png'), card + f'''
<div style="position:absolute;left:{(W2 - 300) / 2}px;top:60px">{plate_html(300, 300, 'resenas')}</div>''', W2, H2, transparent=True)
    A['linea_pro'] = html_png(os.path.join(RES, 'tap-linea-oryzz-pro.png'), card + f'''
<div style="position:absolute;left:{(W2 - 300) / 2}px;top:60px">{plate_html(300, 300, 'pro')}</div>''', W2, H2, transparent=True)
    # formatos con cotas (dibujo técnico)
    def dim_h(x, y, w, label):
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-top:1.5px solid #8A90A0"></div>'
                f'<div style="position:absolute;left:{x}px;top:{y - 8}px;height:16px;border-left:1.5px solid #8A90A0"></div>'
                f'<div style="position:absolute;left:{x + w}px;top:{y - 8}px;height:16px;border-left:1.5px solid #8A90A0"></div>'
                f'<div style="position:absolute;left:{x}px;top:{y + 12}px;width:{w}px;text-align:center;font:500 17px/1 \'JetBrains Mono\';letter-spacing:.08em;color:#5A6172">{label}</div>')

    def dim_v(x, y, h, label):
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;height:{h}px;border-left:1.5px solid #8A90A0"></div>'
                f'<div style="position:absolute;left:{x - 8}px;top:{y}px;width:16px;border-top:1.5px solid #8A90A0"></div>'
                f'<div style="position:absolute;left:{x - 8}px;top:{y + h}px;width:16px;border-top:1.5px solid #8A90A0"></div>'
                f'<div style="position:absolute;left:{x + 14}px;top:{y + h / 2 - 9}px;font:500 17px/1 \'JetBrains Mono\';letter-spacing:.08em;color:#5A6172">{label}</div>')
    A['formato_placa'] = html_png(os.path.join(RES, 'tap-formato-placa-10x10.png'), card + f'''
<div style="position:absolute;left:272px;top:48px">{plate_html(280, 280, 'resenas')}</div>
{dim_h(272, 356, 280, '100 MM')}{dim_v(584, 48, 280, '100 MM')}''', W2, H2, transparent=True)
    side = ('<svg width="130" height="300" viewBox="0 0 130 300" style="position:absolute;left:560px;top:52px;overflow:visible">'
            '<path d="M24 6 L42 6 L112 290 L8 290 Z" fill="#FFFFFF" stroke="#0B0D12" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M24 6 L8 290" stroke="#D5D9E0" stroke-width="2"/></svg>')
    A['formato_stand'] = html_png(os.path.join(RES, 'tap-formato-stand-10x16x4.png'), card + f'''
<div style="position:absolute;left:240px;top:52px">{plate_html(180, 288, 'resenas')}</div>
{side}
{dim_h(240, 366, 180, '100 MM')}{dim_v(206, 52, 288, '') }
<div style="position:absolute;left:120px;top:186px;font:500 17px/1 'JetBrains Mono';letter-spacing:.08em;color:#5A6172">160 MM</div>
{dim_h(568, 366, 104, '40 MM')}
<div style="position:absolute;left:240px;top:22px;font:500 14px/1 'JetBrains Mono';letter-spacing:.14em;color:#8A90A0">FRENTE</div><div style="position:absolute;left:568px;top:22px;font:500 14px/1 'JetBrains Mono';letter-spacing:.14em;color:#8A90A0">PERFIL</div>''', W2, H2, transparent=True)
    return A


# ---------------------------------------------------------------- layouts Tap
def make_tap_layouts(theme, A, base):
    c = theme.c
    s = O.styles(c)
    L = dict(base)
    iso = Img(M, FOOTER_Y, 24, 24, A['iso'], name='Isotipo pie')
    logo = Img(M, M - 8, 44 * TAP_RATIO, 44, A['logo'], name='Logo oryzz tap', descr='oryzz tap')
    L['T1 Tap · Portada producto'] = Layout('T1 Tap · Portada producto', [Box(1000, 0, 920, H, fill=c['ph_bg'], name='Fondo foto'), logo], [
        PH(11, 'pic', 1000, 0, 920, H, 'Foto de producto', name='Foto de producto'),
        PH(10, 'body', M, 388, 820, 34, 'ETIQUETA', name='Etiqueta', **s['eyebrow']),
        PH(0, 'title', M, 432, 840, 340, 'Titular de portada', **merged(s['cover'], dict(size=80))),
        PH(12, 'body', M, 790, 800, 140, 'Subtítulo.', name='Subtítulo', **merged(s['lead'], dict(size=22))),
        PH(13, 'body', M, 968, 820, 30, 'SHOP.ORYZZ.COM', name='Meta', **s['meta']),
    ], footer=False, number=False)
    st = [iso]
    phs = [PH(10, 'body', M, M, 1000, 34, 'ETIQUETA', name='Etiqueta', **s['eyebrow']),
           PH(0, 'title', M, 160, W - 2 * M, 120, 'Título', **s['title'])]
    for k, x in enumerate((col(0), col(6))):
        st.append(Box(x, 300, span(6), 420, fill=c['surf'], r=20, name='Fondo imagen'))
        b = 11 + k * 4
        phs += [PH(b, 'pic', x, 300, span(6), 420, 'Imagen', name=f'Imagen {"AB"[k]}', r=20),
                PH(b + 1, 'body', x, 752, span(6), 34, 'ETIQUETA', name=f'Etiqueta {"AB"[k]}', **merged(s['eyebrow'], dict(color=c['hl']))),
                PH(b + 2, 'body', x, 796, span(6), 70, 'Titular', name=f'Titular {"AB"[k]}', **s['h3']),
                PH(b + 3, 'body', x, 866, span(6) - 40, 116, 'Texto breve.', name=f'Texto {"AB"[k]}', **s['body18'])]
    L['T2 Tap · Dos columnas con imagen'] = Layout('T2 Tap · Dos columnas con imagen', st, phs)
    return L


def tap_slides(theme, L, A):
    c = theme.c
    SHOP = 'https://shop.oryzz.com'
    S = []
    S.append(Slide(L['T1 Tap · Portada producto'], {
        11: A['cover'], 10: 'ORYZZ TAP · PLACAS NFC + QR', 0: 'Tu negocio.\n**A un toque.**',
        12: 'Placas y stands NFC + QR para sumar reseñas en Google con un solo toque.',
        13: 'SHOP.ORYZZ.COM · ENVÍOS EN COLOMBIA'},
        notes='Sustituye la ilustración por una foto real del producto (clic derecho > Cambiar imagen).'))
    S.append(Slide(L['05 Título + texto'], {
        10: 'EL PROBLEMA', 0: 'Tus clientes salen contentos. **Pero no te dejan reseña.**',
        12: 'Pedir una reseña da pena y buscar tu ficha en Google es lento. Casi nadie lo hace por su cuenta.',
        11: [P('Con Oryzz Tap, la reseña está a un toque: el cliente acerca el teléfono y se abre tu ficha lista para valorar.', sa=16),
             P('Sin descargar apps y sin buscar nada.')]}))
    S.append(Slide(L['08 Cifra gigante'], {
        10: 'CÓMO SE SIENTE', 11: '1', 12: 'toque',
        13: 'Es lo que separa a tu cliente de tu ficha de Google. Si su teléfono no tiene NFC, escanea el QR.',
        14: 'NFC EN IPHONE Y ANDROID COMPATIBLES · QR PARA EL RESTO'}))
    S.append(Slide(L['T2 Tap · Dos columnas con imagen'], {
        10: 'CÓMO FUNCIONA', 0: 'Acerca el teléfono **y ocurre**',
        11: A['tap_nfc'], 12: '01 · TOQUE NFC', 13: 'Acerca el teléfono', 14: 'El chip NFC abre tu enlace al instante. No necesita batería ni app.',
        15: A['tap_qr'], 16: '02 · CÓDIGO QR', 17: 'O escanea el código', 18: 'Para teléfonos sin NFC: la cámara lee el QR y abre el mismo enlace.'}))
    S.append(Slide(L['T2 Tap · Dos columnas con imagen'], {
        10: 'LÍNEAS DE PRODUCTO', 0: 'Dos líneas, **un mismo gesto**',
        11: A['linea_resenas'], 12: 'LÍNEA 01', 13: 'Reseñas Google', 14: 'Abre tu ficha para dejar la reseña. Más valoraciones, mejor posición en Maps.',
        15: A['linea_pro'], 16: 'LÍNEA 02', 17: 'Oryzz Pro', 18: 'Abre tu perfil con WhatsApp, redes y web en un solo enlace. Para mostrador, tarjeta o mesa.'}))
    S.append(Slide(L['T2 Tap · Dos columnas con imagen'], {
        10: 'FORMATOS', 0: 'Placa o stand, **según dónde lo pongas**',
        11: A['formato_placa'], 12: 'PLACA · 10 × 10 CM', 13: 'Para pared, puerta o caja', 14: 'Adhesiva y discreta. Ideal junto a la caja o a la salida.',
        15: A['formato_stand'], 16: 'STAND · 10 × 16 × 4 CM', 17: 'Para mostrador o mesa', 18: 'Se sostiene sola y queda a la vista del cliente mientras paga.'}))
    S.append(Slide(L['12 Proceso en pasos'], {
        10: 'ACTIVACIÓN', 0: 'Listo en 4 pasos',
        11: 'Pide', 12: 'Enlaza', 13: 'Recibe', 14: 'Prueba',
        15: 'Elige formato y línea en shop.oryzz.com.',
        16: 'Nos pasas el enlace de tu ficha de Google o de tu perfil.',
        17: 'Te llega la placa programada con NFC y QR.',
        18: 'La colocas y la pruebas con tu teléfono. Nada más.'}))
    S.append(Slide(L['18 Precios / planes'], {
        10: 'PRECIOS · EJEMPLO', 0: 'Pago único. **Sin mensualidades.**',
        11: 'Precios de ejemplo en pesos colombianos (COP). Vigentes en shop.oryzz.com.',
        12: 'RESEÑAS GOOGLE', 13: 'Placa 10 × 10', 14: {'text': '$89.000', 'size': 50}, 15: 'COP · pago único · ejemplo', 16: ['NFC + QR a tu ficha', 'Adhesivo incluido', 'Envío en Colombia'],
        17: 'MÁS ELEGIDO', 18: 'Stand de mesa', 19: {'text': '$119.000', 'size': 50}, 20: 'COP · pago único · ejemplo', 21: ['NFC + QR a tu ficha', '10 × 16 × 4 cm', 'Envío en Colombia'],
        22: 'ORYZZ PRO', 23: 'Perfil Oryzz Pro', 24: {'text': '$149.000', 'size': 50}, 25: 'COP · pago único · ejemplo', 26: ['Placa o stand', 'WhatsApp, redes y web', 'Envío en Colombia']}))
    S.append(Slide(L['23 Lista de seis'], {
        10: 'DÓNDE FUNCIONA', 0: 'Donde tu cliente\n**ya está contento**',
        11: 'En el mostrador, en la mesa o a la salida: justo cuando termina la experiencia.',
        12: 'Restaurantes y cafés', 13: 'En la mesa o junto a la caja, cuando llega la cuenta.',
        14: 'Clínicas y consultorios', 15: 'En recepción, al salir de la cita.',
        16: 'Peluquerías y estética', 17: 'En el tocador, con el resultado recién hecho.',
        18: 'Gimnasios', 19: 'En la entrada, para reseñas y para compartir el perfil.',
        20: 'Hoteles', 21: 'En la recepción y en la habitación.',
        22: 'Tiendas', 23: 'Junto al datáfono, mientras el cliente paga.'}))
    S.append(Slide(L['24 Llamada a la acción'], {
        10: 'PEDIDOS', 0: 'Pide tu placa.\n**Suma reseñas.**',
        11: 'Empresas y volumen: pedidos@oryzz.com',
        12: [P([Rn('shop.oryzz.com   →', link=SHOP)])],
        13: 'ENVÍOS EN COLOMBIA'}))
    S.append(Slide(L['25 Cierre'], {
        10: 'TU NEGOCIO. A UN TOQUE.', 0: 'Gracias.',
        11: [P([Rn('oryzz.com/tap', color=c['text'])]), P([Rn('pedidos@oryzz.com', link='mailto:pedidos@oryzz.com')]), P('@oryzztap · TikTok @oryzz.tap')]}))
    return S


def build(out_pptx=None, out_html=None):
    theme = O.make_theme(False, footer_text='Oryzz Tap · Tu negocio. A un toque.', lang='es-CO', name='Tap Claro')
    A = O.make_assets(theme)
    A.update(make_tap_assets())
    A['logo'] = A['tap_claro']; A['logo_ratio'] = TAP_RATIO; A['logo_descr'] = 'oryzz tap'
    base = O.make_layouts(theme, A)
    L = make_tap_layouts(theme, A, base)
    slides = tap_slides(theme, L, A)
    print(f'· tap: {len(slides)} slides, {len(L)} layouts')
    qa_fit(slides, label='tap')
    b = PptxBuilder(theme, list(L.values()))
    for S in slides:
        b.add(S)
    if out_pptx:
        b.save(out_pptx)
    if out_html:
        html_deck(slides, theme, out_html, os.path.relpath(os.path.join(ROOT, '00_Fuente_Maestra', 'brand.css'), os.path.dirname(out_html)).replace('\\', '/'),
                  'Oryzz Tap · Plantilla de presentación')
    return slides


if __name__ == '__main__':
    tmp = os.path.join(OUT, '_build')
    os.makedirs(tmp, exist_ok=True)
    build(os.path.join(tmp, 'OryzzTap_Plantilla_Presentacion.pptx'), os.path.join(tmp, 'tap.html'))
