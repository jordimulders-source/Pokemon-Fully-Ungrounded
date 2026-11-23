# Sprite A0 r1: model 1-op-1, oppervlak-middeling 78 -> 63 rijen (s=63/78), dan alleen technisch opschonen + gezicht per pixel naar het model.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo/gereedschap')
from gemeen import *; from reduceer import reduceer; from opschoon import *; from palet import *
S=63/78; OY=1-7*S; OX=4-16*S      # natief y7 -> sprite y1 (vleugelpunt 1 px van de rand), natief x16 -> sprite x4
def kaal():
    a,c,L=klassen(); o,cov=reduceer(c,S,OX,OY,10); return o
GEZICHT=(slice(50,64),slice(6,24))   # y, x
# Reparaties buiten het gezicht (wat de reductie kapotmaakt), elk naar het model:
LIJF_FIX={(17,40):1,(15,42):1,   # linkeromlijning nabije oor (model K natief (34,54)-(29,61) doorlopend); reductie liet gaten
          (16,46):4,             # losse K in het oor (model: 1 losse K natief (31,63)) -> lichte oorrand G zoals de buren
          (15,43):4,             # 2x2 zwart blok waar oorlijn en rand samenkomen -> oorrand G (buur)
          (31,45):3,             # losse gele pixel (model-ruis, natief y op de naad vleugel/buik) -> vacht E (buren)
          (9,21):2}              # losse K (model-streepje natief (22,32)) in de vleugelband -> band D
def bouw(gezicht_fix=None,verslag=True):
    o=kaal(); k0=o.copy(); stappen={}
    bes=np.zeros(o.shape,bool); bes[GEZICHT]=True
    o,l=ontkorrel(o,bes); stappen['ontkorrel']=l
    o,l=buitenlijn(o); stappen['buitenlijn']=l
    o,l=streep_binnen(o,l); stappen['lichtstreep 1 px naar binnen']=l
    l=[]
    for (x,y),v in LIJF_FIX.items():
        if o[y,x]!=v: l.append((x,y,o[y,x],v)); o[y,x]=v
    stappen['lijf-reparaties']=l
    if gezicht_fix:
        l=[]
        for (x,y),v in gezicht_fix.items():
            if o[y,x]!=v: l.append((x,y,o[y,x],v)); o[y,x]=v
        stappen['gezicht']=l
    if verslag:
        for k,l in stappen.items(): print(k,len(l))
        print('diff t.o.v. kaal',(o!=k0).sum(),'silhouet-diff',((o>0)!=(k0>0)).sum())
    return o,k0,stappen
if __name__=='__main__':
    o,k0,st=bouw()
    opslaan(k0,'sprite_r1/kaal.png')
    rgb(o).resize((512,512),Image.NEAREST).save(SCR+'a0_try.png')
    print('los zwart',losse_zwart(o))
