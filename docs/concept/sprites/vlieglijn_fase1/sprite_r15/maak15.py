# r15 = r14 (A_L2 / B_L2) + rechteroog weer rond + aansluiting poten smoother
import sys; sys.path.insert(0,'sprite_r14')
from lib import *
def r15(b):
    # oog: omtrek van r13 terug (koepel rij 27, x18-21), maar als dunne rand:
    # direct onder de rand een glansboog (index 3) zodat de rand 1 px leest i.p.v. een zwart blok
    for x in (18,19,20,21): b[x,27]=1
    b[17,28]=1                        # rand sluit schuin aan op (16,28)
    for x in (18,19,20,21): b[x,28]=3
    b[10,28]=3; b[11,28]=3            # zelfde glans onder de rand van het linkeroog
    b[20,29]=2                        # uit-lampje onder de glans weg (anders klontje)
    # uit-lampjes niet tegen de buitenrand
    for p in ((16,29),(10,33)): b[p]=2
    # poten: geen hoekjes waar de kabel uit het lijf komt
    b[27,39]=2      # middenpoot links: rand loopt schuin (26,39)->(27,40)
    b[32,40]=2      # middenpoot rechts: lijf zakt door tot het grijze heupje
    b[39,40]=2      # achterpoot: kapje 2 px, linkerkant komt uit de schaduw
    b[49,46]=1      # onderrand achterlijf rechts dicht, trap 2-3-3
for v in 'A':
    im=Image.open('sprite_r14/vlieg_r14_%s_L2.png'%v); r15(im.load())
    n='sprite_r15/vlieg_r15_%s_L2'%v; im.save(n+'.png',transparency=0)
    onbg(im).resize((512,512),Image.NEAREST).save(n+'_8x.png')
im=Image.open('sprite_r15/vlieg_r15_A_L2.png')
zoom(im,(12,30,54,50),16).save(SP+'j15.png'); zoom(im,(6,20,26,40),12).save(SP+'o15.png')
