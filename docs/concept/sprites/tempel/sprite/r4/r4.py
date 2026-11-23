# r4.py: reparaties op r3 (raster_r3.txt -> raster.txt). Alle voegen/randen op gemeten modelplekken (vmap.py/scan.py/tonen.py).
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
# ===== 1. VLAKKEN =====
# 1a gezicht rechts van de deur (x26-31, y45-60); model: voeg y49 (vmap), zwarte voeg y53 (scan 53.8-54.6; r3 had hier al +++), x29 (scan 29.3-29.5, 54-57)
# (zwarte voeg y46 rechts van de latei niet: zou de latei verlengen)
hl(49,26,30); hl(53,26,31); vl(29,54,57)
for sd in ((27,46),(27,51),(27,56),(31,56)): STEEN.append((sd,'b','a','c','abc',(26,45,31,60)))
# gezichtsvlak links van het linkeroog: model toon 17-18 (linkerhelft van het gezicht is lichter) -> a
for y in range(38,44):
    for x in range(10,13):
        if R[y][x]=='b': R[y][x]='a'
# 1b vleugel (x2-6): model voeg y46 x4-7, y51 x3-5 (verticale voeg x5 past niet: vleugel is daar 4 px breed)
hl(46,4,7); hl(51,3,6)
for sd in ((5,48),(3,54)): STEEN.append((sd,'b','a','c','abc',(2,47,6,58)))
# gezicht links van de deur (x7-12): model voeg y51 x9-12 (verticale voeg x11 past niet: 4 px breed)
hl(51,8,12)
for sd in ((10,49),(9,54)): STEEN.append((sd,'b','a','c','abc',(7,48,12,58)))
# 1c rechter onderblok voorkant (x33-41): model x36 (46-52), y53 x34-41, x38 (54-60)
vl(36,46,51); hl(52,34,36); hl(53,37,41); vl(38,54,60)   # scan: x34-36 52.4-52.5, x37-42 53.3-53.7
for sd in ((34,48),(39,49),(36,56),(40,56)): STEEN.append((sd,'b','a','c','abc',(33,44,41,60)))
# ===== 2. RECHTERBOVENVLAK (x42-53, y10-40): zijkanten terraslagen =====
hl(13,48,53)                       # bovenste terras, zijkant: voeg (scan x48-50 ~13.2)
hl(21,45,49)                       # middelste terras, zijkant: voeg (scan x45-49 ~21)
hl(34,42,46); hl(33,47,48); hl(32,49,50)   # onderste terras, zijkant: voeg (scan x44-50 34.2->32.3)
hl(36,45,48); hl(35,49,52)                 # tweede voeg (scan x46-52 36.4->34.9)
vl(46,30,33)
for sd in ((50,11),(50,15)): STEEN.append((sd,'d','c',None,'cd',(48,11,54,16)))
for sd in ((47,18),(47,24)): STEEN.append((sd,'d','c',None,'cd',(45,17,49,26)))
for sd in ((44,31),(48,31),(51,31),(44,35),(50,34)): STEEN.append((sd,'d','c',None,'cd',(41,30,53,37)))
# ===== 3. GEVELZONE: randen van de gevels in de donkerste steentint (model tonen.py: '#'-lijnen en tonen 7-11) =====
# linker onderste gevel: plankrand (26,19)8,(27,20)#8,(28,21)-11,(28,22)#8; rand (29,23)-11,(30,23)11,(30,24)11
put([(26,19),(27,20),(28,21),(28,22)],'e'); put([(29,23)],'d')
# rechter onderste gevel: linkerrand (33,20)#17,(32,21)-15,(32,22)-17,(31,23)-15,(31,24)-15,(30,25)-11; plankrand x39-42 (#15,-10,-15,-10,-15,-10,10)
put([(33,20),(32,21),(32,22),(31,23),(31,24),(30,25)],'e'); put([(31,25)],'b')
put([(39,20),(39,21),(40,22),(40,23),(41,24),(41,25),(42,26)],'e')
# middelste gevel: plankrand (35,10)#11,(36,11)-11,(36,12)-10,(37,13)-11,(37,14)#10,(37,15)-16; plank (33,12)=10
put([(35,10),(36,11),(36,12),(37,13),(37,15)],'e'); put([(33,12)],'d')
# terrasstrook onder de middelste gevel: (34,17) model -17 lijn/licht in de strook -> strook (b)
put([(34,17)],'b')
# ===== 4. TOPGEVELS: binnenlijn rechtergevel (45,4)-11,(44,5)-10,(44,6)-17,(44,7)-16,(43,8)#15,(43,9)-16; dal (42-43,6-7) #10/10 =====
put([(45,4),(44,5),(44,6),(44,7),(43,8),(43,9),(42,6),(43,6),(42,7),(43,7)],'e')
put([(46,4),(47,4)],'a'); put([(40,8)],'b'); put([(31,26)],'e')
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
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
