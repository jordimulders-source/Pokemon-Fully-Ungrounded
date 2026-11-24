# r5.py: reparaties op r3 (r4-aanpak, aangepast na de coordinator) (raster_r3.txt -> raster.txt). Alle voegen/randen op gemeten modelplekken (vmap.py/scan.py/tonen.py).
import sys
R=[list(l.rstrip('\n')) for l in open('raster_r3.txt')][:64]
R0=[r[:] for r in R]
def put(pts,ch):
    for x,y in pts: R[y][x]=ch
def hl(y,x0,x1,ch='e'): put([(x,y) for x in range(x0,x1+1)],ch)
def vl(x,y0,y1,ch='e'): put([(x,y) for y in range(y0,y1+1)],ch)
def row(y,x0,s):
    for i,ch in enumerate(s):
        if ch!=' ': R[y][x0+i]=ch
STEEN=[]   # (seed, basis, licht, donker, toegestane tinten)
# ===== 1. GEVELS ALS LOSSE GEBOUWTJES: eigen omtrek '+' (lijnkleur), randpixels van de punten ook '+' (alpha gelijk) =====
G=lambda pts: put(pts,'+')
# --- linker onderste gevel (model tonen.py/scan: rug y18 x21-26, plankrand (26,18)->(30,25), voet y27) ---
G([(22,18),(23,18),(24,18),(25,18),(26,18),(20,19),(21,19),(20,20),(19,21),(19,22),(18,23),(18,24),(18,25),(17,26),(16,26)])   # schuine linkerrand + rug
G([(27,19),(27,20),(28,21),(28,22),(29,23),(29,24),(30,25),(30,26)])   # rand van de plank (model #8,#8,-11,#8,-11,#10,#7,-7)
row(19,22,'dddde'); row(20,21,'adddee'); row(21,20,'aaaddeee'); row(22,20,'abbddeee')
row(23,19,'bbbbbdeeee'); row(24,19,'bb+bbcdeee'); row(25,19,'bb+bbbdeee'); row(26,18,'bbbbbbbbdeee')
row(24,24,'d')    # model 11: plank, geen los c-pixel
hl(27,17,30,'+')  # voet (model y27 -15..-17 en #9,#7,#8)
# --- rechter onderste gevel (top y19 x34-39, linkerrand (33,20)->(30,25), plankrand (39,20)->(42,27), voet y28 x31-35) ---
G([(34,19),(35,19),(36,19),(37,19),(38,19),(39,19)])
G([(33,20),(32,21),(32,22),(31,23),(31,24)])
G([(39,20),(39,21),(40,22),(40,23),(41,24),(41,25),(42,26),(42,27)])
row(20,34,'adddd'); row(21,33,'aadddd'); row(22,33,'aaaddd'); row(23,32,'aabbdddd')
row(24,32,'a+bbbdddd'); row(25,31,'bb+bbbdddd'); row(26,31,'bbbbbbbdddd'); row(27,31,'bbbbbbbdddd')
hl(28,27,35,'+')  # voet (model y28 #17,-17,-17,#17,-15..)
put([(30,22),(30,23),(30,24)],'d')   # rand van de linkergevel tussen beide gevels (model 11 op x30 y23-24)
# --- middelste gevel (punt (33,8), plankrand (35,9)->(37,15), voet y16) ---
G([(33,8),(31,9),(32,9),(30,10),(30,11),(29,12),(29,13),(28,14),(28,15)])
G([(35,10),(36,11),(36,12),(37,13),(37,14),(37,15),(36,16)])
row(9,33,'dd'); row(10,31,'addd'); row(11,31,'aaddd'); row(12,30,'aaaddd'); row(13,30,'aaaaddd')
row(14,29,'bb+bbddd'); row(15,29,'bb+bbbee'); hl(16,28,35,'+')
G([(36,9),(37,9)])   # randpixels van het terras achter de gevel, aansluitend op de omtrek
put([(34,17)],'b')
# --- topgevels: linker (rand (40,4)->(38,8)), dal, binnenlijn rechtergevel (45,4)->(43,9), voet y10 ---
G([(40,4),(39,5),(39,6),(39,7),(38,8)])
G([(45,4),(44,5),(44,6),(44,7),(43,8),(43,9)])
put([(42,6),(43,6),(42,7),(43,7)],'e'); put([(46,4),(47,4)],'a'); put([(40,8)],'b')
hl(10,38,47,'+')
# ===== 2. GEZICHTSBLOK RUSTIG: max. 1 voeg, niet binnen 2 px van deurpost/latei =====
for x in (26,27): R[53][x]='b'          # r3-voegje tegen de rechterdeurpost weg
hl(53,28,31)                             # model zwarte voeg y~54 (scan 53.8-54.6), pas vanaf x28 (deurpost x25)
for y in range(38,44):
    for x in range(10,13):
        if R[y][x]=='b': R[y][x]='a'      # linkerhelft gezicht lichter (model 17-18), geen voeg
# vleugel (los blok links): voegen y46, y51
hl(46,4,7); hl(51,3,6)
for sd in ((5,48),(3,54)): STEEN.append((sd,'b','a','c','abc',(2,47,6,58)))
# rechter onderblok voorkant: 2 voegen (model x36 46-51, y52->53)
vl(36,46,51); hl(52,34,36); hl(53,37,41)
for sd in ((34,48),(39,49),(37,56)): STEEN.append((sd,'b','a','c','abc',(33,44,41,60)))
# ===== 3. BERGWAND: een donker vlak (e) rechts van de terrasranden; terraszijkanten blijven d =====
GRENS={**{y:48 for y in range(10,17)},**{y:49 for y in range(17,20)},**{y:50 for y in range(20,26)},26:53,27:54}
for y,x0 in GRENS.items():
    for x in range(x0,64):
        if R[y][x] in 'cd': R[y][x]='e'
def NAZORG():
    put([(39,18)],'a')   # model 17; los geraakt door de gevelomtrek
    put([(26,26)],'e')   # plank, los d-pixel
# ===== stenen kleuren: licht boven/links, donker onder/rechts; clusters <3 terug naar basis =====
N4=((1,0),(-1,0),(0,1),(0,-1))
def comp(sd,ok,bx):
    st=[sd]; seen={sd}
    while st:
        x,y=st.pop()
        for dx,dy in N4:
            q=(x+dx,y+dy)
            if q not in seen and bx[0]<=q[0]<=bx[2] and bx[1]<=q[1]<=bx[3] and R[q[1]][q[0]] in ok: seen.add(q); st.append(q)
    return seen
def clusters(S):
    S=set(S); out=[]
    while S:
        p=S.pop(); c={p}; st=[p]
        while st:
            x,y=st.pop()
            for dx,dy in N4:
                q=(x+dx,y+dy)
                if q in S: S.discard(q); c.add(q); st.append(q)
        out.append(c)
    return out
for sd,base,li,dk,ok,bx in STEEN:
    C=comp(sd,ok,bx)
    if len(C)>60: print('WAARSCHUWING groot vlak',sd,len(C))
    for x,y in C: R[y][x]=base
    xs=[p[0] for p in C]; ys=[p[1] for p in C]; xa,xb,ya,yb=min(xs),max(xs),min(ys),max(ys)
    fx=lambda x:(x-xa)/max(1,xb-xa); fy=lambda y:(y-ya)/max(1,yb-ya)
    # licht: bovenrand in de linker 65%, linkerrand in de bovenste 65%; donker: onderrand in de rechter 65% (geen donkere rechterrand: gaf dubbele verticale lijnen)
    L=[(x,y) for x,y in C if ((x,y-1) not in C and fx(x)<=0.65) or ((x-1,y) not in C and fy(y)<=0.65)]
    D=[(x,y) for x,y in C if dk and ((x,y+1) not in C and fx(x)>=0.35) and (x,y) not in L]
    for grp,ch in ((L,li),(D,dk)):
        for c in clusters(grp):
            if len(c)>=3:
                for x,y in c: R[y][x]=ch
# nazorg: losse clusters < 3 px die de steenverdeling achterliet
put([(10,44),(5,52),(6,52)],'a')
NAZORG()
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
