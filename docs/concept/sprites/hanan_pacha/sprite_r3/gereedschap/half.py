# Stap 2: exacte 2x-reductie van het natieve raster met regels; elke uitkomst is een bestaande modelkleur (label).
# Groepen: L lijn, T donkere penpunt, G goud, W wit/ivoor, R rood. Regels per 2x2-blok:
#  >=3 achtergrond -> achtergrond; lijn >=2 -> lijn; 1 lijnpixel -> lijn als de lijn buiten het blok aan twee kanten doorloopt
#  (anders breekt hij); punt >=2 -> punt; anders de meest voorkomende groep, daarbinnen de meest voorkomende kleur (gelijk: donkerste).
import numpy as np, sys
N=np.load('natief.npy'); PAL=np.load('natief_pal.npy')
GR={}
for k in (2,18): GR[k]='L'
for k in (6,14,23): GR[k]='T'
for k in (1,5,25): GR[k]='D'
for k in (24,15,20,0,11,19,13,4,21,27): GR[k]='G'
for k in (17,3,16,9,7,26): GR[k]='W'
for k in (8,12,10,22): GR[k]='R'
lum=PAL@np.array([.299,.587,.114])
def reduceer(oy,ox):
    H,W=N.shape; h,w=(H-oy)//2,(W-ox)//2; o=np.full((h,w),-1)
    for j in range(h):
        for i in range(w):
            Y,X=oy+2*j,ox+2*i; b=N[Y:Y+2,X:X+2].ravel(); f=b[b>=0]
            if len(f)<=1: continue
            g=[GR[k] for k in f]; kk=None
            for G in ('L','D'):
                nG=g.count(G)
                if nG>=2: kk=[k for k in f if GR[k]==G]; break
                if nG==1:
                    yy,xx=[(Y+d//2,X+d%2) for d in range(4) if b[d]>=0 and GR[b[d]]==G][0]
                    buiten=[(yy+dy,xx+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and not(Y<=yy+dy<Y+2 and X<=xx+dx<X+2)
                            and 0<=yy+dy<H and 0<=xx+dx<W and N[yy+dy,xx+dx]>=0 and GR[N[yy+dy,xx+dx]]==G]
                    if any(abs(p[0]-q[0])>1 or abs(p[1]-q[1])>1 for p in buiten for q in buiten): kk=[k for k in f if GR[k]==G]; break
            if kk is None and g.count('T')>=2: kk=[k for k in f if GR[k]=='T']
            if kk is None:
                rest=[k for k in f if GR[k] not in 'LD'] or f; gg=[GR[k] for k in rest]
                best=max(set(gg),key=lambda x:(gg.count(x),-min(lum[k] for k in rest if GR[k]==x)))
                kk=[k for k in rest if GR[k]==best]
            o[j,i]=max(set(kk),key=lambda k:(kk.count(k),-lum[k]))
    return o
if __name__=='__main__':
    from PIL import Image
    oy,ox=int(sys.argv[1]),int(sys.argv[2]); o=reduceer(oy,ox)
    np.save('half_%d%d.npy'%(oy,ox),o)
    img=np.full(o.shape+(3,),255,'uint8'); img[o>=0]=PAL[o[o>=0]]
    Image.fromarray(img).resize((o.shape[1]*8,o.shape[0]*8),Image.NEAREST).save(sys.argv[3])
    ys,xs=np.where(o>=0); print(o.shape,'fig',xs.max()-xs.min()+1,ys.max()-ys.min()+1)
