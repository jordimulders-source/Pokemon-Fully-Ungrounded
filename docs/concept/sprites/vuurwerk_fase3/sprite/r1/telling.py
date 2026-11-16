# Telt per zone hoeveel pixels per stap afwijken (t.o.v. de vorige stap) en in totaal t.o.v. de kale reductie (kaal.png).
import numpy as np; from PIL import Image
st=['kaal.png','kaal_dg.png','opgeschoond.png','stap_gezicht.png','stap_twinkel.png','sprite.png']
nm=['glitter weg (afw. 1)','opschonen (ruis + buitenlijn)','gezicht (oog/kaak)','twinkels','bovenlaag spikkels (afw. 1+2)']
A=[np.asarray(Image.open(f)).astype(int) for f in st]
Y,X=np.mgrid[:64,:64]
k=A[0]
zone={'kop':(X<25)&(Y<31)&(k>0),'pijl':(Y>=44)&(X<47)&(k>0),'staart/rood':(X>=40)&(Y<44)&(k>0)}
zone['lijf']=(k>0)&~zone['kop']&~zone['pijl']&~zone['staart/rood']
zone['buiten het silhouet']=k==0
print('%-32s'%'stap'+''.join('%14s'%z for z in zone))
for i,n in enumerate(nm):
    d=A[i]!=A[i+1]; print('%-32s'%n+''.join('%14d'%(d&m).sum() for m in zone.values()))
d=A[0]!=A[-1]; print('%-32s'%'TOTAAL t.o.v. kale reductie'+''.join('%14d'%(d&m).sum() for m in zone.values()))
s=A[-1]; print('kleuren gebruikt (incl. transparant):',len(np.unique(s)),sorted(np.unique(s).tolist()))
print('pixels in zone:',{z:int(m.sum()) for z,m in zone.items()})
