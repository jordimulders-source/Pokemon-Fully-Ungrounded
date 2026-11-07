"""r8 = kleur_r7/raster.txt + met de hand geschreven rijstukken (y x0 pixels, '.' = transparant). -> raster.txt + kolibrie_pre.png
Zones: buik links (x16-24, y26-36), pootjes (x24-36, y43-46), vleugelschaduw (x32-41, y28-37), trapjes rug (x34-39, y24-26), kop linksboven (x18-20, y14-15), vleugelpunt (x38-41, y42-43)."""
import sys
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
g=[list(l.rstrip('\n')) for l in open(A+'kleur_r7/raster.txt')][:64]
STUK='''
# 2. buik links: kin-inham weg, één boog (linkerrand 16,16,17,17,18,18,19x7,20,20,21,22,22,23,24,25)
27 18 2666666 5 3
28 19 2 666666
29 19 2 666
30 19 2 66
35 19 . 2
# 1. pootjes (Taillow/Starly): nabije poot x25-30 (twee tenen D met licht C, donker 9 ertussen, zwarte tenen-onderrand),
#    verre poot x30-35 (donkerder: 9 met F), deels achter de nabije
43 26 1 D 9 1 1 1 9 F 1 1
44 25 1 C 9 D 9 1 9 F 9 F 1
45 25 1 D 1 D 1 1 9 1 9 1
46 26 1 . 1 . . 1 . 1
# 3. vleugelschaduw als sikkel (begin A per rij: 39,40,40,39,39,38,38,37,36; daaronder alles A)
28 39 8
29 33 8888888 A
30 33 8888888 A
31 32 8888888 AA
32 32 8888888 AA
33 32 888888 AAAA
34 33 88888 AAAA
35 33 8888 AAAA
36 34 88 AAAAA
# 4. trapjes: rug (rechterrand 33,35,37,38,39,40), kop linksboven (4-2-2-1), vleugelpunt rond
24 36 .
25 36 1
26 39 .
26 35 333
14 19 .
15 19 2
42 40 1 .
43 40 .
'''
for l in STUK.splitlines():
    if not l.strip() or l.startswith('#'): continue
    y,x0,*p=l.split(); p=''.join(p)
    for i,c in enumerate(p): g[int(y)][int(x0)+i]=c
open(A+'kleur_r8/raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
sys.path.insert(0,A+'kleur_r8'); import palet; palet.build(A+'kleur_r8/raster.txt',A+'kleur_r8/kolibrie_pre.png')
