# Palpaca r6: vanaf r5. Alleen de omtrek van de romp ronder/wolliger (rug, bil, borst), met aansluitende schaduw/selout.
# Kop, nek, staart, poten, handschoenen en pootstand ongewijzigd (bewezen hieronder).
import numpy as np; from PIL import Image
R5=Image.open('../../r5/palpaca.png'); pal=R5.getpalette()[:48]; R5=np.array(R5)
a=R5.copy()
NIEUW={  # toegevoegde randpixels (waren transparant)
 (32,37):6,(33,37):6,          # rug: wolbultje 1 (bultje 2 = bestaand x35-36), dip op x34 -> bolle, golvende rug
 (45,42):1,(45,43):1,          # bil: ronde bolling achteraan, zwart (schaduwkant)
 (20,42):6,(20,43):6,          # borst: wolbultje links, zachte lijn (lichtkant)
}
KLEUR={  # bestaande pixels: aansluitende tinten/lijnen langs de nieuwe rand
 (32,38):2,(33,38):2,          # onder het rugbultje: hooglicht (was lijn 6)
 (44,42):5,(44,43):5,(43,42):4,(43,43):4,(42,42):4,(42,43):4,  # bil: oude rand x43 -> wol, sikkel 4 -> 5 naar de rand
 (44,44):1,(43,44):5,(42,44):4, # onderkant bil (rand x44 i.p.v. x43: alleen kleur, x44 was al transparant? zie assert)
 (43,45):6,(42,45):6,          # bil over de verre achterpoot: binnenlijn sluit aan op (41,46)(40,47) 6 en (39,48) 1
 (21,42):2,(21,43):3,(22,42):2,(22,43):2,  # borstbultje: oude lijn x21 -> wol; borsthooglicht als ovaal tot in het bultje
 (41,42):3,(41,43):3,(40,44):3, # bilschaduw 2 px breed + rand 5 (geen brede band)
}
for p,v in NIEUW.items():
    x,y=p; assert R5[y,x]==0,('niet leeg',p); a[y,x]=v
for p,v in KLEUR.items():
    x,y=p
    if R5[y,x]==0: NIEUW[p]=v
    a[y,x]=v
# bevroren delen: alles buiten de romp-rand moet gelijk zijn aan r5
rompzone=set(NIEUW)|set(KLEUR)
diff=[(int(x),int(y)) for y,x in np.argwhere(a!=R5)]
assert all(p in rompzone for p in diff)
weg=[(int(x),int(y)) for y,x in np.argwhere((R5>0)&(a==0))]
erbij=sorted((int(x),int(y)) for y,x in np.argwhere((R5==0)&(a>0)))
im=Image.fromarray(a,'P'); im.putpalette(pal); im.save('../palpaca.png',transparency=0)
open('../normal.pal','w').write(open('../../r5/normal.pal').read())
print('kleuren',len(np.unique(a)),'anders dan r5',len(diff),'randpixels erbij',erbij,'weg',weg)
