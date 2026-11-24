"""voor_na.png + bewijs diff 0 (alfa, gezicht, onderdelen). Draai vanuit de repo-root."""
from PIL import Image
D = 'docs/concept/sprites/gen3_studie/proef/vigiloot/'
v = Image.open('docs/concept/sprites/wasbeer/af/wasbeer.png'); n = Image.open(D + 'na.png')
vp, np_ = v.load(), n.load()
assert n.mode == 'P' and n.size == (64, 64) and len(set(n.getdata())) <= 16
# 1. silhouet
alfa = sum((vp[x, y] == 0) != (np_[x, y] == 0) for x in range(64) for y in range(64))
# 2. gezicht: masker, ogen, neus, snuit en de lijn eromheen (hele kop rij 0-19, x 9-33) + palet
gez = sum(vp[x, y] != np_[x, y] for x in range(9, 34) for y in range(0, 20))
pal = v.getpalette()[:48] == n.getpalette()[:48]
# 3. onderdelen: draagband, buidel, handen, buikvlek (indices 8-15, 3 en strap-kolommen) en staartringen-binnenkant
ond = [(x, y) for x in range(64) for y in range(64)
       if vp[x, y] != np_[x, y] and vp[x, y] in (8, 9, 10, 11, 12, 13, 14, 15)]
diff = [(x, y) for x in range(64) for y in range(64) if vp[x, y] != np_[x, y]]
print('alfa-diff', alfa, '| gezicht-diff', gez, '| palet gelijk', pal, '| onderdelen (8-F) gewijzigd', len(ond), '| totaal', len(diff))
# variant B: alleen paletkleur 5 donkerder; index-diff t.o.v. na.png moet 0 zijn
b = Image.open(D + 'na_variant_palet5.png'); bp = b.load()
print('variant B index-diff t.o.v. na', sum(bp[x, y] != np_[x, y] for x in range(64) for y in range(64)),
      '| B andere paletkleuren', [i for i in range(16) if b.getpalette()[3*i:3*i+3] != n.getpalette()[3*i:3*i+3]],
      '| index 5 in masker/ogen/neus (x9-25, y8-17)', sum(bp[x, y] == 5 for x in range(9, 26) for y in range(8, 18)))
# vel
refs = ['linoone', 'zigzagoon', 'ursaring', 'kangaskhan']
def rgba(im):
    p = im.getpalette(); px = im.load(); o = Image.new('RGB', (64, 64), (255, 255, 255)); oo = o.load()
    for x in range(64):
        for y in range(64):
            i = px[x, y]
            if i: oo[x, y] = tuple(p[3*i:3*i+3])
    return o
ims = [rgba(v), rgba(n), rgba(Image.open(D + 'na_variant_palet5.png'))] + [rgba(Image.open(f'graphics/pokemon/{s}/anim_front_gba.png').crop((0, 0, 64, 64))) for s in refs]
k = 6; g = 8
W = len(ims) * (64*k + g) + g
vel = Image.new('RGB', (W, 64*k + 64 + 3*g), (232, 232, 224))
for i, im in enumerate(ims):
    x = g + i*(64*k + g)
    vel.paste(im.resize((64*k, 64*k), Image.NEAREST), (x, g))
    vel.paste(im, (x, 64*k + 2*g))
vel.save(D + 'voor_na.png')
# diffkaart (rood = gewijzigd) op 8x
dk = rgba(n).convert('RGB'); dd = dk.load()
for (x, y) in diff: dd[x, y] = (255, 0, 0)
dk.resize((512, 512), Image.NEAREST).save(D + 'diffkaart.png')
