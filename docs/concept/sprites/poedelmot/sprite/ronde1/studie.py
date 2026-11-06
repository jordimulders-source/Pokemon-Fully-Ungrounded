"""Studie (SPRITE_KERN stap 4): Butterfree, Venomoth, Dustox, Beautifly + witte wol (Swablu, Altaria, Whimsicott), frame 1 op 6x.
Schrijft studie.png en print per soort het palet (index: rgb)."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, '../../../../../../graphics/pokemon/')
NAMEN = ['butterfree', 'venomoth', 'dustox', 'beautifly', 'swablu', 'altaria', 'whimsicott']
def pal(p):
    L = open(p).read().split('\n'); return [tuple(map(int, L[3 + i].split())) for i in range(int(L[2]))]
def laad(n):
    d = G + n + '/'; f = d + ('anim_front.png' if os.path.exists(d + 'anim_front.png') else 'front.png')
    im = Image.open(f); P = pal(d + 'normal.pal'); a = im.load(); o = Image.new('RGB', (64, 64), (200, 200, 200)); q = o.load()
    for y in range(64):
        for x in range(64):
            if a[x, y]: q[x, y] = P[a[x, y]]
    return o, P
if __name__ == '__main__':
    Z = 6; V = Image.new('RGB', (4 * 64 * Z, 2 * 64 * Z), (200, 200, 200))
    for i, n in enumerate(NAMEN):
        im, P = laad(n); V.paste(im.resize((64 * Z, 64 * Z), Image.NEAREST), ((i % 4) * 64 * Z, (i // 4) * 64 * Z))
        print(n, ' '.join(f'{j:x}:{c}' for j, c in enumerate(P)))
    V.save(os.path.join(HERE, 'studie.png'))
