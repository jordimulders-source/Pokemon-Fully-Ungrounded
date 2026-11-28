"""Cuyby-icoon zonder zelf tekenen (Jordi 28 nov: "zelf tekenen ... moet echt verboden worden").
Frame 1 = front frame 1 met rijen/kolommen geschrapt (elke pixel is een frontpixel), kleuren naar het
dichtstbijzijnde pal0-index. Daarna alleen de vier toegestane ingrepen (zie NOTITIES.md).
python3 schrap.py naam  (vanuit de repo-root)"""
import sys,numpy as np
from PIL import Image
D='docs/concept/sprites/cuyby/'
fr=Image.open(D+'ronde4/anim_front.png'); FP=np.array(fr.getpalette()[:48]).reshape(16,3); F=np.array(fr)
IP=np.array([[int(v) for v in l.split()[:3]] for l in open('graphics/pokemon/icon_palettes/pal0.pal').read().split('\n')[3:19]])
NEAR={0:0}|{k:int(((IP[1:]-FP[k])**2).sum(1).argmin()+1) for k in range(1,16)}
KOL=[int(v) for v in sys.argv[2].split(',')] if len(sys.argv)>2 else [16,17,19,20,21,23,24,26,27,28,30,31,33,34,36,38,40,42,44,46]
RIJ=[int(v) for v in sys.argv[3].split(',')] if len(sys.argv)>3 else [15,16,18,19,20,22,24,26,28,29,31,33,34,36,38,40,42,44,45,46]
def reduceer(f):
    """Rijen/kolommen schrappen; kleur = dichtstbijzijnde pal0-index. Uitzondering (omlijning):
    de oranje omlijningskleur 9 van de front wordt omlijning 15 (anders valt de rechterrand open, 9 -> 6 is licht)."""
    r=f[np.ix_(RIJ,KOL)]; m=dict(NEAR); m[9]=15
    if VAR=='B': m[11]=14; m[10]=1   # zwarte vacht zoals Houndour (pal0): vacht 14, glans 1; oog en omlijning blijven 15
    return np.vectorize(m.get)(r).astype(np.uint8), r
LOG=[]
def opschonen(c,bron):
    """Alleen toegestane ingrepen, automatisch en gelogd:
    los weg: pixel met <=1 gevulde 4-buur aan de rand -> weg;
    los weg: 1-px eiland lichtroze 11 of grijs 14 midden in creme 3 (schaduwspikkel) -> creme."""
    c=c.copy(); h,w=c.shape
    def nb(y,x): return [c[yy,xx] if 0<=yy<h and 0<=xx<w else 0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
    for _ in range(2):
        for y in range(h):
            for x in range(w):
                v=c[y,x]
                if not v: continue
                n=nb(y,x)
                if sum(1 for t in n if t)<=1: c[y,x]=0; LOG.append((x,y,'los weg (bungelend)'))
                elif v in (11,14) and bron[y,x] in (4,5,10) and all(t==3 for t in n): c[y,x]=3; LOG.append((x,y,'los weg (spikkel in creme)'))
                elif VAR=='A' and v==14 and bron[y,x]==10 and all(t in (15,0) for t in n) and sum(1 for t in n if t==15)>=3: c[y,x]=15; LOG.append((x,y,'los weg (glansspikkel in zwart)'))
    return c
def sluit(f1,bron1):
    """omlijning dicht: lichte randpixel (4-buur transparant) waar de geschrapte omlijning ontbrak -> 15 boven, 14 onder.
    Roze kussentjes/oortjes (front 12/13) blijven."""
    f=f1.copy(); m=f>0; pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    ys,_=np.nonzero(m); mid=(ys.min()+ys.max())/2; lum=IP.mean(1)
    for y,x in zip(*np.nonzero(edge)):
        if lum[f[y,x]]>=110 and bron1[y,x] not in (12,13):
            f[y,x]=15 if y<mid else 14; LOG.append((x,y,'omlijning dicht'))
    return f
def plaats(c):
    h,w=c.shape; out=np.zeros((32,32),np.uint8); oy=29-h+1; ox=16-w//2; out[oy:oy+h,ox:ox+w]=c; return out
def frame2(f1):
    """Stap 7 met verschuiven: alles t/m y26 1 px omlaag, rij 27 vervalt, y28-29 blijven."""
    f2=np.zeros_like(f1); f2[11:28]=f1[10:27]; f2[28:]=f1[28:]
    f2[10:13,21:25]=f1[10:13,21:25]   # gebaar: oranje oor (als geheel) blijft staan = spitst 1 px
    return f2
VAR='A'
INGREPEN=[]   # (x,y,nieuw,soort) soort: los weg / kleur dichtstbij / omlijning dicht / deel weg
if __name__=='__main__':
    naam=sys.argv[1]; VAR='B' if naam.endswith('B') else 'A'
    r,b=reduceer(F[:64]); f1=sluit(plaats(opschonen(r,b)),plaats(b))
    for x,y,v,soort in INGREPEN: f1[y,x]=v
    out=np.zeros((64,32),np.uint8); out[:32]=f1; out[32:]=frame2(f1)
    im=Image.fromarray(out,'P'); im.putpalette(IP.flatten().tolist()); im.save(D+f'icoon/schrap/{naam}.png')
    print('map',NEAR); print('ingrepen',LOG)
    for y in range(32):
        r=''.join('.' if v==0 else '%x'%v for v in f1[y])
        if r.strip('.'): print('%2d '%y+r)
