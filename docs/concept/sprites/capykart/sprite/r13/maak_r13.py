"""Capykart r13: geheel/niet blurry, strakke hoepels, blokkentoren in perspectief op de achterbak.
Basis r12_creme; toren (alleen hier vormwijziging) handmatig opgezet; wit = zelfde pixels, ander palet."""
D={1:2,2:2,3:1,4:1,5:0,6:0,7:0,8:0,9:0,10:0,11:0}
TOP={10:"1YY11tttttt11",11:"1YYYY11111111"}
# piramide (groene driehoek) met 1 px overstek links en rechts, zoals het model breder dan de blokken
PYR={-1:(9,9),0:(8,9),1:(7,8),2:(6,8),3:(5,8),4:(4,8),5:(3,9),6:(3,9),7:(4,9),8:(5,9),9:(6,9),10:(7,9),11:(8,9),12:(9,9)}
def tower(B0=32,off=1):
    T={}
    for x in range(1,12):
        d=D[x]
        for k,(a,b) in enumerate([('A','8'),('C','r'),('Y','O')]):
            bot=B0-7*k-d
            T[(x,bot)]='1'
            for y in range(bot-6,bot): T[(x,y)]=a if x<=5 else b
    for r,s in TOP.items():
        for c,ch in enumerate(s):
            if ch!='.': T[(c,r)]=ch
    for y in range(8,B0-2): T.setdefault((0,y),'1')
    for y in range(11,B0): T.setdefault((12,y),'1')
    # belijning lichtkant in eigen donkere tint (zoals r12): linkerrand per blok, piramide linksboven
    fc={'Y':'L4','C':'L7','A':'L8'}
    for y in range(0,B0):
        if T.get((0,y))=='1':
            for yy in (y,y+1,y+2):
                v=T.get((1,yy))
                if v in fc: T[(0,y)]=fc[v]; break
    for c,(t,b) in PYR.items():
        for r in range(t,b+1): T[(c,r)]='F' if c<=5 else 'B'
        T[(c,t-1)]='LB' if c<=5 else '1'
    T[(-2,9)]='LB'; T[(13,9)]='1'; T[(-1,10)]='1'; T[(12,10)]='1'
    T[(1,9)]='1'; T[(2,9)]='1'; T[(3,9)]='t'; T[(4,9)]='t'; T[(11,10)]='1'
    # opvullen tussen piramide-rand en kolomlijn
    T[(0,10)]=T.get((0,10),'1')
    return {(x,y+off):v for (x,y),v in T.items()}

import os, sys
from collections import Counter
from PIL import Image
D13=os.path.dirname(os.path.abspath(__file__))
R=os.path.join(D13,'../../')
im=Image.open(os.path.join(R,'sprite/r12/r12_creme.png')); pal=im.getpalette()
r12=[[im.getpixel((x,y)) for x in range(64)] for y in range(64)]
g=[row[:] for row in r12]
H={'.':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
def put(y,x0,s):
    for i,ch in enumerate(s):
        if ch!='?': g[y][x0+i]=H[ch]
# ---------- linkerdeel auto (x0..35), rijen 35-58 ----------
put(35,12,"889998888"); put(35,21,"555")
rows={
36:"..........88888888888888555555566133",
37:".........888111111111888885555556133",
38:".......441116666666661118888555556613"[:36],
39:"......45555555555566DDDD1188855566144"[:36],
}
# rijen precies opgebouwd uit segmenten
def seg(*p): return ''.join(p)
rows[38]=seg(".......","44","1","11","666666666","111","8888","55555","66","1")
rows[39]=seg("......","4","55555555555","66","DDDD","11","888","555","66","1","4")
rows[40]=seg("....","44","555555555555","66","DDDD","66","11","88","55","66","44")
rows[41]=seg("...","4","5555555555555","666","DDDD","6666","1","88","5","1","6","4","6")
rows[42]=seg("...","4","5555555555555","66","DDDDD","66666","1","888","1","66")
rows[43]=seg("..","4","55","66666","555555","66","DDDDDD","444444","1","88","1","44")
rows[44]=seg("..","4","55","666666666","555","4","DDDDDD","6666666","88","1","DD")
rows[45]=seg(".","4","55","666","D","6666","D","666","4","55","DDDDD","6666666","88","1","DD")
rows[46]=seg(".","4","55","666","D","6666","D","666","4","55","666","DD","6666666","88","1","DD")
rows[47]=seg(".","4","55","666","D","6666","D","666","4","55","666","DD","666","4444","88","1","DD")
rows[48]=seg(".","4","55","666","D","6666","D","666","4","55","666","DD","666666","11111","D")
rows[49]=seg(".","4","5","6666","D","6666","D","666","4","55","44444","??????????","1","4")
rows[50]=seg(".","1","4","6666","D","6666","D","666","4","55","DDDD","????????????","1")
rows[51]=seg("..","1","4","DDDDDDDDDDDD","4","66","DDDD","????????????","1")
rows[52]=seg("..","1","4","DDDDDDDDDDDD","4","66","DDDD","?????????????")
rows[53]=seg("...","111","4444444444","4","DD","4444","?????????????")
rows[54]=seg(".....","1","DDD","1111","4444","DD","4444","?????????????")
rows[55]=seg("......","1","DDD","44","111","44","DD","4444","?????????????")
rows[56]=seg(".......","1","DD","4444","111111111","?????????????")
rows[57]=seg("........","11","444","1")
for y,s in rows.items(): put(y,0,s)
# ---------- kop: E-hooglicht als een sikkel ----------
for y in range(13,24):
    for x in range(14,30):
        if g[y][x]==14: g[y][x]=2
for y,(a,b) in {14:(24,28),15:(25,28),16:(24,27),17:(20,25),18:(18,22)}.items():
    for x in range(a,b+1):
        if g[y][x] in (2,3): g[y][x]=14
if g[21][22]==3: g[21][22]=2
# ---------- middenpaneel x34-48 ----------
for y in range(36,38):
    for x in range(36,49): g[y][x]=4
put(38,36,"4444444"); put(38,43,"555555")
put(39,35,"444444"); put(39,41,"55555566")
put(40,34,"444"); put(40,37,"555555"); put(40,43,"666666")
put(41,36,"555"); put(41,39,"6666666666")
put(42,33,"6666666666666666")
put(43,34,"4444444"); put(43,41,"66666666")
for y in range(44,50):
    for x in range(36 if y==49 else 34,49): g[y][x]=13
g[49][35]=4
put(50,36,"44444444444"); put(50,47,"DD")
put(51,36,"4444444444444")
# ---------- toren + dek (x>=42, y<=35) ----------
cap_end={32:44,33:46,34:46,35:47}
for y in range(0,36):
    for x in range(42,64):
        if y<=31 and (x>=43 or g[y][x] not in (2,3,4,14)): g[y][x]=0
        elif y>=32 and x>cap_end[y]: g[y][x]=0
X=46
M={'L4':4,'L7':7,'L8':8,'LB':11,'F':15,'G':15,'B':11,'Y':9,'O':6,'t':9,'C':12,'r':7,'A':10,'8':8,'1':1}
TW={}
for (c,r),ch in tower().items(): g[r][X+c]=M[ch]; TW[(X+c,r)]=ch
# dek (handmatig)
put(30,43,"444"); g[31][43]=4
put(31,44,"55D")
put(32,45,"55DD")
put(33,47,"5"); put(33,58,"DD4")
put(34,47,"55"); put(34,52,"DDDDDDDD54")
put(35,48,"5"); put(35,51,"55555555555"); g[35][62]=4
put(32,59,"4")
# ---------- achterhoepel ----------
put(33,48,"881")
for y in range(34,45): put(y,49,"881")
g[45][49]=8
# ---------- kofferbak-zijkant x52-61 r36-43 ----------
for y in range(36,44):
    for x in range(52,61): g[y][x]=6 if y<=40 else 13
    g[y][61]=4; g[y][62]=1
for y in range(36,44): g[y][51]=1
g[36][51]=1

def wheel(cx,cy,rx,ry,hub=True):
    inE=lambda x,y: ((x+.5-cx)/rx)**2+((y+.5-cy)/ry)**2<=1
    for y in range(64):
        for x in range(64):
            if not inE(x,y) or r12[y][x]==0: continue
            nb=[(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))]
            if any(r12[b][a]==0 for a,b in nb):
                g[y][x]=r12[y][x] if r12[y][x] in (1,4) else 1; continue
            outside=[(a,b) for a,b in nb if not inE(a,b)]
            dx=(x+.5-cx)/rx; dy=(y+.5-cy)/ry
            l=-(dx+dy)/1.414
            if outside:
                g[y][x]=4 if l>-0.15 else 1
                continue
            r=(dx*dx+dy*dy)**.5
            t=6
            if r>0.66 and l>0.3: t=5
            if r>0.58 and l<-0.2: t=13
            if r>0.82 and l<-0.6: t=4
            if hub:
                if r<0.15: t=5
                elif r<0.30: t=4
            g[y][x]=t
W1={
47:(27,"444441"),
48:(25,"4455666611"),
49:(24,"45566666661"),
50:(24,"4556666666D1"),
51:(23,"45566666666D1"),
52:(23,"45666666666DD1"),
53:(23,"45666644666DD1"),
54:(23,"4566645546DDD1"),
55:(23,"1666645546DDD1"),
56:(23,"16666644666DD1"),
57:(23,"166666666DDD1"),
58:(23,"16666DDDDDDD1"),
59:(24,"1DDDDDDDD41"),
60:(24,"1114444411"),
}
for y,(x0,st) in W1.items(): put(y,x0,st)
for y in range(44,48):
    for x in range(56,61): g[y][x]=13
    g[y][61]=4
W2={
44:(51,"444441"),
45:(49,"4455666611"),
46:(48,"45566666661"),
47:(48,"4556666666DD1D1"),
48:(48,"4566666666DDD1"),
49:(48,"4566644666DDD1"),
50:(48,"456645546 6DD1".replace(' ','')),
51:(48,"166645546 6DD1".replace(' ','')),
52:(48,"6666644666DD1"),
53:(48,"166666666DDD1"),
54:(48,"16666DDDDDD1"),
55:(49,"1DDDDDDDD41"),
56:(50,"114444411"),
}
for y,(x0,st) in W2.items(): put(y,x0,st)
g[47][61]=4

# ---------- uitvoer: creme en wit ----------
def save(grid,palette,name):
    o=Image.new('P',(64,64)); o.putpalette(palette); o.putdata([v for r in grid for v in r]); o.save(os.path.join(D13,name),transparency=0)
    o.convert('RGBA').resize((512,512),Image.NEAREST).save(os.path.join(D13,name.replace('.png','_8x.png')))
save(g,pal,'capykart_creme.png')
wit_im=Image.open(os.path.join(R,'sprite/r12/r12_wit.png')); wpal=wit_im.getpalette()
w=[row[:] for row in g]
for y in range(64):
    for x in range(64):
        if w[y][x]==14: w[y][x]=2                      # vacht-hooglicht bestaat niet in wit
for (x,y),ch in TW.items():
    if ch=='Y': w[y][x]=14                             # geel blok voorvlak = geel
save(w,wpal,'capykart_wit.png')
# ---------- controles ----------
L=[]
zone=lambda x,y: x>=42 and y<=35
r12w=[[wit_im.getpixel((x,y)) for x in range(64)] for y in range(64)]
a_out=[(x,y) for y in range(64) for x in range(64) if (r12[y][x]==0)!=(g[y][x]==0) and not zone(x,y)]
a_in=[(x,y) for y in range(64) for x in range(64) if (r12[y][x]==0)!=(g[y][x]==0) and zone(x,y)]
add=sum(1 for (x,y) in a_in if r12[y][x]==0); rem=len(a_in)-add
L.append(f'silhouet buiten torenzone (x>=42,y<=35): {len(a_out)} px verschil')
L.append(f'silhouet in torenzone: {len(a_in)} px verschil ({add} erbij, {rem} weg)')
fz=[(x,y) for x in range(28,32) for y in range(16,22)]+[(x,y) for x in range(17,24) for y in range(30,34)]+[(21,15),(22,15),(23,15),(21,16),(22,16),(23,16),(15,22),(16,22),(18,28),(19,28)]+[(x,30) for x in range(25,29)]
L.append(f'bevroren (oog, tanden, morrillo, neusgaten/mond; {len(fz)} px): creme diff {sum(g[y][x]!=r12[y][x] for x,y in fz)}, wit diff {sum(w[y][x]!=r12w[y][x] for x,y in fz)}')
for nm,gr in (('creme',g),('wit',w)):
    c=Counter(v for r in gr for v in r); L.append(f'{nm}: {len(c)} kleuren incl. transparant')
zones={'kop/vacht (y<30, x<42)':lambda x,y: y<30 and x<42,'toren+dek (x>=42,y<=35)':zone,
 'voorste hoepel + motorkap/neus (x<36, y>=34)':lambda x,y: x<36 and y>=34,
 'midden/achterhoepel/kofferbak/achterwiel (x>=36,y>=36)':lambda x,y: x>=36 and y>=36}
for k,f in zones.items():
    n=sum(1 for y in range(64) for x in range(64) if f(x,y) and g[y][x]!=r12[y][x])
    L.append(f'zone {k}: {n} px anders dan r12_creme')
open(os.path.join(D13,'controle.txt'),'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
