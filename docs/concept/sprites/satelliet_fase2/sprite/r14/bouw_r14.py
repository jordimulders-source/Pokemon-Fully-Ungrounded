# r14: kap lager en vlakker + groot gewricht naar het model (Jordi: "de bovenste kap is bij ons wat hoger en wat bolliger").
# Basis ../r13/sprite.png (tinten en opbouw van r13). Gemeten per kolom op het modelraster
# sprite-x = (mx-103)/12.703, sprite-y = (my-143)/12.703 + 7 (zie meet_r14.txt):
#   kapbuitenlijn x21-26 op rij 17 (model 16,9-17,5), dunne lila rand rij 18, lijf vanaf rij 19 (model 18,75-20,0);
#   groot gewricht: binnenkant x28-31 (r13: x29-31), boven rij 15 (x29-30), onder rij 21 (x29-30) (r13: rij 20), links x27, rechts x32 rij 17-18.
# Kleine paneelhoek, lijfcontour links, klein gewricht rechts en de rest blijven r13. Draaien vanuit deze map: python3 bouw_r14.py
import numpy as np
from PIL import Image
im0 = Image.open('../r13/sprite.png'); a = np.array(im0).astype(int); pal = im0.getpalette()[:48]; r13 = a.copy()
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c == '-': continue
        a[y, x + i] = 0 if c == '.' else H.index(c)
# rij 15: gewrichtbovenkant (8) blijft x29-30; rechterantenne loopt door tot op het gewricht
put(28, 15, '888666')
# rij 16: oude kapbuitenlijn weg (x23-24), voet linkerantenne (25) + onderkant steel (26-27) blijft; gewricht: rand 8, hooglicht 3, 6, zwart rechtsboven, antenne-onderkant 8
put(23, 16, '..7888361' + '88')
# rij 17: kapbuitenlijn 8 (x21-26, recht), gewricht links 8 (x27), binnen 6 6 6 7, rechts zwart
put(21, 17, '8888888' + '6667' + '1')
# rij 18: dunne lila rand 6 (x22-26), gewricht
put(21, 18, '766666' + '8' + '6677' + '1')
# rij 19: lijf (hooglicht een rij lager: rij 19 basis 2), gewricht onder-links zwart
put(20, 19, '2222222' + '1' + '7778' + '1')
# rij 20/21: onderkant gewricht een rij lager
put(27, 20, '21771' + '2')
put(29, 21, '11')
# ======== OPSLAAN
def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); rgba = im.convert('RGBA'); m = np.array(rgba); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
if __name__ == '__main__':
    sla(a, 'sprite.png'); np.save('r14.npy', a)
    d = a != r13
    print('afwijkend t.o.v. r13:', d.sum(), 'buiten x19-34/y14-22:', d.sum() - d[14:22, 19:35].sum(), ' kleuren', len(np.unique(a)) - 1,
          ' silhouet: +', ((a > 0) & (r13 == 0)).sum(), ' -', ((a == 0) & (r13 > 0)).sum())
    H2 = '.123456789ABCDEF'
    for y in range(12, 23): print('%2d ' % y + ''.join(H2[v] for v in r13[y, 18:40]) + '   ' + ''.join(H2[v] for v in a[y, 18:40]))
