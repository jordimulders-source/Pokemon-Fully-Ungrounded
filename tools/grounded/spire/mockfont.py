"""GBA-lettertypen uit graphics/fonts renderen (voor mockups van Spire-schermen)."""
import os, re
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
CHARMAP = {}
for line in open(os.path.join(ROOT, 'charmap.txt'), encoding='utf-8'):
    m = re.match(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$", line)
    if m:
        CHARMAP.setdefault(m.group(1), int(m.group(2), 16))
CHARMAP.update({'→': 0x7C, '←': 0x7B, '↑': 0x79, '↓': 0x7A})

def _widths(name):
    src = open(os.path.join(ROOT, 'src/fonts.c'), encoding='utf-8').read()
    body = src[src.index(name):]
    body = body[body.index('{') + 1:body.index('};')]
    return [int(x) for x in re.findall(r'\d+', body)]

FONTS = {
    'normal': ('latin_normal.png', 'gFontNormalLatinGlyphWidths', 16, 16),
    'small': ('latin_small_narrow.png', 'gFontSmallNarrowLatinGlyphWidths', 16, 16),
}
_cache = {}

def font(name):
    if name not in _cache:
        png, wname, cw, ch = FONTS[name]
        _cache[name] = (Image.open(os.path.join(ROOT, 'graphics/fonts', png)), _widths(wname), cw, ch)
    return _cache[name]

def text(img, x, y, s, fg=(80, 80, 88), shadow=(208, 208, 216), name='normal'):
    sheet, widths, cw, ch = font(name)
    cols = sheet.width // cw
    px = img.load()
    sp = sheet.load()
    for c in s:
        code = CHARMAP.get(c, 0)
        gx, gy = (code % cols) * cw, (code // cols) * ch
        w = widths[code] if code < len(widths) else 6
        for j in range(ch):
            for i in range(cw):
                v = sp[gx + i, gy + j]
                if v in (1, 2) and 0 <= x + i < img.width and 0 <= y + j < img.height:
                    px[x + i, y + j] = fg if v == 1 else shadow
        x += w
    return x

def width(s, name='normal'):
    _, widths, _, _ = font(name)
    return sum(widths[CHARMAP.get(c, 0)] for c in s)
