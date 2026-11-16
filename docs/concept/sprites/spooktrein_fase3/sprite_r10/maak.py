# r10: alleen de trein (ijzer). Basis r9; groen en de zwarte gezichtslijnen bevroren (bewijs in controle.py).
from PIL import Image; import numpy as np
S='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
im=Image.open(S+'sprite_r9/sprite.png'); a=np.array(im); r9=a.copy()
G={2,3,4,5,6,13}; H={'.':0,'A':10,'B':11,'C':12}
def v(c): return H[c] if c in H else int(c)
# 1. koeienvanger y45-59, x0-23 naar het model ('g' = bevroren groen uit r9, '=' = r9 houden)
KV={ # x: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
45:". 1 7 = 8 = = = = = g g g g = = = = g = = = = =",
46:". 1 7 = = = = = = = = g g g = = = = = = = = = =",
47:". 1 7 8 9 C A A B 9 9 1 g = = = = = = = = = = =",
48:". 1 7 8 9 C A B B B 1 9 9 9 1 7 7 7 7 7 7 7 C 1",
49:". 1 7 8 9 C A B B B C 1 9 1 7 7 A B B B B B C 1",
50:"C 7 7 8 9 C A B B B C 1 1 8 9 1 A B B B B B C 1",
51:"C 7 7 C C 1 A B B B C 1 7 8 9 1 A B 8 8 B C C 1",
52:"C C 7 C C 9 1 A B 8 C 1 7 8 9 1 A B 8 9 B C C 1",
53:"C C 7 8 8 9 1 A 8 8 C 1 7 8 9 1 A B 9 9 B C C 1",
54:"1 C C 7 8 9 1 A B B 1 g 7 8 9 9 1 B B B C C C 1",
55:". 1 C 7 8 9 1 A B 1 g g 7 8 9 1 1 1 1 1 1 1 1 =",
56:". 1 C 7 8 9 1 B B 1 g g 7 8 1 g g g g . . . . g",
57:". . 1 1 7 7 1 B 1 g g g 1 1 g g g g 1 . . . . =",
58:". . . . 1 7 1 1 1 1 g g g g g g g g . . . . . =",
59:". . . . . 1 1 . . = g g g g g g = = = = = = = =",
}
for y,s in KV.items():
    s=s.split()
    assert len(s)==24,(y,s,len(s))
    for x,c in enumerate(s):
        if c=='=': continue
        if c=='g': assert a[y,x] in G,(x,y); continue
        assert a[y,x] not in G,(x,y,c)
        a[y,x]=v(c)
a[44,2]=7
# 2. kop links rond (keurder MOET B)
for (x,y),n in {(0,30):0,(1,30):9,(0,31):0,(1,31):9,(0,32):0,(1,32):9,(0,40):0,(0,41):0,(0,42):0,
                (0,43):0,(1,43):1,(0,45):0,(0,46):0,(0,47):0}.items(): a[y,x]=n
# 3. schoorsteenpijp alleen opschonen (Jordi: "de pijp is geen ramp"): y19 egaal licht | grijs | roest | donker
for x,c in zip(range(14,23),"77AA99CC1"): a[19,x]=v(c)
# 4. grote lichte plaat iets kleiner/hoger (model y21-26 licht, onderrand donkerder)
for (x,y),c in {(4,25):'8',(4,26):'8',(5,26):'8',(5,31):'8',(6,31):'8'}.items(): a[y,x]=v(c)
# 5. onderste plaat rechts: lichte bovenrand/linkerkant zoals het model, roest naar rechtsonder
for (x,y),c in {(37,35):'B',(38,35):'B',(39,35):'B',(36,36):'7',(37,36):'7',(38,36):'B',
                (35,36):'7',(36,37):'7',(32,37):'A',(32,39):'A',(33,37):'7',(34,37):'7',(35,37):'7',(32,38):'A',(31,39):'A',(31,40):'A'}.items():
    assert a[y,x] not in G,(x,y); a[y,x]=v(c)
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save(S+'sprite_r10/sprite.png',transparency=0)
with open(S+'sprite_r10/raster.txt','w') as f:
    f.write(open(S+'sprite_r9/raster.txt').read().split('\n.')[0].rsplit('\n',0)[0].split('\n# D')[0]+'\n# D (232, 248, 232)\n')
    for row in a: f.write(''.join('.' if q==0 else '%X'%q for q in row)+'\n')
print('gewijzigd',int((a!=r9).sum()))
