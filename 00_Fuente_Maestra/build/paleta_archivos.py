"""
Genera los archivos de paleta de 03_Color a partir de tokens.json:
Oryzz_Paleta.ase (Adobe), Oryzz_Paleta.gpl (GIMP/Inkscape/Krita), paleta.json y paleta.csv.

Uso:  python paleta_archivos.py [carpeta_salida]
"""
import csv, json, os, struct, sys
from oryzz_color import PALETA, GRUPOS, NOTA_CMYK, NOTA_PANTONE, TOKENS

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..', '03_Color')
os.makedirs(OUT, exist_ok=True)


# ------------------------------------------------------------------ ASE (Adobe Swatch Exchange 1.0)
def _ase_name(s):
    u = (s + '\0').encode('utf-16-be')
    return struct.pack('>H', len(u) // 2) + u


def _block(btype, data=b''):
    return struct.pack('>HI', btype, len(data)) + data


def write_ase(path):
    blocks = []
    for g in GRUPOS:
        blocks.append(_block(0xC001, _ase_name(f'Oryzz · {g}')))
        for p in [p for p in PALETA if p['grupo'] == g]:
            r, gg, b = [v / 255 for v in p['rgb']]
            data = _ase_name(f"{p['nombre']} {p['hex']}") + b'RGB ' + struct.pack('>fff', r, gg, b) + struct.pack('>H', 0)  # 0 = global
            blocks.append(_block(0x0001, data))
        blocks.append(_block(0xC002))
    with open(path, 'wb') as f:
        f.write(b'ASEF' + struct.pack('>HH', 1, 0) + struct.pack('>I', len(blocks)) + b''.join(blocks))


def read_ase(path):
    """Lector mínimo para verificar el archivo generado."""
    d = open(path, 'rb').read()
    assert d[:4] == b'ASEF'
    n = struct.unpack('>I', d[8:12])[0]; i = 12; out = []
    for _ in range(n):
        t, ln = struct.unpack('>HI', d[i:i + 6]); body = d[i + 6:i + 6 + ln]; i += 6 + ln
        if t in (0xC001, 0x0001):
            nl = struct.unpack('>H', body[:2])[0]
            name = body[2:2 + nl * 2].decode('utf-16-be').rstrip('\0')
            if t == 0x0001:
                model = body[2 + nl * 2:6 + nl * 2]
                vals = struct.unpack('>fff', body[6 + nl * 2:18 + nl * 2])
                out.append(('color', name, model.decode(), [round(v * 255) for v in vals]))
            else:
                out.append(('grupo', name))
        else:
            out.append(('fin',))
    return out


# ------------------------------------------------------------------ GPL
def write_gpl(path):
    lines = ['GIMP Palette', 'Name: Oryzz v2.0', 'Columns: 8',
             '# Oryzz · paleta de marca v2.0 (2026). Fuente: 00_Fuente_Maestra/tokens.json']
    for g in GRUPOS:
        lines.append(f'# ---- {g}')
        for p in [p for p in PALETA if p['grupo'] == g]:
            r, gg, b = p['rgb']
            lines.append(f"{r:3d} {gg:3d} {b:3d}\t{p['nombre']} {p['hex']}")
    open(path, 'w', encoding='utf8', newline='\n').write('\n'.join(lines) + '\n')


# ------------------------------------------------------------------ JSON / CSV
def write_json(path):
    data = {
        'marca': 'Oryzz', 'version': TOKENS['meta']['version'], 'fecha': TOKENS['meta']['date'],
        'fuente': '00_Fuente_Maestra/tokens.json',
        'notas': {'cmyk': f'CMYK {NOTA_CMYK}. Conversión sin perfil ICC; para imprenta pedir prueba de color (FOGRA39 / estucado).',
                  'pantone': f'Pantone {NOTA_PANTONE}. Es la coincidencia visual más cercana en Pantone Solid Coated.',
                  'proporcion': '60 % Grafito · 25 % Blanco / Grafito 50 · 10 % Azul IA / Cyan · ≤ 5 % Lima'},
        'gradientes': TOKENS['gradient'],
        'grupos': {},
    }
    for g in GRUPOS:
        data['grupos'][g] = [{
            'nombre': p['nombre'], 'token': p['token'], 'hex': p['hex'],
            'rgb': dict(zip('rgb', p['rgb'])), 'hsl': dict(zip('hsl', p['hsl'])),
            'cmyk_aproximado': dict(zip('cmyk', p['cmyk'])),
            'pantone_sugerido': p['pantone'] or 'Sin tinta directa (usar papel o tramado del color base)',
            'uso': p['uso'],
            'contraste_con_blanco': p['contraste_blanco'], 'contraste_con_grafito_950': p['contraste_grafito'],
        } for p in PALETA if p['grupo'] == g]
    json.dump(data, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=2)


def write_csv(path):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['Grupo', 'Nombre', 'Token', 'HEX', 'R', 'G', 'B', 'H', 'S %', 'L %',
                    'C', 'M', 'Y', 'K', 'Nota CMYK', 'Pantone sugerido', 'Nota Pantone',
                    'Contraste con blanco', 'Contraste con Grafito 950', 'Uso'])
        for p in PALETA:
            w.writerow([p['grupo'], p['nombre'], p['token'], p['hex'], *p['rgb'], *p['hsl'], *p['cmyk'], NOTA_CMYK,
                        p['pantone'] or '—', NOTA_PANTONE if p['pantone'] else 'sin tinta directa',
                        str(p['contraste_blanco']).replace('.', ','), str(p['contraste_grafito']).replace('.', ','), p['uso']])


if __name__ == '__main__':
    write_ase(os.path.join(OUT, 'Oryzz_Paleta.ase'))
    write_gpl(os.path.join(OUT, 'Oryzz_Paleta.gpl'))
    write_json(os.path.join(OUT, 'paleta.json'))
    write_csv(os.path.join(OUT, 'paleta.csv'))
    chk = read_ase(os.path.join(OUT, 'Oryzz_Paleta.ase'))
    print('ASE ok:', sum(1 for c in chk if c[0] == 'color'), 'colores,', sum(1 for c in chk if c[0] == 'grupo'), 'grupos')
