# Capykart r17b = r17 + één fix: tanden wit i.p.v. blokgeel.
# Slot vrijgemaakt: bruin-midden (183,107,67) samen met bruin-schaduw (164,88,56): kleinste kleurafstand in het palet
# (CIE76 dE 7,9; volgende kandidaten bruin-hoog->licht dE 9,0, bruin-midden->licht 10,6, blauw licht->donker 12,4 maar dat kost
# het blauwe blok zijn tweede vlak). 158 px gaan van midden naar schaduw; de 531 schaduwpixels blijven exact.
# Tanden: de crème-pixels van de r15b-tanden (in r17 op geel gezet) -> wit; tandschaduw blijft hoepel-donker zoals in r17 (r15b blauwgrijs).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'sprite/r17'); from gemeen import PAL, opslaan
r17=np.asarray(Image.open('sprite/r17/capykart.png')).astype(int)
im=Image.open('sprite/r17/capykart.png'); P=[tuple(im.getpalette()[i*3:i*3+3]) for i in range(16)]
stap=np.load('sprite/r17/_stap.npy',allow_pickle=True)
WIT=(240,240,232)
o=r17.copy()
o[r17==4]=3                                   # bruin-midden -> bruin-schaduw
o[o>4]-=1                                     # indices schuiven 1 op (palet 15 kleuren)
P2=P[:4]+P[5:]
P2.append(WIT); iw=len(P2)-1                  # index 15 = wit
tand=(stap=='tanden (r15b)')&(r17==9)
o[tand]=iw
opslaan(o,'sprite/r17b/capykart.png',P2)
Image.open('sprite/r17b/capykart.png').convert('RGBA').resize((512,512),Image.NEAREST).save('sprite/r17b/capykart_8x.png')
np.save('sprite/r17b/_o.npy',o)
# diff-rapport t.o.v. r17 (in kleuren)
a=np.array([P[k] for k in r17.ravel()]).reshape(64,64,3); b=np.array([P2[k] for k in o.ravel()]).reshape(64,64,3)
d=(a!=b).any(2)
print('palet',len(P2),'kleuren incl. transp.; pixels met andere kleur dan r17:',int(d.sum()))
print('  bruin-midden -> bruin-schaduw:',int((r17==4).sum()))
print('  tanden geel -> wit:',int(tand.sum()),[(int(x),int(y)) for y,x in zip(*np.where(tand))])
print('  overig:',int(d.sum()-(r17==4).sum()-tand.sum()))
