"""Driekwart kop van foto 11 (referenties/foto11_driekwart_kop.webp, 819x1024; Jordi 2 nov: "op deze foto zie je
het iets beter vanaf een bijna driekwart pose"), punt voor punt overgenomen. Kijkt naar links, korte snuit,
kleine neus; verre oor alleen als witte rand, nabije oor groot rechtsboven.
Controle: python3 kop11.py -> controle_kop11.png"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
FOTO11 = os.path.join(HERE, '../referenties/foto11_driekwart_kop.webp')
HEAD11 = [(220, 210), (222, 194), (232, 184), (240, 166), (250, 148), (262, 134), (290, 118), (320, 108),
          (360, 104), (400, 112), (430, 128), (470, 172), (474, 215), (455, 250), (420, 272), (370, 288),
          (320, 286), (280, 270), (252, 250), (236, 232)]
EAR11_NEAR = [(428, 132), (445, 114), (470, 106), (498, 107), (508, 124), (500, 150), (482, 178), (460, 175)]
EAR11_FAR = [(258, 140), (264, 122), (276, 115), (290, 120)]
EYES11 = [(252, 165), (340, 170)]
NOSE11 = (228, 210)

if __name__ == '__main__':
    im = Image.open(FOTO11).convert('RGB').crop((180, 80, 540, 320))
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for poly in (HEAD11, EAR11_NEAR, EAR11_FAR):
        d.polygon([(x - 180, y - 80) for x, y in poly], fill=(255, 0, 255, 60), outline=(255, 0, 255, 255))
    for x, y in EYES11 + [NOSE11]:
        d.ellipse([x - 186, y - 86, x - 174, y - 74], outline=(0, 255, 255, 255), width=2)
    Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB').save(os.path.join(HERE, 'controle_kop11.png'))
