# Cuyby ronde 5: C6 linker voetkussen 1 px hoger. Basis: ../../ronde4/anim_front.png (goedgekeurd, leidend).
from fu import *
old,pal=load('cuyby/ronde4'); a=old.copy()
OUT={1,9,5,11}
# frame 1 (f=0) op y43-46, frame 2 (f=1) dezelfde wijziging 1 rij hoger (zoals ronde 3/4)
blok=['?11?',   # y43: bovenrand kussen (27,43) was al 1
      '1cd1',   # y44: kussen 1 hoger
      '4113',   # y45: kussen-onderrand; zijlobben lopen 1 px door (4 links, 3 midden)
      '1..1']   # y46: onderrand lobben, inkeping onder het kussen
n=0
for f,dy in ((0,0),(1,-1)):
    assert ''.join('%x'%old[64*f+45+dy,x] for x in range(25,29))=='1cd1'
    n+=put(a,f,25,43+dy,blok)
zones=[(0,25,43,28,46),(1,25,42,28,45)]
r,outside=report(old,a,zones,OUT); print('\n'.join(r)); assert outside==0
save(a,pal,'cuyby/ronde4','cuyby/ronde5')
