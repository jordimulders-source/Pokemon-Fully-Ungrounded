"""Driekwart kop van foto 6 (referenties/foto6_kaaiman_buit.webp, 1440x1440), punt voor punt overgenomen.
De kop kijkt naar de camera met de snuit links-omlaag (driekwart). Controle: python3 kop6.py -> controle_kop6.png"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
FOTO6 = os.path.join(HERE, '../referenties/foto6_kaaiman_buit.webp')
HEAD6 = [(628, 590), (612, 560), (606, 520), (604, 470), (612, 420), (622, 385), (650, 365), (700, 352),
         (760, 350), (815, 362), (850, 395), (862, 450), (858, 510), (838, 560), (790, 595), (720, 612), (670, 612)]
EAR6_NEAR = [(622, 392), (624, 340), (638, 312), (652, 322), (668, 365)]
EAR6_FAR = [(808, 370), (822, 330), (842, 312), (852, 330), (850, 395)]
EYES6 = [(640, 495), (752, 495)]
NOSE6 = (650, 585)

if __name__ == '__main__':
    im = Image.open(FOTO6).convert('RGB').crop((500, 250, 1000, 700))
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for poly in (HEAD6, EAR6_NEAR, EAR6_FAR):
        d.polygon([(x - 500, y - 250) for x, y in poly], fill=(255, 0, 255, 60), outline=(255, 0, 255, 255))
    for x, y in EYES6 + [NOSE6]:
        d.ellipse([x - 506, y - 256, x - 494, y - 244], outline=(0, 255, 255, 255), width=2)
    Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB').save(os.path.join(HERE, 'controle_kop6.png'))
