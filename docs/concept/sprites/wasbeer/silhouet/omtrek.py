"""Wasbeer: omtrek van foto 10 (referenties/foto10_staand_reikend.jpg, 500x375), punt voor punt in
fotocoördinaten overgenomen (kolibriemethode; Jordi 2 nov: "hier is een goede staande pose").
Delen apart, zodat klauwen (koevoet) en staart (haak) later los aangepast kunnen worden.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet/omtrek.py  -> controle_omtrek.png"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(HERE, '../referenties/foto10_staand_reikend.jpg')

HEAD_BODY = [(346, 86), (338, 96), (320, 103), (300, 108), (292, 125), (291, 160), (287, 195), (280, 225),
             (268, 250), (252, 268), (225, 278), (195, 280), (170, 272), (155, 250), (150, 215), (152, 180),
             (160, 150), (180, 120), (200, 98), (225, 78), (248, 60), (262, 50), (275, 30), (290, 20),
             (305, 22), (318, 40), (330, 60), (342, 75)]
EAR_NEAR = [(258, 54), (257, 38), (265, 29), (276, 32), (279, 46)]
EAR_FAR = [(288, 24), (291, 9), (299, 6), (306, 13), (305, 26)]
LEG_NEAR = [(165, 262), (195, 268), (198, 300), (195, 330), (205, 355), (208, 372), (178, 374), (176, 350),
            (172, 320), (162, 290)]
LEG_FAR = [(252, 262), (268, 272), (270, 290), (290, 295), (306, 302), (300, 310), (268, 310), (258, 300), (250, 280)]
TAIL = [(165, 255), (130, 252), (95, 255), (70, 258), (60, 268), (68, 282), (95, 285), (130, 285), (165, 285)]
ARM_NEAR = [(228, 160, 10), (255, 190, 9), (280, 220, 8), (300, 235, 8), (315, 245, 6)]    # hangt voor de buik
ARM_FAR = [(290, 150, 9), (320, 165, 8), (350, 175, 7), (378, 184, 7)]                    # reikt naar voren
POLYS = {'kop/lijf': HEAD_BODY, 'oor': EAR_NEAR, 'oor2': EAR_FAR, 'poot': LEG_NEAR, 'poot2': LEG_FAR, 'staart': TAIL}


def tube(d, pts, k=1.0, ox=0, oy=0, fill=255):
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        for i in range(11):
            t = i / 10
            x, y, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, (r0 + (r1 - r0) * t)
            d.ellipse([(x - r) * k + ox, (y - r) * k + oy, (x + r) * k + ox, (y + r) * k + oy], fill=fill)


if __name__ == '__main__':
    im = Image.open(FOTO).convert('RGB').resize((1000, 750))
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for name, poly in POLYS.items():
        d.polygon([(x * 2, y * 2) for x, y in poly], fill=(255, 0, 255, 70), outline=(255, 0, 255, 255))
    for arm in (ARM_NEAR, ARM_FAR):
        tube(d, arm, 2, fill=(0, 255, 255, 90))
    Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB').save(os.path.join(HERE, 'controle_omtrek.png'))
