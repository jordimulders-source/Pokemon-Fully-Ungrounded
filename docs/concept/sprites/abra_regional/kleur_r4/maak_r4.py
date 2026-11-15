# maak_r4.py: r3 + de 11 MOET-punten van KEURING_r3.md (letters: zie ../kleur_r3/maak_r3.py NAAM)
import sys; sys.path.insert(0,'../kleur_r2'); sys.path.insert(0,'../kleur_r3')
import numpy as np; from PIL import Image
from auto import NAAM,K,L,S,B,H
T=6; I=11; NAAM=dict(NAAM); NAAM[T]='T'; NAAM[I]='I'; CH={v:k for k,v in NAAM.items()}
src=Image.open('../kleur_r3/abra_r3.png'); a=np.array(src).astype(int)
MOET=[('1',[(22,31,'b'),(23,31,'b')]),
 ('2',[(36,42,'L'),(36,43,'L'),(35,44,'L'),(34,45,'L'),(33,46,'L'),(33,47,'L'),(32,48,'L'),(32,49,'L')]),
 ('3',[(x,y,'L') for x,y in [(31,50),(31,51),(33,51),(34,50),(32,52),(34,52),(35,53),(35,55),(34,48),(35,49)]]),
 ('4',[(34,27,'I')]),('5',[(44,32,'K'),(43,33,'K')]),('6',[(24,60,'b'),(25,60,'s')]),
 ('7',[(37,26,'K'),(38,26,'1')]),('8',[(21,19,'L'),(18,22,'L'),(19,24,'L')]),('9',[(11,49,'I')]),
 ('10',[(15,55,'K'),(16,55,'s')]),('11',[(34,17,'s'),(34,16,'b')])]
n=0
for nr,px in MOET:
    for x,y,c in px:
        v=CH[c]
        if a[y,x]!=v: a[y,x]=v; n+=1
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(src.getpalette()); out.save('abra_r4.png',transparency=0)
im=Image.open('abra_r4.png').convert('RGBA'); im.resize((512,512),Image.NEAREST).save('abra_r4_8x.png')
print('gewijzigd',n)
