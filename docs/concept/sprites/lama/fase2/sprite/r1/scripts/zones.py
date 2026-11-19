def _rand(y, x): return any(a[yy, xx] == 0 for yy, xx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)))
# zones voor bewerk.py: (rij, x_start, tekens)

# --- handschoenen (r3, op de voorvoeten); vorm/tinten naar de verkleinde r3-handschoen
zet('handschoen', [
 (52, 25, '131'),                       # verre voorpoot boven de polsband
 (53, 17, '1541'), (53, 24, '1dee1'),
 (54, 16, '1ddde1'), (54, 23, '1deeee1'),
 (55, 15, '1dddee1'), (55, 23, '1eeee1'),
 (56, 13, '111deee1'), (56, 23, '1888771'),
 (57, 12, '19998887'), (57, 20, '1'), (57, 22, '18888771'),
 (58, 12, '199888871'), (58, 22, '1887771'),
 (59, 12, '188888771'), (59, 22, '1777771'),
 (60, 12, '17777771'), (60, 23, '13131'),
 (61, 12, '1651651'), (61, 23, '11111'),
 (62, 13, '11111'),
], wis=(53, 62, 11, 31))

# --- achterpoten (r12-gang): buitenlijn 1 px om een vulling; nabij licht, ver donker
zet('achterpoten', [
 (50, 37, '1331'), (51, 37, '1431'), (52, 37, '1541'),
 (53, 36, '1541'), (54, 36, '1541'), (55, 36, '151'), (56, 35, '151'), (57, 34, '151'),
 (58, 33, '151'), (59, 32, '1111'),
 (50, 45, '11321'),
 (51, 47, '1321'), (52, 48, '1321'), (53, 49, '131'), (54, 49, '131'), (55, 50, '131'),
 (56, 50, '131'), (57, 51, '131'), (58, 51, '131'), (59, 51, '131'), (60, 51, '131'), (61, 51, '111'),
], wis=(50, 62, 32, 56))

# --- oren en kwastjes (r4): rechteroor lichte rand + donkere binnenkant, kwastjes rood met licht linksboven
zet('oren', [
 (2, 20, '1221'), (3, 20, '1421'), (4, 20, '14287'), (5, 20, '142897'), (6, 20, '1428987'),
 (7, 20, '1428887'), (8, 20, '342777'),
 (5, 12, '9'), (6, 12, '9'),
])

# --- gezicht (r4): zwaar vlak ooglid, oogwit + iris + pupil, neusgat, platte mond; licht op de snuit
zet('gezicht', [
 (11, 16, '33333'),
 (12, 18, '33'),
 (13, 17, '1111'), (13, 12, '5'),
 (14, 17, '6216'), (14, 11, '55'),
 (15, 11, '2'),
 (17, 12, '222'),
])

# --- rugkleed (r4): randen gemeten op het model (linksboven (27.4, 26.5) -> linksonder (31.7, 39.7),
# rechtsboven (39.6, 26.5) -> rechtsonder (42.4, 39.4)); rood met verticale aguayo-strepen langs de schuine rand,
# licht linksboven, donker rechts en onder; kwastjes op de onderhoeken (32.5, 40.5) en (42.5, 40)
regels = []
for y in range(25, 42):          # oude kleedresten -> vacht
    for x in range(26, 46):
        if a[y, x] in (7, 8, 9) or (a[y, x] == 1 and not _rand(y, x)): regels.append((y, x, '4'))
zet('kleed', regels)
regels = []
for y in range(26, 40):
    L = int(round(27.4 + (y - 26.5) * (4.3 / 13.2))); R = int(round(39.6 + (y - 26.5) * (2.8 / 12.9)))
    for x in range(L, R + 1):
        if a[y, x] == 0: continue
        if y in (26, 39) or x in (L, R): k = '1'
        else:
            off = x - L
            # tonen gemeten op het model (1x): boven (rij 27-31) lum 100-115 -> licht, onder (32-37) 65-80 -> midden;
            # onderrand en rechterrand donker; twee donkere strepen als aguayo-patroon (posities: voorstel maker)
            if y == 38 or x == R - 1: k = '7'
            elif off in (3, 7): k = '7' if y >= 32 else '8'
            else: k = '9' if y <= 31 else '8'
        regels.append((y, x, k))
regels += [(40, 32, '87'), (41, 32, '77'), (40, 42, '87'), (41, 42, '7')]
zet('kleed', regels)

# --- halsband en pompons (r4; toegestane afwijking 5: strepen ±1 px, pompons als stipjes met donkere rand)
# band: middellijn van het model gemeten van (13.5, 30.3) tot (25, 26); strepen rood/geel/groen, donkere rand onder
regels = []
for y in range(25, 36):          # oude bandresten in de hals terug naar vacht (niet de silhouetrand, niet het kleed)
    for x in range(12, 27):
        if a[y, x] in (7, 8, 9, 10, 11, 12, 1, 2) and not _rand(y, x) and not (x >= 25 and y <= 26):
            regels.append((y, x, '4'))
zet('halsband', regels)
regels = []
for x in range(13, 27):
    c = 30.3 - (x - 13.5) * (4.3 / 11.5)
    t = int(round(c - 1.5))
    for yy, k in ((t, '9' if x < 20 else '8'), (t + 1, 'a'), (t + 2, 'b')):
        if a[yy, x] != 0 and not _rand(yy, x): regels.append((yy, x, k))   # binnen het silhouet; rand blijft buitenlijn
# pompons: 2x2 kleur, donkere rand rechts en onder, draadje naar de band
for (cx, cy, k) in ((12, 32, '9'), (15, 33, 'a'), (19, 32, 'b'), (23, 30, 'c'), (26, 28, '8')):
    regels += [(cy, cx, k + k + '1'), (cy + 1, cx, k + k + '1'), (cy + 2, cx, '111')]
zet('halsband', regels)
# linkerpompon steekt buiten de hals: rand links
zet('halsband', [(32, 11, '1'), (33, 11, '1')])

# --- losse resten: rest van de oude kleedrand boven het kleed weg; rechterpompon licht linksboven tegen het kleed
zet('kleed', [(25, 36, '..')])
zet('halsband', [(28, 26, '9')])

# --- wolcontouren (r4): binnenlijnen waar het model een lijn heeft (>=20% lijnpixels in het blok) binnen de vacht
# van romp/voorpoot (rij 30-48), als donkere vachttoon 2; alleen lijnstukken van >=3 px (geen ruis)
import numpy as _np
from reduceer import klassen as _kl, S as _S, X0 as _X0, Y0 as _Y0, COLS as _C, MODEL as _M
_m = _np.asarray(Image.open(_M).convert('RGB')).astype(int); _K = _kl(_m)['drk']; _ox = (64 - _C) // 2
_cand = _np.zeros(a.shape, bool)
for y in range(30, 49):
    for x in range(10, 56):
        if a[y, x] not in (3, 4, 5) or _rand(y, x): continue
        ya, yb = int(round(_Y0 + (y - 1) * _S)), int(round(_Y0 + y * _S)); xa, xb = int(round(_X0 + (x - _ox) * _S)), int(round(_X0 + (x - _ox + 1) * _S))
        if _K[ya:yb, xa:xb].mean() >= 0.20: _cand[y, x] = True
regels = []
for y, x in zip(*_np.nonzero(_cand)):
    if _cand[max(y-2,0):y+3, max(x-2,0):x+3].sum() >= 3 and not any(a[yy, xx] in (7, 8, 9) for yy in range(y-1, y+2) for xx in range(x-1, x+2)):
        regels.append((y, x, '2'))
zet('wol', regels)
