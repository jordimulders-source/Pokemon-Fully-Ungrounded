"""v15: lijf zonder manen rechts dicht en rond (Jordi 16 nov: "nu moet je zonder manen na nog fixen").
Rechtsonder lag de voet-maan over de bol: rand rij 50-54 was 47,43,42(open),42(open),41(open).
Ellips die de onaangetaste omtrek volgt (zelfde als v14 links): x = 29.5 + 22.5*sqrt(1-((y-34)/24)^2)
-> rij 49..57: 47.1 46.3 45.4 44.4 43.2 41.9 40.4 38.5 35.9 -> rand 47,46,45,44,43,42,40,38,36.
Rij 55-57 (40,38,36) en rij 49 (47) klopten al; alleen rij 50-54 aangevuld.
Rechts onder de gasarm (rij 21-23): losse lijnpixel (53,22) met gat (51-52,22) en open rand (50,23);
omlijning loopt nu diagonaal (53,21)->(52,22)->(51,23)->(51,24).
Alleen bestaande indexen; buurtinten doorgetrokken (donkere band 2 rij 50-52), omlijning index 1."""
from PIL import Image
import numpy as np, os
D = os.path.dirname(os.path.abspath(__file__))
BRON = os.path.join(D, '..', 'sprite_v14', 'lijf_zonder_manen_v14.png')
ZONES = [(40, 48, 49, 56),   # rechtsonder x0..x1, y0..y1 incl.
         (50, 54, 20, 24)]   # onder de gasarm
EDIT = {
    # rechtsonder
    (47, 50): 0,  # platte snede (lijn 45-47) wordt rand 46
    (45, 50): 2,  # donkere band loopt door tot de rand
    (43, 51): 2,  # oude maangrens-lijn wordt binnenkant (band 2)
    (44, 51): 2,
    (45, 51): 1,  # omlijning rij 51
    (43, 52): 2,  # band 2 doorgetrokken
    (44, 52): 1,  # omlijning rij 52
    (43, 53): 1,  # omlijning rij 53 (band 5 eindigt op 42 zoals al stond)
    (41, 54): 1,  # open rand (lichte 5 op de buitenrand) wordt omlijning
    (42, 54): 1,  # omlijning rij 54, sluit diagonaal aan op (40,55)
    # onder de gasarm
    (51, 22): 2,  # gat dicht met arm-tint
    (52, 22): 1,  # omlijning diagonaal
    (53, 22): 0,  # losse lijnpixel weg
    (51, 23): 1,  # open rand dicht
}

def inzone(x, y):
    return any(x0 <= x <= x1 and y0 <= y <= y1 for x0, x1, y0, y1 in ZONES)

def rand(a):
    return {y: int(np.nonzero(a[y])[0][-1]) for y in range(64) if a[y].any()}

im = Image.open(BRON); a = np.array(im); b = a.copy()
for (x, y), v in EDIT.items():
    assert inzone(x, y); assert a[y, x] != v, (x, y)
    b[y, x] = v
d = np.argwhere(a != b)
for y, x in d: assert inzone(x, y), (x, y)
assert len(d) == len(EDIT)
assert set(np.unique(b)) <= set(np.unique(a))
# gezicht/ogen/grijns/oren/linkerkant pixel voor pixel gelijk
assert (a[:, :40] == b[:, :40]).all()
assert (a[:20] == b[:20]).all() and (a[25:49] == b[25:49]).all() and (a[57:] == b[57:]).all()
# geen open rand rechtsonder: laatste pixel per rij 44-57 is omlijning
for y in range(44, 58): assert b[y, rand(b)[y]] == 1, y
# geen losse pixels in de zones (elke niet-achtergrondpixel heeft een 4-buur die niet-achtergrond is)
for x0, x1, y0, y1 in ZONES:
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if b[y, x]:
                assert any(b[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), (x, y)
out = Image.fromarray(b, 'P'); out.putpalette(im.getpalette())
out.save(os.path.join(D, 'lijf_zonder_manen_v15.png'))
print('gewijzigd:', len(d), sorted((int(x), int(y), int(a[y, x]), int(b[y, x])) for y, x in d))
ra, rb = rand(a), rand(b)
print('rij: rechts-x voor -> na (ellips)')
for y in list(range(20, 25)) + list(range(46, 58)):
    e = 29.5 + 22.5 * np.sqrt(max(0, 1 - ((y - 34) / 24) ** 2))
    print('  %d: %d -> %d   (%.1f, laatste index %d -> %d)' % (y, ra[y], rb[y], e, a[y, ra[y]], b[y, rb[y]]))

# 8x op wit
pal = im.getpalette()
def rgb(arr, wit=False):
    p = Image.fromarray(arr, 'P'); p.putpalette(pal); r = p.convert('RGB')
    if wit:
        m = Image.fromarray(((arr == 0) * 255).astype('uint8'))
        r.paste((255, 255, 255), mask=m)
    return r
def groot(arr, s, box=None, wit=False):
    r = rgb(arr, wit)
    if box: r = r.crop(box)
    return r.resize((r.width * s, r.height * s), Image.NEAREST)
groot(b, 8, wit=True).save(os.path.join(D, 'lijf_zonder_manen_v15_8x.png'))
# vel: boven v14 | v15 op 8x; onder uitsneden 16x (rechtsonder en gasarm)
box1 = (34, 44, 52, 59); box2 = (44, 16, 58, 28)
z = [groot(a, 16, box1), groot(b, 16, box1), groot(a, 16, box2), groot(b, 16, box2)]
W = 2 * 512 + 3 * 8
H = 8 + 512 + 8 + max(t.height for t in z) + 8
W = max(W, 8 + sum(t.width + 8 for t in z))
vel = Image.new('RGB', (W, H), (40, 40, 40))
vel.paste(groot(a, 8), (8, 8)); vel.paste(groot(b, 8), (528, 8))
x = 8
for t in z: vel.paste(t, (x, 528)); x += t.width + 8
vel.save(os.path.join(D, 'voor_na.png'))
