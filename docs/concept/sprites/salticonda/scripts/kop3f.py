"""Salticonda kleurronde 3f: kleur3e met de shading van de kop gelijkgetrokken met het lijf, en de overgang kop -> halsband -> winding.
Alleen tinten; het silhouet blijft (alpha-diff 0 met 3e). Zones: KOP (schaduwkant kuif rechts) en OVERGANG (slagschaduw op de bovenste winding).
Bevroren: vorm/naden van de kuif (g blijft g), neus en neusgaten, oog, wenkbrauw, gezicht, wang, halsband, rest van het lijf."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'; I=CH.index
DONKER={'a':'b','b':'c','c':'d','d':'e','e':'e'}
def kuifmasker(x,y): return y<20 and ((y<=5 and x>=13) or (6<=y<=9 and x>=21) or (y>=10 and x>=34))
def vast(x,y): return (21<=x<=33 and 7<=y<=9) or (23<=x<=30 and y==6) or (25<=x<=27 and y==5) or (20<=x<=33 and 10<=y<=15) or (33<=x<=36 and 9<=y<=19)
def build(log=None):
    E=Image.open(D+'kleur3e/salticonda.png'); P=E.load(); out=E.copy(); Q=out.load()
    zones={'kop':[],'overgang':[]}
    # 1) kop: schaduwkant rechts net zo diep als op de windingen (daar is het rechter ~40% d/e).
    #    Per rij: vanaf 66% van de kopbreedte 1 tint donkerder, vanaf 86% nog een tint (naden g en omlijning blijven).
    for y in range(5,20):          # rij 0-4 = lichte bovenkant van de koepel: blijft licht
        xs=[x for x in range(48) if P[x,y]!=0]; L,R=min(xs),max(xs)
        for x in range(L,R+1):
            v=CH[P[x,y]]
            if v not in DONKER or not kuifmasker(x,y) or vast(x,y): continue
            f=(x-L)/(R-L)
            n=v
            if f>=0.66: n=DONKER[n]
            if f>=0.86: n=DONKER[n]
            if n!=v: Q[x,y]=I(n); zones['kop'].append((x,y))
    # 2) overgang: slagschaduw van kaak en halsband op de bovenste winding (rij 26, onder de band), 1 tint;
    #    links blijft het hooglicht van de winding (licht van linksboven), naar rechts loopt hij op in de schaduwkant.
    for x in range(15,31):
        v=CH[P[x,26]]
        if v in DONKER and DONKER[v]!=v: Q[x,26]=I(DONKER[v]); zones['overgang'].append((x,26))
    return out,zones
if __name__=='__main__':
    im,z=build(); im.save(D+'kleur3f/salticonda.png',transparency=0); Q=im.load()
    open(D+'kleur3f/salticonda_raster.txt','w').write('\n'.join(''.join(CH[Q[x,y]] for x in range(64)) for y in range(64))+'\n')
    print({k:len(v) for k,v in z.items()})
