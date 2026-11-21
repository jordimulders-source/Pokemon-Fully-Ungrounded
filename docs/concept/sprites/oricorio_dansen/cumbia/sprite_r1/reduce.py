# (NIET GEBRUIKT: stemming gaf gebroken poten) Kale reductie: natief (klassen) -> 0,75x via oppervlakgewogen stemming per klasse. Niets getekend.
# Gebruik: python3 reduce.py [fy fx]  (fase van het 4->3 raster in natieve px)
import sys; from PIL import Image; import numpy as np
lab=np.load('km_lab.npy')
# k-means-cluster -> semantische modelklasse
KL={0:'O',1:'O',2:'O',3:'N',4:'N',5:'N',6:'B3',7:'M',8:'B3',9:'M',10:'K2',11:'M',12:'R',13:'B2',14:'L1',15:'G',16:'B1',17:'L2',18:'L2',19:'K1',20:'Y',21:'P'}
NAMEN=['_','O','B1','B2','B3','N','M','L1','L2','P','K1','K2','R','G','Y']
IDX={n:i for i,n in enumerate(NAMEN)}
cl=np.zeros(lab.shape,int)
for k,v in KL.items(): cl[lab==k]=IDX[v]
S=0.75; fy=float(sys.argv[1]) if len(sys.argv)>1 else 0; fx=float(sys.argv[2]) if len(sys.argv)>2 else 0
H,W=cl.shape; n=int(H*S)+2
out=np.zeros((n,n),int)
ACC=[IDX[c] for c in ('R','G','Y','K1','K2','P')]
for j in range(n):
    for i in range(n):
        y0,y1=fy+j/S,fy+(j+1)/S; x0,x1=fx+i/S,fx+(i+1)/S
        w=np.zeros(len(NAMEN))
        for yy in range(int(np.floor(y0)),int(np.ceil(y1))):
            for xx in range(int(np.floor(x0)),int(np.ceil(x1))):
                if not(0<=yy<H and 0<=xx<W): continue
                a=(min(y1,yy+1)-max(y0,yy))*(min(x1,xx+1)-max(x0,xx))
                if a>0: w[cl[yy,xx]]+=a
        if w.sum()==0: continue
        w/=w.sum()
        if w[0]>=0.5: continue
        if w[IDX['O']]>=0.42: out[j,i]=IDX['O']; continue
        w2=w.copy(); w2[0]=0; w2[IDX['O']]=0
        acc=max(ACC,key=lambda c:w2[c])
        if w2[acc]>=0.30: out[j,i]=acc; continue
        out[j,i]=int(w2.argmax())
np.save('kaal.npy',out)
ys,xs=np.where(out>0); print('bbox',xs.min(),xs.max(),ys.min(),ys.max(),xs.max()-xs.min()+1,ys.max()-ys.min()+1)
