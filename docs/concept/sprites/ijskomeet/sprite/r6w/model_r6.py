# r6 onderlaag: ALLES uit het model. Per spritepixel het 3x3-blok natieve modelpixels:
#  - kleur = mediaan van de niet-lijnpixels -> dichtstbijzijnde paletkleur
#  - modellijn (natief lum<70) in een licht (ijs/gas) blok -> naad (lichtere naadtint S)
#  - modellijn in een paars blok -> spike-omlijning K
import sys; sys.path.insert(0,'r6w')
import numpy as np; from PIL import Image
from p6 import CH,PAL,to_txt,save
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); lum=n.mean(2)
m=np.load('mask_r1.npy'); ox,oy=11,-4
P=np.array(PAL,float); I={c:i for i,c in enumerate(CH)}
o=np.full((64,64),-1); kd=np.zeros((64,64),int); med=np.zeros((64,64,3))
LIGHT='WLMD'; CAND='WLMDabcdGerCg'
for j in range(64):
  for i in range(64):
    if not m[j,i]: continue
    y=3*j+oy; x=3*i+ox
    if y<0: o[j,i]=I['W']; continue
    px=n[y:y+3,x:x+3].reshape(-1,3); l=lum[y:y+3,x:x+3].ravel()
    kd[j,i]=(l<70).sum()
    keep=l>=40
    md=np.median(px[keep],0) if keep.sum()>=2 else np.median(px,0)
    med[j,i]=md
    c=CAND[int(np.argmin([((md-P[I[c]])**2).sum() for c in CAND]))]
    if keep.sum()<2 or ((l<40).sum()>=3 and c in 'abcdG'): c='K'
    o[j,i]=I[c]
np.save('r6w/kd.npy',kd); np.save('r6w/med.npy',med)
# naden: lijnpixels in lichte blokken
light=np.isin(o,[I[c] for c in LIGHT])
seam=light&(kd>=1)
# dun maken (L-hoek-pixels terug naar modelkleur)
s=seam.copy(); ch=True
while ch:
    ch=False
    for j in range(1,63):
        for i in range(1,63):
            if not s[j,i]: continue
            nb=[s[j-1,i],s[j,i+1],s[j+1,i],s[j,i-1]]
            if sum(nb)!=2 or (nb[0] and nb[2]) or (nb[1] and nb[3]): continue
            a=j-1 if nb[0] else j+1; b=i+1 if nb[1] else i-1
            if s[a,b]: continue
            # alleen weg als het minst-lijnige van de twee
            s[j,i]=False; ch=True
o[s]=I['S']
# donkere blokken (vrijwel geheel lijn) in paars gebied -> K
to_txt(o,'r6w/m6.txt'); save(o,'r6w/m6')
