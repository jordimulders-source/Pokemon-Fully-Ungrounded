# Ronde 2: opnieuw uit het model (natief, gegumd, zelfde schaal/indrukking als r1 B) met andere lijnregels per zone,
# daarna bevroren zones (gezicht/geest/vuist/wielen) letterlijk uit r1. Niets getekend.
import sys; from PIL import Image; import numpy as np; from comp import label
TH=float(sys.argv[1]) if len(sys.argv)>1 else 0.75   # vanaf deze lijndekking zwart (dikke modellijn)
TW=float(sys.argv[2]) if len(sys.argv)>2 else 0.35
WF=sys.argv[3] if len(sys.argv)>3 else 'mode'   # vanaf deze dekking een dunne modellijn als donkere houttint
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int).copy()
fg=a.min(2)<225; lab,n=label(fg)
for k in range(1,n+1):
    m=lab==k; c=a[m].mean(0)
    if m.sum()<200 and not (c[1]>c[0]+25): a[m]=255; fg[m]=False          # gummen (zoals r1)
H=lambda s:int(s,16)
PAL=['#292018','#b5f3b6','#72d779','#67b370','#467e4b','#3f6036','#9cf08d','#a0846a','#725641','#3d3827','#8c6246','#aba09a','#7b7c7e','#4a443c']
P=np.array([[H(c[1:3]),H(c[3:5]),H(c[5:7])] for c in PAL],float); LUM=P@[0.3,0.59,0.11]
GROUP={1:'O',2:'G',3:'G',4:'G',5:'G',6:'G',7:'N',8:'W',9:'W',10:'W',11:'W',12:'S',13:'S',14:'S'}
CEN={'#1e1b10':1,'#271f16':1,'#3d3827':10,'#4a443c':14,'#3f6036':6,'#437e45':5,'#725641':9,'#4e774f':5,
     '#8c6246':11,'#539555':4,'#589d5c':4,'#7b7c7e':13,'#67ac66':4,'#a0846a':8,'#72c071':3,'#7cc777':3,
     '#aba09a':12,'#8cd585':3,'#9cf08d':7,'#b9f3b0':2}
CC=np.array([[H(k[1:3]),H(k[3:5]),H(k[5:7])] for k in CEN],float); CI=np.array(list(CEN.values()))
cls=CI[((a[...,None,:]-CC[None,None])**2).sum(-1).argmin(-1)]; cls[~fg]=0
s,X0,Y0,oy,XC,k=[float(v) for v in open('r1.meta').read().split()]
def inv(u): return np.where(u<XC-X0, X0+u, XC+(u-(XC-X0))/k)
SS=8; out=np.zeros((64,64),int); BLK={}; ZONE=np.zeros((64,64),'<U1')
for j in range(64):
    for i in range(64):
        us=(i+(np.arange(SS)+0.5)/SS)/s; vs=Y0+(j-oy+(np.arange(SS)+0.5)/SS)/s
        xx=np.clip(inv(us).astype(int),0,198); yy=np.clip(vs.astype(int),0,198)
        c=cls[np.ix_(yy,xx)].ravel(); cov=(c>0).mean()
        cc=c[c>0]
        if len(cc)==0: continue
        g=np.array([GROUP[v] for v in cc]); gs,gc=np.unique(g[cc!=1],return_counts=True) if (cc!=1).any() else (np.array(['O']),np.array([1]))
        G=gs[gc.argmax()]; ZONE[j,i]=G
        thr=0.35 if G=='G' and j>=23 else 0.5          # staart/wolk: zachte uitlopers houden
        if cov<thr: continue
        BLK[(j,i)]=cc
        L1=(cc==1).mean()
        sel=cc[g==G]; u,uc=np.unique(sel,return_counts=True); fill=u[uc.argmax()] if len(u) else 1
        if G in 'WS':                                    # wagon: dunne lijnen zachter
            if WF=='avg' and G=='W':                     # vlakgemiddelde van het hout -> dichtstbijzijnde houtkleur
                w=cc[np.isin(cc,[8,9,10,11,14,1])]; rgb=P[w-1].mean(0)
                fill=[8,9,10][int(np.argmin(((P[[7,8,9]]-rgb)**2).sum(1)))]   # roest niet uit een gemiddelde
                if (cc==11).mean()>=0.4: fill=11                                # roest alleen waar het model hem echt heeft
            if L1>=TH: out[j,i]=1
            elif (cc==14).mean()>=0.4: out[j,i]=14       # stalen band van het model
            elif L1>=TW: out[j,i]=9 if fill==8 else 10   # in licht hout: #725641, anders #3d3827
            else: out[j,i]=fill
            continue
        if G=='N' or (cc==7).mean()>=0.25: out[j,i]=7; continue
        if G=='G':
            if L1>=0.4:
                rr=a[np.ix_(yy,xx)].reshape(-1,3)[c==1].mean(0); out[j,i]=5 if rr[1]-rr[0]>12 else 1; continue
            if j>=23 and fill==3 and np.isin(cc,[4,5,6]).mean()>=0.35:   # draaikolk/strepen: donkere modelstreep wint
                v=cc[np.isin(cc,[4,5,6])]; u2,c2=np.unique(v,return_counts=True); out[j,i]=u2[c2.argmax()]; continue
            out[j,i]=fill; continue
        out[j,i]=fill
out[out==6]=5                                           # tintreductie zoals r1
np.save('kaal_r2.npy',out); np.save('cls.npy',cls); np.save('zone.npy',ZONE)
import pickle; pickle.dump(BLK,open('blk.pkl','wb'))
print('fg',(out>0).sum())
