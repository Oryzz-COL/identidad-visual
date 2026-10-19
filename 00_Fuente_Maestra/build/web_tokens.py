"""
Genera 11_Web_y_Codigo/tokens/* y fonts/fonts.css a partir de 00_Fuente_Maestra/tokens.json.
No edites los archivos generados a mano: cambia tokens.json y vuelve a ejecutar.

Uso:  python web_tokens.py
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
T = json.load(open(os.path.join(HERE, '..', 'tokens.json'), encoding='utf8'))
OUT = os.path.join(ROOT, '11_Web_y_Codigo', 'tokens')
FONTS_OUT = os.path.join(ROOT, '11_Web_y_Codigo', 'fonts')
os.makedirs(OUT, exist_ok=True)
C, SEM, TS = T['color'], T['semantic'], T['type-scale-px']
V = T['meta']['version']
HEAD = f'Oryzz · design tokens v{V} ({T["meta"]["date"]}) — GENERADO desde 00_Fuente_Maestra/tokens.json con build/web_tokens.py. No editar a mano.'

FONTS = [
    ('Space Grotesk', 'SpaceGrotesk', [(300, 'Light'), (400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold')]),
    ('Manrope', 'Manrope', [(400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold')]),
    ('JetBrains Mono', 'JetBrainsMono', [(400, 'Regular'), (500, 'Medium'), (700, 'Bold')]),
]
FAMILY = {'display': T['font']['display'], 'texto': T['font']['texto'], 'mono': T['font']['mono']}


def ff(key):
    f = FAMILY[key]
    return f"'{f['family']}', {f['fallback']}"


def font_faces(base='/fonts/'):
    out = []
    for fam, file, ws in FONTS:
        for w, n in ws:
            out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;"
                       f"src:url('{base}{file}-{n}.woff2') format('woff2')}}")
    return '\n'.join(out)


# Semántica ampliada (estados de interacción y foco) sobre la de tokens.json
EXTRA = {
    'oscuro': {'cta-fondo-hover': 'linear-gradient(135deg, #9FB8FF 0%, #7DE6F2 100%)', 'cta-2-fondo': 'transparent',
               'cta-2-texto': '#FFFFFF', 'cta-2-borde': '#5A6172', 'foco': '#5C8BFF', 'seleccion': '#2C5BD0',
               'enlace-hover': '#FFFFFF', 'borde-fuerte': '#5A6172', 'exito': '#1F9D55', 'aviso': '#F2A33A', 'error': '#E5484D',
               'texto-sobre-dato': '#0B0D12', 'dato-texto': '#BFF24A'},
    'claro': {'cta-fondo-hover': '#1F43A0', 'cta-2-fondo': '#FFFFFF', 'cta-2-texto': '#0B0D12', 'cta-2-borde': '#8A90A0',
              'foco': '#2C5BD0', 'seleccion': '#9FB8FF', 'enlace-hover': '#1F43A0', 'borde-fuerte': '#8A90A0',
              'exito': '#1F9D55', 'aviso': '#F2A33A', 'error': '#E5484D', 'texto-sobre-dato': '#FFFFFF', 'dato-texto': '#3A4A12'},
}


def sem_value(v):
    if v.startswith('gradient.'):
        return T['gradient'][v.split('.', 1)[1]]
    return v


def hex_to_var(v):
    """Sustituye un HEX por la variable primitiva equivalente si existe."""
    for g, scale in C.items():
        for k, hx in scale.items():
            if hx.upper() == v.upper():
                return f'var(--{g}-{k})'
    if v.startswith('linear-gradient(135deg, #5C8BFF'):
        return 'var(--grad-ia-oscuro)'
    if v.startswith('linear-gradient(135deg, #3B72FF'):
        return 'var(--grad-ia-claro)'
    return v


def semantic_block(mode):
    lines = []
    for k, v in list(SEM[mode].items()) + list(EXTRA[mode].items()):
        lines.append(f'  --color-{k}:{hex_to_var(sem_value(v))};')
    lines.append(f"  color-scheme:{'dark' if mode == 'oscuro' else 'light'};")
    return '\n'.join(lines)


# ------------------------------------------------------------------ tokens.css
def write_css():
    prim = []
    for g, scale in C.items():
        for k, hx in scale.items():
            prim.append(f'  --{g}-{k}:{hx.upper()};')
    for k, v in T['gradient'].items():
        prim.append(f'  --grad-{k}:{v};')
    prim += [f"  --font-display:{ff('display')};", f"  --font-texto:{ff('texto')};", f"  --font-mono:{ff('mono')};"]
    for k, s in TS.items():
        prim.append(f"  --text-{k}:{s['size'] / 16:g}rem; --leading-{k}:{s['line']}; --tracking-{k}:{s['tracking'] if s['tracking'] != '0' else '0em'};")
    for i, s in enumerate(T['space-px']):
        prim.append(f'  --space-{i + 1}:{s}px;')
    for k, v in T['radius-px'].items():
        prim.append(f'  --radius-{k}:{v if isinstance(v, str) else str(v) + "px"};')
    for k, v in T['stroke-px'].items():
        prim.append(f'  --stroke-{k}:{v}px;')
    for k, v in T['motion'].items():
        prim.append(f'  --motion-{k}:{v};')
    prim += ['  --max-ancho:1200px;', '  --gutter:24px;']

    css = f"""/* {HEAD}
 *
 * Uso:
 *   <link rel="stylesheet" href="/tokens.css">          (incluye @font-face → /fonts/*.woff2)
 *   <html data-tema="oscuro">  → oryzz.com (por defecto)
 *   <html data-tema="claro">   → oryzz.com/tap, documentos web, emails claros
 *   Se puede anidar: <section data-tema="claro"> dentro de una página oscura.
 */

/* ---------------------------------------------------------------- Fuentes */
{font_faces()}

/* ---------------------------------------------------------------- Primitivos */
:root{{
{chr(10).join(prim)}
}}

/* ---------------------------------------------------------------- Semántica · oscuro (por defecto) */
:root, [data-tema="oscuro"]{{
{semantic_block('oscuro')}
}}

/* ---------------------------------------------------------------- Semántica · claro */
[data-tema="claro"]{{
{semantic_block('claro')}
}}

/* Opcional: seguir la preferencia del sistema con data-tema="auto" */
@media (prefers-color-scheme: light){{
  [data-tema="auto"]{{
{semantic_block('claro')}
  }}
}}

/* ---------------------------------------------------------------- Base mínima */
[data-tema]{{background-color:var(--color-fondo);color:var(--color-texto-2)}}
::selection{{background:var(--color-seleccion);color:var(--color-texto)}}
:focus-visible{{outline:2px solid var(--color-foco);outline-offset:3px;border-radius:var(--radius-xs)}}
@media (prefers-reduced-motion: reduce){{*,*::before,*::after{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}}}
"""
    open(os.path.join(OUT, 'tokens.css'), 'w', encoding='utf8').write(css)


# ------------------------------------------------------------------ tokens.scss
def write_scss():
    L = [f'// {HEAD}', '// Uso: @use "tokens" as ox;  →  color: ox.$azul-600;  @include ox.tema(claro);', '@use "sass:map";', '']
    for g, scale in C.items():
        for k, hx in scale.items():
            L.append(f'${g}-{k}: {hx.upper()};')
        L.append('')
    for k, v in T['gradient'].items():
        L.append(f'$grad-{k}: {v};')
    L += ['', f"$font-display: {ff('display')};", f"$font-texto: {ff('texto')};", f"$font-mono: {ff('mono')};", '']
    L.append('$paleta: (')
    for g, scale in C.items():
        L.append(f'  "{g}": (' + ', '.join(f'"{k}": {hx.upper()}' for k, hx in scale.items()) + '),')
    L.append(');\n')
    L.append('$escala-tipo: (')
    for k, s in TS.items():
        L.append(f'  "{k}": (size: {s["size"]}px, line: {s["line"]}, tracking: {s["tracking"] if s["tracking"] != "0" else "0em"}, '
                 f'font: "{s["font"]}", weight: {s["weight"]}),')
    L.append(');\n')
    L.append('$espacio: (' + ', '.join(f'{i + 1}: {s}px' for i, s in enumerate(T['space-px'])) + ');')
    L.append('$radio: (' + ', '.join(f'"{k}": {v if isinstance(v, str) else str(v) + "px"}' for k, v in T['radius-px'].items()) + ');')
    L.append(f'$ease-marca: {T["motion"]["ease-marca"]};\n$ease-salto: {T["motion"]["ease-salto"]};\n')
    for mode in ('oscuro', 'claro'):
        L.append(f'$tema-{mode}: (')
        for k, v in list(SEM[mode].items()) + list(EXTRA[mode].items()):
            L.append(f'  "{k}": {sem_value(v)},')
        L.append(');\n')
    L.append('''@function color($grupo, $tono) { @return map.get(map.get($paleta, $grupo), $tono); }

/// Vuelca las variables semánticas del tema como custom properties.
@mixin tema($modo: oscuro) {
  @if $modo == claro {
    @each $k, $v in $tema-claro { --color-#{$k}: #{$v}; }
    color-scheme: light;
  } @else {
    @each $k, $v in $tema-oscuro { --color-#{$k}: #{$v}; }
    color-scheme: dark;
  }
}

/// Aplica un paso de la escala tipográfica.
@mixin tipo($paso) {
  $t: map.get($escala-tipo, $paso);
  $f: map.get($t, font);
  @if $f == "display" { font-family: $font-display; } @else if $f == "mono" { font-family: $font-mono; } @else { font-family: $font-texto; }
  font-size: map.get($t, size); line-height: map.get($t, line);
  letter-spacing: map.get($t, tracking); font-weight: map.get($t, weight);
}
''')
    open(os.path.join(OUT, 'tokens.scss'), 'w', encoding='utf8').write('\n'.join(L))


# ------------------------------------------------------------------ Tailwind
def write_tailwind():
    colors = {g: {k: hx.upper() for k, hx in scale.items()} for g, scale in C.items()}
    sem = {k: f'var(--color-{k})' for k in list(SEM['oscuro'].keys()) + list(EXTRA['oscuro'].keys()) if not k.startswith('cta-fondo')}
    fsize = {k: [f"{s['size'] / 16:g}rem", {'lineHeight': str(s['line']), 'letterSpacing': s['tracking'] if s['tracking'] != '0' else '0em',
                                           'fontWeight': str(s['weight'])}] for k, s in TS.items()}
    # Nombres de Tailwind (s/m/l chocarían con rounded-l = «lado izquierdo»)
    TWR = {'xs': 'xs', 's': 'sm', 'm': 'md', 'l': 'lg', 'xl': 'xl', 'pill': 'full', 'app-icon': 'app'}
    radius = {TWR.get(k, k): (v if isinstance(v, str) else f'{v}px') for k, v in T['radius-px'].items()}
    js = f"""// {HEAD}
//
// ── Tailwind v3 ─────────────────────────────────────────────────────────────
//   // tailwind.config.js
//   module.exports = {{ presets: [require('./tailwind.preset.js')], content: ['./src/**/*.html'] }}
//   Clases: bg-grafito-950 text-azul-600 font-display text-h1 rounded-lg bg-grad-ia-oscuro
//   Radios: xs 6 · sm 10 · md 14 · lg 20 · xl 28 · full · app (22,5 %). Eyebrow: text-eyebrow font-texto (Manrope 600, tipo frase, sin tracking)
//           y semánticas (dependen de tokens.css): bg-fondo text-texto border-borde text-enlace
//
// ── Tailwind v4 (oryzz.com/tap usa v4) ──────────────────────────────────────
//   v4 no usa presets JS: importa `tailwind-v4.css` (mismo directorio), que declara los
//   tokens con `@theme`. En globals.css:
//       @import "tailwindcss";
//       @import "./tailwind-v4.css";
//   y elimina los `--color-*` y `--font-*` antiguos (#0075FF, #C5F500, Syne, Outfit…).
/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  theme: {{
    extend: {{
      colors: {{
{chr(10).join(f'        {g}: ' + json.dumps(v) + ',' for g, v in colors.items())}
        // semánticos (cambian con data-tema="oscuro|claro")
{chr(10).join(f"        '{k}': '{v}'," for k, v in sem.items())}
      }},
      fontFamily: {{
        display: {json.dumps([FAMILY['display']['family'], 'Arial', 'Helvetica', 'sans-serif'])},
        texto: {json.dumps([FAMILY['texto']['family'], 'Arial', 'Helvetica', 'sans-serif'])},
        sans: {json.dumps([FAMILY['texto']['family'], 'Arial', 'Helvetica', 'sans-serif'])},
        mono: {json.dumps([FAMILY['mono']['family'], 'Consolas', 'Courier New', 'monospace'])},
      }},
      fontSize: {json.dumps(fsize, ensure_ascii=False)},
      borderRadius: {json.dumps(radius)},
      backgroundImage: {{
        'grad-ia-oscuro': '{T['gradient']['ia-oscuro']}',
        'grad-ia-claro': '{T['gradient']['ia-claro']}',
        'cta': 'var(--color-cta-fondo)',
      }},
      maxWidth: {{ contenido: '1200px' }},
      transitionTimingFunction: {{ marca: '{T['motion']['ease-marca']}', salto: '{T['motion']['ease-salto']}' }},
      transitionDuration: {{ rapido: '160ms', base: '280ms', lento: '560ms' }},
      strokeWidth: {{ icono: '1.75', grafico: '2' }},
    }},
  }},
}};
"""
    open(os.path.join(OUT, 'tailwind.preset.js'), 'w', encoding='utf8').write(js)

    th = [f'/* {HEAD}', ' * Tailwind v4: @import "tailwindcss"; @import "./tailwind-v4.css";', ' * Genera bg-grafito-950, text-azul-600, font-display, text-h1, rounded-lg, bg-fondo… (eyebrow: text-eyebrow font-texto, Manrope 600 en tipo frase) */', '@theme {',
          '  --color-*: initial;  /* borra la paleta por defecto de Tailwind: solo colores de marca */',
          '  --color-white: #FFFFFF;', '  --color-transparent: transparent;', '  --color-current: currentColor;']
    for g, scale in C.items():
        for k, hx in scale.items():
            th.append(f'  --color-{g}-{k}: {hx.upper()};')
    th += [f"  --font-display: {ff('display')};", f"  --font-sans: {ff('texto')};", f"  --font-texto: {ff('texto')};", f"  --font-mono: {ff('mono')};"]
    for k, s in TS.items():
        th.append(f"  --text-{k}: {s['size'] / 16:g}rem; --text-{k}--line-height: {s['line']}; --text-{k}--letter-spacing: {s['tracking'] if s['tracking'] != '0' else '0em'}; --text-{k}--font-weight: {s['weight']};")
    for k, v in radius.items():
        th.append(f'  --radius-{k}: {v};')
    th += [f"  --ease-marca: {T['motion']['ease-marca']};", f"  --ease-salto: {T['motion']['ease-salto']};", '}', '',
           '/* Semánticos: los valores viven en tokens.css (cambian con data-tema="oscuro|claro").',
           ' * No se redeclaran en @theme para no crear referencias circulares; en v4 usa la sintaxis',
           ' * de variable directa: bg-(--color-fondo) text-(--color-texto-2) border-(--color-borde),',
           ' * o las utilidades de atajo de abajo. */']
    for util, prop, var in [('bg-fondo', 'background-color', 'fondo'), ('bg-superficie', 'background-color', 'superficie'),
                            ('bg-superficie-2', 'background-color', 'superficie-2'), ('text-texto', 'color', 'texto'),
                            ('text-texto-2', 'color', 'texto-2'), ('text-texto-3', 'color', 'texto-3'),
                            ('text-enlace', 'color', 'enlace'), ('text-dato', 'color', 'dato'), ('border-borde', 'border-color', 'borde')]:
        th.append(f'@utility {util} {{ {prop}: var(--color-{var}); }}')
    th.append('@utility bg-cta { background: var(--color-cta-fondo); color: var(--color-cta-texto); }')
    open(os.path.join(OUT, 'tailwind-v4.css'), 'w', encoding='utf8').write('\n'.join(th) + '\n')


# ------------------------------------------------------------------ W3C Design Tokens (DTCG)
def _grad_dtcg(v):
    stops = re.findall(r'(#[0-9A-Fa-f]{6})\s+(\d+)%', v)
    return [{'color': c.upper(), 'position': int(p) / 100} for c, p in stops]


def _alias(v):
    if v.startswith('gradient.'):
        return '{gradient.' + v.split('.', 1)[1] + '}'
    for g, scale in C.items():
        for k, hx in scale.items():
            if hx.upper() == v.upper():
                return '{color.' + g + '.' + k + '}'
    return v


def write_dtcg():
    d = {'$description': HEAD}
    d['color'] = {g: {k: {'$type': 'color', '$value': hx.upper()} for k, hx in scale.items()} for g, scale in C.items()}
    d['gradient'] = {k: {'$type': 'gradient', '$value': _grad_dtcg(v), '$extensions': {'com.oryzz.angle': '135deg', 'com.oryzz.css': v}}
                     for k, v in T['gradient'].items()}
    d['semantic'] = {}
    for mode in ('oscuro', 'claro'):
        d['semantic'][mode] = {}
        for k, v in list(SEM[mode].items()) + list(EXTRA[mode].items()):
            val = _alias(v)
            typ = 'gradient' if val.startswith('{gradient') else 'color'
            if v.startswith('linear-gradient') or v == 'transparent':
                d['semantic'][mode][k] = {'$type': 'color' if v == 'transparent' else 'gradient',
                                          '$value': '#00000000' if v == 'transparent' else _grad_dtcg(v)}
            else:
                d['semantic'][mode][k] = {'$type': typ, '$value': val}
    d['font'] = {'family': {k: {'$type': 'fontFamily', '$value': [f['family']] + [x.strip().strip("'") for x in f['fallback'].split(',')]}
                            for k, f in FAMILY.items()}}
    d['typography'] = {k: {'$type': 'typography', '$value': {
        'fontFamily': '{font.family.' + s['font'] + '}', 'fontSize': {'value': s['size'], 'unit': 'px'},
        'fontWeight': s['weight'], 'lineHeight': s['line'],
        'letterSpacing': {'value': float(s['tracking'].replace('em', '') or 0) if s['tracking'] != '0' else 0, 'unit': 'em'}}}
        for k, s in TS.items()}
    d['space'] = {str(i + 1): {'$type': 'dimension', '$value': {'value': s, 'unit': 'px'}} for i, s in enumerate(T['space-px'])}
    d['radius'] = {k: {'$type': 'dimension', '$value': {'value': v, 'unit': 'px'}} for k, v in T['radius-px'].items() if not isinstance(v, str)}
    d['stroke'] = {k: {'$type': 'dimension', '$value': {'value': v, 'unit': 'px'}} for k, v in T['stroke-px'].items()}
    d['motion'] = {
        'ease-marca': {'$type': 'cubicBezier', '$value': [0.2, 0.8, 0.2, 1]},
        'ease-salto': {'$type': 'cubicBezier', '$value': [0.34, 1.4, 0.5, 1]},
        'rapido': {'$type': 'duration', '$value': {'value': 160, 'unit': 'ms'}},
        'base': {'$type': 'duration', '$value': {'value': 280, 'unit': 'ms'}},
        'lento': {'$type': 'duration', '$value': {'value': 560, 'unit': 'ms'}},
    }
    json.dump(d, open(os.path.join(OUT, 'tokens.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=2)


# ------------------------------------------------------------------ Tokens Studio (Figma)
WNAME = {300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}


def write_figma():
    g = {'color': {gg: {k: {'value': hx.upper(), 'type': 'color'} for k, hx in scale.items()} for gg, scale in C.items()}}
    g['gradient'] = {k: {'value': v, 'type': 'color', 'description': 'Gradiente IA 135°'} for k, v in T['gradient'].items()}
    g['fontFamilies'] = {k: {'value': f['family'], 'type': 'fontFamilies'} for k, f in FAMILY.items()}
    g['typography'] = {}
    for k, s in TS.items():
        tr = s['tracking']
        ls = f"{float(tr.replace('em', '')) * 100:g}%" if tr != '0' else '0%'
        g['typography'][k] = {'type': 'typography', 'value': {
            'fontFamily': '{fontFamilies.' + s['font'] + '}', 'fontWeight': WNAME[s['weight']],
            'fontSize': str(s['size']), 'lineHeight': f"{round(s['line'] * 100)}%", 'letterSpacing': ls,
            'textCase': 'uppercase' if s.get('case') == 'upper' else 'none'}}
    g['spacing'] = {str(i + 1): {'value': str(s), 'type': 'spacing'} for i, s in enumerate(T['space-px'])}
    g['borderRadius'] = {k: {'value': str(v).replace('%', '') + ('%' if isinstance(v, str) else ''), 'type': 'borderRadius'} for k, v in T['radius-px'].items()}
    g['borderWidth'] = {k: {'value': str(v), 'type': 'borderWidth'} for k, v in T['stroke-px'].items()}

    def sem(mode):
        out = {}
        for k, v in list(SEM[mode].items()) + list(EXTRA[mode].items()):
            if v.startswith('gradient.'):
                out[k] = {'value': '{gradient.' + v.split('.', 1)[1] + '}', 'type': 'color'}
            else:
                a = _alias(v)
                out[k] = {'value': a if a.startswith('{') else v, 'type': 'color'}
        return {'semantic': out}
    doc = {'global': g, 'oscuro': sem('oscuro'), 'claro': sem('claro'),
           '$themes': [
               {'id': 'oryzz-oscuro', 'name': 'Oryzz · Oscuro', 'selectedTokenSets': {'global': 'source', 'oscuro': 'enabled'}},
               {'id': 'oryzz-claro', 'name': 'Oryzz · Claro (Tap)', 'selectedTokenSets': {'global': 'source', 'claro': 'enabled'}}],
           '$metadata': {'tokenSetOrder': ['global', 'oscuro', 'claro']}}
    json.dump(doc, open(os.path.join(OUT, 'figma-tokens.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=2)


def write_fonts_css():
    css = f"""/* Oryzz · fuentes de marca en WOFF2 (licencia SIL OFL 1.1, ver /Licencias).
 * Copia esta carpeta a la raíz pública del sitio como /fonts/ y enlaza: <link rel="stylesheet" href="/fonts/fonts.css">
 * Precarga solo lo que se ve arriba del todo:
 *   <link rel="preload" href="/fonts/SpaceGrotesk-Bold.woff2" as="font" type="font/woff2" crossorigin>
 *   <link rel="preload" href="/fonts/Manrope-Regular.woff2" as="font" type="font/woff2" crossorigin>
 * Alternativa: las variables *-VF.woff2 (un archivo por familia) — ver bloque comentado al final. */
{font_faces()}

/* --- Variante con fuentes variables (sustituye todo lo anterior si la usas) ---
@font-face{{font-family:'Space Grotesk';font-weight:300 700;font-display:swap;src:url('/fonts/SpaceGrotesk-VF.woff2') format('woff2')}}
@font-face{{font-family:'Manrope';font-weight:200 800;font-display:swap;src:url('/fonts/Manrope-VF.woff2') format('woff2')}}
@font-face{{font-family:'JetBrains Mono';font-weight:100 800;font-display:swap;src:url('/fonts/JetBrainsMono-VF.woff2') format('woff2')}}
*/
"""
    open(os.path.join(FONTS_OUT, 'fonts.css'), 'w', encoding='utf8').write(css)


if __name__ == '__main__':
    write_css(); write_scss(); write_tailwind(); write_dtcg(); write_figma(); write_fonts_css()
    print('ok', sorted(os.listdir(OUT)))
