# Stap 3: naar 64 door rijen en kolommen te schrappen die het meest op hun buur lijken (Gengas-methode). Kop + kam + snavel +
# witte kraag = beschermde zone (rijen KY, kolommen KX): daar wordt niets geschrapt, dus de kop wordt relatief groter.
# Uiteinden (eerste/laatste 3 rijen/kolommen van de figuur) worden nooit geschrapt. Uit: kaal_lab.npy (64x64 labels, -1 leeg).
import numpy as np, sys
o=np.load('half_11.npy'); PAL=np.load('natief_pal.npy'); PAL=np.concatenate([PAL,np.zeros((72,3),int),PAL*0+[222,118,50],np.zeros((72,3),int),PAL*0+[166,48,63]])
ys,xs=np.where(o>=0); o=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; H,W=o.shape
KY=range(20-ys.min(),43-ys.min()); KX=range(18-xs.min(),36-xs.min())
rgb=np.where(o[...,None]>=0,PAL[np.maximum(o,0)],400)
def kies(A,n,verboden):
    cost=[np.abs(A[i]-A[i+1]).sum() for i in range(len(A)-1)]
    gek=[]
    for i in np.argsort(cost,kind='stable'):
        if i in verboden or i+1 in verboden or i<3 or i>len(A)-5: continue
        if all(abs(i-j)>=3 for j in gek): gek.append(int(i))
        if len(gek)==n: break
    return sorted(gek)
rows=kies(rgb,H-64,set(KY)) if H>64 else []
cols=kies(rgb.transpose(1,0,2),W-64,set(KX)) if W>64 else []
b=np.delete(np.delete(o,rows,0),cols,1)
print('figuur',W,'x',H,'-> geschrapt rijen',rows,'kolommen',cols,'(figuurcoord.) ->',b.shape)
out=np.full((64,64),-1); h,w=b.shape; x0=(64-w)//2; out[64-h:,x0:x0+w]=b
np.save('kaal_lab.npy',out)
open('schrap.txt','w').write('rijen %s\nkolommen %s\nbeschermd rijen %d-%d kolommen %d-%d (figuurcoord.)\n'%(rows,cols,KY[0],KY[-1],KX[0],KX[-1]))
from PIL import Image
img=np.full((64,64,3),255,'uint8'); img[out>=0]=PAL[out[out>=0]]
Image.fromarray(img).save('kaal.png'); Image.fromarray(img).resize((512,512),Image.NEAREST).save(sys.argv[1])
