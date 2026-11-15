# Hauntflare v4: keurpunten v3 1-op-1, alleen herkleuren op de plek, vanaf ../sprite_v3/hauntflare_v3.png.
# Indexen: 1 zwart, 8 bol licht, A=10 donker vlamrood, B=11 kuifrood, C=12 oranje, D=13 geel, F=15, 5=bol-selout.
import json; from PIL import Image; import numpy as np
from scipy import ndimage as nd
D='docs/concept/sprites/hauntflare/'; S=D+'sprite_v4/'
im=Image.open(D+'sprite_v3/hauntflare_v3.png'); PALF=im.getpalette()[:48]; o3=np.array(im).astype(int); out=o3.copy()
G=np.load(D+'sprite_v2/groep.npy'); OP=o3>0
RAND=OP&nd.binary_dilation(~OP,[[0,1,0],[1,1,1],[0,1,0]])
LOG=[]
def zet(pts,v,punt):
    for x,y in pts:
        LOG.append(dict(punt=punt,x=x,y=y,oud=int(out[y,x]),nieuw=v)); out[y,x]=v
zet([(38,18),(39,19)],1,1); zet([(40,19),(41,20),(42,21),(43,22),(44,23)],11,1)
zet([(43,42),(42,43),(41,44)],1,2); zet([(40,44)],8,2)
zet([(12,33),(12,34)],1,3)
zet([(23,31),(26,31)],1,4)
zet([(52,16),(52,17),(51,18),(52,18),(50,19),(51,19),(50,20),(51,20),(48,21),(49,21),(50,21),(48,22),(49,22),(47,23),
     (47,44),(48,45),(48,46),(48,47),(48,48),(49,48),(41,52),(42,52),(43,52),(44,52),(51,52),(52,52),(53,53)],11,5)
zet([(32,33),(27,34),(28,34),(26,35),(27,35),(29,35),(31,35),(32,35)],10,6)
# 7: linkerhand: F -> C, 5 -> B; losse oranje stipjes -> B
lh=np.zeros((64,64),bool); lh[46:64,0:32]=True; lh&=(G==5)
zet([(int(x),int(y)) for y,x in zip(*np.where(lh&(out==15)))],12,7)
zet([(int(x),int(y)) for y,x in zip(*np.where(lh&(out==5)))],11,7)
zet([(19,51),(18,52),(17,53),(16,54),(15,55),(21,55),(24,55),(14,56),(20,56),(25,56),(19,57),(18,59)],11,7)
# 8: kluit: (47,24) ligt tussen kuifpunt en ringomlijning, geen omlijning -> kuifrood; de rest is omlijning
zet([(47,24)],11,8)
zet([(13,35),(14,36),(15,36),(14,37)],6,9)
zet([(14,41)],1,10); zet([(14,42)],4,10)
pim=Image.fromarray(out.astype('uint8'),'P'); pim.putpalette(PALF+[0]*(768-48)); pim.save(S+'hauntflare_v4.png',transparency=0)
P=np.array(PALF).reshape(-1,3); rgb=P[out].astype('uint8'); rgb[out==0]=255
Image.fromarray(rgb).resize((512,512),0).save(S+'hauntflare_v4_8x.png')
gew=set((d['x'],d['y']) for d in LOG); d=out!=o3
print('gelogd',len(LOG),'echt gewijzigd',int(d.sum()),'diff buiten de lijst',[(int(x),int(y)) for y,x in zip(*np.where(d)) if (x,y) not in gew])
print('ongewijzigd (stond al goed):',[(e['punt'],e['x'],e['y']) for e in LOG if e['oud']==e['nieuw']])
json.dump(LOG,open(S+'v4_log.json','w'))
