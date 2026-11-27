# Klassen per natieve modelcel (alleen indelen van modelkleuren, niets tekenen).
# 0 bg | 1 K omlijning | 2 sneeuw | 3 hout | 4 band (grijs) | 5 steen donker | 6 gloed rood/oranje | 7 gloed geel | 8 hand/voet (blauwgrijs)
import os, numpy as np; from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
NAMEN=['bg','K','sneeuw','hout','band','steen','gloed','geel','hand']
def flood(mask,seeds):
    H,W=mask.shape; out=np.zeros_like(mask); st=[s for s in seeds if mask[s]]
    for s in st: out[s]=True
    while st:
        y,x=st.pop()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and mask[yy,xx] and not out[yy,xx]: out[yy,xx]=True; st.append((yy,xx))
    return out
def dil(m,r=1):
    o=m.copy()
    for dy in range(-r,r+1):
        for dx in range(-r,r+1): o|=np.roll(np.roll(m,dy,0),dx,1)
    return o
def ero(m,r=1): return ~dil(~m,r)
def label(mask):
    lab=np.zeros(mask.shape,int); n=0
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        n+=1; f=flood(mask&(lab==0),[(y,x)]); lab[f]=n
    return lab,n
def klassen():
    a=np.asarray(Image.open(os.path.join(D,'..','natief.png')).convert('RGB')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]; L=.299*r+.587*g+.114*b; H,W=L.shape
    bg=flood(a.min(2)>=238,[(0,0),(H-1,0),(0,W-1),(H-1,W-1)])
    c=np.full((H,W),2)
    global ZONE
    warm=(r-b>60)&(r>140)                       # gloed
    donkerwarm=(L<90)&(r>b+6)                    # steen
    # steenzones: componenten van gloed/donkerwarm, opgevuld en 1 cel verbreed (omlijning van de steen hoort erbij)
    kern=warm|donkerwarm; yy=np.arange(H)[:,None]
    hout=(r-b>35)&(r>70)&(yy<25)&~warm          # emmer (boven)
    kern&=~hout
    lab,n=label(dil(kern,1)); zone=np.zeros((H,W),bool)
    emmer=np.zeros((H,W),bool)
    for i in range(1,n+1):
        m=lab==i
        if np.where(m)[0].mean()<20: emmer|=m        # component bovenaan = de emmer, geen steen
        elif m.sum()>=12: zone|=m
    zone=~flood(~zone,[(0,0)])                   # gaten dicht
    emmer=(emmer|hout)&~bg
    band=(a.max(2)-a.min(2)<30)&(L>=45)&(L<140)&(yy<28)&~zone
    c[emmer&(r>b+6)]=3
    c[band]=4
    mid=(b-g<=19)&(L<180)&(L>=55)&~zone&~bg&(yy>=55)   # blauwgrijs (groener dan de sneeuwschaduw)
    hand=dil(ero(mid,1),1)&mid
    lab,n=label(hand)
    for i in range(1,n+1):
        if (lab==i).sum()<40: hand[lab==i]=False
    c[hand]=8
    c[(L<70)&~zone&~(emmer&(r>b+6))]=1
    c[zone&~warm&(L<125)]=5
    c[zone&~warm&(L>=125)&(b-g<=19)&(L<180)]=8   # licht binnen de steenzone = sneeuw of hand (blijft c=2 als sneeuw)
    c[zone&warm]=6; c[zone&warm&(g>165)]=7
    c[bg]=0; ZONE=zone
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen(); CH='.K-hbsgyH'
    for i,nm in enumerate(NAMEN):
        m=c==i; print(nm,m.sum(),a[m].mean(0).astype(int) if m.any() else '')
    ys,xs=np.where(c>0); print('bbox natief',xs.min(),xs.max(),ys.min(),ys.max())
    for y in range(ys.min(),ys.max()+1): print('%3d '%y+''.join(CH[v] for v in c[y,xs.min():xs.max()+1]))
