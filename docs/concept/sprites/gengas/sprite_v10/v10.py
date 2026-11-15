# v10 = v9 + Jordi (15 nov): spiraal vervangen, "probeer maar 2" = ovale stormvlek zonder spiraal (Grote Rode Vlek):
# liggend ovaal in de band, iets donkerdere rand, lichtere kern, bestaande tinten, geen zwarte omlijning; banden lopen
# er omheen. Twee varianten: a = vlek iets lichter dan de band (rand m/b, vulling l, kern v);
# b = vlek iets donkerder/roder (rand a, vulling b, kern m). Rand alleen donker aan de schaduwkant (rechtsonder);
# aan de lichtkant gaat de vlek met één tintstap over in de band (a: m, b: b), zoals de bandranden elders. Diff buiten x 33-48, y 26-42 = 0 (gemeten).
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
V9=[l.rstrip('\n') for l in open(D+'../sprite_v9/raster.txt')][:64]
# ovaal 11x7 (x37-47, y32-38): r = rand, f = vulling, c = kern (licht van linksboven: kern links/boven van het midden)
OVAAL=['..ttttttt..',     # t = rand lichtkant (linksboven), r = rand schaduwkant (rechtsonder), zoals de bandranden
       '.tfffffffr.',
       'tffccccfffr',
       'tfcccccfffr',
       'rfffcccfffr',
       '.rfffffffr.',
       '..rrrrrrr..']
X0,Y0=37,32
def zone(x,y): return 33<=x<=48 and 26<=y<=42
KLEUR={'a':{'t':'m','r':'b','f':'l','c':'v'},'b':{'t':'b','r':'a','f':'b','c':'m'}}
for v in 'ab':
    R=[list(r) for r in V9]; log=[]
    def zet(x,y,c,reden):
        assert zone(x,y)
        if R[y][x]!=c: log.append(f'({x},{y}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
    # spiraallijn (b) buiten het ovaal -> l: de lichte stroom loopt om de vlek heen (boven rij 31-32, onder rij 39-40)
    for y in range(31,41):
        for x in range(35,47):
            inov = 0<=y-Y0<7 and 0<=x-X0<11 and OVAAL[y-Y0][x-X0]!='.'
            if R[y][x]=='b' and not inov: zet(x,y,'l','spiraallijn weg; lichte stroom om de vlek')
    for j,rij in enumerate(OVAAL):
        for i,c in enumerate(rij):
            if c!='.': zet(X0+i,Y0+j,KLEUR[v][c],f'stormvlek {c}')
    buiten=sum(1 for y in range(64) for x in range(64) if V9[y][x]!=R[y][x] and not zone(x,y))
    open(D+f'raster_v10{v}.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
    open(D+f'raster_v10{v}.txt.log','w').write('\n'.join(log)+'\n')
    print(f'v10{v}: {len(log)} wijzigingen; buiten de zone: {buiten}')
