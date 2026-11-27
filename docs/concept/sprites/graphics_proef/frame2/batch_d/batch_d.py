# Frame 2 per script voor batch D (27 nov), 13 twijfelsoorten, per soort één variant.
# Alleen bestaande pixels verschuiven/rekken/buigen/draaien (../batch_b/f2b.py, RotSprite, connected components);
# engine-animaties uit ../f2lib.py. Wat bloot komt: dicht met de buurkleur van hetzelfde deel (gaten_dicht).
import sys, os, numpy as np
from PIL import Image, ImageDraw
HIER = os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
sys.path.insert(0, HIER); sys.path.insert(0, os.path.join(HIER, '..')); sys.path.insert(0, os.path.join(HIER, '..', 'batch_b'))
from f2lib import save_anim_front, render_gif, rgba
from f2b import *
B = '../../../'

SOORTEN = {
    'hitmongroove': 'hitmontop_evo/af/hitmongroove.png',
    'krassault': 'octillery_evo/af/krassault.png',
    'dundragoon': 'dundragoon/af/dundragoon.png',
    'colugo': 'emolga_evo/af/model.png',
    'fruitvampier': 'emolga_evo_fase3/af/fruitvampier.png',
    'ledian_evo': 'ledian_evo/af/ledian_evo.png',
    'oddish_regional': 'oddish_regional/af/oddish_regional.png',
    'gloom_regional': 'oddish_regional/gloom_sprite/af/gloom.png',
    'vileplume_regional': 'oddish_regional/vileplume_sprite/af/vileplume_regional.png',
    'baltoy_regional': 'baltoy_regional/af/baltoy_regional.png',
    'lotad_gaucho': 'lotad_regional/af/lotad_gaucho.png',
    'grimer_regional': 'grimer_hoenn/af/grimer_hoenn.png',
    'hitmonlee_regional': 'hitmonlee_regional/af/hitmonlee_regional.png',
}

def laad(p):
    im = Image.open(B+p); a = np.array(im)
    if a.shape == (128, 64): a = a[:64]
    assert a.shape == (64, 64) and im.mode == 'P' and a.max() < 16
    return a, im.getpalette()

def deel_uit(a, ruw, zaad=None):
    """Connected component binnen een ruwe zone: alleen de pixels die via het deel zelf samenhangen."""
    cs = comps(a, (a > 0) & ruw)
    cs = sorted(cs, key=lambda m: -m.sum())
    if zaad is None: return cs[0]
    return [m for m in cs if m[zaad[1], zaad[0]]][0]

def hitmongroove(a):
    # breakdance: benen scharen open/dicht om de heup, kop blijft op de grond
    L = deel_uit(a, (XX <= 30) & (YY <= 24), zaad=(18, 4))
    R = deel_uit(a, (XX >= 33) & (YY <= 22), zaad=(48, 6))
    o = rotsprite(a, L, 11, 30, 23)
    o = rotsprite(o, R, -11, 34, 22)
    o = gaten_dicht(o, a, L | R)
    return o, 'ANIM_V_SHAKE'

def krassault(a):
    # kop/mantel komt 1 omhoog uit de rupsbanden, zijtentakels zwaaien 1 naar buiten
    o = rek(a, 44, 1)
    return o, 'ANIM_V_SLIDE'

def dundragoon(a):
    # vleugels slaan omhoog: draaien om de vleugelwortel (RotSprite), kop en lijf blijven
    vl = (a > 0) & (XX >= 25) & (YY <= 24) & ~np.isin(a, [2, 3, 4, 5, 7, 8])
    vl = np.any([m for m in comps(a, vl) if m.sum() >= 20], axis=0)
    o = rotsprite(a, vl, 10, 35, 23)
    o[(a > 0) & ~vl] = a[(a > 0) & ~vl]
    o = gaten_dicht(o, a, vl)
    return o, 'ANIM_V_SLIDE'

def colugo(a):
    # zweefvlieger helt over (bocht), gezicht draait als vast blok mee
    gez = (a > 0) & (XX >= 9) & (XX <= 20) & (YY >= 52) & (YY <= 61)
    o = rotsprite_gezicht(a, a > 0, gez, -8, 30, 34)
    return o, 'ANIM_H_SLIDE_WOBBLE'

def fruitvampier(a):
    # hangt aan de voeten: slingert om het ophangpunt bovenaan
    gez = (a > 0) & (XX >= 15) & (XX <= 29) & (YY >= 38) & (YY <= 46)
    o = rotsprite_gezicht(a, a > 0, gez, 6, 31, 0)
    return o, 'ANIM_H_SLIDE'

def ledian_evo(a, pal):
    # held stoot vooruit: hele figuur kantelt (RotSprite), gezicht als vast blok zodat de ogen 1-op-1 blijven
    gez = (a > 0) & (XX >= 18) & (XX <= 30) & (YY >= 20) & (YY <= 30)
    o = rotsprite_gezicht(a, a > 0, gez, 6, 32, 34)
    return o, 'ANIM_V_SLIDE'

def oddish_regional(a):
    # kelpbladeren veren 2 omhoog (bladvoet rekt), lijf en voetjes blijven
    o = rek(a, 29, 2)
    return o, 'ANIM_V_SQUISH_AND_BOUNCE'

def gloom_regional(a):
    # lavakap en kop komen 1 omhoog, armpjes 1 hoger (gebaar)
    o = rek(a, 40, 1)
    return o, 'ANIM_V_SLIDE'

def vileplume_regional(a):
    # bloem kantelt op de steeltjes, mond blijft 1-op-1
    bloem = (a > 0) & (YY <= 30)
    gez = bloem & (XX >= 24) & (XX <= 40) & (YY >= 9) & (YY <= 17)
    o = rotsprite_gezicht(a, bloem, gez, -6, 32, 31)
    o[(a > 0) & ~bloem] = a[(a > 0) & ~bloem]
    o = gaten_dicht(o, a, bloem)
    return o, 'ANIM_V_SLIDE'

def baltoy_regional(a):
    # armen zwaaien omhoog, monoliet 1 omhoog
    Larm = deel_uit(a, (XX <= 22) & (YY >= 46), zaad=(17, 53))
    Rarm = deel_uit(a, (XX >= 40) & (YY >= 46), zaad=(46, 54))
    o = rotsprite(a, Larm, -22, 22, 47)
    o = rotsprite(o, Rarm, 22, 40, 47)
    o = gaten_dicht(o, a, Larm | Rarm)
    return o, 'ANIM_V_SLIDE'

def lotad_gaucho(a):
    # hoed kantelt naar achteren (groet), gezicht en poncho blijven
    hoed = (a > 0) & (YY <= 37)
    o = rotsprite(a, hoed, 7, 34, 37)
    o[(a > 0) & ~hoed] = a[(a > 0) & ~hoed]
    o = gaten_dicht(o, a, hoed)
    return o, 'ANIM_V_SLIDE'

def grimer_regional(a):
    # slijmarmen rekken 2 omhoog, kop zakt 1 in
    o = rek(a, 28, 2, (XX <= 21) | (XX >= 39))
    return o, 'ANIM_V_SQUISH_AND_BOUNCE'

def hitmonlee_regional(a):
    # trappend been schiet verder door (draait om de heup)
    been = deel_uit(a, ~((YY >= 20) & (XX <= 38)) & (YY <= 31), zaad=(42, 10))
    o = rotsprite(a, been, -8, 42, 30)
    o[(a > 0) & ~been] = a[(a > 0) & ~been]
    o = gaten_dicht(o, a, been)
    return o, 'ANIM_V_SHAKE'

def stofjes_weg(f2, a):
    # losse spikkels (<=2 px) die door het draaien ontstaan en in frame 1 niet bestaan
    klein1 = sum(1 for m in comps(a) if m.sum() <= 2)
    if klein1: return f2
    o = f2.copy()
    for m in comps(f2):
        if m.sum() <= 2: o[m] = 0
    return o

FUN = dict(hitmongroove=hitmongroove, krassault=krassault, dundragoon=dundragoon, colugo=colugo,
           fruitvampier=fruitvampier, oddish_regional=oddish_regional, gloom_regional=gloom_regional,
           vileplume_regional=vileplume_regional, baltoy_regional=baltoy_regional, lotad_gaucho=lotad_gaucho,
           grimer_regional=grimer_regional, hitmonlee_regional=hitmonlee_regional)

def vel(rij, pad='batch_d_vel.png', Z=4, K=3):
    W = 64*Z; n = len(rij); R = (n+K-1)//K
    sh = Image.new('RGB', (8+K*(2*W+28), R*(W+40)+4), 'white'); d = ImageDraw.Draw(sh)
    for i, (s, anim) in enumerate(rij):
        x0, y0 = 8+(i % K)*(2*W+28), 4+(i//K)*(W+40)
        im = Image.open(f'{s}_anim_front.png').convert('RGBA')
        for j in range(2):
            bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(im.crop((0, 64*j, 64, 64*j+64)))
            sh.paste(bg.convert('RGB').resize((W, W), Image.NEAREST), (x0+j*(W+4), y0))
            d.rectangle([x0+j*(W+4), y0, x0+j*(W+4)+W-1, y0+W-1], outline=(210, 210, 210))
        d.text((x0, y0+W+4), f'{s}: frame 1 | frame 2', fill=(0, 0, 0))
        d.text((x0, y0+W+18), anim, fill=(0, 0, 0))
    sh.save(pad)

if __name__ == '__main__':
    kies = sys.argv[1:] or list(SOORTEN)
    regels = []
    for s in kies:
        a, pal = laad(SOORTEN[s])
        f2, anim = ledian_evo(a, pal) if s == 'ledian_evo' else FUN[s](a)
        f2 = stofjes_weg(f2, a)
        assert f2.shape == (64, 64) and f2.max() < 16
        save_anim_front(a, f2, pal, f'{s}_anim_front.png')
        chk = np.array(Image.open(f'{s}_anim_front.png'))
        assert chk.shape == (128, 64) and (chk[:64] == a).all() and (chk[64:] == f2).all(), s   # frame 1 = front exact
        render_gif(a, f2, pal, anim, f'{s}_anim.gif')
        regels.append((s, anim))
        print(s, anim, 'pixels anders:', int((f2 != a).sum()))
    if not sys.argv[1:]:
        open('animids.txt', 'w').write(''.join(f'{s} {an}\n' for s, an in regels))
        vel(regels)
    else:
        vel(regels, 'proef_vel.png')
