# bouw12.py: s12 = s10 met nieuwe inkleuring (ronde 2 na s11, keurderpunten A1-C3) van hoofd, poten en verre vleugel (studie in NOTITIES.md).
# Silhouet en oog bevroren (assert). Alleen kleur/schaduw/belijning binnen de vorm; per zone een tekstraster.
# Raster-tekens: '.' = transparant (moet transparant zijn in s10), '-' = laat s10 staan, 1-9/A-F = paletindex.
import numpy as np
from PIL import Image
PAL = [(255, 255, 255), (16, 14, 24),
       (100, 114, 178),                                     # 2 navy licht (= gezicht schaduw)
       (64, 60, 104),                                       # 3 navy midden (= gezicht diepe schaduw, krop donker, selout poten/snavel)
       (34, 32, 60),                                        # 4 navy donker (verre vleugel schaduw, penlijnen)
       (244, 236, 212), (208, 198, 172),                    # 5-6 creme licht/midden (5 ook klauwen)
       (146, 144, 136),                                     # 7 creme schaduw = grijs midden
       (192, 192, 188),                                     # 8 grijs licht (snavel, poten)
       (184, 136, 188), (146, 96, 148),                     # 9-10 krop licht/midden
       (200, 126, 78), (150, 80, 54), (96, 42, 32),         # 11-13 kuif licht/midden/donker
       (196, 60, 52),                                       # 14 oogrood
       (116, 158, 204)]                                     # 15 gezicht licht
S10 = np.array(Image.open('../s10/hoatzin.png')).astype(int)
B = S10.copy()
HEX = '0123456789ABCDEF'

def zone(x0, y0, rows):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            x, y = x0 + i, y0 + j
            if ch == ' ': continue
            if ch == '.':
                assert S10[y, x] == 0, ('niet transparant in s10', x, y); continue
            assert S10[y, x] != 0, ('transparant in s10', x, y)
            if ch == '-': continue
            B[y, x] = HEX.index(ch)

# ---- verre vleugel (x12-29, y7-28), met de hand naar Pidgeot/Fearow/Honchkrow: elke veer een lichte linkerrand (2)
#      naast een donkere penlijn (4) die vanuit de inkepingen van de lobben naar rechtsonder loopt (richting van de veren
#      in het model); veertoppen licht, lichaam midden, sikkel 4 rechts, schaduwzone 4 onderaan achter kop en nek ----
VER = [
    "........1..111....",  # 7
    ".......11.1221....",  # 8
    "......1221222211..",  # 9
    ".....12224224221..",  # 10
    ".....12234423421..",  # 11
    "....122333433411..",  # 12
    "....123333443341..",  # 13
    "...1223333343341..",  # 14
    "...12233333443441.",  # 15
    "..12233333334441..",  # 16
    ".122333333333441..",  # 17
    "..12333333333444-1",  # 18
    "..1233333344444---",  # 19
    "..1443344443333---",  # 20
    "-----4333333444441",  # 21
    "----11344444444441",  # 22
    "---1..144444444444",  # 23
    "--1....14433444444",  # 24
    "--1.....1444444444",  # 25
    "-----1..1444444441",  # 26
    "---11....144444441",  # 27
    "---......134111111",  # 28
]
zone(12, 7, VER)

# ---- kop (x0-17, y17-36): kuif als twee lobben met donkere scheiding (Spearow/Pidgeot), licht linksboven,
#      donker onder en rechts; spikes licht aan de lichtkant, zwart aan de schaduwkant ----
KOP = [
    ".............-----",  # 17
    "........1.....----",  # 18
    "........B.....----",  # 19
    ".......B1.....----",  # 20
    ".......C1...DDBCC-",  # 21
    ".......C1DDDBBCD11",  # 22
    ".....11BBCBBCCD1..",  # 23
    ".....1BBCCDCCD1...",  # 24
    ".....1BCCCDDCC1...",  # 25
    ".....1CCDDDDDCCDD1",  # 26
    "....1BD1111DDCD11.",  # 27
    "...1BD1FFFF1DD1...",  # 28
    "....D1FFFEE21D1...",  # 29
    "....1FFFE1E31771..",  # 30
    "..1111222EE31671..",  # 31
    ".18888122331556711",  # 32
    ".711771111166665--",  # 33
    ".1..8887766666666-",  # 34
    "...111111111117776",  # 35
    "..............1117",  # 36
]
zone(0, 17, KOP)

# ---- poten (x16-45, y48-61): Dodrio/Doduo/Skarmory: scheen 1 px kleur met selout (3) aan de lichtkant en zwart
#      aan de schaduwkant; teen = selout boven, kleur, zwart onder; klauw = lichte pixel ingesloten door lijn.
#      Nabije poot licht (8/7), verre poot in schaduw (7/3). ----
POOT = [
    #678901234567890123456789012345
    "............------...-------..",  # 49
    ".............-----.....-----..",  # 50
    ".............781.........771..",  # 51
    "............781..........71...",  # 52
    "..........781............71...",  # 53
    ".........781............771...",  # 54
    ".......77881............71....",  # 55
    "..7777788887777........171....",  # 56
    ".15788111..1111.......1777781.",  # 57
    "..1111............77777771111.",  # 58
    ".................11118771.....",  # 59
    "................1811.111......",  # 60
]
zone(16, 49, POOT)

# ---- staartveer boven (x44-53, y42-45): een lichte rand boven, midden eronder (was per pixel 2/3) ----
STAART = [
    #4567890123
    "2222",  # 42
    "22222224",  # 43
    "2333333334",  # 44
    "-33333333",  # 45
]
zone(44, 42, STAART)

# ---- bewijs ----
assert ((S10 > 0) == (B > 0)).all(), 'silhouet anders dan s10'
OOG = [(9, 29), (10, 29), (8, 30), (10, 30), (9, 31), (10, 31)]
assert all(B[y, x] == 14 for x, y in OOG) and B[30, 9] == 1 and (B == 14).sum() == 6
assert B.max() < 16
im = Image.fromarray(B.astype(np.uint8), 'P'); im.putpalette([c for p in PAL for c in p]); im.save('hoatzin.png', transparency=0)
im.convert('RGB').resize((512, 512), Image.NEAREST).save('hoatzin_8x.png')
with open('normal.pal', 'w') as f: f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % p for p in PAL))
print('silhouet anders dan s10: 0; oog gelijk; pixels anders dan s10:', int((S10 != B).sum()))
