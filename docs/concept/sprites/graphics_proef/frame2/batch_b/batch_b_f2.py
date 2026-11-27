# Frame 2 per script voor batch B (27 nov), 17 soorten, per soort één variant.
# Alleen bestaande pixels verschuiven/rekken/buigen/draaien (f2b.py); engine-animaties uit ../f2lib.py.
# Draaien in de geest van Gengas combi_c: lijf kantelt en gaat omhoog, losse delen bewegen tegen in.
import sys, os, numpy as np
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
sys.path.insert(0, HIER); sys.path.insert(0, os.path.join(HIER, '..'))
from f2lib import save_anim_front, render_gif, rgba
from f2b import *
B = '../../../'

SOORTEN = {
    'zandloper2': 'zandloper/fase2/af/zandloper_fase2.png',
    'shuppetto': 'banette_evo/af/shuppetto.png',
    'sunflora_evo': 'sunflora_evo/af/sunflora_evo.png',
    'solrock_evo': 'solrock_evo/af/solrock_evo.png',
    'bloedmaan': 'lunatone_evo/af/bloedmaan.png',
    'dustly': 'dustly/af/dustly.png',
    'hauntflare': 'hauntflare/af/hauntflare.png',
    'claydol_regional': 'baltoy_regional/claydol_af/claydol_regional.png',
    'swablu_regional': 'swablu_regional/af/swablu.png',
    'altaria_regional': 'swablu_regional/altaria/af/altaria.png',
    'pincurchin_regional': 'pincurchin_regional/af/pincurchin_regional.png',
    'staryu_regional': 'staryu_regional/staryu/af/staryu_regional.png',
    'starmie_regional': 'staryu_regional/starmie/af/starmie_regional.png',
    'muk_regional': 'muk_hoenn/af/muk_hoenn.png',
    'dj_rotom': 'dj_rotom/af/dj_rotom.png',
    'regiaqua': 'regiaqua/af/regiaqua.png',
    'regicosmo': 'regicosmo/af/regicosmo.png',
}

def laad(p):
    im = Image.open(B+p); a = np.array(im)
    if a.shape == (128, 64): a = a[:64]
    assert a.shape == (64, 64) and im.mode == 'P'
    return a, im.getpalette()

def groot_klein(a):
    cs = sorted(comps(a), key=lambda m: -m.sum()); return cs[0], cs[1:]

def zandloper2(a):
    lijf, los = groot_klein(a)                 # los = de '!'-hand
    uitroep = los[0]
    o = a.copy(); o[uitroep] = 0
    o = rek(o, 42, 2)                          # lijf + '?' 2 omhoog, staart rekt; zandloper blijft
    ys, xs = np.where(uitroep); o[ys+1, xs] = a[ys, xs]   # '!' 1 omlaag: tegenbeweging
    return o, 'ANIM_V_SLIDE'

def shuppetto(a):
    nz = (a > 0) & (a != 13)
    L = nz & (XX <= 17) & (YY >= 40); R = nz & (XX >= 45) & (YY >= 42)
    o = a.copy(); o[L | R] = 0
    o = knijp(o, 40, 1)                        # kop/lijf/kruizen/draden 1 omlaag (knik)
    ys, xs = np.where(L); o[ys-2, xs] = a[ys, xs]   # poppetjes worden opgetrokken
    ys, xs = np.where(R); o[ys-1, xs+1] = a[ys, xs]
    return o, 'ANIM_V_SLIDE'

def sunflora_evo(a, pal):
    groen = np.zeros(16, bool)
    for i in range(16):
        r, g, b = pal[3*i:3*i+3]; groen[i] = g > r+15 and g > b
    BLAD = groen[a] | ((YY >= 47) & (a > 0) & ~groen[a] & (XX >= 25) & (XX <= 41) & (YY >= 51))
    BLAD = groen[a] & (a > 0)
    stengel = (a > 0) & (YY >= 50)
    kop = (a > 0) & ~BLAD & ~stengel
    o = rotsprite(a, kop, -7, 30, 47)          # bloem kantelt rechtsom op de stengel (draaipunt onderaan)
    o[BLAD | stengel] = a[BLAD | stengel]     # bladeren en stengel blijven staan, liggen vóór
    o = gaten_dicht(o, a, kop)
    return o, 'ANIM_V_SLIDE'

def solrock_evo(a):
    cx, cy = 31, 34
    r = np.hypot(XX-cx, YY-cy)
    buiten = (a > 0) & (r > 17.5)
    o = rotsprite(a, buiten, -10, cx, cy, knip=True)   # stralen en brokjes draaien om de bol (RotSprite)
    o[(a > 0) & (r <= 17.5)] = a[(a > 0) & (r <= 17.5)]   # bol met gezicht blijft staan
    return o, 'ANIM_V_SLIDE'

def bloedmaan(a):
    lijf, los = groot_klein(a)
    ys, xs = np.where(lijf); cx, cy = xs.mean(), ys.mean()
    o = a.copy(); o[lijf] = 0
    o = radiaal(o, los, cx, cy, 2)             # brokken spatten uit elkaar
    ys2, xs2 = np.where(lijf); o[ys2-1, xs2] = a[ys2, xs2]   # maan 1 omhoog
    return o, 'ANIM_V_SLIDE'

def dustly(a):
    lijf, los = groot_klein(a)
    o = a.copy(); [o.__setitem__(m, 0) for m in los]
    gez = lijf & np.isin(a, [1, 2, 9, 10]) & (XX >= 10) & (XX <= 25) & (YY >= 25) & (YY <= 40)
    o = rotsprite_gezicht(o, lijf, gez, -8, 32, 30, 0, -2)   # zoals Gengas: kantelt rechtsom, 2 omhoog; ogen 1-op-1
    for m in los:
        ys, xs = np.where(m); o[ys+2, xs] = a[ys, xs]
    return o, 'ANIM_V_SLIDE'

def hauntflare(a):
    lijf, los = groot_klein(a)
    klauw2 = lijf & (XX >= 51) & (YY >= 36) & (YY <= 47)
    klauw1 = los[0]
    lijf = lijf & ~klauw2
    o = a.copy(); o[klauw1 | klauw2] = 0
    gez = lijf & np.isin(a, [1, 2, 10, 11, 12, 13, 14]) & (XX >= 14) & (XX <= 35) & (YY >= 23) & (YY <= 38)
    o = rotsprite_gezicht(o, lijf, gez, -8, 24, 32, 0, -2)   # bol + ring + vlammen kantelen, 2 omhoog; gezicht 1-op-1
    ys, xs = np.where(klauw1); o[ys+1, xs-1] = a[ys, xs]   # klauwen zakken (tegenbeweging)
    ys, xs = np.where(klauw2); o[ys+2, xs+1] = a[ys, xs]
    return o, 'ANIM_V_SLIDE'

def claydol_regional(a):
    lijf, los = groot_klein(a)
    o = a.copy(); [o.__setitem__(m, 0) for m in los]
    o = knijp(o, 40, 1)                        # kop knikt 1 omlaag (raakt het vak boven)
    for m in los:
        ys, xs = np.where(m); o[ys-2, xs] = a[ys, xs]   # staven 2 omhoog: tegenbeweging
    return o, 'ANIM_V_SLIDE'

def swablu_regional(a):
    o = rek(a, 37, 1)                          # vogel + wolkbovenkant 1 omhoog
    o = rek(o, 23, 1, (XX >= 23) & (XX <= 41))  # bliksemsprietjes nog 1 hoger
    return o, 'ANIM_V_SLIDE'

def altaria_regional(a):
    o = rek(a, 30, 2)                          # kop/kuif/wolkvleugels 2 omhoog, nek rekt
    return o, 'ANIM_V_SLIDE'

def pincurchin_regional(a):
    cx, cy = 32, 38
    r = np.hypot(XX-cx, YY-cy)
    stekels = comps(a, (a > 0) & (r > 19))
    o = radiaal(a, stekels, cx, cy, 1, wis=False)   # stekels 1 px langer (zet op)
    return o, 'ANIM_H_SHAKE'

def staryu_regional(a):
    o = rotsprite(a, a > 0, 12, 31, 33)
    return o, 'ANIM_H_SLIDE_WOBBLE'

def starmie_regional(a):
    o = rotsprite(a, a > 0, -12, 30, 30)
    return o, 'ANIM_H_SLIDE_WOBBLE'

def muk_regional(a):
    arm = (a > 0) & (XX >= 38) & (YY <= 31)
    o = rijschuif(a, arm, lambda y: -int(round((31-y)*0.16)))  # arm buigt naar voren, voet blijft vast
    o = knijp(o, 46, 1, XX < 38)                               # lijf zakt 1 in
    return o, 'ANIM_V_SQUISH_AND_BOUNCE'

def dj_rotom(a):
    o = a.copy()
    oud = {19: 1, 21: 3, 23: 4, 25: 2, 27: 4}; nieuw = {19: 3, 21: 1, 23: 2, 25: 4, 27: 2}
    for c in oud:                              # equalizerbalkjes springen (onderkant rij 49)
        for y in range(45, 50): o[y, c] = 14 if y > 49-nieuw[c] else 8
    bliksem = (a > 0) & (YY <= 22)
    o = rijschuif(o, bliksem, lambda y: int(round((22-y)/9)))  # bliksemspriet buigt naar rechts
    o = rek(o, 51, 1, (XX >= 16) & (XX <= 35))                 # Rotom-kastje veert 1 op de beat, boxen staan
    return o, 'ANIM_V_SHAKE'

def regiaqua(a):
    lijf, los = groot_klein(a)
    o = a.copy(); [o.__setitem__(m, 0) for m in los]
    o = rijschuif(o, lijf, lambda y: int(round(-2+3*(y-12)/49)))   # wervel zwiept: top 2 links
    for m in los:
        ys, xs = np.where(m); o[ys-2, xs] = a[ys, xs]                # armen 2 omhoog
    return o, 'ANIM_H_SLIDE'

def regicosmo(a):
    lijf, los = groot_klein(a)
    ys, xs = np.where(lijf)
    o = baan(a, los, 14, xs.mean(), ys.mean())      # manen draaien om de planeet
    return o, 'ANIM_V_SLIDE'

FUN = dict(zandloper2=zandloper2, shuppetto=shuppetto, solrock_evo=solrock_evo, bloedmaan=bloedmaan,
           dustly=dustly, hauntflare=hauntflare, claydol_regional=claydol_regional, swablu_regional=swablu_regional,
           altaria_regional=altaria_regional, pincurchin_regional=pincurchin_regional, staryu_regional=staryu_regional,
           starmie_regional=starmie_regional, muk_regional=muk_regional, dj_rotom=dj_rotom, regiaqua=regiaqua,
           regicosmo=regicosmo)

if __name__ == '__main__':
    kies = sys.argv[1:] or list(SOORTEN)
    regels = []
    for s in kies:
        a, pal = laad(SOORTEN[s])
        f2, anim = sunflora_evo(a, pal) if s == 'sunflora_evo' else FUN[s](a)
        assert f2.shape == (64, 64) and f2.max() < 16
        save_anim_front(a, f2, pal, f'{s}_anim_front.png')
        chk = np.array(Image.open(f'{s}_anim_front.png'))
        assert (chk[:64] == a).all() and (chk[64:] == f2).all(), s   # frame 1 = front exact
        render_gif(a, f2, pal, anim, f'{s}_anim.gif')
        regels.append(f'{s} {anim}')
        print(s, anim, 'pixels anders:', int((f2 != a).sum()))
    if not sys.argv[1:]:
        open('animids.txt', 'w').write('\n'.join(regels)+'\n')
