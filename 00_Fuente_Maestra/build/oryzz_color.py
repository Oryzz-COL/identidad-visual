"""
Oryzz · datos de color v2.0 y utilidades (contraste WCAG, conversiones).
Fuente de los HEX: 00_Fuente_Maestra/tokens.json. Aquí solo se añaden nombres,
usos, CMYK aproximado y Pantone de referencia.

    from oryzz_color import PALETA, contraste, hex_rgb
"""
import colorsys, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENS = json.load(open(os.path.join(HERE, '..', 'tokens.json'), encoding='utf8'))
C = TOKENS['color']

NOTA_CMYK = 'aproximado, pedir prueba de color'
NOTA_PANTONE = 'referencia a validar con guía Pantone física'

# (grupo, token, nombre, pantone sugerido o None, uso)
_DEF = [
    ('Grafito', 'grafito.950', 'Grafito 950', 'Black 6 C', 'Fondo principal oscuro; texto sobre claro'),
    ('Grafito', 'grafito.900', 'Grafito 900', 'Black 6 C (70 %)', 'Fondo alternativo de sección en oscuro'),
    ('Grafito', 'grafito.850', 'Grafito 850', '419 C', 'Superficie / tarjetas en oscuro'),
    ('Grafito', 'grafito.800', 'Grafito 800', '433 C', 'Superficie elevada en oscuro'),
    ('Grafito', 'grafito.700', 'Grafito 700', '432 C', 'Bordes y órbitas en oscuro'),
    ('Grafito', 'grafito.600', 'Grafito 600', '7545 C', 'Texto secundario sobre claro'),
    ('Grafito', 'grafito.500', 'Grafito 500', '431 C', 'Texto terciario sobre claro'),
    ('Grafito', 'grafito.400', 'Titanio 400', '430 C', 'Texto terciario sobre oscuro (no sobre blanco)'),
    ('Grafito', 'grafito.300', 'Grafito 300', '428 C', 'Iconos inactivos sobre claro, rellenos de gráfico'),
    ('Grafito', 'grafito.200', 'Grafito 200', '649 C', 'Bordes en claro; texto secundario en oscuro'),
    ('Grafito', 'grafito.100', 'Grafito 100', '656 C', 'Separadores y superficies claras'),
    ('Grafito', 'grafito.50', 'Grafito 50', None, 'Fondo claro alternativo (papel)'),
    ('Grafito', 'grafito.0', 'Blanco', None, 'Fondo claro principal; texto sobre oscuro'),
    ('Azul', 'azul.50', 'Azul 50', '656 C', 'Fondo de aviso informativo en claro'),
    ('Azul', 'azul.300', 'Azul 300', '2717 C', 'Enlaces sobre oscuro'),
    ('Azul', 'azul.400', 'Azul 400', '2718 C', 'Azul de marca sobre oscuro; inicio del gradiente oscuro'),
    ('Azul', 'azul.500', 'Azul IA 500', '2727 C', 'Color de marca: logo, gráficos, acento (texto ≥ 24 px)'),
    ('Azul', 'azul.600', 'Azul 600', '2726 C', 'Botones y enlaces sobre claro'),
    ('Azul', 'azul.700', 'Azul 700', '2728 C', 'Estado pulsado sobre claro'),
    ('Azul', 'azul.900', 'Azul 900', '2767 C', 'Fondos de dato azul muy oscuros'),
    ('Cyan', 'cyan.50', 'Cyan 50', '9520 C', 'Fondo suave de dato en claro'),
    ('Cyan', 'cyan.300', 'Cyan 300', '311 C (tinta 60 %)', 'Datos secundarios sobre oscuro'),
    ('Cyan', 'cyan.500', 'Cyan 500', '311 C', 'Final del gradiente en oscuro; datos'),
    ('Cyan', 'cyan.600', 'Cyan 600', '3125 C', 'Final del gradiente en claro'),
    ('Lima', 'lima.50', 'Lima 50', '7485 C', 'Fondo de «en marcha» en claro'),
    ('Lima', 'lima.300', 'Lima 300', '373 C', 'Texto lima atenuado sobre oscuro'),
    ('Lima', 'lima.500', 'Lima 500', '374 C', 'El nodo: dato destacado, acción, «en marcha» (sobre oscuro)'),
    ('Lima', 'lima.600', 'Lima 600', '376 C', 'Nodo sobre fondo claro (no para texto pequeño)'),
    ('Lima', 'lima.900', 'Lima 900', '5747 C', 'Texto sobre fondos lima claros'),
    ('Estado', 'estado.exito', 'Éxito', '355 C', 'Confirmaciones'),
    ('Estado', 'estado.aviso', 'Aviso', '1375 C', 'Avisos (con texto Grafito 950)'),
    ('Estado', 'estado.error', 'Error', '7417 C', 'Errores y validación'),
]


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = [ch(x) for x in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    a = hex_rgb(a) if isinstance(a, str) else a
    b = hex_rgb(b) if isinstance(b, str) else b
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def nivel(r):
    """Devuelve la etiqueta WCAG 2.2 para texto."""
    if r >= 7: return 'AAA'
    if r >= 4.5: return 'AA'
    if r >= 3: return 'AA grande'
    return 'No apto'


def rgb_hsl(rgb):
    r, g, b = [x / 255 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return round(h * 360), round(s * 100), round(l * 100)


def rgb_cmyk(rgb):
    """Conversión aproximada (sin perfil ICC) con un leve GCR para oscuros."""
    r, g, b = [x / 255 for x in rgb]
    k = 1 - max(r, g, b)
    if k >= 0.999:
        return (0, 0, 0, 100)
    c = (1 - r - k) / (1 - k); m = (1 - g - k) / (1 - k); y = (1 - b - k) / (1 - k)
    if k > 0.8:  # negro enriquecido frío para grafitos muy oscuros
        c, m, y = max(c, 0.6) * 0.75 + 0.15, max(m, 0.5) * 0.7 + 0.1, max(y, 0.4) * 0.6 + 0.1
    return tuple(round(v * 100) for v in (c, m, y, k))


def _get(token):
    g, t = token.split('.')
    return C[g][t].upper()


PALETA = []
for grupo, token, nombre, pantone, uso in _DEF:
    hx = _get(token)
    rgb = hex_rgb(hx)
    PALETA.append(dict(grupo=grupo, token=token, nombre=nombre, hex=hx, rgb=rgb, hsl=rgb_hsl(rgb),
                       cmyk=rgb_cmyk(rgb), pantone=pantone, uso=uso,
                       contraste_blanco=round(contraste(hx, '#FFFFFF'), 2),
                       contraste_grafito=round(contraste(hx, '#0B0D12'), 2)))

POR_NOMBRE = {p['nombre']: p for p in PALETA}
GRUPOS = ['Grafito', 'Azul', 'Cyan', 'Lima', 'Estado']
