"""Vel voor Jordi: het model in 3/4-hoeken naast Taillow, Starly en het goedgekeurde profiel. python3 vel_hoeken.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import model as M
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
FBs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
BG = (236, 234, 228); INK = (40, 36, 50); GR = (95, 90, 105)
LIJF = (25, 32, 40); KOP = (6, 12, 18); KANTEL = 8
C = 256            # 4x
def sprite(p):
    im = Image.open(p).convert('RGBA').crop((0, 0, 64, 64))
    pal = Image.open(p).getpalette()
    a = np.array(Image.open(p).crop((0, 0, 64, 64))) != 0
    rgba = np.array(im); rgba[..., 3] = a * 255
    return Image.fromarray(rgba)
def op_bg(im, schaal, achter=BG):
    v = Image.new('RGB', im.size, achter); v.paste(im, (0, 0), im)
    return v.resize((im.width * schaal, im.height * schaal), Image.NEAREST)
def silh(m, schaal=1):
    return Image.fromarray(np.where(m, 40, 255).astype(np.uint8)).convert('RGB').resize((64 * schaal, 64 * schaal), Image.NEAREST)
def render_rgba(occ, Z, y, k, kantel=KANTEL):
    img, al = M.render(occ, Z, y, k, kantel)
    rgba = np.dstack([img, al * 255]).astype(np.uint8)
    return Image.fromarray(rgba), al
def klein(rgba):
    """modelrender terug naar spritemaat (1x), alleen ter oriëntatie"""
    return rgba.resize((64, 64), Image.LANCZOS)

occ, Z = M.bouw()
tail = sprite('../../../../../graphics/pokemon/taillow/anim_front.png')
star = sprite('../../../../../graphics/pokemon/starly/anim_front.png')
r10 = sprite('../maker/kleur_r10/kolibrie_pre.png')
nul, a0 = render_rgba(occ, Z, 0, 0, 0)
m0 = M.naar64(a0); iou2 = M.iou(m0, M.P2); iou10 = M.iou(m0, M.S)
zl = M.yy > 23; iou_lijf = M.iou(m0 & zl, M.P2 & zl); iou_kop = M.iou(m0 & ~zl, M.S & ~zl)
ov = np.full((64, 64, 3), 255, np.uint8); ov[m0 & M.P2] = (90, 170, 90); ov[M.P2 & ~m0] = (220, 60, 60); ov[m0 & ~M.P2] = (60, 90, 220)

W = 24 + 4 * (C + 16) + 300; H = 60 + (C + 70) + 3 * (C + 64) + 40
V = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(V)
d.text((24, 14), 'Kolibrie pre-evo: 3D-model op de goedgekeurde vorm, gedraaid naar driekwart (kies een hoek)', font=FB, fill=INK)
# rij 1: referenties + bewijs zijaanzicht
y0 = 50
items = [(op_bg(tail, 4), 'Taillow (maatstaf)'), (op_bg(star, 4), 'Starly'), (op_bg(r10, 4), 'r10 (bron: profiel r2 + kop r8 lager)'),
         (op_bg(nul.resize((C, C), Image.LANCZOS), 1), 'model 0 graden (zijaanzicht)')]
for i, (im, lab) in enumerate(items):
    x = 24 + i * (C + 16); V.paste(im, (x, y0)); d.text((x, y0 + C + 4), lab, font=F, fill=GR)
x = 24 + 4 * (C + 16)
V.paste(Image.fromarray(ov).resize((192, 192), Image.NEAREST), (x, y0))
d.text((x, y0 + 196), f'model 0 graden over silhouet r2', font=F, fill=GR)
d.text((x, y0 + 214), f'lijf vs profiel r2: {iou_lijf:.1%}', font=FBs, fill=(30, 120, 50))
d.text((x, y0 + 234), f'kop vs kop r8 lager/r10: {iou_kop:.1%}', font=FBs, fill=(30, 120, 50))
d.text((x, y0 + 254), f'geheel vs r10: {iou10:.1%}; vs r2: {iou2:.1%}', font=F, fill=GR)
d.text((x, y0 + 270), '(r10 zelf wijkt in de kop 4,8% af van r2)', font=F, fill=GR)
# raster: rijen = lijf, kolommen = kop extra
y1 = y0 + C + 56
d.text((24, y1 - 22), f'lijf naar de kijker (rijen) x kop draait extra mee (kolommen); kanteling {KANTEL} graden (iets van boven), licht linksboven', font=F, fill=INK)
for r, ly in enumerate(LIJF):
    for c, kp in enumerate(KOP):
        rgba, al = render_rgba(occ, Z, ly, kp)
        x = 24 + c * (C + 16); y = y1 + r * (C + 64)
        V.paste(op_bg(rgba.resize((C, C), Image.LANCZOS), 1), (x, y))
        m = M.naar64(al)
        naam = 'ABC'[r] + str(c + 1)
        d.text((x + 6, y + 4), naam, font=FB, fill=INK)
        d.text((x, y + C + 4), f'lijf {ly} gr, kop {ly + kp} gr  ·  {m.sum()} px', font=F, fill=GR)
    # rechts: Taillow en Starly silhouetten 1x/2x ter vergelijking in de eerste rij
x = 24 + 3 * (C + 16); y = y1
d.text((x, y), 'op ware grootte (1x):', font=FBs, fill=INK)
for r, ly in enumerate(LIJF):
    for c, kp in enumerate(KOP):
        rgba, al = render_rgba(occ, Z, ly, kp)
        V.paste(op_bg(klein(rgba), 1), (x + c * 70, y + 26 + r * 74))
        d.text((x + c * 70 + 2, y + 26 + r * 74 + 58), 'ABC'[r] + str(c + 1), font=F, fill=GR)
yy = y + 26 + 3 * 74 + 10
V.paste(op_bg(tail, 1), (x, yy)); V.paste(op_bg(star, 1), (x + 70, yy)); V.paste(op_bg(r10, 1), (x + 140, yy))
d.text((x, yy + 66), 'Taillow   Starly    r10', font=F, fill=GR)
d.text((x, yy + 100), 'De 1x-plaatjes zijn de render verkleind,', font=F, fill=GR)
d.text((x, yy + 116), 'geen sprite: die tekent de maker straks', font=F, fill=GR)
d.text((x, yy + 132), 'met de hand op het gekozen silhouet.', font=F, fill=GR)
d.text((x, yy + 156), 'Oog = het bevroren Starly-oog, op de plek', font=F, fill=GR)
d.text((x, yy + 172), 'waar het model het zet (niet vervormd).', font=F, fill=GR)
d.text((x, yy + 196), 'Profiel r2: 732 px; doel 3/4: 700-750 px.', font=F, fill=GR)
V.save('vel_hoeken.png'); print(iou2, iou10)
