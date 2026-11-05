"""Bewijs: de kop van ronde-1 variant A is in D en E alleen verschoven (0,-5), niet hertekend.
1) alle pixels van de kopvorm HEAD (silhouet1.py) zitten in A op (9,11) en in D/E op (9,6);
2) het vrije deel van de kop (boven de kegel: A rijen < 24, D/E rijen < 19) is pixel voor pixel gelijk."""
import sys
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/scripts')
from PIL import Image
from silhouet1 import head
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
def load(f):
    P=Image.open(f).load(); return {(x,y) for x in range(64) for y in range(64) if P[x,y]!=0}
A=load(D+'silhouet1/variant_A.png')
hA=head(9,11); print('A: kopvorm volledig aanwezig:', hA<=A, len(hA),'px')
freeA={(x,y-5) for (x,y) in A if y<24}
for k in 'DE':
    V=load(D+'silhouet2/variant_%s.png'%k)
    hV=head(9,6)
    freeV={(x,y) for (x,y) in V if y<19}
    print(k+': kopvorm volledig aanwezig:', hV<=V, '| vrije kop gelijk aan A verschoven (0,-5):', freeV==freeA,
          '| verschil:', len(freeV^freeA),'px')
