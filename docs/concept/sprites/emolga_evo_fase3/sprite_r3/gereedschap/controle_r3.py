# controle_r3.py: diff r3 t.o.v. r2 moet precies de benoemde pixels van bouw_r3.py zijn (buiten de zones 0), plus tintvlakjes < 3 px.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r3/gereedschap')
from fv import *; import palet, bouw_r3 as b
for nm,extra in (('A0',b.A0_ONLY),('A',b.A_ONLY),('A_geel',b.A_ONLY)):
    r2=np.asarray(Image.open(b.R2+nm+'.png')).astype(int); im=Image.open(b.R3+nm+'.png'); r3=np.asarray(im).astype(int)
    assert im.size==(64,64) and im.mode=='P'
    zones={**b.ALLE,**extra}; benoemd={p:z for z,px in zones.items() for p in px}
    diff={(x,y) for y,x in zip(*np.where(r2!=r3))}
    buiten=diff-set(benoemd)
    per={}
    for p in diff: per[benoemd[p][:1]]=per.get(benoemd[p][:1],0)+1
    print(nm,'diff',len(diff),'buiten zones',len(buiten),'per zone',dict(sorted(per.items())),'kleuren',len(set(r3.flatten())))
    assert not buiten
    for t in 'DEGWB':
        m=r3==b.I[t]; lab,n=label(m,acht=False)
        k=[(int(np.where(lab==i)[1][0]),int(np.where(lab==i)[0][0])) for i in range(1,n+1) if (lab==i).sum()<3]
        if k: print('  ',t,'vlakjes <3 px:',k)
