from PIL import Image
import numpy as np
src=Image.open('../../r17/picapau.png'); a=np.array(src); PAL=src.getpalette()
b=a.copy()
Lc,M,Dk,D,Z=2,3,4,13,1
# --- losse D-pixel in de zwarte buitenlijn linksonder (om en om) -> zwart
assert a[49,18]==D; b[49,18]=Z
# --- kop: per rij (x0,x1,kleur) op gele pixels
kop={
 18:[(26,27,Lc)],
 19:[(26,26,Lc)],
 20:[(25,26,M)],
 21:[(25,27,M)],
 22:[(24,28,Lc),(29,30,M)],
 23:[(20,27,Lc),(28,29,M),(30,30,Dk)],
 24:[(19,27,Lc),(28,29,M),(30,31,Dk)],
 25:[(18,26,Lc),(27,28,M),(29,31,Dk)],
 26:[(18,25,Lc),(26,28,M),(29,32,Dk)],
 27:[(17,24,Lc),(28,29,M),(30,32,Dk)],
 28:[(18,23,Lc),(29,29,M),(30,32,Dk)],
 29:[(19,23,Lc),(29,30,M),(31,33,Dk)],
 30:[(20,22,Lc),(23,23,M),(29,30,M),(31,32,Dk)],
 31:[(21,22,Lc),(23,24,M),(28,29,M),(30,32,Dk)],
 32:[(22,24,Lc),(25,29,M),(30,32,Dk)],
 33:[(22,24,Lc),(28,29,M),(30,32,Dk)],
 34:[(17,17,M),(21,23,M),(29,29,M),(30,32,Dk)],
 35:[(17,23,M),(29,33,Dk)],
 36:[(17,23,M),(29,31,Dk)],
 37:[(18,24,M),(28,31,Dk)],
 38:[(19,30,Dk)],
}
for y,segs in kop.items():
    for x0,x1,c in segs:
        for x in range(x0,x1+1):
            assert a[y,x] in (2,3,4),(x,y,a[y,x]); b[y,x]=c
# --- lijf: met de hand per rij (licht = ovaal midden-links, donker = sikkel rechts/onder)
lijf={
 39:[(19,28,M),(29,30,Dk)],
 40:[(19,28,M),(29,30,Dk)],
 41:[(18,20,M),(21,23,Lc),(24,29,M),(30,30,Dk)],
 42:[(18,19,M),(20,25,Lc),(26,29,M),(30,31,Dk)],
 43:[(18,18,M),(19,25,Lc),(26,29,M),(30,31,Dk)],
 44:[(18,18,M),(19,24,Lc),(25,29,M),(30,31,Dk)],
 45:[(18,19,M),(20,23,Lc),(24,29,M),(30,32,Dk)],
 46:[(18,28,M),(29,33,Dk)],
 47:[(18,28,M),(29,33,Dk)],
 48:[(18,27,M),(28,34,Dk)],
 49:[(19,27,M),(28,35,Dk)],
 50:[(19,26,M),(27,36,Dk)],
 51:[(20,29,M),(30,37,Dk)],
 52:[(21,25,M),(26,27,Dk),(28,30,M),(31,37,Dk)],
 53:[(23,36,Dk)],
 54:[(26,35,Dk)],
 55:[(31,31,Dk)],
}
for y,segs in lijf.items():
    for x0,x1,c in segs:
        for x in range(x0,x1+1):
            assert a[y,x] in (2,3,4),(x,y,a[y,x]); b[y,x]=c
# --- vleugel onder (slagpennen): lichte baan C links, sikkel D rechts/onder
C,W=12,13
vl={44:(33,36),45:(34,37),46:(35,37),47:(35,38),48:(36,38),49:(37,38),50:(38,39)}
for y,(x0,x1) in vl.items():
    for x in range(x0,x1+1):
        assert a[y,x]==W,(x,y,a[y,x]); b[y,x]=C
# --- staart: lichte baan langs de bovenrand doorgetrokken, wortel donker
T7,T8,T9=7,8,9
st={(39,54):T7,(38,55):T8,(39,55):T7,(40,55):T7,(38,56):T8,(39,56):T8,(40,56):T7,(41,56):T7,(45,60):T9}
for (x,y),c in st.items():
    assert a[y,x] in (7,8,9),(x,y,a[y,x]); b[y,x]=c
np.save('_tmp/b.npy',b)
p=Image.fromarray(b,'P'); p.putpalette(PAL); p.save('_tmp/b.png',transparency=0)
for y in range(12,63): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in b[y,14:49]))
