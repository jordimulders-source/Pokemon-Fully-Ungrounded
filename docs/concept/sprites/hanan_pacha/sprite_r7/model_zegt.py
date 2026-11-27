# Per spritepixel in de klauwzones: wat zegt het model r7 (natief 2x2-blok via kaart.py)? Klasse: L lijn, K klauw (ivoor/wit),
# T teen (goud, met toon), . achtergrond. Regels: klauw bij >=1 witte/ivoren pixel (vorm voor kleur), lijn bij >=2 of 1 die buiten
# het blok doorloopt, achtergrond bij >=3, anders teen; toon teen = gemiddelde modelhelderheid (licht/midden/schaduw).
import sys,numpy as np; sys.path.insert(0,'../sprite_r4'); sys.path.insert(0,'../sprite_r3/gereedschap')
from kaart import blok; from half import GR
N=np.load('../sprite_r3/natief.npy'); P=np.load('../sprite_r3/natief_pal.npy'); lum=P@np.array([.299,.587,.114])
KMIN=2
ZONES=[(21,31,49,52),(32,38,49,52)]
def iskl(k): return k>=0 and GR[k]=='W' and lum[k]>185
def model(X,Y):
    x,y=blok(X,Y); b=[(y+a,x+c) for a in (0,1) for c in (0,1)]
    ks=[N[p] for p in b]; nL=sum(1 for k in ks if k>=0 and GR[k]=='L')
    if sum(1 for k in ks if k<0)>=3: return ('.',None)
    if sum(iskl(k) for k in ks)>=KMIN: return ('K',None)
    if nL>=2: return ('L',None)
    if nL==1:
        (yy,xx)=[p for p,k in zip(b,ks) if k>=0 and GR[k]=='L'][0]
        bu=[(yy+dy,xx+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (yy+dy,xx+dx) not in b and N[yy+dy,xx+dx]>=0 and GR[N[yy+dy,xx+dx]]=='L']
        if any(abs(p[0]-q[0])>1 or abs(p[1]-q[1])>1 for p in bu for q in bu): return ('L',None)
    gl=[lum[k] for k in ks if k>=0 and GR[k] in 'GDT']
    m=np.mean(gl) if gl else 150
    return ('T',10 if m>185 else (9 if m>150 else 8))
if __name__=='__main__':
    for x0,x1,y0,y1 in ZONES:
        for Y in range(y0,y1+1): print(Y,''.join(model(X,Y)[0] if model(X,Y)[0]!='T' else str(model(X,Y)[1]%10) for X in range(x0,x1+1)))
        print()
