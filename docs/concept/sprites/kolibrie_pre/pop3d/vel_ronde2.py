"""Vel ronde 2: poppetje passend op foto 1 (pas_foto.py, 88% overlap), daarna cute gemaakt in 3D:
kop groter, lijf en staart korter. Raster van drie standen + kleur."""
import json, numpy as np
from PIL import Image, ImageDraw, ImageFont
import pas, pop3d_kuiken as K
K.set_palet('fluweel (als eindvorm)')
P0 = json.load(open('pas_foto_params.json'))
def cute(k_kop, k_lijf, k_staart):
    p = dict(P0)
    top = p['by'] + p['bry']
    p['bry'] *= k_lijf; p['ery'] *= k_lijf
    p['by'] = top - p['bry'] - (1 - k_lijf) * 10   # lijf korter van onderen; kop zakt mee
    dy = (1 - k_lijf) * 34
    p['hy'] -= dy; p['ey'] -= dy * 0.5; p['wy'] -= dy * 0.2
    p['hr'] *= k_kop; p['hx'] -= (k_kop - 1) * 6; p['hy'] += (k_kop - 1) * 8
    p['tl'] *= k_staart; p['ty'] += (1 - k_staart) * 14 - dy * 0.6; p['wl'] *= (0.5 + 0.5 * k_lijf)
    return p
STANDEN = {'1: foto-getrouw': (1.0, 1.0, 1.0), '2: iets cute': (1.2, 0.88, 0.75), '3: cute': (1.4, 0.78, 0.6)}
if __name__ == '__main__':
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    cell = 262; V = Image.new('RGB', (12 + cell * 4, 44 + (256 + 30) * 2), 'white'); d = ImageDraw.Draw(V)
    d.text((12, 12), 'Kolibrie pre-evo ronde 2: poppetje volgt foto 1 (88% overlap), daarna cute in 3D', font=FB, fill=(30, 30, 30))
    foto = Image.open('../referenties/jordi_1_zittend_jong.webp').convert('RGB').crop((200, 140, 740, 710)); foto.thumbnail((256, 256))
    V.paste(foto, (12, 44)); d.text((14, 44 + 260), 'foto 1 (bron)', font=F, fill=(60, 60, 60))
    for i, (lab, k) in enumerate(STANDEN.items()):
        m = pas.model(cute(*k), dons=True); img, _ = K.view(m, 15, 4)
        V.paste(img, (12 + cell * (i + 1), 44)); d.text((14 + cell * (i + 1), 44 + 260), f'{lab}, kop {K.kopaandeel(m, 15, 4):.0%}', font=F, fill=(60, 60, 60))
    ov = Image.open('overlay_foto.png'); ov.thumbnail((256, 256))
    V.paste(ov, (12, 44 + 286)); d.text((14, 44 + 286 + 260), 'stand 1 over foto 1: 88%', font=F, fill=(60, 60, 60))
    for i, naam in enumerate(['dons (jong, doffer)', 'hillstar + violet']):
        K.set_palet(naam); img, _ = K.view(pas.model(cute(*STANDEN['2: iets cute']), dons=True), 15, 4)
        V.paste(img, (12 + cell * (i + 1), 44 + 286)); d.text((14 + cell * (i + 1), 44 + 286 + 260), f'stand 2, {naam}', font=F, fill=(60, 60, 60))
    f3 = Image.open('../referenties/jordi_3_nestjongen.png').convert('RGB').crop((0, 225, 220, 447)).resize((256, 256))
    V.paste(f3, (12 + cell * 3, 44 + 286)); d.text((14 + cell * 3, 44 + 286 + 260), 'foto 3 (bek)', font=F, fill=(60, 60, 60))
    V.save('vel_ronde2.png')
