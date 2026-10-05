"""
Oryzz · generador del recurso «Órbitas» (BRAND_SPEC §5.1).
Arcos abiertos concéntricos, trazo fino, un solo nodo.

    from orbitas import orbitas_svg, orbitas_group
    svg = orbitas_svg(210, 297, cx=178, cy=92, radios=[34, 56, 78, 100, 122],
                      trazo='#232836', grosor=0.35, nodo='#BFF24A')

Las unidades son las del viewBox (mm en piezas impresas, px en pantalla).
"""
import math

# Hueco de cada órbita (grados, y hacia abajo). Se rota para que los cortes no se alineen.
_HUECOS = [(-115, -65), (150, 196), (20, 58), (-160, -128), (95, 128), (-40, -12), (205, 232)]


def _pt(cx, cy, r, a):
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arco(cx, cy, r, a0, a1):
    """Arco desde a1 hasta a0 recorriendo el lado largo (órbita abierta)."""
    x0, y0 = _pt(cx, cy, r, a1)
    x1, y1 = _pt(cx, cy, r, a0 + 360)
    span = (a0 + 360) - a1
    large = 1 if span > 180 else 0
    return f'M{x0:.2f} {y0:.2f}A{r:.2f} {r:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}'


def orbitas_group(cx, cy, radios, trazo='#232836', grosor=0.35, nodo='#BFF24A',
                  nodo_en=2, nodo_r=None, nodo_ang=None, opacidad=1.0):
    """Devuelve un <g> con las órbitas. `nodo_en` = índice de la órbita que lleva el nodo."""
    nodo_r = nodo_r or max(grosor * 5.5, 1.6)
    out = [f'<g fill="none" stroke="{trazo}" stroke-width="{grosor}" stroke-linecap="round" opacity="{opacidad}">']
    node_xy = None
    for i, r in enumerate(radios):
        a0, a1 = _HUECOS[i % len(_HUECOS)]
        if i == nodo_en and nodo:
            ang = nodo_ang if nodo_ang is not None else a1
            # el nodo se sitúa en un extremo del arco, separado por un corte (como el isotipo v2)
            gap_deg = math.degrees((nodo_r + grosor * 2 + nodo_r * 0.6) / r)
            node_xy = _pt(cx, cy, r, ang)
            # como en el isotipo: hueco abierto de ~50° antes del nodo y un corte fino después
            a0, a1 = ang - 50, ang + gap_deg
        out.append(f'<path d="{_arco(cx, cy, r, a0, a1)}"/>')
    out.append('</g>')
    if node_xy:
        out.append(f'<circle cx="{node_xy[0]:.2f}" cy="{node_xy[1]:.2f}" r="{nodo_r:.2f}" fill="{nodo}"/>')
    return ''.join(out)


def orbitas_svg(w, h, cx, cy, radios, fondo=None, **kw):
    bg = f'<rect width="{w}" height="{h}" fill="{fondo}"/>' if fondo else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}mm" height="{h}mm">'
            f'{bg}{orbitas_group(cx, cy, radios, **kw)}</svg>\n')


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else 'orbitas.svg'
    open(out, 'w', encoding='utf8').write(orbitas_svg(210, 297, 178, 92, [34, 56, 78, 100, 122, 144]))
    print('ok')
