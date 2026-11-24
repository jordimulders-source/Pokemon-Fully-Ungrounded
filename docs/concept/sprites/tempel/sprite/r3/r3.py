# r3.py: reparaties van de coördinator op r2 (raster_r2.txt -> raster.txt). Ogen, deur en latei onaangeroerd.
import sys
R=[list(l.rstrip('\n')) for l in open('raster_r2.txt')][:64]
def row(y,x0,s):
    for i,ch in enumerate(s):
        if ch!=' ': R[y][x0+i]=ch
FROZEN=lambda x,y: (12<=x<=26 and 37<=y<=43) or (11<=x<=27 and 44<=y<=60)
# --- 2. GEVELS, gemeten op het model (tonen.py: mediaanhelderheid + lijnfractie per spritepixel) ---
# bovenste doos: linkergevel licht 39-40, dakplaat donker, gedeelde rand (44,4)->(42,9), rechtergevel licht, donkere dakplaat 47-51
row(4,41,'ddd+aaaddd')
row(5,40,'dddd+aadddd')
row(6,40,'bdd+aaaddddd')
row(7,40,'bdd+aaaadddd')
row(8,39,'bdd+aaaaddddd')
row(9,38,'bbbd+bbbbddddd')
# bovenste linkergevel (raampje 31,14-15)
row(10,31,'addd+')
row(11,31,'aaddd+')
row(12,30,'aaaadd+')
row(13,30,'aaaaddd+')
row(14,29,'bb+bbddd+')
row(15,29,'bb+bbbee+')
# onderste gevels (L: raampje 21,24-25; R: raampje 33,24-25) + muur ertussen
row(19,21,'adddd+bbbbbbb+++++')
row(20,21,'adddee+bbbbb+adddd+')
row(21,20,'aaaddeee+bbb+aadddd+')
row(22,20,'abbddeee+bbb+aaadddd+')
row(23,19,'bbbbbdeeee+d+aabbdddd+')
row(24,19,'bb+bbddeee+d+a+bbbdddd+')
row(25,19,'bb+bbbdeee+d+b+bbbdddd+')
row(26,20,'bbbbbdeeee++bbbbbbddd+')
# --- 3. terras-bovenvlakken als lichte strook ---
for y,x0,x1 in ((11,37,47),(17,25,34),(28,17,26)):
    for x in range(x0,x1+1):
        if R[y][x] in 'bc': R[y][x]='a'
# kistje: rechterdeel in schaduw (model 10)
row(16,42,'ddd')
# --- 4. rechter buitenrand: regelmatige diagonaal op de modelrand (55.2@9 -> 62.9@47) ---
inside=lambda x,y: R[y][x]!='.'
for y in range(9,48):
    last=int(55.3+0.2025*(y-9)-0.45)
    cur=max(x for x in range(64) if inside(x,y))
    for x in range(last+1,64): R[y][x]='.'
    for x in range(cur,last+1):
        if R[y][x] in '.X+': R[y][x]=R[y][x-1] if R[y][x-1] not in '.X+' else 'e'
# buitenlijn opnieuw: elke rand-pixel X, oude buitenlijnpixels die binnen vallen -> buurtint
M=[[R[y][x]!='.' for x in range(64)] for y in range(64)]
edge=lambda x,y: M[y][x] and any(not(0<=x+dx<64 and 0<=y+dy<64) or not M[y+dy][x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
for y in range(64):
    for x in range(64):
        if M[y][x] and edge(x,y): R[y][x]='X'
        elif M[y][x] and R[y][x]=='X' and x>=50:
            nb=[R[y][x-1],R[y-1][x],R[y+1][x]]; R[y][x]=next((c for c in nb if c in 'abcde'),'e')
# selout van r2 ('+' op de buitenrand) eerst terug naar X
for y in range(64):
    for x in range(64):
        if R[y][x]=='+' and edge(x,y): R[y][x]='X'
# --- 1. BINNENLIJNEN in de donkerste tint van het vlak (niet in ogen/deur/latei, niet in raampjes) ---
RAMEN={(31,14),(31,15),(21,24),(21,25),(33,24),(33,25)}
T='abcdemn'; tone={'a':0,'b':1,'c':2,'d':3,'e':4,'m':1,'n':3}
new={}
for y in range(64):
    for x in range(64):
        if R[y][x]!='+' or FROZEN(x,y) or (x,y) in RAMEN: continue
        nb=[tone[R[y+dy][x+dx]] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if R[y+dy][x+dx] in tone]
        if not nb: continue
        t=min(nb)
        new[(x,y)]= 'd' if t<=1 else ('e' if t<=3 else '+')
for (x,y),c in new.items(): R[y][x]=c
# --- 5. selout: buitenlijn aan de lichtkant (linksboven) in de donkerste steentint e ---
for y in range(64):
    for x in range(64):
        if R[y][x]!='X' or FROZEN(x,y): continue
        nx=ny=0
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy,xx=y+dy,x+dx
                if not(0<=yy<64 and 0<=xx<64) or not M[yy][xx]: nx+=dx; ny+=dy
        if (nx+ny)<0 and nx<=0 and ny<=0: R[y][x]='e'
for x,y in ((27,27),(55,33),(42,53)):
    if R[y][x]=='+': R[y][x]='e'  # losse zwarte punt tussen donkere lijnen
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
