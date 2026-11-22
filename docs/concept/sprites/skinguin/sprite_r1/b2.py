# Variant B2: verre poot + ski dichter naar de nabije ski, vooral OMLAAG. Alleen pixels uit A, niets getekend.
# Een rechte verschuiving omlaag kan niet: 1 px omlaag raakt al de opgebogen punt van de nabije ski (kolom 25-27),
# terwijl de tussenruimte bij de staart 5-6 px is. Daarom verschuift de ski in drie vaste stukken (2 naden van 1 px):
#   rasterkolom <= 28 (punt + voet): 1 px omlaag, 29-31: 2 px, 32-34: 3 px, >= 35 (staartpunt): 4 px; alles 1 px naar links (DX)
# Been: rij 41-43 (aansluiting dij) blijft, rij 43 wordt herhaald, rij 44-45 schuift 1 px omlaag -> been 1 px langer.
# Gebruik: python3 b2.py [grens1 grens2]
import sys, numpy as np; from PIL import Image
G1,G2,G3=29,32,35; DX=-1
# werk op 1 px brede marge links (= canvaskolom 0), zodat de punt 1 px naar links mag
A0=np.loadtxt('A.txt',dtype=int); m0=np.load('poot_masker.npy')
A=np.zeros((61,62),int); A[:,1:]=A0; m=np.zeros((61,62),bool); m[:,1:]=m0; H,W=A.shape
dy=lambda c: 1 if c-1<G1 else (2 if c-1<G2 else (3 if c-1<G3 else 4))   # c = kolom incl. marge, c-1 = rasterkolom
B2=A.copy(); B2[m]=0; far=np.zeros_like(m)
def zet(y,x,v):
    B2[y,x]=v; far[y,x]=True
for y,x in zip(*np.where(m)):
    dx=0 if y<=41 else DX                      # been vanaf rij 42 en de ski DX opzij (rij 41 sluit aan op de dij)
    if y<=43: zet(y,x+dx,A[y,x])
    if y==43: zet(44,x+dx,A[y,x])                 # herhaalde beenrij
    if y in (44,45): zet(y+1,x+dx,A[y,x])
    if y>=46: zet(y+dy(x),x+dx,A[y,x])
# naadreparaties (rij, kolom incl. marge), alleen lijnpixels op de naden, steeds naar het patroon van A:
NAAD=[(48,28,1,'rechterrand voet open na de naad -> zwarte lijn zoals A (47,28)'),
      (49,32,12,'bovenlijn staart: gat in de bruine lijn op de naad gedicht (bruin zoals de buren)'),
      (50,32,11,'daaronder: bruin -> geel schaduw (binnenkant staart, zoals (50,33))'),
      (52,29,1,'onderlijn ski doorgetrokken over naad 1 (was geel tussen zwart)'),
      (52,32,1,'onderlijn ski doorgetrokken over naad 2'),
      (53,29,0,'losse zwarte pixel onder naad 1 weg (onderlijn ligt op rij 52)'),
      (53,32,0,'losse zwarte pixel onder naad 2 weg')]
for y,x,v,w in NAAD: B2[y,x]=v; far[y,x]=v!=0
# naden: een kolom die verder zakt dan zijn linkerbuur laat bovenaan een gat in de lijn als de stap > 1 -> controle
rest=(A>0)&~m; near=rest.copy(); near[:44]=False
fy,fx=np.where(far&(np.arange(H)[:,None]>=44)); ny,nx=np.where(near)
vrij=np.maximum(np.abs(fy[:,None]-ny[None]),np.abs(fx[:,None]-nx[None])).min()-1
def gaten(F):
    g=[]
    for x in range(W):
        a=np.where(F[:,x])[0]; b=np.where(near[:,x])[0]
        if len(a) and len(b):
            bb=b[b>a.max()]
            if len(bb): g.append(int(bb.min()-a.max()-1))
    return g
mA=m.copy(); mA[:44]=False; fB=far.copy(); fB[:44]=False
gA,gB=gaten(mA),gaten(fB)
print('vrij (Chebyshev, px achtergrond ertussen):',vrij)
print('A  tussenruimte per kolom',gA,'gem %.1f max %d'%(np.mean(gA),max(gA)))
print('B2 tussenruimte per kolom',gB,'gem %.1f max %d'%(np.mean(gB),max(gB)))
d=np.argwhere(B2!=A); buiten=[(y,x) for y,x in d if not (m[y,x] or far[y,x])]
print('diff A-B2',len(d),'| buiten verre poot (oud+nieuw):',len(buiten))
np.savetxt('B2.txt',B2,fmt='%d'); np.save('b2_far.npy',far)   # 62 breed: kolom 0 = canvaskolom 0
