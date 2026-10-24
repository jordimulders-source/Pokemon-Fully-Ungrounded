"""Kolibrie silhouet v5 (Jordi, 24 okt: "kijk heel goed naar de anatomie en ga niet gokken").
Het lijf, de kop en de vleugels komen nu letterlijk uit Jordi's anatomiefoto
(`referenties/jordi_anatomie_mango.png`): het silhouet is uit de foto gesneden (achtergrond geschat en
afgetrokken), gespiegeld en 60 graden gedraaid naar de pose van Jordi's eerste schets (kop linksonder,
snavel schuin omlaag, vleugels omhoog, staart naar rechtsonder). Alleen de staart (mango-waaier) en de
pootjes gaan eruit; daarvoor in de plaats franje + drie slierten met Articuno-krul, en de jeguaka.
Anatomie volgens de foto: beide vleugels zitten met een brede aanzet op de rug net achter de nek
(geen gat), wijzen van de kop af, stompe/rechte punten, ongeveer zo lang als het lijf; kleine kop
met platte kruin die recht doorloopt in de snavel; slanke nek."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from silhouet import catmull, tube, SS, HERE

REF = os.path.join(HERE, '..', 'referenties', 'jordi_anatomie_mango.png')
ANG = 60          # draaiing tegen de klok in, na spiegelen
BOX = 64


def segment():
    im = Image.open(REF).convert('RGB')
    a = np.array(im).astype(float)
    m = np.zeros(a.shape[:2], bool)
    for _ in range(4):
        w = (~m).astype(float)
        num = np.stack([np.array(Image.fromarray((a[..., c] * w).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))).astype(float)
                        for c in range(3)], -1)
        den = np.array(Image.fromarray((w * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))).astype(float) / 255
        bg = num / np.maximum(den[..., None], 1e-3)
        m = np.abs(a - bg).sum(-1) > 45
        m = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))) > 0
    return m


def transform(img):
    """Spiegelen en draaien; hetzelfde voor masker en markeringen."""
    return img.transpose(Image.FLIP_LEFT_RIGHT).rotate(ANG, resample=Image.BILINEAR, expand=True)


def build():
    m = segment()
    H, W = m.shape
    yy, xx = np.mgrid[0:H, 0:W]
    # staart (mango-waaier) en pootjes eruit; staartwortel en kruin onthouden als markering
    m &= ~((yy > 455) & (xx < 520))
    m &= ~((yy > 438) & (xx > 492) & (xx < 540))
    marks = {'staart': (452, 452), 'kruin': (565, 228)}
    body = Image.fromarray((m * 255).astype(np.uint8))
    tb = transform(body)
    pts = {}
    for k, (x, y) in marks.items():
        mk = Image.new('L', (W, H), 0)
        ImageDraw.Draw(mk).ellipse([x - 6, y - 6, x + 6, y + 6], fill=255)
        t = np.array(transform(mk)) > 100
        ys, xs = np.nonzero(t)
        pts[k] = (xs.mean(), ys.mean())
    # schalen: vogel zonder slierten ±52 px breed, in een 64-box, ruimte rechtsonder voor de slierten
    bb = tb.getbbox()
    k = 52 / (bb[2] - bb[0])
    ox, oy = 1 - bb[0] * k, 2 - bb[1] * k
    big = tb.resize((int(tb.width * k * SS), int(tb.height * k * SS)), Image.BILINEAR)
    canvas = Image.new('L', (BOX * SS, BOX * SS), 0)
    canvas.paste(big, (int(ox * SS), int(oy * SS)))
    P = {n: (x * k + ox, y * k + oy) for n, (x, y) in pts.items()}
    d = ImageDraw.Draw(canvas)
    # jeguaka op de kruin: drie korte veertjes, naar achteren (van de snavel af)
    cx, cy = P['kruin']
    for dx, dy in ((1.0, -4.5), (3.5, -3.8), (5.5, -2.0)):
        tube(d, [(cx, cy), (cx + dx * 0.5, cy + dy * 0.55), (cx + dx, cy + dy)], 2.4, 1.3)
    # staart: franje + drie slierten met Articuno-krul en racketpunt
    tx, ty = P['staart']
    for a in (-10, 20, 50):
        r = math.radians(a)
        tube(d, [(tx, ty), (tx + math.cos(r) * 7, ty + math.sin(r) * 7)], 3.0, 1.8)
    ribbons = [[(tx, ty), (tx + 9, ty - 2), (tx + 15, ty + 3), (tx + 15, ty + 9), (tx + 11, ty + 11)],
               [(tx, ty), (tx + 7, ty + 4), (tx + 10, ty + 11), (tx + 7, ty + 16), (tx + 2, ty + 17)],
               [(tx, ty), (tx + 3, ty + 7), (tx + 2, ty + 14), (tx - 2, ty + 18)]]
    for rb in ribbons:
        tube(d, rb, 1.8, 1.3)
        (px, py), (x, y) = rb[-2], rb[-1]
        a = math.atan2(y - py, x - px)
        tube(d, [(x, y), (x + math.cos(a) * 3.5, y + math.sin(a) * 3.5)], 1.6, 4.4)
    m64 = np.array(canvas.resize((BOX, BOX), Image.BOX)) > 110
    return m64, P


if __name__ == '__main__':
    m, P = build()
    print({k: (round(x, 1), round(y, 1)) for k, (x, y) in P.items()})
    sil = np.zeros((64, 64, 4), np.uint8); sil[m] = (40, 30, 60, 255)
    S = Image.fromarray(sil)
    ref = Image.open(REF).convert('RGB')
    rt = transform(ref.convert('RGBA'))
    rt = rt.crop(rt.getbbox()); rt.thumbnail((256, 256))
    Wd = Image.new('RGB', (256 * 3 + 64 + 50, 280), (236, 236, 230))
    Wd.paste(rt, (0, 0), rt)
    v4 = Image.open(os.path.join(HERE, 'silhouet_v4_1x.png')).resize((256, 256), Image.NEAREST)
    Wd.paste(v4, (266, 0), v4)
    S4 = S.resize((256, 256), Image.NEAREST)
    Wd.paste(S4, (532, 0), S4)
    Wd.paste(S, (800, 20), S)
    dr = ImageDraw.Draw(Wd)
    for x, t in ((0, 'foto, gespiegeld + gedraaid'), (266, 'v4 (vorige)'), (532, 'v5 4x'), (800, '1x')):
        dr.text((x + 2, 262), t, fill='black')
    Wd.save(os.path.join(HERE, 'silhouet_v5.png'))
    S.save(os.path.join(HERE, 'silhouet_v5_1x.png'))
