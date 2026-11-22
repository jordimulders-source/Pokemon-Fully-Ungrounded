# maak.py r11: drie varianten vanaf r10 voor Jordi's veer (kleine liggende veer rechtsboven, x42-50, y9-13)
# en het gat tussen die veer en de grote rechtopstaande veer (gat r10: (43,10) en (42,11)).
# A = r10; B = kleine veer neemt het gat (verder naar links); C = hybride, elke veer neemt de helft.
import numpy as np, json
from render import schrijf
r10=np.load('../sprite_r10/samba_r10.npy'); H='.123456789abcdef'
V={'A':[],
   'B':[(43,10,0,5),(42,11,0,5),(43,11,5,2)],                 # kleine veer: selout 5 schuift 1 px naar links, lichtrand 2 erachter
   'C':[(43,10,0,5),(42,11,0,1),(41,11,1,4)]}                 # kleine veer neemt (43,10); grote veer neemt (42,11): zwarte schaduwrand 1 px naar rechts, vulling 4 erachter
zone={(43,10),(42,11)}
log={}
for k,l in V.items():
    a=r10.copy()
    for x,y,o,n in l: assert a[y,x]==o,(k,x,y,a[y,x]); a[y,x]=n
    d=[(int(x),int(y)) for y,x in np.argwhere((a>0)!=(r10>0))]
    assert set(d)<=zone,(k,d)
    np.save('samba_%s.npy'%k,a); schrijf(a,'samba_%s.png'%k)
    log[k]={'herkleurd':int((a!=r10).sum()),'silhouet_px':d}
    print(k,log[k])
    for y in range(8,14): print('  %02d '%y+''.join(H[v] for v in a[y,36:52]))
json.dump(log,open('log_r11.json','w'),indent=1)
