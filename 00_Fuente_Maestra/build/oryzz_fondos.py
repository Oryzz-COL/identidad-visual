"""
oryzz_fondos.py · Fondos de marca listos para usar (Oryzz v2.0).

Cada fondo combina: órbita grande recortada + retícula 64 px desvanecida + un halo ≤ 20 % + un nodo.
Composición asimétrica con una zona de texto reservada (se exporta en fondos.json para que
slides, redes y documentos coloquen el texto sin tapar el nodo).

Uso:  python oryzz_fondos.py   → 05_Elementos_Graficos/03_Fondos
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oryzz_svg import C, THEME, ROOT, write, doc, halo, png_from_svg, T, embed_logo
from oryzz_patrones import orbitas, reticula_comp, nodos, convergencia

OUT = os.path.join(ROOT, '05_Elementos_Graficos', '03_Fondos')

# A4 se diseña a 1240×1754 (150 ppp) y se exporta a 2480×3508 (300 ppp)
FMT = {'16x9': (1920, 1080), '4x5': (1080, 1350), '9x16': (1080, 1920), 'A4': (1240, 1754)}

FONDOS = [
    # id, formato, tema, receta, parámetros, zona de texto (x, y, w, h)
    ('01', '16x9', 'oscuro', 'orbita', dict(np=(1350, 480), cx=1650, cy=760, esc=1.55, rot=0, halo=(1650, 760, 900, .13)), (120, 120, 880, 840)),
    ('02', '16x9', 'claro', 'orbita', dict(np=(1500, 700), cx=1900, cy=1060, esc=2.0, rot=-40, halo=(1800, 980, 900, .10)), (120, 120, 960, 840)),
    ('03', '16x9', 'oscuro', 'rutas', dict(hub=(1472, 800), fuentes=[(832, 800), (1024, 672), (704, 992), (960, 928)],
                                           salida=[(1728, 800), (1728, 608), (1940, 608)], halo=(1472, 800, 700, .14)), (120, 120, 1000, 440)),
    ('04', '16x9', 'claro', 'reticula', dict(np=(1500, 300), cx=2080, cy=-160, esc=2.4, rot=35, halo=(1700, 200, 800, .08)), (120, 360, 1000, 600)),
    ('05', '4x5', 'oscuro', 'orbita', dict(np=(700, 850), cx=900, cy=1180, esc=1.45, rot=-70, halo=(900, 1180, 800, .16)), (96, 96, 888, 620)),
    ('06', '4x5', 'claro', 'orbita', dict(np=(800, 500), cx=1060, cy=260, esc=1.35, rot=90, halo=(1000, 260, 700, .10)), (96, 700, 888, 554)),
    ('07', '4x5', 'oscuro', 'nodos', dict(np=(800, 1000), cx=1120, cy=1300, esc=1.8, rot=-60, halo=(820, 980, 700, .14)), (96, 96, 888, 600)),
    ('08', '9x16', 'oscuro', 'orbita', dict(np=(600, 1250), cx=860, cy=1560, esc=1.6, rot=-80, halo=(860, 1560, 900, .16)), (96, 192, 888, 900)),
    ('09', '9x16', 'claro', 'orbita', dict(np=(760, 640), cx=1040, cy=380, esc=1.5, rot=100, halo=(960, 380, 800, .10)), (96, 960, 888, 768)),
    ('10', '9x16', 'oscuro', 'rutas', dict(hub=(736, 1472), fuentes=[(160, 1472), (288, 1216), (224, 1728), (352, 1024)],
                                          salida=[(864, 1472), (864, 1216), (1100, 1216)], halo=(736, 1472, 700, .14)), (96, 192, 888, 720)),
    ('11', 'A4', 'oscuro', 'orbita', dict(np=(850, 1230), cx=1090, cy=1480, esc=1.35, rot=-75, halo=(1090, 1480, 900, .16)), (100, 140, 900, 760)),
    ('12', 'A4', 'claro', 'orbita', dict(np=(950, 340), cx=1200, cy=120, esc=1.3, rot=110, halo=(1150, 150, 800, .08)), (100, 900, 1000, 700)),
]


def receta(w, h, tema, kind, p, uid):
    t = THEME[tema]
    s = ''
    hx, hy, hr, hop = p['halo']
    s += halo(uid + 'h', hx, hy, hr, t['halo'], hop)
    s += reticula_comp(w, h, tema, uid=uid + 'r', fx=hx, fy=hy, fr=max(w, h) * 0.6)
    if kind in ('orbita', 'reticula', 'nodos'):
        if kind == 'nodos':
            s += nodos(w, h, tema, uid=uid + 'n', fx=p['cx'] - 300, fy=p['cy'] - 300, fr=max(w, h) * 0.75, op=0.9)
        n_en = 2
        s += orbitas(w, h, tema, cx=p['cx'], cy=p['cy'], uid=uid + 'o', escala=p['esc'], rot=p['rot'],
                     nodo_en=n_en, sw=1.5, nodo_r=8 if w < 1500 else 9, op_out=0.3,
                     satelites=kind != 'reticula', nodo_hacia=p.get('np'))
    elif kind == 'rutas':
        s += convergencia(w, h, tema, p['hub'], p['fuentes'], uid=uid + 'c', salida=p['salida'], sw=1.75, rad=40)
    return s


def build():
    jobs = []; meta = []
    for fid, fmt, tema, kind, p, zona in FONDOS:
        w, h = FMT[fmt]
        name = f'oryzz-fondo-{fid}_{kind}_{tema}_{fmt}'
        body = receta(w, h, tema, kind, p, f'f{fid}')
        svg = doc(w, h, body, f'Oryzz · fondo {fid} · {kind} · {tema} · {fmt}', bg=THEME[tema]['fondo'],
                  desc=f'Zona de texto recomendada: x={zona[0]} y={zona[1]} w={zona[2]} h={zona[3]} (px del viewBox).')
        sp = os.path.join(OUT, 'SVG', name + '.svg'); write(sp, svg)
        outw = 2480 if fmt == 'A4' else w
        jobs.append((sp, os.path.join(OUT, 'PNG', name + '.png'), outw))
        sc = outw / w
        meta.append(dict(id=fid, archivo=name, formato=fmt, tema=tema, receta=kind, px=[outw, round(h * sc)],
                         zona_texto_px=[round(v * sc) for v in zona],
                         zona_texto_pct=[round(zona[0] / w * 100, 1), round(zona[1] / h * 100, 1),
                                         round(zona[2] / w * 100, 1), round(zona[3] / h * 100, 1)]))
    png_from_svg(jobs)
    write(os.path.join(OUT, 'fondos.json'), json.dumps(dict(
        nota='Zona de texto en px del PNG exportado y en % del lienzo [x, y, ancho, alto]. El nodo lima queda siempre fuera.',
        fondos=meta), ensure_ascii=False, indent=2))
    # A4 → PDF a sangre
    from render import html_to_pdf
    for m in meta:
        if m['formato'] != 'A4':
            continue
        hp = os.path.join(OUT, 'PDF', m['archivo'] + '.html')
        write(hp, f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:210mm 297mm;margin:0}}'
                  f'html,body{{margin:0}}img{{display:block;width:210mm;height:297mm}}</style></head>'
                  f'<body><img src="../SVG/{m["archivo"]}.svg"></body></html>')
        html_to_pdf(hp, os.path.join(OUT, 'PDF', m['archivo'] + '.pdf'))
        os.remove(hp)
    return meta


def lamina(meta):
    """Lámina de muestra con la zona de texto dibujada y un titular real de ejemplo."""
    from render import html_to_png, html_to_pdf
    frases = {'01': ('Más <em>clientes</em>.<br>No más likes.', 'Sistemas que captan clientes'),
              '02': ('Un sistema de captación,<br>no acciones <em>sueltas</em>.', 'Método Oryzz'),
              '03': ('No es que no te vean.<br>Es que no te <em>contactan</em>.', 'Diagnóstico'),
              '04': ('30 minutos.', 'Valoración gratuita'),
              '05': ('Te traemos <em>clientes</em>,<br>no likes.', 'Captación con IA'),
              '06': ('Tu negocio.<br>A un <em>toque</em>.', 'Oryzz Tap'),
              '07': ('Validamos con datos<br>antes de que <em>gastes</em>.', 'Prueba inicial'),
              '08': ('Más <em>clientes</em>.<br>No más likes.', 'Oryzz'),
              '09': ('Acerca el teléfono<br>y <em>ocurre</em>.', 'Oryzz Tap'),
              '10': ('Si no encajamos,<br>te lo <em>decimos</em>.', 'Valoración 30 min'),
              '11': ('Propuesta de<br><em>captación</em>', 'Documento · 2026'),
              '12': ('Informe<br>mensual', 'Clínica dental · Ejemplo')}
    cards = ''
    for m in meta:
        pw, ph = m['px']; zx, zy, zw, zh = m['zona_texto_pct']
        dark = m['tema'] == 'oscuro'
        t, e = frases[m['id']]
        cards += (f'<figure class="f{m["formato"]}{" r2" if m["id"] == "04" else ""} {"d" if dark else "l"}"><div class="art" style="aspect-ratio:{pw}/{ph}">'
                  f'<img src="PNG/{m["archivo"]}.png">'
                  f'<div class="z" style="left:{zx}%;top:{zy}%;width:{zw}%;height:{zh}%"><span class="eb">{e}</span><b>{t}</b></div></div>'
                  f'<figcaption><span>{m["id"]}</span>{m["receta"]} · {m["tema"]} · {m["formato"].replace("x", ":")}</figcaption></figure>')
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Fondos Oryzz</title>
<link rel="stylesheet" href="../../00_Fuente_Maestra/brand.css"><style>
@page{{size:1920px 2000px;margin:0}} *{{box-sizing:border-box}}
html,body{{margin:0;background:var(--grafito-900);color:#fff;font-family:var(--font-texto)}}
body{{width:1920px;height:2000px;padding:112px 120px;overflow:hidden}}
.t-eyebrow{{color:var(--grafito-400)}}
h1{{font-family:var(--font-display);font-size:72px;letter-spacing:-.04em;line-height:1;margin:20px 0 16px}}
p.lead{{color:var(--grafito-200);font-size:20px;max-width:980px;margin:0 0 56px;line-height:1.5}}
.grid{{display:grid;grid-template-columns:repeat(24,1fr);gap:48px 32px;align-items:end}}
figure{{margin:0}} figure.f16x9{{grid-column:span 8}} figure.f4x5{{grid-column:span 5}} figure.f9x16{{grid-column:span 4}} figure.fA4{{grid-column:span 6}} figure.f16x9.r2{{grid-column:span 9}}
.art{{container-type:inline-size;position:relative;border-radius:10px;overflow:hidden;outline:1px solid var(--grafito-700)}}
.art img{{position:absolute;inset:0;width:100%;height:100%}}
.z{{position:absolute;outline:1px dashed rgba(92,139,255,.7);display:flex;flex-direction:column;gap:8px;padding:6% 5%;justify-content:flex-start}}
.z b{{font-family:var(--font-display);font-weight:700;letter-spacing:-.035em;line-height:1.02;font-size:4.6cqw}}
.z .eb{{font-family:var(--font-mono);font-size:max(11px,1.5cqw);letter-spacing:.16em;text-transform:uppercase}}
.d .z b{{color:#fff}} .d .z b em{{font-style:normal;color:var(--azul-400)}} .d .eb{{color:var(--grafito-400)}}
.l .z b{{color:var(--grafito-950)}} .l .z b em{{font-style:normal;color:var(--azul-500)}} .l .eb{{color:var(--grafito-500)}}
.f9x16 .z b,.fA4 .z b{{font-size:9cqw}} .f4x5 .z b{{font-size:7.5cqw}}
figcaption{{font-family:var(--font-mono);font-size:14px;color:var(--grafito-400);margin-top:14px;letter-spacing:.04em}}
figcaption span{{color:#fff;margin-right:10px}}
.note{{position:absolute;left:120px;bottom:72px;font-family:var(--font-mono);font-size:14px;color:var(--grafito-500);letter-spacing:.06em}}
</style></head><body>
<p class="t-eyebrow">Oryzz · 05 · Elementos gráficos · 03 Fondos</p>
<h1>Fondos de marca</h1>
<p class="lead">Doce fondos listos en 16:9, 4:5, 9:16 y A4. La línea discontinua marca la zona de texto recomendada (en fondos.json). El nodo lima queda siempre fuera de ella y es el único acento de la pieza.</p>
<div class="grid">{cards}</div>
<div class="note">LÍNEA DISCONTINUA = ZONA DE TEXTO · NO SE EXPORTA CON EL FONDO</div>
</body></html>'''
    hp = os.path.join(OUT, 'fondos-lamina.html'); write(hp, page)
    html_to_png(hp, os.path.join(OUT, 'fondos-lamina.png'), 1920, 2000)
    html_to_pdf(hp, os.path.join(OUT, 'fondos-lamina.pdf'))


if __name__ == '__main__':
    m = build()
    lamina(m)
    print(len(m), 'fondos')
