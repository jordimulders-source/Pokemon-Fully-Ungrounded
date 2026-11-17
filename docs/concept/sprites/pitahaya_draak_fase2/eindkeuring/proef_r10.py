# proef_r10.py: toets van de keurder op r10 (geen oplevering). Bek: verre lipband naar de modelbreedte (2 px p, daarachter r) en
# mondhoek dicht met r (model (19,43) r); keel: d-plak rij 48 terug naar r (blokmodeltoon r). -> proef_r10.png
import numpy as np; from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
src=Image.open(B+'sprite_r10/pitahaya2_r10.png'); a=np.array(src).astype(int); o=a.copy()
N='.KdrpPgGhHwWsv'; I={c:i for i,c in enumerate(N)}
def zet(l,doel,oud):
    for x,y in l: assert N[o[y,x]] in oud,(x,y,N[o[y,x]]); o[y,x]=I[doel]
zet([(19,43)],'r','p')
zet([(19,48),(18,49),(19,49),(17,50),(18,50),(19,50),(16,51),(17,51)],'r','p')
zet([(24,48),(25,48),(26,48),(27,48),(26,49)],'r','d')
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(src.getpalette()); im.save('proef_r10.png',transparency=0)
print('diff',(o!=a).sum())
