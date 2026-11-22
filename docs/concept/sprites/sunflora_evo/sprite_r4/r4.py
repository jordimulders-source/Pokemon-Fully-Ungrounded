# r4 = r3-buiten met alleen het lijf herkleurd/herlijnd (Gen 3: zwart onder/rechts, donkergroen 11 boven/links,
# hooglicht 14 linksboven, hoofdtint 13, schaduwsikkel 12 onder/rechts). Hoofd bevroren (assert).
# Tekens: 0 leeg, 1 zwart, b=11 selout, c=12 schaduw, d=13 hoofd, e=14 hooglicht.
import numpy as np; from PIL import Image
import sys; sys.path.insert(0,'../sprite_r3'); from pal import PAL
C=np.load('r3_buiten.npy'); kop=np.load('../sprite_r2/kop_r1.npy'); O=C.copy()
V={'0':0,'1':1,'b':11,'c':12,'d':13,'e':14}
E={ # (rij,kol): teken
 # linkerarm
 (44,18):'b',(45,17):'b',(45,18):'e',(46,14):'b',(46,15):'b',(46,16):'b',(46,17):'e',(46,18):'d',
 (47,14):'b',(47,15):'e',(47,16):'d',(47,17):'d',(47,18):'d',(47,19):'c',(47,22):'c',(47,23):'c',
 (48,14):'b',(48,15):'1',(48,16):'d',(48,17):'c',(48,18):'c',(48,19):'c',(48,20):'c',(48,21):'1',
 (49,21):'0',
 # rechterarm
 (47,39):'d',(47,40):'e',(47,41):'e',(47,42):'d',(47,43):'d',
 (48,39):'d',(48,40):'c',(48,41):'c',(48,42):'c',(48,43):'c',(48,44):'c',(48,45):'1',(49,45):'0',
 # lijfje
 (47,33):'d',(48,32):'e',(48,33):'d',(48,34):'d',(49,31):'e',(49,32):'d',(49,33):'d',(49,34):'c',(49,35):'c',
 (50,31):'d',(50,32):'d',(50,33):'c',(50,34):'c',(51,31):'d',(51,32):'c',(51,33):'c',(52,30):'d',(52,31):'c',(52,32):'c',
 (53,30):'c',
 # linkervoet
 (54,28):'b',(54,29):'b',(54,30):'b',
 (55,27):'b',(55,28):'e',(55,29):'d',(55,30):'1',
 (56,26):'b',(56,27):'e',(56,28):'d',(56,29):'c',(56,30):'1',
 (57,26):'b',(57,27):'d',(57,28):'d',(57,29):'c',(57,30):'1',
 (58,26):'b',(58,27):'d',(58,28):'c',(58,29):'1',
 (59,26):'0',(59,27):'1',(59,28):'1',(60,27):'1',
 # rechtervoet
 (53,34):'c',(53,35):'1',
 (54,34):'b',(54,35):'e',(54,36):'d',(54,37):'b',
 (55,34):'b',(55,35):'e',(55,36):'d',(55,37):'d',(55,38):'b',(55,39):'b',
 (56,35):'b',(56,36):'d',(56,37):'d',(56,38):'c',(56,39):'1',
 (57,35):'b',(57,36):'d',(57,37):'d',(57,38):'c',(57,39):'c',(57,40):'1',
 (58,36):'1',(58,37):'1',(58,38):'c',(58,39):'c',(58,40):'1',
 (59,38):'1',(59,39):'1',(59,40):'1',
}
for (y,x),t in E.items():
    assert kop[y,x]==0,(y,x)
    C[y,x]=V[t]
assert (C[kop>0]==kop[kop>0]).all(); print('hoofddiff 0 (bewezen)')
ch='.123456789abcdef'
print('gewijzigde lijfpixels',int((C!=O).sum()),'| buiten r3-silhouet erbij',int(((C>0)&(O==0)).sum()),'| weg uit silhouet',[(int(y),int(x)) for y,x in zip(*np.where((C==0)&(O>0)))])
for y in range(43,62): print('%2d'%y,''.join('H' if kop[y,x] else ch[C[y,x]] for x in range(10,52)))
np.save('r4.npy',C)
im=Image.fromarray(C,'P'); im.putpalette([v for c in PAL for v in c]); im.save('sunflora_evo_r4.png',transparency=0)
Image.open('sunflora_evo_r4.png').convert('RGBA').resize((512,512),Image.NEAREST).save('sunflora_evo_r4_8x.png')
