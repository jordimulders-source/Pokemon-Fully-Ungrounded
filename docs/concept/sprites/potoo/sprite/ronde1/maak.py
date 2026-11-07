"""Ronde 1: tekstraster met de hand. Kop/snavel/muil als letterlijke rijen; mantel/lijf uit handgekozen randen en tintbanden; daarna handgeplaatste details."""
import sys
G=[['.']*64 for _ in range(64)]
def R(y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': G[y][x0+i]=c
def P(pts,c):
    for x,y in pts: G[y][x]=c
# ---- rechterrand (rug/mantel/staart) ----
RE={8:36,9:37,10:38,11:39,12:40,13:41,14:42,15:42,16:43,17:43,18:44,19:44}
RE.update({y:45 for y in range(20,35)}); RE.update({y:44 for y in range(35,41)}); RE.update({y:43 for y in range(41,44)})
RE.update({y:42 for y in range(44,47)}); RE.update({y:41 for y in range(47,50)}); RE.update({y:40 for y in range(50,61)})
# ---- kop, snavel, muil (letterlijk) ----
R(3,24,"2222211")
R(4,22,"22666665511")
R(5,21,"2666666655541")
R(6,20,"266668888555441")
R(7,20,"2666888888554431")
R(8,19,"266448888885544331")
R(9,19,"2644588888855544441")
R(10,19,"26665888888555544431")
R(11,19,"266655888855555444331")
R(12,18,"2665555555555555443")
P([(16,12),(17,12)],'1')
R(13,15,"1FF55555555555555555443443 1".replace(' ',''))
R(14,14,"1EFE"+"1"*10+"5555554443443"+"31")
R(15,14,"1EEAAA9999999911115554434433 1".replace(' ',''))
R(16,14,"1EAAAAAAA99999A99D1224434443 31".replace(' ',''))
R(17,15,"1EAAAAAAA999AAA9DD55243444331")
R(18,16,"11AAAAAAA9AAAA9DD55443444333 1".replace(' ',''))
R(19,18,"2DAAAAA9AAAA9DD5544")
R(20,17,"2DBAAAAA9AAA9DD5544")
R(21,17,"2DBAAAAAAAAA9DD5544")
R(22,17,"2DBAAAAAAAAA9DD4543")
R(23,17,"2DBBAAAAAAA9DD4442")
R(24,18,"2DBBBBBAAA9DD441")
R(25,18,"2DBBCCCBA9DD4441")
R(26,19,"1DBCCCBB9DD331")
R(27,20,"1DBBBB9DD331")
R(28,21,"1DBB9DD331")
R(29,22,"1D9DD331")
R(30,23,"1EEE1")
R(31,24,"111")
# mantel/borsttop automatisch: lege cellen rechts van de kop tot de rugrand
for y in range(4,32):
    xr=RE.get(y)
    if xr is None: continue
    xs=max(x for x in range(64) if G[y][x]!='.')+1 if y<12 else None
    row=G[y]; last=max(x for x in range(64) if row[x]!='.')
    if last>=xr: continue
    first=True
    for x in range(last+1,xr+1):
        if x==xr: c='1'
        elif (x-last)<= (2 if y>=24 else 1) and y>=20: c='3'
        elif y>=29 and x==32: c='2'
        elif x>=xr-3: c='3'
        else: c='4'
        row[x]=c; first=False
# ---- lijf (letterlijk, per rij vanaf x) ----
R(28,31,"3"+"4"*10+"333"+"1")
R(29,30,"33"+"2"+"55"+"4"*7+"333"+"1")
R(30,28,"3344"+"2"+"55"+"4"*7+"333"+"1")
R(31,27,"33"+"44"+"2"+"55"+"4"*8+"333"+"1")
XL={32:23,**{y:24 for y in range(33,41)},41:25,42:25,43:26,44:27,45:28,46:29,47:30,48:31,49:32,50:32,**{y:33 for y in range(51,61)}}
XW={**{y:31 for y in range(32,41)},41:32,42:32,43:33,44:33,45:34,46:34,47:35,48:35,49:36,50:36,51:37,52:37,53:38,54:38,55:39}
BR={32:"4445555",33:"665555",34:"665555",35:"664555",36:"664455",37:"665555",38:"665555",39:"665555",40:"665545",
    41:"664455",42:"665555",43:"665555",44:"65555",45:"55555",46:"5555",47:"5555",48:"555",49:"555",50:"555",
    51:"555",52:"555",53:"5544",54:"5544",55:"55444"}
for y in range(32,61):
    xl,xr=XL[y],RE[y]; row=G[y]
    for x in range(64): row[x]='.' if x<xl or x>xr else row[x]
    row[xl]='2' if y<58 else '1'; row[xr]='1'
    if y in XW:
        xw=XW[y]; br=BR[y]; assert len(br)==xw-xl-1,(y,len(br),xw-xl-1)
        for i,c in enumerate(br): row[xl+1+i]=c
        row[xw]='2'
        for x in range(xw+1,xr):
            row[x]='3' if x>=xr-3 else ('5' if x<=xw+2 and y<43 else '4')
    else:
        t={56:"554433",57:"554433",58:"554433",59:"544433",60:"444333"}[y]
        for i,c in enumerate(t): row[xl+1+i]=c
# staart waaiert onderaan iets uit (y58-60 1 px breder aan beide kanten), middenveer-lijn
for y,t in ((58,"1555443331"),(59,"1554443331"),(60,"1444433331")):
    for x in range(64): G[y][x]='.'
    for i,c in enumerate(t): G[y][32+i]=c
for x in range(33,41): G[61][x]='1'
P([(37,57),(37,58),(37,59)],'3')
P([(37,16),(37,17)],'4')
# ruige rugrand: veerpuntjes van 2 rijen die 1 px uitsteken
for y in (14,22,30):
    for yy in (y,y+1):
        xr=RE[yy]; G[yy][xr]='3'; G[yy][xr+1]='1'
G[13][42]='1'
# vleugel: dekverengrens en veerlijn (3)
P([(32,38),(33,38),(34,38),(34,37),(35,37),(36,37),(37,37),(37,36),(38,36),(39,36),(40,36),(40,35)],'3')
P([(38,y) for y in range(39,53)],'3')
# schorsstreepjes (7) dicht op mantel/vleugel/staart; ijle tekening (4) op kruin, wang en borst
SH={'a':[(0,0),(1,0),(1,1)],'b':[(1,0),(1,1),(0,1)],'c':[(0,0),(0,1),(1,1)],'v':[(0,0),(0,1),(0,2)],'h':[(0,0),(1,0),(2,0)]}
def M(lst,c,ok='345'):
    for x,y,k in lst:
        for dx,dy in SH[k]:
            if G[y+dy][x+dx] in ok: G[y+dy][x+dx]=c
M([(37,13,'v'),(41,15,'c'),(37,17,'b'),(40,18,'a'),(42,21,'c'),(38,21,'a'),(36,24,'b'),(41,25,'a'),(38,27,'c'),(43,24,'v'),
   (35,29,'a'),(39,28,'b'),(42,29,'c'),(34,33,'a'),(38,32,'c'),(41,32,'v'),
   (36,40,'c'),(40,39,'v'),(36,44,'c'),(39,43,'a'),(39,47,'v'),(34,52,'c'),(35,57,'c')],'7')
M([(31,5,'v'),(22,5,'a'),(34,12,'c')],'4',ok='56')
open(sys.argv[1] if len(sys.argv)>1 else 'raster.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
