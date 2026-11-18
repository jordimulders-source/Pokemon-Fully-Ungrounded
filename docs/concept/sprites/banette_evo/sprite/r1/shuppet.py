# Shuppet-zones: eigen reductie (blauw + omlijning), silhouet, binnenlijnen (skelet), helderheid
import numpy as np; from scipy import ndimage as nd; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); L=a.sum(2)/3
C=np.load('fijnC.npy'); dr=np.load('draden_mask.npy'); sk=np.load('skel.npy')
S=968/62
ZON={'L':(60,535,270,835),'R':(740,595,960,910)}
res={}
for z,(x0,y0,x1,y1) in ZON.items():
    m=np.zeros(C.shape,bool); sub=(C[y0:y1,x0:x1]==8)|(C[y0:y1,x0:x1]==1)|((C[y0:y1,x0:x1]==2))
    sub&=~dr[y0:y1,x0:x1]
    lab,n=nd.label(sub); szs=nd.sum(sub,lab,range(1,n+1)); k=1+np.argmax(szs)
    mm=nd.binary_fill_holes(nd.binary_closing(lab==k,structure=np.ones((5,5))))
    m[y0:y1,x0:x1]=mm
    blue=m&(C==8)
    cov=np.zeros((64,64)); lum=np.zeros((64,64)); sc=np.zeros((64,64))
    for j in range(64):
      for i in range(64):
        xa,ya=int(round(24+(i-1)*S)),int(round(1+(j-4)*S)); xb,yb=int(round(24+i*S)),int(round(1+(j-3)*S))
        xa,ya=max(xa,0),max(ya,0)
        if xb<=xa or yb<=ya: continue
        cov[j,i]=m[ya:yb,xa:xb].mean()
        bb=blue[ya:yb,xa:xb]
        if bb.sum(): lum[j,i]=L[ya:yb,xa:xb][bb].mean()
        sc[j,i]=(sk[ya:yb,xa:xb]&m[ya:yb,xa:xb]).sum()
    res[z]=(cov,lum,sc)
    sil=cov>=0.5
    print(z)
    for j in range(36,64):
        if sil[j].any(): print('%2d'%j,''.join(('#' if sc[j,i]>=0.6*S else str(min(9,int((lum[j,i]-80)/10)))) if sil[j,i] else '.' for i in range(0,64))[int(x0/S)-1:int(x1/S)+3])
np.save('shuppet.npy',np.array([res],dtype=object))
