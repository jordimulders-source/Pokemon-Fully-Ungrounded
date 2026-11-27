# Uku Pacha r2 stap 2b: vlakken opnieuw bepalen met het oppervlak-gewogen GEMIDDELDE modelkleur
# per spritepixel (lijncellen, achtergrond en accenten niet meegeteld) -> dichtstbijzijnde
# vlaktoon. Minder ruis dan meerderheid; tintgrenzen blijven op de modelplek. Ghost-masker apart.
import numpy as np, geom
cls=np.load('cls.npy'); N=geom.N
M=np.load('M2.npy')
VLAK=[6,8,9,11,12,13,14,15,10,7]
P=np.load('nat_pal.npy')
# vlaktinten opnieuw meten als mediaan van de echte modelcellen (k-means centra bevatten wit)
PAL={}
for k in range(16):
    m=cls==k
    if m.any(): PAL[k]=np.median(N[m],axis=0)
GHOSTN=np.isin(cls,[13,14,15])&(np.arange(100)[None,:]>=72)
GH=np.zeros((64,64),bool)
for j in range(64):
  for i in range(64):
    if M[j,i]<0: continue
    x0,x1,y0,y1=geom.s2n(i,j); s=np.zeros(3); a_t=0; g=0; tot=0
    for cy in range(max(0,int(y0)),min(100,int(np.ceil(y1)))):
      for cx in range(max(0,int(x0)),min(100,int(np.ceil(x1)))):
        a=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy))
        if a<=0 or cls[cy,cx]<0: continue
        tot+=a; g+=a*GHOSTN[cy,cx]
        if cls[cy,cx] in VLAK: s+=a*N[cy,cx]; a_t+=a
    if tot and g/tot>=0.5: GH[j,i]=True
    if M[j,i] in (0,2) or M[j,i]>=16 or a_t==0: continue
    c=s/a_t
    M[j,i]=min(VLAK,key=lambda k:((PAL[k]-c)**2).sum())
np.save('GH.npy',GH); np.save('M2b.npy',M)
np.save('PALmed.npy',np.array([PAL.get(k,[0,0,0]) for k in range(16)]))
for k in VLAK: print(k,PAL[k].round())
