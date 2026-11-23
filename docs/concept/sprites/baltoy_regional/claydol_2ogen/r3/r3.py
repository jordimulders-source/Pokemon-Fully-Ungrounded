# Ronde 3: alleen de rode lijn rechts van de top van boog 2 (zone rij 14-19, kol 40-50); rest = r2.
import sys, os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'../r2'))
from r2 import *
from PIL import ImageDraw
R2=maak(**KEUZE); ROOD=E[14,32]
def basis():
    S=R2.copy()
    # steen: samenhangend voorhoofdblok (3-ogenbasis rij 9-13, kol 22-31, rood-vrij) -> rij 15-19, kol 40-49
    for y in range(15,20):
        for x in range(40,50): S[y,x]=E[y-6,x-18]
    S[19,50]=E[18,51]                       # einde koprand (donker)
    for x in range(40,49):                  # rij 14: oude rode afdaling weg, steen van r2 erboven/ernaast laten
        if S[14,x]==9: S[14,x]=E[13,x-18]
    return S
def rood(S,cellen):
    for c in cellen: S[c]=ROOD
    return S
V={}
V['V1']=rood(basis(),[(14,x) for x in range(40,49)])
# V2: spiegelbeeld van het linkereinde (boog 1: 13,18 -> 14,16-17 -> 15,15-16 -> 16,15 -> 17,14 -> 18,13)
V['V2']=rood(basis(),[(14,x) for x in range(40,46)]+[(15,46),(15,47),(16,47),(16,48),(17,48),(18,49),(19,50)])
# V3: korte V-dip (linkerarm = bovenste 3 rijen van de oude afdaling), dan recht op tophoogte
V['V3']=rood(basis(),[(15,40),(15,41),(16,41),(16,42),(17,42),(17,43),(16,44),(16,45),(15,45),(15,46),(14,47),(14,48)])
LICHT=E[14,20]   # lichtrood onder de top van boog 1 (8)
def dik(S,cellen):
    for c in cellen: S[c]=LICHT
    return S
# dikke versies: zoals de top van boog 1 (donkerrood rij 13, lichtrood eronder, 2 kolommen ingesprongen)
V['V1d']=dik(V['V1'].copy(),[(15,x) for x in range(37,49)])
V['V2d']=dik(V['V2'].copy(),[(15,x) for x in range(37,46)])
V['V3d']=dik(V['V3'].copy(),[(15,47),(15,48)])
V['V4']=B.copy()
if __name__=='__main__':
    for n,S in V.items():
        assert ((S>0)==(E>0)).all()
        if n!='V4':
            z=np.zeros_like(S,bool); z[14:20,40:51]=True; z[15,36:40]=True
            assert not ((S!=R2)&~z).any()
        save(S,os.path.join(H,'claydol_2ogen_'+n)); print(n,'diff t.o.v. r2:',(S!=R2).sum())
    ims=[(n,rgba(V[n])) for n in ['V1','V1d','V2','V2d','V3','V3d','V4']]
    t={'V1d':'V1 dik','V2d':'V2 dik','V3d':'V3 dik','V1':'V1 recht op tophoogte','V2':'V2 recht + afzakkend einde','V3':'V3 korte V, dan recht','V4':'V4 = B (ronde 1)'}
    v=Image.new('RGBA',(7*530+10,16+512+12+16*12+12+80),(255,255,255,255)); d=ImageDraw.Draw(v)
    for i,(n,im) in enumerate(ims):
        x=10+i*530; d.text((x,3),t[n],fill='black')
        v.alpha_composite(im.resize((512,512),Image.NEAREST),(x,16))
        v.alpha_composite(im.crop((10,8,53,24)).resize((43*12,16*12),Image.NEAREST),(x,540))
        for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
            b=Image.new('RGBA',(80,80),bg); b.alpha_composite(im,(8,8)); v.alpha_composite(b,(x+j*90,540+192+12))
    v.save(os.path.join(H,'vel.png'))
