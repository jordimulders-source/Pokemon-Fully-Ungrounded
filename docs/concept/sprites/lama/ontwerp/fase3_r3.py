"""Lama fase 3 (cholita-luchadora), poppetje ronde 3: het goedgekeurde ontwerp 3Y (lijn_ronde2.png, fase3_r2(voet='wrap'))
overgezet op wat bij fase 2 is geleerd: lamakop naar foto 1 (kop_lama), kaarsrechte hals, lijf horizontaal met de kop
driekwart naar de kijker (foto 8, pose F van fase 2), alle poten op de grond.
3Y: zwaar en geschoren (wol alleen als kleding), brede borst, kortere dikke hals, dikke poten; bombín, pony, vlechten met
tullma's, manta met gouden zoom, pollera in drie ruches, aguayo-windsels (hoeven vrij), brede halsband (5 strepen, 7 pompons).
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/ontwerp/fase3_r3.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d_lama as L
P = L.P

# Benen: grond op y = -66. Vooraan windsels (wrap), achter hoeven.
POSES3 = {
    'F_pas': [   # als fase 2 (Jordi: "F, want daar zijn alle poten zichtbaar")
        ('leg', [(-32, -12, 15, 10), (-40, -40, 17, 7.5), (-46, -64, 17, 6.8)], 'wrap'),
        ('far', [(-20, -12, -15, 10), (-18, -40, -17, 7.5), (-16, -64, -17, 6.8)], 'wrap'),
        ('leg', [(32, -10, 15, 11.5), (42, -38, 17, 7.5), (42, -64, 17, 6.8)], None),
        ('far', [(40, -10, -15, 11.5), (46, -38, -17, 7.5), (52, -62, -17, 6.8)], None)],
    'W_breed': [  # geworteld: poten recht onder het lijf, breed uit elkaar (z), voor en achter iets gespreid
        ('leg', [(-32, -12, 16, 10), (-40, -40, 21, 7.5), (-44, -64, 23, 6.8)], 'wrap'),
        ('far', [(-20, -12, -16, 10), (-18, -40, -21, 7.5), (-18, -64, -23, 6.8)], 'wrap'),
        ('leg', [(32, -10, 16, 11.5), (38, -38, 21, 7.5), (40, -64, 23, 6.8)], None),
        ('far', [(40, -10, -16, 11.5), (46, -38, -21, 7.5), (50, -64, -23, 6.8)], None)],
    'U_uitval': [  # vechtstand: nabije voorpoot ver vooruit gezet, verre achterpoot ver achter; gewicht naar voren
        ('leg', [(-32, -12, 16, 10), (-54, -36, 20, 7.5), (-68, -62, 21, 6.8)], 'wrap'),
        ('far', [(-20, -12, -16, 10), (-20, -40, -20, 7.5), (-20, -64, -21, 6.8)], 'wrap'),
        ('leg', [(32, -10, 16, 11.5), (38, -38, 20, 7.5), (40, -64, 21, 6.8)], None),
        ('far', [(40, -10, -16, 11.5), (58, -36, -20, 7.5), (72, -60, -21, 6.8)], None)],
}


def kop3(m, top, hs, yaw_extra, lid):
    """kop_lama (fase 2, goedgekeurd) zonder oorkwasten + bombín, pony en vlechten; daarna samen gedraaid."""
    h0 = len(m.parts)
    L.kop_lama(m, top, hs, 0, top, pitch=0, lid=lid, kleding=False)
    cr = top + np.array((-4, 5, 0)) * hs
    hc = cr + np.array((-0.5, 8.8, 0)) * hs                   # bombín: klein, hoog op de kruin, vóór de oren
    m.ell(hc, np.array((7.6, 1.1, 6.4)) * hs, 'hat')                                   # rand
    m.ell(hc + np.array((0, 1.4, 0)) * hs, np.array((4.9, 1.3, 4.4)) * hs, 'hatband')
    m.ell(hc + np.array((0, 3.6, 0)) * hs, np.array((4.6, 4.2, 4.1)) * hs, 'hat')       # bol
    for dx in (-6, -3.5):                                      # crème pony onder de rand
        m.ell(cr + np.array((dx, 7.2, 0)) * hs, np.array((2.4, 2.0, 3.0)) * hs, 'pony')
    for sz in (1, -1):                                         # vlechten uit de oorwol, langs de hals, rode tullma
        b = cr + np.array((6, 3, 7.5 * sz)) * hs
        pts = [b + np.array((1.6 * i, -4.6 * i, 0.5 * sz * i)) * hs for i in range(7)]
        for i, q in enumerate(pts):
            m.ell(q, np.array((2.5, 2.8, 2.5)) * hs * (1 - 0.05 * i), 'braid')
        m.ell(pts[-1] + np.array((0.3, -3.6, 0)) * hs, np.array((2.3, 3.2, 2.3)) * hs, 'tassel')
    Rp = P.rot_z(math.radians(-8)); Ry = P.rot_y(math.radians(yaw_extra))
    m.parts[h0:] = [(top + Ry @ (top + Rp @ (c - top) - top), r, Ry @ Rp @ R0, g) for c, r, R0, g in m.parts[h0:]]


def fase3_r3(pose='F_pas', hs=1.4, neck=46, lid=0.55, head_yaw=55, borst=0):
    m = P.Model()
    lx = 1.12
    for c, r in (((-26, 2, 0), (27, 27, 25)), ((4, 2, 0), (33, 24, 23)), ((33, 4, 0), (22, 24, 23))):
        m.ell((c[0] * lx, c[1], c[2]), (r[0] * lx, r[1], r[2]), 'body')               # geschoren: glad
    m.chain([(54, 14, 0, 5.5), (59, 22, 0, 6), (58, 28, 0, 4.5)], 'tail')
    m.ell((58, 28, 0), 5.5, 'tail')
    top = np.array((-38, 10 + neck, 0.0))
    nk = [(-34, 14, 0, 19.5), (-36, 10 + neck * 0.5, 0, 16), (top[0], top[1], 0, 13)]    # kaarsrecht, kort, krachtig
    h0 = len(m.parts)
    m.chain(nk, 'neck')
    L.halsband(m, nk[0][:3], nk[1][:3], 0.95, 16.5, ['ag3', 'ag0', 'ag1', 'ag2', 'ag0'], pompons=7)
    kop3(m, top, hs, head_yaw, lid)
    h1 = len(m.parts)
    for th in np.arange(-100, 101, 8):                       # manta over de schouders, gouden zoom
        t = math.radians(th)
        c = np.array((-26 * lx, 4 + 28.5 * math.cos(t), 26.5 * math.sin(t)))
        m.ell(c, np.array((14, 3.4, 6.5)), 'manta', P.rot_x(t))
        m.ell(c + np.array((-12, -1.5, 0)), np.array((3.6, 3.4, 5.5)), 'mantarand', P.rot_x(t))
    for j, (yy, ext) in enumerate(((2, 0), (-9, 3), (-20, 6))):   # pollera: drie ruches om het achterlijf
        for th in np.arange(0, 360, 7):
            t = math.radians(th)
            rr = 26 + ext
            m.ell(np.array((32 * lx * 0.95 + rr * 0.85 * math.cos(t), yy, rr * math.sin(t))), np.array((6.5, 6.5, 6.5)), f'pol{j}')
    if borst:   # borst vooruit / kop hoog: voorlijf licht omhoog, hals blijft kaarsrecht
        piv = np.array((30, -8, 0.0))
        L._rot(m, 0, len(m.parts), piv, P.rot_z(math.radians(-borst)))
        pv = piv + P.rot_z(math.radians(-borst)) @ (np.array(nk[0][:3], float) - piv)
        L._rot(m, h0, h1, pv, P.rot_z(math.radians(borst)))
    for g, pts, voet in POSES3[pose]:
        L.poot(m, pts, g, 1.5, voet)
    return m


# (pose, borst, lijfhoek camera, kop extra, label); Jordi 5 nov: "ik wil wel een iets andere pose dan fase 2"
OPTS = [('W_breed', 6, 32, 30, 'A: geworteld, lijf 32°'), ('U_uitval', 5, 14, 50, 'B: uitval (vechtstand)'),
        ('W_breed', 6, 55, 10, 'C: bijna frontaal'), ('W_breed', 8, 8, 85, 'D: zij, kop naar je toe')]
KEUS = OPTS[0]


def vel():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    ref = os.path.join(HERE, '../referenties')
    L.set_vacht('bont (foto 4)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#C9A982'
    cell = 262
    im = Image.new('RGB', (12 + cell * 5, 44 + (cell + 30) * 2), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Lama fase 3 (3Y), poppetje ronde 3: eigen pose (anders dan fase 2), lamakop, kaarsrechte hals', font=FB, fill=(30, 30, 30))
    def tegel(img, i, rij, lab):
        x, y = 12 + cell * i, 44 + rij * (cell + 30)
        im.paste(img, (x + (256 - img.width) // 2, y + (256 - img.height) // 2)); d.text((x + 4, y + 260), lab, font=F, fill=(60, 60, 60))
    oud = L.fase3_r2(voet='wrap'); img, _ = L.view(oud, 40); tegel(img, 0, 0, 'goedgekeurd ontwerp 3Y (2 nov)')
    for i, (pose, borst, yaw, hy, lab) in enumerate(OPTS):
        m = fase3_r3(pose, borst=borst, head_yaw=hy); img, _ = L.view(m, yaw)
        tegel(img, i + 1, 0, f'{lab}')
    # rij 2: lijn op schaal (sprites fase 1 en 2, fase 3 = optie B) + kop naast foto 1
    def sprite(p, h):
        s = Image.open(p).convert('RGBA'); s = s.crop(s.getbbox()); k = h / s.height
        s = s.resize((int(s.width * k), int(s.height * k)), Image.NEAREST)
        bg = Image.new('RGBA', s.size, 'white'); bg.alpha_composite(s); return bg.convert('RGB')
    tegel(sprite(os.path.join(ref, 'fase1_alpaca.png'), 160), 0, 1, 'fase 1: alpaca (af)')
    tegel(sprite(os.path.join(HERE, '../fase2/af/lama.png'), 200), 1, 1, 'fase 2: lama (af, 4 nov)')
    m = fase3_r3(KEUS[0], borst=KEUS[1], head_yaw=KEUS[3]); img, a = L.view(m, KEUS[2])
    bb = Image.fromarray((a * 255).astype(np.uint8)).resize(img.size).getbbox(); f3 = img.crop(bb)
    k = 236 / max(f3.size); f3 = f3.resize((int(f3.width * k), int(f3.height * k)), Image.LANCZOS)
    tegel(f3, 2, 1, 'fase 3 (A), op dezelfde spritehoogte')
    big, a = L.view(m, KEUS[2], size=236)
    bb = Image.fromarray((a * 255).astype(np.uint8)).resize(big.size).getbbox()
    kz = big.crop((bb[0] - 4, bb[1] - 4, bb[0] + 96, bb[1] + 96)).resize((256, 256), Image.LANCZOS)
    tegel(kz, 3, 1, 'kop fase 3 (A), uitvergroot')
    foto1 = Image.open(os.path.join(ref, 'foto1_lama_driekwart_POSE.png')).convert('RGB'); w, h = foto1.size
    kf = foto1.crop((int(w * 0.18), int(h * 0.1), int(w * 0.55), int(h * 0.4))); kf.thumbnail((256, 256))
    tegel(kf, 4, 1, 'kop foto 1 (lama-bron)')
    im.save(os.path.join(HERE, 'vel_fase3_ronde3.png'))


if __name__ == '__main__':
    vel()
