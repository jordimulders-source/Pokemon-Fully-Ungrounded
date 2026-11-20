# bouw11.py: s11 = s10 met nieuwe inkleuring van hoofd, poten en verre vleugel (studie in NOTITIES.md).
# Silhouet en oog bevroren (assert). Alleen kleur/schaduw/belijning binnen de vorm; per zone een tekstraster.
# Raster-tekens: '.' = transparant (moet transparant zijn in s10), '-' = laat s10 staan, 1-9/A-F = paletindex.
import numpy as np
from PIL import Image
PAL = [(255, 255, 255), (16, 14, 24),
       (96, 108, 170),                                      # 2 navy licht (= gezicht schaduw)
       (64, 60, 104),                                       # 3 navy midden (= gezicht diepe schaduw, krop donker, selout poten/snavel)
       (40, 38, 68),                                        # 4 navy donker (verre vleugel schaduw, penlijnen)
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
    "......1221224211..",  # 9
    ".....12224224221..",  # 10
    ".....12233423421..",  # 11
    "....122333423411..",  # 12
    "....123423342341..",  # 13
    "...1223342342341..",  # 14
    "...12233423342341.",  # 15
    "..12233334233441..",  # 16
    ".122333334333441..",  # 17
    "..12233333333344-1",  # 18
    "..1233333333444---",  # 19
    "..1443333333344---",  # 20
    "-----4333444444441",  # 21
    "----11334444444441",  # 22
    "---1..134444444444",  # 23
    "--1....13444444444",  # 24
    "--1.....1344444444",  # 25
    "-----1..1344444441",  # 26
    "---11....134444441",  # 27
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
    ".....11BBBBBBCD1..",  # 23
    ".....1BBBCDBCD1...",  # 24
    ".....1BCCCCDCC1...",  # 25
    ".....1CDDDDDDCCDD1",  # 26
    "....1BD1111DDDD11.",  # 27
    "...1BD1FFFF1DD1...",  # 28
    "....D1FFFEE21D1...",  # 29
    "....1FFFE1E31771..",  # 30
    "..111122FEE31671..",  # 31
    ".18888122331556711",  # 32
    ".711771111166665--",  # 33
    ".1..1877177666666-",  # 34
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
    ".............771.........331..",  # 51
    "............881..........71...",  # 52
    "..........781............71...",  # 53
    ".........781............371...",  # 54
    ".......77881............71....",  # 55
    "..7777888887775........371....",  # 56
    ".15888111..1111.......3777781.",  # 57
    "..1111............33337771111.",  # 58
    ".................77718771.....",  # 59
    "................1811.111......",  # 60
]
zone(16, 49, POOT)

# ---- bewijs ----
assert ((S10 > 0) == (B > 0)).all(), 'silhouet anders dan s10'
OOG = [(9, 29), (10, 29), (8, 30), (10, 30), (9, 31), (10, 31)]
assert all(B[y, x] == 14 for x, y in OOG) and B[30, 9] == 1 and (B == 14).sum() == 6
assert B.max() < 16
im = Image.fromarray(B.astype(np.uint8), 'P'); im.putpalette([c for p in PAL for c in p]); im.save('hoatzin.png', transparency=0)
im.convert('RGB').resize((512, 512), Image.NEAREST).save('hoatzin_8x.png')
with open('normal.pal', 'w') as f: f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % p for p in PAL))
print('silhouet anders dan s10: 0; oog gelijk; pixels anders dan s10:', int((S10 != B).sum()))
