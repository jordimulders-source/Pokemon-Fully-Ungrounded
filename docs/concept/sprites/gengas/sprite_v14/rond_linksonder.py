"""v14: bol linksonder de mond rond maken (Jordi 16 nov: "linksonder de mond is ook een puntje").
Linkerrand rij 52-54 was 15,15,18 (knik + sprong van 3); wordt 15,16,17 = de ellips
x = 29.5 - 22.5*sqrt(1-((y-34)/24)^2) die de rest van de bol volgt. Alleen bestaande indexen."""
from PIL import Image
import numpy as np, os
D = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(D, '..')
ZONE = (5, 18, 36, 55)  # x0..x1, y0..y1 incl.; opdracht zei "ongeveer x 5-16", de rand loopt hier tot x 17
EDIT = {(15, 53): 0,   # puntje weg (achtergrond)
        (17, 53): 5,   # binnenkant: lichte onderband (index 5) loopt door zoals (18,53)
        (17, 54): 1}   # omlijning schuift 1 px naar links: rand 16,17 i.p.v. 15,18

def rand(a):
    return {y: int(np.nonzero(a[y])[0][0]) for y in range(36, 60) if a[y].any()}

def doe(bron, doel, maan_voor=False):
    im = Image.open(bron); a = np.array(im); b = a.copy()
    for (x, y), v in EDIT.items():
        assert ZONE[0] <= x <= ZONE[1] and ZONE[2] <= y <= ZONE[3]
        b[y, x] = v
    d = np.argwhere(a != b)
    for y, x in d:
        assert ZONE[0] <= x <= ZONE[1] and ZONE[2] <= y <= ZONE[3], (x, y)
    assert set(np.unique(b)) <= set(np.unique(a))
    # linkermaan (grijs, x0-11, rij 41-52) onaangeroerd
    assert (a[41:53, 0:12] == b[41:53, 0:12]).all()
    out = Image.fromarray(b, 'P'); out.putpalette(im.getpalette()); out.save(doel)
    print(os.path.basename(doel), 'gewijzigd:', len(d), [(int(x), int(y)) for y, x in d])
    if not maan_voor:
        ra, rb = rand(a), rand(b)
        print(' rij: links-x voor -> na')
        for y in range(44, 59): print('  %d: %d -> %d' % (y, ra[y], rb[y]))
    return a, b

a1, b1 = doe(os.path.join(G, 'af/gengas.png'), os.path.join(D, 'gengas_v14.png'), True)
a2, b2 = doe(os.path.join(G, 'frame2/lijf_zonder_manen.png'), os.path.join(D, 'lijf_zonder_manen_v14.png'))

# vel: voor/na 8x + uitsnede 16x van de zone
pal = Image.open(os.path.join(G, 'af/gengas.png')).getpalette()
def rgb(arr):
    im = Image.fromarray(arr, 'P'); im.putpalette(pal); return im.convert('RGB')
def groot(arr, s, box=None):
    im = rgb(arr)
    if box: im = im.crop(box)
    return im.resize((im.width * s, im.height * s), Image.NEAREST)
box = (2, 40, 26, 60)
tiles = [groot(a1, 8), groot(b1, 8), groot(a2, 8), groot(b2, 8)]
zoom = [groot(a1, 16, box), groot(b1, 16, box), groot(a2, 16, box), groot(b2, 16, box)]
W = 4 * 512 + 5 * 8; H = 512 + zoom[0].height + 24
vel = Image.new('RGB', (W, H), (40, 40, 40))
for i, t in enumerate(tiles): vel.paste(t, (8 + i * 520, 8))
for i, t in enumerate(zoom): vel.paste(t, (8 + i * 520, 528))
vel.save(os.path.join(D, 'voor_na.png'))
