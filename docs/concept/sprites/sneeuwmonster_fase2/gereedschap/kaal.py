# Kale reductie model -> 64x64 (oppervlakgewogen per klasse, tint uit modelhelderheid). Niets getekend.
# Gebruik (vanuit de map sneeuwmonster_fase2): python3 gereedschap/kaal.py UIT.png
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *; from klassen import klassen
LT2,LT3=0.28,0.15   # vachtlijnen: aandeel lijnpixels -> lijntint 2 of schaduwtint 3
GB=2.2   # gloed telt zwaarder: de scheuren zijn 1 cel (beschermde zone)
def reduceer():
    a,c,L=klassen(); H,W=c.shape; yy,xx=np.mgrid[0:H,0:W]
    X=np.floor((xx-MX0)/F).astype(int); Y=np.floor((yy-MY0)/F).astype(int)
    ok=(X>=0)&(X<64)&(Y>=0)&(Y<64); idx=(Y*64+X)[ok]; cc=c[ok]; LL=L[ok]; aa=a[ok]
    n=np.bincount(idx,minlength=4096).astype(float)
    w=np.stack([np.bincount(idx,(cc==k).astype(float),minlength=4096) for k in range(8)],1)/np.maximum(n,1)[:,None]
    def mean_of(mask,v): s=np.bincount(idx,v*mask,minlength=4096); m=np.bincount(idx,mask.astype(float),minlength=4096); return s/np.maximum(m,1)
    lijn=((cc==2)&(LL<130))|(cc==1)        # dunne vachtlijnen/mond (1 natieve cel) + zwart
    lf=np.bincount(idx,lijn.astype(float),minlength=4096)/np.maximum(n,1)
    Lsn=mean_of((cc==2)&~lijn,LL)          # vlaktoon sneeuw zonder de lijnen
    wd=np.bincount(idx,((cc==3)&(LL<100)).astype(float),minlength=4096); wm=np.bincount(idx,((cc==3)&(LL>=100)&(LL<138)).astype(float),minlength=4096)
    wl=np.bincount(idx,((cc==3)&(LL>=138)).astype(float),minlength=4096)
    Lho=mean_of((cc==3),LL); Lgr=mean_of(cc==4,LL); Ggl=mean_of(cc==6,aa[:,1].astype(float))
    o=np.zeros(4096,int)
    for i in range(4096):
        if n[i]==0 or w[i,0]>=0.5: continue
        st=w[i,5]+w[i,6]+w[i,7]
        if st>=0.4:
            gl=w[i,6]+w[i,7]
            if gl*GB>=max(w[i,5],w[i,1],w[i,2]): o[i]=15 if w[i,7]>=0.15 else (14 if Ggl[i]>105 else 13)
            elif w[i,1]>w[i,5]*1.3: o[i]=1
            elif w[i,2]>w[i,5]+w[i,1]+gl: o[i]=5
            else: o[i]=12
        elif w[i,4]>=0.3 and w[i,2]<0.5:     # band/ogen: dunne grijze strook gaat voor (beschermd)
            o[i]=1 if w[i,1]>=0.4 else (10 if Lgr[i]<128 else 11)
        elif w[i,3]>=max(w[i,2],w[i,4]) and w[i,3]>0.25:
            # hout: meerderheid van de drie modeltonen (geen gemiddelde -> geen modder); veel zwart = donker hout (duiglijn/rand)
            o[i]=7 if w[i,1]>=0.45 else 7+int(np.argmax([wd[i],wm[i],wl[i]]))
        elif w[i,1]>=0.45: o[i]=1
        elif lf[i]>=LT2: o[i]=2
        elif lf[i]>=LT3: o[i]=3
        else:
            l=Lsn[i]; o[i]=3 if l<160 else 4 if l<186 else 5 if l<222 else 6
    return o.reshape(64,64)
if __name__=='__main__':
    o=reduceer(); opslaan(o,sys.argv[1]); toon(o)
