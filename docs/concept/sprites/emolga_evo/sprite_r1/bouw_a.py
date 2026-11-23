# Sprite A r1: A0 met alleen de kop 1,4x (op modelniveau; kop.py), zelfde verkleining (oppervlak-middeling), geplakt op A0.
# Kopzone = nieuwe kop + oude kop; daarbuiten pixeldiff 0 t.o.v. A0 (assert).
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo/gereedschap')
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo/sprite_r1')
from gemeen import *; from opschoon import *; from palet import *
import bouw_a0; from kop import kop_sprite
def dubbel_lijn(o,m):
    # 1,13x vergroting verdubbelt soms een 1-px modellijn (K naast K). Binnenste K (zonder transparante buur) die een
    # buitenste K-buur heeft en aan de andere kant vulkleur -> neemt die vulkleur aan. Alleen binnen masker m.
    n=o.copy(); log=[]
    for y_,x_ in zip(*np.where((o==1)&m)):
        if any(v==0 for v,_,_ in buren(o,y_,x_)): continue
        for dy,dx in N4:
            a=(y_+dy,x_+dx); b=(y_-dy,x_-dx)
            if not(0<=a[0]<64 and 0<=a[1]<64 and 0<=b[0]<64 and 0<=b[1]<64): continue
            if o[a]==1 and any(v==0 for v,_,_ in buren(o,*a)) and o[b] not in (0,1):
                n[y_,x_]=o[b]; log.append((x_,y_,1,o[b])); break
    return n,log
def bouw(fix_a0=None,fix_a=None,verslag=True):
    import gezicht_a0
    a0,_,_=bouw_a0.bouw(fix_a0 or gezicht_a0.FIX,verslag=False)
    kop,kop0,_,_=kop_sprite(bouw_a0.S,bouw_a0.OX,bouw_a0.OY)
    nieuw=kop>0; zone=nieuw|(kop0>0)
    o=a0.copy(); stappen={}
    o[nieuw]=kop[nieuw]
    # oude kop die buiten de nieuwe kop valt
    rest=zone&~nieuw; stappen['oude kop buiten nieuwe kop']=[(x,y,a0[y,x],0) for y,x in zip(*np.where(rest))]
    o[rest]=0
    k_kaal=o.copy()
    o,l=dubbel_lijn(o,zone); stappen['dubbele lijn']=l
    # naad: kopranden die aan lijf/vleugel grenzen krijgen de kopomlijning (zwart)
    l=[]
    for y_,x_ in zip(*np.where(nieuw)):
        if o[y_,x_]==1: continue
        if any(v not in (0,) and not nieuw[y_+dy,x_+dx] for v,dy,dx in buren(o,y_,x_) if 0<=y_+dy<64 and 0<=x_+dx<64):
            l.append((x_,y_,o[y_,x_],1))
    for x_,y_,v,nv in l: o[y_,x_]=nv
    stappen['naad']=l
    bes=~zone.copy()
    o,l=ontkorrel(o,bes|GEZ_A_mask()); stappen['ontkorrel']=l
    b,l=buitenlijn(o)
    l=[t for t in l if zone[t[1],t[0]]]
    for x_,y_,v,nv in l: o[y_,x_]=nv
    stappen['buitenlijn']=l
    b,l=streep_binnen(o,l); l=[t for t in l if zone[t[1],t[0]]]
    for x_,y_,v,nv in l: o[y_,x_]=nv
    stappen['lichtstreep 1 px naar binnen']=l
    if fix_a:
        l=[]
        for (x,y),v in fix_a.items():
            assert zone[y,x], ('fix buiten kopzone',x,y)
            if o[y,x]!=v: l.append((x,y,o[y,x],v)); o[y,x]=v
        stappen['gezicht']=l
    assert ((o!=a0)&~zone).sum()==0, 'diff buiten kopzone'
    if verslag:
        for k,l in stappen.items(): print(k,len(l))
        print('diff t.o.v. A0',(o!=a0).sum(),'waarvan buiten kopzone',((o!=a0)&~zone).sum(),'| kopzone px',zone.sum())
    return o,a0,zone,k_kaal,stappen
def GEZ_A_mask():
    m=np.zeros((64,64),bool); m[46:64,4:28]=True; return m
if __name__=='__main__':
    o,a0,zone,kk,st=bouw()
    rgb(o).resize((512,512),Image.NEAREST).save(SCR+'a_try.png')
    toon(o,y0=26,y1=64,x0=0,x1=34)
