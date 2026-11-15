# v12 = v11 + (15 nov): de lichte strook waar de spiraal zat liep als bijna verticale wig omlaag (x30-40, y30-41).
# Jordi vroeg "het reguliere golfpatroon": banden liggend, licht gebogen met de bol mee (aan de rechterkant lopen de
# banden licht omhoog, zie de onderband rij 43-48 en de bovenband rij 22-29), met golvende randen.
# Nu: de verticale l-wig wordt m (middenband); door de middenband loopt één liggende lichte band (l) van naast het
# gezicht (x31) tot vlak voor de schaduwkant (x44), 4-5 rijen breed zoals de lichte banden elders, golvende randen met
# trapjes van 1-3 px, rechts taps. Alleen x 30-48, y 26-44; diff erbuiten = 0 (gemeten).
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
V11=[l.rstrip('\n') for l in open(D+'../sprite_v11/raster.txt')][:64]
R=[list(r) for r in V11]; log=[]
def zone(x,y): return 30<=x<=48 and 26<=y<=44
def zet(x,y,c,reden):
    assert zone(x,y)
    if R[y][x]!=c: log.append(f'({x},{y}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
# boven- en onderrand (eerste en laatste l-rij) per kolom
top={31:33,32:33,33:33,34:32,35:32,36:32,37:31,38:32,39:32,40:32,41:31,42:31,43:31,44:32}
bot={31:37,32:37,33:37,34:37,35:36,36:36,37:36,38:36,39:36,40:36,41:35,42:35,43:34,44:33}
for y in range(29,43):
    for x in range(30,48):
        if R[y][x] not in 'lm': continue
        c='l' if x in top and top[x]<=y<=bot[x] else 'm'
        zet(x,y,c,'liggende lichte band' if c=='l' else 'middenband (geen verticale strook)')
open(D+'raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
open(D+'raster.txt.log','w').write('\n'.join(log)+'\n')
print(len(log),'wijzigingen; buiten de zone:',sum(1 for y in range(64) for x in range(64) if V11[y][x]!=R[y][x] and not zone(x,y)))
