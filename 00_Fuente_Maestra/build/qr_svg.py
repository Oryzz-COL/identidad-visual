"""
Oryzz · QR vectorial (una sola <path>, sin rasterizar).

    from qr_svg import qr_group, qr_svg
    g = qr_group('https://oryzz.com', x=10, y=10, size=18, color='#0B0D12')
    open('qr.svg','w').write(qr_svg('https://oryzz.com', 30))

Corrección de errores M. Zona de silencio: 4 módulos (incluida en `size` si quiet=True).
Regla de marca: QR siempre oscuro sobre claro (Grafito 950 sobre blanco / Grafito 50);
sobre fondos oscuros va dentro de una pastilla clara.
"""
import qrcode
from qrcode.constants import ERROR_CORRECT_M


def _matrix(data, ec=ERROR_CORRECT_M):
    q = qrcode.QRCode(error_correction=ec, border=0, box_size=1)
    q.add_data(data); q.make(fit=True)
    return q.get_matrix()


def qr_path_d(data, x=0.0, y=0.0, size=20.0, quiet=True):
    m = _matrix(data)
    n = len(m)
    total = n + (8 if quiet else 0)
    u = size / total
    off = 4 * u if quiet else 0
    parts = []
    for r, row in enumerate(m):
        c = 0
        while c < n:
            if row[c]:
                s = c
                while c < n and row[c]:
                    c += 1
                parts.append(f'M{x + off + s * u:.3f} {y + off + r * u:.3f}h{(c - s) * u:.3f}v{u:.3f}h{-(c - s) * u:.3f}z')
            else:
                c += 1
    return ''.join(parts), n


def qr_group(data, x=0, y=0, size=20, color='#0B0D12', fondo=None, radio=0, quiet=True, id_=None):
    d, _ = qr_path_d(data, x, y, size, quiet)
    bg = f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{radio}" fill="{fondo}"/>' if fondo else ''
    ida = f' id="{id_}"' if id_ else ''
    return f'<g{ida}>{bg}<path d="{d}" fill="{color}"/></g>'


def qr_svg(data, size=30, color='#0B0D12', fondo='#FFFFFF'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}mm" height="{size}mm">'
            f'{qr_group(data, 0, 0, size, color, fondo)}</svg>\n')


if __name__ == '__main__':
    import sys
    data = sys.argv[1] if len(sys.argv) > 1 else 'https://oryzz.com'
    out = sys.argv[2] if len(sys.argv) > 2 else 'qr.svg'
    open(out, 'w', encoding='utf8').write(qr_svg(data))
    print('ok', out)
