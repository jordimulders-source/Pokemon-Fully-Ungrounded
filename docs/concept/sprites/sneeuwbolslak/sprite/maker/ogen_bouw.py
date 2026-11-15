import numpy as np, importlib.util
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/sneeuwbolslak/sprite/maker/'
s=importlib.util.spec_from_file_location('s',D+'ogen_spec.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
r2im=Image.open(D+'r2.png'); r2=np.array(r2im)
for naam,g in m.V.items():
    a=r2.copy()
    assert len(g)==6 and all(len(r)==14 for r in g),naam
    for j,row in enumerate(g):
        for i,c in enumerate(row):
            a[31+j,9+i]=0 if c=='.' else int(c,16)
    im=Image.fromarray(a,'P'); im.putpalette(r2im.getpalette()); im.save(D+'ogen_'+naam+'.png',transparency=0)
    d=a!=r2; ys,xs=np.nonzero(d)
    buiten=[(x,y) for y,x in zip(ys,xs) if not (31<=y<=36 and 9<=x<=22)]
    sil=int(((a>0)!=(r2>0)).sum())
    print(f'{naam}: gewijzigde px {int(d.sum())}, buiten oogzone {len(buiten)}, silhouet-diff {sil}, indices {sorted(int(v) for v in np.unique(a))}')
