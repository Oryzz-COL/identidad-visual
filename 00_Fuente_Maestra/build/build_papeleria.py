"""
Oryzz · genera 10_Papeleria_e_Impresion (PDF imprenta con/sin marcas, SVG editables, PNG de vista previa).

    python build_papeleria.py            # todo
    python build_papeleria.py tarjetas   # grupos: tarjetas papeleria pegatinas tap gran_formato merch
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from print_kit import *  # noqa
from orbitas import orbitas_group
from qr_svg import qr_group

OUT = os.path.join(ROOT, '10_Papeleria_e_Impresion')
D = lambda *p: os.path.join(OUT, *p)

PERSONAS = [
    ('juan-salazar', 'Juan Salazar', 'Estrategia y Ads', '{{juan@oryzz.com}}', '{{+34 600 000 000}}'),
    ('david-morales', 'David Morales', 'Automatización e IA', '{{david@oryzz.com}}', '{{+34 600 000 000}}'),
]
URL_QR_TARJETA = 'https://oryzz.com'
URL_QR_TAP = 'https://oryzz.com/tap'          # sustituir por la URL de activación definitiva
URL_QR_AGENDA = 'https://cal.com/oryzz/30min'


def nodo(cx, cy, r, color, relleno=None, trazo=None):
    """Nodo de paso: los pasos se distinguen por nodo y título, nunca por número (BRAND_SPEC §4)."""
    sw = trazo if trazo is not None else r * 0.45
    return (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{relleno or "none"}" '
            f'stroke="{color}" stroke-width="{sw:.3f}"/>')


# ============================================================ 1. TARJETAS 85 × 55
def tarjetas():
    W, H = 85, 55
    for tema in ('oscura', 'clara'):
        osc = tema == 'oscura'
        bg = C['g950'] if osc else C['w']
        ink = C['w'] if osc else C['g950']
        ink2 = C['g200'] if osc else C['g600']
        ink3 = C['g400'] if osc else C['g500']
        way = 'color-sobre-oscuro' if osc else 'color-sobre-claro'
        # anverso: identidad
        lg, lw, lh = logo('h', way, 7, 19.5, w=38)
        orb = orbitas_group(86, 54, [9, 17, 25, 33], trazo=C['g700'] if osc else C['g100'], grosor=0.25,
                            nodo=C['li500'] if osc else C['li600'], nodo_en=2, nodo_r=1.0, nodo_ang=240)
        anverso = (fondo(W, H, bg) + orb + lg +
                   text(7, 48, 'Sistemas que captan clientes.', 9, 'display', 500, ink2, track=-0.01))
        for slug, nombre, rol, mail, tel in PERSONAS:
            iso, _, _ = logo('i', way, 71.5, 6.5, w=7)
            qr = qr_group(URL_QR_TARJETA, 60.5, 27.5, 19, C['g950'], fondo=C['w'], radio=1.6)
            reverso = (fondo(W, H, bg) + iso +
                       text(7, 13.2, nombre, 13, 'display', 600, ink, track=-0.02) +
                       text(7, 19.2, rol, 9, 'texto', 600, ink3) +
                       lines(7, 36.5, [mail, tel, 'oryzz.com'], 9, 1.5, font='texto', weight=500, fill=ink) +
                       (rect(60, 27, 20, 20, 'none', 2.2, f' stroke="{C["g200"]}" stroke-width="0.25"') if not osc else '') +
                       qr)
            exportar(f'oryzz_tarjeta_{slug}_{tema}', D('01_Tarjetas_de_Visita'), W, H,
                     [('anverso', anverso), ('reverso', reverso)], info=f'Oryzz · Tarjeta {nombre} · {tema}')


# ============================================================ 2. MEMBRETE, SOBRE, CARPETA
def papeleria():
    # --- Membrete A4
    W, H = 210, 297
    lg, _, _ = logo('h', 'color-sobre-claro', 20, 18, w=34)
    orb = orbitas_group(213, 300, [20, 34, 48, 62], trazo=C['g100'], grosor=0.3, nodo=None)
    body = (fondo(W, H, C['w']) + orb + lg +
            lines(190, 21, ['oryzz.com', 'cal.com/oryzz/30min', 'linkedin.com/company/oryzz'], 9, 1.55, font='texto', weight=500, fill=C['g500'], anchor='end') +
            f'<line x1="20" y1="281" x2="150" y2="281" stroke="{C["g100"]}" stroke-width="0.25"/>' +
            text(20, 287, 'Oryzz', 9, 'texto', 600, C['g950']) +
            text(32, 287, 'Sistemas que captan clientes', 9, 'texto', 500, C['g500']) +
            text(96, 287, '{{Razón social}} · NIF {{B00000000}}', 9, 'texto', 500, C['g500']))
    exportar('oryzz_membrete_A4', D('02_Membrete_Sobre_Carpeta'), W, H, [('', body)], info='Oryzz · Membrete A4')

    # --- Sobre DL 220 × 110
    W, H = 220, 110
    lg, _, _ = logo('h', 'color-sobre-claro', 14, 12, w=34)
    orb = orbitas_group(224, 114, [18, 30, 42], trazo=C['g100'], grosor=0.3, nodo=None)
    frente = (fondo(W, H, C['w']) + orb + lg +
              lines(14, 29, ['Oryzz · {{Dirección}}', '{{CP}} {{Ciudad}} · España'], 9, 1.5, font='texto', weight=500, fill=C['g500']))
    iso, _, _ = logo('i', 'color-sobre-claro', 104, 24, w=12)
    dorso = (fondo(W, H, C['w']) + iso + text(110, 44, 'oryzz.com', 9, 'texto', 500, C['g500'], 'middle') +
             text(110, 92, 'Más clientes. No más likes.', 9, 'display', 500, C['g600'], 'middle'))
    exportar('oryzz_sobre_DL', D('02_Membrete_Sobre_Carpeta'), W, H, [('frente', frente), ('dorso', dorso)], info='Oryzz · Sobre DL')

    # --- Carpeta A4 con bolsillo. Pliego abierto 445 × 410 mm, visto desde el EXTERIOR:
    #     contraportada (0–220) | lomo 5 mm (220–225) | portada (225–445); solapa-bolsillo de 100 mm bajo la contraportada.
    #     Al plegar la solapa hacia dentro, su cara exterior queda a la vista (girada 180°) en el panel derecho interior.
    W, H = 445, 410
    P0 = 225
    troquel = (f'<path d="M0 0H{W}V310H220V{H - 8}L212 {H}H8L0 {H - 8}Z"/>'
               f'<g stroke-dasharray="3 2"><line x1="220" y1="0" x2="220" y2="310"/><line x1="{P0}" y1="0" x2="{P0}" y2="310"/>'
               f'<line x1="0" y1="310" x2="220" y2="310"/></g>'
               f'<path d="M150 392 l-10 6 M190 392 l10 6"/>')
    lg, _, _ = logo('h', 'color-sobre-oscuro', P0 + 24, 36, w=72)
    orb = orbitas_group(W + 10, 260, [40, 62, 84, 106, 128, 150], trazo=C['g700'], grosor=0.35, nodo=C['li500'], nodo_en=2, nodo_r=2.4, nodo_ang=200)
    iso, _, _ = logo('i', 'mono-blanco', 104, 250, w=12)
    flap_txt = (text(24, 310 + 30, 'Más clientes. No más likes.', 14, 'display', 600, C['w'], track=-0.02) +
                text(24, 310 + 40, 'cal.com/oryzz/30min', 9, 'texto', 500, C['g400']))
    exterior = (rect(-3, -3, W + 6, 313, C['g950']) + rect(-3, 310, 226, 103, C['g950']) + orb + lg +
                text(P0 + 24, 262, 'Sistemas que', 30, 'display', 700, C['w'], track=-0.035) +
                text(P0 + 24, 275, 'captan clientes.', 30, 'display', 700, C['az400'], track=-0.035) +
                text(P0 + 24, 292, 'oryzz.com', 9, 'texto', 500, C['g400']) +
                iso + text(110, 272, 'oryzz.com', 9, 'texto', 500, C['g400'], 'middle') +
                f'<g transform="rotate(180 110 360)">{flap_txt}</g>' +
                rect(223, 310, W - 220, 103, C['w']))
    interior = (rect(-3, -3, W + 6, 313, C['g50']) + rect(P0 - 3, 310, W - P0 + 6, 103, C['g50']) +
                logo('i', 'color-sobre-claro', 20, 20, w=10)[0] +
                text(20, 296, 'oryzz.com', 9, 'texto', 500, C['g500']) +
                rect(-3, 310, P0, 103, C['w']))
    exportar('oryzz_carpeta_A4', D('02_Membrete_Sobre_Carpeta'), W, H, [('exterior', exterior), ('interior', interior)],
             troquel=troquel, info='Oryzz · Carpeta A4 con bolsillo (pliego abierto, troquel visto desde el exterior)', preview_dpi=60)


# ============================================================ 3. PEGATINAS Y ETIQUETAS
def pegatinas():
    # Sticker circular isotipo Ø 50
    W = H = 50
    iso, _, _ = logo('i', 'color-sobre-oscuro', 12, 12, w=26)
    body = fondo(W, H, C['g950']) + iso
    exportar('oryzz_sticker_isotipo_50mm', D('03_Pegatinas_y_Etiquetas'), W, H, [('', body)],
             troquel=f'<circle cx="25" cy="25" r="25"/>', info='Oryzz · Sticker circular isotipo Ø 50 mm')

    # Sticker Oryzz Tap 70 × 35 (esquinas r 6)
    W, H = 70, 35
    lg, _, _ = logo('t', 'color-sobre-claro', 6, 6.5, w=30)
    body = (fondo(W, H, C['w']) + lg +
            text(6, 25, 'Acerca tu', 12, 'display', 600, C['g950'], track=-0.02) +
            text(6, 30, 'teléfono.', 12, 'display', 600, C['az500'], track=-0.02) +
            rect(46, 6, 18, 23, C['g950'], 3) + nfc_icon(48.5, 9.5, 13, C['w']) +
            f'<circle cx="55" cy="25" r="0.9" fill="{C["li500"]}"/>')
    exportar('oryzz-tap_sticker_acerca-tu-telefono_70x35', D('03_Pegatinas_y_Etiquetas'), W, H, [('', body)],
             troquel=f'<rect x="0" y="0" width="{W}" height="{H}" rx="6"/>', info='Oryzz Tap · Sticker 70 × 35 mm')

    # Etiqueta de caja de envío Oryzz Tap 100 × 60
    W, H = 100, 60
    lg, _, _ = logo('t', 'color-sobre-claro', 6, 6, w=32)
    qr = qr_group(URL_QR_TAP, 76, 30, 18, C['g950'])
    body = (fondo(W, H, C['w']) + lg +
            text(94, 9.6, 'Pedido {{#0000}}', 9, 'mono', 500, C['g500'], 'end') +
            text(6, 26, 'Tu negocio.', 14, 'display', 700, C['g950'], track=-0.03) +
            text(6, 32, 'A un toque.', 14, 'display', 700, C['az500'], track=-0.03) +
            f'<line x1="6" y1="37" x2="70" y2="37" stroke="{C["g100"]}" stroke-width="0.25"/>' +
            text(6, 42.5, 'Para', 9, 'texto', 600, C['g500']) + text(16, 42.5, '{{Nombre del negocio}}', 9, 'texto', 600, C['g950']) +
            text(6, 47.5, 'Contiene', 9, 'texto', 600, C['g500']) + text(21, 47.5, '{{1 × Placa Reseñas Google}}', 9, 'texto', 500, C['g950']) +
            text(6, 54, 'shop.oryzz.com · pedidos@oryzz.com', 9, 'texto', 500, C['g500']) +
            qr + text(85, 52, 'Actívala aquí', 9, 'texto', 500, C['g600'], 'middle'))
    exportar('oryzz-tap_etiqueta-caja-envio_100x60', D('03_Pegatinas_y_Etiquetas'), W, H, [('', body)],
             troquel=f'<rect x="0" y="0" width="{W}" height="{H}" rx="3"/>', info='Oryzz Tap · Etiqueta de caja 100 × 60 mm')


# ============================================================ 4. TARJETA DE PRODUCTO TAP · A6
def tarjeta_tap():
    W, H = 105, 148
    lg, _, _ = logo('t', 'color-sobre-claro', 10, 11, w=36)
    pasos = [('Escanea el QR', ['o entra en oryzz.com/tap desde tu teléfono.']),
             ('Escribe tu código', ['Está en el reverso de la placa:', '{{XXXX-XXXX}}']),
             ('Elige a dónde lleva', ['Tu reseña de Google, tu WhatsApp', 'o tu perfil Oryzz Pro.']),
             ('Colócala y pruébala', ['Déjala a la vista y acerca', 'tu teléfono. Ya está.'])]
    y0 = 57
    st = ''
    for i, (t, d) in enumerate(pasos):
        y = y0 + i * 16.5
        st += f'<line x1="10" y1="{y - 5}" x2="95" y2="{y - 5}" stroke="{C["g200"]}" stroke-width="0.25"/>'
        st += nodo(12.5, y - 1.3, 1.3, C['az600'], relleno=C['az600'] if i == len(pasos) - 1 else None)
        st += text(20, y, t, 10.5, 'display', 600, C['g950'], track=-0.01)
        st += lines(20, y + 4.6, d, 9, 1.4, font='texto', fill=C['g600'])
    qr = qr_group(URL_QR_TAP, 71, 118, 24, C['g950'], fondo=C['w'], radio=1.6)
    frente = (fondo(W, H, C['g50']) + lg +
              text(10, 32, 'Tu placa ya está lista.', 17, 'display', 700, C['g950'], track=-0.035) +
              text(10, 39.5, 'Actívala en 2 minutos.', 17, 'display', 700, C['az500'], track=-0.035) +
              st + qr +
              lines(10, 128, ['¿Dudas? Escríbenos:', 'pedidos@oryzz.com'], 9, 1.45, font='texto', fill=C['g600']) +
              text(10, 139, 'oryzz.com/tap', 9, 'texto', 600, C['g950']))
    orb = orbitas_group(122, 150, [18, 32, 46, 60], trazo=C['g700'], grosor=0.3, nodo=C['li500'], nodo_en=2, nodo_r=1.4, nodo_ang=205)
    tips = [('Cerca del pago', 'Colócala junto a la caja o el mostrador: es donde tu cliente ya tiene el teléfono en la mano.'),
            ('Invita a acercarlo', '«¿Nos dejas tu opinión? Acerca el teléfono aquí.» Una frase basta.'),
            ('iPhone y Android', 'En iPhone, acerca la parte superior. En Android, NFC debe estar activado. Si no, el QR funciona siempre.')]
    tt = ''
    for i, (t, d) in enumerate(tips):
        y = 42 + i * 24
        tt += text(10, y, t, 10.5, 'display', 600, C['w'], track=-0.01)
        words = d.split(); rows = []; cur = ''
        for wd in words:
            if len(cur) + len(wd) + 1 > 44:
                rows.append(cur); cur = wd
            else:
                cur = (cur + ' ' + wd).strip()
        rows.append(cur)
        tt += lines(10, y + 5, rows, 9, 1.45, font='texto', fill=C['g200'])
    dorso = (fondo(W, H, C['g950']) + orb +
             text(10, 20, 'Consejos', 9, 'texto', 600, C['g400']) +
             text(10, 30, 'Para que la usen.', 15, 'display', 700, C['w'], track=-0.03) + tt +
             text(10, 124, 'Conecta lo que eres.', 11, 'display', 600, C['w'], track=-0.02) +
             text(10, 129.5, 'Acerca lo que sigue.', 11, 'display', 600, C['az400'], track=-0.02) +
             text(10, 139, '@oryzztap · shop.oryzz.com', 9, 'texto', 500, C['g400']))
    exportar('oryzz-tap_tarjeta-producto_A6', D('04_Tarjeta_Producto_Tap'), W, H, [('frente', frente), ('dorso', dorso)],
             info='Oryzz Tap · Tarjeta de producto A6')


# ============================================================ 5. ROLL-UP Y CARTEL
def gran_formato():
    # Roll-up 850 × 2000 (los 100 mm inferiores quedan ocultos en el cassette)
    W, H = 850, 2000
    lg, _, _ = logo('h', 'color-sobre-oscuro', 90, 120, w=380)
    orb = orbitas_group(900, 980, [120, 200, 280, 360, 440, 520], trazo=C['g700'], grosor=1.2, nodo=C['li500'], nodo_en=2, nodo_r=9, nodo_ang=175)
    srv = ['Meta, Google y TikTok Ads', 'Automatización con IA', 'SEO local y reseñas', 'GEO · ChatGPT, Gemini y Perplexity']
    ss = ''
    for i, t in enumerate(srv):
        y = 1130 + i * 70
        ss += f'<line x1="90" y1="{y - 45}" x2="760" y2="{y - 45}" stroke="{C["g700"]}" stroke-width="1"/>'
        ss += nodo(102, y - 10, 7, C['g400'], trazo=2.2) + text(130, y, t, 90, 'display', 600, C['w'], track=-0.02)
    ss += f'<line x1="90" y1="{1130 + 4 * 70 - 45}" x2="760" y2="{1130 + 4 * 70 - 45}" stroke="{C["g700"]}" stroke-width="1"/>'
    qr = qr_group(URL_QR_AGENDA, 560, 1520, 200, C['g950'], fondo=C['w'], radio=14)
    body = (fondo(W, H, C['g950']) + orb + lg +
            text(90, 470, 'Captación de clientes con IA para pymes', 64, 'texto', 600, C['g400']) +
            text(90, 640, 'Más clientes.', 330, 'display', 700, C['w'], track=-0.045) +
            text(90, 755, 'No más likes.', 330, 'display', 700, C['az400'], track=-0.045) +
            lines(90, 860, ['Un sistema de captación que gira solo:', 'anuncios, IA que responde al momento', 'y un informe en citas y en euros.'], 104, 1.35, font='texto', fill=C['g200']) +
            ss +
            text(90, 1560, '30 minutos.', 190, 'display', 700, C['w'], track=-0.035) +
            lines(90, 1620, ['Sales con un diagnóstico,', 'no con un presupuesto.'], 96, 1.35, font='texto', fill=C['g200']) +
            text(90, 1790, 'cal.com/oryzz/30min', 84, 'texto', 600, C['w']) +
            text(90, 1840, 'oryzz.com · @oryzzai', 66, 'texto', 500, C['g400']) + qr +
            f'<rect x="-3" y="1900" width="{W + 6}" height="103" fill="{C["g950"]}"/>')
    exportar('oryzz_rollup_85x200cm', D('05_Rollup_y_Cartel'), W, H, [('', body)], info='Oryzz · Roll-up 850 × 2000 mm (100 mm inferiores ocultos)', preview_dpi=12)

    # Cartel A3 Oryzz Tap 297 × 420
    W, H = 297, 420
    lg, _, _ = logo('t', 'color-sobre-claro', 24, 24, w=62)
    k = 1.8
    stand = (f'<g transform="translate(140 176) scale({k})">'
             f'<path d="M14 100 L66 100 L60 107 L20 107 Z" fill="{C["g200"]}"/>'
             f'<rect x="12" y="6" width="56" height="94" rx="6" fill="{C["g950"]}"/>'
             + logo('i', 'color-sobre-oscuro', 33, 15, w=14)[0] +
             text(40, 40, 'Acerca tu', 15.9, 'display', 600, C['w'], 'middle', -0.02) +
             text(40, 46.6, 'teléfono', 15.9, 'display', 600, C['w'], 'middle', -0.02) +
             f'<g fill="none" stroke="{C["g600"]}" stroke-width="0.7" stroke-linecap="round"><path d="M34.5 55.5a8 8 0 0 1 11 0"/><path d="M31.5 52.5a12 12 0 0 1 17 0"/></g>'
             f'<circle cx="40" cy="59.2" r="1.3" fill="{C["g400"]}"/>'
             + qr_group(URL_QR_TAP, 25, 66, 30, C['g950'], fondo=C['w'], radio=2.4) +
             text(40, 104.6, 'Reseñas Google', 8.4, 'texto', 600, C['g500'], 'middle') + '</g>')
    pasos = [('Acerca el teléfono', ['El chip NFC abre tu enlace', 'al instante.']),
             ('Se abre tu página', ['Reseña, WhatsApp o perfil,', 'sin pasos de más.']),
             ('Lo cambias cuando quieras', ['El destino se edita', 'sin reimprimir nada.'])]
    pp = ''
    for i, (t, d) in enumerate(pasos):
        y = 218 + i * 44
        pp += f'<line x1="24" y1="{y - 9}" x2="146" y2="{y - 9}" stroke="{C["g950"]}" stroke-width="0.5"/>'
        pp += nodo(27.5, y - 2.1, 2.1, C['az600'], relleno=C['az600'] if i == len(pasos) - 1 else None) + text(38, y, t, 17, 'display', 600, C['g950'], track=-0.015)
        pp += lines(38, y + 8.5, d, 13, 1.4, font='texto', fill=C['g600'])
    body = (fondo(W, H, C['g50']) + lg +
            text(24, 70, 'Placas y stands NFC + QR', 13, 'texto', 600, C['g500']) +
            text(24, 108, 'Tu negocio.', 96, 'display', 700, C['g950'], track=-0.045) +
            text(24, 142, 'A un toque.', 96, 'display', 700, C['az500'], track=-0.045) +
            lines(24, 164, ['Tus clientes acercan el teléfono y ocurre:', 'dejan una reseña, te escriben o te siguen.'], 15, 1.4, font='texto', fill=C['g600']) +
            stand + pp +
            f'<line x1="24" y1="378" x2="273" y2="378" stroke="{C["g200"]}" stroke-width="0.35"/>' +
            text(24, 393, 'Conecta lo que eres. Acerca lo que sigue.', 17, 'display', 600, C['g950'], track=-0.02) +
            text(24, 403, 'shop.oryzz.com · pedidos@oryzz.com · @oryzztap', 11, 'texto', 500, C['g500']) +
            rect(207, 386, 66, 17, C['az600'], 8.5) + text(240, 396.8, 'Pídela en la tienda', 12, 'texto', 700, C['w'], 'middle'))
    exportar('oryzz-tap_cartel_A3', D('05_Rollup_y_Cartel'), W, H, [('', body)], info='Oryzz Tap · Cartel A3', preview_dpi=60)


# ============================================================ 6. MERCHANDISING (mockup plano)
def merch():
    W, H = 420, 297
    out = [fondo(W, H, C['g50'])]
    out.append(text(24, 30, 'Merchandising · aplicación del logo', 10, 'texto', 600, C['g500']))
    out.append(text(24, 46, 'Una tinta cuando se borda. El gradiente, solo en impresión a color.', 16, 'display', 700, C['g950'], track=-0.03))
    # --- camiseta grafito
    tx, ty = 24, 70
    tee = (f'<path transform="translate({tx} {ty})" d="M38 0 C44 8 70 8 76 0 L108 12 L120 44 L100 52 L96 40 L96 160 Q96 166 90 166 L24 166 Q18 166 18 160 L18 40 L14 52 L-6 44 L6 12 Z" fill="{C["g850"]}"/>'
           f'<path transform="translate({tx} {ty})" d="M38 0 C44 8 70 8 76 0" fill="none" stroke="{C["g700"]}" stroke-width="1.2"/>')
    out.append(tee)
    out.append(logo('h', 'solido-sobre-oscuro', tx + 34, ty + 38, w=46)[0])
    out.append(text(tx - 6, ty + 180, 'Camiseta grafito', 11, 'display', 600, C['g950']))
    out.append(lines(tx - 6, ty + 187, ['Serigrafía 2 tintas: solido-sobre-oscuro.', 'Bordado: mono-blanco, 1 hilo.', 'Ancho de pecho: 80–100 mm.'], 9, 1.45, font='texto', fill=C['g600']))
    # --- taza blanca
    mx, my = 168, 96
    mug = (f'<path d="M{mx + 86} {my + 28} h10 a22 22 0 0 1 0 44 h-10" fill="none" stroke="{C["g300"]}" stroke-width="8"/>'
           f'{rect(mx, my, 90, 104, C["w"], 6, f" stroke=\"{C["g200"]}\" stroke-width=\"0.5\"")}'
           f'<ellipse cx="{mx + 45}" cy="{my + 2}" rx="45" ry="5" fill="{C["g100"]}"/>')
    out.append(mug)
    out.append(logo('h', 'color-sobre-claro', mx + 14, my + 42, w=62)[0])
    out.append(text(mx - 4, ty + 180, 'Taza blanca', 11, 'display', 600, C['g950']))
    out.append(lines(mx - 4, ty + 187, ['Sublimación a color: color-sobre-claro.', 'Tampografía 1 tinta: mono-grafito.', 'Logo centrado, 55–65 mm.'], 9, 1.45, font='texto', fill=C['g600']))
    # --- tote
    bx, by = 292, 86
    tote = (f'<path d="M{bx + 30} {by + 22} C{bx + 30} {by - 18} {bx + 74} {by - 18} {bx + 74} {by + 22}" fill="none" stroke="{C["g300"]}" stroke-width="5"/>'
            f'{rect(bx, by + 20, 104, 118, "#ECE9E1", 2)}')
    out.append(tote)
    out.append(logo('i', 'mono-grafito', bx + 30, by + 52, w=44)[0])
    out.append(text(bx - 4, ty + 180, 'Tote de algodón natural', 11, 'display', 600, C['g950']))
    out.append(lines(bx - 4, ty + 187, ['Serigrafía o bordado 1 tinta: mono-grafito.', 'Isotipo grande, ≥ 25 % de respeto.', 'El corte del nodo se conserva.'], 9, 1.45, font='texto', fill=C['g600']))
    # nota de bordado
    out.append(rect(24, 274, 372, 0.35, C['g200']))
    out.append(text(24, 284, 'Bordado → versión sólida, una tinta (mono-blanco o mono-grafito). Sin gradiente ni degradados de hilo. Isotipo bordado ≥ 15 mm; logo horizontal ≥ 40 mm.',
                    9, 'texto', 500, C['g950']))
    exportar('oryzz_merchandising_mockup', D('06_Merchandising'), W, H, [('', ''.join(out))], info='Oryzz · Mockup de merchandising (plano)', preview_dpi=90)


GRUPOS = {'tarjetas': tarjetas, 'papeleria': papeleria, 'pegatinas': pegatinas, 'tap': tarjeta_tap, 'gran_formato': gran_formato, 'merch': merch}

if __name__ == '__main__':
    for g in (sys.argv[1:] or GRUPOS):
        GRUPOS[g](); print('ok', g)
