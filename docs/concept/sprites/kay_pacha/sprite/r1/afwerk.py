# Kay Pacha r1: technische opschoning van de kale reductie (kaal.npy) + oog (Jordi). Silhouet blijft gelijk.
# Run vanuit docs/concept/sprites/kay_pacha na bouw.py:  python3 sprite/r1/afwerk.py
import numpy as np; from PIL import Image
D='sprite/r1/'
K0=np.load(D+'kaal.npy'); S=K0.copy(); PAL=[tuple(c) for c in np.load(D+'pal.npy')]
# indexen: 1 zwart | groen 2 donker 3 midden 4 licht | goud 5 lijn 6 schaduw 7 midden 8 licht
#          creme 9 lijn donker 10 lijn 11 schaduw(tan) 12 licht | 13 paars | 14 wit (oog) | 15 oogpaars
GROEP={2:'g',3:'g',4:'g',5:'y',6:'y',7:'y',8:'y',9:'c',10:'c',11:'c',12:'c',13:'p'}
SELOUT={'g':2,'y':5,'c':9,'p':2}
log={}
def zet(x,y,v,why):
    if S[y,x]!=v: log.setdefault(why,[]).append((x,y,int(S[y,x]),v)); S[y,x]=v
fg=S>0
def tr(x,y): return not(0<=x<64 and 0<=y<64) or not fg[y,x]
# 4. pootjes: zwarte pixels die in het model donkergroene teenlijnen/teenvlak zijn (gemeten L 71-119, rgb ±(60-110,90-145,59-103)) -> donkergroen
for (x,y) in [(9,56),(12,56),(13,56),(12,57),            # linker voorpoot
              (37,54),(35,55),(37,55),(35,56),(37,56),    # verre voorpoot (teenlijn x36 blijft)
              (24,61),(25,61),(27,61),                    # nabije voorpoot
              (49,57)]:                                   # achterpoot
    assert S[y,x] in (1,2),(x,y,S[y,x]); zet(x,y,2,'pootjes: zwart -> donkergroen (model)')
# 5. bek: zwart waar het model donkere cremelijn/tan is (gemeten L 103-155, rgb ±(115-172,110-161,85-132)); bekstreep/kaaklijn (L<=91) blijft zwart
for (x,y,v) in [(6,21,9),(10,21,10),(4,22,9),(5,22,9),(6,22,9)]:
    assert S[y,x] in (1,9),(x,y,S[y,x]); zet(x,y,v,'bek: zwart -> cremelijn (model)')
# 1. buitenlijn: richting van de rand = som van de transparante buren in 5x5 (gewogen 1/afstand^2);
#    wijst hij naar rechtsonder (schaduwkant, nx+ny>=0) -> zwart; naar linksboven (lichtkant) -> selout in de donkerste eigen tint
#    (ook waar het model daar zwart heeft: Gen 3-eis "zwart alleen aan de schaduwkant")
def groep_van(x,y):
    nb=[S[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and 0<=x+dx<64 and 0<=y+dy<64 and S[y+dy,x+dx] in GROEP]
    if S[y,x] in GROEP: return GROEP[S[y,x]]
    return GROEP[max(set(nb),key=nb.count)] if nb else None
K1=S.copy()
for y in range(64):
    for x in range(64):
        if not fg[y,x]: continue
        if not any(tr(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): continue
        nx=ny=0.0
        for dy in range(-2,3):
            for dx in range(-2,3):
                if (dx or dy) and tr(x+dx,y+dy): w=1/(dx*dx+dy*dy); nx+=dx*w; ny+=dy*w
        if nx+ny>=0: zet(x,y,1,'buitenlijn zwart (schaduwkant)')
        else:
            if K1[y,x]==13 and y<25: continue        # ver oog (paars) aan de koprand: modelpixel, blijft
            g=groep_van(x,y)
            if not g: continue
            inn=[K1[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if not tr(x+dx,y+dy) and not any(tr(x+dx+ex,y+dy+ey) for ex,ey in((1,0),(-1,0),(0,1),(0,-1)))]
            if inn and inn.count(SELOUT[g])*2>=len(inn): continue   # vulling is al de donkerste tint (verre poot): modelzwart blijft, anders open rand
            zet(x,y,SELOUT[g],'buitenlijn selout (lichtkant)')
# 1a. verre voorpoot: bovenrand van de voet; selout = vulkleur (donkergroen) gaf een open rand -> zwart zoals het model (L 77)
for (x,y) in [(35,53),(34,54)]:
    assert S[y,x]==2; zet(x,y,1,'verre poot: open rand -> zwart (model)')
# 1b. geen losse selout tussen zwart op één rand
f2=S>0
for y in range(64):
    for x in range(64):
        if S[y,x] in (2,5,9) and any(tr(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
            nb=[S[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and 0<=x+dx<64 and 0<=y+dy<64 and f2[y+dy,x+dx] and any(tr(x+dx+ex,y+dy+ey) for ex,ey in((1,0),(-1,0),(0,1),(0,-1)))]
            if nb.count(1)>=2 and not any(v in (2,5,9) for v in nb): zet(x,y,1,'rand: losse selout tussen zwart -> zwart')
# 2. losse zwarte pixels binnenin (geen zwarte 8-buur, niet aan de rand) -> meest voorkomende 4-buur
for y in range(1,63):
    for x in range(1,63):
        if S[y,x]!=1 or any(tr(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): continue
        nb8=[S[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy)]
        if 1 not in nb8:
            nb=[S[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1))]; zet(x,y,max(set(nb),key=nb.count),'losse zwarte pixel')
# 3. ontkorrelen: alleen enkele vul-pixels (geen gelijke 4-buur) waar >=3 van 4 buren één andere tint van dezelfde groep zijn
VUL={3,4,6,7,8,11,12}
for y in range(1,63):
    for x in range(1,63):
        v=S[y,x]
        if v not in VUL: continue
        nb=[S[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1))]
        if v in nb: continue
        best=max(set(nb),key=nb.count)
        if nb.count(best)>=3 and best in VUL and GROEP[best]==GROEP[v]: zet(x,y,best,'ontkorrelen (1-px tintvlekje)')
basis=S.copy()
# 4. oog (Jordi): rij wit-paars-wit + 2e wit boven de rechtse witte (+ variant A: 2e paars boven het paars); modelplek natief x43-49,y62-66 -> sprite (9-11, 17-18)
WIT=(248,243,237); OOGPAARS=(150,88,155)   # gemeten: modelwit fa f4 f0/f9 f4 e9/fb f4 e8/f3 f0 e8; oogpaars mediaan 8c5598/915496/925597/995c9e/ab6bb3
PAL=PAL+[WIT,OOGPAARS]
def oog(A):
    T=basis.copy(); ch=[]
    for (x,y,v) in [(9,18,14),(10,18,15),(11,18,14),(11,17,14)]+([(10,17,15)] if A else []):
        ch.append((x,y,int(T[y,x]),v)); T[y,x]=v
    return T,ch
def save(arr,name):
    im=Image.fromarray(arr.astype('uint8'),'P'); p=[]
    for c in PAL: p+=list(c)
    im.putpalette(p); im.save(D+name,transparency=0)   # palet precies 16 (of minder) kleuren
A,chA=oog(True); B,chB=oog(False)
save(A,'kay_pacha_r1_A.png'); save(B,'kay_pacha_r1_B.png'); np.save(D+'A.npy',A); np.save(D+'B.npy',B)
assert ((A>0)==(K0>0)).all() and ((B>0)==(K0>0)).all(), 'silhouet gewijzigd'
tot=0
for k,v in log.items(): print(f'{k}: {len(v)} px'); tot+=len(v)
print('oog A',chA); print('oog B',chB)
print('afwijking t.o.v. kale reductie: opschoning',tot,'+ oog',len(chA),'(A) /',len(chB),'(B); figuur',int((K0>0).sum()),'px')
print('kleuren A',len(np.unique(A)),'B',len(np.unique(B)),'palet',len(PAL))
import json; json.dump({k:v for k,v in log.items()},open(D+'afwijkingen.json','w'),default=int)
