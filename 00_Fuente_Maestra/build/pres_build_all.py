"""
Oryzz · construye todas las presentaciones de 06_Presentaciones.

    python pres_build_all.py            (requiere Chrome; PowerPoint opcional)

1. python-pptx genera los .pptx (master + layouts + slides) en 06_Presentaciones/_build
2. Si hay PowerPoint (Windows): los re-guarda con las fuentes incrustadas en 06_Presentaciones/
   y exporta cada slide a PNG nativo en _previews/<deck>/  (sin PowerPoint: copia el .pptx tal cual)
3. HTML de previsualización (mismo modelo) -> PDF 1920x1080 por página con Chrome
"""
import os, sys, shutil, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pres_oryzz as O
import pres_tap as TAP
from render import html_to_pdf

OUT = O.OUT
TMP = os.path.join(OUT, '_build')
PREV = os.path.join(OUT, '_previews')
PS1 = os.path.join(HERE, 'pres_powerpoint.ps1')


def powerpoint(src, dst, png_dir):
    try:
        if os.path.isdir(png_dir):
            shutil.rmtree(png_dir)
        r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', PS1, '-In', src, '-Out', dst,
                            '-PngDir', png_dir, '-PngWidth', '1280'], capture_output=True, text=True, timeout=900)
        ok = r.returncode == 0 and os.path.exists(dst)
        if not ok:
            print('  PowerPoint no disponible o error:', (r.stderr or r.stdout)[-300:])
        return ok
    except Exception as e:
        print('  PowerPoint no disponible:', e)
        return False


def main():
    os.makedirs(TMP, exist_ok=True)
    jobs = [
        ('Oryzz_Plantilla_Presentacion_Oscura', lambda p, h: O.build(True, 'template', p, h), 'Oryzz_Plantilla_Presentacion_Previsualizacion'),
        ('Oryzz_Plantilla_Presentacion_Clara', lambda p, h: O.build(False, 'template', p, h), 'Oryzz_Plantilla_Presentacion_Clara_Previsualizacion'),
        ('Oryzz_Deck_Comercial_Ejemplo', lambda p, h: O.build(True, 'deck', p, h), 'Oryzz_Deck_Comercial_Ejemplo_Previsualizacion'),
        ('OryzzTap_Plantilla_Presentacion', lambda p, h: TAP.build(p, h), 'OryzzTap_Plantilla_Presentacion_Previsualizacion'),
    ]
    for name, fn, prev in jobs:
        raw = os.path.join(TMP, name + '.pptx')
        # la previsualización principal se queda como HTML en la carpeta (la usa la guía de marca)
        keep_html = prev == 'Oryzz_Plantilla_Presentacion_Previsualizacion'
        html = os.path.join(OUT if keep_html else TMP, prev + '.html')
        fn(raw, html)
        final = os.path.join(OUT, name + '.pptx')
        if not powerpoint(raw, final, os.path.join(PREV, name)):
            shutil.copyfile(raw, final)
        html_to_pdf(html, os.path.join(OUT, prev + '.pdf'))
        print('  ->', final)
    # limpieza de intermedios
    shutil.rmtree(TMP, ignore_errors=True)
    for f in glob.glob(os.path.join(OUT, '*_Clara_Previsualizacion.html')):
        os.remove(f)


if __name__ == '__main__':
    main()
