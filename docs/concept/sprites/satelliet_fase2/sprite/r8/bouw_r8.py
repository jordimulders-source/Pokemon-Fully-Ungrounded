# r8: volume/schaduw, ring linksboven 1 px, antennes/bolletjes netjes, twee pupilvarianten.
# Basis: ../../eindkeuring_r6/r7/oog_b.png. Alles met de hand als tekstruns (put), geen automatische kleuring.
# Draaien vanuit deze map:  python3 bouw_r8.py
import numpy as np
from PIL import Image
BASIS = '../../eindkeuring_r6/r7/oog_b.png'
im0 = Image.open(BASIS); a = np.array(im0).astype(int); pal = im0.getpalette()[:48]
r7 = a.copy()
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c == '-': continue
        a[y, x + i] = 0 if c == '.' else H.index(c)

# ---- palet: lijframp 2-3-4-5 gelijkmatiger (3 lichter, 4 donkerder) ----
pal[3*3:3*3+3] = [218, 210, 230]
pal[4*3:4*3+3] = [182, 164, 204]

# ---- punt 4: antennes, staafjes, bolletjes (posities uit het model) ----
for y in range(5, 16):
    for x in range(21, 51): a[y, x] = 0
for y in range(16, 19):
    for x in range(21, 46): a[y, x] = 0
for x in range(21, 44): a[19, x] = 0
# linker antenne: staaf 7 (licht) + 8 (donker), bol x34-37 r7-10 (model x33,9-37,0 y7,0-10,1)
put(35, 7, '88')
put(34, 8, '8368')
put(32, 9, '788671')
put(31, 10, '78'); put(35, 10, '11')
put(30, 11, '78')
put(28, 12, '778')
put(27, 13, '788')
put(26, 14, '78')
put(25, 15, '78')
put(24, 16, '78')
# rechter antenne: boog 6 boven / 8 onder, runs 1-1-2-2-3-6; bol x47-50 r9-12 (model x47,2-50,7 y8,6-12,1)
put(48, 9, '88')
put(41, 10, '666666'); put(47, 10, '8368')
put(38, 11, '666888888'); put(47, 11, '8671')
put(48, 12, '11')
put(36, 12, '66888')
put(34, 13, '6688')
put(33, 14, '688')
put(32, 15, '68')
# groot gewricht x27-32 r15-20 (model x27,5-32,2 y15,2-21,0): 8 boven/links, zwart rechts/onder
put(28, 15, '8888')
put(27, 16, '866671')
put(27, 17, '863671')
put(27, 18, '866781')
put(27, 19, '877881')
# staafje links: r17 bovenlijn, r18 kleur, r19 binnenlijn
put(21, 17, '888888')
put(21, 18, '866667')
put(21, 19, '888888')
# staafje rechts van het gewricht (model x32-36 y16,8-18,3)
put(33, 16, '8')
put(33, 17, '6888')
put(33, 18, '86778')
put(33, 19, '38888')
# rechter gewricht x37-40 r19-22 (model x37,4-40,7 y19,6-23,1) + staaf naar paneel
put(38, 19, '888888')
put(40, 18, '6666'); put(44, 18, '88')
put(44, 17, '666')
put(37, 20, '8361')
put(37, 21, '8671')
put(38, 22, '111')

# ---- punt 3 + lijf: rij voor rij (2 hooglicht, 3 basis, 4 schaduw, 5 diepe schaduw/selout) ----
put(22, 20, '322222'); put(32, 20, '33333')
put(18, 21, '5533322222233333333')
put(17, 22, '543322222222233333344')
put(16, 23, '54433222222223333444444')
put(15, 24, '54443322222223334444444')
put(14, 25, '54433333222223344444455')   # r25 x15-20 was ring (7): nu lijf
put(15, 26, '6666666673334444444555')    # ring linksboven 1 px (r26), licht want naar de lamp
put(14, 27, '83222233667733333333555')    # 15-16 was ring (8): nu witte rand
put(15, 28, '3222233366773222223334')
put(15, 29, '22')
put(21, 29, '3336711222233334')
put(14, 30, '2'); put(23, 30, '336711'); put(29, 30, '222333344')
put(24, 31, '3788'); put(29, 31, '322333444')
put(24, 32, '3378'); put(29, 32, '333888844')
put(25, 33, '378'); put(28, 33, '3'); put(30, 33, '3866671')
put(25, 34, '378'); put(28, 34, '3'); put(30, 34, '386361')
put(25, 35, '378'); put(28, 35, '3'); put(30, 35, '38667')
put(25, 36, '478'); put(28, 36, '4'); put(30, 36, '48777')
put(24, 37, '4478'); put(28, 37, '4'); put(30, 37, '4878')
put(24, 38, '478'); put(27, 38, '4'); put(29, 38, '445111')
put(23, 39, '4478'); put(27, 39, '4'); put(29, 39, '4555')
put(15, 40, '33'); put(21, 40, '444788')
put(16, 41, '3344444')
put(18, 42, '444'); put(26, 42, '445555')
put(17, 43, '4'); put(22, 43, '444445555')
put(18, 44, '444444455555')
put(19, 45, '44445555555')

# ---- paneel: glansband (model: lichtere vlek links in de derde celrij) ----
put(40, 34, 'BBBB'); put(45, 34, 'BB')
put(39, 35, 'BBBB'); put(44, 35, 'BBB')
put(38, 36, 'BBBBB'); put(44, 36, 'BB')
put(39, 37, 'BBB')

def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); rgba = im.convert('RGBA'); m = np.array(rgba); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))

# ---- punt 1: pupil naar de kijkrichting (figuur kijkt naar kijker-links) ----
p1 = a.copy()   # pupil 1 px links; lichte iristint en glans schuiven mee
put_ = lambda arr, x, y, s: [arr.__setitem__((y, x + i), H.index(c)) for i, c in enumerate(s)]
put_(p1, 17, 32, 'EDDE'); put_(p1, 16, 33, 'EE2DEE'); put_(p1, 16, 34, 'E99EEE'); put_(p1, 16, 35, 'E99EEE')
p2 = a.copy()   # pupil 1 px links + 1 px omlaag (zoals Magnemite: pupil links-onder van het midden)
put_(p2, 17, 32, 'EEEE'); put_(p2, 16, 33, 'EEDDEE'); put_(p2, 16, 34, 'EE2DEE'); put_(p2, 16, 35, 'E99EEE'); put_(p2, 16, 36, 'E99EEE')
sla(p1, 'sprite_p1.png'); sla(p2, 'sprite_p2.png')
np.save('r7.npy', r7)
