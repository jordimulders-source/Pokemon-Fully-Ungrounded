"""Ronde 10: Jordi's rode vormen zijn grenzen (Jordi: "ik bedoel dat ik cirkels heb getekend met de vraag of je daar
binnen wil blijven" / "daar is de ruimte waar je in kan proberen te werken"). Vanuit ronde 9:
- rechts: alles in de pootzone buiten de lange lus weg (achterlijf naar rechts, R1, klauwtjes); S blijft binnen de lus
  en staat op y56 (de lus loopt onderaan tot y57, dus de klauwtjes passen alleen op y56);
- midden: blijft binnen de U-vormen (al zo in ronde 9);
- links: de linkerrand loopt van de borst (x17, y39-40) langs x17/x16 naar de linkervoorpoot (x16, y52), niets erbuiten.
Voorpoten (pixels van ronde 6) ongewijzigd. Schrijft raster.txt."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde9/raster.txt'))][:64]
def zet(y, x0, s):
    for i, c in enumerate(s): R[y][x0 + i] = c
# links: x <= 15 (rij 41-51) leeg, nieuwe rand
for y in range(41, 52):
    for x in range(0, 16): R[y][x] = '.'
for y in (41, 42, 43): R[y][16] = '.'; R[y][17] = '2'
for y in range(44, 52): R[y][16] = '2'
# rechts: x >= 42 in rij 45-58 leeg (de vleugel ligt op rij <= 44)
for y in range(45, 59):
    for x in range(42, 50): R[y][x] = '.'
zet(45, 39, "431"); zet(46, 40, "41"); zet(47, 40, "41"); zet(48, 40, "41"); zet(49, 40, "41")
zet(50, 39, "431"); zet(51, 38, "4431"); zet(52, 41, "1")
R8 = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde8/raster.txt'))][:64]
# inham onder de vleugel: buiten de lus terug naar ronde 8 (transparant), binnen de lus alleen de bovenrand van S
for y in range(41, 45):
    for x in range(39, 44): R[y][x] = R8[y][x]
zet(44, 39, "22")
R[55][41] = '.'; R[56][41] = '.'
zet(52, 23, "11")  # onderrand van de buik zoals in ronde 6 (net links van de U)
# S: onderkant op y55, punt 121, 2 klauwtjes op y56 (binnen de lus)
zet(55, 36, "11211")
zet(56, 35, "..b.b.")
zet(57, 36, ".....")
zet(58, 37, "...")
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
