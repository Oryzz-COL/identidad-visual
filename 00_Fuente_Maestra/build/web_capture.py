"""
Captura y análisis de páginas web con Chrome headless vía DevTools Protocol.
Sin dependencias salvo `websocket-client` (pip install websocket-client).

    from web_capture import Browser
    with Browser(width=1440, height=900) as b:
        b.goto('https://oryzz.com/')
        b.hide_text('Usamos cookies')          # oculta el banner de cookies
        b.shot('hero.png')                     # captura del viewport
        b.shot_element('#servicios', 'servicios.png')
        b.full_page('full.png')                # página completa sin romper los 100vh
        data = b.eval('document.title')

Uso en auditorías: `b.eval(JS)` permite leer estilos computados (colores, fuentes)
para calcular contrastes reales de la página publicada.
"""
import base64, json, os, socket, subprocess, tempfile, time, urllib.request
import websocket

from render import CHROME


def _free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


class Browser:
    def __init__(self, width=1440, height=900, mobile=False, scale=1):
        self.w, self.h, self.mobile, self.scale = width, height, mobile, scale
        self.port = _free_port()
        self.profile = tempfile.mkdtemp(prefix='oryzz_cdp_')
        self._id = 0

    # ------------------------------------------------------------------ ciclo de vida
    def __enter__(self):
        self.proc = subprocess.Popen([
            CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
            '--no-default-browser-check', f'--remote-debugging-port={self.port}',
            f'--user-data-dir={self.profile}', f'--window-size={self.w},{self.h}', 'about:blank'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{self.port}/json'))
                page = next(t for t in tabs if t.get('type') == 'page')
                break
            except Exception:
                time.sleep(0.15)
        self.ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=90, suppress_origin=True)
        self.cmd('Page.enable'); self.cmd('Runtime.enable')
        self.cmd('Emulation.setDeviceMetricsOverride', width=self.w, height=self.h,
                 deviceScaleFactor=self.scale, mobile=self.mobile)
        if self.mobile:
            self.cmd('Emulation.setTouchEmulationEnabled', enabled=True)
        return self

    def __exit__(self, *a):
        try: self.ws.close()
        except Exception: pass
        self.proc.kill()

    def cmd(self, method, **params):
        self._id += 1; mid = self._id
        self.ws.send(json.dumps({'id': mid, 'method': method, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('id') == mid:
                if 'error' in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get('result', {})

    # ------------------------------------------------------------------ navegación
    def goto(self, url, wait=3.5):
        self.cmd('Page.navigate', url=url)
        t0 = time.time()
        while time.time() - t0 < 30:
            if self.eval('document.readyState') == 'complete':
                break
            time.sleep(0.2)
        time.sleep(wait)

    def eval(self, js):
        r = self.cmd('Runtime.evaluate', expression=js, returnByValue=True, awaitPromise=True)
        if 'exceptionDetails' in r:
            raise RuntimeError('JS: ' + json.dumps(r['exceptionDetails'])[:600])
        return r.get('result', {}).get('value')

    def hide_text(self, text):
        """Oculta el contenedor fijo más externo que contenga `text` (p. ej. banners de cookies)."""
        js = """(function(t){var n=[...document.querySelectorAll('body *')].filter(e=>e.children.length<40&&e.innerText&&e.innerText.includes(t));
        var hit=0;n.forEach(e=>{var p=e;while(p&&p!==document.body){var cs=getComputedStyle(p);if(cs.position==='fixed'||cs.position==='sticky'&&false){p.style.setProperty('display','none','important');hit++;break}p=p.parentElement}});return hit})(%s)""" % json.dumps(text)
        return self.eval(js)

    def unstick(self):
        """Convierte cabeceras sticky/fixed en estáticas para que no tapen los recortes."""
        return self.eval("""[...document.querySelectorAll('body *')].filter(e=>{var p=getComputedStyle(e).position;return p==='sticky'||p==='fixed'}).map(e=>{var p=getComputedStyle(e).position;e.style.setProperty('position',p==='sticky'?'relative':'absolute','important');return e.tagName}).length""")

    def scroll_to(self, y):
        self.eval(f'window.scrollTo(0,{int(y)})'); time.sleep(0.9)

    def reveal_all(self):
        """Fuerza el estado final de las animaciones de aparición al hacer scroll."""
        h = self.eval('document.documentElement.scrollHeight') or self.h
        for y in range(0, int(h), int(self.h * 0.6)):
            self.eval(f'window.scrollTo(0,{y})'); time.sleep(0.25)
        self.eval('window.scrollTo(0,0)'); time.sleep(0.6)

    # ------------------------------------------------------------------ capturas
    def _save(self, data, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(base64.b64decode(data))

    def shot(self, path):
        self._save(self.cmd('Page.captureScreenshot', format='png')['data'], path)

    def shot_clip(self, path, x, y, w, h):
        """Recorte en coordenadas de documento (px CSS)."""
        r = self.cmd('Page.captureScreenshot', format='png', captureBeyondViewport=True,
                     clip=dict(x=x, y=y, width=w, height=h, scale=1))
        self._save(r['data'], path)

    def rect(self, selector):
        return self.eval("""(function(s){var e=document.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();
        return {x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height}})(%s)""" % json.dumps(selector))

    def shot_element(self, selector, path, pad=0):
        r = self.rect(selector)
        if not r:
            raise RuntimeError(f'No existe {selector}')
        self.scroll_to(max(0, r['y'] - 80))
        self.shot_clip(path, max(0, r['x'] - pad), max(0, r['y'] - pad), r['w'] + 2 * pad, r['h'] + 2 * pad)

    def full_page(self, path, max_h=16000):
        """Captura la página entera por tramos del viewport y los une (respeta 100vh)."""
        from PIL import Image
        self.reveal_all()
        total = min(int(self.eval('document.documentElement.scrollHeight')), max_h)
        tiles, y = [], 0
        tmp = tempfile.mkdtemp()
        while y < total:
            self.scroll_to(y)
            actual = self.eval('window.scrollY')
            p = os.path.join(tmp, f'{y}.png'); self.shot(p)
            tiles.append((actual, p)); y += self.h
        W = int(self.w * self.scale)
        out = Image.new('RGB', (W, int(total * self.scale)), 'white')
        for actual, p in tiles:
            out.paste(Image.open(p).convert('RGB'), (0, int(actual * self.scale)))
        out.save(path)
