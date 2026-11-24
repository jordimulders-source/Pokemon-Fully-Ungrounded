# r5 (Jordi: "ik zie dat heel veel opnieuw getekend is"): basis = kaal34 (kale 2x2-reductie van het model).
# Elke wijziging kiest een van de 4 bronpixels van het blok (gereedschap/bron.py); uitzonderingen staan apart in NIETBRON.
# Tintkeuze naar het palet (h->l, ringpixels ->d) telt als kleur, niet als vorm.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import *; from bron import bron
kaal=lees('gereedschap/kaal34.txt'); H,W=len(kaal),len(kaal[0]); g=[list(r) for r in kaal]
LOG=[]; NIETBRON=[]
def zet(y,x,c,waarom,tint=None):
    b=bron(y,x); bc=tint or c
    if c=='.': ok=b.count('.')>=1
    else: ok=bc in b
    if not ok: NIETBRON.append((y,x,c,b,waarom))
    if g[y][x]!=c: LOG.append((y,x,g[y][x],c,b,waarom)); g[y][x]=c
# ---- 1. GEZICHT: ronde ogen (4 breed, 5 hoog) met streep, rood als vlak boven de ogen met de V ertussen ----
F={  # (y,x): (kleur, bronklasse waaruit gekozen of None=zelfde)
}
rijen={
 9:(7,'DRRRRMMMRRRRRD'),
10:(7,'mRddRRlRRddRRD'),
11:(7,'rdlldRRRdlldRD'),
12:(7,'dDDDDlRlDDDDrD'),
13:(7,'.dlldlrldlldlD'),
14:(7,'.dddlllllddllD'),
15:(7,'.KllldMdlllllD'),
}
# tintafbeelding: ringpixels zijn in het model m/M/d (middengrijze ring); op het palet -> d
for y,(x0,s) in rijen.items():
    for i,c in enumerate(s):
        x=x0+i
        if c==g[y][x]: continue
        b=bron(y,x)
        tint=None
        if c=='d' and 'd' not in b:
            for t in 'mMD':
                if t in b: tint=t; break
        if c=='R' and 'R' not in b and 'r' in b: tint='r'
        zet(y,x,c,'gezicht: oog/rood/mond',tint)
# ---- 2. BUITENLIJN sluiten + h->l ----
nb=lambda y,x: g[y][x] if 0<=y<H and 0<=x<W else '.'
for y in range(H):
    for x in range(W):
        c=g[y][x]
        if c=='.': continue
        if c=='h': zet(y,x,'l','tint h->l (palet, 3 tinten)',tint='h'); c='l'
        if not (9<=y<=15 and 7<=x<=20):   # gezicht hierboven al gedaan
            schaduw=nb(y,x+1)=='.' or nb(y+1,x)=='.'
            licht=nb(y,x-1)=='.' or nb(y-1,x)=='.'
            if (schaduw or licht) and c in 'lMm':
                b=bron(y,x)
                if schaduw and 'K' in b: zet(y,x,'K','buitenlijn schaduwkant (zwart uit bron)')
                elif licht and c in 'lM':
                    for t in 'Ddm':
                        if t in b: zet(y,x,t,'buitenlijn lichtkant (selout uit bron)'); break
                elif schaduw and c in 'lM':
                    for t in 'KDdm':
                        if t in b: zet(y,x,t,'buitenlijn schaduwkant (donkerste bron)'); break
zet(17,22,'m','losse ruis: m-pixel (17,23) ingesloten door zwart; bron mmKK')
zet(21,4,'m','buitenlijn lichtkant: tint d->m, zelfde selout als de rest van de armrand',tint='d')
rows=[''.join(r) for r in g]
UIT='sprite_r5/baltoy_r5'
open(UIT+'.txt','w').write('\n'.join(rows)+'\n')
for y,r in enumerate(rows): print('%2d %s'%(y,r))
print('gewijzigd t.o.v. kaal34:',len(LOG))
for l in LOG: print('  (%d,%d) %s->%s bron %s  %s'%l)
print('NIET uit de bronpixels:',NIETBRON)
pi=png(rows,UIT+'.png'); op(rgba(pi),(255,255,255,255),8).save(UIT+'_8x.png')
