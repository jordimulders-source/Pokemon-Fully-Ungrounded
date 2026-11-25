# r10: koepel met volume (licht linksboven), lichtverloop op beide panelen, bovenkant netter (bol-opbouw gewrichten,
# kraag = lijn boven / vulling / lijn onder). Basis: ../r9/sprite.png (oog b + pupil p2 ongewijzigd). Draaien: python3 bouw_r10.py
import numpy as np
from PIL import Image
im0 = Image.open('../r9/sprite.png'); a = np.array(im0).astype(int); pal = im0.getpalette()[:48]
r9 = a.copy()
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c == '-': continue
        a[y, x + i] = 0 if c == '.' else H.index(c)

# ================= 3. bovenkant =================
# groot gewricht x28-32 r15-20: bol-opbouw, glans linksboven, 6 -> 7 -> 8 naar rechtsonder; omlijning 8 linksboven, 1 rechtsonder
put(29, 15, '881')
put(28, 16, '83671')
put(28, 17, '86671')
put(28, 18, '86771')
put(28, 19, '87781')
put(29, 20, '111')
# kraag links: lijn boven (8) / vulling (6 boven, 7 onder) / lijn onder (1), tot tegen het gewricht
put(22, 17, '866666')
put(22, 18, '777777')
put(22, 19, '111111')
# kraag rechts: lijn boven 8 / vulling 6-7 / lijn onder 1, buigt in het kleine gewricht
put(33, 17, '8888')
put(33, 18, '6677')
put(33, 19, '1111')
# klein gewricht x37-40 r19-23: zelfde bol-opbouw
put(37, 19, '888')
put(37, 20, '8361')
put(37, 21, '8671')
put(37, 22, '8781')
put(38, 23, '11')

# ================= 1. koepel =================
# binnenste wit (tussen lensring en paarse rand): 2 linksboven/links, 3 rechts, 4 onder/rechtsonder
put(15, 27, '66'); put(17, 27, '22222')                 # bovenkant: helemaal 2
put(15, 28, '2222222'); put(22, 28, '3')
put(15, 29, '22'); put(21, 29, '233')
put(14, 30, '2'); put(23, 30, '33')
a[31, 13] = 2; put(12, 32, '22'); a[33, 12] = 2; a[34, 12] = 2; a[35, 12] = 2   # linkerkant (licht): 2
a[36, 12] = 3; a[37, 13] = 3; a[38, 14] = 3; a[39, 14] = 3                       # linksonder: 3
put(15, 40, '34')                                                                # onder: 4
put(16, 41, '3444444')
put(18, 42, '444')
# paarse rand: boven 6, rechts 7/8, onder 8; linksonder 7 (halflicht)
put(16, 42, '77'); put(18, 43, '7788')
# onderlijf onder de koepel: 4, met een sikkel in 5 die de ronding langs onder en rechts volgt
put(22, 43, '44444445555')
put(18, 44, '444444444555')
put(19, 45, '44444455555')
put(22, 46, '5555555')

# paarse rand rechts loopt mee met het licht: rechtsboven 6/7, midden 7/8 (r9), onder 8
put(25, 31, '677'); put(26, 32, '67'); put(26, 33, '67')
# buitenste koepellijn rechtsboven (lichtkant, tegen het witte lijf) in de donkerste lijftint 5; vanaf r33 zwart (schaduwkant)
for x, y in [(26, 29), (27, 29), (27, 30), (28, 30), (28, 31), (28, 32)]: a[y, x] = 5

# ================= 2. panelen =================
# groot paneel: cel linksboven (r1 links, de cel die aan (48,20) vastzit) in B = lichtste cel; lijnen C blijven
from scipy import ndimage
lab, _ = ndimage.label(a == 10)
a[lab == lab[20, 48]] = 11
# klein paneel (achter): bovenste celrij (r17-24) in A = licht boven, de rest blijft 9; omlijning (9 tegen transparant) blijft 9
for y in range(17, 25):
    for x in range(0, 21):
        if a[y, x] == 9 and all(a[y + dy, x + dx] != 0 for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1))):
            a[y, x] = 10

def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); rgba = im.convert('RGBA'); m = np.array(rgba); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
sla(a, 'sprite.png'); np.save('r10.npy', a)
d = a != r9
print('afwijkend t.o.v. r9:', d.sum())
for nm, (x0, x1, y0, y1) in {'boven': (21, 51, 5, 24), 'koepel': (11, 30, 26, 47), 'groot paneel': (36, 64, 12, 55), 'klein paneel': (0, 21, 12, 43)}.items():
    print(' ', nm, d[y0:y1, x0:x1].sum())
oog = r9[30:40, 14:24] != a[30:40, 14:24]
print('  oog (lens x14-23 r30-39) gewijzigd:', oog.sum())
