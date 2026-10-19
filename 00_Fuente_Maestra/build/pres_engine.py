"""
Oryzz · motor de presentaciones (v2.0)

Un único modelo (coordenadas en px sobre un lienzo 1920x1080) que se emite a:
  - PPTX nativo con slide master, layouts y placeholders reales (python-pptx + XML)
  - HTML (una <section> por slide) para previsualizar y exportar a PDF con Chrome

1 px = 6350 EMU = 0,5 pt  ->  los tamaños de letra se escriben en pt (tamaño PowerPoint)
y en HTML se multiplican por 2.
"""
import os, re, copy, hashlib
from xml.sax.saxutils import escape as _esc
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.opc.packuri import PackURI
from pptx.opc.constants import RELATIONSHIP_TYPE as RT, CONTENT_TYPE as CT
from pptx.parts.slide import SlideLayoutPart
from pptx.oxml import parse_xml
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_MARK, XL_TICK_LABEL_POSITION

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, '..', 'fonts', 'static')
W, H = 1920, 1080
EMU = 6350


def E(px):
    return int(round(px * EMU))


def esc(s):
    return _esc(s, {'"': '&quot;'})


NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')

# ---------------------------------------------------------------- tipografía
# pptx: nombre de familia que ve PowerPoint (+mj-lt / +mn-lt = fuentes del tema)
FONTS = {
    'display':      dict(pptx='+mj-lt', b=True,  css="'Space Grotesk'", w=700, file='SpaceGrotesk-Bold.ttf'),
    'display_semi': dict(pptx='Space Grotesk SemiBold', b=False, css="'Space Grotesk'", w=600, file='SpaceGrotesk-SemiBold.ttf'),
    'display_med':  dict(pptx='Space Grotesk Medium', b=False, css="'Space Grotesk'", w=500, file='SpaceGrotesk-Medium.ttf'),
    'display_reg':  dict(pptx='+mj-lt', b=False, css="'Space Grotesk'", w=400, file='SpaceGrotesk-Regular.ttf'),
    'text':         dict(pptx='+mn-lt', b=False, css="'Manrope'", w=400, file='Manrope-Regular.ttf'),
    'text_med':     dict(pptx='Manrope Medium', b=False, css="'Manrope'", w=500, file='Manrope-Medium.ttf'),
    'text_semi':    dict(pptx='Manrope SemiBold', b=False, css="'Manrope'", w=600, file='Manrope-SemiBold.ttf'),
    'text_bold':    dict(pptx='+mn-lt', b=True,  css="'Manrope'", w=700, file='Manrope-Bold.ttf'),
    'mono':         dict(pptx='JetBrains Mono', b=False, css="'JetBrains Mono'", w=400, file='JetBrainsMono-Regular.ttf'),
    'mono_bold':    dict(pptx='JetBrains Mono', b=True, css="'JetBrains Mono'", w=700, file='JetBrainsMono-Bold.ttf'),
}
CSS_FALLBACK = {"'Space Grotesk'": 'Arial, Helvetica, sans-serif', "'Manrope'": 'Arial, Helvetica, sans-serif',
                "'JetBrains Mono'": "Consolas, 'Courier New', monospace"}

_metrics = {}


def _font_metrics(key):
    if key not in _metrics:
        from fontTools.ttLib import TTFont
        f = TTFont(os.path.join(FONT_DIR, FONTS[key]['file']))
        cmap = f.getBestCmap(); hm = f['hmtx']; upm = f['head'].unitsPerEm
        _metrics[key] = (cmap, hm, upm)
    return _metrics[key]


def text_width(text, st):
    """Ancho aproximado en px (sin kerning) del texto con el estilo resuelto."""
    cmap, hm, upm = _font_metrics(st.get('font', 'text'))
    size_px = st.get('size', 20) * 2
    if st.get('caps'):
        text = text.upper()
    w = 0
    for ch in text:
        g = cmap.get(ord(ch)) or cmap.get(ord('n'))
        w += hm[g][0] / upm * size_px
    w += len(text) * st.get('spc', 0) * size_px
    return w


# ---------------------------------------------------------------- modelo
class Rn:
    def __init__(self, text, **st):
        self.text, self.st = text, st


class P:
    def __init__(self, runs, **st):
        if isinstance(runs, str):
            runs = parse_inline(runs)
        self.runs, self.st = runs, st


def parse_inline(s):
    """**texto** -> run resaltado (color 'hl' del estilo)."""
    out = []
    for i, part in enumerate(re.split(r'\*\*', s)):
        if part:
            out.append(Rn(part, hl=True) if i % 2 else Rn(part))
    return out or [Rn('')]


def to_paras(content):
    if content is None:
        return []
    if isinstance(content, P):
        return [content]
    if isinstance(content, str):
        return [P(line) for line in content.split('\n')]
    out = []
    for item in content:
        if isinstance(item, P):
            out.append(item)
        elif isinstance(item, tuple):
            out.append(P(item[0], **item[1]))
        else:
            out.append(P(item))
    return out


class T:
    """Caja de texto (fuera de placeholder)."""
    kind = 'text'

    def __init__(self, x, y, w, h, content, name='Texto', **st):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.paras, self.st, self.name = to_paras(content), st, name


class Box:
    kind = 'box'

    def __init__(self, x, y, w, h, fill=None, line=None, lw=1, r=0, grad=None, alpha=None, name='Forma', shape=None):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.fill, self.line, self.lw, self.r, self.grad, self.alpha = fill, line, lw, r, grad, alpha
        self.name, self.shape = name, shape


class Dot(Box):
    def __init__(self, cx, cy, r, fill, line=None, lw=1, name='Nodo'):
        super().__init__(cx - r, cy - r, 2 * r, 2 * r, fill=fill, line=line, lw=lw, name=name, shape='ellipse')


class Ln:
    kind = 'line'

    def __init__(self, x1, y1, x2, y2, color, w=1, dash=None, name='Línea'):
        self.x1, self.y1, self.x2, self.y2, self.color, self.w, self.dash, self.name = x1, y1, x2, y2, color, w, dash, name


class Img:
    kind = 'img'

    def __init__(self, x, y, w, h, path, name='Imagen', descr=''):
        self.x, self.y, self.w, self.h, self.path, self.name, self.descr = x, y, w, h, path, name, descr


class PH:
    """Placeholder de layout. kind: title | body | pic | chart | tbl"""

    def __init__(self, idx, kind, x, y, w, h, prompt='', name=None, **st):
        self.idx, self.kind = idx, kind
        self.x, self.y, self.w, self.h = x, y, w, h
        self.prompt, self.st = prompt, st
        self.name = name or {'title': 'Título', 'pic': 'Imagen', 'chart': 'Gráfico', 'tbl': 'Tabla'}.get(kind, 'Texto')


class Layout:
    def __init__(self, name, statics=(), phs=(), bg=None, footer=True, number=True):
        self.name, self.statics, self.phs, self.bg = name, list(statics), list(phs), bg
        self.footer, self.number = footer, number

    def ph(self, idx):
        for p in self.phs:
            if p.idx == idx:
                return p
        raise KeyError(f'{self.name}: no hay placeholder {idx}')


class Chart:
    def __init__(self, categories, series, kind='bar', y_max=None, y_unit=None, fmt='0', labels=False,
                 label_fmt=None, point_colors=None, gap=70, legend=False, label_color=None):
        self.categories, self.series, self.kind = categories, series, kind   # series: [(nombre, valores, color)]
        self.y_max, self.y_unit, self.fmt, self.labels, self.label_fmt = y_max, y_unit, fmt, labels, label_fmt or fmt
        self.point_colors = point_colors or {}                              # {(serie, i): color}
        self.gap, self.legend, self.label_color = gap, legend, label_color


class Table:
    def __init__(self, rows, col_w, row_h, header=True, styles=None, col_styles=None, col_fill=None, col_top=None):
        """rows: lista de listas de contenido (str con ** o lista de P). col_w/row_h en px."""
        self.rows, self.col_w, self.row_h, self.header = rows, col_w, row_h, header
        self.styles = styles or {}             # 'head', 'cell', 'first'
        self.col_styles = col_styles or {}     # {col: estilo}
        self.col_fill = col_fill or {}         # {col: color de fondo}
        self.col_top = col_top or {}           # {col: color de borde superior grueso}


class Slide:
    def __init__(self, layout, fill=None, extras=(), under=(), notes='', footer=None):
        self.layout, self.fill, self.extras, self.under = layout, fill or {}, list(extras), list(under)
        self.notes, self.footer = notes, footer


# ---------------------------------------------------------------- estilos
def merged(*dicts):
    out = {}
    for d in dicts:
        if d:
            out.update({k: v for k, v in d.items() if v is not None})
    return out


def run_style(base, para, run):
    st = merged(base, para, run.st)
    if run.st.get('hl') and base.get('hl_color'):
        st['color'] = base['hl_color']
    return st


# ---------------------------------------------------------------- XML DrawingML
def _clr(c, alpha=None):
    c = c.lstrip('#').upper()
    a = f'<a:alpha val="{int(alpha * 100000)}"/>' if alpha is not None and alpha < 1 else ''
    return f'<a:srgbClr val="{c}">{a}</a:srgbClr>'


def _fill(color=None, grad=None, alpha=None, angle=45):
    if grad:
        stops = ''.join(f'<a:gs pos="{int(i * 100000 / (len(grad) - 1))}">{_clr(c, alpha)}</a:gs>' for i, c in enumerate(grad))
        return f'<a:gradFill rotWithShape="1"><a:gsLst>{stops}</a:gsLst><a:lin ang="{int(angle * 60000)}" scaled="0"/></a:gradFill>'
    if color:
        return f'<a:solidFill>{_clr(color, alpha)}</a:solidFill>'
    return '<a:noFill/>'


def _ln(color=None, w=1, dash=None, cap=None):
    if not color:
        return '<a:ln><a:noFill/></a:ln>'
    d = f'<a:prstDash val="{dash}"/>' if dash else ''
    c = f' cap="{cap}"' if cap else ''
    return f'<a:ln w="{E(w)}"{c}><a:solidFill>{_clr(color)}</a:solidFill>{d}</a:ln>'


def _xfrm(x, y, w, h, flipV=False):
    fv = ' flipV="1"' if flipV else ''
    return f'<a:xfrm{fv}><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'


def rpr(st, lang, tag='a:rPr', explicit_keys=None, size_for_spc=None, link_rid=None):
    keys = explicit_keys if explicit_keys is not None else st.keys()
    attrs = [f'lang="{lang}"']
    kids = ''
    if 'size' in keys and 'size' in st:
        attrs.append(f'sz="{int(round(st["size"] * 100))}"')
    f = FONTS.get(st.get('font')) if 'font' in keys else None
    if f:
        attrs.append(f'b="{1 if f["b"] else 0}"')
    if 'spc' in keys and 'spc' in st:
        size = st.get('size') or size_for_spc or 20
        attrs.append(f'spc="{int(round(st["spc"] * size * 100))}"')
    if 'caps' in keys and 'caps' in st:
        attrs.append(f'cap="{"all" if st["caps"] else "none"}"')
    if link_rid:
        attrs.append('u="none"')
    attrs.append('dirty="0"')
    if 'grad' in keys and st.get('grad'):
        kids += _fill(grad=st['grad'], angle=st.get('grad_angle', 0))
    elif 'color' in keys and st.get('color'):
        kids += _fill(st['color'])
    if f:
        kids += f'<a:latin typeface="{f["pptx"]}"/><a:cs typeface="{f["pptx"]}"/>'
    if link_rid:
        # hlinkClr=tx: el enlace conserva el color del texto (Office 2019+/365) en vez del color hlink del tema
        kids += (f'<a:hlinkClick r:id="{link_rid}"><a:extLst><a:ext uri="{{A12FA001-AC4F-418D-AE19-62706E023703}}">'
                 f'<ahyp:hlinkClr xmlns:ahyp="http://schemas.microsoft.com/office/drawing/2018/hyperlinkcolor" val="tx"/>'
                 f'</a:ext></a:extLst></a:hlinkClick>')
    return f'<{tag} {" ".join(attrs)}>{kids}</{tag}>'


def ppr(st, explicit_keys=None, lvl_tag='a:pPr', def_rpr=''):
    keys = explicit_keys if explicit_keys is not None else st.keys()
    attrs = []
    if 'align' in keys and 'align' in st:
        attrs.append(f'algn="{ {"l": "l", "c": "ctr", "r": "r"}[st["align"]] }"')
    bullet = st.get('bullet') if 'bullet' in keys else None
    if bullet:
        ind = st.get('indent', 32)
        attrs.append(f'marL="{E(ind)}" indent="{-E(ind)}"')
    elif lvl_tag != 'a:pPr' or ('bullet' in keys):
        attrs.append('marL="0" indent="0"')
    kids = ''
    if ('lh' in keys or 'size' in keys) and 'lh' in st and 'size' in st:
        kids += f'<a:lnSpc><a:spcPts val="{int(round(st["size"] * st["lh"] * 100))}"/></a:lnSpc>'
    if 'sb' in keys and 'sb' in st:
        kids += f'<a:spcBef><a:spcPts val="{int(st["sb"] * 100)}"/></a:spcBef>'
    elif lvl_tag != 'a:pPr':
        kids += '<a:spcBef><a:spcPts val="0"/></a:spcBef>'
    if 'sa' in keys and 'sa' in st:
        kids += f'<a:spcAft><a:spcPts val="{int(st["sa"] * 100)}"/></a:spcAft>'
    if bullet:
        bc = st.get('bullet_color') or st.get('color')
        kids += (f'<a:buClr>{_clr(bc)}</a:buClr><a:buSzPct val="100000"/>'
                 f'<a:buFont typeface="Arial"/><a:buChar char="{esc(bullet)}"/>')
    elif lvl_tag != 'a:pPr' or 'bullet' in keys:
        kids += '<a:buNone/>'
    kids += def_rpr
    a = (' ' + ' '.join(attrs)) if attrs else ''
    return f'<{lvl_tag}{a}>{kids}</{lvl_tag}>'


def paras_xml(paras, base, lang, explicit=False, link_cb=None):
    """explicit=False -> estilo completo (caja de texto). True -> solo lo que define el contenido (placeholder)."""
    out = ''
    for p in paras:
        pst = merged(base, p.st)
        pkeys = set(p.st.keys()) if explicit else None
        if explicit and 'size' in p.st:
            pkeys |= {'lh'}
        runs = ''
        for r in p.runs:
            st = run_style(base, p.st, r)
            if explicit:
                keys = set(r.st.keys()) | set(p.st.keys())
                if r.st.get('hl') and base.get('hl_color'):
                    keys.add('color')
                keys.discard('hl')
            else:
                keys = None
            rid = link_cb(st['link']) if (link_cb and st.get('link')) else None
            parts = r.text.split('\v')
            for i, t in enumerate(parts):
                if i:
                    runs += f'<a:br>{rpr(st, lang, explicit_keys=keys, size_for_spc=pst.get("size"))}</a:br>'
                if t:
                    runs += f'<a:r>{rpr(st, lang, explicit_keys=keys, size_for_spc=pst.get("size"), link_rid=rid)}<a:t>{esc(t)}</a:t></a:r>'
        end = rpr(pst, lang, tag='a:endParaRPr', explicit_keys=pkeys)
        pp = ppr(pst, explicit_keys=pkeys)
        out += f'<a:p>{pp if pp != "<a:pPr></a:pPr>" else ""}{runs}{end}</a:p>'
    return out or f'<a:p><a:endParaRPr lang="{lang}"/></a:p>'


def body_pr(st, ph=False):
    anchor = {'t': 't', 'm': 'ctr', 'b': 'b'}[st.get('anchor', 't')]
    return (f'<a:bodyPr vert="horz" wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}" '
            f'anchorCtr="0" rtlCol="0"><a:noAutofit/></a:bodyPr>')


class IdGen:
    def __init__(self, start=2):
        self.n = start

    def __call__(self):
        self.n += 1
        return self.n


def el_xml(el, ids, img_rid, lang, link_cb=None):
    if el.kind == 'text':
        return (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="{esc(el.name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
                f'<p:spPr>{_xfrm(el.x, el.y, el.w, el.h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
                f'<p:txBody>{body_pr(el.st)}<a:lstStyle/>{paras_xml(el.paras, el.st, lang, link_cb=link_cb)}</p:txBody></p:sp>')
    if el.kind == 'box':
        geom = el.shape or ('roundRect' if el.r else 'rect')
        av = ''
        if geom == 'roundRect':
            av = f'<a:gd name="adj" fmla="val {int(min(50000, el.r / min(el.w, el.h) * 100000))}"/>'
        return (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="{esc(el.name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
                f'<p:spPr>{_xfrm(el.x, el.y, el.w, el.h)}<a:prstGeom prst="{geom}"><a:avLst>{av}</a:avLst></a:prstGeom>'
                f'{_fill(el.fill, el.grad, el.alpha)}{_ln(el.line, el.lw)}</p:spPr>'
                f'<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:endParaRPr lang="{lang}"/></a:p></p:txBody></p:sp>')
    if el.kind == 'line':
        x, y = min(el.x1, el.x2), min(el.y1, el.y2)
        w, h = abs(el.x2 - el.x1), abs(el.y2 - el.y1)
        flip = (el.x2 - el.x1) * (el.y2 - el.y1) < 0
        return (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{ids()}" name="{esc(el.name)}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
                f'<p:spPr>{_xfrm(x, y, w, h, flipV=flip)}<a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
                f'{_ln(el.color, el.w, el.dash, cap="rnd" if el.dash else None)}</p:spPr></p:cxnSp>')
    if el.kind == 'img':
        rid = img_rid(el.path)
        return (f'<p:pic><p:nvPicPr><p:cNvPr id="{ids()}" name="{esc(el.name)}" descr="{esc(el.descr)}"/>'
                f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr userDrawn="1"/></p:nvPicPr>'
                f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
                f'<p:spPr>{_xfrm(el.x, el.y, el.w, el.h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    raise ValueError(el.kind)


PH_TYPE = {'title': 'title', 'body': 'body', 'pic': 'pic', 'chart': 'chart', 'tbl': 'tbl'}


def ph_xml(ph, ids, lang):
    t = PH_TYPE[ph.kind]
    phtag = '<p:ph type="title"/>' if t == 'title' else f'<p:ph type="{t}" sz="quarter" idx="{ph.idx}"/>'
    st = ph.st
    def_rpr = rpr(st, lang, tag='a:defRPr') if ph.kind in ('title', 'body') else ''
    lvl = ppr(st, lvl_tag='a:lvl1pPr', def_rpr=def_rpr) if ph.kind in ('title', 'body') else ''
    geom = ''
    if ph.kind == 'pic':
        r = st.get('r', 0)
        if r:
            geom = f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {int(r / min(ph.w, ph.h) * 100000)}"/></a:avLst></a:prstGeom>'
        else:
            geom = '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        geom += _fill(st.get('fill'))
    prompt = f'<a:p><a:r><a:rPr lang="{lang}" dirty="0"/><a:t>{esc(ph.prompt)}</a:t></a:r></a:p>' if ph.prompt else f'<a:p><a:endParaRPr lang="{lang}"/></a:p>'
    if ph.kind == 'pic':
        pst = merged({'size': 12, 'font': 'text_med', 'color': st.get('prompt_color', '#8A90A0'), 'align': 'c', 'lh': 1.3})
        lvl = ppr(pst, lvl_tag='a:lvl1pPr', def_rpr=rpr(pst, lang, tag='a:defRPr'))
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="{esc(ph.name)}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr>{phtag}</p:nvPr></p:nvSpPr><p:spPr>{_xfrm(ph.x, ph.y, ph.w, ph.h)}{geom}</p:spPr>'
            f'<p:txBody>{body_pr({"anchor": "m"} if ph.kind == "pic" else st, ph=True)}<a:lstStyle>{lvl}</a:lstStyle>{prompt}</p:txBody></p:sp>')


# ---------------------------------------------------------------- tema
class Theme:
    """Paleta + reglas de cada expresión (oscura / clara)."""

    def __init__(self, key, name, dark, colors, clr_scheme, hlink, folhlink, footer_style, number_style,
                 footer_logo=None, footer_text='Oryzz · Sistemas que captan clientes', lang='es-ES'):
        self.key, self.name, self.dark, self.c = key, name, dark, colors
        self.clr_scheme, self.hlink, self.folhlink = clr_scheme, hlink, folhlink
        self.footer_style, self.number_style, self.footer_logo = footer_style, number_style, footer_logo
        self.footer_text, self.lang = footer_text, lang


FOOTER_Y = 1004
FOOTER_H = 24


def footer_elements(theme):
    """Pie discreto (estático) + placeholders ftr y sldNum."""
    return []


def master_xml(theme, layout_rids, theme_rid):
    c = theme.c
    clrmap = ('bg1="dk1" tx1="lt1" bg2="dk2" tx2="lt2"' if theme.dark else 'bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2"')
    lang = theme.lang
    title_st = dict(font='display', size=44, color=c['text'], spc=-0.035, lh=1.02, align='l')
    body_st = dict(font='text', size=20, color=c['text2'], lh=1.5, align='l')
    ids = IdGen(1)
    fst = theme.footer_style
    nst = theme.number_style
    title = ph_xml(PH(0, 'title', 120, 168, 1300, 120, 'Título de la diapositiva', **title_st), ids, lang)
    body = ph_xml(PH(1, 'body', 120, 360, 1100, 560, 'Texto', **body_st), ids, lang).replace('<p:ph type="body" sz="quarter" idx="1"/>', '<p:ph type="body" idx="1"/>')
    ftr = (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="Pie"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
           f'<p:nvPr><p:ph type="ftr" sz="quarter" idx="3"/></p:nvPr></p:nvSpPr><p:spPr>{_xfrm(164, FOOTER_Y, 1000, FOOTER_H)}'
           f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr><p:txBody>{body_pr({"anchor": "m"})}<a:lstStyle>'
           f'{ppr(fst, lvl_tag="a:lvl1pPr", def_rpr=rpr(fst, lang, tag="a:defRPr"))}</a:lstStyle>'
           f'<a:p><a:r><a:rPr lang="{lang}" dirty="0"/><a:t>{esc(theme.footer_text)}</a:t></a:r></a:p></p:txBody></p:sp>')
    num = (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="Número de diapositiva"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
           f'<p:nvPr><p:ph type="sldNum" sz="quarter" idx="4"/></p:nvPr></p:nvSpPr><p:spPr>{_xfrm(1640, FOOTER_Y, 160, FOOTER_H)}'
           f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr><p:txBody>{body_pr({"anchor": "m"})}<a:lstStyle>'
           f'{ppr(nst, lvl_tag="a:lvl1pPr", def_rpr=rpr(nst, lang, tag="a:defRPr"))}</a:lstStyle>'
           f'<a:p><a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum"><a:rPr lang="{lang}"/><a:t>‹#›</a:t></a:fld>'
           f'<a:endParaRPr lang="{lang}"/></a:p></p:txBody></p:sp>')
    sp_tree_head = ('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm>'
                    '<a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')

    def lvl(i, st):
        tag = f'a:lvl{i}pPr'
        if i == 1:
            return ppr(st, lvl_tag=tag, def_rpr=rpr(st, lang, tag='a:defRPr'))
        s2 = dict(st, bullet='–', indent=32 * (i - 1) + 0, bullet_color=c['text3'])
        return ppr(s2, lvl_tag=tag, def_rpr=rpr(st, lang, tag='a:defRPr'))

    title_style = ''.join(lvl(i, title_st) for i in [1]) + ''.join(
        ppr(title_st, lvl_tag=f'a:lvl{i}pPr', def_rpr=rpr(title_st, lang, tag='a:defRPr')) for i in range(2, 10))
    body_style = ''.join(lvl(i, body_st) for i in range(1, 10))
    other_st = dict(font='text', size=18, color=c['text2'])
    other_style = ''.join(ppr(other_st, lvl_tag=f'a:lvl{i}pPr', def_rpr=rpr(other_st, lang, tag='a:defRPr')) for i in range(1, 10))
    ids_lst = ''.join(f'<p:sldLayoutId id="{2147483649 + i}" r:id="{rid}"/>' for i, rid in enumerate(layout_rids))
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster {NS}><p:cSld name="Oryzz {theme.name}">'
            f'<p:bg><p:bgPr>{_fill(c["bg"])}<a:effectLst/></p:bgPr></p:bg><p:spTree>{sp_tree_head}{title}{body}{ftr}{num}</p:spTree></p:cSld>'
            f'<p:clrMap {clrmap} accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" '
            f'accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst>{ids_lst}</p:sldLayoutIdLst>'
            f'<p:hf hdr="0" dt="0"/>'
            f'<p:txStyles><p:titleStyle>{title_style}</p:titleStyle><p:bodyStyle>{body_style}</p:bodyStyle>'
            f'<p:otherStyle>{other_style}</p:otherStyle></p:txStyles></p:sldMaster>')


def theme_blob(old_blob, theme):
    s = old_blob.decode('utf8')
    cs = theme.clr_scheme

    def sc(tag, hexv):
        return f'<a:{tag}><a:srgbClr val="{hexv.lstrip("#").upper()}"/></a:{tag}>'
    clr = (f'<a:clrScheme name="Oryzz {theme.name}">' + sc('dk1', cs['dk1']) + sc('lt1', cs['lt1']) + sc('dk2', cs['dk2']) +
           sc('lt2', cs['lt2']) + ''.join(sc(f'accent{i}', cs[f'accent{i}']) for i in range(1, 7)) +
           sc('hlink', theme.hlink) + sc('folHlink', theme.folhlink) + '</a:clrScheme>')
    font = ('<a:fontScheme name="Oryzz"><a:majorFont><a:latin typeface="Space Grotesk" panose="00000000000000000000" pitchFamily="34" charset="0"/>'
            '<a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Manrope" panose="00000000000000000000" pitchFamily="34" charset="0"/>'
            '<a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>')
    s = re.sub(r'<a:clrScheme.*?</a:clrScheme>', clr, s, flags=re.S)
    s = re.sub(r'<a:fontScheme.*?</a:fontScheme>', font, s, flags=re.S)
    s = re.sub(r'<a:theme ([^>]*?)name="[^"]*"', rf'<a:theme \1name="Oryzz {theme.name}"', s, count=1)
    return s.encode('utf8')


# ---------------------------------------------------------------- PPTX
class PptxBuilder:
    def __init__(self, theme, layouts, footer_logo_el=None):
        self.theme, self.layouts = theme, layouts
        self.prs = Presentation()
        prs = self.prs
        prs.slide_width, prs.slide_height = Emu(E(W)), Emu(E(H))
        master_part = prs.slide_masters[0].part if False else prs.part.related_part(
            prs.part._element.sldMasterIdLst[0].rId)
        pkg = prs.part.package
        # tema
        theme_part = master_part.part_related_by(RT.THEME)
        theme_part._blob = theme_blob(theme_part.blob, theme)
        # quitar layouts por defecto
        for rId in [r.rId for r in list(master_part.rels.values()) if r.reltype == RT.SLIDE_LAYOUT]:
            master_part.rels.pop(rId)
        theme_rid = [r.rId for r in master_part.rels.values() if r.reltype == RT.THEME][0]
        self.layout_parts = {}
        rids = []
        dummy = parse_xml(f'<p:sldLayout {NS}><p:cSld><p:spTree/></p:cSld></p:sldLayout>')
        for i, L in enumerate(layouts):
            part = SlideLayoutPart(PackURI(f'/ppt/slideLayouts/slideLayout{i + 1}.xml'), CT.PML_SLIDE_LAYOUT, pkg, copy.deepcopy(dummy))
            part.relate_to(master_part, RT.SLIDE_MASTER)
            rids.append(master_part.relate_to(part, RT.SLIDE_LAYOUT))
            part._element = parse_xml(self._layout_xml(L, part).encode('utf8'))
            self.layout_parts[L.name] = part
        master_part._element = parse_xml(master_xml(theme, rids, theme_rid).encode('utf8'))

    def _layout_xml(self, L, part):
        lang = self.theme.lang
        ids = IdGen(1)

        def img_rid(path):
            return part.get_or_add_image_part(path)[1]
        statics = ''.join(el_xml(e, ids, img_rid, lang) for e in L.statics)
        phs = ''.join(ph_xml(p, ids, lang) for p in L.phs)
        extra = ''
        if L.footer:
            extra += (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="Pie"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
                      f'<p:nvPr><p:ph type="ftr" sz="quarter" idx="3"/></p:nvPr></p:nvSpPr><p:spPr/>'
                      f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="{lang}" dirty="0"/><a:t>{esc(self.theme.footer_text)}</a:t></a:r></a:p></p:txBody></p:sp>')
        if L.number:
            extra += (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="Número de diapositiva"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
                      f'<p:nvPr><p:ph type="sldNum" sz="quarter" idx="4"/></p:nvPr></p:nvSpPr><p:spPr/>'
                      f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum">'
                      f'<a:rPr lang="{lang}"/><a:t>‹#›</a:t></a:fld><a:endParaRPr lang="{lang}"/></a:p></p:txBody></p:sp>')
        bg = f'<p:bg><p:bgPr>{_fill(L.bg)}<a:effectLst/></p:bgPr></p:bg>' if L.bg else ''
        head = ('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm>'
                '<a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')
        return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout {NS} preserve="1" userDrawn="1">'
                f'<p:cSld name="{esc(L.name)}">{bg}<p:spTree>{head}{statics}{phs}{extra}</p:spTree></p:cSld>'
                f'<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')

    # ---------------------------------------------------------- slides
    def add(self, S):
        L = S.layout
        lang = self.theme.lang
        slide = self.prs.slides.add_slide(self.layout_parts[L.name].slide_layout)
        tree = slide.shapes._spTree
        part = slide.part
        ids = IdGen(max([int(e.get('id')) for e in tree.iter() if e.tag.endswith('}cNvPr')] + [1]) + 1)

        def img_rid(path):
            return part.get_or_add_image_part(path)[1]

        def link_cb(url):
            return part.relate_to(url, RT.HYPERLINK, is_external=True)

        phmap = {}
        for shp in list(slide.placeholders):
            idx = shp.placeholder_format.idx
            phmap[idx] = shp
        pic_el = None
        for p in L.phs:
            key = 0 if p.kind == 'title' else p.idx
            shp = phmap.get(key)
            if shp is None:
                continue
            content = S.fill.get(p.idx if p.kind != 'title' else 0, S.fill.get(p.idx))
            if content is None:
                tree.remove(shp._element)
                continue
            if p.kind in ('title', 'body'):
                if isinstance(content, dict):
                    extra_st = {k: v for k, v in content.items() if k != 'text'}
                    paras = to_paras(content['text'])
                    for pp in paras:
                        pp.st = merged({k: v for k, v in extra_st.items() if k in ('align', 'lh', 'size', 'sa', 'sb')}, pp.st)
                        for r in pp.runs:
                            r.st = merged({k: v for k, v in extra_st.items() if k in ('color', 'font', 'size', 'spc', 'caps', 'grad', 'grad_angle')}, r.st)
                else:
                    paras = to_paras(content)
                base = dict(p.st)
                runs_all = [r for pp in paras for r in pp.runs if r.text]
                shape_link = None
                if len(runs_all) == 1 and runs_all[0].st.get('link'):
                    # enlace único (p. ej. botón): va en la forma, así no se subraya y todo el botón es clicable
                    shape_link = runs_all[0].st.pop('link')
                    cnv = shp._element.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}cNvPr')
                    cnv.append(parse_xml(f'<a:hlinkClick {NS} r:id="{link_cb(shape_link)}"/>'))
                xml = f'<p:txBody {NS}><a:bodyPr/><a:lstStyle/>{paras_xml(paras, base, lang, explicit=True, link_cb=link_cb)}</p:txBody>'
                if shape_link:
                    runs_all[0].st['link'] = shape_link
                old = shp._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}txBody')
                new = parse_xml(xml)
                if old is not None:
                    old.getparent().replace(old, new)
                else:
                    shp._element.append(new)
            elif p.kind == 'pic':
                pic = shp.insert_picture(content)
                pic_el = pic._element
            elif p.kind == 'chart':
                self._chart(shp, content)
            elif p.kind == 'tbl':
                self._table(shp, content, p)
        # capas bajo el texto (velos sobre la foto)
        if S.under:
            anchor = pic_el
            for e in S.under:
                node = parse_xml(f'<p:root {NS}>{el_xml(e, ids, img_rid, lang)}</p:root>')[0]
                if anchor is not None:
                    anchor.addnext(node); anchor = node
                else:
                    tree.insert(2, node)
        for e in S.extras:
            if isinstance(e, tuple) and e[0] == 'chart':
                continue
            node = parse_xml(f'<p:root {NS}>{el_xml(e, ids, img_rid, lang, link_cb)}</p:root>')[0]
            tree.append(node)
        # pie + número (los placeholders de pie no se clonan solos)
        if L.footer:
            txt = S.footer if S.footer is not None else self.theme.footer_text
            tree.append(parse_xml(
                f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="{ids()}" name="Pie"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
                f'<p:nvPr><p:ph type="ftr" sz="quarter" idx="3"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>'
                f'<a:p><a:r><a:rPr lang="{lang}" dirty="0"/><a:t>{esc(txt)}</a:t></a:r></a:p></p:txBody></p:sp>'))
        if L.number:
            tree.append(parse_xml(
                f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="{ids()}" name="Número de diapositiva"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
                f'<p:nvPr><p:ph type="sldNum" sz="quarter" idx="4"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>'
                f'<a:p><a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum"><a:rPr lang="{lang}"/><a:t>{len(self.prs.slides)}</a:t></a:fld>'
                f'<a:endParaRPr lang="{lang}"/></a:p></p:txBody></p:sp>'))
        if S.notes:
            slide.notes_slide.notes_text_frame.text = S.notes
        return slide

    def _chart(self, shp, ch):
        c = self.theme.c
        data = CategoryChartData()
        data.categories = ch.categories
        for name, vals, _ in ch.series:
            data.add_series(name, vals)
        kind = {'bar': XL_CHART_TYPE.COLUMN_CLUSTERED, 'line': XL_CHART_TYPE.LINE_MARKERS}[ch.kind]
        gf = shp.insert_chart(kind, data)
        chart = gf.chart
        chart.has_legend = ch.legend
        chart.has_title = False
        chart.font.name = 'Manrope'
        chart.font.size = Pt(14)
        chart.font.color.rgb = RGBColor.from_string(c['text3'].lstrip('#'))
        plot = chart.plots[0]
        if ch.kind == 'bar':
            plot.gap_width = ch.gap
            plot.overlap = -10 if len(ch.series) > 1 else 0
        plot.vary_by_categories = False
        for si, (s, (_, vals, color)) in enumerate(zip(plot.series, ch.series)):
            if ch.kind == 'bar':
                s.format.fill.solid(); s.format.fill.fore_color.rgb = RGBColor.from_string(color.lstrip('#'))
                s.format.line.fill.background()
            else:
                s.format.line.color.rgb = RGBColor.from_string(color.lstrip('#'))
                s.format.line.width = Pt(2.25)
                s.smooth = False
                from pptx.enum.chart import XL_MARKER_STYLE
                s.marker.style = XL_MARKER_STYLE.CIRCLE; s.marker.size = 7
                s.marker.format.fill.solid(); s.marker.format.fill.fore_color.rgb = RGBColor.from_string(color.lstrip('#'))
                s.marker.format.line.fill.background()
            for i in range(len(vals)):
                pc = ch.point_colors.get((si, i))
                if pc:
                    pt = s.points[i]
                    if ch.kind == 'bar':
                        pt.format.fill.solid(); pt.format.fill.fore_color.rgb = RGBColor.from_string(pc.lstrip('#'))
                    else:
                        pt.marker.format.fill.solid(); pt.marker.format.fill.fore_color.rgb = RGBColor.from_string(pc.lstrip('#'))
                        pt.marker.size = 11
        if ch.labels:
            plot.has_data_labels = True
            dl = plot.data_labels
            dl.number_format = ch.label_fmt; dl.number_format_is_linked = False
            dl.font.size = Pt(14); dl.font.name = 'JetBrains Mono'
            dl.font.color.rgb = RGBColor.from_string((ch.label_color or c['text2']).lstrip('#'))
            dl.position = XL_LABEL_POSITION.OUTSIDE_END if ch.kind == 'bar' else XL_LABEL_POSITION.ABOVE
        va = chart.value_axis
        if ch.y_max is not None:
            va.maximum_scale = ch.y_max; va.minimum_scale = 0
        if ch.y_unit:
            va.major_unit = ch.y_unit
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = RGBColor.from_string(c['border'].lstrip('#'))
        va.major_gridlines.format.line.width = Pt(0.75)
        va.format.line.fill.background()
        va.major_tick_mark = XL_TICK_MARK.NONE
        va.tick_labels.number_format = ch.fmt; va.tick_labels.number_format_is_linked = False
        va.tick_labels.font.size = Pt(14); va.tick_labels.font.name = 'JetBrains Mono'
        ca = chart.category_axis
        ca.format.line.color.rgb = RGBColor.from_string(c['border'].lstrip('#'))
        ca.major_tick_mark = XL_TICK_MARK.NONE
        ca.tick_labels.font.size = Pt(14); ca.tick_labels.font.name = 'JetBrains Mono'
        # fondo transparente
        cs = chart._chartSpace
        nsC = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
        spPr = parse_xml(f'<c:spPr xmlns:c="{nsC}" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:noFill/><a:ln><a:noFill/></a:ln></c:spPr>')
        txPr = cs.find(f'{{{nsC}}}txPr')
        (txPr.addprevious(spPr) if txPr is not None else cs.append(spPr))
        pa = cs.find(f'.//{{{nsC}}}plotArea')
        pa.append(parse_xml(f'<c:spPr xmlns:c="{nsC}" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:noFill/><a:ln><a:noFill/></a:ln></c:spPr>'))
        rc = cs.find(f'{{{nsC}}}roundedCorners')
        if rc is None:
            cs.insert(0, parse_xml(f'<c:roundedCorners xmlns:c="{nsC}" val="0"/>'))
        return gf

    def _table(self, shp, tb, ph):
        c = self.theme.c
        lang = self.theme.lang
        nrows, ncols = len(tb.rows), len(tb.rows[0])
        gf = shp.insert_table(nrows, ncols)
        tbl = gf.table
        tblPr = tbl._tbl.tblPr
        tblPr.set('firstRow', '0'); tblPr.set('bandRow', '0')
        sid = tblPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}tableStyleId')
        if sid is not None:
            sid.text = '{2D5ABB26-0587-4C30-8999-92F81FD0307C}'
        for j, wpx in enumerate(tb.col_w):
            tbl.columns[j].width = Emu(E(wpx))
        for i, hpx in enumerate(tb.row_h):
            tbl.rows[i].height = Emu(E(hpx))
        gf.width = Emu(E(sum(tb.col_w))); gf.height = Emu(E(sum(tb.row_h)))
        for i, row in enumerate(tb.rows):
            for j, content in enumerate(row):
                st = table_cell_style(tb, i, j)
                cell = tbl.cell(i, j)
                tc = cell._tc
                paras = to_paras(content)
                txb = parse_xml(f'<a:txBody xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:bodyPr/><a:lstStyle/>{paras_xml(paras, st, lang)}</a:txBody>')
                old = tc.find('{http://schemas.openxmlformats.org/drawingml/2006/main}txBody')
                tc.replace(old, txb)
                oldpr = tc.find('{http://schemas.openxmlformats.org/drawingml/2006/main}tcPr')
                if oldpr is not None:
                    tc.remove(oldpr)
                lnB = _ln(st.get('border_b'), st.get('border_w', 1)).replace('<a:ln', '<a:lnB').replace('</a:ln>', '</a:lnB>')
                lnT = _ln(st.get('border_t'), st.get('border_tw', 1)).replace('<a:ln', '<a:lnT').replace('</a:ln>', '</a:lnT>')
                none = lambda t: f'<a:{t} w="0"><a:noFill/></a:{t}>'
                anchor = {'t': 't', 'm': 'ctr', 'b': 'b'}[st.get('anchor', 'm')]
                pad = st.get('pad', (0, 24, 0, 0))  # l, r, t, b (px)
                tcpr = (f'<a:tcPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" marL="{E(pad[0])}" marR="{E(pad[1])}" '
                        f'marT="{E(pad[2])}" marB="{E(pad[3])}" anchor="{anchor}">{none("lnL")}{none("lnR")}{lnT}{lnB}'
                        f'{_fill(st.get("fill"))}</a:tcPr>')
                tc.append(parse_xml(tcpr))
        return gf

    def save(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self.prs.save(path)


def table_cell_style(tb, i, j):
    st = dict(tb.styles.get('cell', {}))
    if j == 0 and 'first' in tb.styles:
        st.update(tb.styles['first'])
    if j in tb.col_styles:
        st.update(tb.col_styles[j])
    if i == 0 and tb.header:
        st.update(tb.styles.get('head', {}))
        if j in tb.col_styles and 'head' in tb.col_styles[j]:
            st.update(tb.col_styles[j]['head'])
    if j in tb.col_fill:
        st['fill'] = tb.col_fill[j]
    if i == 0 and j in tb.col_top:
        st['border_t'] = tb.col_top[j]; st['border_tw'] = 3
    if i == len(tb.rows) - 1 and 'last_b' in tb.styles:
        st['border_b'] = tb.styles['last_b']
    return st


# ---------------------------------------------------------------- HTML
def css_font(st):
    f = FONTS[st.get('font', 'text')]
    return f"font-family:{f['css']},{CSS_FALLBACK[f['css']]};font-weight:{f['w']};"


def html_runs(p, base):
    out = ''
    for r in p.runs:
        st = run_style(base, p.st, r)
        s = css_font(st) + f"font-size:{st.get('size', 20) * 2:.1f}px;"
        if st.get('spc'):
            s += f"letter-spacing:{st['spc']}em;"
        if st.get('caps'):
            s += 'text-transform:uppercase;'
        if st.get('grad'):
            # SVG <text> con degradado: vectorial y sin costuras en PDF (background-clip:text deja filetes)
            fpx = st.get('size', 20) * 2
            wpx = text_width(r.text, st) + fpx * 0.08
            f = FONTS[st.get('font', 'text')]
            stops = ''.join(f'<stop offset="{i / (len(st["grad"]) - 1):.2f}" stop-color="{col_}"/>' for i, col_ in enumerate(st['grad']))
            gid = 'g' + hashlib.md5((r.text + str(fpx)).encode()).hexdigest()[:8]
            out += (f'<svg width="{wpx:.0f}" height="{fpx * 1.276:.0f}" style="display:inline-block;overflow:visible;vertical-align:{-fpx * 0.292:.1f}px">'
                    f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient></defs>'
                    f'<text x="0" y="{fpx * 0.984:.1f}" fill="url(#{gid})" style="font-family:{f["css"]};font-weight:{f["w"]};'
                    f'font-size:{fpx:.0f}px;letter-spacing:{st.get("spc", 0)}em">{esc(r.text)}</text></svg>')
            continue
        else:
            s += f"color:{st.get('color', '#000')};"
        txt = esc(r.text).replace('\v', '<br>')
        if st.get('link'):
            txt = f'<a href="{esc(st["link"])}" style="color:inherit;text-decoration:none">{txt}</a>'
        out += f'<span style="{s}">{txt}</span>'
    return out


def html_text(x, y, w, h, paras, base):
    jc = {'t': 'flex-start', 'm': 'center', 'b': 'flex-end'}[base.get('anchor', 't')]
    inner = ''
    for p in paras:
        pst = merged(base, p.st)
        size = pst.get('size', 20)
        lh = pst.get('lh', 1.2) * size * 2
        s = (f"margin:0 0 {pst.get('sa', 0) * 2}px 0;line-height:{lh:.1f}px;font-size:{size * 2:.1f}px;{css_font(pst)}"
             f"text-align:{ {'l': 'left', 'c': 'center', 'r': 'right'}[pst.get('align', 'l')] };")
        if pst.get('sb'):
            s += f"margin-top:{pst['sb'] * 2}px;"
        if pst.get('bullet'):
            ind = pst.get('indent', 32)
            bc = pst.get('bullet_color') or pst.get('color')
            s += f'padding-left:{ind}px;position:relative;'
            bul = (f'<span style="position:absolute;left:0;top:0;{css_font(dict(font="text"))}font-size:{size * 2}px;'
                   f'color:{bc}">{esc(pst["bullet"])}</span>')
        else:
            bul = ''
        body = html_runs(p, base) if any(r.text for r in p.runs) else '&nbsp;'
        inner += f'<p style="{s}">{bul}{body}</p>'
    return (f'<div class="t" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;justify-content:{jc}">{inner}</div>')


def html_el(el, rel):
    if el.kind == 'text':
        return html_text(el.x, el.y, el.w, el.h, el.paras, el.st)
    if el.kind == 'box':
        s = f'left:{el.x}px;top:{el.y}px;width:{el.w}px;height:{el.h}px;'
        if el.grad:
            s += f'background:linear-gradient(135deg,{",".join(el.grad)});'
        elif el.fill:
            s += f'background:{hex_rgba(el.fill, el.alpha)};'
        if el.line:
            s += f'box-shadow:inset 0 0 0 {el.lw}px {el.line};'
        if el.shape == 'ellipse':
            s += 'border-radius:50%;'
        elif el.r:
            s += f'border-radius:{el.r}px;'
        return f'<div class="b" style="{s}"></div>'
    if el.kind == 'line':
        x, y = min(el.x1, el.x2), min(el.y1, el.y2)
        w, h = abs(el.x2 - el.x1), abs(el.y2 - el.y1)
        if h == 0:
            st = f'left:{x}px;top:{y - el.w / 2}px;width:{w}px;height:0;border-top:{el.w}px {"dashed" if el.dash else "solid"} {el.color};'
        else:
            st = f'left:{x - el.w / 2}px;top:{y}px;width:0;height:{h}px;border-left:{el.w}px {"dashed" if el.dash else "solid"} {el.color};'
        return f'<div class="b" style="{st}"></div>'
    if el.kind == 'img':
        return f'<img class="b" src="{rel(el.path)}" style="left:{el.x}px;top:{el.y}px;width:{el.w}px;height:{el.h}px" alt="{esc(el.descr)}">'
    raise ValueError(el.kind)


def hex_rgba(c, a=None):
    c = c.lstrip('#')
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return f'rgba({r},{g},{b},{a if a is not None else 1})'


def html_chart(ch, x, y, w, h, c):
    pad_l, pad_b, pad_t = 64, 48, 24
    pw, ph_ = w - pad_l, h - pad_b - pad_t
    n = len(ch.categories)
    vmax = ch.y_max or max(max(v) for _, v, _ in ch.series) * 1.15
    unit = ch.y_unit or vmax / 4
    svg = [f'<svg class="b" style="left:{x}px;top:{y}px" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    mono = "font-family:'JetBrains Mono',Consolas,monospace;font-size:28px"
    v = 0
    while v <= vmax + 1e-9:
        yy = pad_t + ph_ * (1 - v / vmax)
        svg.append(f'<line x1="{pad_l}" x2="{w}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="{c["border"]}" stroke-width="1.5"/>')
        svg.append(f'<text x="{pad_l - 16}" y="{yy + 9:.1f}" text-anchor="end" style="{mono}" fill="{c["text3"]}">{fmt_num(v, ch.fmt)}</text>')
        v += unit
    slot = pw / n
    ns = len(ch.series)
    for si, (name, vals, color) in enumerate(ch.series):
        pts = []
        for i, val in enumerate(vals):
            col = ch.point_colors.get((si, i), color)
            cx = pad_l + slot * (i + 0.5)
            yy = pad_t + ph_ * (1 - val / vmax)
            if ch.kind == 'bar':
                gw = slot / (1 + ch.gap / 100)
                bw = gw / ns
                bx = pad_l + slot * i + (slot - gw) / 2 + bw * si
                svg.append(f'<rect x="{bx:.1f}" y="{yy:.1f}" width="{bw:.1f}" height="{pad_t + ph_ - yy:.1f}" fill="{col}"/>')
                lx = bx + bw / 2
            else:
                pts.append((cx, yy, col))
                lx = cx
            if ch.labels:
                svg.append(f'<text x="{lx:.1f}" y="{yy - 14:.1f}" text-anchor="middle" style="{mono}" fill="{ch.label_color or c["text2"]}">{fmt_num(val, ch.label_fmt)}</text>')
        if pts:
            svg.append(f'<polyline fill="none" stroke="{color}" stroke-width="4.5" points="{" ".join(f"{a:.1f},{b:.1f}" for a, b, _ in pts)}"/>')
            for a, b, col in pts:
                r = 11 if col != color else 7
                svg.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r}" fill="{col}"/>')
    svg.append(f'<line x1="{pad_l}" x2="{w}" y1="{pad_t + ph_}" y2="{pad_t + ph_}" stroke="{c["border"]}" stroke-width="1.5"/>')
    for i, cat in enumerate(ch.categories):
        cx = pad_l + slot * (i + 0.5)
        svg.append(f'<text x="{cx:.1f}" y="{h - 8}" text-anchor="middle" style="{mono}" fill="{c["text3"]}">{esc(str(cat))}</text>')
    svg.append('</svg>')
    return ''.join(svg)


def fmt_num(v, fmt):
    suffix = ''
    m = re.match(r'^([#0.,]+)(.*)$', fmt.replace('"', ''))
    if m:
        core, suffix = m.group(1), m.group(2)
    else:
        core = fmt
    dec = len(core.split('.')[1]) if '.' in core else 0
    s = f'{v:,.{dec}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return s + suffix.replace('\\', '')


def html_table(tb, x, y):
    out = ''
    yy = y
    for i, row in enumerate(tb.rows):
        xx = x
        for j, content in enumerate(row):
            st = table_cell_style(tb, i, j)
            w, h = tb.col_w[j], tb.row_h[i]
            s = f'left:{xx}px;top:{yy}px;width:{w}px;height:{h}px;'
            if st.get('fill'):
                s += f'background:{st["fill"]};'
            if st.get('border_b'):
                s += f'box-shadow:inset 0 -{st.get("border_w", 1)}px 0 {st["border_b"]};'
            if st.get('border_t'):
                s += f'border-top:{st.get("border_tw", 1)}px solid {st["border_t"]};box-sizing:border-box;'
            out += f'<div class="b" style="{s}"></div>'
            pad = st.get('pad', (0, 24, 0, 0))
            out += html_text(xx + pad[0], yy + pad[2], w - pad[0] - pad[1], h - pad[2] - pad[3], to_paras(content), dict(st, anchor=st.get('anchor', 'm')))
            xx += w
        yy += tb.row_h[i]
    return out


def html_slide(S, theme, rel, number):
    L = S.layout
    c = theme.c
    parts = [html_el(e, rel) for e in L.statics]
    under_done = False
    for p in L.phs:
        key = 0 if p.kind == 'title' else p.idx
        content = S.fill.get(key, S.fill.get(p.idx))
        if content is None:
            continue
        if p.kind in ('title', 'body'):
            if isinstance(content, dict):
                extra = {k: v for k, v in content.items() if k != 'text'}
                paras = to_paras(content['text'])
                base = merged(p.st, extra)
            else:
                paras, base = to_paras(content), p.st
            parts.append(html_text(p.x, p.y, p.w, p.h, paras, base))
        elif p.kind == 'pic':
            r = p.st.get('r', 0)
            parts.append(f'<img class="b" src="{rel(content)}" style="left:{p.x}px;top:{p.y}px;width:{p.w}px;height:{p.h}px;object-fit:cover;border-radius:{r}px">')
            parts += [html_el(e, rel) for e in S.under]
            under_done = True
        elif p.kind == 'chart':
            parts.append(html_chart(content, p.x, p.y, p.w, p.h, c))
        elif p.kind == 'tbl':
            parts.append(html_table(content, p.x, p.y))
    if not under_done:
        parts = parts[:len(L.statics)] + [html_el(e, rel) for e in S.under] + parts[len(L.statics):]
    parts += [html_el(e, rel) for e in S.extras]
    if L.footer:
        txt = S.footer if S.footer is not None else theme.footer_text
        parts.append(html_text(164, FOOTER_Y, 1000, FOOTER_H, [P(txt)], dict(theme.footer_style, anchor='m')))
    if L.number:
        parts.append(html_text(1640, FOOTER_Y, 160, FOOTER_H, [P(str(number))], dict(theme.number_style, anchor='m')))
    bg = L.bg or c['bg']
    return f'<section class="slide" style="background:{bg}">{"".join(parts)}</section>'


def html_deck(slides, theme, out_html, brand_css_rel, title):
    base = os.path.dirname(os.path.abspath(out_html))

    def rel(p):
        return os.path.relpath(os.path.abspath(p), base).replace('\\', '/')
    body = ''.join(html_slide(S, theme, rel, i + 1) for i, S in enumerate(slides))
    doc = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{esc(title)}</title>
<link rel="stylesheet" href="{brand_css_rel}">
<style>
@page {{ size: 1920px 1080px; margin: 0 }}
html,body {{ margin:0; padding:0; background:#0B0D12 }}
.slide {{ position:relative; width:1920px; height:1080px; overflow:hidden; page-break-after:always; break-after:page }}
.slide:last-child {{ page-break-after:auto; break-after:auto }}
.b {{ position:absolute; display:block }}
.t {{ position:absolute; display:flex; flex-direction:column; overflow:visible; -webkit-font-smoothing:antialiased;
      font-kerning:normal; text-rendering:geometricPrecision }}
.t p {{ white-space:pre-wrap; overflow-wrap:break-word }}
@media screen {{ body {{ background:#05060A }} .slide {{ margin:0 auto 24px }} }}
</style></head><body>{body}</body></html>'''
    open(out_html, 'w', encoding='utf8').write(doc)
    return out_html


# ---------------------------------------------------------------- QA de texto
def qa_fit(slides, label=''):
    """Avisa de textos que probablemente desbordan su caja (medición con métricas reales de la fuente)."""
    warnings = []

    def check(where, x, y, w, h, paras, base):
        total = 0
        for p in paras:
            pst = merged(base, p.st)
            lh = pst.get('lh', 1.2) * pst.get('size', 20) * 2
            # reparto en líneas (greedy)
            text_runs = [(r.text, run_style(base, p.st, r)) for r in p.runs]
            full = ''.join(t for t, _ in text_runs)
            st0 = text_runs[0][1] if text_runs else pst
            avail = w - (pst.get('indent', 32) if pst.get('bullet') else 0)
            lines = 0
            for seg in full.split('\v'):
                words = seg.split(' ')
                cur = ''
                n = 1
                for wd in words:
                    cand = (cur + ' ' + wd) if cur else wd
                    if text_width(cand, st0) > avail + 1 and cur:
                        n += 1; cur = wd
                        if text_width(wd, st0) > avail + 1:
                            warnings.append(f'{label} {where}: palabra más ancha que la caja «{wd}»')
                    else:
                        cur = cand
                lines += n
            total += lines * lh + pst.get('sa', 0) * 2
        if total > h + 4:
            warnings.append(f'{label} {where}: alto {total:.0f}px > caja {h}px · «{"".join(r.text for r in paras[0].runs)[:40]}»')

    for si, S in enumerate(slides):
        L = S.layout
        for p in L.phs:
            if p.kind not in ('title', 'body'):
                continue
            key = 0 if p.kind == 'title' else p.idx
            content = S.fill.get(key, S.fill.get(p.idx))
            if content is None:
                continue
            if isinstance(content, dict):
                paras = to_paras(content['text']); base = merged(p.st, {k: v for k, v in content.items() if k != 'text'})
            else:
                paras, base = to_paras(content), p.st
            check(f'#{si + 1} {L.name} ph{p.idx}', p.x, p.y, p.w, p.h, paras, base)
        for e in S.extras + L.statics:
            if getattr(e, 'kind', '') == 'text':
                check(f'#{si + 1} {L.name} {e.name}', e.x, e.y, e.w, e.h, e.paras, e.st)
    for w_ in warnings:
        print('  [QA]', w_)
    return warnings
