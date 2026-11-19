# Kale 3x-reductie van de klassenkaart (geen tekenen): per 3x3-blok groep = meerderheid, zwart wint bij >=3 px,
# toon = meerderheid binnen de groep. Uitvoer: kaal_OYOX.npy (codes zoals klassen.py, 0 = transparant)
import sys; import numpy as np
K=np.load('klassen.npy'); K=np.where(K==15,-1,K)   # 15 = AA-randpixel: halve achtergrond
OY,OX=int(sys.argv[1]),int(sys.argv[2])
GRP={1:'z',2:'g',3:'g',4:'g',5:'w',6:'w',7:'s',8:'s',9:'s',10:'r',11:'r',12:'v',13:'v',14:'c'}
H,W=K.shape; h=(H-OY)//3; w=(W-OX)//3; o=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        b=K[OY+3*j:OY+3*j+3,OX+3*i:OX+3*i+3].ravel()
        nbg=(b==0).sum()+0.5*(b==-1).sum()
        if nbg>=4.5: continue
        f=[v for v in b if v>0]
        if not f: continue
        if (b==1).sum()>=3: o[j,i]=1; continue
        cnt={}
        for v in f:
            if v==1: continue
            cnt[GRP[v]]=cnt.get(GRP[v],0)+1
        if not cnt: o[j,i]=1; continue
        g=max(cnt,key=cnt.get)
        if (b==1).sum()>cnt[g]: o[j,i]=1; continue
        tv=[v for v in f if v!=1 and GRP[v]==g]
        o[j,i]=max(set(tv),key=tv.count)
np.save('kaal_%d%d.npy'%(OY,OX),o)
