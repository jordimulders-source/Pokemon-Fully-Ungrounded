# telling.py: afwijkingen van A0 t.o.v. de kale reductie (tussen/kaal.png), per zone en per soort ingreep
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r1/gereedschap')
from fv import *; import palet, pickle
from collections import Counter, defaultdict
kaal=np.asarray(Image.open(D+'sprite_r1/tussen/kaal.png')).astype(int); a0=np.asarray(Image.open(D+'sprite_r1/A0.png')).astype(int)
def zone(x,y):
    if y<=9: return 'poten (rij 0-9)'
    if y<=37: return 'vleugelpakket + buik (rij 10-37)'
    if y<=49 or (y<=51 and 23<=x<=30): return 'kop/gezicht (rij 38-51)'
    return 'oren (rij 50-63)'
d=np.argwhere(a0!=kaal); z=Counter(zone(x,y) for y,x in d)
print('totaal afwijkend van kaal:',len(d),'van',(a0>0).sum()|(kaal>0).sum()); [print(' ',k,v) for k,v in sorted(z.items())]
sil=np.argwhere((a0>0)!=(kaal>0)); print('silhouet anders dan kaal:',[(int(x),int(y)) for y,x in sil])
l1=pickle.load(open(D+'sprite_r1/tussen/log1.pkl','rb')); l2=pickle.load(open(D+'sprite_r1/tussen/log2.pkl','rb'))
print('handmatige reparaties (bouw1) per zone:',Counter(r[0] for r in l1))
print('automatische opschoning (bouw2):',Counter(r[0] for r in l2))
