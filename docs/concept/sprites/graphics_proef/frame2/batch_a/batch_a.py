# Frame 2 batch A per script (27 nov): 18 soorten. Alleen bestaande pixels verschuiven/buigen/spiegelen;
# wat bloot komt dichten met de aangrenzende kleur van hetzelfde deel. Draaien niet (rafels).
# Draaien vanuit deze map: python3 batch_a.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '..')
from f2lib import rgba, render_gif, save_anim_front, ANIMS
B = '../../../'
YY, XX = np.mgrid[0:64, 0:64]

def laad(p):
    im = Image.open(B+p)
    if im.mode == 'P':
        a = np.array(im)[:64].copy(); pal = im.getpalette()[:48]
        t = im.info.get('transparency', 0)
        assert t == 0, p
        return a, pal + [0]*(768-48)
    # RGBA zonder palet (glitch-lijn, Scrapstack): exact omzetten, index 0 = transparant
    d = np.array(im.convert('RGBA'))[:64]
    kl = sorted({tuple(c) for c in d[d[..., 3] > 0][:, :3]})
    assert len(kl) <= 15, (p, len(kl))
    a = np.zeros((64, 64), np.uint8)
    for i, c in enumerate(kl):
        a[(d[..., 3] > 0) & np.all(d[..., :3] == c, -1)] = i+1
    pal = [152, 208, 160] + [v for c in kl for v in c]
    return a, pal + [0]*(768-len(pal))

# ---------- bewerkingen ----------
def warp(a, fx, fy, mask=None):
    """Achterwaarts: out(p) = a(p - d(p)), d = (fx, fy) per pixel (gehele getallen). Geen gaten.
    Met mask: alleen pixels waarvan de bron in mask ligt verplaatsen; rest blijft."""
    fx = np.broadcast_to(np.round(fx).astype(int), a.shape); fy = np.broadcast_to(np.round(fy).astype(int), a.shape)
    sx, sy = XX-fx, YY-fy
    ok = (sx >= 0) & (sx < 64) & (sy >= 0) & (sy < 64)
    o = np.zeros_like(a); o[ok] = a[sy[ok], sx[ok]]
    return o

def rij_weg(a, r):        # rij r verdwijnt, alles erboven 1 omlaag
    o = a.copy(); o[1:r+1] = a[0:r]; o[0] = 0; return o
def kol_dubbel_l(a, c):   # kolom c dubbel, alles links ervan 1 naar links
    o = a.copy(); o[:, 0:c] = a[:, 1:c+1]; return o
def kol_dubbel_r(a, c):   # kolom c dubbel, alles rechts ervan 1 naar rechts
    o = a.copy(); o[:, c+1:] = a[:, c:63]; return o

def schuif(a, mask, dx, dy, dicht='rek'):
    """Deel verplaatsen. dicht='rek': wat vrijkomt houdt de oude pixels van het deel;
    'buur': vrijgekomen pixels krijgen de kleur van de eerste pixel buiten het deel aan de kant
    tegenover de beweging (het deel erachter); 'leeg': transparant."""
    o = a.copy()
    if dicht != 'rek':
        o[mask] = 0
        if dicht == 'buur':
            sx, sy = -np.sign(dx), -np.sign(dy)
            for y, x in zip(*np.where(mask)):
                yy, xx = y, x
                while 0 <= yy < 64 and 0 <= xx < 64 and mask[yy, xx]:
                    yy += sy; xx += sx
                    if sx == 0 and sy == 0: break
                if 0 <= yy < 64 and 0 <= xx < 64: o[y, x] = a[yy, xx]
    ys, xs = np.where(mask); ny, nx = ys+dy, xs+dx
    ok = (ny >= 0) & (ny < 64) & (nx >= 0) & (nx < 64)
    o[ny[ok], nx[ok]] = a[ys[ok], xs[ok]]
    return o

def wiel(a, cx, cy, rx, ry, mask=None):
    o = a.copy()
    for y in range(64):
        for c in range(64):
            if ((c-cx)/rx)**2+((y-cy)/ry)**2 <= 1 and (mask is None or mask[y, c]):
                o[y, c] = a[int(round(2*cy-y)), int(round(2*cx-c))]
    return o

def glitch(a, banden):
    o = a.copy()
    for r0, r1, dx in banden:
        for r in range(r0, r1+1):
            o[r] = 0
            if dx >= 0: o[r, dx:] = a[r, :64-dx]
            else: o[r, :64+dx] = a[r, -dx:]
    return o

def clip(v, lo, hi): return np.clip(v, lo, hi)

# ---------- soorten ----------
S = {}
def soort(slug, pad, anim, naam):
    def deco(f): S[slug] = (pad, anim, naam, f); return f
    return deco

@soort('pupoodle', 'poedellarve/af/poedellarve.png', 'ANIM_H_SLIDE', 'Pupoodle')
def _(a):  # rupsbult: middenlijf 2 px omhoog, kop 1 px op
    fy = np.where(XX < 30, -1, -np.round(2*np.sin(np.pi*clip(XX-30, 0, 22)/22)))
    return warp(a, 0, fy)

@soort('purrpillar', 'poesrups/af/poesrups.png', 'ANIM_H_SLIDE', 'Purrpillar')
def _(a):
    fy = -np.round(2*np.sin(np.pi*clip(XX-22, 0, 34)/34))
    return warp(a, 0, fy)

@soort('cryomet', 'ijskomeet/af/ijskomeet.png', 'ANIM_V_SLIDE', 'Cryomet')
def _(a):  # staart flakkert: staartpunt 2 naar binnen en 1 opzij, kern blijft
    s = clip(((XX-16)-(YY-46))/2 - 14, 0, 30)/30      # afstand langs de staart vanaf de kern
    w = np.round(1.5*np.sin(np.pi*s))
    return warp(a, -3*s + w, 3*s + w)

@soort('blobpudding', 'blobfish_fase2/af/blobfish_fase2.png', 'ANIM_V_SQUISH_AND_BOUNCE', 'blobfish pudding')
def _(a):  # pudding zakt 2 rijen in (voorhoofd), bovenkant waggelt 1 naar rechts, lagen blijven
    v = rij_weg(rij_weg(a, 20), 24)
    return warp(v, np.where(YY < 30, 1, 0), 0)

@soort('scrapstack', 'spooktrein_fase1/af/spooktrein_fase1.png', 'ANIM_V_SHAKE', 'Scrapstack')
def _(a):  # schoorsteen-kop rekt 2 omhoog en 1 naar links, wagen zakt 1, wiel halve slag
    v = rij_weg(a, 48)
    kop = (v > 0) & (YY <= 31) & (XX <= 30)
    v = schuif(v, kop, -1, -2, 'rek')
    return wiel(v, 49.5, 45.5, 6, 6)

@soort('pyrowyrm', 'vuurwerk_fase3/af/vuurwerkslang.png', 'ANIM_H_SLIDE_WOBBLE', 'Pyrowyrm')
def _(a):  # slingerende golf door het lijf
    return warp(a, np.round(1.4*np.sin(2*np.pi*YY/26)), 0)

@soort('spoetnik', 'satelliet_lijn/fase1/af/satelliet_fase1.png', 'ANIM_H_SLIDE_WOBBLE', 'Spoetnik')
def _(a):  # bol 1 naar links, antennes schuiven 2 uit (telescoop)
    fx = np.where(XX < 33, -1, -1 + 3*clip(XX-33, 0, 22)/22)
    return warp(a, fx, 0)

@soort('satelliet', 'satelliet_fase2/af/satelliet.png', 'ANIM_V_SLIDE', 'satelliet')
def _(a):  # beide panelen klappen op: punten 2 omhoog
    fy = np.where(XX > 38, -2*clip(XX-38, 0, 24)/24, np.where(XX < 14, -2*clip(14-XX, 0, 14)/14, 0))
    return warp(a, 0, fy)

@soort('ruimtestation', 'satelliet_fase3/af/ruimtestation.png', 'ANIM_H_SLIDE_WOBBLE', 'ruimtestation')
def _(a):  # de vier oogbollen schuiven 1-2 px naar buiten (station zet uit), armen blijven
    v = a.copy()
    for cx, cy, r, dx, dy in ((17, 31, 6.5, -1, -1), (15, 50, 8.5, -1, 1), (51, 39, 7.5, 2, 1), (53, 22, 6, 1, -2)):
        bol = (a > 0) & ((XX-cx)**2+(YY-cy)**2 <= r*r)
        v = schuif(v, bol, dx, dy, 'rek')
    return v

@soort('tempel', 'tempel/af/tempel.png', 'ANIM_V_SHAKE', 'levende tempel')
def _(a):  # tempel ademt: bovenkant 2 rijen omlaag, voet 1 breder
    v = rij_weg(rij_weg(a, 14), 24)
    return kol_dubbel_r(kol_dubbel_l(v, 14), 50)

@soort('missingraph', 'glitch_lijn/fase1_glitch/af/glitch_fase1.png', 'ANIM_H_SHAKE', 'Missingraph')
def _(a):
    return glitch(a, [(20, 22, 4), (29, 29, -3), (36, 38, 3), (44, 45, -4), (51, 51, 2)])

@soort('glitch2', 'glitch_lijn/fase2_bug/af/glitch_fase2.png', 'ANIM_V_SHAKE_H_SLIDE', 'glitch fase 2')
def _(a):
    return glitch(a, [(22, 23, -3), (30, 30, 2), (38, 39, 3), (46, 47, -4), (53, 53, 3)])

@soort('glitch3', 'glitch_lijn/fase3_virus/af/glitch_fase3.png', 'ANIM_H_SHAKE', 'glitch fase 3')
def _(a):
    return glitch(a, [(12, 13, 3), (21, 22, -4), (31, 31, 3), (40, 42, -3), (50, 51, 4), (57, 57, -2)])

@soort('guarana1', 'guarana/af/guarana.png', 'ANIM_H_SLIDE_WOBBLE', 'guarana fase 1')
def _(a):  # liaan zwiept: kop 2 naar links, voet blijft
    return warp(a, -np.round(2*clip(46-YY, 0, 30)/30), 0)

@soort('guarana2', 'guarana_fase2/af/guarana_fase2.png', 'ANIM_H_SLIDE', 'guarana fase 2')
def _(a):  # ranken 1 naar links, trossen in tegenbeweging 1 naar rechts en 1 omlaag
    v = warp(a, -np.round(clip(48-YY, 0, 40)/40), 0)
    tros = np.isin(v, [1, 2, 3, 4, 5, 10])
    tros &= (((XX <= 19) & (YY >= 18) & (YY <= 44)) | ((XX >= 19) & (XX <= 37) & (YY >= 9) & (YY <= 33))
             | ((XX >= 41) & (YY >= 18) & (YY <= 44)))
    # zwarte lijn van de ranken telt niet mee: alleen zwart dat aan rood/wit grenst
    rood = np.isin(v, [2, 3, 4, 5, 10])
    nb = np.zeros_like(rood)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            nb |= np.roll(np.roll(rood, dy, 0), dx, 1)
    tros &= rood | nb
    return schuif(v, tros, 1, 1, 'buur')

@soort('sneeuw1', 'sneeuwmonster/af/sneeuwmonster.png', 'ANIM_V_SQUISH_AND_BOUNCE', 'sneeuwmonster fase 1')
def _(a):  # zakt in: 2 rijen weg, 2 kolommen breder
    v = rij_weg(rij_weg(a, 30), 46)
    w = kol_dubbel_r(kol_dubbel_l(v, 20), 40)
    v[31:] = w[31:]          # alleen het lijf breder, kop (gezicht) blijft gelijk
    return v

@soort('sneeuw2', 'sneeuwmonster_fase2/af/sneeuwmonster2.png', 'ANIM_V_SLIDE', 'sneeuwmonster fase 2')
def _(a):  # lijf zakt 1, emmer blijft hangen (1 omhoog t.o.v. de kop); wat vrijkomt = de sneeuw van de kop eronder
    v = rij_weg(a, 42)
    emmer = np.isin(v, [7, 8, 9, 10, 11, 12]) & (YY <= 20)
    emmer |= (v == 1) & (YY <= 20) & (XX >= 22) & (XX <= 50) & ~np.isin(np.roll(v, 1, 0), [5, 6, 4, 3, 2])
    return schuif(v, emmer, 0, -1, 'buur')

@soort('zandloper1', 'zandloper/fase1/af/zandloper_fase1.png', 'ANIM_V_SLIDE', 'zandloper fase 1')
def _(a):  # zandloper 1 omhoog, losse handen in tegenbeweging 2 omlaag en 1 naar buiten
    from scipy.ndimage import label
    lab, n = label(a > 0, np.ones((3, 3)))
    hl = np.isin(lab, np.unique(lab[(a > 0) & (XX <= 19) & (YY <= 40)])); hr = np.isin(lab, np.unique(lab[(a > 0) & (XX >= 52) & (YY <= 45)]))
    v = schuif(a, (a > 0) & ~hl & ~hr, 0, -1, 'leeg')
    v = schuif(v, hl, -1, 2, 'leeg')
    return schuif(v, hr, 1, 2, 'leeg')

# ---------- uitvoer ----------
if __name__ == '__main__':
    kies = sys.argv[1:] or list(S)
    rijen = []
    for slug in S:
        pad, anim, naam, f = S[slug]
        a, pal = laad(pad)
        f2 = f(a).astype(np.uint8)
        if slug in kies:
            save_anim_front(a, f2, pal, f'{slug}_anim_front.png')
            chk = np.array(Image.open(f'{slug}_anim_front.png'))
            assert chk.shape == (128, 64) and (chk[:64] == a).all(), slug
            render_gif(a, f2, pal, anim, f'{slug}_anim.gif')
        rijen.append((slug, naam, anim, a, f2, pal))
    with open('animids.txt', 'w') as fh:
        for slug, naam, anim, *_ in rijen: fh.write(f'{slug} {anim}\n')
    # vel: 3 soorten per rij, frame 1 | frame 2 op 4x
    Z = 4; W = 64*Z; N = 3
    sh = Image.new('RGB', (8+N*(2*W+28), ((len(rijen)+N-1)//N)*(W+44)+4), 'white'); d = ImageDraw.Draw(sh)
    for i, (slug, naam, anim, a, f2, pal) in enumerate(rijen):
        x0, y0 = 8+(i % N)*(2*W+28), 4+(i//N)*(W+44)
        for j, f in enumerate((a, f2)):
            bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(Image.fromarray(rgba(f, pal)))
            sh.paste(bg.convert('RGB').resize((W, W), Image.NEAREST), (x0+j*(W+4), y0))
            d.rectangle([x0+j*(W+4), y0, x0+j*(W+4)+W-1, y0+W-1], outline=(210, 210, 210))
        d.text((x0, y0+W+6), f'{naam} ({slug}): frame 1 | frame 2', fill=(0, 0, 0))
        d.text((x0, y0+W+20), anim, fill=(0, 0, 0))
    sh.save('batch_a_vel.png')
