# controle_r2.py: pixeldiff r2 t.o.v. r1 per zone (A0, A, A_geel); buiten de zones moet het 0 zijn. Plus clustertelling van de nieuwe tinten.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r2/gereedschap')
from fv import *; import palet
CH=palet.CH
def zone(x,y,kap):
    if 9<=y<=37: return 'vleugel'
    if 43<=y<=48 and 33<=x<=38: return 'wang'
    if kap and 48<=y<=51 and 21<=x<=31: return 'kap'
    return 'BUITEN'
tot={}
for n in ('A0','A','A_geel'):
    r1=np.asarray(Image.open(D+'sprite_r1/%s.png'%n)).astype(int); r2im=Image.open(D+'sprite_r2/%s.png'%n); r2=np.asarray(r2im).astype(int)
    assert r2im.size==(64,64) and r2im.mode=='P' and r2.max()<16
    d={}
    for y,x in zip(*np.where(r1!=r2)):
        z=zone(x,y,n!='A0'); d.setdefault(z,[]).append((x,y,CH[r1[y,x]],CH[r2[y,x]]))
    print(n,'kleuren',len(set(r2.flatten())),' '.join('%s=%d'%(k,len(v)) for k,v in d.items()))
    sil=((r1>0)!=(r2>0)); print('  silhouet anders:',[(x,y,CH[r1[y,x]],CH[r2[y,x]]) for y,x in zip(*np.where(sil))])
    assert 'BUITEN' not in d, d.get('BUITEN')
    if n=='A': 
        for k in ('wang','kap'): print('  ',k,d.get(k))
# tintvlakjes < 3 px (4-buren) van G en E in het vleugelpakket
o=np.asarray(Image.open(D+'sprite_r2/A0.png')).astype(int)
for t in 'GE':
    m=np.zeros_like(o,bool); m[9:38]=(o[9:38]==CH.index(t))
    lab,nl=label(m,acht=False)
    klein=[(int(np.where(lab==i)[1][0]),int(np.where(lab==i)[0][0]),int((lab==i).sum())) for i in range(1,nl+1) if (lab==i).sum()<3]
    print('vleugel',t,'vlakken',nl,'kleiner dan 3 px:',klein)
