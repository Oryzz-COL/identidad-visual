"""
Texto vectorizado (trazados) con las fuentes de marca, para SVG portables
(se ven igual en Figma, Illustrator, <img> y navegadores sin las fuentes instaladas).

    from svg_text import text
    text('ÁREA DE RESPETO', 'mono-medium', 14, x, y, fill='#8A90A0', tracking=0.16)
    text('Tamaños mínimos', 'display-bold', 44, x, y, fill='#fff', tracking=-0.03, anchor='start')

Aplica el kerning GPOS (PairPos formato 1 y 2) de la fuente. Devuelve '<path …/>' o '' si vacío.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts', 'static')
FILES = {
    'mono': 'JetBrainsMono-Regular.ttf', 'mono-medium': 'JetBrainsMono-Medium.ttf', 'mono-bold': 'JetBrainsMono-Bold.ttf',
    'display-medium': 'SpaceGrotesk-Medium.ttf', 'display-semibold': 'SpaceGrotesk-SemiBold.ttf', 'display-bold': 'SpaceGrotesk-Bold.ttf',
    'texto': 'Manrope-Regular.ttf', 'texto-medium': 'Manrope-Medium.ttf', 'texto-semibold': 'Manrope-SemiBold.ttf', 'texto-bold': 'Manrope-Bold.ttf',
}
_cache = {}
MISSING = set()


class _F:
    def __init__(self, path):
        self.f = TTFont(path)
        self.gs = self.f.getGlyphSet(); self.cmap = self.f.getBestCmap(); self.hmtx = self.f['hmtx']
        self.upm = self.f['head'].unitsPerEm
        self.kern = {}
        self._pairs1 = {}; self._pairs2 = []
        if 'GPOS' in self.f:
            g = self.f['GPOS'].table
            idx = set()
            for fr in g.FeatureList.FeatureRecord:
                if fr.FeatureTag == 'kern':
                    idx.update(fr.Feature.LookupListIndex)
            for i in sorted(idx):
                lk = g.LookupList.Lookup[i]
                for st in lk.SubTable:
                    if lk.LookupType == 9:
                        st = st.ExtSubTable
                    if getattr(st, 'LookupType', 2) != 2 and lk.LookupType not in (2, 9):
                        continue
                    if not hasattr(st, 'Format'):
                        continue
                    if st.Format == 1:
                        for g1, ps in zip(st.Coverage.glyphs, st.PairSet):
                            for r in ps.PairValueRecord:
                                v = getattr(r.Value1, 'XAdvance', 0) if r.Value1 else 0
                                self._pairs1.setdefault((g1, r.SecondGlyph), v)
                    elif st.Format == 2:
                        self._pairs2.append(st)

    def pair(self, a, b):
        k = (a, b)
        if k in self.kern:
            return self.kern[k]
        v = self._pairs1.get(k)
        if v is None:
            v = 0
            for st in self._pairs2:
                if a not in st.Coverage.glyphs:
                    continue
                c1 = st.ClassDef1.classDefs.get(a, 0); c2 = st.ClassDef2.classDefs.get(b, 0)
                rec = st.Class1Record[c1].Class2Record[c2]
                v = getattr(rec.Value1, 'XAdvance', 0) if rec.Value1 else 0
                break
        self.kern[k] = v
        return v


def font(key):
    if key not in _cache:
        _cache[key] = _F(os.path.join(FONTS_DIR, FILES[key]))
    return _cache[key]


def measure(s, key, size, tracking=0.0):
    return _layout(s, key, size, tracking)[1]


def _layout(s, key, size, tracking):
    F = font(key); sc = size / F.upm
    items = []; x = 0.0; prev = None
    for ch in s:
        g = F.cmap.get(ord(ch))
        if g is None:
            MISSING.add((key, ch)); g = F.cmap.get(ord(' '))
        if prev is not None:
            x += F.pair(prev, g) * sc
        items.append((g, x))
        x += F.hmtx[g][0] * sc + tracking * size
        prev = g
    width = x - (tracking * size if s else 0)
    return items, width


def text(s, key, size, x, y, fill='#000', tracking=0.0, anchor='start', opacity=None, upper=False):
    if upper:
        s = s.upper()
    if not s:
        return ''
    F = font(key); sc = size / F.upm
    items, width = _layout(s, key, size, tracking)
    if anchor == 'middle': x -= width / 2
    elif anchor == 'end': x -= width
    pen = SVGPathPen(F.gs, ntos=lambda v: ('%.2f' % v).rstrip('0').rstrip('.'))
    for g, gx in items:
        F.gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x + gx, y)))
    d = pen.getCommands()
    if not d:
        return ''
    op = f' opacity="{opacity}"' if opacity is not None else ''
    return f'<path d="{d}" fill="{fill}"{op}/>'
