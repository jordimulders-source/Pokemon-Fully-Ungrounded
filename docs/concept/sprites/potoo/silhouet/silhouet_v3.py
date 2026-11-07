"""Great potoo silhouet v3 (Jordi, 5 nov: optie 1, op een onzichtbare tak).
Bron: referenties/jordi_great_potoo_tak_bek_open_volledig.png (335x597). De omtrek is punt voor punt
overgenomen in fotocoördinaten (raster_foto.png / raster_kop.png), niet verzonnen. De tak is weggelaten;
klauwen verborgen (Jordi). Daarna: LEAN graden voorover gekanteld (Jordi: "licht vooruit hangt") en
gespiegeld (Gen 3-frontsprites kijken naar links).
v2: muil overdreven open (V-inkeping, onderkaak zakt naar voren, zoals het drieluik) zodat de bek op 64 leest.
v3: muil nog verder open (onderkaak hangt, zoals het drieluik boven) en kop 15% groter (Pokémon-verhouding; de echte vogel heeft geen nek).
Uitvoer: silhouet_v3_1x.png (64x64), model_v3.png (de foto zelf, uitgesneden langs dezelfde omtrek)."""
import os, math
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(HERE, '..', 'referenties', 'jordi_great_potoo_tak_bek_open_volledig.png')

# met de klok mee vanaf de kruin: kop, muil (rechts), borst/buik rechts, staart, rug/vleugel links
OMTREK = [(150, 127), (168, 122), (188, 122), (207, 127), (223, 138), (235, 153), (239, 167), (241, 178),
          (250, 178), (208, 200), (252, 234), (232, 248), (233, 240), (236, 255), (236, 275), (235, 300),
          (233, 330), (229, 355), (224, 380), (217, 402), (206, 422), (192, 438), (176, 452), (163, 470),
          (156, 495), (150, 525), (145, 552), (139, 575), (129, 591), (117, 594), (105, 586), (95, 566),
          (87, 540), (80, 510), (75, 480), (68, 440), (62, 400), (56, 360), (54, 320), (57, 290), (63, 265),
          (75, 240), (92, 212), (107, 185), (118, 163), (130, 145), (140, 134)]
LEAN = 10          # graden voorover (kop naar de kijkrichting)
HOOGTE = 60        # px op 64; formaat volgt de vorm (zie Noctowl/Xatu)
SS = 8


def kantel(p, c, a):
    r = math.radians(a); x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(r) - y * math.sin(r), c[1] + x * math.sin(r) + y * math.cos(r))


def main():
    c = (150, 450)  # draaipunt: waar hij op de (weggelaten) tak zit
    kop = lambda p: (190 + (p[0] - 190) * 1.15, 205 + (p[1] - 205) * 1.15) if p[1] < 250 else p
    pts = [kantel(kop(p), c, LEAN) for p in OMTREK]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = HOOGTE / (max(ys) - min(ys))
    w = (max(xs) - min(xs)) * k
    ox, oy = (64 - w) / 2 - min(xs) * k, 64 - 2 - HOOGTE - min(ys) * k
    T = lambda p: ((p[0] * k + ox) * SS, (p[1] * k + oy) * SS)
    im = Image.new('L', (64 * SS, 64 * SS), 0)
    ImageDraw.Draw(im).polygon([T(p) for p in pts], fill=255)
    sil = im.resize((64, 64), Image.BOX).point(lambda v: 255 if v >= 128 else 0)
    sil = sil.transpose(Image.FLIP_LEFT_RIGHT)
    sil.save(os.path.join(HERE, 'silhouet_v3_1x.png'))
    print('pixels:', sum(1 for v in sil.getdata() if v), 'breedte:', round(w, 1))

    # model: de foto zelf langs dezelfde omtrek, dezelfde kanteling en spiegeling
    foto = Image.open(FOTO).convert('RGBA')
    mask = Image.new('L', foto.size, 0); ImageDraw.Draw(mask).polygon(OMTREK, fill=255)
    from PIL import ImageFilter; mask = mask.filter(ImageFilter.MinFilter(5)); foto.putalpha(mask)
    groot = foto.resize((foto.width * 3, foto.height * 3), Image.LANCZOS)
    groot = groot.rotate(-LEAN, resample=Image.BICUBIC, center=(c[0] * 3, c[1] * 3), expand=False)
    groot = groot.crop(groot.getbbox()).transpose(Image.FLIP_LEFT_RIGHT)
    groot.save(os.path.join(HERE, 'model_v3.png'))


if __name__ == '__main__':
    main()
