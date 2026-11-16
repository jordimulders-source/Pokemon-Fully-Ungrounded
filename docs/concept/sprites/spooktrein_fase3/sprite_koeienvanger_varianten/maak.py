# Varianten A-E van alleen de koeienvanger (x0-25, y42-61) op basis r13. Groen diff 0 (assert), silhouet = r13.
from PIL import Image; import numpy as np
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
im=Image.open(D+'sprite_r13/sprite.png'); R=np.array(im)
G={2,3,4,5,6,13}; IJ={1,7,8,9,10,11,12}
H={'.':0,'A':10,'B':11,'C':12}
def v(c): return H[c] if c in H else int(c)
def bouw(T):
    a=R.copy()
    for y,s in T.items():
        t=s.split(); assert len(t)==24,(y,len(t))
        for x,c in enumerate(t):
            if c=='=': continue
            if c=='g': assert a[y,x] in G,(x,y); continue
            assert a[y,x] not in G,(x,y,c); a[y,x]=v(c)
    return a
# E: eigen beste. Bovenkanten in V's, naden schuin naar de punt, middentand met punt, 3 roestvlekken.
#       x: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
E={47:". 1 7 7 1 8 9 7 7 1 9 9 g 9 9 9 9 9 9 9 9 = = =",
   48:". 9 7 7 1 8 9 7 B 7 1 9 9 9 9 9 9 1 1 7 7 C 1 1",
   49:". 9 7 7 8 1 9 7 B C 7 1 1 7 7 1 1 7 7 B C C C 1",
   50:". 9 7 7 8 1 8 7 B C C 1 7 8 C 1 7 B B C C 1 C 1",
   51:". 9 7 8 8 9 1 7 B C C 1 7 8 C 1 7 8 8 C C 1 C 1",
   52:". 9 7 8 8 9 1 7 B C C 1 7 8 1 7 B 8 8 C 1 C C 1",
   53:". 9 7 7 8 9 1 7 B C C 1 7 8 1 B C 9 9 C 1 C C 1",
   54:". 9 7 7 9 1 7 B C C 1 g 7 9 1 C C C C 1 C C C 1",
   55:". 9 7 7 9 1 7 B C 1 g g 7 9 1 1 1 1 1 1 1 1 1 1",
   56:". . 1 7 7 1 B C 1 1 g g 9 1 1 g g g g = = = = =",
   57:". . . 1 7 B C C 1 g g g 1 1 g g g g = = = = = =",
   58:". . . 1 7 C 1 1 1 1 g g g g g g g g = = = = = ="}
def zonder_roest(T,keep_rows=(47,48)):  # roest in de bladen -> donkergrijs (band boven blijft)
    out={}
    for y,s in T.items():
        t=s.split()
        if y not in keep_rows:
            t=[('C' if (c in '89' and x>=6) else c) for x,c in enumerate(t)]
        out[y]=' '.join(t)
    return out
# B: donkere kaak, alleen 3 smalle lichte bladranden (wig, linkerplaat, rechterplaat); middentand donker met vlakke onderkant (als r13)
Bv=zonder_roest(E)
def zet(T,y,x,c):
    t=T[y].split(); t[x]=c; T[y]=' '.join(t)
for y in range(49,56): zet(Bv,y,12,'C')   # geen lichte rand op de tand
for y in (49,): zet(Bv,y,13,'C'); zet(Bv,y,14,'C')
zet(Bv,56,12,'C'); zet(Bv,56,13,'C')       # vlakke onderkant
# C: zoals B, maar middentand met lichte rand en een punt omlaag
Cv=dict(Bv)
for y in range(50,56): zet(Cv,y,12,'7')
zet(Cv,49,13,'7'); zet(Cv,49,14,'7'); zet(Cv,56,12,'C'); zet(Cv,56,13,'1')
# D: minder bladen, grotere vlakken: wig + linkerplaat als één plaat, rechterplaat zonder groef
Dv={47:". 1 7 7 7 7 7 7 1 9 9 9 g 9 9 9 9 9 9 9 9 = = =",
    48:". 9 7 B B B B B 7 1 9 9 9 9 9 9 9 1 1 7 7 C 1 1",
    49:". 9 7 B B B B C C 7 1 1 1 7 7 1 1 7 7 B C C C 1",
    50:". 9 7 B 8 8 C C C C 1 1 7 8 C 1 7 B B B C C C 1",
    51:". 9 7 B 8 8 C C C C C 1 7 8 C 1 7 B 8 8 C C C 1",
    52:". 9 7 B 8 9 C C C C C 1 7 8 1 7 B B 8 8 C C C 1",
    53:". 9 7 B 9 9 C C C C C 1 7 8 1 B B C 9 9 C C C 1",
    54:". 9 7 B C C C C C C 1 g 7 9 1 C C C C C C C C 1",
    55:". 9 7 B C C C C C 1 g g 7 9 1 1 1 1 1 1 1 1 1 1",
    56:". . 1 7 B C C C 1 1 g g 9 1 1 g g g g = = = = =",
    57:". . . 1 7 C C C 1 g g g 1 1 g g g g = = = = = =",
    58:". . . 1 7 C 1 1 1 1 g g g g g g g g = = = = = ="}
# A: zo letterlijk mogelijk uit natief.png (dichtstbijzijnde natieve pixel, palet 1/7/8/9/11/12), binnen het r13-silhouet; alleen 1-px-ruis weg
def variant_A():
    n=np.array(Image.open(D+'model/natief.png').convert('RGB')).astype(int)
    P=np.array(im.getpalette()[:14*3]).reshape(14,3); idx=[1,7,8,9,11,12]
    a=R.copy()
    for y in range(47,59):
        for x in range(0,24):
            if a[y,x] not in IJ: continue
            nx=int(round(9+(x+0.5)/0.744-0.5)); ny=int(round(6+(y-2+0.5)/0.744-0.5))
            c=n[ny,nx]
            if c.min()>215 or c[1]>c[0]+20: continue   # wit/groen in het model: r13 houden
            a[y,x]=idx[int(np.argmin([((c-P[i])**2).sum() for i in idx]))]
    from collections import Counter
    for _ in range(2):
        b=a.copy()
        for y in range(47,59):
            for x in range(1,24):
                q=a[y,x]
                if q not in IJ: continue
                nb=[a[y+dy,x+dx] for dy,dx in((0,1),(1,0),(0,-1),(-1,0))]
                if q in nb: continue
                c=Counter(t for t in nb if t in IJ)
                if c: b[y,x]=c.most_common(1)[0][0]
        a=b
    return a
V={'A':variant_A(),'B':bouw(Bv),'C':bouw(Cv),'D':bouw(Dv),'E':bouw(E)}
for k,a in V.items():
    g=np.isin(R,list(G))|np.isin(a,list(G)); assert (a[g]==R[g]).all(),k
    d=np.argwhere(a!=R); assert all(0<=x<=25 and 42<=y<=61 for y,x in d),k
    o=Image.fromarray(a,'P'); o.putpalette(im.getpalette()); o.save(D+'sprite_koeienvanger_varianten/%s.png'%k,transparency=0)
    print(k,'gewijzigd t.o.v. r13:',len(d),'| groen-diff 0')
