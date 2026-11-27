# Eindkeuring Hanan Pacha: basis = sprite_r9/sprite_C.png (Jordi koos C). Alleen tintwissels op bestaande pixels;
# silhouet (index 0) en klauwzone X16-41/Y47-57 en kop/oog X13-27/Y16-31 blijven pixeldiff 0 (assert).
import numpy as np; from PIL import Image, ImageDraw; from scipy import ndimage as nd
src=Image.open('../sprite_r9/sprite_C.png'); r9=np.array(src).astype(int); o=r9.copy()
PAL=np.array(src.getpalette()[:48]).reshape(16,3)
GOUD={2,3,4,5}
tr=r9==0; n4=nd.binary_dilation(tr,[[0,1,0],[1,1,1],[0,1,0]])
VAST=np.zeros((64,64),bool); VAST[16:32,13:28]=True; VAST[47:58,16:42]=True
log={}
def zet(pts,k,reden):
    for x,y in pts:
        assert not VAST[y,x] and r9[y,x]!=0; o[y,x]=k
    log[reden]=log.get(reden,0)+len(pts)
# 1. zwart blokje van 3 px in het lijf (35,32)(34,33)(35,33): modellijn = 1 px diagonaal (voorrand rechtervleugel)
zet([(35,33)],3,'1 blokje: dubbele pixel -> vlaktint g')
zet([(35,32),(34,33),(35,31)],2,'1 blokje: lijn 1 px diagonaal in donkerste goud (35,31 was gat in de modellijn)')
# 2a. binnenlijnen zwart geheel in goud -> donkerste goud (outline base); buitenlijn blijft zwart
A=[]
for y,x in zip(*np.where((r9==1)&~n4&~VAST)):
    nb=set(int(r9[y+p,x+q]) for p in (-1,0,1) for q in (-1,0,1) if (p or q))-{1}
    if nb and nb<=GOUD and (x,y) not in [(35,32),(34,33),(35,33)]: A.append((int(x),int(y)))
zet(A,2,'2 binnenlijn zwart in goud -> donkerste goud')
# 2b. scheidingen tussen rode pennen (binnen) -> donkerste rood; uiteinde aan de buitenrand blijft zwart
zet([(7,24),(8,24),(8,25),(9,25),(10,25),(51,25),(52,25),(53,25),(55,25)],8,'2 pennenscheiding binnen -> donkerrood')
# 2c. lichte kleur (grijswit 6) op de buitenrand -> selout donkerste goud
zet([(44,11),(37,26),(34,29),(23,45)],2,'2 lichte buitenrand -> selout goud')
assert ((o==0)==(r9==0)).all() and not ((o!=r9)&VAST).any()
d=o!=r9; print('gewijzigd',int(d.sum()),log); print('silhouet diff',int(((o==0)!=(r9==0)).sum()))
im=Image.new('P',(64,64)); flat=[int(v) for v in PAL.ravel()]; im.putpalette(flat+[0]*(768-len(flat)))
im.putdata([int(v) for v in o.ravel()]); im.save('sprite.png',transparency=0); np.save('sprite.npy',o)
