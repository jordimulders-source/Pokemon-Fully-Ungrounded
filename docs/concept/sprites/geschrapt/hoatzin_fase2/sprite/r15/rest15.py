# rest15.py (r15): buiktop, voeten, staart, nekrand op k15.npy -> r15.npy + hoatzin.png
# Tekens in de rijen: . transparant, 1 lijn, 2-5 mauve, 6/7 bruin, A/B/C buik (11/12/13), D/E grijs (14/15).
import numpy as np; from PIL import Image
a = np.load('k15.npy'); P = np.load('part.npy')
V = {'.': 0, 'A': 11, 'B': 12, 'C': 13, 'D': 14, 'E': 15}
def paint(rows, wis=False):
    for y, (x0, s) in rows.items():
        for i, c in enumerate(s):
            if c == '.' and not wis: continue
            a[y, x0+i] = V[c] if c in V else int(c)
# ---------- 6 buiktop: koepel, y36 x20-25, y35 x22-23 ----------
paint({35: (22, 'BB'), 36: (20, 'BCCBBA'), 37: (19, 'C')})
# ---------- 4/5/7 voeten (x12-41, y54-63), maat van de nabije voet uit het model ----------
paint({54: (12, '.....11111DDD21...2EDD21...13'),
       55: (12, '....1EEEEEEDD1111EEEDDD11..13'),
       56: (12, '....122222' + '2D21EEEEDDDDDEE1.13'),
       57: (12, '...1......' + '.21EDDDEDDD22DDE122'),
       58: (12, '...1......' + '.1DD221ED21111221.2'),
       59: (12, '..........' + '.111111ED21...11.1.'),
       60: (12, '..........' + '1....1ED21.........'),
       61: (12, '..........' + '.....1D21..........'),
       62: (12, '..........' + '......1............'),
       63: (12, '..........' + '.....1.............')}, wis=True)
a[58, 38] = 1; a[59, 39] = 1; a[59, 38] = 0   # klauw rechter teen: 2 px diagonaal
a[57, 39] = 0; a[57, 40] = 1; a[58, 40] = 1   # staartrand naast de rechter teen in lijnkleur
# ---------- staart: vlak 2, licht randje 3 links, twee doorlopende veerlijnen 1 (op 1/3 en 2/3), taps ----------
bg = a == 0
rand = np.zeros_like(bg)
rand[1:-1, 1:-1] = bg[:-2, 1:-1] | bg[2:, 1:-1] | bg[1:-1, :-2] | bg[1:-1, 2:]
for y in range(44, 64):
    xs = [x for x in range(36, 64) if P[y, x] == 1 and not rand[y, x]]
    if not xs: continue
    x0, x1 = min(xs), max(xs); w = x1 - x0 + 1
    for x in xs: a[y, x] = 2
    if 50 <= y <= 59: a[y, x0] = 3
    for f, ya, yb in [(1/3, 51, 59), (2/3, 50, 60)]:
        if ya <= y <= yb and w >= 6:
            xl = x0 + round(w * f); a[y, xl] = 1
            if y <= yb - 2 and xl + 1 <= x1: a[y, xl + 1] = 3   # lichte bovenrand van de volgende veer
# ---------- nek: lichte rand 5 één keer onderbreken (y34) ----------
for x in range(16, 21):
    if a[34, x] == 5: a[34, x] = 4
np.save('r15.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(Image.open('../r14/hoatzin.png').getpalette()); im.save('hoatzin.png', transparency=0)
