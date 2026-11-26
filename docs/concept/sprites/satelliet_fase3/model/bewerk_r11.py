# r11 (Jordi, 25 nov): "wacht we kunnen ook de zijwaartse ogen dezelfde kant op laten kijken als het voorste oog,
# zodat je nu met links doet, bij deze" (uitsnede linkeroog r10a).
# Vanuit r10 (variant b), zelfde 200-raster/canvas (r10-coordinaten: x_r9 = X - 21, y_r9 = Y + 15).
# 1. linker zijbol: oog van r10a overzetten (positie/vorm/grootte), bol en lichtval van r10 houden.
# 2. rechter zijbol: hetzelfde oog (niet gespiegeld) op de voor-linkerkant van de bol, rechts naast de kraag;
#    waar het oude oog zat: eigen bolkleuren (dichtstbijzijnde bolpixel), aan de buitenrand de bolomlijning.
# 3. binnen de ring alleen iris + pupil (het r10a-oog heeft geen wit; wordt gecontroleerd).
from PIL import Image
import numpy as np

B = np.asarray(Image.open('r10_natief.png').convert('RGB')).astype(int)
A = np.asarray(Image.open('r10a_natief.png').convert('RGB')).astype(int)
H, W = B.shape[:2]
out = B.copy()

def lum(c): return c.sum() / 3
def cls(c):
    r, g, b = c; l = (r + g + b) / 3
    if g > r + 20 and b > r + 10: return 'T'
    if r > g + 25 and b > g + 25 and l > 60: return 'P'
    if l < 60: return 'o'
    if l > 235 and max(c) - min(c) < 20: return '.'
    if l > 150: return 'w'
    return '-'
def bg(a, x, y): return np.all(a[y, x] >= 250)

def in_ell(x, y, cx, cy, rx, ry): return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1

# oogmasker uit r10a (linkeroog): ring, iris, pupil en de donkere rand eromheen
EYE_A = {}
for y in range(59, 72):
    for x in range(62, 79):
        if in_ell(x, y, 70, 65.5, 7.2, 6.4) and cls(A[y, x]) in 'TPo-':
            EYE_A[(x, y)] = A[y, x].copy()

def bulb_fill_pixels(a, box, excl):
    x0, y0, x1, y1 = box
    return [(x, y) for x in range(x0, x1) for y in range(y0, y1)
            if (x, y) not in excl and cls(a[y, x]) in 'w.' and not bg(a, x, y)
            and not all(bg(a, x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < W and 0 <= y + dy < H)]

def nearest(pts, x, y): return min(pts, key=lambda q: (q[0] - x) ** 2 + (q[1] - y) ** 2)

# ---------------------------------------------------------------- 1. linker zijbol
EYE_B = {(x, y) for y in range(56, 72) for x in range(60, 74)
         if in_ell(x, y, 67, 64, 5.5, 7.5) and cls(B[y, x]) in 'TPo-'}
fillL = bulb_fill_pixels(B, (60, 52, 82, 76), EYE_B)
for (x, y) in EYE_B:
    if (x, y) in EYE_A: continue
    if bg(A, x, y): out[y, x] = 255; continue          # buiten het nieuwe silhouet
    q = nearest(fillL, x, y); out[y, x] = B[q[1], q[0]]
for (x, y), c in EYE_A.items(): out[y, x] = c

# ---------------------------------------------------------------- 2. rechter zijbol
OLD_R = {(x, y) for y in range(84, 101) for x in range(186, 203)
         if in_ell(x, y, 194.5, 92, 6.8, 7.5) and cls(B[y, x]) in 'TPo-'}
DX, DY = 179 - 64, 86 - 60          # linker oogrand net rechts van de kraag (x 176-178)
NEW_R = {(x + DX, y + DY): c for (x, y), c in EYE_A.items()}
fillR = bulb_fill_pixels(B, (178, 79, 205, 104), OLD_R | set(NEW_R))
EDGE = np.array([24, 20, 36])
outl = [(x, y) for (x, y) in OLD_R if any(bg(B, x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (0, -1)))]
for (x, y) in OLD_R:
    if (x, y) in NEW_R: continue
    # buitenrand van de bol blijft omlijning; de rest eigen bolkleur
    if any(bg(B, x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (0, -1), (1, 1), (1, -1))):
        out[y, x] = B[y, x] if cls(B[y, x]) == 'o' else EDGE
        continue
    q = nearest(fillR, x, y); out[y, x] = B[q[1], q[0]]
for (x, y), c in NEW_R.items(): out[y, x] = c

# ---------------------------------------------------------------- controle: geen wit in de ogen
for name, eye in (('links', EYE_A), ('rechts', NEW_R)):
    wit = [p for p in eye if lum(out[p[1], p[0]]) > 190]
    print(name, 'oogpixels', len(eye), 'wit/bijna wit:', len(wit))

im = Image.fromarray(out.astype('uint8')); im.save('r11_natief.png')
im.resize((W * 8, H * 8), Image.NEAREST).save('r11_natief_8x.png')
r10 = Image.fromarray(B.astype('uint8'))
sh = Image.new('RGB', (W * 16 + 16, H * 8), 'white')
sh.paste(r10.resize((W * 8, H * 8), Image.NEAREST), (0, 0)); sh.paste(im.resize((W * 8, H * 8), Image.NEAREST), (W * 8 + 16, 0))
sh.save('r11_vs_r10.png')
L = im.crop((56, 50, 86, 80)); R = im.crop((172, 74, 208, 108))
z = Image.new('RGB', (30 * 8 + 16 + 36 * 8, 34 * 8), 'white')
z.paste(L.resize((240, 240), Image.NEAREST), (0, 0)); z.paste(R.resize((288, 272), Image.NEAREST), (256, 0))
z.save('r11_zijogen.png')
