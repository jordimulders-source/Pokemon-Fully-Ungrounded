import numpy as np; from view import png,zij
d=np.load('stap1.npz'); cov,lf,maj,lum=d['cov'],d['lf'],d['maj'],d['lum']; cnt=np.load('skel_cnt.npy')
S=968/62; COV=0.45
sil=cov>=COV
g=np.zeros((64,64),int)
def fill(m,l):
    if m==2: return 3 if l>=118 else 4
    if m==3: return 6 if l>=112 else 7
    if m==4: return 8
    if m==5: return 9
    if m==6: return 10 if l>=135 else (11 if l>=108 else 12)
    if m==7: return 13
    return 1
for j in range(64):
  for i in range(64):
    if sil[j,i]: g[j,i]=fill(maj[j,i],lum[j,i])
g[(cnt>=0.5*S)&sil]=1
# buitenrand
P=np.pad(sil,1)
edge=sil&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
g[edge]=1
np.save('b2.npy',g); png(g,'b2.png'); zij(g,'b2_zij.png')
