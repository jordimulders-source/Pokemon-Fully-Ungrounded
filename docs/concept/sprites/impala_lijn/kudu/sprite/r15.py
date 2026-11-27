# r15 = rechte lijnen nalopen (Jordi 27 nov: "check alleen nog of al deze rechte lijnen nodig zijn", r15/jordi_rechte_lijnen.png).
# Per gemarkeerde lijn: modelmeting (model_A3, cel 16 px, x0=91, sprite-x = (mx-91)/16+6) + Gen 3-runs; knik alleen waar het
# model >= 0,2 px van de spritelijn afwijkt (impala-regel). Elke pixel: (x,y): oud -> nieuw, met assert. Zie r15/NOTITIES.md.
import numpy as np
from PIL import Image
im=Image.open('r14/kudu_r14.png'); idx=np.array(im); g=np.load('r14/grid.npy').copy()
L2I={}
for y in range(64):
    for x in range(64): L2I.setdefault(g[y,x],idx[y,x])
assert L2I['.']==0
W={  # lijn -> lijst (x,y,oud,nieuw)
 1:[(30,6,'3','0')]+[p for y in (7,8,9) for p in ((30,y,'0','.'),(29,y,'3','0'))],
 3:[(27,15,'0','K'),(28,15,'.','K'),(27,16,'K','R'),(28,16,'K','R')],
 4:[(10,22,'0','r'),(10,23,'.','0')],
 5:[(14,27,'M','D'),(14,28,'D','M')],
 7:[(18,34,'K','l'),(19,34,'M','K')],
 8:[(44,31,'D','.'),(45,31,'D','.'),(46,31,'D','.'),(44,32,'L','D'),(45,32,'L','D'),(46,32,'W','D')],
 9:[(36,34,'M','W'),(37,34,'W','M'),(36,42,'M','W'),(37,42,'W','M'),(36,43,'D','W'),(37,43,'W','M')],
 10:[(43,34,'M','W'),(44,34,'W','M'),(43,41,'M','W'),(44,41,'W','M'),(43,42,'M','W'),(44,42,'W','M')],
 11:[(53,44,'.','0'),(52,44,'0','M'),(53,47,'.','0'),(52,47,'0','M')],
 12:[(43,43,'M','D')],
 13:[p for y in (57,58,59) for p in ((55,y,'.','0'),(54,y,'0','M'))],
 14:[p for y in (50,51) for p in ((22,y,'.','K'),(23,y,'K','D'))],
 15:[p for y in (51,52,53) for p in ((33,y,'.','0'),(32,y,'0','M'))],
}
g0=g.copy()
for n,lst in W.items():
    for x,y,o,nw in lst:
        assert g0[y,x]==o,(n,x,y,g0[y,x],o); g[y,x]=nw; idx[y,x]=L2I[nw]
out=Image.fromarray(idx,'P'); out.putpalette(im.getpalette()); out.save('r15/kudu_r15.png',transparency=0)
out.convert('RGBA').resize((512,512),Image.NEAREST).save('r15/kudu_r15_8x.png')
np.save('r15/grid.npy',g)
with open('r15/pixels.txt','w') as f:
    for n,lst in W.items():
        for x,y,o,nw in lst: f.write(f'lijn {n}: ({x},{y}) {o} -> {nw}\n')
oog=(slice(21,25),slice(15,20))
print('oog K4 diff',(g0[oog]!=g[oog]).sum(),'| silhouet diff',((g0=='.')!=(g=='.')).sum(),'| px totaal',(g0!=g).sum())
