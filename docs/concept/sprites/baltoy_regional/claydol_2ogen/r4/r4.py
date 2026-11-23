# Ronde 4: uitwerkingen van V2 (recht op tophoogte vanaf de top van boog 2, einde zakt mee met de kop). Alleen lijnzone.
import sys, os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'../r3'))
from r3 import basis, rood, dik, V as V3, R2, E, B, save, rgba, ROOD, LICHT
import numpy as np
from PIL import Image, ImageDraw
def lijn(rij14_tot, stappen, top_rij=14, start=40):
    return [(top_rij,x) for x in range(start,rij14_tot+1)]+stappen
U={}
U['V2']=V3['V2']
U['U1']=rood(basis(),lijn(42,[(15,43),(15,44),(15,45),(16,46),(16,47),(17,48),(17,49),(18,50),(19,50)]))
u2=rood(basis(),lijn(45,[(15,46),(15,47),(16,47),(16,48),(17,48),(18,49),(19,50),(17,51)]))
U['U2']=dik(u2,[(15,x) for x in range(38,44)])
U['U3']=rood(basis(),[(15,x) for x in range(40,45)]+[(16,45),(16,46),(16,47),(17,48),(17,49),(18,50),(19,50)])
U['U4']=dik(rood(basis(),lijn(42,[(15,43),(15,44),(15,45),(16,46),(16,47),(17,48),(17,49),(18,50),(19,50)])),[(15,x) for x in range(36,41)])
U['U5']=rood(basis(),lijn(41,[(15,42),(15,43),(15,44),(16,45),(16,46),(17,47),(17,48),(18,49),(19,50)]))
TXT={'V2':'V2 (ronde 3)','U1':'U1 eerder afdalen, 3-2-2-1-1, eind verticaal','U2':'U2 exact spiegel boog-1-eind + tinten',
     'U3':'U3 = U1, recht stuk 1 rij lager','U4':'U4 = U1 dik (tinten als top boog 1)','U5':'U5 nog eerder, 3-2-2-1-1, eind diagonaal'}
if __name__=='__main__':
    z=np.zeros((64,64),bool); z[14:20,36:52]=True
    for n,S in U.items():
        assert ((S>0)==(E>0)).all(); assert not ((S!=R2)&~z).any(), n
        if n!='V2': save(S,os.path.join(H,'claydol_2ogen_'+n))
        print(n,'diff t.o.v. r2:',(S!=R2).sum())
    v=Image.new('RGBA',(6*530+10,16+512+12+16*12+12+80),(255,255,255,255)); d=ImageDraw.Draw(v)
    for i,n in enumerate(U):
        im=rgba(U[n]); x=10+i*530; d.text((x,3),TXT[n],fill='black')
        v.alpha_composite(im.resize((512,512),Image.NEAREST),(x,16))
        v.alpha_composite(im.crop((10,8,53,24)).resize((43*12,16*12),Image.NEAREST),(x,540))
        for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
            b=Image.new('RGBA',(80,80),bg); b.alpha_composite(im,(8,8)); v.alpha_composite(b,(x+j*90,540+192+12))
    v.save(os.path.join(H,'vel.png'))
