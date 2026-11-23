# meet_schaduw.py: aandeel schaduwtint per groot vlak (binnenpixels: niet grenzend aan achtergrond, geen lijnkleur).
# niveau: L=lijn, S=schaduw, M=midden, H=licht/hooglicht. Schaduwaandeel = S/(S+M+H).
import numpy as np, sys; from PIL import Image
from scipy import ndimage as nd
D='/home/user/Pokemon-Fully-Ungrounded/'
REF={
 'gnomad':(D+'docs/concept/sprites/gnomad/af/gnomad.png',{'muts':{2:'L',3:'S',4:'M',5:'H'},'roze':{6:'L',7:'S',8:'M'},'blauw':{9:'L',10:'S',11:'M'},'snor':{12:'S',13:'H'}}),
 'welp':(D+'docs/concept/sprites/steenmozaiek/af/welp.png',{'steen':{2:'L',3:'S',4:'M',5:'H',14:'H',9:'H',10:'H'}}),
 'steenjaguar':(D+'docs/concept/sprites/steenmozaiek/af/steenjaguar.png',{'blauwsteen':{2:'L',6:'S',7:'M',8:'H'},'bruinsteen':{3:'L',9:'S',10:'M',11:'H'}}),
 'bloedmaan':(D+'docs/concept/sprites/lunatone_evo/af/bloedmaan.png',{'maan':{2:'S',3:'S',4:'M',5:'M',7:'H'}}),
 'regirock':(D+'graphics/pokemon/regirock/anim_front.png',{'grijs':{6:'L',8:'S',10:'M',9:'M',12:'H',7:'H'},'oranje':{2:'L',5:'S',3:'M',4:'H',11:'H'}}),
}
def meet(a,groups,mask=None):
    a=a[:64]; fig=a>0 if a[0,0]==0 else a!=a[0,0]
    rand=fig&nd.binary_dilation(~fig)
    out={}
    for g,m in groups.items():
        sel=np.isin(a,list(m))&~rand
        if mask is not None and g in mask: sel&=mask[g]
        n={k:0 for k in 'LSMH'}
        for i,l in m.items(): n[l]+=int((sel&(a==i)).sum())
        f=n['S']+n['M']+n['H']
        out[g]=(n, n['S']/f if f else 0)
    return out
def toon(naam,out):
    for g,(n,s) in out.items(): print(f'{naam:12s} {g:10s} S {n["S"]:4d} M {n["M"]:4d} H {n["H"]:4d}  schaduw {100*s:4.0f}%')
def gnome(pad):
    a=np.array(Image.open(pad)); z=np.load(D+'docs/concept/sprites/gnometrotter_rock/sprite/zone_af.npy')
    # onderdelen: muts=1, baard=2,3,4, lijf=6, armen/handen=7,8,9 (+neus 5 apart), riem=10, stok=11, broek=12, zolen=13,14
    G={'muts':({2:'L',3:'S',4:'M',5:'H'},z==1),'baard':({4:'L',5:'S',13:'M',14:'H'},np.isin(z,[2,3,4])),
       'lijf':({6:'L',7:'S',8:'M',15:'H'},z==6),'armen':({6:'L',7:'S',8:'M',15:'H'},np.isin(z,[7,8,9])),'neus':({6:'L',7:'S',8:'M',15:'H'},z==5),
       'riem':({2:'L',3:'S',4:'M',5:'H'},z==10),'stok':({2:'L',3:'S',4:'M',5:'H'},z==11),'broek':({9:'L',10:'S',11:'M',12:'H'},z==12),
       'zolen':({2:'L',3:'S',4:'M',5:'H'},np.isin(z,[13,14]))}
    return meet(a,{k:v[0] for k,v in G.items()},{k:v[1] for k,v in G.items()})
if __name__=='__main__':
    for k,(p,g) in REF.items(): toon(k,meet(np.array(Image.open(p)),g))
    for p in sys.argv[1:]: toon(p.split('/')[-2],gnome(p))
