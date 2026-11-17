import numpy as np; from view import png,zij
d=np.load('stap1.npz'); cov,lf,maj,lum=d['cov'],d['lf'],d['maj'],d['lum']
COV=0.45; LT=0.30
g=np.zeros((64,64),int)
sil=cov>=COV
for j in range(64):
  for i in range(64):
    if not sil[j,i]: continue
    m=maj[j,i]; l=lum[j,i]
    if lf[j,i]>=LT or m==0: g[j,i]=1; continue
    if m==2: g[j,i]=3 if l>=118 else 4
    elif m==3: g[j,i]=6 if l>=112 else 7
    elif m==4: g[j,i]=8
    elif m==5: g[j,i]=9
    elif m==6: g[j,i]=10 if l>=135 else (11 if l>=108 else 12)
    elif m==7: g[j,i]=13
np.save('b1.npy',g); png(g,'b1.png'); zij(g,'b1_zij.png')
