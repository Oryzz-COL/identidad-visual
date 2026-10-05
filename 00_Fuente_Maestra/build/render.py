"""
Utilidades de render con Chrome headless (sin dependencias externas).

    from render import svg_to_png, html_to_pdf, html_to_png
    svg_to_png('logo.svg', 'logo.png', width=2000)          # PNG transparente
    html_to_pdf('guia.html', 'guia.pdf')                    # respeta @page del CSS
    html_to_png('post.html', 'post.png', 1080, 1350)

CLI:  python render.py png  in.svg out.png 2000
      python render.py pdf  in.html out.pdf
      python render.py shot in.html out.png 1080 1350
"""
import os, re, subprocess, sys, tempfile, pathlib

CHROME_CANDIDATES = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
]
CHROME = next((c for c in CHROME_CANDIDATES if os.path.exists(c)), None)

def _url(p):
    return pathlib.Path(os.path.abspath(p)).as_uri()

def _run(args):
    if not CHROME:
        raise RuntimeError('No se encontró Chrome/Edge')
    base = [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
            '--no-first-run', '--no-default-browser-check', '--allow-file-access-from-files',
            '--run-all-compositor-stages-before-draw', '--virtual-time-budget=4000']
    subprocess.run(base + args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)

def _svg_size(svg_path):
    s = open(svg_path, encoding='utf8').read()
    m = re.search(r'viewBox="([-\d.\s]+)"', s)
    x, y, w, h = [float(v) for v in m.group(1).split()]
    return w, h

def svg_to_png(svg_path, png_path, width=None, height=None, background=None):
    """Rasteriza un SVG con fondo transparente (o `background` CSS)."""
    w, h = _svg_size(svg_path)
    if width and not height:
        height = round(width * h / w)
    elif height and not width:
        width = round(height * w / h)
    elif not width:
        width, height = round(w), round(h)
    bg = background or 'transparent'
    html = (f'<!doctype html><html><head><style>html,body{{margin:0;padding:0;background:{bg};overflow:hidden}}'
            f'img{{display:block;width:{width}px;height:{height}px}}</style></head>'
            f'<body><img src="{_url(svg_path)}"></body></html>')
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf8') as t:
        t.write(html); tmp = t.name
    try:
        os.makedirs(os.path.dirname(os.path.abspath(png_path)), exist_ok=True)
        _run([f'--window-size={width},{height}', '--default-background-color=00000000',
              f'--screenshot={os.path.abspath(png_path)}', _url(tmp)])
    finally:
        os.unlink(tmp)

def html_to_png(html_path, png_path, width, height, transparent=False):
    os.makedirs(os.path.dirname(os.path.abspath(png_path)), exist_ok=True)
    args = [f'--window-size={width},{height}', f'--screenshot={os.path.abspath(png_path)}']
    if transparent:
        args.insert(0, '--default-background-color=00000000')
    _run(args + [_url(html_path)])

def html_to_pdf(html_path, pdf_path):
    """Usa el tamaño de @page definido en el CSS del HTML."""
    os.makedirs(os.path.dirname(os.path.abspath(pdf_path)), exist_ok=True)
    _run(['--no-pdf-header-footer', '--print-to-pdf-no-header', '--generate-pdf-document-outline',
          f'--print-to-pdf={os.path.abspath(pdf_path)}', _url(html_path)])

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'png':
        svg_to_png(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else None)
    elif cmd == 'pdf':
        html_to_pdf(sys.argv[2], sys.argv[3])
    elif cmd == 'shot':
        html_to_png(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
    print('ok')
