# r15 = r14 + keurderspunten (alleen bestaande pixels omkleuren/weghalen). # 1 D 2 d 3 m 4 g 5 l 6 L 7 W 8
import numpy as np, sys
sys.path.insert(0,'../sprite_r7'); from build import save
o=np.load('../sprite_r14/bokser.npy'); a=o.copy()
def z(x,y,van,naar):
    if van is not None: assert a[y,x]==van,(x,y,a[y,x],van)
    a[y,x]=naar
# 1 nabije schouderrand
for x,y in [(41,27),(42,28),(43,29),(42,33)]: z(x,y,4,1)
# 2 onderkant nabije schouder
for x,y in [(40,33),(41,33)]: z(x,y,1,4)
z(42,32,5,4)
# 3 verre schouder
g=[(x,y) for y in range(28,33) for x in range(15,21) if o[y,x]==5]
for x,y in [(16,29),(17,29),(16,30),(17,30)]: z(x,y,7,5)
for x,y in g: z(x,y,5,4)
for x in (15,16,17): z(x,34,4,1); z(x,35,1,0)
z(20,27,4,1); z(21,28,4,1)
# 4 verre scheen: linkerrand 1 px naar binnen, been 1 toon donkerder
for x,y in [(27,49),(28,50),(29,51),(29,52),(29,53),(29,54)]: z(x,y,8,1); z(x-1,y,1,0)
grens={45:29,46:29,47:29,48:29,49:30,50:31,51:31,52:31,53:31,54:31}
for y,xm in grens.items():
    for x in range(20,xm+1):
        if a[y,x]==8: a[y,x]=7
        elif a[y,x]==7: a[y,x]=6
# 5 rompsikkel
for x in range(26,32):
    if a[35,x]==8: a[35,x]=7
for x in list(range(22,31))+[31,32,35]:
    if a[36,x]==8: a[36,x]=7
# 6 broeksband, 7 Y-naad
for x in (27,28,29): z(x,38,6,3)
z(27,42,1,2)
# 8 nabije onderarm: licht boven, rechts ervan midden
for x,y in [(35,37),(36,38),(37,39),(38,40),(39,41)]: z(x,y,6,8); z(x+1,y,8,7)
# 9 kuif
z(47,11,3,1); z(48,12,3,1)
z(22,37,8,7)   # eigen controle: losse W-pixel na de rompsikkel -> L (zelfde sikkel)
save(a,'bokser')
d=a!=o; print('gewijzigd:',int(d.sum()))
