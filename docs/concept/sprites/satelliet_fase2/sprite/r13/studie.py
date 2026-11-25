# Studie Gen 3 (GBA-sprites + normal_gba.pal): vel op 6x + tinten per sprite.
import numpy as np
from PIL import Image
G = '../../../../../../graphics/pokemon/'
NAMEN = ['magnemite', 'magneton', 'claydol', 'glalie', 'beldum', 'metang', 'lunatone']
def laad(n):
    im = Image.open(G + n + '/anim_front_gba.png'); a = np.array(im)[:64]
    pal = []
    for l in open(G + n + '/normal_gba.pal').read().split('\n')[3:19]:
        pal.append(tuple(int(v) for v in l.split()))
    return a, pal
if __name__ == '__main__':
    Z = 6; vel = Image.new('RGB', (64 * Z * 4 + 30, 64 * Z * 2 + 20), (255, 255, 255))
    for i, n in enumerate(NAMEN):
        a, pal = laad(n)
        rgb = np.array([pal[v] for v in a.flat], dtype='uint8').reshape(64, 64, 3); rgb[a == 0] = 255
        vel.paste(Image.fromarray(rgb).resize((64 * Z, 64 * Z), Image.NEAREST), ((i % 4) * (64 * Z + 10), (i // 4) * (64 * Z + 10)))
        print(n)
        for k in range(1, 16):
            c = (a == k).sum()
            if c: print('   %X %-16s L=%3d n=%d' % (k, pal[k], int(0.299 * pal[k][0] + 0.587 * pal[k][1] + 0.114 * pal[k][2]), c))
    vel.save('studie_gen3_6x.png')
