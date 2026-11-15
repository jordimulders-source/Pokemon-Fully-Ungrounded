# Bewaakt c6: silhouet-diff 0 met p8; gezicht-rechthoek index-diff 0 met p8 en gezichtskleuren gelijk aan c5;
# lijfpatroon bevroren: elke groef van c5 (binnen-index 2 onder rij 32) is nog groef (2) of spleet (1);
# palet <=16; verschillen met c5 per soort (kop / buitenlijn / schaduwband / hooglichtrand / spleet).
import numpy as np
from PIL import Image
from basis import bevroren_kop
from rots import rand
p8=np.array(Image.open('../p8/welp_p8.png')); c5=np.array(Image.open('../c5/welp_c5.png'))
F=bevroren_kop(); R=rand(p8>0); pc5=Image.open('../c5/welp_c5.png').getpalette()[:48]
ok=True
for v in ('a','b','c'):
  for t in ('','_grijs'):
    I=Image.open(f'welp_c6_{v}{t}.png'); a=np.array(I); pa=I.getpalette()[:48]
    ref=Image.open('../c5/welp_c5'+t+'.png').getpalette()[:48]
    sil=int(((a>0)!=(p8>0)).sum()); kop=int((F&(a!=p8)).sum())
    kl=all(pa[3*k:3*k+3]==ref[3*k:3*k+3] for k in range(16)); n=len(np.unique(a))
    gr=(c5==2)&~R; gr[:32]=False; patroon=int((gr&~np.isin(a,[1,2])).sum())
    d=(a!=c5); dk=int(d[:32].sum()); db=d.copy(); db[:32]=False
    print(f'{v}{t}: silhouet {sil} | gezicht {kop} | palet = c5 {kl} | kleuren {n} | lijfgroeven weg {patroon} | diff kop {dk}, lijf {int(db.sum())} (buitenlijn {int((db&R).sum())}, binnen {int((db&~R).sum())})')
    ok&=sil==0 and kop==0 and kl and n<=16 and patroon==0
print('ALLES OK' if ok else 'FOUT')
