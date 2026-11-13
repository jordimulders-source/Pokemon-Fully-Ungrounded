# natief (figuur 96x96) -> exacte 2x2-reductie met regels -> 64x64 geindexeerd (onderlaag r1).
# Niets wordt getekend: elke spritepixel komt uit zijn 2x2-blok modelpixels.
#  - silhouet: blok is figuur als >=2 van de 4 modelpixels figuur zijn; gaten in het model (achtergrond) idem.
#  - buitenrand (en rand van gaten): 1 px omlijning waar het model daar zwart heeft (blok of 1-px-ring eromheen);
#    waar het model een gekleurde rand heeft (bovenkant staart) houdt het blok de modeltoon.
#  - binnenlijnen: blok met >=2 zwarte modelpixels = lijn; blok met 1 zwarte modelpixel alleen als brug
#    (anders breekt een modellijn in de sprite in twee stukken).
#  - vulling: meest voorkomende modeltoon in het blok (gelijkspel: tint linksboven, anders donkerste).
# Gebruik: python3 half2.py UIT.png [oy ox]
import sys; from PIL import Image; import numpy as np

def erode4(m):
    p=np.pad(m,1); return m&p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]
def ncomp8(win):
    seen=np.zeros_like(win); n=0
    for y,x in zip(*np.where(win)):
        if seen[y,x]: continue
        n+=1; st=[(y,x)]; seen[y,x]=True
        while st:
            cy,cx=st.pop()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=cy+dy,cx+dx
                    if 0<=yy<win.shape[0] and 0<=xx<win.shape[1] and win[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
    return n
UIT=sys.argv[1]; OY=int(sys.argv[2]) if len(sys.argv)>2 else 0; OX=int(sys.argv[3]) if len(sys.argv)>3 else 0
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); H,W=a.shape[:2]
PAL=[(255,0,255),(14,13,22),(49,48,61),(71,68,87),(89,88,103),(115,111,132),(130,126,150),(142,139,158),(161,158,174),(180,179,191),(209,206,219)]
P=np.array(PAL[1:],float)
bg=a.min(axis=2)>=215
lab=((a[:,:,None,:]-P[None,None])**2).sum(3).argmin(2)+1; lab[bg]=0
drk=lab==1
h=(H-OY)//2; w=(W-OX)//2
def B(m): return m[OY:OY+2*h,OX:OX+2*w].reshape(h,2,w,2).sum((1,3))
nfig=B(~bg); ndk=B(drk)
fig=nfig>=2
rand=fig&~erode4(fig)
o=np.zeros((h,w),int)
# rand = omlijning alleen waar het model daar zwart heeft (in het blok of in de 1-px-ring eromheen);
# waar het model een gekleurde rand heeft (bovenkant staart) houdt het blok zijn modeltoon
dp=np.pad(drk,1)
ringdk=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        ringdk[j,i]=dp[OY+2*j:OY+2*j+4,OX+2*i:OX+2*i+4].sum()
dun=rand&(ringdk==0)
line=fig&((rand&~dun)|(ndk>=2))
# brugpixels
for it in range(3):
    add=[]
    for j in range(h):
        for i in range(w):
            if not fig[j,i] or line[j,i] or ndk[j,i]!=1: continue
            win=line[max(0,j-1):j+2,max(0,i-1):i+2].copy(); cj,ci=j-max(0,j-1),i-max(0,i-1)
            win[cj,ci]=False
            n=ncomp8(win)
            if n>=2:
                # alleen als de zwarte modelpixel echt aan beide stukken grenst in het model
                add.append((j,i))
    if not add: break
    for j,i in add: line[j,i]=True
for j in range(h):
    for i in range(w):
        if not fig[j,i]: continue
        if line[j,i]: o[j,i]=1; continue
        L=lab[OY+2*j:OY+2*j+2,OX+2*i:OX+2*i+2]; Lr=L.ravel(); Lr=Lr[Lr>1]
        if len(Lr)==0: o[j,i]=2; continue
        v,c=np.unique(Lr,return_counts=True); m=v[c==c.max()]
        o[j,i]=int(m[0]) if len(m)==1 else (int(L[0,0]) if L[0,0] in m else int(m.min()))
ys,xs=np.where(o>0); o2=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; hh,ww=o2.shape
full=np.zeros((64,64),int); x0=(64-ww)//2; full[64-hh:64,x0:x0+ww]=o2
p=Image.fromarray(full.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(UIT,transparency=0)
tot=(full>0).sum(); print(UIT,'%dx%d'%(ww,hh),'px',tot,'omlijning %.1f%%'%(100*(full==1).sum()/tot),'kleuren',len(set(full.ravel()))-1)
