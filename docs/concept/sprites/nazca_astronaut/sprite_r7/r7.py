# r7: keurdersreparaties op r6 per pixel (x,y in de 64x64-png), P2 = zwarte grond + rood + wit.
import numpy as np; from PIL import Image
K1=['.','1','2','3','B','D','G','H','K','L','M','R','S','W','b','g']   # r6-P1-indexen (keurder)
R=np.array(K1)[np.asarray(Image.open('../sprite_r6/astro_P1.png'))]; r6=R.copy()
K2=['.','1','2','3','B','D','K','L','M','R','S','W','b','g','r']
R2_6=np.array(K2)[np.asarray(Image.open('../sprite_r6/astro_P2.png'))]
PUNTEN={
 '1 rechterelleboog':[((40,36),'G'),((41,36),'H')],
 '3 volume onderarmen':[((20,21),'D'),((20,22),'D'),((20,23),'D'),((42,37),'D'),((43,38),'D'),((44,39),'D')],
 '4 volume schenen':[((29,50),'D'),((29,51),'D'),((37,49),'D'),((37,50),'D'),((38,51),'D')],
 '5 beenstrepen':[((28,55),'R'),((29,55),'R'),((30,55),'R'),((27,57),'b'),
                  ((38,54),'M'),((35,57),'r'),((36,57),'R'),((37,57),'R'),((38,57),'R'),((39,57),'R')],
 '6 ruis voeten':[((28,61),'D'),((36,59),'L'),((38,62),'D')],
 '7 linkerarm streep':[((17,16),'B'),((18,16),'B'),((19,16),'B')],
 '8 zwart tussen selout':[((16,22),'S')],
}
for naam,lst in PUNTEN.items():
    uit=[]
    for (x,y),c in lst:
        assert R[y,x]!='.'; uit.append('(%d,%d) %s->%s'%(x,y,R[y,x],c)); R[y,x]=c
    print(naam+':',', '.join(uit))
KL={'.':(0,0,0),'K':(16,14,22),'1':(30,28,44),'2':(48,46,70),'3':(76,74,108),'g':(128,126,166),
    'L':(246,236,202),'M':(228,208,158),'D':(186,156,104),'S':(126,94,54),'B':(80,120,200),'b':(44,66,140),
    'R':(214,66,58),'r':(140,36,40),'W':(248,248,248),'G':(56,160,72),'H':(40,104,56)}
def schrijf(naam,r):
    keys=['.']+sorted(set(r.ravel())-{'.'}); assert len(keys)<=16,keys
    im=Image.fromarray(np.vectorize(keys.index)(r).astype('uint8'),'P')
    flat=[v for k in keys for v in KL[k]]; im.putpalette(flat+[0]*(768-len(flat))); im.save(naam,transparency=0); print(naam,len(keys),'kleuren')
P1=R.copy(); P1[P1=='r']='K'; schrijf('astro_P1.png',P1)
P2=R.copy(); P2[P2=='G']='R'; P2[P2=='H']='r'
P2[(R2_6=='r')&(r6=='K')]='r'          # donkerrode selout van de strepen terug (in P2 is er plek)
schrijf('astro_P2.png',P2)
# bewijs
p6=np.asarray(Image.open('../sprite_r6/astro_P1.png'))
for f in ('astro_P1.png','astro_P2.png'):
    print(f,'alpha-diff t.o.v. r6:',((np.asarray(Image.open(f))>0)!=(p6>0)).sum())
d=(P1!=r6); print('P1: rollen gewijzigd t.o.v. r6-P1:',d.sum(),'kop (y<26):',d[:26].sum())
