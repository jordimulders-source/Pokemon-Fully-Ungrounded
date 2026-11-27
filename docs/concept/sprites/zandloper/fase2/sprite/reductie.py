# Kale reductie: model (1024) -> raster met pitch T, stemming per cel met voorrang voor lijnklassen.
import sys, json; import numpy as np; from gemeen import *
T=float(sys.argv[1]) if len(sys.argv)>1 else 10.24/0.70
OUT=sys.argv[2] if len(sys.argv)>2 else 'kaal.png'
rgb=model(); k,bg=klassen_model(rgb)
yy,xx=np.where(~bg); x0,x1,y0,y1=xx.min(),xx.max(),yy.min(),yy.max()
W=int(np.ceil((x1-x0+1)/T)); H=int(np.ceil((y1-y0+1)/T))
cx=(x0+x1)/2-W*T/2; cy=(y0+y1)/2-H*T/2
out=np.zeros((H,W),int)
LIJN=[1,2,7]
for j in range(H):
    for i in range(W):
        a=k[int(round(cy+j*T)):int(round(cy+(j+1)*T)), int(round(cx+i*T)):int(round(cx+(i+1)*T))].ravel()
        h=np.bincount(a,minlength=16)/len(a)
        if h[0]>0.5: continue
        hl=h.copy(); hl[0]=0
        lijn=max(LIJN,key=lambda c:h[c])
        if h[1]>=0.3 or h[lijn]>=0.3: out[j,i]=lijn if h[lijn]>=h[1]*0.6 or lijn==1 else 1
        else: out[j,i]=hl.argmax()
print(W,H,'gevuld',(out>0).sum())
# in 64x64 zetten, onderaan gecentreerd
S=np.zeros((64,64),int); ox=(64-W)//2; oy=59-H
S[oy:oy+H,ox:ox+W]=out
json.dump(dict(T=T,cx=float(cx),cy=float(cy),ox=ox,oy=oy),open('geo.json','w'))
np.save(OUT.replace('.png','.npy'),S); opslaan(S,OUT)
