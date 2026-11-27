# Overbodige rechte lijnen: lijnpixels (1/2) in rechte stukken >= 4 px (recht.py) waarvan het natieve 2x2-blok GEEN modellijn
# heeft (sterkte 0). Binnenin -> de kleur van de kale versie op die plek (of de meest voorkomende vulbuur); op de buitenrand aan
# de lichtkant (achtergrond boven/links) -> selout = donkerste eigen tint; op de schaduwkant blijft de buitenlijn zwart.
import sys,numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'../sprite_r3/gereedschap')
from kaart import blok; from recht import runs; from half import GR
N=np.load('../sprite_r3/natief.npy'); KAAL=np.load('../sprite_r3/stap_palet.npy')
GRP={2:'g',3:'g',4:'g',5:'g',6:'w',7:'w',14:'w',8:'r',9:'r',10:'r',11:'o',12:'o',13:'t',15:'t'}
DONKER={'g':2,'w':6,'r':8,'o':11,'t':13}
def sterkte(X,Y):
    x,y=blok(X,Y); b=[N[y+a,x+c] for a in (0,1) for c in (0,1) if y+a<160 and x+c<160]
    return sum(1 for k in b if k>=0 and GR[k] in 'LD')
def g(o,Y,X): return o[Y,X] if 0<=Y<64 and 0<=X<64 else 0
def repareer(o,beschermd=None):
    o=o.copy(); v=o.copy(); gewijzigd=[]
    for (dy,dx),Y,X,n in runs(v):
        for i in range(n):
            YY,XX=Y+dy*i,X+dx*i
            if beschermd is not None and beschermd[YY,XX]: continue
            if v[YY,XX] not in (1,2) or sterkte(XX,YY)>0: continue
            u,d,l,r=g(v,YY-1,XX),g(v,YY+1,XX),g(v,YY,XX-1),g(v,YY,XX+1)
            if 0 in (u,d,l,r):
                if d==0 or r==0: continue                      # schaduwkant: buitenlijn blijft zwart
                gs=[GRP[q] for q in (u,d,l,r) if q in GRP and q!=2]
                if not gs: continue
                G=max(set(gs),key=gs.count); nieuw=DONKER[G]
            else:
                nieuw=KAAL[YY,XX]
                if nieuw in (0,1,2):
                    nb=[q for q in (u,d,l,r) if q not in (0,1,2)]
                    if not nb: continue
                    nieuw=max(set(nb),key=nb.count)
            if nieuw!=o[YY,XX]: o[YY,XX]=nieuw; gewijzigd.append((YY,XX))
    return o,gewijzigd

def binnenlijn_goud(o,MIN=4,beschermd=None):
    """Zwarte binnenlijnen in rechte stukken >= MIN px die geheel in goud liggen (alle niet-lijnburen goud, geen
    achtergrond in de 8-buurt) -> donkerste goudtint 2 (Gen 3: binnenlijn in de eigen tint, Ho-Oh doet dat ook)."""
    v=o.copy(); o=o.copy(); gew=[]
    N8=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if a or b]
    for (dy,dx),Y,X,n in runs(v,ks=(1,),MIN=MIN):
        for i in range(n):
            YY,XX=Y+dy*i,X+dx*i
            if beschermd is not None and beschermd[YY,XX]: continue
            nb=[g(v,YY+a,XX+b) for a,b in N8]
            if 0 in nb: continue
            vul=[q for q in nb if q not in (1,2)]
            if vul and all(GRP.get(q)=='g' for q in vul) and o[YY,XX]==1: o[YY,XX]=2; gew.append((YY,XX))
    return o,gew
