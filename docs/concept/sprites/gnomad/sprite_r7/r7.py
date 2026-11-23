# r7.py A|B: vanaf r6. Alleen de riem rechts van de gesp (x24-40): (1) boven- en onderrand buigen weer met de bol mee
# (Gen 3-trapjes 4-5-4-3 die korter worden naar de flank), aansluitend op rij 44 naast de gesp (geen sprongetje);
# (2) aan het rechteruiteinde lopen de zwarte riemlijnen door tot in de buitenlijn; geen gaten of losse pixels.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r1'); from gemeen import opslaan
VAR=sys.argv[1]
R1='../sprite_r1/'
zone=np.load(R1+'zone_af.npy'); L=np.load(R1+'lijn.npy'); riem1=np.load(R1+'riem.npy')
zone[43,26]=5; L[43,26]=False
im=Image.open('../sprite_r6/gnomad_%s.png'%VAR); pal=[tuple(im.getpalette()[3*k:3*k+3]) for k in range(16)]
r6=np.asarray(im).astype(int); o=r6.copy()
cx,cy,rx,ry=27.0,45.5,14.0,8.5
l=np.array([-0.55,-0.6,0.58]); l/=np.linalg.norm(l)
def I(X,Y):
    nx=(X+0.5-cx)/rx; ny=(Y+0.5-cy)/ry; r2=nx*nx+ny*ny
    n=np.array([nx,ny,np.sqrt(max(0.04,1-min(r2,0.96)))]); n/=np.linalg.norm(n); return float(n@l)
def top(X):            # bovenlijn van de riem
    if X<=27: return 44
    if X<=32: return 43
    if X<=36: return 42
    return 41
B=3
fg=o>0
body=(np.isin(zone,(5,8))|riem1)&~L
ZONE=np.zeros((64,64),bool); ZONE[38:52,24:42]=True
for X in range(24,42):
    t=top(X)
    for Y in range(38,52):
        if not fg[Y,X]: continue
        rand=not body[Y,X]                       # buitenlijn van het lijf
        if t<=Y<=t+B+1:
            if rand or Y in (t,t+B+1): o[Y,X]=1   # riemlijnen lopen door tot in de buitenlijn; band op de buitenlijn = zwart
            else: o[Y,X]=14 if (Y==t+1 and X<=21) else 15
        elif not body[Y,X]: continue              # rest van de buitenlijn ongemoeid
        elif Y<t:
            o[Y,X]=8 if I(X,Y)>=0.30 else 7
        elif Y==t+B+2: o[Y,X]=10 if X<30 else 9
        else:
            i=I(X,Y); o[Y,X]=11 if i>=0.25 else (10 if i>=-0.25 else 9)
# buitenlijn rechtsonder direct onder de riem: zwart (schaduwkant), zodat de onderlijn naadloos in de omtrek overgaat
for X in range(30,42):
    Y=top(X)+B+2
    if fg[Y,X] and not body[Y,X] and o[Y,X]==9: o[Y,X]=1
# Jordi: "op de andere 2 hoeken ook 1 zwarte pixel weg" -> alle 4 gesphoeken gelijk afgerond. A had alleen rechts de hoeken weg (trapezium):
# linksboven (18,43) -> lijftint, linksonder (18,49) -> broek in schaduw (zoals de rij onder de riem). B had al 4 hoeken weg.
if VAR=='A':
    o[43,18]=8 if I(18,43)>=0.30 else 7
    o[49,18]=10
    ZONE[43,18]=ZONE[49,18]=True
d=o!=r6
assert not (d&~ZONE).any()
opslaan(o,'gnomad_%s.png'%VAR,pal)
print(VAR,'diff t.o.v. r6: %d px (alleen riem rechts van de gesp + roze/blauw/buitenlijn eromheen), elders 0'%d.sum())
