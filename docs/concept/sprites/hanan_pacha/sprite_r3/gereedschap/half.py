# Stap 2: exacte 2x-reductie van het natieve raster met regels; elke uitkomst is een bestaande modelkleur (label).
# Groepen: L lijn, T donkere penpunt, G goud, W wit/ivoor, R rood. Regels per 2x2-blok:
#  >=3 achtergrond -> achtergrond; lijn >=2 -> lijn; 1 lijnpixel -> lijn als de lijn buiten het blok aan twee kanten doorloopt
#  (anders breekt hij); punt >=2 -> punt; anders de meest voorkomende groep, daarbinnen de meest voorkomende kleur (gelijk: donkerste).
import numpy as np, sys
import os
N=np.load('natief2.npy' if os.path.exists('natief2.npy') and __name__=='__main__' else 'natief.npy'); PAL=np.load('natief_pal.npy')
GR={}
for k in (2,18): GR[k]='L'
for k in (6,14,23): GR[k]='T'
for k in (1,5,25): GR[k]='D'
for k in (24,15,20,0,11,19,13,4,21,27): GR[k]='G'
for k in (17,3,16,9,7,26): GR[k]='W'
for k in (8,12,10,22): GR[k]='R'
for k in range(28): GR[100+k]='O'; GR[200+k]='K'
lum=PAL@np.array([.299,.587,.114]); lum=np.concatenate([lum,np.zeros(72),lum,np.zeros(72),lum])
PALX=np.concatenate([PAL,np.zeros((72,3),int),PAL*0+[222,118,50],np.zeros((72,3),int),PAL*0+[166,48,63]])
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
                staart=Y>=104 and not((53<=X<=74 and Y<=122) or (76<=X<=93 and Y<=121))
                voet=104<=Y<=123 and (53<=X<=74 or 76<=X<=93)
                if voet and G=='D': continue   # poten: geen schaduwstreepjes, tenen = goud + zwarte lijn + klauw
                if staart and G=='D':   # staart: veerscheiding uit de bovenste natieve rij van het blok (periode 5 -> d s d s s, doorlopend)
                    top=[k for k in b[:2] if k>=0 and GR[k] in 'DL']
                    if top: kk=top; break
                    continue
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

# Vorm gaat voor vlakkleur (Jordi: "de vormen zijn belangrijker dan welke kleur dominant is"): kleine natieve vormen
# (klauw, snavelhaak, oog, kamrand, lijnstukje, penpunt; <=16 px, groep niet goud) die na de reductie nergens meer
# terugkomen, krijgen het blok waar het grootste deel van hun pixels ligt.
def vorm_terug(o,oy,ox,MAX=16):
    from scipy import ndimage
    H,W=N.shape; h,w=o.shape; n=0
    for G in 'LTW':
        m=np.zeros(N.shape,bool)
        for k,g in GR.items():
            if g==G: m|=N==k
        lab,nc=ndimage.label(m,structure=np.ones((3,3)))
        for c in range(1,nc+1):
            ys,xs=np.where(lab==c)
            voet=(104<=ys.mean()<=123) and (53<=xs.mean()<=93)
            if len(ys)>MAX or (len(ys)<3 and not(voet and G=='W')): continue
            bj=(ys-oy)//2; bi=(xs-ox)//2; ok=(bj>=0)&(bi>=0)&(bj<h)&(bi<w)
            if not ok.any(): continue
            blokken=set(zip(bj[ok],bi[ok]))
            if any(o[j,i]>=0 and GR[o[j,i]]==G for j,i in blokken): continue
            cnt={}
            for j,i in zip(bj[ok],bi[ok]): cnt[(j,i)]=cnt.get((j,i),0)+1
            j,i=max(cnt,key=cnt.get); kk=[N[y,x] for y,x in zip(ys,xs)]
            o[j,i]=max(set(kk),key=kk.count); n+=1
    return n

if __name__=='__main__':
    from PIL import Image
    oy,ox=int(sys.argv[1]),int(sys.argv[2]); o=reduceer(oy,ox); print('vormen terug',vorm_terug(o,oy,ox))
    np.save('half_%d%d.npy'%(oy,ox),o)
    img=np.full(o.shape+(3,),255,'uint8'); img[o>=0]=PALX[o[o>=0]]
    Image.fromarray(img).resize((o.shape[1]*8,o.shape[0]*8),Image.NEAREST).save(sys.argv[3])
    ys,xs=np.where(o>=0); print(o.shape,'fig',xs.max()-xs.min()+1,ys.max()-ys.min()+1)
