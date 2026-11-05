"""Ronde 3: r2-rasters + met de hand gekozen wijzigingen -> raster_A.txt, raster_B.txt.
Palet: e (iris) vervalt -> oog e wordt k (verder pixel voor pixel Pikachu); kuiftop-binnentint e wordt G
(zelfde posities, Pikachu's eigen oortint (64,64,72)); vrije plek = h (bleke hoorn). g = warm grijs: donkere hoorn en poot licht."""
import os
D = os.path.dirname(os.path.abspath(__file__))
def lees(v):
    return [list(r.rstrip('\n')) for r in open(os.path.join(D, '..', 'kleur_r2', f'raster_{v}.txt'))][:64]
def zetter(rows):
    def zet(y, x0, s):
        for i, c in enumerate(s):
            if c != '_':
                rows[y][x0 + i] = c
    return zet
for v in ('A', 'B'):
    rows = lees(v); zet = zetter(rows)
    for y in range(64):
        for x in range(64):
            if rows[y][x] == 'e':
                rows[y][x] = 'k' if y >= 18 else 'G'
    # 2. geen naad onder de wang: alleen een sikkel aan de schaduwkant
    zet(26, 28, '22233')
    zet(27, 23, '22222222333')
    zet(28, 33, '3')
    # 3. derde schubbenrij weg (twee duidelijke rijen)
    zet(35, 37, 'dbbbbbbdk')
    zet(36, 38, 'dbbbbbbdk')
    zet(37, 38, 'dbbbbbbdk')
    # 1. snavel: bleke hoorn, donkere hoorn boven/onder, punt zwart, aanzet lichter dan de kop
    if v == 'A':
        zet(17, 15, 'kg')
        zet(18, 15, 'khg')
        zet(19, 16, 'khgh2')
        zet(20, 17, 'khhh2')
        zet(21, 17, 'kghhh2')
        zet(22, 18, 'kgg32')
        zet(23, 19, 'kk3')
    else:
        zet(17, 15, 'kg')
        zet(18, 15, 'khgg')
        zet(19, 16, 'khhh2')
        zet(20, 17, 'khhh2')
        zet(21, 17, 'khhhh2')
        zet(22, 17, 'kggg32')
        zet(23, 18, 'kkk3')
        # 4. verre poot met tenen (schaduwtint), kolom 33 lucht
        zet(45, 34, 'kGGk')
        zet(46, 34, 'kGGGk')
        zet(47, 34, 'GkGkG')
    open(os.path.join(D, f'raster_{v}.txt'), 'w').write('\n'.join(''.join(r) for r in rows) + '\n')
