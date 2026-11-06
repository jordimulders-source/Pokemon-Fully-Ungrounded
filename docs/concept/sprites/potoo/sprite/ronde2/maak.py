"""Ronde 2 (met de hand): grotere koepel, haak 2 px langer, kin loopt over de kaakrand door (geen losse kaaklijn),
gevouwen vleugel als eigen donkere vorm (boeg, dekveren in rijen, getrapte pennen, vleugelpunt in het silhouet),
staart met veerpunten, ruige randen, meer waardebereik."""
import sys
G=[['.']*64 for _ in range(64)]
def R(y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': G[y][x0+i]=c
def P(pts,c):
    for x,y in pts: G[y][x]=c
SH={'a':[(0,0),(1,0),(1,1)],'b':[(1,0),(1,1),(0,1)],'c':[(0,0),(0,1),(1,1)],'v':[(0,0),(0,1),(0,2)],'h':[(0,0),(1,0),(2,0)]}
def M(lst,c,ok):
    for x,y,k in lst:
        for dx,dy in SH[k]:
            if G[y+dy][x+dx] in ok: G[y+dy][x+dx]=c
# ---------- randen ----------
WB={9:38,10:39,11:40,12:41,13:42,14:43,15:44,16:44,17:45,18:45,19:46}
WB.update({y:46 for y in range(20,37)}); WB.update({y:45 for y in range(37,45)}); WB.update({y:44 for y in range(45,53)})
WF={20:35,21:34,22:33,**{y:32 for y in range(23,29)},**{y:31 for y in range(29,39)},39:32}
WL={40:32,41:33,42:33,43:34,44:35,45:35,46:36,47:37,48:37,49:38,50:39,51:40,52:41}
L={**{y:22 for y in range(30,39)},39:23,40:24,41:25,42:26,43:27,44:28,45:29,46:30,47:31,48:32,**{y:33 for y in range(49,60)}}
# ---------- mantel ----------
for y in range(9,19):
    for x in range(37,WB[y]+1): G[y][x]='1' if x==WB[y] else ('3' if x>=WB[y]-2 else '4')
# ---------- vleugel ----------
for y in range(17,53):
    xb=WB[y]
    if y<20: xa={17:41,18:38,19:36}[y]
    else: xa=WF.get(y) or WL[y]
    for x in range(xa,xb+1):
        if x==xb: c='1'
        elif x==xa: c='2' if (y<40 or x<=40) else '1'
        elif x<=xa+(2 if y<23 else 1) and 20<=y<40: c='4'
        elif x>=xb-2: c='F'
        else: c='3'
        G[y][x]=c
P([(38,18),(39,18),(40,18),(41,17),(42,17),(43,17)],'2')   # bovenrand vleugel (schouderveren)
P([(42,53),(43,53)],'1')                                    # vleugelpunt
# dekveren: rijen lichte veerranden, dekverengrens, pennen met veerlijnen
# twee rijen dekveren: schuine veerrand (2) met licht (4) eronder, opgaand naar de rug
for pts in ([(33,27),(34,27),(35,26),(36,26),(37,26),(38,25),(39,25),(40,25),(41,24),(42,24),(43,23)],
            [(33,31),(34,31),(35,30),(36,30),(37,30),(38,29),(39,29),(40,29),(41,28),(42,28),(43,27)]):
    for x,y in pts:
        if G[y][x] in '34': G[y][x]='2'
        if G[y+1][x] in '3' and x<=40: G[y+1][x]='4'
P([(32,35),(33,35),(34,35),(34,34),(35,34),(36,34),(37,34),(37,33),(38,33),(39,33),(40,33),(40,32),(41,32),(42,32),(43,32)],'2')
P([(35,y) for y in range(36,42)]+[(36,y) for y in range(42,44)],'2')
P([(38,y) for y in range(35,41)]+[(39,y) for y in range(41,49)],'2')
P([(41,y) for y in range(33,41)]+[(42,y) for y in range(41,52)],'2')
# ---------- borst + staart ----------
for y in range(30,60):
    xl=L[y]; xe=(WF.get(y) or WL.get(y) or 41)-1
    if y>=53: xe=40
    for x in range(xl,xe+1):
        if x==xl: c='2' if y<57 else '1'
        elif y>=46 and x>=33:
            d=x-33; c='5' if d<=2 else ('4' if d<=4 else '3')
            if x==40 and y>=53: c='1'
        else:
            c='6' if x-xl<=2 and y<44 else ('4' if (y>=42 and x>=xe-1) or y>=45 else '5')
        G[y][x]=c
R(59,33,"15544331")
R(60,33,"15144131"); R(61,34,"1 11 1")
# ---------- kop ----------

R(1,24,"2222111")
R(2,22,"226666555111")
R(3,21,"2666666655541")
R(4,20,"266666666555441")
R(5,19,"26666666665554441")
R(6,19,"266668888555554441")
R(7,18,"26645888888555544431")
R(8,18,"26445888888555544431")
R(9,18,"2664588888855554443")
R(10,18,"2666588888855554443")
R(11,18,"2666558888555554443")
R(12,16,"11266"+"5"*12+"4443")
R(13,16,"1446"+"5"*13+"4443")
R(14,15,"1E4E"+"5"*14+"4443")
R(15,15,"1EEEE"+"1"*10+"555"+"4443")
R(16,15,"1EAAAA9999999AA11544 43".replace(' ',''))
R(17,15,"1EAAAAAA999AAA99D12243")
R(18,15,"1EAAAAAAA9AAAA9DD55523")
R(19,16,"1EAAAAAA9AAAA9DD55552")
R(20,17,"11DAAAA9AAA9DD5555")
R(21,17,"2DBAAAAAAAA9DD555")
R(22,17,"2DBAAAAAAA9DD555")
R(23,17,"2DBBAAAAAA9DD55")
R(24,18,"2DBBBAAA9DD555")
R(25,18,"2DBCCCC9DD5555")
R(26,19,"1DCCC9DD55555")
R(27,20,"1DC9DD455555")
R(28,21,"1EEE4455555")
R(29,22,"111444555")
R(30,22,"24444555")
R(31,22,"2665555")
# ---------- ruige randen (veerpuntjes van 1 px) ----------
for ys,dx in (((12,13),1),((26,27),1),((38,39),1)):
    for y in ys: xr=WB[y]; G[y][xr]='3' if y<19 else 'F'; G[y][xr+1]='1'
G[11][41]='1'
for y in (34,35): G[y][21]='2'; G[y][22]='6'
P([(33,28),(34,28),(33,39)],'3')
# ---------- patroon ----------
M([(37,11,'a'),(39,13,'a'),(37,15,'h'),(38,17,'h')],'7','34')
P([(43,15),(43,16)],'3')       # mantel: streepjes in rijen
M([(40,37,'v'),(37,40,'v'),(40,43,'v'),(43,36,'v')],'F','34')          # pennen
M([(34,50,'c'),(36,54,'a'),(35,57,'c')],'7','45')                                               # staart
M([(26,37,'b')],'4','56')                                                           # borst: rustig
open(sys.argv[1] if len(sys.argv)>1 else 'raster.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
