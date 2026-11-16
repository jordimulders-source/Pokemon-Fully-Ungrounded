# Blobfish r5. A = r4 + (17,32) zwart -> lijnrood (KEURING r4, polijstpunt 2).
# B = A + lichtronde (KEURING r4 punt 1): alleen tinten; tint 4 -> helderheid ~70, tint 6+7 samen -> ~97, tint 9 -> ~122
# (lippen schuiven mee). Elke tint wordt met een factor geschaald (R:G:B-verhouding = hue/verzadiging van het model blijft).
# Indexkaart B = A behalve: 7 -> 6 (samenvoegen) en de losse tint-6-pixels in het tint-4-vlak -> 4 (lijst KEURING).
# Ribbel (26,36) (25,37) (24,38) blijft. Geen extra schaduwtint.
import numpy as np; from PIL import Image
R4=Image.open('r4.png'); r4=np.asarray(R4).astype(int); pal=R4.getpalette()[:3*14]
def opslaan(a,P,naam):
    p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(list(P)+[0]*(768-len(P))); p.save(naam,transparency=0)
A=r4.copy(); A[32,17]=2; opslaan(A,pal,'blobfish_r5A.png')
lum=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2]
P=np.array(pal,float).reshape(-1,3)
def schaal(c,doel): f=doel/lum(c); return np.clip(np.round(c*f),0,255)
n67=((A==6).sum(),(A==7).sum()); m67=(P[6]*n67[0]+P[7]*n67[1])/sum(n67)   # gewogen gemiddelde van 6 en 7 (zelfde hue-familie)
P[4]=schaal(P[4],70); P[6]=schaal(m67,97); P[7]=P[6]; P[9]=schaal(P[9],122)
B=A.copy(); B[B==7]=6
LOS=[(14,42),(16,44),(15,45),(32,43),(33,44),(26,48),(25,49),(39,29),(40,30),(39,31)]
for x,y in LOS: assert A[y,x]==6; B[y,x]=4
assert ((B>0)==(r4>0)).all()
d=(B!=A)&~((A==7)&(B==6)); assert set(zip(*np.where(d)))=={(y,x) for x,y in LOS}
opslaan(B,[int(v) for v in P.ravel()],'blobfish_r5B.png')
for i in (4,6,8,9,10,11): print(i,P[i].astype(int).tolist(),round(lum(P[i])))
print('A diff r4',int((A!=r4).sum()),' B diff A: samenvoegen 7->6',int(((A==7)).sum()),'+ losse 6->4',len(LOS),'kleuren B',len(set(B.ravel()))-1)
