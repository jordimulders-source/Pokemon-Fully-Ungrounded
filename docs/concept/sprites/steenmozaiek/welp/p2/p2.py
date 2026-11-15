# p2: keuring p1 (MOET 1-4 + MAG rugstreep) op welp_p1_C, alleen binnen de patroonzones.
import numpy as np
from PIL import Image
C=np.array(Image.open('../p1/welp_p1_C.png')); R=np.array(Image.open('../r11/welp_r11.png')); B=np.load('../p1/basis.npy')
PAL=Image.open('../r11/welp_r11.png').getpalette()
MAG=np.isin(R,[3,4,5,14,6,7,8,11])           # bruinvulling of oud patroon in r11; lijnen 1/2 nooit
a=C.copy()
def zet(x,y,v):
    assert MAG[y,x], ('lijn/leeg', x,y); a[y,x]=v
# MOET 1: oog terug (fout uit basis.py), daarna y<30 gelijk aan r11
a[:30]=R[:30]
# MOET 4: lila schijf schouder: sikkel rechtsonder in 7; perzik 14 in de ring -> 9
for y in range(37,48):
    for x in range(25,37):
        if a[y,x]==8 and (x+y>=76 or (x>=34 and y>=40)): a[y,x]=7
for y in range(34,54):
    for x in range(22,38):
        if a[y,x]==14 and R[y,x]!=14: a[y,x]=9
# clusterscan: smalle 1-px lila strook rechtsonder tussen groef en ring wordt ring (crème schaduw 9)
for (x,y) in [(34,43),(34,44),(33,45),(32,46)]: zet(x,y,9)
# MOET 2: staart onder de ring = één haak (crème 11 links, 9 rechts), oude korrels terug naar bruin
for y in range(49,55):
    for x in range(26,36):
        if MAG[y,x] and a[y,x] in (6,7,8,9,11,14) and R[y,x]!=14: a[y,x]=B[y,x]
for (x,y,v) in [(30,49,11),(31,49,9),(30,50,11),(31,50,9),(30,51,11),(31,51,9),
                (28,52,11),(30,52,11),(31,52,9),(28,53,9),(29,53,9),(30,53,9)]: zet(x,y,v)
# MOET 3: heup opnieuw (x38-48, y46-56): basis terug, licht facet 5 (y47-48) blijft, groef = bruin 3
for y in range(46,57):
    for x in range(37,49):
        if MAG[y,x] and a[y,x] in (6,7,8,9,11,14): a[y,x]=B[y,x]
for y in range(49,56):
    for x in range(38,49):
        if MAG[y,x] and a[y,x]==2: a[y,x]=3
HEUP={ # crème spiraal: 2 px bovenste/linker winding (11), naar binnen 1 px (9 aan schaduwkant), tip (44,52)
 (42,49):11,(43,49):11,(44,49):11,(45,49):11,
 (41,50):11,(42,50):11,(43,50):11,(44,50):11,(45,50):11,(46,50):9,
 (41,51):11,(42,51):9,(46,51):9,
 (41,52):11,(42,52):9,(44,52):11,(46,52):9,
 (42,53):9,(44,53):9,(45,53):9,(46,53):9,
 # lila boog rechts en onder (8 op mid-bruin 4, 7 op donker 3, rand 6)
 (47,50):8,(47,51):8,(47,52):8,(48,51):7,(48,52):7,(47,53):7,
 (42,54):7,(43,54):7,(44,54):7,(45,54):7,(46,54):7,(47,54):6,
 (41,55):6,(42,55):6,(43,55):6,(44,55):6,(45,55):6,
 # lila streep linksboven (zoals het model), los van de spiraal
 (39,49):8,(40,49):8,(38,50):8,(39,50):7,(38,51):7 }
for (x,y),v in HEUP.items(): zet(x,y,v)
for (x,y) in [(43,51),(44,51),(45,51),(43,52),(45,52),(43,53)]:
    if MAG[y,x]: a[y,x]=3            # groef binnen de spiraal
# MAG: rugstreep strak: per rij links (onderrand) 7, rest 8; eindkrul 8 boven/links, 7 onder/rechts, groef 3
import sys; sys.path.insert(0,'../p1'); import os
_cwd=os.getcwd(); os.chdir('../p1'); from varC import RUG as RUGMAT; os.chdir(_cwd)
for (x,y),m in RUGMAT.items():
    if m in 'Lg' and MAG[y,x] and a[y,x] in (3,4,5,6,7,8): a[y,x]=B[y,x]
RUG={32:(32,33),33:(33,35),34:(34,36),35:(35,37),36:(36,38),37:(37,39)}
for y,(x0,x1) in RUG.items():
    for x in range(x0,x1+1):
        if MAG[y,x]: a[y,x]= 7 if (x==x0 and y>32) else 8
for (x,y,v) in [(38,38,8),(39,38,8),(40,38,8),(38,39,8),(39,39,3),(40,39,8),(41,39,7),
                (38,40,7),(39,40,8),(40,40,7),(39,41,7),(40,41,7)]:
    if MAG[y,x]: a[y,x]=v
im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PAL); im.save('welp_p2.png',transparency=0)
q=Image.open('welp_p2.png').convert('RGBA'); bg=Image.new('RGBA',q.size,(255,255,255,255)); bg.alpha_composite(q)
bg.resize((512,512),Image.NEAREST).save('welp_p2_8x.png')
