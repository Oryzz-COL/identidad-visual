"""
Oryzz · Redes sociales · gráficos vectoriales del sistema «Órbita y nodo».

Todas las funciones devuelven SVG en texto y usan variables CSS del tema
(--orb, --nodo, --acento, --tx, --tx3, --bg), así que el mismo gráfico sirve
en oscuro, claro y Tap sin tocar nada.

Se exponen como funciones globales dentro de las plantillas Jinja:
    {{ orbitas(1080, 1350, 860, 300, [130, 190, 250]) | safe }}
"""
import math
import re

try:
    import qrcode  # pip install qrcode   (opcional: si falta se dibuja un QR de muestra)
except ImportError:  # pragma: no cover
    qrcode = None


_ATTR_VAR = re.compile(r'\s(fill|stroke|stop-color)="(var\([^"]+\))"')


def _css(svg):
    """Los atributos de presentación SVG no resuelven var(); se pasan a style=""."""
    def tag(m):
        t = m.group(0)
        estilos = ';'.join(f'{a}:{v}' for a, v in _ATTR_VAR.findall(t))
        if not estilos:
            return t
        t = _ATTR_VAR.sub('', t)
        cierre = '/>' if t.endswith('/>') else '>'
        return t[:-len(cierre)] + f' style="{estilos}"' + cierre
    return re.sub(r'<[^<>]+>', tag, svg)


def _p(cx, cy, r, ang):
    a = math.radians(ang)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arco(cx, cy, r, a0, a1):
    """Arco en sentido horario de a0 a a1 (grados, 0 = 3 en punto, crece hacia abajo)."""
    x0, y0 = _p(cx, cy, r, a0)
    x1, y1 = _p(cx, cy, r, a1)
    barrido = (a1 - a0) % 360
    grande = 1 if barrido > 180 else 0
    return f'M{x0:.2f} {y0:.2f}A{r} {r} 0 {grande} 1 {x1:.2f} {y1:.2f}'


def orbitas(w, h, cx, cy, radios, hueco=52, giro=-62, paso=31, nodo=0,
            nodo_r=11, trazo=1.5, clase='orb', color='var(--orb)', nodo_color='var(--nodo)',
            destacar=None):
    """Órbitas abiertas concéntricas. Cada una con un hueco de `hueco` grados,
    desfasado `paso` grados respecto a la anterior. El nodo se coloca en el hueco
    de la órbita `nodo` (None = sin nodo), igual que en el isotipo.
    `destacar`: índice de una órbita que se pinta en --acento (opcional, una sola)."""
    partes = []
    nodo_svg = ''
    for i, r in enumerate(radios):
        centro = giro + i * paso
        a0 = centro + hueco / 2
        a1 = centro - hueco / 2 + 360
        col = 'var(--acento)' if destacar == i else color
        partes.append(f'<path d="{arco(cx, cy, r, a0, a1)}" fill="none" stroke="{col}" '
                      f'stroke-width="{trazo}" stroke-linecap="round"/>')
        if nodo is not None and i == nodo:
            nx, ny = _p(cx, cy, r, centro)
            nodo_svg = f'<circle cx="{nx:.2f}" cy="{ny:.2f}" r="{nodo_r}" fill="{nodo_color}"/>'
    return _css(f'<svg class="capa-svg {clase}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{"".join(partes)}{nodo_svg}</svg>')


def ruta_d(puntos, radio=28):
    """Trazado ortogonal con esquinas redondeadas que pasa por `puntos`."""
    if len(puntos) < 2:
        return ''
    d = [f'M{puntos[0][0]:.1f} {puntos[0][1]:.1f}']
    for i in range(1, len(puntos) - 1):
        (x0, y0), (x1, y1), (x2, y2) = puntos[i - 1], puntos[i], puntos[i + 1]
        l1 = math.hypot(x1 - x0, y1 - y0) or 1
        l2 = math.hypot(x2 - x1, y2 - y1) or 1
        r = min(radio, l1 / 2, l2 / 2)
        ax, ay = x1 - (x1 - x0) / l1 * r, y1 - (y1 - y0) / l1 * r
        bx, by = x1 + (x2 - x1) / l2 * r, y1 + (y2 - y1) / l2 * r
        d.append(f'L{ax:.1f} {ay:.1f}Q{x1:.1f} {y1:.1f} {bx:.1f} {by:.1f}')
    d.append(f'L{puntos[-1][0]:.1f} {puntos[-1][1]:.1f}')
    return ''.join(d)


def nodo_svg(x, y, tipo='hueco', r=9):
    if tipo == 'lleno':
        return f'<circle cx="{x}" cy="{y}" r="{r + 2}" fill="var(--nodo)"/>'
    if tipo == 'acento':
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--acento)"/>'
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--bg)" stroke="var(--tx3)" '
            f'stroke-width="2"/>')


def ruta(w, h, puntos, nodos=(), trazo=2, radio=28, clase='', color='var(--orb-fuerte)'):
    """Ruta + nodos. `nodos` = [(x, y, 'hueco'|'lleno'|'acento'), ...]."""
    d = ruta_d(puntos, radio)
    ns = ''.join(nodo_svg(x, y, t) for x, y, t in nodos)
    return _css(f'<svg class="capa-svg {clase}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{trazo}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>{ns}</svg>')


def panorama_carrusel(n, w=1080, h=1350, estaciones=None, y_base=1130, salto=64):
    """Una sola ruta que atraviesa las `n` slides (ancho total n*w).
    Cada slide recibe el SVG completo desplazado -i*w, así la línea
    continúa exactamente en el corte. Devuelve el SVG de todo el panorama."""
    estaciones = estaciones or [''] * n
    total = n * w
    pts = [(300, y_base)]
    nodos = []
    etiquetas = []
    nivel = y_base
    for i in range(n):
        x0 = i * w
        if i > 0:
            nuevo = y_base - salto if i % 2 else y_base
            pts.append((x0 + 150, nivel))
            pts.append((x0 + 150, nuevo))
            nivel = nuevo
        sx = x0 + (700 if i < n - 1 else 760)
        if i == n - 1:
            pts.append((sx, nivel))
            nodos.append((sx, nivel, 'lleno'))
        else:
            nodos.append((sx, nivel, 'hueco'))
        if estaciones[i]:
            etiquetas.append((sx, nivel, estaciones[i], i == n - 1))
    if len(pts) == 1 or pts[-1][0] < (n - 1) * w:
        pts.append(((n - 1) * w + 760, nivel))
    d = ruta_d(pts, 30)
    ns = ''.join(nodo_svg(x, y, t) for x, y, t in nodos)
    txt = ''.join(
        f'<text x="{x + 26}" y="{y - 24}" class="svg-mono{" svg-mono-on" if fin else ""}">{et}</text>'
        for x, y, et, fin in etiquetas)
    # órbita final alrededor del nodo de llegada (el cliente)
    fx, fy = pts[-1]
    sx0, sy0 = nodos[0][0], nodos[0][1]
    orb0 = ''.join(
        f'<path d="{arco(sx0, sy0, r, 120 + k * 34 + 24, 120 + k * 34 - 24 + 360)}" fill="none" '
        f'stroke="var(--orb)" stroke-width="1.5" stroke-linecap="round"/>'
        for k, r in enumerate((44, 78)))
    orb = orb0 + ''.join(
        f'<path d="{arco(fx, fy, r, -60 + k * 34 + 24, -60 + k * 34 - 24 + 360)}" fill="none" '
        f'stroke="var(--orb)" stroke-width="1.5" stroke-linecap="round"/>'
        for k, r in enumerate((44, 78)))
    return _css(f'<svg class="capa-svg" width="{total}" height="{h}" viewBox="0 0 {total} {h}" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<path d="{d}" fill="none" stroke="var(--orb-fuerte)" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"/>{orb}{ns}{txt}</svg>')


def arco_reloj(size, minutos=30, total=60, trazo=3):
    """Órbita-reloj: anillo completo tenue + arco de `minutos` sobre `total` en gradiente,
    nodo lima al final. Para el CTA de la valoración de 30 minutos."""
    c = size / 2
    r = size / 2 - 24
    fin = -90 + 360 * minutos / total
    ticks = []
    for k in range(12):
        a = -90 + k * 30
        x0, y0 = _p(c, c, r - 18, a)
        x1, y1 = _p(c, c, r - 30, a)
        ticks.append(f'<path d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}" stroke="var(--orb-fuerte)" '
                     f'stroke-width="2" stroke-linecap="round"/>')
    nx, ny = _p(c, c, r, fin)
    return _css(f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<defs><linearGradient id="gr-reloj" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="var(--grad-a)"/><stop offset="1" stop-color="var(--grad-b)"/></linearGradient></defs>'
            f'<path d="{arco(c, c, r, fin + 8, -90 - 8 + 360)}" fill="none" stroke="var(--orb)" stroke-width="{trazo}" stroke-linecap="round"/>'
            f'{"".join(ticks)}'
            f'<path d="{arco(c, c, r, -90, fin - 5)}" fill="none" stroke="url(#gr-reloj)" stroke-width="{trazo * 3}" stroke-linecap="round"/>'
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{trazo * 4}" fill="var(--nodo)"/></svg>')


# --------------------------------------------------------------------------- iconos
# Retícula 24 px · trazo 1,75 px · puntas y uniones redondeadas · monocromo.
ICONOS = {
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'cruz': '<path d="M7 7l10 10M17 7L7 17"/>',
    'flecha': '<path d="M4 12h15M13 6l6 6-6 6"/>',
    'flecha-abajo': '<path d="M12 4v15M6 13l6 6 6-6"/>',
    'chat': '<path d="M20 11.5a7.5 7.5 0 0 1-11.1 6.6L4 19.5l1.4-4.6A7.5 7.5 0 1 1 20 11.5z"/>',
    'calendario': '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    'estrella': '<path d="M12 3.6l2.55 5.2 5.7.83-4.13 4.02.98 5.68L12 16.64l-5.1 2.69.98-5.68-4.13-4.02 5.7-.83z"/>',
    'nfc': '<path d="M7.5 9.2a4 4 0 0 1 0 5.6M10.8 6.6a7.6 7.6 0 0 1 0 10.8M14.1 4a11.2 11.2 0 0 1 0 16"/><circle cx="4.6" cy="12" r=".6"/>',
    'qr': '<rect x="3.5" y="3.5" width="6.5" height="6.5" rx="1.5"/><rect x="14" y="3.5" width="6.5" height="6.5" rx="1.5"/><rect x="3.5" y="14" width="6.5" height="6.5" rx="1.5"/><path d="M14 14h2.5v2.5H14zM18 18h2.5v2.5H18zM14 20.5h.01M20.5 14h.01"/>',
    'movil': '<rect x="6.5" y="2.5" width="11" height="19" rx="2.8"/><path d="M10.5 18.3h3"/>',
    'sobre': '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7.5l8 5.5 8-5.5"/>',
    'equipo': '<circle cx="9" cy="8.5" r="3.3"/><path d="M3 19.5a6 6 0 0 1 12 0"/><path d="M15.5 5.4a3.3 3.3 0 0 1 0 6.3M17.6 13.9a6 6 0 0 1 3.4 5.6"/>',
    'capas': '<path d="M12 3.5l8.5 4.7L12 13 3.5 8.2z"/><path d="M3.5 12.2L12 17l8.5-4.8M3.5 16.2L12 21l8.5-4.8"/>',
    'casos': '<path d="M3.5 20h17"/><path d="M5 16l4.5-4.5 3.5 3.5 6-6.5"/><path d="M15 8.5h4v4"/>',
    'pregunta': '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.6a2.5 2.5 0 1 1 3.4 2.33c-.6.25-1 .83-1 1.47v.5"/><path d="M12 16.8v.01"/>',
    'geo': '<path d="M19.5 11a7.5 7.5 0 0 1-11 6.63L4.5 19l1.2-3.9A7.5 7.5 0 1 1 19.5 11z"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01"/>',
    'tap': '<rect x="3.5" y="6" width="10" height="13" rx="2.2"/><path d="M16.2 9.4a3.6 3.6 0 0 1 0 5.2M18.8 7a7 7 0 0 1 0 10"/>',
    'reloj': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    'enlace': '<path d="M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1 1"/><path d="M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1-1"/>',
    'buscar': '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.3-4.3"/>',
    'ubicacion': '<path d="M12 21s6.5-5.7 6.5-11a6.5 6.5 0 0 0-13 0c0 5.3 6.5 11 6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
    'mas': '<path d="M12 5v14M5 12h14"/>',
    'perfil': '<rect x="4" y="3.5" width="16" height="17" rx="3"/><circle cx="12" cy="9.5" r="2.6"/><path d="M8 16.5h8"/>',
    'pantalla': '<rect x="3" y="4.5" width="18" height="12" rx="2.5"/><path d="M9 20h6M12 16.5V20"/>',
}


def icono(nombre, size=48, color='currentColor', trazo=1.75, clase=''):
    cuerpo = ICONOS.get(nombre, ICONOS['mas'])
    return _css(f'<svg class="icono {clase}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{trazo}" stroke-linecap="round" stroke-linejoin="round" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{cuerpo}</svg>')


# --------------------------------------------------------------------------- QR
def qr(datos='https://oryzz.com/tap', size=240, color='currentColor'):
    """QR real (módulos cuadrados, legible). Sin la librería qrcode dibuja uno de muestra."""
    if qrcode:
        q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
        q.add_data(datos)
        q.make(fit=True)
        m = q.get_matrix()
    else:
        import random
        rnd = random.Random(7)
        m = [[rnd.random() > .5 for _ in range(25)] for _ in range(25)]
        for ox, oy in ((0, 0), (18, 0), (0, 18)):
            for y in range(7):
                for x in range(7):
                    m[oy + y][ox + x] = x in (0, 6) or y in (0, 6) or (2 <= x <= 4 and 2 <= y <= 4)
    n = len(m)
    d = ''.join(f'M{x} {y}h1v1h-1z' for y, fila in enumerate(m) for x, v in enumerate(fila) if v)
    return _css(f'<svg width="{size}" height="{size}" viewBox="0 0 {n} {n}" shape-rendering="crispEdges" '
            f'xmlns="http://www.w3.org/2000/svg" aria-label="Código QR"><path d="{d}" fill="{color}"/></svg>')
