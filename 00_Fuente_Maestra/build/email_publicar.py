# -*- coding: utf-8 -*-
"""
Oryzz · publicar plantillas de email con URL absolutas
======================================================

Las plantillas de 08_Email/ usan rutas relativas («assets/…») para poder abrirlas
y editarlas en local. Los clientes de correo necesitan URL públicas. Este script
copia cada plantilla a 08_Email/_listo_para_enviar/ sustituyendo «assets/» por
BASE_URL. Respeta tus ediciones manuales: trabaja sobre los HTML tal como estén.

    python email_publicar.py                                   # usa la BASE_URL por defecto
    python email_publicar.py https://cdn.midominio.com/email   # otra URL

Recuerda subir antes el contenido de 08_Email/assets/ a esa URL.
"""
import pathlib, sys

BASE_URL = 'https://oryzz.com/brand/email'


def publicar(out_dir, base_url=BASE_URL):
    out_dir = pathlib.Path(out_dir)
    dest = out_dir / '_listo_para_enviar'
    dest.mkdir(exist_ok=True)
    base = base_url.rstrip('/') + '/'
    n = 0
    for p in sorted(out_dir.glob('[0-9][0-9]_*.html')):
        s = p.read_text(encoding='utf8')
        s = s.replace('src="assets/', 'src="' + base).replace("url('assets/", "url('" + base)
        s = s.replace('Imágenes:    rutas relativas «assets/…».', 'Imágenes:    URL absolutas (copia publicada).')
        (dest / p.name).write_text(s, encoding='utf8')
        n += 1
    print('publicadas %d plantillas en %s (BASE_URL = %s)' % (n, dest, base))


if __name__ == '__main__':
    here = pathlib.Path(__file__).resolve().parents[2] / '08_Email'
    publicar(here, sys.argv[1] if len(sys.argv) > 1 else BASE_URL)
