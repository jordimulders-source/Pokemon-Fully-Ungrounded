"""Cuyby-icoon route 3: Gemini-driekwartmodel (gemini_r1.png, door Jordi goedgekeurd: "hij is ietsje anders geworden,
maar dat is niet erg voor een icoon") -> natief raster (natief.png, 16 px-cellen) -> frontpalet (q.npy) ->
rijen/kolommen schrappen -> dichtstbijzijnde pal3-index -> alleen: los weg / omlijning dicht. Niets getekend.
python3 bouw.py [naam]"""
import sys,numpy as np; from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/'
q=np.load('q.npy')
fr=Image.open(R+'docs/concept/sprites/cuyby/ronde4/anim_front.png'); FP=np.array(fr.getpalette()[:48]).reshape(16,3)
PAL=3; IP=np.array([[int(v) for v in l.split()[:3]] for l in open(R+f'graphics/pokemon/icon_palettes/pal{PAL}.pal').read().split('\n')[3:19]])
NEAR={0:0}|{k:int(((IP[1:]-FP[k])**2).sum(1).argmin()+1) for k in range(1,16)}
# bijna-gelijke afstanden: kies de tint met dezelfde kleurtoon (crèmeschaduw 2434 grijs vs 2645 geelcrème; oogbruin 3330 rood vs 3620 donker)
NEAR[4]=12; NEAR[15]=14
RIJ=[14,16,18,19,21,23,24,26,28,29,31,33,34,36,38,39,41,43,44,46]   # gelijkmatig, factor 0,6 (zelfde factor als KOL: verhoudingen blijven)
KOL=[17,19,21,22,24,26,27,29,31,32,34,36,37,39,41,42,44,46]
LOG=[]
def opschonen(c):
    c=c.copy(); h,w=c.shape
    for _ in range(2):
        for y in range(h):
            for x in range(w):
                if not c[y,x]: continue
                n=[c[yy,xx] if 0<=yy<h and 0<=xx<w else 0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
                if sum(1 for t in n if t)<=1: c[y,x]=0; LOG.append((x,y,'los weg'))
    return c
def sluit(f):
    f=f.copy(); m=f>0; p=np.pad(m,1); edge=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
    ys,_=np.nonzero(m); mid=(ys.min()+ys.max())/2; lum=IP.mean(1)
    for y,x in zip(*np.nonzero(edge)):
        if lum[f[y,x]]>=110 and f[y,x]!=7:   # roze oortjes blijven
            f[y,x]=15 if y<mid else 14; LOG.append((x,y,'omlijning dicht'))
    return f
def plaats(c):
    h,w=c.shape; out=np.zeros((32,32),np.uint8); oy=29-h+1; ox=15-w//2; out[oy:oy+h,ox:ox+w]=c; return out
def frame2(f1):
    ys,_=np.nonzero(f1); top,bot=ys.min(),ys.max()
    f2=np.zeros_like(f1); f2[top+1:bot]=f1[top:bot-1]; f2[bot]=f1[bot]   # alles 1 omlaag, rij boven de voet vervalt
    f2[top:top+2]=f1[top:top+2]   # gebaar: oren blijven staan = spitsen 1 px
    return f2
if __name__=='__main__':
    naam=sys.argv[1] if len(sys.argv)>1 else 'icon'
    r=np.vectorize(NEAR.get)(q[np.ix_(RIJ,KOL)]).astype(np.uint8)
    f1=sluit(plaats(opschonen(r)))
    out=np.zeros((64,32),np.uint8); out[:32]=f1; out[32:]=frame2(f1)
    im=Image.fromarray(out,'P'); im.putpalette(IP.flatten().tolist()+[0]*(768-48)); im.save(naam+'.png',transparency=0)
    print('map',NEAR); print('ingrepen',LOG)
    for y in range(32):
        s=''.join('.' if v==0 else '%x'%v for v in f1[y])
        if s.strip('.'): print('%2d '%y+s)
