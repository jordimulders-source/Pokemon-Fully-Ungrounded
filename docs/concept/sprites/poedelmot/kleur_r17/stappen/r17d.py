# r17d: crème-groep max 3 tinten (A, 7, D) + lijnen 5/4/3/2: schaduw-6 in de vacht/dons -> D, B2-dons 8 -> D.
# 6 blijft alleen voor de tan plaatjes (x34-45, y44-53) en de oogring (x28-34, y31-41); 8/9 alleen in het middenstuk.
import os
H=os.path.dirname(os.path.abspath(__file__))
R=[list(l.rstrip('\n')) for l in open(os.path.join(H,'basis.txt'))]
import importlib
for m in ('r17a','r17b','r17c'):
    for y,v in importlib.import_module(m).W.items():
        for x0,s in v:
            for i,c in enumerate(s):
                if c!='=': R[y][x0+i]=c
Z=set(tuple(map(int,l.split(','))) for l in open(os.path.join(H,'..','spriet_zone.txt')))
W={}
for y in range(64):
    for x in range(64):
        c=R[y][x]
        if c=='6' and (x,y) not in Z and not (34<=x<=45 and 44<=y<=53) and not (28<=x<=34 and 31<=y<=41):
            W.setdefault(y,[]).append((x,'D'))
        if c=='8' and x<=30 and y>=55:
            W.setdefault(y,[]).append((x,'D'))
