"""Wasbeer silhouet (ronde 1 -> ronde 2: gespiegeld, armen en koevoeten korter): omtrek van foto 10 (omtrek.py) direct verkleind naar 64x64, met alleen twee
benoemde aanpassingen (Jordi, 2 nov): (1) klauwen = koevoet (2 klauwen tegen elkaar, rechte steel + J-bocht),
(2) staart eindigt in een haak omhoog. Alles in fotocoördinaten, dan verkleind (massa van de foto).
Draaien: python3 docs/concept/sprites/wasbeer/silhouet/silhouet.py -> ronde1.txt, ronde1_1x.png, vel_ronde1.png"""
import os
import numpy as np
from PIL import Image, ImageDraw
from omtrek import HERE, FOTO, POLYS, ARM_NEAR, ARM_FAR, tube

# dunne delen (SPRITE_WERKWIJZE stap 2): onderarmen op 64 minstens 3-4 px dik, koevoetsteel minstens 2 px
# ronde 2 (Jordi): armen + klauwen iets korter; alles gespiegeld (kijkt naar links, zoals frontsprites)
ARM_NEAR = [(x, y, max(r * 1.45, 11)) for x, y, r in ARM_NEAR[:-1]] + [(306, 239, 11)]
ARM_FAR = [(x, y, max(r * 1.45, 10)) for x, y, r in ARM_FAR[:-1]] + [(362, 179, 10)]

SS = 8
TOP, H = 2, 60          # hoogte van de figuur op 64
# koevoeten (fotocoördinaten, straal ≥ 6 zodat de steel op 64 ≥ 2 px blijft)
CROW_NEAR = [(308, 242, 9), (318, 254, 8.5), (328, 264, 8), (340, 268, 7.5), (348, 262, 7), (350, 252, 6.5)]   # schuin vooruit-omlaag, haak omhoog naar voren   # omlaag, haak naar voren
CROW_FAR = [(366, 180, 9), (382, 183, 8.5), (396, 187, 8), (406, 195, 7.5), (406, 206, 7), (398, 213, 6.5)]   # vooruit, haak omlaag
# staart: de punt van de foto eraf, haak omhoog terug naar het lijf
TAIL_HOOK = [(90, 270, 14), (70, 266, 12), (52, 256, 10.5), (44, 238, 9.5), (50, 222, 8.5), (64, 216, 7.5), (76, 222, 6.5)]
VARIANTS = {'foto': False, 'ronde1': True}


def build(mods=True):
    pts = [p for poly in POLYS.values() for p in poly]
    extra = ARM_NEAR + ARM_FAR + ((CROW_NEAR + CROW_FAR + TAIL_HOOK) if mods else [])
    ys = [p[1] for p in pts] + [y - r for x, y, r in extra] + [y + r for x, y, r in extra]
    xs = [p[0] for p in pts] + [x - r for x, y, r in extra] + [x + r for x, y, r in extra]
    k = H / (max(ys) - min(ys))
    ox = (64 - (max(xs) - min(xs)) * k) / 2 - min(xs) * k
    oy = TOP - min(ys) * k
    im = Image.new('L', (64 * SS, 64 * SS), 0)
    d = ImageDraw.Draw(im)
    for name, poly in POLYS.items():
        if mods and name == 'staart':
            poly = [p for p in poly if p[0] > 85]
        d.polygon([((x * k + ox) * SS, (y * k + oy) * SS) for x, y in poly], fill=255)
    for t in [ARM_NEAR, ARM_FAR] + ([CROW_NEAR, CROW_FAR, TAIL_HOOK] if mods else []):
        tube(d, t, k * SS, ox * SS, oy * SS)
    small = (np.array(im.resize((64, 64), Image.BOX)) >= 128)[:, ::-1]   # gespiegeld
    return small, (k, ox, oy)


def save_txt(a, path):
    open(path, 'w').write('\n'.join(''.join('#' if v else '.' for v in row) for row in a) + '\n')


if __name__ == '__main__':
    a0, _ = build(False)
    a1, (k, ox, oy) = build(True)
    save_txt(a1, os.path.join(HERE, 'ronde2.txt'))
    one = Image.fromarray(np.where(a1, 0, 255).astype(np.uint8))
    rgba = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); rgba.putalpha(Image.fromarray((a1 * 255).astype(np.uint8)))
    blk = Image.new('RGBA', (64, 64), (34, 30, 30, 255)); blk.putalpha(Image.fromarray((a1 * 255).astype(np.uint8)))
    blk.save(os.path.join(HERE, 'ronde2_1x.png'))
    # vel: foto (uitsnede) | silhouet 4x | silhouet over de foto | 1x | Gen 3-referenties
    S = 4
    foto = Image.open(FOTO).convert('RGB')
    x0, y0 = -ox / k, -oy / k
    crop = foto.transform((64 * S, 64 * S), Image.AFFINE, (1 / (k * S), 0, x0, 0, 1 / (k * S), y0), Image.BICUBIC, fillcolor=(235, 235, 235))
    crop = crop.transpose(Image.FLIP_LEFT_RIGHT)
    sil = blk.resize((64 * S, 64 * S), Image.NEAREST)
    over = crop.convert('RGBA').copy()
    m = Image.new('RGBA', (64 * S, 64 * S), (255, 0, 255, 0))
    a_big = np.array(sil)[..., 3] > 0
    edge = a_big ^ (np.roll(a_big, 1, 0) & np.roll(a_big, -1, 0) & np.roll(a_big, 1, 1) & np.roll(a_big, -1, 1))
    ov = np.zeros((64 * S, 64 * S, 4), np.uint8); ov[a_big] = (255, 0, 255, 60); ov[edge] = (255, 0, 255, 255)
    over = Image.alpha_composite(over, Image.fromarray(ov))
    refs = []
    for n in ('linoone', 'zangoose', 'sneasel', 'ursaring'):
        p = os.path.join(HERE, '../../../../../graphics/pokemon', n, 'anim_front.png')
        if os.path.exists(p):
            r = Image.open(p).convert('RGBA').crop((0, 0, 64, 64)); bg = r.getpixel((0, 0)); a = np.array(r); a[(a[..., :3] == bg[:3]).all(-1), 3] = 0; refs.append((n, Image.fromarray(a)))
    W = 20 + (64 * S + 20) * 3 + 100 + 80 * len(refs)
    sheet = Image.new('RGB', (W, 64 * S + 60), (236, 234, 228))
    d = ImageDraw.Draw(sheet)
    x = 20
    for lab, img in (('foto 10 (onderlaag)', crop), ('silhouet ronde 2 (4x)', sil), ('silhouet over de foto', over)):
        sheet.paste(img, (x, 40), img if img.mode == 'RGBA' else None); d.text((x, 20), lab, fill=(30, 30, 30)); x += 64 * S + 20
    sheet.paste(blk, (x, 40), blk); d.text((x, 20), f'1x ({int(a1.sum())} px)', fill=(30, 30, 30)); x += 100
    for n, r in refs:
        sheet.paste(r, (x, 40), r); d.text((x, 110), n, fill=(30, 30, 30)); x += 80
    sheet.save(os.path.join(HERE, 'vel_ronde2.png'))
    print(int(a0.sum()), int(a1.sum()))
