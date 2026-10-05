"""
Render rápido con UNA sesión de Chrome headless controlada por CDP (DevTools Protocol).
Mismo resultado que render.py, pero ~20x más rápido para lotes (cientos de PNG o fotogramas).

    from render_fast import Chrome
    with Chrome() as c:
        c.svg_to_png('logo.svg', 'logo.png', width=1600)          # transparente
        c.html_to_png('pieza.html', 'pieza.png', 1080, 1080)
        c.svg_string_to_png('<svg ...>', 'frame.png', 800, 300, background='#0B0D12')

Requiere: websocket-client (pip install websocket-client). Usa el mismo Chrome que render.py.
"""
import base64, json, os, pathlib, re, shutil, socket, subprocess, tempfile, time, urllib.request

from render import CHROME, _svg_size

import websocket


def _free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


class Chrome:
    def __init__(self):
        self.port = _free_port()
        self.profile = tempfile.mkdtemp(prefix='oryzz_cdp_')
        self.tmpdir = tempfile.mkdtemp(prefix='oryzz_cdp_html_')
        self.proc = subprocess.Popen(
            [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
             '--no-default-browser-check', '--allow-file-access-from-files', '--force-color-profile=srgb',
             f'--remote-debugging-port={self.port}', f'--user-data-dir={self.profile}', 'about:blank'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ws_url = None
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{self.port}/json', timeout=1))
                page = next(t for t in tabs if t.get('type') == 'page')
                ws_url = page['webSocketDebuggerUrl']; break
            except Exception:
                time.sleep(0.1)
        if not ws_url:
            raise RuntimeError('No se pudo conectar con Chrome (CDP)')
        self.ws = websocket.create_connection(ws_url, timeout=60, suppress_origin=True)
        self._id = 0
        self.cmd('Page.enable')
        self.cmd('Runtime.enable')

    # -------------------------------------------------------------- CDP
    def cmd(self, method, **params):
        self._id += 1; mid = self._id
        self.ws.send(json.dumps({'id': mid, 'method': method, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('id') == mid:
                if 'error' in msg:
                    raise RuntimeError(f'{method}: {msg["error"]}')
                return msg.get('result', {})

    def _wait_event(self, name, timeout=30):
        end = time.time() + timeout
        while time.time() < end:
            msg = json.loads(self.ws.recv())
            if msg.get('method') == name:
                return msg
        raise TimeoutError(name)

    def load(self, url, width, height):
        self.cmd('Emulation.setDeviceMetricsOverride', width=int(width), height=int(height),
                 deviceScaleFactor=1, mobile=False)
        self.cmd('Emulation.setDefaultBackgroundColorOverride', color={'r': 0, 'g': 0, 'b': 0, 'a': 0})
        self._id += 1; mid = self._id
        self.ws.send(json.dumps({'id': mid, 'method': 'Page.navigate', 'params': {'url': url}}))
        self._wait_event('Page.loadEventFired')
        # fuentes e imágenes listas
        self.cmd('Runtime.evaluate', expression='document.fonts.ready.then(()=>true)', awaitPromise=True)
        self.cmd('Runtime.evaluate', expression='new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>r(true))))', awaitPromise=True)

    def shot(self, png_path, width, height):
        r = self.cmd('Page.captureScreenshot', format='png', captureBeyondViewport=False,
                     clip={'x': 0, 'y': 0, 'width': int(width), 'height': int(height), 'scale': 1})
        os.makedirs(os.path.dirname(os.path.abspath(png_path)), exist_ok=True)
        with open(png_path, 'wb') as f:
            f.write(base64.b64decode(r['data']))

    # -------------------------------------------------------------- alto nivel
    def html_to_png(self, html_path, png_path, width, height):
        self.load(pathlib.Path(os.path.abspath(html_path)).as_uri(), width, height)
        self.shot(png_path, width, height)

    def html_string_to_png(self, html, png_path, width, height, base_dir=None):
        d = base_dir or self.tmpdir
        tmp = os.path.join(d, f'__cdp_{os.getpid()}_{self._id}.html')
        with open(tmp, 'w', encoding='utf8') as f:
            f.write(html)
        try:
            self.html_to_png(tmp, png_path, width, height)
        finally:
            os.unlink(tmp)

    def svg_to_png(self, svg_path, png_path, width=None, height=None, background=None):
        w, h = _svg_size(svg_path)
        if width and not height:
            height = round(width * h / w)
        elif height and not width:
            width = round(height * w / h)
        elif not width:
            width, height = round(w), round(h)
        bg = background or 'transparent'
        src = pathlib.Path(os.path.abspath(svg_path)).as_uri()
        html = (f'<!doctype html><html><head><style>html,body{{margin:0;padding:0;background:{bg};overflow:hidden}}'
                f'img{{display:block;width:{width}px;height:{height}px}}</style></head>'
                f'<body><img src="{src}"></body></html>')
        self.html_string_to_png(html, png_path, width, height)
        return width, height

    def svg_string_to_png(self, svg, png_path, width, height, background=None):
        bg = background or 'transparent'
        svg = re.sub(r'<svg ', f'<svg width="{width}" height="{height}" ', svg, count=1)
        html = (f'<!doctype html><html><head><style>html,body{{margin:0;padding:0;background:{bg};overflow:hidden}}'
                f'svg{{display:block}}</style></head><body>{svg}</body></html>')
        self.html_string_to_png(html, png_path, width, height)

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass
        try:
            self.proc.terminate(); self.proc.wait(10)
        except Exception:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()
