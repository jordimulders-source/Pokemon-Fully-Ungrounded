# Guarana fase 2, r7: alleen de pupillen van de grote ogen (2x2). Jordi r6: "er is geen enkel oog dat echte driekwart kijkt",
# "laat in elk geval de grote ogen dat doen", "ja dus iets naar linksonder vanaf het midden".
# Groot oog (stempel r5): rij0 '..OOO..' rij1 '.OwWwK.' rij2 'OWWWWWK' rij3 'OWWWWWK' rij4 '.KWWWK.' rij5 '..KKK..'.
# Nieuwe pupil = 2x2 op kolom 2-3, rij 2-3: één stap naar links t.o.v. het midden (kolom 3), met wit links (kol 1), onder (rij 4),
# rechts (kol 4-5) en boven (rij 1). Oude pupilpixels -> oogwit volgens de stempel. Alles buiten de grote ogen: diff 0.
import sys; sys.path.insert(0,'sprite_r7'); import numpy as np; from PIL import Image; from gemeen2 import *
r6=np.array(Image.open('sprite_r6/guarana2_r6.png')).astype(int); o=r6.copy()
PUP5=np.load('sprite_r5/pupil.npy')
ST=['..OOO..','.OwWwK.','OWWWWWK','OWWWWWK','.KWWWK.','..KKK..']
GROOT={'L4':(12,28),'L5':(15,32),'M4':(29,19),'R5':(46,29),'R6':(41,32)}
NIEUW=[(2,2),(3,2),(2,3),(3,3)]
VOLG=['L3','R3','M3','R4','L1','M2','L2','L5','L4','M1','M4','R1','R2','R5','R6']
OGEN={'L3':(16,25,4,4),'R3':(42,25,4,4),'M3':(20,19,5,3),'R4':(49,26,5,3),'L1':(6,26,6,3),'M2':(24,16,5,3),'L2':(12,22,6,5),
      'L5':(15,32,7,6),'L4':(12,28,7,6),'M1':(30,12,6,5),'M4':(29,19,7,6),'R1':(46,22,6,5),'R2':(52,22,6,5),'R5':(46,29,7,6),'R6':(41,32,7,6)}
def later(n,x,y):   # ligt (x,y) in de stempel van een oog dat later (ervoor) getekend is?
    for m in VOLG[VOLG.index(n)+1:]:
        X,Y,w,h=OGEN[m]
        if X<=x<X+w and Y<=y<Y+h: return True
    return False
log=[]
for n,(X,Y) in GROOT.items():
    for dy,rij in enumerate(ST):
        for dx,c in enumerate(rij):
            x,y=X+dx,Y+dy
            if c in '.OK' or later(n,x,y) or not (0<=x<64 and 0<=y<64): continue
            nieuw_p=(dx,dy) in NIEUW
            if nieuw_p and r6[y,x] in (10,11,1): o[y,x]=1
            elif not nieuw_p and r6[y,x]==1 and PUP5[y,x]: o[y,x]=10 if c=='W' else 11
            if o[y,x]!=r6[y,x]: log.append((n,x,y,int(r6[y,x]),int(o[y,x])))
d=o!=r6
print('anders dan r6:',int(d.sum())); [print(l) for l in log]
assert ((o>0)==(r6>0)).all()
opslaan(o,'sprite_r7/guarana2_r7.png'); open('sprite_r7/normal.pal','w').write(open('sprite_r6/normal.pal').read())
W=(255,255,255); T=Image.new('RGB',(1056,512),'white')
T.paste(rgb(o,W).resize((512,512),0),(0,0)); T.paste(rgb(r6,W).resize((512,512),0),(544,0)); T.save('sprite_r7/voor_jordi_r7_8x.png')
