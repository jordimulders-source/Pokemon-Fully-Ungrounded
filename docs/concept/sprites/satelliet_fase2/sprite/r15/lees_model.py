# model op het spriteraster in grove klassen, 4x4 subsamples per spritepixel: '#'zwart 'd'donkerpaars 'm'paars 'l'lila 'w'wit 'g'grijslila 'P'paneel 't'teal '.'leeg
import numpy as np
from PIL import Image
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(int); k = 12.703
def kl(c):
    r, g, b = c; L = .299 * r + .587 * g + .114 * b
    if min(c) > 248: return '.'
    if g > r + 20 and g > 100: return 't'
    if L < 40: return '#'
    if abs(r - 50) < 14 and abs(g - 43) < 14 and abs(b - 88) < 16: return 'P'
    if L < 80: return 'd'
    if L < 135: return 'm'
    sat = max(c) - min(c)
    if L < 195 and sat > 40: return 'l'
    if L < 215: return 'g'
    return 'w'
X0, X1, Y0, Y1 = 8, 34, 20, 49
rows = []
for y in range(Y0, Y1):
    s1 = s2 = ''
    for x in range(X0, X1):
        cs = [kl(M[int(143 + (y + v - 7) * k), int(103 + (x + u) * k)]) for u in (.125, .375, .625, .875) for v in (.125, .375, .625, .875)]
        from collections import Counter
        c = Counter(cs); s1 += c.most_common(1)[0][0]
        order = '#dPtmlgw.'; s2 += min(cs, key=order.index) if c['#'] + c['d'] >= 4 else c.most_common(1)[0][0]
    rows.append('%2d %s   %s' % (y, s1, s2))
print('   ' + ''.join(str(x % 10) for x in range(X0, X1)) + '   ' + ''.join(str(x % 10) for x in range(X0, X1)))
print('\n'.join(rows))
