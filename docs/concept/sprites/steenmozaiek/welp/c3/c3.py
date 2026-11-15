# c3: c2 + licht gegraveerd lijnenpatroon op de kop (kopgravure.py, Jordi: 'mogelijk cirkelend om de bovenkant van de ogen heen').
# c2 (basis welp_c1_A, keuring c1/keuring.md): kop als één gehouwen volume, lichtere steen, elke groef een kerf
# (donkere groef index 2 + lichte lip onder/rechts), 10-15 px hooglicht (index 14), borstbanden buigen mee, dijkrul rustiger.
# Tekens in stempels: g/i = groef, c = verhoogd hart (lip-tint), H = hooglicht (14), 3/4/5 = steentoon zetten, . = niets.
import sys, numpy as np
from PIL import Image
from basis import bevroren_kop
B0=np.load('basis_facet.npy'); P8=np.array(Image.open('../p8/welp_p8.png'))
import motieven, kop, kopgravure
VAR='A'
def opbouw():
    base=B0.copy(); lay=np.full((64,64),'.',dtype='<U1')
    for (x0,y0),txt in motieven.STEMPELS:
        for j,r in enumerate(txt.strip('\n').split('\n')):
            for i,ch in enumerate(r):
                if ch in ' .12': continue
                y,x=y0+j,x0+i
                if ch in '345': base[y,x]=int(ch)
                else: lay[y,x]=ch
    for (x,y) in kopgravure.LIJNEN[VAR]: lay[y,x]='k'
    for y,rij in kop.TONEN.items():           # kopvolume: (x0, tonen) per rij
        for x0,s in rij:
            for i,ch in enumerate(s):
                x=x0+i
                assert P8[y,x] in (3,4,5,6,7,8,9,11), ('geen vlakpixel',x,y,P8[y,x])
                if ch=='H': lay[y,x]='H'; base[y,x]=5
                else: base[y,x]=int(ch)
    return base,lay
LIP={3:5,4:5,5:14}          # lichte lip onder/rechts van elke groef
def kleur():
    base,lay=opbouw(); a=P8.copy()
    vlak=np.isin(P8,[3,4,5,6,7,8,9,11])&~bevroren_kop()
    a[vlak]=base[vlak]
    G=np.isin(lay,['g','i','k'])&vlak
    a[G]=2
    K=(lay=='k')&vlak
    a[K&(base==5)]=3            # kopgravure licht: op het lichte voorhoofd een groef in 3 i.p.v. 2
    for y,x in zip(*np.where(vlak&~G)):
        if lay[y,x]=='H': a[y,x]=14; continue
        if lay[y,x]=='c': a[y,x]=LIP[base[y,x]]; continue
        if (y>0 and G[y-1,x]) or (x>0 and G[y,x-1]): a[y,x]=LIP.get(base[y,x],base[y,x])
    return a
STEEN={  # 1 zwart, 2 selout/groef, 3 donker, 4 midden, 5 licht, 14 lip-op-licht/hooglicht. Index 6 = pupil (p8-kleur).
 'greige':{1:(30,24,26),2:(84,74,70),3:(126,114,104),4:(162,150,136),5:(196,186,168),14:(224,216,198)},
 'grijs': {1:(28,26,30),2:(78,76,78),3:(120,118,116),4:(156,152,146),5:(192,188,178),14:(222,218,208)},
}
def bewaar(steen,naam):
    a=kleur(); p=Image.open('../p8/welp_p8.png').getpalette()[:48]
    for k,rgb in STEEN[steen].items(): p[3*k:3*k+3]=list(rgb)
    im=Image.fromarray(a.astype(np.uint8),'P'); im.putpalette(p+[0]*(768-48)); im.save(naam+'.png',transparency=0)
    r=Image.open(naam+'.png').convert('RGBA'); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r)
    bg.resize((512,512),Image.NEAREST).save(naam+'_8x.png')
if __name__=='__main__':
    for v in 'AB':
        VAR=v; bewaar('greige','welp_c3_'+v); bewaar('grijs','welp_c3_'+v+'_grijs')
