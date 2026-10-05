"""
Oryzz · librería para plantillas Word (.docx) v2.0

- Estilos con nombre: Título, Subtítulo, Título 1-3 (alias «Encabezado 1-3»), Cuerpo, Entradilla,
  Cita, Eyebrow, Nota, Dato, Campo, Acento, Aviso legal, Línea de respuesta y el estilo de tabla «Tabla Oryzz».
- Tema de Office «Oryzz» (colores y fuentes del tema).
- Fuentes de marca incrustadas (Space Grotesk, Space Grotesk Medium, Manrope, JetBrains Mono)
  con Arial como alternativa declarada en la tabla de fuentes.
- Encabezado con logo + etiqueta, pie con oryzz.com y folio «01 / 08».

Marcado en línea para los textos:  **negrita**  {{campo editable}}  [[acento azul]]
"""
import os, re, uuid, zipfile, shutil, tempfile
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.shared import Mm, Pt, RGBColor, Emu

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.normpath(os.path.join(HERE, '..', 'fonts', 'static'))
RES = os.path.normpath(os.path.join(HERE, '..', '..', '07_Documentos', '_fuente', 'recursos_docx'))

# ---------------------------------------------------------------- paleta
G950, G850, G700, G600, G500, G400, G300, G200, G100, G50 = (
    '0B0D12', '12151D', '232836', '3A4152', '5A6172', '8A90A0', 'C7CBD6', 'D5D9E0', 'E5E8EE', 'F6F7F9')
AZ500, AZ600, AZ400, AZ50 = '3B72FF', '2C5BD0', '5C8BFF', 'EEF3FF'
CY600, LI600, LI500 = '17A9C2', '7FB02E', 'BFF24A'
AVISO_TXT, AVISO_BG = '8A5200', 'FFF6E8'

DISPLAY, DISPLAY_MED, TEXTO, MONO = 'Space Grotesk', 'Space Grotesk Medium', 'Manrope', 'JetBrains Mono'


# ---------------------------------------------------------------- utilidades XML
def _set_fonts(rpr, name):
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.insert(0, rf)
    for a in list(rf.attrib):
        del rf.attrib[a]
    for a in ('ascii', 'hAnsi', 'cs', 'eastAsia'):
        rf.set(qn(f'w:{a}'), name)


def _set_color(rpr, hexc):
    for c in rpr.findall(qn('w:color')):
        rpr.remove(c)
    c = OxmlElement('w:color'); c.set(qn('w:val'), hexc); rpr.append(c)


def _rpr_el(style):
    return style.element.get_or_add_rPr()


def _spacing_chars(rpr, twips):
    for c in rpr.findall(qn('w:spacing')):
        rpr.remove(c)
    s = OxmlElement('w:spacing'); s.set(qn('w:val'), str(twips)); rpr.append(s)


def _shade(el_pr, fill):
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), fill)
    el_pr.append(sh)


def _pborder(ppr, side, sz=4, color=G100, space=4):
    b = ppr.find(qn('w:pBdr'))
    if b is None:
        b = OxmlElement('w:pBdr'); ppr.append(b)
    e = OxmlElement(f'w:{side}')
    e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz)); e.set(qn('w:space'), str(space)); e.set(qn('w:color'), color)
    b.append(e)


def style_font(style, name, size=None, color=None, bold=None, caps=None, tracking=None):
    rpr = _rpr_el(style)
    _set_fonts(rpr, name)
    f = style.font
    if size: f.size = Pt(size)
    if bold is not None: f.bold = bold
    if caps is not None: f.all_caps = caps
    f.italic = False
    if color: _set_color(rpr, color)
    if tracking is not None: _spacing_chars(rpr, tracking)


def style_par(style, before=0, after=6, line=1.35, keep_next=False, align=None):
    pf = style.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    pf.line_spacing = line
    pf.keep_with_next = keep_next
    if align is not None: pf.alignment = align


def _alias(style, alias):
    el = style.element
    for a in el.findall(qn('w:aliases')):
        el.remove(a)
    a = OxmlElement('w:aliases'); a.set(qn('w:val'), alias)
    el.find(qn('w:name')).addnext(a)


# ---------------------------------------------------------------- estilos
def setup_styles(doc):
    st = doc.styles
    # docDefaults
    rpr_def = doc.styles.element.find(qn('w:docDefaults')).find(qn('w:rPrDefault')).find(qn('w:rPr'))
    _set_fonts(rpr_def, TEXTO)
    for l in rpr_def.findall(qn('w:lang')):
        rpr_def.remove(l)
    lang = OxmlElement('w:lang'); lang.set(qn('w:val'), 'es-ES'); lang.set(qn('w:eastAsia'), 'es-ES'); lang.set(qn('w:bidi'), 'ar-SA'); rpr_def.append(lang)

    normal = st['Normal']
    style_font(normal, TEXTO, 9.5, G950); style_par(normal, 0, 6, 1.35)

    def para(name, base='Normal'):
        try:
            s = st[name]
        except KeyError:
            s = st.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = st[base] if base else None
        s.quick_style = True
        return s

    def char(name):
        try:
            return st[name]
        except KeyError:
            s = st.add_style(name, WD_STYLE_TYPE.CHARACTER); s.quick_style = True; return s

    cuerpo = para('Cuerpo'); style_font(cuerpo, TEXTO, 9.5, G950); style_par(cuerpo, 0, 6, 1.35)

    t = para('Title'); style_font(t, DISPLAY, 34, G950, bold=True, tracking=-24); style_par(t, 0, 14, 1.0)
    for b in t.element.pPr.findall(qn('w:pBdr')) if t.element.pPr is not None else []:
        t.element.pPr.remove(b)
    sub = para('Subtitle'); style_font(sub, TEXTO, 12.5, G600, tracking=0); style_par(sub, 0, 10, 1.4)
    h1 = para('Heading 1'); style_font(h1, DISPLAY, 22, G950, bold=True, tracking=-12); style_par(h1, 4, 12, 1.05, True)
    h2 = para('Heading 2'); style_font(h2, DISPLAY, 14, G950, bold=True, tracking=-5); style_par(h2, 16, 6, 1.15, True)
    h3 = para('Heading 3'); style_font(h3, DISPLAY, 11, G950, bold=True, tracking=-2); style_par(h3, 10, 3, 1.2, True)
    for s, a in ((h1, 'Encabezado 1'), (h2, 'Encabezado 2'), (h3, 'Encabezado 3')):
        _alias(s, a)
        s.element.get_or_add_pPr()
    q = para('Quote'); style_font(q, DISPLAY_MED, 14, G950, tracking=-3); style_par(q, 12, 12, 1.25)
    q.paragraph_format.left_indent = Mm(6)
    _pborder(q.element.get_or_add_pPr(), 'left', 18, AZ500, 14)
    _alias(q, 'Cita')

    ey = para('Eyebrow'); style_font(ey, MONO, 9, G500, caps=True, tracking=29); style_par(ey, 0, 8, 1.1, True)
    lead = para('Entradilla'); style_font(lead, TEXTO, 12, G600); style_par(lead, 0, 14, 1.4)
    nota = para('Nota'); style_font(nota, TEXTO, 9, G500); style_par(nota, 0, 4, 1.35)
    dato = para('Dato'); style_font(dato, DISPLAY_MED, 26, G950, tracking=-15); style_par(dato, 0, 2, 1.0)
    aviso = para('Aviso legal'); style_font(aviso, MONO, 9, AVISO_TXT, tracking=6); style_par(aviso, 0, 4, 1.2, True)
    _shade(aviso.element.get_or_add_pPr(), AVISO_BG)
    resp = para('Línea de respuesta'); style_font(resp, TEXTO, 9.5, G950); style_par(resp, 0, 0, 1.0)
    resp.paragraph_format.left_indent = Mm(9); resp.paragraph_format.space_before = Pt(14)
    _pborder(resp.element.get_or_add_pPr(), 'bottom', 4, G200, 2)
    tabla_txt = para('Texto de tabla'); style_font(tabla_txt, TEXTO, 9.5, G950); style_par(tabla_txt, 0, 0, 1.25)
    tabla_cab = para('Cabecera de tabla', 'Texto de tabla'); style_font(tabla_cab, MONO, 9, G500, caps=True, tracking=14)
    pie = para('Pie Oryzz'); style_font(pie, MONO, 9, G500, tracking=2); style_par(pie, 0, 0, 1.0)

    # listas
    for nm, alias in (('List Bullet', 'Lista Oryzz'), ('List Number', 'Lista numerada Oryzz')):
        try:
            ls = st[nm]; style_font(ls, TEXTO, 9.5, G950); style_par(ls, 0, 3, 1.35); _alias(ls, alias)
        except KeyError:
            pass

    campo = char('Campo'); _set_color(_rpr_el(campo), AZ500)
    acento = char('Acento'); _set_color(_rpr_el(acento), AZ500)
    negr = char('Destacado'); negr.font.bold = True

    # hipervínculo
    try:
        hl = st['Hyperlink']; _set_color(_rpr_el(hl), AZ600); hl.font.underline = False
    except KeyError:
        pass
    # estilos de carácter vinculados («Título 1 Car», etc.): misma fuente y color que su párrafo
    for base in ('Title', 'Subtitle', 'Heading 1', 'Heading 2', 'Heading 3', 'Quote'):
        try:
            ch = st[base + ' Char']
        except KeyError:
            continue
        src = st[base]
        fam = _rpr_el(src).find(qn('w:rFonts')).get(qn('w:ascii'))
        col = _rpr_el(src).find(qn('w:color'))
        style_font(ch, fam, src.font.size.pt if src.font.size else None, col.get(qn('w:val')) if col is not None else None,
                   bold=src.font.bold)
    _tabla_oryzz(doc)


def _tabla_oryzz(doc):
    styles = doc.styles.element
    if styles.find(f".//{qn('w:style')}[@{qn('w:styleId')}='TablaOryzz']") is not None:
        return
    xml = f'''<w:style {nsdecls("w")} w:type="table" w:customStyle="1" w:styleId="TablaOryzz">
  <w:name w:val="Tabla Oryzz"/><w:basedOn w:val="TableNormal"/><w:uiPriority w:val="40"/><w:qFormat/>
  <w:pPr><w:spacing w:before="0" w:after="0" w:line="300" w:lineRule="auto"/></w:pPr>
  <w:rPr><w:rFonts w:ascii="{TEXTO}" w:hAnsi="{TEXTO}" w:cs="{TEXTO}" w:eastAsia="{TEXTO}"/><w:color w:val="{G950}"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
  <w:tblPr><w:tblStyleRowBandSize w:val="1"/><w:tblStyleColBandSize w:val="1"/>
    <w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="{G100}"/><w:right w:val="nil"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="{G100}"/><w:insideV w:val="nil"/></w:tblBorders>
    <w:tblCellMar><w:top w:w="110" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:bottom w:w="110" w:type="dxa"/><w:right w:w="170" w:type="dxa"/></w:tblCellMar></w:tblPr>
  <w:tblStylePr w:type="firstRow"><w:pPr><w:keepNext/></w:pPr><w:rPr><w:rFonts w:ascii="{MONO}" w:hAnsi="{MONO}" w:cs="{MONO}" w:eastAsia="{MONO}"/><w:color w:val="{G500}"/><w:spacing w:val="14"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
    <w:tblPr/><w:trPr><w:tblHeader/></w:trPr><w:tcPr><w:tcBorders><w:bottom w:val="single" w:sz="8" w:space="0" w:color="{G950}"/></w:tcBorders><w:vAlign w:val="bottom"/></w:tcPr></w:tblStylePr>
  <w:tblStylePr w:type="lastRow"><w:rPr><w:rFonts w:ascii="{DISPLAY}" w:hAnsi="{DISPLAY}" w:cs="{DISPLAY}" w:eastAsia="{DISPLAY}"/><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
    <w:tblPr/><w:tcPr><w:tcBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="{G950}"/><w:bottom w:val="nil"/></w:tcBorders></w:tcPr></w:tblStylePr>
</w:style>'''
    styles.append(parse_xml(xml))
    # tabla sin bordes para maquetar
    xml2 = f'''<w:style {nsdecls("w")} w:type="table" w:customStyle="1" w:styleId="MaquetaOryzz">
  <w:name w:val="Maqueta Oryzz (sin bordes)"/><w:basedOn w:val="TableNormal"/><w:uiPriority w:val="41"/>
  <w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr>
  <w:tblPr><w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>
  <w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="284" w:type="dxa"/></w:tblCellMar></w:tblPr>
</w:style>'''
    styles.append(parse_xml(xml2))


# ---------------------------------------------------------------- texto con marcado
_TOK = re.compile(r'(\*\*.+?\*\*|\{\{.+?\}\}|\[\[.+?\]\])')


def add_text(p, text, color=None, size=None, bold=None, font=None):
    for part in _TOK.split(text):
        if not part:
            continue
        if part.startswith('**'):
            r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith('{{'):
            r = p.add_run(part); r.style = p.part.document.styles['Campo']
        elif part.startswith('[['):
            r = p.add_run(part[2:-2]); r.style = p.part.document.styles['Acento']
        else:
            r = p.add_run(part)
        if color and not part.startswith(('{{', '[[')): r.font.color.rgb = RGBColor.from_string(color)
        if size: r.font.size = Pt(size)
        if bold is not None and not part.startswith('**'): r.bold = bold
        if font: _set_fonts(r._r.get_or_add_rPr(), font)
    return p


def P(doc_or_cell, text='', style='Cuerpo', **kw):
    p = doc_or_cell.add_paragraph(style=style)
    if text:
        add_text(p, text, **kw)
    return p


# ---------------------------------------------------------------- imágenes
def anchor_image(run, path, w_mm, h_mm, x_mm=0, y_mm=0, behind=True, rel='page'):
    run.add_picture(path, width=Mm(w_mm), height=Mm(h_mm))
    inline = run._r.xpath('.//wp:inline')[-1]
    graphic = inline.find(qn('a:graphic'))
    docpr = inline.find(qn('wp:docPr'))
    cx, cy = Mm(w_mm), Mm(h_mm)
    anchor = parse_xml(
        f'<wp:anchor {nsdecls("wp", "a", "r")} distT="0" distB="0" distL="0" distR="0" simplePos="0" '
        f'relativeHeight="{1 if behind else 251659264}" behindDoc="{1 if behind else 0}" locked="1" layoutInCell="1" allowOverlap="1">'
        f'<wp:simplePos x="0" y="0"/>'
        f'<wp:positionH relativeFrom="{rel}"><wp:posOffset>{int(Mm(x_mm))}</wp:posOffset></wp:positionH>'
        f'<wp:positionV relativeFrom="{rel}"><wp:posOffset>{int(Mm(y_mm))}</wp:posOffset></wp:positionV>'
        f'<wp:extent cx="{int(cx)}" cy="{int(cy)}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
        f'<wp:docPr id="{docpr.get("id")}" name="{docpr.get("name")}" descr="Recurso gráfico Oryzz"/><wp:cNvGraphicFramePr/></wp:anchor>')
    anchor.append(graphic)
    inline.getparent().replace(inline, anchor)


def res(name):
    return os.path.join(RES, name)


# ---------------------------------------------------------------- página y secciones
def new_doc():
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Mm(210), Mm(297)
    s.left_margin = s.right_margin = Mm(20)
    s.top_margin, s.bottom_margin = Mm(30), Mm(24)
    s.header_distance, s.footer_distance = Mm(11), Mm(11)
    setup_styles(doc)
    doc.core_properties.author = 'Oryzz'
    doc.core_properties.language = 'es-ES'
    # borra el párrafo vacío inicial
    body = doc.element.body
    for p in body.findall(qn('w:p')):
        body.remove(p)
    return doc


def _tab_right(p, pos_mm=170):
    tabs = p.paragraph_format.tab_stops
    from docx.enum.text import WD_TAB_ALIGNMENT
    tabs.add_tab_stop(Mm(pos_mm), WD_TAB_ALIGNMENT.RIGHT)


def _field(p, instr, placeholder='1'):
    r1 = p.add_run(); fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), 'begin'); r1._r.append(fc)
    r2 = p.add_run(); it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = f' {instr} '; r2._r.append(it)
    r3 = p.add_run(); fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), 'separate'); r3._r.append(fc)
    r4 = p.add_run(placeholder)
    r5 = p.add_run(); fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), 'end'); r5._r.append(fc)
    for r in (r4,):
        r.font.color.rgb = RGBColor.from_string(G950)


def running_header(section, label, pie='oryzz.com', logo='logo-horizontal-claro.png', folio=True):
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False
    h = section.header
    p = h.paragraphs[0]; p.text = ''
    p.style = section.part.document.styles['Pie Oryzz']
    p.paragraph_format.space_after = Pt(0)
    _tab_right(p)
    r = p.add_run(); r.add_picture(res(logo), width=Mm(24))
    r = p.add_run('\t' + label)
    r.font.name = MONO; _set_fonts(r._r.get_or_add_rPr(), MONO); r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string(G500)
    _pborder(p._p.get_or_add_pPr(), 'bottom', 4, G100, 8)
    f = section.footer
    fp = f.paragraphs[0]; fp.text = ''
    fp.style = section.part.document.styles['Pie Oryzz']
    _tab_right(fp)
    fp.add_run(pie)
    if folio:
        fp.add_run('\t')
        _field(fp, 'PAGE \\# "00"', '01')
        r = fp.add_run(' / ')
        _field(fp, 'NUMPAGES \\# "00"', '01')


def new_section(doc):
    return doc.add_section(WD_SECTION.NEW_PAGE)


# ---------------------------------------------------------------- bloques
def eyebrow(doc, text, n=None, color=None):
    p = doc.add_paragraph(style='Eyebrow')
    if n:
        r = p.add_run(n + '   '); r.font.color.rgb = RGBColor.from_string(color or AZ600)
    add_text(p, text)
    return p


def h(doc, text, level=1):
    p = doc.add_paragraph(style=f'Heading {level}')
    add_text(p, text); return p


def bullets(doc, items, numbered=False):
    for it in items:
        P(doc, it, 'List Number' if numbered else 'List Bullet')


def _cell_shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr(); _shade(tcpr, fill)


def _cell_margins(cell, top=0, left=0, bottom=0, right=0):
    tcpr = cell._tc.get_or_add_tcPr()
    m = OxmlElement('w:tcMar')
    for side, v in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        e = OxmlElement(f'w:{side}'); e.set(qn('w:w'), str(int(v * 56.7))); e.set(qn('w:type'), 'dxa'); m.append(e)
    tcpr.append(m)


def _tbl_look(table, first=True, last=False):
    tblpr = table._tbl.tblPr
    for l in tblpr.findall(qn('w:tblLook')):
        tblpr.remove(l)
    lk = OxmlElement('w:tblLook')
    lk.set(qn('w:val'), '0000'); lk.set(qn('w:firstRow'), '1' if first else '0'); lk.set(qn('w:lastRow'), '1' if last else '0')
    lk.set(qn('w:firstColumn'), '0'); lk.set(qn('w:lastColumn'), '0'); lk.set(qn('w:noHBand'), '1'); lk.set(qn('w:noVBand'), '1')
    tblpr.append(lk)


def _widths(table, widths_mm):
    table.autofit = False
    tblpr = table._tbl.tblPr
    w = tblpr.find(qn('w:tblW'))
    if w is None:
        w = OxmlElement('w:tblW'); tblpr.append(w)
    w.set(qn('w:w'), str(int(sum(widths_mm) * 56.7))); w.set(qn('w:type'), 'dxa')
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblpr.append(lay)
    grid = table._tbl.tblGrid
    for i, gc in enumerate(grid.findall(qn('w:gridCol'))):
        gc.set(qn('w:w'), str(int(widths_mm[i] * 56.7)))
    for row in table.rows:
        for i, c in enumerate(row.cells):
            c.width = Mm(widths_mm[i])


def tabla(doc, header, rows, widths=None, total=False, right_cols=(), detail_sep=' | '):
    """rows: listas de celdas. Una celda 'Título | detalle' pone el detalle en gris debajo."""
    n = len(header)
    t = doc.add_table(rows=1 + len(rows), cols=n)
    t.style = doc.styles['Tabla Oryzz']
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    _tbl_look(t, True, total)
    widths = widths or [170 / n] * n
    for i, htxt in enumerate(header):
        c = t.rows[0].cells[i]; c.paragraphs[0].style = doc.styles['Cabecera de tabla']
        add_text(c.paragraphs[0], htxt)
        if i in right_cols: c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for ri, row in enumerate(rows, start=1):
        for i, val in enumerate(row):
            c = t.rows[ri].cells[i]; p = c.paragraphs[0]; p.style = doc.styles['Texto de tabla']
            main, _, det = str(val).partition(detail_sep)
            add_text(p, main)
            if det:
                p2 = c.add_paragraph(style='Texto de tabla'); add_text(p2, det, color=G500, size=9)
            if i in right_cols:
                for pp in c.paragraphs: pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _widths(t, widths)
    P(doc, '', 'Nota').paragraph_format.space_after = Pt(4)
    return t


def maqueta(doc, n_cols, widths=None):
    t = doc.add_table(rows=1, cols=n_cols)
    t.style = doc.styles['Maqueta Oryzz (sin bordes)']
    _tbl_look(t, False, False)
    _widths(t, widths or [170 / n_cols] * n_cols)
    for c in t.rows[0].cells:
        c.paragraphs[0].style = doc.styles['Cuerpo']
    return t


def datos(doc, items, fill=G50, dark=False):
    """Tarjetas dato: [(eyebrow, cifra, unidad, delta)]"""
    n = len(items)
    gap = 5
    w = (170 - gap * (n - 1)) / n
    widths = []
    for i in range(n):
        widths.append(w);
        if i < n - 1: widths.append(gap)
    t = doc.add_table(rows=1, cols=len(widths))
    t.style = doc.styles['Maqueta Oryzz (sin bordes)']; _tbl_look(t, False, False)
    _widths(t, widths)
    for i, (ey, cifra, unidad, delta) in enumerate(items):
        c = t.rows[0].cells[i * 2]
        _cell_shade(c, G850 if dark else fill); _cell_margins(c, 4.5, 5, 4.5, 4)
        p = c.paragraphs[0]; p.style = doc.styles['Eyebrow']; add_text(p, ey, color=G400 if dark else None)
        p = c.add_paragraph(style='Dato'); r = p.add_run(cifra)
        if dark: r.font.color.rgb = RGBColor.from_string('FFFFFF')
        if unidad:
            r = p.add_run(' ' + unidad); r.font.size = Pt(12); r.font.color.rgb = RGBColor.from_string(G400 if dark else G600)
        p = c.add_paragraph(style='Nota'); p.paragraph_format.space_before = Pt(6)
        r = p.add_run('●  '); r.font.color.rgb = RGBColor.from_string(LI500 if dark else LI600); r.font.size = Pt(8)
        add_text(p, delta, color=G200 if dark else G600)
    P(doc, '', 'Nota')
    return t


def nota(doc, titulo, texto, fill=G50):
    t = doc.add_table(rows=1, cols=1)
    t.style = doc.styles['Maqueta Oryzz (sin bordes)']; _tbl_look(t, False, False); _widths(t, [170])
    c = t.rows[0].cells[0]; _cell_shade(c, fill); _cell_margins(c, 5, 6, 5, 6)
    p = c.paragraphs[0]; p.style = doc.styles['Eyebrow']; add_text(p, titulo)
    p = c.add_paragraph(style='Cuerpo'); add_text(p, texto); p.paragraph_format.space_after = Pt(0)
    P(doc, '', 'Nota')
    return t


def cita(doc, texto, fuente=None):
    P(doc, texto, 'Quote')
    if fuente:
        p = P(doc, fuente, 'Eyebrow'); p.paragraph_format.left_indent = Mm(6)


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def firma(doc, etiquetas):
    n = len(etiquetas)
    t = maqueta(doc, n)
    for i, (ey, pie) in enumerate(etiquetas):
        c = t.rows[0].cells[i]
        p = c.paragraphs[0]; p.style = doc.styles['Eyebrow']; add_text(p, ey)
        p = c.add_paragraph(style='Línea de respuesta'); p.paragraph_format.left_indent = Mm(0); p.paragraph_format.space_before = Pt(40)
        p = c.add_paragraph(style='Nota'); p.paragraph_format.space_before = Pt(4); add_text(p, pie)
    return t


# ---------------------------------------------------------------- portada
def portada(doc, tipo, titulo, lead, meta, oscura=True, etiqueta=None):
    """Primera sección (sin encabezado). meta: [(eyebrow, valor)] (máx. 4)."""
    s = doc.sections[0]
    s.top_margin = Mm(20); s.bottom_margin = Mm(20)
    s.different_first_page_header_footer = False
    blanco = 'FFFFFF' if oscura else G950
    p = doc.add_paragraph(style='Cuerpo'); p.paragraph_format.space_after = Pt(0)
    anchor_image(p.add_run(), res('portada-oscura.png' if oscura else 'portada-clara.png'), 210, 297)
    p.add_run().add_picture(res('logo-horizontal-oscuro.png' if oscura else 'logo-horizontal-claro.png'), width=Mm(34))
    if etiqueta:
        _tab_right(p); r = p.add_run('\t' + etiqueta.upper())
        _set_fonts(r._r.get_or_add_rPr(), MONO); r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string(G400 if oscura else AVISO_TXT)
    p = doc.add_paragraph(style='Eyebrow'); p.paragraph_format.space_before = Pt(262)
    add_text(p, tipo, color=G400 if oscura else G500)
    p = doc.add_paragraph(style='Title'); add_text(p, titulo, color=blanco)
    p.paragraph_format.right_indent = Mm(20)
    p = doc.add_paragraph(style='Subtitle'); add_text(p, lead, color=G200 if oscura else G600)
    p.paragraph_format.right_indent = Mm(52)
    # ficha inferior: tabla flotante anclada a la página
    t = doc.add_table(rows=1, cols=len(meta))
    t.style = doc.styles['Maqueta Oryzz (sin bordes)']; _tbl_look(t, False, False)
    ws = {4: [52, 34, 22, 62], 3: [60, 50, 60], 2: [85, 85]}[len(meta)]
    _widths(t, ws)
    tblpr = t._tbl.tblPr
    pos = parse_xml(f'<w:tblpPr {nsdecls("w")} w:leftFromText="0" w:rightFromText="0" w:vertAnchor="page" w:horzAnchor="margin" w:tblpY="{int(250 * 56.7)}"/>')
    tblpr.insert(1, pos)
    for i, (ey, val) in enumerate(meta):
        c = t.rows[0].cells[i]
        tcpr = c._tc.get_or_add_tcPr()
        b = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="{G700 if oscura else G200}"/></w:tcBorders>')
        tcpr.append(b); _cell_margins(c, 4, 0, 0, 3)
        p = c.paragraphs[0]; p.style = doc.styles['Eyebrow']; p.paragraph_format.space_after = Pt(3)
        add_text(p, ey, color=G400 if oscura else G500)
        p = c.add_paragraph(style='Cuerpo'); add_text(p, val, color=blanco, size=10)
    s2 = new_section(doc)
    s2.top_margin, s2.bottom_margin = Mm(30), Mm(24)
    return s2


# ---------------------------------------------------------------- posproceso: tema, fuentes, incrustación
THEME_COLORS = dict(dk1=G950, lt1='FFFFFF', dk2=G700, lt2=G50, accent1=AZ500, accent2=CY600, accent3=LI600,
                    accent4=G500, accent5=AZ600, accent6=G400, hlink=AZ600, folHlink='1F43A0')

EMBED = [  # (familia en Word, regular, negrita)
    (DISPLAY, 'SpaceGrotesk-Regular.ttf', 'SpaceGrotesk-Bold.ttf'),
    (DISPLAY_MED, 'SpaceGrotesk-Medium.ttf', None),
    (TEXTO, 'Manrope-Regular.ttf', 'Manrope-Bold.ttf'),
    (MONO, 'JetBrainsMono-Regular.ttf', None),
]


def _obfuscate(data, guid):
    key = bytes.fromhex(guid.strip('{}').replace('-', ''))[::-1]
    b = bytearray(data)
    for i in range(32):
        b[i] ^= key[i % 16]
    return bytes(b)


def _theme(xml):
    xml = re.sub(r'<a:clrScheme name="[^"]*">', '<a:clrScheme name="Oryzz">', xml)
    for k, v in THEME_COLORS.items():
        xml = re.sub(rf'<a:{k}>.*?</a:{k}>', f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>', xml, flags=re.S)
    xml = re.sub(r'<a:fontScheme name="[^"]*">', '<a:fontScheme name="Oryzz">', xml)
    xml = re.sub(r'(<a:majorFont>\s*<a:latin typeface=")[^"]*"', rf'\g<1>{DISPLAY}"', xml)
    xml = re.sub(r'(<a:minorFont>\s*<a:latin typeface=")[^"]*"', rf'\g<1>{TEXTO}"', xml)
    xml = re.sub(r'<a:theme ([^>]*)name="[^"]*"', r'<a:theme \1name="Oryzz"', xml)
    return xml


def finalize(docx_path, embed=True):
    """Aplica tema Oryzz, tabla de fuentes con Arial alternativa e incrusta las TTF de marca."""
    tmp = docx_path + '.tmp'
    zin = zipfile.ZipFile(docx_path)
    zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
    fonts_xml = [f'<w:fonts {nsdecls("w", "r")}>']
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    font_files = {}
    k = 0
    for fam, reg, bold in EMBED:
        e = f'<w:font w:name="{fam}"><w:altName w:val="Arial"/><w:charset w:val="00"/><w:family w:val="swiss"/><w:pitch w:val="variable"/>'
        if fam == MONO:
            e = e.replace('<w:family w:val="swiss"/><w:pitch w:val="variable"/>', '<w:family w:val="modern"/><w:pitch w:val="fixed"/>').replace('Arial', 'Consolas')
        if embed:
            for tag, fn in (('embedRegular', reg), ('embedBold', bold)):
                if not fn:
                    continue
                k += 1
                g = '{' + str(uuid.uuid4()).upper() + '}'
                name = f'font{k}.odttf'
                font_files['word/fonts/' + name] = _obfuscate(open(os.path.join(FONTS, fn), 'rb').read(), g)
                rels.append(f'<Relationship Id="rIdF{k}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/{name}"/>')
                e += f'<w:{tag} r:id="rIdF{k}" w:fontKey="{g}"/>'
        fonts_xml.append(e + '</w:font>')
    for fam in ('Arial', 'Consolas', 'Times New Roman', 'Calibri', 'Cambria', 'Symbol'):
        fonts_xml.append(f'<w:font w:name="{fam}"/>')
    fonts_xml.append('</w:fonts>')
    rels.append('</Relationships>')
    names = zin.namelist()
    for item in names:
        data = zin.read(item)
        if item == 'word/fontTable.xml':
            data = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ''.join(fonts_xml)).encode('utf8')
        elif item == 'word/theme/theme1.xml':
            data = _theme(data.decode('utf8')).encode('utf8')
        elif item == 'word/settings.xml' and embed:
            s = data.decode('utf8')
            if 'embedTrueTypeFonts' not in s:
                if re.search(r'<w:zoom[^>]*/>', s):
                    s = re.sub(r'(<w:zoom[^>]*/>)', r'\1<w:embedTrueTypeFonts/>', s, count=1)
                else:
                    s = re.sub(r'(<w:settings[^>]*>)', r'\1<w:embedTrueTypeFonts/>', s, count=1)
            data = s.encode('utf8')
        elif item == '[Content_Types].xml' and embed:
            s = data.decode('utf8')
            if 'odttf' not in s:
                s = s.replace('<Default Extension="xml"', '<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/><Default Extension="xml"')
            data = s.encode('utf8')
        elif item == 'word/_rels/fontTable.xml.rels':
            continue
        zout.writestr(item, data)
    if embed:
        zout.writestr('word/_rels/fontTable.xml.rels', '\n'.join(rels))
        for n, b in font_files.items():
            zout.writestr(n, b)
    zout.close(); zin.close()
    shutil.move(tmp, docx_path)


_ORDER = {
    'pPr': 'pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange',
    'rPr': 'rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow emboss imprint noProof snapToGrid vanish webHidden color spacing w kern position sz szCs highlight u effect bdr shd fitText vertAlign rtl cs em lang eastAsianLayout specVanish oMath',
    'tblPr': 'tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize tblStyleColBandSize tblW jc tblCellSpacing tblInd tblBorders shd tblLayout tblCellMar tblLook tblCaption tblDescription',
    'tcPr': 'cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar textDirection tcFitText vAlign hideMark',
}
_ORDER = {k: {t: i for i, t in enumerate(v.split())} for k, v in _ORDER.items()}
_W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def _reorder(root):
    for tag, order in _ORDER.items():
        for el in root.iter(_W + tag):
            kids = list(el)
            key = lambda e: order.get(e.tag.replace(_W, '') if isinstance(e.tag, str) else '', 999)
            srt = sorted(kids, key=key)
            if srt != kids:
                for k in kids:
                    el.remove(k)
                for k in srt:
                    el.append(k)
            # elementos duplicados (p. ej. dos w:tblLayout): se queda el último
            seen = {}
            for k in list(el):
                if isinstance(k.tag, str) and k.tag in seen and tag in ('tblPr', 'tcPr'):
                    el.remove(seen[k.tag])
                seen[k.tag] = k


def save(doc, path, embed=True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for part in doc.part.package.iter_parts():
        el = getattr(part, '_element', None)
        if el is not None:
            _reorder(el)
    doc.save(path)
    finalize(path, embed)
    return path
