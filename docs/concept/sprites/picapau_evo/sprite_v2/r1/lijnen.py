# Dunne zwarte modellijnen in de lucht (kuifslierten, staartkoord), overgenomen uit het 1024-model:
# middenlijn van de streek = middens van korte donkere runs (rij- en kolomscan, run <= 26 px; koord is ±20 px dik), elk middenpunt -> spritecel;
# daarna verdunning (Zhang-Suen) en L-hoekjes weg (pixel-perfect). Alleen in de lucht-zone (kaal <=1 en niet naast lijf).
import numpy as np; from PIL import Image
kaal=np.load('kaal.npy'); OY,OX=1,4; h,w=kaal.shape; S=15.36
a=np.asarray(Image.open('../../gemini/r9_prompt_v6.png').convert('RGB')).astype(int)
lum=a.mean(2); sat=a.max(2)-a.min(2); D=(lum<150)&(sat<40)
body=(kaal>1)
nb=body.copy(); nb[1:]|=body[:-1]; nb[:-1]|=body[1:]; nb[:,1:]|=body[:,:-1]; nb[:,:-1]|=body[:,1:]
zone=(kaal<=1)&~nb
pts=[]
def runs(v):
    r=[]; s=None
    for k,b in enumerate(v):
        if b and s is None: s=k
        if not b and s is not None: r.append((s,k-1)); s=None
    if s is not None: r.append((s,len(v)-1))
    return r
for y in range(1024):
    for s,e in runs(D[y]):
        if e-s<=26: pts.append(((s+e)/2,y))
for x in range(1024):
    for s,e in runs(D[:,x]):
        if e-s<=26: pts.append((x,(s+e)/2))
m=np.zeros((h,w),bool)
for x,y in pts:
    i=int((x-OX*5.12)//S); j=int((y-OY*5.12)//S)
    if 0<=i<w and 0<=j<h and zone[j,i]: m[j,i]=True
def zs(img):
    img=img.copy().astype(np.uint8); ch=True
    while ch:
        ch=False
        for step in (0,1):
            P=np.pad(img,1); rm=[]
            for y,x in zip(*np.where(img)):
                n=[P[y,x+1],P[y,x+2],P[y+1,x+2],P[y+2,x+2],P[y+2,x+1],P[y+2,x],P[y+1,x],P[y,x]]
                B=sum(n); A=sum((n[k]==0 and n[(k+1)%8]==1) for k in range(8))
                if 2<=B<=6 and A==1:
                    if step==0 and n[0]*n[2]*n[4]==0 and n[2]*n[4]*n[6]==0: rm.append((y,x))
                    if step==1 and n[0]*n[2]*n[6]==0 and n[0]*n[4]*n[6]==0: rm.append((y,x))
            for y,x in rm: img[y,x]=0; ch=True
    return img
L=zs(m)
# L-hoekjes: pixel met een 4-buur horizontaal en een 4-buur verticaal die elkaar diagonaal raken -> overbodig
ch=True
while ch:
    ch=False
    P=np.pad(L,1)
    for y,x in zip(*np.where(L)):
        N,S_,W,E=P[y,x+1],P[y+2,x+1],P[y+1,x],P[y+1,x+2]
        if sum(P[y:y+3,x:x+3].ravel())-1==2 and ((N and E) or (N and W) or (S_ and E) or (S_ and W)):
            L[y,x]=0; ch=True; P=np.pad(L,1)
np.save('_m.npy',m); np.save('lucht.npy',zone); np.save('lijn.npy',L)
print('zone',zone.sum(),'middenlijncellen',m.sum(),'lijn',L.sum())
