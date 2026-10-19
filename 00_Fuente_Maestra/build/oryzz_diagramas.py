"""
oryzz_diagramas.py · Diagramas de sistema del método Oryzz (v2.0).

Estilo: líneas finas, nodos huecos, rutas ortogonales redondeadas, etiquetas en Manrope 600 en tipo
frase (sin mayúsculas, sin tracking, sin números de paso), un único acento lima (el resultado).
Sin gradientes, sin azul de acento. JetBrains Mono solo para datos técnicos (URL).

Salida por diagrama y tema (oscuro / claro):
  SVG/            texto vivo, editable (requiere Space Grotesk, Manrope y JetBrains Mono instaladas)
  SVG_contornos/  texto convertido a trazados: se ve igual en cualquier sitio (usar en web, email, <img>)
  PNG/            1920×1080 (y 3840×2160 @2x)

Uso:  python oryzz_diagramas.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oryzz_svg import (C, THEME, ROOT, write, doc, T, text_width, wrap, arc, pol, gap_deg, ruta,
                       reticula, png_from_svg, embed_logo)
import oryzz_iconos as IC

OUT = os.path.join(ROOT, '05_Elementos_Graficos', '04_Diagramas')
W, H = 1920, 1080
M = 120  # margen


class D:
    """Lienzo de diagrama con estilo de marca para un tema."""

    def __init__(self, tema, contornos):
        self.t = THEME[tema]; self.tema = tema; self.k = contornos; self.s = []
        self.line = C['grafito-600'] if tema == 'oscuro' else C['grafito-300']
        self.line2 = C['grafito-700'] if tema == 'oscuro' else C['grafito-200']
        self.nodo = self.t['nodo']

    def add(self, x):
        self.s.append(x)

    # ---- texto
    def txt(self, x, y, s, fam='texto', wt=400, size=24, fill=None, **kw):
        self.add(T(x, y, s, fam, wt, size, fill or self.t['texto2'], contornos=self.k, **kw))

    def etq(self, x, y, s, size=22, fill=None, wt=600, anchor='start'):
        """Etiqueta en tipo frase: Manrope 600, sin tracking ni mayúsculas (BRAND_SPEC §4)."""
        self.add(T(x, y, s, 'texto', wt, size, fill or self.t['texto3'], anchor=anchor, contornos=self.k))

    def para(self, x, y, s, maxw, size=24, fill=None, lh=1.45, fam='texto', wt=400, anchor='start'):
        lines = wrap(s, fam, wt, size, maxw)
        for i, l in enumerate(lines):
            self.add(T(x, y + i * size * lh, l, fam, wt, size, fill or self.t['texto3'], anchor=anchor, contornos=self.k))
        return y + (len(lines) - 1) * size * lh

    def titulo(self, eyebrow, lineas, x=M, y=M, size=64):
        self.etq(x, y + 16, eyebrow, 24, self.t['texto3'])
        yy = y + 36 + size * 0.95
        for l in lineas:
            self.add(T(x, yy, l, 'display', 700, size, self.t['texto'], tracking=-0.035, contornos=self.k))
            yy += size * 1.05
        return yy

    # ---- elementos
    def path(self, d, sw=1.75, col=None, dash=None, op=None):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.add(f'<path d="{d}" fill="none" stroke="{col or self.line}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{da}{o}/>')

    def hueco(self, x, y, r=7, sw=1.75, col=None):
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{self.t["fondo"]}" stroke="{col or self.t["texto3"]}" stroke-width="{sw}"/>')

    def punto(self, x, y, r=4, col=None):
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col or self.t["texto3"]}"/>')

    def lima(self, x, y, r=12, anillo=True):
        if anillo:
            self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.6:.1f}" fill="none" stroke="{self.nodo}" stroke-width="1.5" opacity=".45"/>')
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{self.nodo}"/>')

    def caja(self, x, y, w, h, r=16):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{self.t["superficie"]}" stroke="{self.t["borde"]}" stroke-width="1"/>')

    def icono(self, name, x, y, size=32, col=None, acento=None):
        body = IC.ICONS[name][2]
        sc = size / 24
        st = f'color:{col or self.t["texto2"]}' + (f';--oz-acento:{acento}' if acento else '')
        body = body.replace('style="color:var(--oz-acento,currentColor)"',
                            f'style="color:{acento or col or self.t["texto2"]}"')
        self.add(f'<g transform="translate({x:.1f} {y:.1f}) scale({sc:.4f})" style="{st}" fill="none" stroke="currentColor" '
                 f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{body}</g>')

    def chevron(self, x, y, ang, size=9, col=None):
        a1 = math.radians(ang + 180 - 40); a2 = math.radians(ang + 180 + 40)
        d = (f'M{x + size * math.cos(a1):.1f} {y + size * math.sin(a1):.1f}L{x:.1f} {y:.1f}'
             f'L{x + size * math.cos(a2):.1f} {y + size * math.sin(a2):.1f}')
        self.path(d, 1.75, col)

    def pie(self, texto):
        self.add(f'<path d="M{M} {H - 96}H{W - M}" stroke="{self.line2}" stroke-width="1"/>')
        self.etq(M, H - 54, texto, 20, self.t['texto3'], wt=500)
        way = 'solido-sobre-oscuro' if self.tema == 'oscuro' else 'solido-sobre-claro'
        lg, lh = embed_logo(W - M - 132, H - 76, 132, 'horizontal', way, uid='lg' + self.tema[0])
        self.add(lg)

    def fondo(self):
        op = 0.035 if self.tema == 'oscuro' else 0.05
        self.s.insert(0, reticula('rt', W, H, 64, self.t['reticula'], op, True, W * 0.62, H * 0.52, W * 0.6))

    def svg(self, title, desc=''):
        return doc(W, H, ''.join(self.s), title, bg=self.t['fondo'], desc=desc)


# ================================================================== 1 · Canales → Sistema → Cliente
def d1(tema, k):
    d = D(tema, k); t = d.t
    d.titulo('Método Oryzz: canales, sistema y cliente', ['Cuatro canales.', 'Un solo sistema.'])
    canales = [('ads-meta', 'Meta Ads', 'Instagram y Facebook'), ('ads-google', 'Google Ads', 'Buscador y Maps'),
               ('ads-tiktok', 'TikTok Ads', 'Vídeo corto'), ('geo-ia', 'GEO · IA', 'ChatGPT, Gemini, Perplexity')]
    cx0, cw, ch = M, 400, 104
    ys = [440, 568, 696, 824]
    HX, HY, R = 1120, 632, 176
    for i, ((ic, lab, sub), y) in enumerate(zip(canales, ys)):
        d.caja(cx0, y - ch / 2, cw, ch, 18)
        d.icono(ic, cx0 + 28, y - 18, 36)
        d.etq(cx0 + 92, y - 6, lab, 24, t['texto'])
        d.txt(cx0 + 92, y + 26, sub, size=22, fill=t['texto3'])
    # rutas convergentes: giran antes las más cercanas al eje
    order = sorted(range(4), key=lambda i: abs(ys[i] - HY))
    for n, i in enumerate(order):
        y = ys[i]; xt = 620 + 64 * n
        d.path(ruta([(cx0 + cw, y), (xt, y), (xt, HY), (HX - R - 22, HY)], 28))
        d.punto(cx0 + cw, y, 4, d.line)
    d.chevron(HX - R - 34, HY, 0, 10)
    # órbita (sistema) abierta por la salida
    cut = gap_deg(R, 64)
    d.path(arc(HX, HY, R, cut / 2, -cut / 2), 2.5, t['texto2'])
    d.path(arc(HX, HY, R - 44, 40, -20), 1.25, d.line2)
    for a in (-120, 150, 70):
        x, y = pol(HX, HY, R, a); d.hueco(x, y, 6, 1.75, t['texto3'])
    from oryzz_svg import isotipo_group
    d.add(isotipo_group(HX - 28, HY - 92, 56, t['texto2'], t['texto2'], uid='isd1' + tema[0]))
    d.etq(HX, HY + 8, 'Sistema Oryzz', 24, t['texto'], anchor='middle')
    d.txt(HX, HY + 46, 'Responde · clasifica · sigue', size=20, fill=t['texto3'], anchor='middle')
    # salida → cliente
    NX = 1560
    d.path(f'M{HX + R + 8} {HY}H{NX - 44}', 2.5, t['texto2'])
    d.lima(NX, HY, 14)
    d.etq(NX + 64, HY - 14, 'Cliente', 24, t['texto'])
    d.para(NX + 64, HY + 22, 'Cita, venta o reserva medida en euros.', 240, 22)
    d.pie('Cuatro canales, un sistema y una métrica: clientes y euros')
    d.fondo()
    return d.svg('Oryzz · diagrama · canales, sistema y cliente',
                 'Meta Ads, Google Ads, TikTok Ads y GEO convergen en el sistema Oryzz, que entrega clientes medidos en euros.')


# ================================================================== 2 · Embudo como órbita
def d2(tema, k):
    d = D(tema, k); t = d.t
    yy = d.titulo('Método Oryzz: embudo de captación', ['El embudo', 'es una órbita.'])
    d.para(M, yy + 24, 'No acaba en el clic. Cada contacto se responde, se clasifica y se sigue hasta que es cliente. '
           'Lo que se mide vuelve a alimentar la captación.', 560, 24, t['texto3'], 1.5)
    CX, CY, R = 1260, 560, 272
    # Las etapas se distinguen por su nombre y su nodo, sin números (BRAND_SPEC §4).
    etapas = [('Captar', 'Meta, Google, TikTok y búsqueda con IA.'),
              ('Responder', 'WhatsApp o email en minutos, también de noche.'),
              ('Clasificar', 'La IA separa curiosos de clientes con intención.'),
              ('Seguir', 'Recordatorios y seguimiento hasta la cita.'),
              ('Medir', 'Coste por lead, citas y euros.')]
    angs = [-90 + 72 * i for i in range(5)]
    g = gap_deg(R, 44)
    for i, a in enumerate(angs):
        b = angs[(i + 1) % 5] + (360 if i == 4 else 0)
        d.path(arc(CX, CY, R, a + g / 2, b - g / 2), 2, t['texto2'] if i < 4 else d.line)
        m = (a + b) / 2; x, y = pol(CX, CY, R, m)
        d.chevron(x, y, m + 90, 9, t['texto2'] if i < 4 else d.line)
    d.path(arc(CX, CY, R - 72, -60, 250), 1.25, d.line2, dash='2 8')
    for (name, desc), a in zip(etapas, angs):
        x, y = pol(CX, CY, R, a)
        d.hueco(x, y, 9, 2, t['texto'])
        # etiqueta fuera del anillo
        lx, ly = pol(CX, CY, R + 44, a)
        right = math.cos(math.radians(a)) > 0.2
        left = math.cos(math.radians(a)) < -0.2
        anchor = 'start' if right else ('end' if left else 'middle')
        if a == -90:
            ly -= 96
        elif a in (54, 126):
            ly += 34
        else:
            ly -= 10
        d.add(T(lx, ly + 38, name, 'display', 600, 32, t['texto'], tracking=-0.02, anchor=anchor, contornos=k))
        mw = 300
        ls = wrap(desc, 'texto', 400, 22, mw)
        for j, l in enumerate(ls):
            d.add(T(lx, ly + 72 + j * 31, l, 'texto', 400, 22, t['texto3'], anchor=anchor, contornos=k))
    d.lima(CX, CY, 14)
    d.etq(CX, CY + 72, 'Cliente', 24, t['texto'], anchor='middle')
    d.pie('Captar, responder, clasificar, seguir y medir')
    d.fondo()
    return d.svg('Oryzz · diagrama · embudo de captación como órbita',
                 'Cinco etapas en ciclo alrededor del cliente: captar, responder, clasificar, seguir y medir.')


# ================================================================== 3 · Valoración 30 min
def d3(tema, k):
    d = D(tema, k); t = d.t
    yy = d.titulo('Método Oryzz: valoración gratuita', ['30 minutos.'])
    d.para(M, yy + 20, 'Sales con un diagnóstico, no con un presupuesto. Si no encajamos, te lo decimos.', 520, 26, t['texto2'], 1.45)
    d.etq(M, 860, 'Agenda', 22, t['texto3'])
    d.add(T(M, 900, 'cal.com/oryzz/30min', 'mono', 500, 26, t['texto'], contornos=k))
    CX, CY, R = 930, 566, 270
    # esfera: mitad de 60 min = 30 min
    d.path(arc(CX, CY, R, 90, 270), 1.25, d.line2, dash='2 10')
    pasos = [(-90, "0'"), (-30, "10'"), (30, "20'"), (90, "30'")]
    g = gap_deg(R, 40)
    for i in range(3):
        a, b = pasos[i][0], pasos[i + 1][0]
        d.path(arc(CX, CY, R, a + g / 2, b - g / 2), 2.5, t['texto2'])
    for a, lab in pasos:
        x, y = pol(CX, CY, R, a)
        if a == 90:
            d.lima(x, y, 13)
        else:
            d.hueco(x, y, 9, 2, t['texto'])
        ix, iy = pol(CX, CY, R - 56, a)
        d.etq(ix, iy + 8, lab, 22, t['texto3'], anchor='middle' if abs(a) == 90 else 'end')
    steps = [(-60, '0–10 min', 'Tu negocio hoy', 'Cómo te llegan los clientes y cuánto te cuesta cada uno.'),
             (0, '10–20 min', 'Dónde se pierden', 'Anuncios, web, tiempo de respuesta y reseñas.'),
             (60, '20–30 min', 'Qué haríamos', 'Prioridades y siguiente paso. Sin compromiso.')]
    for a, tramo, name, desc in steps:
        x, y = pol(CX, CY, R + 70, a)
        y0 = y - 50 if a != 60 else y - 60
        d.etq(x, y0, tramo, 22, t['texto3'])
        d.add(T(x, y0 + 42, name, 'display', 600, 34, t['texto'], tracking=-0.02, contornos=k))
        d.para(x, y0 + 80, desc, 420, 22, t['texto3'], 1.4)
    x, y = pol(CX, CY, R, 90)
    d.etq(x, y + 62, 'Diagnóstico', 24, t['texto'], anchor='middle')
    d.pie('Valoración de 30 minutos en tres tramos, gratis')
    d.fondo()
    return d.svg('Oryzz · diagrama · valoración de 30 minutos en 3 pasos',
                 'Media esfera de reloj: 0–10 min tu negocio hoy, 10–20 dónde se pierden, 20–30 qué haríamos.')


# ================================================================== 4 · Prueba inicial
def d4(tema, k):
    d = D(tema, k); t = d.t
    d.titulo('Método Oryzz: prueba inicial', ['Validamos con datos', 'antes de que gastes.'])
    # cifras clave (dato)
    for i, (big, lab) in enumerate([('50–100 €', 'Inversión en anuncios'), ('3–7 días', 'Hasta tener datos')]):
        x = 1160 + i * 360
        d.etq(x, 150, lab, 22, t['texto3'])
        d.add(T(x, 226, big, 'display', 500, 64, t['texto'], tracking=-0.03, contornos=k))
    # pista de días
    X0, X1, Y = M + 20, W - M - 20, 600
    step = (X1 - X0) / 6
    d.path(f'M{X0} {Y}H{X1 - 40}', 2, t['texto2'])
    for i in range(7):
        x = X0 + i * step
        if i == 6:
            d.lima(x, Y, 13)
        else:
            d.hueco(x, Y, 8 if i else 9, 2, t['texto'] if i in (0, 2) else t['texto3'])
        d.etq(x, Y + 56, f'Día {i + 1}', 22, t['texto3'] if i != 6 else t['texto'], anchor='middle')
    # corchete ventana de lectura 3–7
    xa, xb = X0 + 2 * step, X1
    d.path(f'M{xa} {Y - 60}V{Y - 76}H{xb}V{Y - 60}', 1.5, d.line)
    d.etq(xa + 16, Y - 96, 'Ventana de lectura: 3–7 días', 22, t['texto2'])
    fases = [(X0, 'Día 1', 'Montamos', 'Campaña, formulario y respuesta automática.'),
             (X0 + 2 * step, 'Días 2–6', 'Medimos', 'Coste por lead y calidad de cada contacto.'),
             (X1, 'Día 3–7', 'Decidimos', 'Escalar, ajustar o parar. Con datos, no con intuición.')]
    for x, n, name, desc in fases:
        a = 'end' if x == X1 else 'start'
        d.path(f'M{x} {Y + 88}V{Y + 120}', 1.25, d.line)
        d.add(T(x, Y + 170, name, 'display', 600, 34, t['texto'], tracking=-0.02, anchor=a, contornos=k))
        d.para(x, Y + 210, desc, 380, 22, t['texto3'], 1.4, anchor=a)
    d.pie('Prueba inicial: 50–100 € y 3–7 días')
    d.fondo()
    return d.svg('Oryzz · diagrama · prueba inicial 50–100 € en 3–7 días',
                 'Día 1 montamos, días 2–6 medimos, entre el día 3 y el 7 decidimos con datos.')


# ================================================================== 5 · Oryzz Tap
def d5(tema, k):
    d = D(tema, k); t = d.t
    yy = d.titulo('Oryzz Tap: cómo funciona', ['Tu negocio.', 'A un toque.'])
    d.para(M, yy + 20, 'El cliente acerca el móvil a la placa y se abre la acción que elijas. También con QR.', 520, 24, t['texto3'], 1.45)
    # placa NFC (producto) con isotipo oficial
    PX, PY, PS = 700, 380, 280
    d.add(f'<rect x="{PX}" y="{PY}" width="{PS}" height="{PS}" rx="36" fill="{t["superficie"]}" stroke="{t["borde"]}" stroke-width="1.5"/>')
    from oryzz_svg import isotipo_group
    ring = C['blanco'] if tema == 'oscuro' else C['grafito-950']
    d.add(isotipo_group(PX + 36, PY + 36, 56, ring, ring, uid='isp' + tema[0]))
    d.icono('nfc', PX + PS / 2 - 44, PY + PS / 2 - 36, 88, t['texto2'])
    d.etq(PX + 36, PY + PS - 40, 'Acerca el teléfono', 20, t['texto3'])
    HX, HY = 1120, PY + PS / 2
    d.path(f'M{PX + PS + 8} {HY}H{HX - 30}', 2.5, t['texto2'])
    d.lima(HX, HY, 13)
    d.etq(HX, HY - 52, 'Toque', 24, t['texto'], anchor='middle')
    dest = [('resenas', 'Reseña en Google', 'Valoración directa en tu ficha.'),
            ('mensaje', 'WhatsApp', 'Chat abierto con tu negocio.'),
            ('menu-carta', 'Menú', 'Carta siempre actualizada.'),
            ('pago', 'Pago', 'Enlace de pago en el móvil.')]
    CXd, cw, chh = 1340, 460, 116
    ys = [HY - 3 * 72, HY - 72, HY + 72, HY + 3 * 72]
    order = sorted(range(4), key=lambda i: abs(ys[i] - HY))
    for n, i in enumerate(order):
        y = ys[i]; xt = 1200 + 40 * (n // 2)
        d.path(ruta([(HX + 30, HY), (xt, HY), (xt, y), (CXd - 8, y)], 24), 1.75)
    for (ic, lab, sub), y in zip(dest, ys):
        d.caja(CXd, y - chh / 2 + 8, cw, chh - 16, 18)
        d.icono(ic, CXd + 28, y - 18, 36)
        d.add(T(CXd + 92, y - 4, lab, 'display', 600, 26, t['texto'], tracking=-0.015, contornos=k))
        d.txt(CXd + 92, y + 28, sub, size=20, fill=t['texto3'])
    d.pie('Oryzz Tap: NFC y QR · oryzz.com/tap')
    d.fondo()
    return d.svg('Oryzz · diagrama · flujo Oryzz Tap',
                 'Toque NFC o QR en la placa → reseña en Google, WhatsApp, menú o pago.')


# ================================================================== 6 · GEO
def d6(tema, k):
    d = D(tema, k); t = d.t
    d.titulo('Método Oryzz: GEO', ['Que la IA', 'te recomiende.'])
    Y = 690
    cols = [(M, 'La pregunta'), (640, 'El asistente'), (1080, 'Las fuentes'), (1520, 'La respuesta')]
    for x, lab in cols:
        d.etq(x, 540, lab, 22, t['texto3'])
    # 1 · pregunta
    d.caja(M, Y - 80, 420, 160, 20)
    d.icono('mensaje', M + 28, Y - 52, 32, t['texto3'])
    d.para(M + 28, Y + 14, '«¿Qué clínica dental me recomiendas en Valencia?»', 360, 24, t['texto'], 1.35)
    # 2 · asistentes
    for i, n in enumerate(['ChatGPT', 'Gemini', 'Perplexity']):
        y = Y - 64 + i * 64
        d.hueco(640 + 8, y - 7, 6, 1.75, t['texto3'])
        d.add(T(640 + 32, y, n, 'texto', 600, 24, t['texto'], contornos=k))
    d.path(f'M{M + 428} {Y}H{620}', 1.75)
    d.chevron(620, Y, 0, 9)
    # 3 · fuentes
    fuentes = ['Tu web', 'Ficha de Google', 'Reseñas', 'Directorios y prensa']
    for i, f in enumerate(fuentes):
        y = Y - 96 + i * 64
        d.punto(1080 + 6, y - 7, 4, d.line)
        d.txt(1080 + 28, y, f, size=24, fill=t['texto2'])
    d.path(ruta([(880, Y - 64 - 7), (960, Y - 64 - 7), (960, Y - 7), (1060, Y - 7)], 20), 1.5)
    d.path(ruta([(880, Y + 64 - 7), (960, Y + 64 - 7), (960, Y - 7)], 20), 1.5)
    d.path(f'M{860} {Y - 7}H{960}', 1.5)
    # 4 · respuesta
    d.path(f'M1350 {Y - 103}H1366V{Y + 89}H1350', 1.5)
    d.path(f'M1366 {Y - 7}H{1490}', 1.75, t['texto2'])
    d.lima(1540, Y - 7, 13)
    d.add(T(1600, Y - 12, 'Tu negocio,', 'display', 600, 32, t['texto'], tracking=-0.02, contornos=k))
    d.add(T(1600, Y + 28, 'citado.', 'display', 600, 32, t['texto'], tracking=-0.02, contornos=k))
    d.para(1600, Y + 72, 'Con nombre, zona y motivo.', 200, 22, t['texto3'], 1.4)
    d.para(M, 340, 'Cada vez más clientes preguntan a un asistente antes que a Google. '
           'Trabajamos las fuentes que las IA leen para que tu negocio aparezca en la respuesta.', 1040, 24, t['texto3'], 1.45)
    d.pie('GEO: posicionamiento en ChatGPT, Gemini y Perplexity')
    d.fondo()
    return d.svg('Oryzz · diagrama · GEO, posicionamiento en asistentes de IA',
                 'Pregunta del cliente → asistente de IA → fuentes (web, ficha, reseñas, directorios) → respuesta que cita al negocio.')


DIAGRAMAS = [('01', 'canales-sistema-cliente', d1), ('02', 'embudo-orbita', d2), ('03', 'valoracion-30min', d3),
             ('04', 'prueba-inicial', d4), ('05', 'oryzz-tap-flujo', d5), ('06', 'geo-ia', d6)]


def build(only=None):
    jobs = []
    for n, slug, fn in DIAGRAMAS:
        if only and n not in only:
            continue
        for tema in ('oscuro', 'claro'):
            name = f'oryzz-diagrama-{n}_{slug}_{tema}'
            write(os.path.join(OUT, 'SVG', name + '.svg'), fn(tema, False))
            sp = os.path.join(OUT, 'SVG_contornos', name + '_contornos.svg')
            write(sp, fn(tema, True))
            jobs.append((sp, os.path.join(OUT, 'PNG', name + '.png'), 1920))
            jobs.append((sp, os.path.join(OUT, 'PNG', name + '@2x.png'), 3840))
    png_from_svg(jobs)
    return jobs


if __name__ == '__main__':
    only = sys.argv[1:] or None
    print(len(build(only)), 'PNG')
