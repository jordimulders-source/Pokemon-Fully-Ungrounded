# r13 (Jordi, 25 nov): "rechtsboven paneel moet nog wat hoger" = de tweeling achter de rechter zijarm.
# Vanuit r12: tweeling (en staafje) weghalen en opnieuw plaatsen met bewerk_r10.step_twin, 3 px (a) en 6 px (b) hoger.
# Plakken alleen op achtergrond, dus achterarm, zijarm en oogbol blijven ervoor; het staafje wordt vanzelf korter
# waar het achter de achterarm verdwijnt. Vrijgekomen pixels: wit (daar was in r9 achtergrond).
from PIL import Image
import numpy as np
import bewerk_r10 as b10

CROP = (19, 15)                     # r10..r12 = gepad canvas vanaf (19,15)
r12 = np.asarray(Image.open('r12_natief.png').convert('RGB')).astype(int)
h, w = r12.shape[:2]
r9pad = b10.new_canvas()

def make(dy, name):
    im = b10.Img()
    im.a = np.full_like(r9pad, 255)
    im.a[CROP[1]:CROP[1] + h, CROP[0]:CROP[0] + w] = r12
    # tweeling weg: alles in het tweelinggebied dat in r9 achtergrond was en nu niet
    n = 0
    for x in range(128, 215):
        for y in range(66, 115):
            X, Y = x + b10.PADL, y + b10.PADT
            if b10.is_white(r9pad[Y, X]) and not np.all(im.a[Y, X] >= 250):
                im.a[Y, X] = 255; n += 1
    b10.TWIN_T = (89, 38 - dy)
    b10.step_twin(im)
    out = im.a[CROP[1]:CROP[1] + h, CROP[0]:CROP[0] + w]
    diff = np.any(out != r12, axis=2)
    ys, xs = np.where(diff)
    print(name, 'weggehaald', n, 'gewijzigd', diff.sum(), 'in r9-x', xs.min() - 21, '..', xs.max() - 21,
          'y', ys.min() + 15, '..', ys.max() + 15)
    img = Image.fromarray(out.astype('uint8'))
    img.save(name + '.png'); img.resize((w * 8, h * 8), Image.NEAREST).save(name + '_8x.png')
    return img

a = make(3, 'r13a_natief')
b = make(6, 'r13b_natief')
box = (110, 30, 231, 125)
crops = [Image.fromarray(r12.astype('uint8')).crop(box), a.crop(box), b.crop(box)]
cw, ch = (box[2] - box[0]) * 8, (box[3] - box[1]) * 8
sh = Image.new('RGB', (cw * 3 + 32, ch), 'white')
for i, c in enumerate(crops): sh.paste(c.resize((cw, ch), Image.NEAREST), (i * (cw + 16), 0))
sh.save('r13_varianten.png')
