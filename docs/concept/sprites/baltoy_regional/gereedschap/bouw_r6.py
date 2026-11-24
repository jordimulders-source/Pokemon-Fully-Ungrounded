# r6 = r5 + afwerking (Jordi: "best prima ... lijnen erg hard en dik, kleur- en schaduwgebruik nog niet goed, weinig tinten,
# lijnen op het lichaam een blur, hoofd 1 px langer onderaan, smooth waar het kan" · "vooral afwerking").
# Vorm: elke gewijzigde vormpixel komt uit de 4 bronpixels (gereedschap/bron.py, r5-coordinaten); kleur vrij (Gen 3-ramp).
import sys; sys.path.insert(0,'gereedschap'); from r4lib import lees, op, rgba; from bron import bron
from klassen import laad; import numpy as np; from PIL import Image
r5=lees('sprite_r5/baltoy_r5.txt'); H,W=len(r5),len(r5[0]); g=[list(r) for r in r5]
LOG=[]
def zet(y,x,c,zone,waarom):
    b=bron(y,x); ok=(c in b) or (c=='.' and '.' in b)
    if g[y][x]!=c: LOG.append((zone,y,x,g[y][x],c,b,ok,waarom)); g[y][x]=c
# ---- A. LIJFRELIEF scherp (r5-rijen 20-27, x11-19): per pixel lijn of vlak uit de bron, dunste lezing ----
# model: zuil tussen natief kol 27 (x13) en kol 32 (x16); links richel natief rij 43 (r21); rechts korte lijn natief rij 40
# (r20, x18-19) en lange lijn natief rij 46 (r23, x17-19). Dubbele lijnen (kol 25 naast 27, kol 35 naast 32, kol 22 naast de rand)
# en de lijnen om de 1,5 px (natief 43/49 rechts) vallen weg: daar is de vlakpixel uit de bron gekozen.
lijn={(y,13) for y in range(20,28)}|{(y,16) for y in range(20,28)}|{(21,11),(21,12),(20,18),(20,19),(23,17),(23,18),(23,19)}
for y in range(20,28):
    for x in range(11,20):
        if x==11 and y>=24: continue      # linkerrand van het lijf (model kol 22) blijft
        b=bron(y,x)
        if (y,x) in lijn and ('d' in b or 'D' in b): c='d' if 'd' in b else 'D'
        else: c='l' if ('l' in b or 'h' in b) else ('M' if 'M' in b else g[y][x])
        zet(y,x,c,'lijfreliëf','lijn/vlak uit bron')
# ---- B. armen: binnenrand rechterarm sluiten ----
zet(24,27,'K','arm rechts','binnenrand open (M aan transparant) -> zwart uit bron MMKM')
# ---- C. HOOFD 1 PX LANGER: rij invoegen onder het gezicht (natief rij 32), kinlijn recht ----
k,_=laad(); S='.KDdmMlhRr'
nat32=[S[v] for v in k[32]]
def uit32(x,voorkeur='lMm'):
    pp=[nat32[2*x],nat32[2*x+1]]
    for t in voorkeur:
        if t in pp: return t
    return pp[0]
nieuw=['.']*W
nieuw[8]='K'                                             # natief kol 16-17 '.K'
for x in range(9,20): nieuw[x]=uit32(x)                  # gezicht onderste rij (natief 32), vulpixel gekozen
nieuw[11]='l'; nieuw[15]='l'                             # natief 'ld'/'Md': vlakpixel (geen losse groef)
nieuw[20]='D'; nieuw[21]='m'; nieuw[22]='m'; nieuw[23]='m'; nieuw[24]='K'   # natief rij 32/33 kol 40-49: 'MD mm mK mm(r33) K.'
nieuw[9]='M'                                             # natief 'MM'
chin=list(g[16]); 
for x in range(17,21): chin[x]='K'                       # kinlijn recht: natief rij 34 'KKKK' (rechterdeel kin)
oud17=list(g[17])
for x in range(17,20): oud17[x]='m'                      # oude kinpixels onder het rechterdeel -> schaduw lijf (bron KKmm)
oud17[20]='D'                                            # hoek (bron KKDm)
g=g[:16]+[nieuw,chin,oud17]+g[18:]
LOG.append(('kop +1 rij',16,'*','-','rij',None,True,'natief rij 32 ingevoegd; kin r17 x17-20 K (natief 34), r18 x17-20 m/D (bron)'))
H=len(g)
open('gereedschap/baltoy_r6_klassen.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')   # vorm (klassen) voor r7
# ---- D. KLEUR: Gen 3-ramp, licht linksboven, warm licht / koele schaduw ----
PAL={'.':(255,255,255),'H':(238,231,210),'1':(212,202,176),'2':(182,172,148),'3':(148,140,124),'4':(114,108,100),
     'L':(86,78,74),'S':(104,90,78),'K':(40,32,36),'R':(220,90,86),'r':(166,52,60),'P':(240,138,124)}
nb=lambda y,x: g[y][x] if 0<=y<H and 0<=x<W else '.'
out=[['.']*W for _ in range(H)]
def regio(y,x):
    if y<=1 and x<=21: return 'top'
    if y<=8 and x<=21: return 'band'
    if y<=9 and x>=22: return 'bandzij'
    if y<=17 and x<=20: return 'gezicht'
    if y<=17: return 'gezichtzij'
    if y>=30 and 12<=x<=22: return 'punt'
    if 10<=x<=20 and y<=29: return 'lijf'
    if 21<=x<=24 and y<=29: return 'lijfzij'
    return 'arm'
for y in range(H):
    for x in range(W):
        c=g[y][x]
        if c=='.': continue
        rand=any(nb(y+a,x+b)=='.' for a,b in((1,0),(-1,0),(0,1),(0,-1)))
        schaduwrand=nb(y,x+1)=='.' or nb(y+1,x)=='.'
        R=regio(y,x)
        if c in 'Rr': out[y][x]=c; continue
        if rand and c in 'KDdm' or (rand and c=='K'):
            out[y][x]='K' if (c=='K' or (schaduwrand and c in 'KDdm') or (R=='arm' and x>=21)) else 'S'; continue   # rechterarm: hele rand zwart (geen S/K om en om)
        if c=='K': out[y][x]='L'; continue                     # binnen: geen zwart
        if c=='D': out[y][x]='L' if R in ('band','bandzij','gezicht') and not (R=='gezicht' and x==20) else '4'; continue
        if R=='top': out[y][x]={'l':'H','h':'H','M':'1','m':'2','d':'4'}.get(c,'1')
        elif R=='band': out[y][x]={'l':'1','h':'H','M':'2','m':'2','d':'4'}[c]
        elif R in ('bandzij','gezichtzij','lijfzij'): out[y][x]={'l':'2','h':'2','M':'2','m':'3','d':'4'}[c]
        elif R=='gezicht': out[y][x]={'l':'1','h':'H','M':'2','m':'2','d':'4'}[c]
        elif R=='lijf': out[y][x]={'l':'1','h':'H','M':'2','m':'3','d':'4'}[c]
        elif R=='punt': out[y][x]={'l':'1','h':'1','M':'2','m':'3','d':'4','D':'4'}.get(c,'3')
        else: out[y][x]={'l':'1','h':'H','M':'2','m':'3','d':'4'}[c]
# schaduw/volume (alleen kleur):
for y in range(H):
    for x in range(W):
        o=out[y][x]
        if regio(y,x)=='bandzij' and y==9 and o in '23': out[y][x]='4'        # schaduw onder de band op de zijkant
        if regio(y,x)=='gezichtzij' and o=='3' and y in (10,): out[y][x]='4'   # onder de bandoverhang
        if regio(y,x)=='lijfzij' and o in '23' and y in (18,19): out[y][x]='4' # onder de kop
        if regio(y,x)=='lijf' and y==18 and o in '123': out[y][x]='3'         # schaduw onder de kin
        if regio(y,x)=='lijf' and y==19 and o=='1': out[y][x]='2'
        if regio(y,x)=='lijf' and x==19 and 20<=y<=27 and o=='1': out[y][x]='2' # voorvlak loopt naar de hoek iets af
        if regio(y,x)=='lijf' and y==28 and o in '12': out[y][x]='2'           # onderaan het lijf
        if regio(y,x)=='lijf' and y==29 and o in '123': out[y][x]='3'
        if regio(y,x)=='gezicht' and x==19 and 13<=y<=16 and o=='1': out[y][x]='2'
        if regio(y,x)=='band' and y==3 and o=='1' and x<=13: out[y][x]='H'    # bovenkant band vangt licht (links)
        if regio(y,x)=='arm' and o=='2' and any(nb(y+a,x+b)=='K' for a,b in((1,0),(0,1),(0,-1))) and any(out[y+a][x+b]=='2' for a,b in((-1,0),(0,-1),(0,1)) if 0<=y+a<H and 0<=x+b<W): out[y][x]='3'  # onderzijde arm
rows=[''.join(r) for r in out]
UIT='sprite_r6/baltoy_r6'; open(UIT+'.txt','w').write('\n'.join(rows)+'\n')
for y,r in enumerate(rows): print('%2d %s'%(y,r))
keys=list(PAL); full=np.zeros((64,64),'uint8'); y0=64-H-1+ (1 if not any(c!='.' for c in rows[-1]) else 0); x0=(64-W)//2
for y,r in enumerate(rows):
    for x,c in enumerate(r): full[y0+y,x0+x]=keys.index(c)
im=Image.fromarray(full,'P'); im.putpalette([v for kk in keys for v in PAL[kk]]+[0]*(768-3*len(keys))); im.save(UIT+'.png',transparency=0)
op(rgba(Image.open(UIT+'.png')),(255,255,255,255),8).save(UIT+'_8x.png')
from collections import Counter
print('vormwijzigingen per zone:',Counter(l[0] for l in LOG))
print('niet uit bron:',[l for l in LOG if not l[6]])
