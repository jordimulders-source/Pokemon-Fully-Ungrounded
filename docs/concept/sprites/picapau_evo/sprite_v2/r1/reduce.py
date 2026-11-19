# Kale 3x-reductie van de klassenkaart (geen tekenen): per 3x3-blok achtergrond bij >=5 bg, zwart bij >=2 zwart (1-px modellijnen blijven heel),
# anders meerderheidsgroep en daarbinnen meerderheidstoon. Uitvoer kaal.npy (64 breed)
import sys; import numpy as np
ZT=int(sys.argv[3]) if len(sys.argv)>3 else 2
K=np.load('klassen.npy'); OY,OX=int(sys.argv[1]) if len(sys.argv)>1 else 1,int(sys.argv[2]) if len(sys.argv)>2 else 4
GRP={1:'z',2:'b',3:'b',4:'b',5:'c',6:'c',7:'c',8:'r',9:'g',10:'g',11:'g',12:'y',13:'y',14:'w'}
H,W=K.shape; h=(H-OY)//3; w=min(64,(W-OX)//3); o=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        b=K[OY+3*j:OY+3*j+3,OX+3*i:OX+3*i+3].ravel()
        if (b==0).sum()>=5: continue
        if (b==1).sum()>=ZT: o[j,i]=1; continue
        cnt={}
        for v in b:
            if v>1: cnt[GRP[v]]=cnt.get(GRP[v],0)+1
        if not cnt: o[j,i]=1; continue
        g=max(cnt,key=cnt.get)
        if (b==1).sum()>cnt[g]: o[j,i]=1; continue
        tv=[v for v in b if v>1 and GRP[v]==g]
        o[j,i]=max(set(tv),key=tv.count)
np.save('kaal.npy',o); ys,xs=np.where(o>0); print(o.shape,'bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())
