# r16: Jordi: "daar zijn de benen gewoon een normale vorm alsof ze getaped zijn, dus alleen binnen de lijnen zie je die golven"
# + "naar dat betekent dat je alleen de buitenste lijn hoeft te fixen".
# Basis r15. ALLEEN de buitenomtrek van beide benen: de inkepingen (r15 ringonderrijen) worden gelijk aan de omtrek van
# de bandrijen erboven/eronder -> gladde cilinder die in gelijke stappen buigt. Binnenkant = r15.
# De oude inkeping-omtrekpixels liggen nu binnen het been en zijn precies de uiteinden van de r15-bogen: ze blijven
# donkerrood 2 (binnenlijn raakt de omtrek).
from PIL import Image; import numpy as np
D='docs/concept/sprites/hitmonlee_regional/'
ek=Image.open(D+'eindkeuring/ek2.png'); e=np.array(ek)
r=np.array(Image.open(D+'sprite/r15/r15.png')).copy()
ZONE={}
def zet(y,x,v,why):
    if r[y,x]!=v: r[y,x]=v; ZONE[(y,x)]=why
def glad(naam,y,oud,nieuw):
    (oL,oR),(nL,nR)=oud,nieuw
    assert r[y,oL]==2 and r[y,oR]==1,(naam,y,r[y,oL],r[y,oR])
    zet(y,oR,2,naam+': oude inkeping rechts -> uiteinde binnenboog (2)')
    zet(y,nL,2,naam+': gladde omtrek links (selout)'); zet(y,nR,1,naam+': gladde omtrek rechts (zwart)')
# trapbeen: bandrijen r15 = 12-15 (42,48), 17-18 (41,47), 20-21 (40,46) -> inkepingen 13,16,19,22 gelijktrekken
glad('trapbeen',13,(43,47),(42,48)); glad('trapbeen',16,(42,46),(41,47))
glad('trapbeen',19,(42,46),(41,47)); glad('trapbeen',22,(41,45),(40,46))
# standbeen: 44-48 (51,56), 49-53 (52,57)
glad('standbeen',45,(52,55),(51,56)); glad('standbeen',48,(52,55),(51,56)); glad('standbeen',51,(53,56),(52,57))
# rechterrand standbeen sprong 57 -> 56 -> 57 bij rij 54 (bovenkant voet): rij 54 een pixel breder
zet(54,56,3,'standbeen: rechterrand rij 54 gelijk met rij 53/55 (was deuk)'); zet(54,57,1,'standbeen: rechterrand zwart')

np.save(D+'sprite/r16/idx.npy',r)
im=Image.fromarray(r.astype('uint8'),'P'); im.putpalette(ek.getpalette())
im.save(D+'sprite/r16/r16.png',transparency=0)
im.convert('RGBA').resize((512,512),0).save(D+'sprite/r16/r16_8x.png')
prev={}
for l in open(D+'sprite/r15/log.txt'):
    xy=l.split(')')[0][1:]; x,y=map(int,xy.split(',')); prev[(y,x)]=l.split('  ',1)[1].strip()
with open(D+'sprite/r16/log.txt','w') as f:
    n=0
    for y,x in zip(*np.where(r!=e)):
        f.write('(%d,%d) %d -> %d  %s\n'%(x,y,e[y,x],r[y,x],ZONE.get((y,x)) or ('r15: '+prev.get((y,x),'?')))); n+=1
r15=np.array(Image.open(D+'sprite/r15/r15.png'))
print(n,'px t.o.v. ek2; t.o.v. r15',(r!=r15).sum(),'silhouet t.o.v. ek2',((r>0)!=(e>0)).sum(),'kleuren',len(set(r.ravel())-{0}))
