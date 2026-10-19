# -*- coding: utf-8 -*-
"""Oryzz · catálogo PDF de plantillas de email (reportlab). Lo llama email_build.py."""
import pathlib
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

G950, G850, G700, G600, G500, G400, G200, G100, G50 = ('#0B0D12', '#12151D', '#232836', '#3A4152', '#5A6172',
                                                       '#8A90A0', '#D5D9E0', '#E5E8EE', '#F6F7F9')
AZUL, LIMA, LIMA6 = '#3B72FF', '#BFF24A', '#7FB02E'
PT = 0.75            # 1 px CSS = 0,75 pt


def _fonts(root):
    f = root / '00_Fuente_Maestra' / 'fonts' / 'static'
    for n, fn in [('SG', 'SpaceGrotesk-Bold'), ('SGM', 'SpaceGrotesk-Medium'), ('MR', 'Manrope-Regular'),
                  ('MRS', 'Manrope-SemiBold'), ('JB', 'JetBrainsMono-Medium')]:
        pdfmetrics.registerFont(TTFont(n, str(f / (fn + '.ttf'))))


def _wrap(c, text, font, size, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if c.stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def _eb(c, x, y, text, col=G500, node=LIMA6, size=12):
    """Etiqueta en tipo frase (Manrope 600, sin mayúsculas ni tracking) con nodo delante (BRAND_SPEC §4)."""
    c.setFillColor(node); c.circle(x + 3, y + size * 0.33, 3, stroke=0, fill=1)
    c.setFillColor(col); c.setFont('MRS', size)
    c.drawString(x + 14, y, text)


def _rotulo(c, x, y, text, col=G500, size=11):
    """Rótulo de campo en tipo frase, Manrope 600."""
    c.setFont('MRS', size); c.setFillColor(col); c.drawString(x, y, text)


def _img(c, path, x, ytop, w):
    ir = ImageReader(str(path))
    iw, ih = ir.getSize()
    h = w * ih / iw
    c.drawImage(ir, x, ytop - h, w, h)
    c.setStrokeColor(G100); c.setLineWidth(0.6); c.rect(x, ytop - h, w, h, stroke=1, fill=0)
    return h


def construir(out, meta, root):
    out = pathlib.Path(out); root = pathlib.Path(root)
    _fonts(root)
    pv = out / '_previews'
    pdf = out / 'Oryzz_Email_Catalogo.pdf'
    nombres = sorted(p.stem for p in out.glob('[0-9][0-9]_*.html'))
    c = canvas.Canvas(str(pdf))
    c.setTitle('Oryzz · Catálogo de email'); c.setAuthor('Oryzz'); c.setSubject('Plantillas de email, firmas y previsualizaciones v2.0')

    # ---------------- portada
    W, H = 1280, 900
    c.setPageSize((W, H))
    c.setFillColor(G950); c.rect(0, 0, W, H, stroke=0, fill=1)
    # órbitas de fondo (sistema gráfico)
    c.setStrokeColor(G700); c.setLineWidth(1.2)
    for r in (180, 300, 420):
        c.arc(W - 40 - r, -r + 120, W - 40 + r, r + 120, 95, 150)
    c.setFillColor(LIMA); c.circle(W - 40 - 300 * 0.5736 - 0, 120 + 300 * 0.8192, 7, stroke=0, fill=1)
    logo = out / 'assets' / 'oryzz-logo_sobre-oscuro.png'
    c.drawImage(ImageReader(str(logo)), 96, H - 150, 224 * 0.75, 55.5 * 0.75, mask='auto')
    _eb(c, 96, H - 330, 'Sistema de email · v2.0 · septiembre 2026', col=G400, node=LIMA, size=14)
    c.setFillColor('#FFFFFF'); c.setFont('SG', 64)
    c.drawString(92, H - 410, 'Sistema de email')
    c.setFont('MR', 20); c.setFillColor(G200)
    c.drawString(96, H - 452, 'Plantillas HTML, firmas y previsualizaciones en escritorio, móvil y modo oscuro.')
    # índice
    y = H - 540
    _rotulo(c, 96, y, 'Índice', col=G400, size=13); y -= 26
    for i, n in enumerate(nombres, 1):
        m = meta.get(n, {})
        c.setFillColor('#5C8BFF'); c.circle(100, y + 4, 2.5, stroke=0, fill=1)
        c.setFont('MRS', 13); c.setFillColor('#FFFFFF'); c.drawString(130, y, n + '.html')
        c.setFont('MR', 12); c.setFillColor(G400); c.drawString(420, y, (m.get('descripcion') or '')[:95])
        y -= 22
    c.setFillColor('#5C8BFF'); c.circle(100, y + 4, 2.5, stroke=0, fill=1)
    c.setFont('MRS', 13); c.setFillColor('#FFFFFF'); c.drawString(130, y, 'firmas/')
    c.setFont('MR', 12); c.setFillColor(G400); c.drawString(420, y, 'Juan Salazar, David Morales y Oryzz Tap · completa y compacta')
    c.setFont('MR', 11); c.setFillColor(G500)
    c.drawString(96, 48, 'oryzz.com  ·  Más clientes. No más likes.')
    c.showPage()

    # ---------------- cómo leer
    W, H = 1280, 900
    c.setPageSize((W, H))
    c.setFillColor(G50); c.rect(0, 0, W, H, stroke=0, fill=1)
    _eb(c, 96, H - 110, 'Cómo está hecho', size=14)
    c.setFillColor(G950); c.setFont('SG', 40); c.drawString(94, H - 170, 'Un sistema, tres tipos de correo.')
    cols = [
        ('Marca', 'Newsletter, confirmaciones, bienvenida, informe y propuesta. Cabecera Grafito 950 con logo sólido, '
                  'tarjeta blanca de 600 px, un solo botón Azul 600 y pie con motivo del envío.'),
        ('1 a 1', 'Prospección y seguimientos. Sin imágenes, sin botón, sin preheader oculto y en tipografía del sistema: '
                  'tiene que parecer escrito a mano desde Gmail, porque lo está.'),
        ('Oryzz Tap', 'Pedido y activación. Mismo sistema en expresión clara: cabecera blanca, logo «oryzz tap» que cambia '
                      'en modo oscuro e iconos de la familia oficial.'),
    ]
    x = 96
    for t, d in cols:
        c.setFillColor('#FFFFFF'); c.setStrokeColor(G100); c.roundRect(x, H - 470, 340, 230, 14, stroke=1, fill=1)
        c.setFillColor(G950); c.setFont('SG', 24); c.drawString(x + 24, H - 290, t)
        c.setFont('MR', 13.5); c.setFillColor(G600)
        yy = H - 322
        for ln in _wrap(c, d, 'MR', 13.5, 292):
            c.drawString(x + 24, yy, ln); yy -= 20
        x += 364
    specs = ['600 px · tablas + CSS en línea · responsive a 375 px', 'Botón «bulletproof» con VML para Outlook Windows',
             'Modo oscuro: Apple Mail, iOS, Outlook.com (clases o-t1, o-bd…)', 'Fuentes web con alternativa Arial · texto mínimo 14 px',
             'Preheader oculto · alt en todas las imágenes · versión .txt', 'Enlace de baja {{baja_url}} en correos comerciales']
    y = H - 540
    _rotulo(c, 96, y, 'Especificaciones', size=13); y -= 28
    for i, s_ in enumerate(specs):
        cx = 96 + (i % 2) * 560
        cy = y - (i // 2) * 30
        c.setFillColor(AZUL); c.rect(cx, cy + 3, 6, 6, stroke=0, fill=1)
        c.setFillColor(G950); c.setFont('MR', 14); c.drawString(cx + 18, cy, s_)
    c.setFont('MR', 12); c.setFillColor(G500)
    c.drawString(96, 60, 'Las previsualizaciones usan datos de muestra en lugar de los {{marcadores}}. Las cifras del informe son de ejemplo.')
    c.showPage()

    # ---------------- una página por plantilla
    for i, n in enumerate(nombres, 1):
        m = meta.get(n, {})
        d = pv / ('%s_escritorio-600.png' % n)
        mo = pv / ('%s_movil-375.png' % n)
        dk = pv / ('%s_oscuro-600.png' % n)
        from PIL import Image
        dh = Image.open(d).size[1] / 2 * PT
        mh = Image.open(mo).size[1] / 2 * PT * 0.9
        kh = (Image.open(dk).size[1] / 2 * PT * 0.6) if dk.exists() else 0
        top = 200
        H = max(dh, mh, kh) + top + 70
        W = 60 + 280 + 40 + 664 * PT + 36 + 375 * PT * 0.9 + (36 + 664 * PT * 0.6 if dk.exists() else 0) + 60
        c.setPageSize((W, H))
        c.setFillColor(G50); c.rect(0, 0, W, H, stroke=0, fill=1)
        # columna info
        _eb(c, 60, H - 70, m.get('tipo', ''), size=13)
        c.setFillColor(G950); c.setFont('SG', 26)
        yy = H - 108
        for ln in _wrap(c, n.split('_', 1)[1].replace('_', ' ').capitalize(), 'SG', 26, 280):
            c.drawString(60, yy, ln); yy -= 30
        c.setFont('JB', 10); c.setFillColor(G500); c.drawString(60, yy - 4, n + '.html'); yy -= 34
        for lab, val in [('Asunto', m.get('asunto', '')), ('Preheader', m.get('preheader') or '— (correo 1 a 1)'),
                         ('Uso', m.get('descripcion', ''))]:
            _rotulo(c, 60, yy, lab); yy -= 17
            c.setFont('MR', 12.5); c.setFillColor(G950)
            for ln in _wrap(c, val, 'MR', 12.5, 280):
                c.drawString(60, yy, ln); yy -= 17
            yy -= 14
        mk = m.get('marcadores') or []
        if mk:
            _rotulo(c, 60, yy, 'Marcadores'); yy -= 16
            c.setFont('JB', 9.5); c.setFillColor(G600)
            for ln in _wrap(c, '  '.join('{{%s}}' % k for k in mk), 'JB', 9.5, 280):
                c.drawString(60, yy, ln); yy -= 14
        # imágenes
        x = 60 + 280 + 40
        ytop = H - 70
        for lab, path, w in [('Escritorio · 600 px', d, 664 * PT), ('Móvil · 375 px', mo, 375 * PT * 0.9),
                             ('Modo oscuro · Apple Mail', dk, 664 * PT * 0.6)]:
            if not path.exists():
                continue
            _rotulo(c, x, ytop + 12, lab)
            _img(c, path, x, ytop, w)
            x += w + 36
        c.showPage()

    # ---------------- firmas
    fp = pv / 'firmas_escritorio.png'
    if fp.exists():
        from PIL import Image
        ih = Image.open(fp).size[1] / 2 * PT
        W, H = 920 * PT + 120, ih + 150
        c.setPageSize((W, H))
        c.setFillColor(G50); c.rect(0, 0, W, H, stroke=0, fill=1)
        _eb(c, 60, H - 60, 'Firmas', size=13)
        c.setFillColor(G950); c.setFont('SG', 26); c.drawString(60, H - 96, 'Firmas de correo')
        _img(c, fp, 60, H - 120, 920 * PT)
        c.showPage()
    c.save()
    print('catálogo ok:', pdf)
