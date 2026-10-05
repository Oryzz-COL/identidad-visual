"""
Oryzz · Generador de piezas para redes sociales
================================================

Lee el copy de `contenido/*.json` (o `*.csv`), lo pinta con las plantillas de
`../_plantillas/*.html` (Jinja2) y exporta PNG con Chrome headless.

    python generar.py                         # genera todo
    python generar.py instagram_oryzz         # un archivo de contenido
    python generar.py instagram_oryzz --solo 03_mito,08_cta
    python generar.py --html                  # solo HTML (para abrirlo y ajustar en el navegador)
    python generar.py --lista                 # plantillas, formatos y piezas disponibles
    python generar.py --hojas                 # además, hojas de contacto en _generador/_hojas/

Requisitos: Python 3.9+, `pip install jinja2 qrcode`, Google Chrome o Edge.
Formato del texto en el JSON:
    **texto**  → resaltado en azul (un fragmento por titular)
    ==texto==  → dato en lima (solo sobre oscuro; en claro, lima 600)
    ~~texto~~  → tachado          __texto__ → negrita          \n → salto de línea
"""
import argparse, csv, html, json, os, re, shutil, subprocess, sys, tempfile, pathlib, time
from concurrent.futures import ThreadPoolExecutor

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent                                  # 09_Redes_Sociales
IDENTIDAD = RAIZ.parent                             # Identidad_Visual
MAESTRA = IDENTIDAD / '00_Fuente_Maestra'
LOGOS = IDENTIDAD / '02_Logos'
PLANTILLAS = RAIZ / '_plantillas'
CONTENIDO = AQUI / 'contenido'
HTML_OUT = AQUI / '_html'
HOJAS = AQUI / '_hojas'

sys.path.insert(0, str(MAESTRA / 'build'))
sys.path.insert(0, str(AQUI))
import graficos  # noqa: E402

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined
    from markupsafe import Markup
except ImportError:
    sys.exit('Falta Jinja2:  pip install jinja2')

try:
    from render import CHROME  # 00_Fuente_Maestra/build/render.py
except Exception:  # pragma: no cover
    CHROME = None

# --------------------------------------------------------------------------- formatos
# nombre: (ancho, alto, clase CSS, escala de exportación)
FORMATOS = {
    'post':               (1080, 1350, 'f-post', 1),       # Instagram feed 4:5
    'story':              (1080, 1920, 'f-story', 1),      # Stories, Reels, TikTok
    'cuadrado':           (1200, 1200, 'f-cuadrado', 1),   # LinkedIn 1:1
    'li':                 (1200, 1500, 'f-li', 1),         # LinkedIn 4:5
    'documento':          (1080, 1350, 'f-post', 1),       # Portada de documento PDF de LinkedIn
    'li_banner_empresa':  (1128, 191, 'f-banner', 2),      # LinkedIn empresa (se exporta @2x)
    'li_banner_personal': (1584, 396, 'f-banner', 2),      # LinkedIn perfil (se exporta @2x)
    'youtube':            (1280, 720, 'f-horizontal', 1),
    'og':                 (1200, 630, 'f-horizontal', 1),
    'gbp':                (1200, 675, 'f-horizontal', 1),  # Google Business Profile, portada 16:9
    'avatar':             (640, 640, 'f-avatar', 1),       # WhatsApp Business (recorte circular)
}

# Límite de palabras por campo (aviso, no bloquea). Ver Guia_de_contenido_redes.md §4.
LIMITES = {'titular': 14, 'texto': 32, 'cita': 34, 'mito': 16, 'realidad': 24, 'cierre': 16, 'nota': 24}
LIMITE_ITEM = 11


def uri(p):
    return pathlib.Path(p).resolve().as_uri()


def logos_ctx():
    h = LOGOS / '01_Horizontal' / 'SVG'
    t = LOGOS / '07_Submarca_Tap' / 'SVG'
    i = LOGOS / '04_Isotipo' / 'SVG'
    v = LOGOS / '02_Vertical' / 'SVG'
    return {
        'oryzz_oscuro': uri(h / 'oryzz-logo-horizontal_color-sobre-oscuro.svg'),
        'oryzz_claro': uri(h / 'oryzz-logo-horizontal_color-sobre-claro.svg'),
        'oryzz_solido_oscuro': uri(h / 'oryzz-logo-horizontal_solido-sobre-oscuro.svg'),
        'oryzz_solido_claro': uri(h / 'oryzz-logo-horizontal_solido-sobre-claro.svg'),
        'tap_oscuro': uri(t / 'oryzz-tap-horizontal_color-sobre-oscuro.svg'),
        'tap_claro': uri(t / 'oryzz-tap-horizontal_color-sobre-claro.svg'),
        'tap_mono_oscuro': uri(t / 'oryzz-tap-horizontal_mono-grafito.svg'),   # tinta oscura (placa blanca)
        'tap_mono_claro': uri(t / 'oryzz-tap-horizontal_mono-blanco.svg'),     # tinta blanca (placa negra)
        'iso_oscuro': uri(i / 'oryzz-isotipo_color-sobre-oscuro.svg'),
        'iso_claro': uri(i / 'oryzz-isotipo_color-sobre-claro.svg'),
        'vertical_oscuro': uri(v / 'oryzz-logo-vertical_color-sobre-oscuro.svg'),
        'vertical_claro': uri(v / 'oryzz-logo-vertical_color-sobre-claro.svg'),
    }


# --------------------------------------------------------------------------- texto
def fmt(s):
    """Escapa y aplica el marcado ligero del copy."""
    if s is None or isinstance(s, Undefined):
        return Markup('')
    s = html.escape(str(s), quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<span class="hl">\1</span>', s, flags=re.S)
    s = re.sub(r'==(.+?)==', r'<span class="dato-tx">\1</span>', s, flags=re.S)
    s = re.sub(r'~~(.+?)~~', r'<s>\1</s>', s, flags=re.S)
    s = re.sub(r'__(.+?)__', r'<b>\1</b>', s, flags=re.S)
    s = s.replace('\n', '<br>')
    s = re.sub(r'(\d) (%|€|×|h\b|min\b|mm\b|COP\b)', '\\1&nbsp;\\2', s)
    s = s.replace('$ ', '$&nbsp;').replace(' · ', '&nbsp;· ')
    s = re.sub(r'(\d+[–-]\d+(?:&nbsp;[^\s<]+)?)', r'<span style="white-space:nowrap">\1</span>', s)
    return Markup(s)


def palabras(s):
    return len(re.sub(r'[*=~_]', '', str(s)).split())


def validar(p):
    avisos = []
    for campo, lim in LIMITES.items():
        v = p.get(campo)
        if isinstance(v, str) and palabras(v) > lim:
            avisos.append(f'{campo}: {palabras(v)} palabras (máx. recomendado {lim})')
    for campo in ('items', 'antes', 'despues', 'pasos'):
        for it in p.get(campo) or []:
            txt = it if isinstance(it, str) else (it.get('titulo') or it.get('texto') or '')
            if palabras(txt) > LIMITE_ITEM + 3:
                avisos.append(f'{campo}: «{txt[:40]}…» es largo ({palabras(txt)} palabras)')
    return avisos


# --------------------------------------------------------------------------- carga de contenido
def cargar(ruta):
    ruta = pathlib.Path(ruta)
    if ruta.suffix == '.csv':
        with open(ruta, encoding='utf-8-sig', newline='') as f:
            filas = list(csv.DictReader(f))
        piezas = []
        for fila in filas:
            p = {}
            for k, v in fila.items():
                if k is None or v is None or v == '':
                    continue
                if k.endswith('[]'):
                    p[k[:-2]] = [x.strip() for x in v.split('|') if x.strip()]
                else:
                    p[k] = v.replace('\\n', '\n')
            piezas.append(p)
        grupo = piezas[0].get('grupo', ruta.stem) if piezas else ruta.stem
        return {'grupo': grupo, 'comun': {}, 'piezas': piezas}
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


def expandir(doc):
    """Aplica valores comunes, temas múltiples y slides de carrusel. Devuelve trabajos."""
    comun = doc.get('comun', {})
    grupo = doc.get('grupo', 'salida')
    por_tema = doc.get('salida_por_tema', 'sufijo')     # 'sufijo' | 'carpeta'
    trabajos = []
    for pieza in doc['piezas']:
        base = {**comun, **pieza}
        temas = base.pop('temas', None) or [base.get('tema', 'oscuro')]
        slides = base.pop('slides', None)
        for tema in temas:
            variantes = [dict(base)] if not slides else [
                {**base, **s, 'id': f"{base['id']}_{i + 1:02d}", 'slide': i, 'n_slides': len(slides),
                 'contador': (i + 1, len(slides)), 'carrusel_id': base['id']}
                for i, s in enumerate(slides)]
            for v in variantes:
                v['tema'] = tema
                v.setdefault('grupo', grupo)
                nombre = v['id']
                carpeta = v.get('carpeta', '')
                if len(temas) > 1:
                    if por_tema == 'carpeta':
                        carpeta = os.path.join(carpeta, tema)
                    else:
                        nombre = f'{nombre}_{tema}'
                v['_salida'] = RAIZ / v['grupo'] / carpeta / f'{nombre}.png'
                v['_html'] = HTML_OUT / v['grupo'] / carpeta / f'{nombre}.html'
                trabajos.append(v)
    return trabajos


# --------------------------------------------------------------------------- render
def entorno():
    env = Environment(loader=FileSystemLoader(str(PLANTILLAS)), autoescape=True,
                      trim_blocks=True, lstrip_blocks=True)
    env.filters['t'] = fmt
    for nombre in ('orbitas', 'ruta', 'panorama_carrusel', 'arco_reloj', 'icono', 'qr', 'arco'):
        env.globals[nombre] = getattr(graficos, nombre)
    env.globals['logos'] = logos_ctx()
    return env


def contexto(p):
    fmt_nombre = p.get('formato', 'post')
    W, H, clase, escala = FORMATOS[fmt_nombre]
    W, H = int(p.get('ancho', W)), int(p.get('alto', H))
    marca = p.get('marca', 'oryzz')
    tema = p.get('tema', 'oscuro')
    lg = logos_ctx()
    if marca == 'tap':
        logo = lg['tap_oscuro'] if tema == 'oscuro' else lg['tap_claro']
    else:
        logo = lg['oryzz_oscuro'] if tema == 'oscuro' else lg['oryzz_claro']
    ctx = dict(p)
    ctx.update(W=W, H=H, formato=fmt_nombre, formato_clase=clase, escala=int(p.get('escala', escala)),
               marca=marca, tema=tema, logo=logo, iso=lg['iso_oscuro'] if tema == 'oscuro' else lg['iso_claro'],
               css_marca=uri(MAESTRA / 'brand.css'), css_social=uri(PLANTILLAS / 'social.css'))
    ctx.setdefault('handle', '@oryzztap' if marca == 'tap' else '@oryzzai')
    ctx.setdefault('web', 'oryzz.com/tap' if marca == 'tap' else 'oryzz.com')
    for k in ('foto', 'foto_2'):
        if ctx.get(k) and not str(ctx[k]).startswith(('http', 'file:')):
            ctx[k] = uri(RAIZ / ctx[k])
    return ctx


def chrome_png(html_path, png_path, W, H, escala=1):
    if not CHROME:
        raise RuntimeError('No se encontró Chrome/Edge (ver 00_Fuente_Maestra/build/render.py)')
    os.makedirs(png_path.parent, exist_ok=True)
    perfil = tempfile.mkdtemp(prefix='oryzz_chrome_')
    try:
        args = [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
                '--no-default-browser-check', '--allow-file-access-from-files',
                '--run-all-compositor-stages-before-draw', '--virtual-time-budget=6000',
                f'--user-data-dir={perfil}', f'--force-device-scale-factor={escala}',
                f'--window-size={W},{H}', f'--screenshot={png_path}', uri(html_path)]
        subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    finally:
        shutil.rmtree(perfil, ignore_errors=True)


def desborda_png(ruta):
    """True si la pieza muestra la franja roja de «texto demasiado largo» (requiere Pillow)."""
    try:
        from PIL import Image
        im = Image.open(ruta).convert('RGB')
        r, g, b = im.getpixel((im.width // 2, 4))
        return abs(r - 0xE5) < 12 and abs(g - 0x48) < 12 and abs(b - 0x4D) < 12
    except Exception:
        return False


def generar(trabajos, solo_html=False, hilos=4):
    env = entorno()
    pendientes = []
    for p in trabajos:
        ctx = contexto(p)
        plantilla = env.get_template(p['plantilla'] + '.html')
        out = plantilla.render(**ctx)
        p['_html'].parent.mkdir(parents=True, exist_ok=True)
        p['_html'].write_text(out, encoding='utf-8')
        for a in validar(p):
            print(f'  aviso  {p["id"]}: {a}')
        pendientes.append((p, ctx))
    if solo_html:
        print(f'HTML en {HTML_OUT}')
        return
    t0 = time.time()

    def uno(item):
        p, ctx = item
        chrome_png(p['_html'], p['_salida'], ctx['W'], ctx['H'], ctx['escala'])
        return p['_salida']

    with ThreadPoolExecutor(max_workers=hilos) as ex:
        for ruta in ex.map(uno, pendientes):
            estado = 'ok    '
            if desborda_png(ruta):
                estado = 'DESBORDA'   # franja roja: el texto no cabe ni al cuerpo mínimo
            print(f'  {estado}', ruta.relative_to(RAIZ))
    print(f'{len(pendientes)} piezas en {time.time() - t0:.0f} s')


def hoja(grupo, pngs, columnas=4):
    """Hoja de contacto para revisar un grupo de un vistazo."""
    HOJAS.mkdir(parents=True, exist_ok=True)
    celdas = ''.join(f'<figure><img src="{uri(p)}"><figcaption>{p.relative_to(RAIZ)}</figcaption></figure>' for p in pngs)
    doc = (f'<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="{uri(MAESTRA / "brand.css")}">'
           f'<style>body{{margin:0;padding:40px;background:#1c1f27;font-family:var(--font-mono);color:#8A90A0}}'
           f'main{{display:grid;grid-template-columns:repeat({columnas},1fr);gap:28px}}figure{{margin:0}}'
           f'img{{width:100%;display:block;border-radius:6px;box-shadow:0 0 0 1px #2b303c}}figcaption{{font-size:13px;margin-top:8px}}'
           f'h1{{font:600 22px var(--font-display);color:#fff;margin:0 0 24px}}</style><h1>{grupo}</h1><main>{celdas}</main>')
    ruta_html = HOJAS / f'{grupo.replace("/", "_")}.html'
    ruta_html.write_text(doc, encoding='utf-8')
    return ruta_html


def main():
    ap = argparse.ArgumentParser(description='Genera las piezas de redes de Oryzz.')
    ap.add_argument('contenido', nargs='*', help='archivos de contenido (sin extensión) · por defecto todos')
    ap.add_argument('--solo', help='ids separados por comas')
    ap.add_argument('--html', action='store_true', help='solo genera HTML')
    ap.add_argument('--lista', action='store_true')
    ap.add_argument('--hojas', action='store_true')
    ap.add_argument('--hilos', type=int, default=4)
    a = ap.parse_args()

    archivos = sorted(list(CONTENIDO.glob('*.json')) + list(CONTENIDO.glob('*.csv')))
    if a.contenido:
        archivos = [f for f in archivos if f.stem in a.contenido]
        if not archivos:
            sys.exit('No encuentro ese contenido. Usa --lista.')

    if a.lista:
        print('Plantillas:', ', '.join(sorted(p.stem for p in PLANTILLAS.glob('*.html') if not p.stem.startswith('_'))))
        print('Formatos:  ', ', '.join(f'{k} {v[0]}×{v[1]}' for k, v in FORMATOS.items()))
        for f in archivos:
            print(f'\n{f.name}')
            for t in expandir(cargar(f)):
                print(f'   {t["id"]:<28} {t["plantilla"]:<22} {t.get("formato", "post"):<18} {t["tema"]}')
        return

    todos = []
    for f in archivos:
        trabajos = expandir(cargar(f))
        if a.solo:
            ids = set(a.solo.split(','))
            trabajos = [t for t in trabajos if t['id'] in ids or t.get('carrusel_id') in ids]
        if not trabajos:
            continue
        print(f'\n{f.name} · {len(trabajos)} piezas')
        todos += trabajos
    generar(todos, solo_html=a.html, hilos=a.hilos)

    # Vista continua de cada carrusel (todas las slides juntas, al 40 %) para revisar la ruta
    if not a.html:
        carruseles = {}
        for t in todos:
            if t.get('carrusel_id'):
                carruseles.setdefault((t['carrusel_id'], t['tema'], str(t['_salida'].parent)), []).append(t['_salida'])
        for (cid, tema, carpeta), pngs in carruseles.items():
            try:
                from PIL import Image
            except ImportError:
                break
            ims = [Image.open(p) for p in pngs]
            w, h = ims[0].size
            k = 0.4
            tira = Image.new('RGB', (int(w * k) * len(ims), int(h * k)))
            for i, im in enumerate(ims):
                tira.paste(im.convert('RGB').resize((int(w * k), int(h * k)), Image.LANCZOS), (int(w * k) * i, 0))
            destino = pathlib.Path(carpeta) / f'_vista_continua_{cid}.png'
            tira.save(destino)
            print('  tira  ', destino.relative_to(RAIZ))

    if a.hojas and not a.html:
        grupos = {}
        for t in todos:
            grupos.setdefault(t['grupo'], []).append(t)
        for g, ts in grupos.items():
            cols = 3 if ts[0].get('formato') in ('story',) else (2 if ts[0].get('formato', '').startswith(('li_banner', 'og', 'youtube', 'gbp')) else 4)
            h = hoja(g, [t['_salida'] for t in ts], cols)
            try:
                from PIL import Image
                ancho_c = (1800 - 80 - (cols - 1) * 28) / cols
                altos = [Image.open(t['_salida']).size for t in ts]
                altos = [ancho_c * h / w + 40 for w, h in altos]
                filas = [max(altos[i:i + cols]) for i in range(0, len(altos), cols)]
                alto = int(140 + sum(filas) + 28 * len(filas))
            except Exception:
                alto = 200 + ((len(ts) + cols - 1) // cols) * 900
            chrome_png(h, HOJAS / f'{g.replace("/", "_")}.png', 1800, alto)
            print('  hoja  ', (HOJAS / f'{g.replace("/", "_")}.png').relative_to(RAIZ))


if __name__ == '__main__':
    main()
