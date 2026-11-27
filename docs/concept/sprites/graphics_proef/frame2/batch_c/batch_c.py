# Frame 2 per script voor batch C (27 nov), 14 twijfelsoorten, per soort één variant.
# Alleen bestaande pixels verschuiven/rekken/knijpen/draaien (RotSprite) via ../batch_b/f2b.py;
# wat bloot komt wordt dichtgezet met de dichtstbijzijnde pixel van hetzelfde deel (geen kolomvulling).
# Engine-animaties uit ../f2lib.py. Gebruik: python3 batch_c.py [slug ...]
import sys, os, numpy as np
import scipy.ndimage as nd
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
sys.path.insert(0, os.path.join(HIER, '..')); sys.path.insert(0, os.path.join(HIER, '..', 'batch_b'))
from f2lib import save_anim_front, render_gif, rgba
from PIL import ImageDraw
from f2b import *
B = '../../../'

SOORTEN = {
    'curiqui': 'nachtaap_fase3/af/nachtaap_fase3.png',
    'bootoo': 'potoo/af/potoo.png',
    'globsnail': 'sneeuwbolslak/af/sneeuwbolslak.png',
    'clionice': 'sneeuwbolslak_fase2/af/sneeuwbolslak_fase2.png',
    'wagogogon': 'spooktrein_fase2/af/spooktrein_fase2.png',
    'axolaunch': 'vuurwerk_fase1/af/vuurwerk_fase1.png',
    'mate': 'mate/af/mate.png',
    'rowmate': 'mate_fase2/af/mate2.png',
    'flytron': 'vlieglijn_fase1/af/vlieg.png',
    'buzzquito': 'vlieglijn_fase2/af/mug.png',
    'capykart': 'capykart/af/capykart.png',
    'zanddjinn': 'zandloper/fase3/af/zandloper_fase3.png',
    'glyptodon1': 'glyptodon/fase1/af/glyptodon_fase1.png',
    'glyptodon2': 'glyptodon/fase2/af/glyptodon_fase2.png',
}

def laad(p):
    im = Image.open(B+p); a = np.array(im)
    if a.shape == (128, 64): a = a[:64]
    assert a.shape == (64, 64) and im.mode == 'P' and a.max() < 16
    return a, im.getpalette()

def dicht(o, a, rest, sluit=0):
    """Gaten binnen het nieuwe silhouet (waar frame 1 iets had) dicht met de dichtstbijzijnde pixel van `rest`
    (het deel dat eronder ligt, uit frame 1). sluit=k: ook vrijgekomen pixels binnen de k×k-sluiting van rest
    (een deel dat vóór het lijf lag en tot de rand doorliep)."""
    gat = (o == 0) & nd.binary_fill_holes(o > 0) & (a > 0)
    if sluit:
        gat |= (o == 0) & (a > 0) & nd.binary_closing(np.pad(rest, sluit), np.ones((sluit, sluit)))[sluit:-sluit, sluit:-sluit]
    if gat.any():
        _, (iy, ix) = nd.distance_transform_edt(~rest, return_indices=True)
        o = o.copy(); o[gat] = a[iy[gat], ix[gat]]
    return o

def plak(o, a, deel, nieuw):
    """Getransformeerd deel (array met 0 = leeg) bovenop o leggen."""
    o = o.copy(); m = nieuw > 0; o[m] = nieuw[m]; return o

def los_draai(a, deel, graden, cx, cy, dx=0, dy=0, knip=False, onder=None, sluit=0):
    """Deel los draaien (RotSprite) en terugleggen; vrijgekomen plek dicht met het deel eronder."""
    nieuw = rotsprite(np.where(deel, a, 0), deel, graden, cx, cy, dx, dy, knip)
    o = a.copy(); o[deel] = 0
    rest = (a > 0) & ~deel if onder is None else onder
    o = dicht(o, a, rest, sluit)
    return plak(o, a, deel, nieuw)

def lijn_masker(a, p0, p1, d, kleuren=None):
    """Pixels binnen afstand d van het lijnstuk p0-p1 (voor stokjes zoals een bombilla)."""
    (x0, y0), (x1, y1) = p0, p1
    vx, vy = x1-x0, y1-y0; L2 = vx*vx+vy*vy
    t = np.clip(((XX-x0)*vx+(YY-y0)*vy)/L2, 0, 1)
    m = np.hypot(XX-(x0+t*vx), YY-(y0+t*vy)) <= d
    m &= a > 0
    if kleuren is not None: m &= np.isin(a, kleuren)
    return m

def rek_onder(x, r, d, mask=None):
    """Spiegel van rek: alles vanaf rij r (binnen mask) d px omlaag; rijen r..r+d-1 blijven ook staan."""
    m = (YY >= r) & (x > 0)
    if mask is not None: m &= mask
    o = x.copy(); o[m & (YY >= r+d)] = 0
    ys, xs = np.where(m); assert (ys+d < 64).all(), 'deel valt uit het vak'
    o[ys+d, xs] = x[ys, xs]
    return o

def _kop(o, kop, oog):
    n = rotsprite_gezicht(o, kop, oog, 6, 31, 24)
    return dicht(n, o, (o > 0) & ~kop)

# ---------------- per soort ----------------
def curiqui(a):
    # hangt aan de opgestoken hand: hele aap zwaait rechtsom om die hand
    gez = (XX >= 4) & (XX <= 15) & (YY >= 35) & (YY <= 45) & np.isin(a, [1, 6, 7, 8, 10, 14, 15])
    o = rotsprite_gezicht(a, a > 0, gez, -5, 36, 6)     # gezicht als vast blok: ogen 1-op-1
    return o, 'ANIM_H_SLIDE_WOBBLE'

def bootoo(a):
    # potoo duikt in elkaar (kop/bovenlijf 2 omlaag, 2 lijfrijen weg); staart blijft
    o = knijp(a, 38, 2)
    kop = (o > 0) & (YY <= 23)                          # en de kop kantelt 6 graden linksom (oog als vast blok)
    oog = kop & np.isin(o, [1, 2]) & (XX >= 29) & (XX <= 40) & (YY >= 5) & (YY <= 18)
    o = _kop(o, kop, oog)
    return o, 'ANIM_V_SLIDE'

def globsnail(a):
    # oogsteeltjes schieten 2 uit, sneeuwbol-huis knikt 1 naar voren-omlaag
    o = rek(a, 41, 2, XX <= 23)
    return o, 'ANIM_H_SLIDE'

def clionice(a):
    # rechtervleugel slaat omlaag (draait rechtsom om de schouder), lijf 1 omhoog
    vl = (a > 0) & (XX >= 45) & (YY <= 38)
    o = kolomschuif(a, vl, lambda x: int(round(max(0, x-45)*0.22)))   # vleugel buigt omlaag, voet vast
    return o, 'ANIM_V_SLIDE'

def wagogogon(a):
    # geest juicht: kop + arm 1 omhoog, arm zwaait rechtsom
    arm = (a > 0) & (XX >= 48) & (YY >= 4) & (YY <= 16)
    o = los_draai(a, arm, -14, 51, 17)
    pass
    return o, 'ANIM_H_SLIDE'

def axolaunch(a):
    # vuurpijl tilt op: alles boven rij 44 1 omhoog, de vlam eronder rekt mee (en 1 omlaag)
    o = rek(a, 44, 1)
    o = rek_onder(o, 50, 1)
    return o, 'ANIM_V_SLIDE'

def mate(a):
    # kalebas veert in (1 rij weg boven de voetjes), bombilla wipt rechtsom
    o = knijp(a, 52, 1)
    bomb = (o > 0) & (YY <= 23) & (XX >= 37)
    o = los_draai(o, bomb, -10, 37, 24, knip=True)
    return o, 'ANIM_V_SQUISH_AND_BOUNCE'

def rowmate(a):
    # roeien: rechter bombilla-roeispaan zwaait om de dolpen op de bootrand
    roei = lijn_masker(a, (37, 33), (51, 55), 1.5, [1, 10, 11, 12])
    blad = (a > 0) & (XX >= 49) & (YY >= 54)
    deel = roei | blad
    o = los_draai(a, deel, 10, 41, 40, knip=True, sluit=7)
    return o, 'ANIM_H_SLIDE'

def flytron(a):
    # vleugels slaan omhoog (draaien om de vleugelwortel), omlijning gaat mee
    vl = np.isin(a, [9, 10, 11, 12]) & (YY <= 28)
    vl |= nd.binary_dilation(vl) & (a == 1) & (XX >= 31) & (YY <= 27)
    o = los_draai(a, vl, 12, 29, 27, knip=True)
    return o, 'ANIM_V_SLIDE'

def buzzquito(a):
    # vleugels: bovenste klapt naar links, rechter twee omhoog (samen om de wortel)
    vl = (a > 0) & (((XX >= 21) & (XX <= 31) & (YY <= 15)) | ((XX >= 38) & (YY <= 25)) | ((XX >= 33) & (YY <= 20)))
    o = los_draai(a, vl, 10, 32, 22, knip=True)
    return o, 'ANIM_V_SLIDE'

def capykart(a):
    # capibara knikt (kop draait om de nek naar voren-omlaag, oog als vast blok), kar veert 1 op
    kop = (a > 0) & (XX <= 42) & (YY <= 31) & ~((XX >= 40) & (YY <= 11))
    oog = (XX >= 24) & (XX <= 30) & (YY >= 13) & (YY <= 18) & np.isin(a, [1, 2])
    src = a.copy()
    o = rotsprite_gezicht(src, kop, oog, 6, 40, 31)
    o = dicht(o, a, (a > 0) & ~kop)
    o = rek(o, 47, 1)
    return o, 'ANIM_V_SHAKE'

def zanddjinn(a):
    # djinn zakt 2 in (staart wordt korter), de zwevende handen blijven hangen: tegenbeweging
    hand = (a > 0) & (((XX <= 19) & (YY <= 15)) | ((XX >= 43) & (YY <= 13)))
    o = knijp(a, 47, 2, ~hand)
    o[hand] = a[hand]
    return o, 'ANIM_V_SLIDE'

def glyptodon1(a):
    # schild en kop 1 omhoog (poten strekken), staart zwiept omhoog
    staart = (a > 0) & (XX >= 45) & (YY <= 52)
    o = los_draai(a, staart, 12, 45, 48, knip=True)
    o = rek(o, 51, 1)
    return o, 'ANIM_V_SHAKE'

def glyptodon2(a):
    # lijf 1 omhoog boven de poten, staartknots zwiept naar buiten
    staart = (a > 0) & (XX >= 51) & (YY >= 32)
    o = los_draai(a, staart, -10, 52, 50, knip=True)
    o = rek(o, 47, 1, XX <= 50)
    return o, 'ANIM_V_SHAKE'

def maak_vel(rijen, pad, Z=4, per_rij=2):
    W = 64*Z; bw = 2*W+4+24; H = W+34
    n = len(rijen); R = (n+per_rij-1)//per_rij
    sh = Image.new('RGB', (min(n, per_rij)*bw+8, R*H+8), 'white'); d = ImageDraw.Draw(sh)
    for i, (naam, f1, f2, anim, pal) in enumerate(rijen):
        x0 = 8+(i % per_rij)*bw; y0 = 4+(i//per_rij)*H
        for j, f in enumerate((f1, f2)):
            im = Image.alpha_composite(Image.new('RGBA', (64, 64), (255, 255, 255, 255)), Image.fromarray(rgba(f, pal)))
            sh.paste(im.convert('RGB').resize((W, W), Image.NEAREST), (x0+j*(W+4), y0))
            d.rectangle([x0+j*(W+4), y0, x0+j*(W+4)+W-1, y0+W-1], outline=(200, 200, 200))
        d.text((x0, y0+W+4), f'{naam}: frame 1 | frame 2', fill=(0, 0, 0))
        d.text((x0, y0+W+16), anim, fill=(0, 0, 0))
    sh.save(pad)

FUN = {k: globals()[k] for k in SOORTEN}

if __name__ == '__main__':
    kies = sys.argv[1:] or list(SOORTEN)
    regels, rijen = [], []
    for s in kies:
        a, pal = laad(SOORTEN[s])
        f2, anim = FUN[s](a)
        assert f2.shape == (64, 64) and f2.max() < 16
        save_anim_front(a, f2, pal, f'{s}_anim_front.png')
        chk = np.array(Image.open(f'{s}_anim_front.png'))
        assert (chk[:64] == a).all() and (chk[64:] == f2).all(), s   # frame 1 = front exact
        render_gif(a, f2, pal, anim, f'{s}_anim.gif')
        regels.append(f'{s} {anim}'); rijen.append((s, a, f2, anim, pal))
        print(s, anim, 'pixels anders:', int((f2 != a).sum()))
    if not sys.argv[1:]:
        open('animids.txt', 'w').write('\n'.join(regels)+'\n')
    maak_vel(rijen, 'batch_c_vel.png' if not sys.argv[1:] else os.environ.get('PREVIEW', '/tmp/f2c_preview.png'))
