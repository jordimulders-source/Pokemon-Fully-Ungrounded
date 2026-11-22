# mug r2 = mug_r1 + reparaties uit keuring_r1 (MOET 1-3, MAG 2). Variant B (oog) = A + 2 extra oogcellen.
import numpy as np
from txt import CH
r1=np.loadtxt('mug_r1.idx',dtype=int)
GEMEEN=[
 ('vleugel links rand',21,5,'k','lichtkant-selout zoals rest van de rand (was # tussen k)'),
 ('vleugel links rand',22,10,'k','idem'),('vleugel links rand',23,11,'k','idem'),('vleugel links rand',23,12,'k','idem'),
 ('gele knie',22,44,'#','omtrek: model heeft donkere lijn om het gewricht; was lucht (silhouet +1)'),
 ('gele knie',22,45,'#','idem (silhouet +1)'),
 ('borststuk',27,29,'p','losse P -> p: model 6/9 donker + lichtpaars, buurtint in de paarse band'),
]
OOG={'A':[('oog ver',16,24,'E','model 30% oog (e16+E14), antraciet 41: oogpunt rechtsonder geeft de \\')],
     'B':[('oog ver',16,24,'E','als A'),('oog ver',14,25,'k','model: oog 50% (E38 e12) / vizier 50%: linkeronderhoek weg, linkerkant loopt ook schuin'),
          ('oog ver',16,25,'E','model E33 / zwart 66: onderste oogpunt rechts, schuine band 15-16')]}
for v in 'AB':
    a=r1.copy(); rep=GEMEEN+OOG[v]
    for z,x,y,c,_ in rep: a[y,x]=CH.index(c)
    np.savetxt(f'mug_r2{v}.idx',a,fmt='%d')
    d=list(zip(*np.where(a!=r1)))
    with open(f'diff_r2{v}.txt','w') as f:
        for z,x,y,c,rd in rep: f.write(f'{z}: ({x},{y}) {CH[r1[y,x]]} -> {c}  {rd}\n')
        f.write(f'totaal {len(d)} px anders dan mug_r1; buiten deze lijst: {sum((x,y) not in {(p[1],p[2]) for p in rep} for y,x in d)}\n')
    print(v,len(d),'silhouet-diff',((a>0)!=(r1>0)).sum())
