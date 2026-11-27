# Guarana fase 2, r13 (start r12). Jordi: "je maakt er een zooitje van, alles wat ik omlijnd heb zijn vierkanten, waarom? Fix dat, en blijf
# telkens kijken naar de verhouding, zodat het een stuk fruit aan de tros lijkt" (sprite_r12/jordi_vierkanten.png).
# Per omlijnd oog: een rond oog (wit 2-4-2, pupil 2 px; half dicht = gebogen lid van 2-4 over de bovenkant; klein = wit 2-2 met pupil 1)
# met schil die de ronde vorm volgt (lijnrood links/boven, zwart rechts/onder zoals fase 1), daaromheen een ring vrucht
# (licht linksboven, midden, schaduw rechtsonder) zodat er rondom rood is. Ring alleen op rood; tegen blad/achtergrond wordt de ring buitenlijn.
# Pixels die een ander (niet omlijnd) oog raken worden niet aangeraakt. Vanuit guarana_fase2/: python3 sprite_r13/bouw13.py
import sys; sys.path.insert(0,'sprite_r9'); import numpy as np; from PIL import Image; from gemeen2 import *; from hulp import *
K,L,S,M,H=1,2,3,4,5; W,G=10,11; GROEN=(6,7,8,9)
CH={'L':L,'K':K,'W':W,'S':S,'M':M,'H':H}
OPEN=["..LL..",".LWWL.","LWKKWK",".LWWK.","..KK.."]          # rond oog 2-4-2, pupil midden
OPEN_LO=["..LL..",".LWWL.","LWKWWK",".LKWK.","..KK.."]       # pupil linksonder (2 px, verticaal), wit eromheen
HALF=["..LL..",".LMML.","LWKKWK",".KWWK.","..KK.."]          # half dicht: gebogen lid (vruchthuid met boog lijnrood) over de bovenkant, onderkant rond
KLEIN=[".LL.","LWWK","LKWK",".KK."]                          # klein: wit 3 px, pupil 1 px linksonder
OGEN=[  # naam, (x0,y0), sjabloon
 ('M1 middelste tros rechtsboven',(30,12),OPEN_LO),
 ('H1 middelste tros half dicht oog',(24,14),HALF),
 ('M2 middelste tros links',(21,20),KLEIN),
 ('L2 linkertros boven',(12,22),OPEN_LO),
 ('L1 linkertros links',(7,25),OPEN_LO),
 ('L5 linkertros onder',(14,33),OPEN_LO),
 ('RT rechtertros boven',(45,22),OPEN_LO),
 ('R2 rechtertros rechtsboven',(52,22),OPEN_LO),
 ('R1 rechtertros klein oog links-midden',(42,25),KLEIN),
 ('R5 rechtertros linksonder',(42,32),OPEN_LO),
]
def g(o,y,x): return o[y,x] if ok(y,x) else 0
def maak(src):
    o=np.array(Image.open(src)).astype(int); o0=o.copy()
    kern={}
    for n,(x0,y0),T in OGEN:
        for j,r in enumerate(T):
            for i,c in enumerate(r):
                if c!='.': kern[(x0+i,y0+j)]=(n,CH[c])
    eigen_wit={p for p,(n,v) in kern.items() if v==W}
    boxen=[(x0-1,y0-1,x0+len(T[0]),y0+len(T)) for n,(x0,y0),T in OGEN]
    inbox=lambda x,y: any(a<=x<=c and b<=y<=d for a,b,c,d in boxen)
    # oud wit: een witvlak (8-samenhangend) hoort bij een omlijnd oog als het grootste deel in diens kernvak ligt; ander wit = ander oog
    lab,nl=label((o0==W)|(o0==G),N8); kernvak=[(x0,y0,x0+len(T[0])-1,y0+len(T)-1) for n,(x0,y0),T in OGEN]
    eigen=set()
    for k in range(1,nl+1):
        ys,xs=np.where(lab==k)
        if any(sum(a<=x<=c and b<=y<=d for x,y in zip(xs,ys))*2>len(xs) for a,b,c,d in kernvak): eigen|=set(zip(xs.tolist(),ys.tolist()))
    ander_oog={(x,y) for y in range(64) for x in range(64) if o0[y,x] in (W,G) and (x,y) not in eigen and (x,y) not in kern}
    def raakt_ander(x,y): return any((x+dx,y+dy) in ander_oog for dy,dx in N8)
    # 1 ring vrucht rond elke kern (8-buren van de kern die zelf geen kern zijn), alleen op rood
    for n,(x0,y0),T in OGEN:
        h,w=len(T),len(T[0]); cx,cy=x0+(w-1)/2,y0+(h-1)/2
        for y in range(y0-1,y0+h+1):
            for x in range(x0-1,x0+w+1):
                if (x,y) in kern or not ok(y,x) or o0[y,x] not in (L,S,M,H,K) or (x,y) in ander_oog or raakt_ander(x,y): continue
                if o0[y,x]==K and not any(g(o0,y+dy,x+dx) in (L,S,M,H) for dy,dx in N4): continue
                if not any((x+dx,y+dy) in kern for dy,dx in N8): continue
                t=((x-cx)+(y-cy))
                o[y,x]=H if t<=-3 else (S if t>=3.5 else M)
    for n,(x0,y0),T in OGEN:
        h,w=len(T),len(T[0])
        for y in range(y0-2,y0+h+2):
            for x in range(x0-2,x0+w+2):
                rand=(y in (y0-2,y0+h+1)) or (x in (x0-2,x0+w+1))
                hoek=(y in (y0-2,y0+h+1)) and (x in (x0-2,x0-1,x0+w,x0+w+1)) or (x in (x0-2,x0+w+1)) and (y in (y0-2,y0-1,y0+h,y0+h+1))
                if not rand or hoek or not ok(y,x) or (x,y) in kern or o0[y,x] not in (S,M,H) or (x,y) in ander_oog or raakt_ander(x,y): continue
                if any(abs(x-a)<=1 and abs(y-b)<=1 for (a,b) in kern): continue
                o[y,x]=L
    for p,(n,v) in kern.items(): o[p[1],p[0]]=v
    # buitenlijn: rood aan achtergrond/blad = lijn (zwart als de achtergrond rechts/onder ligt, anders lijnrood); kernwit nooit op de rand
    vak=set(kern)|{(x+dx,y+dy) for (x,y) in kern for dy in (-1,0,1) for dx in (-1,0,1)}
    for (x,y) in vak:
        if not ok(y,x) or o[y,x] not in (L,S,M,H,K) or (x,y) in ander_oog: continue
        if (x,y) in kern and o[y,x]==K: continue
        nb=[(dy,dx) for dy,dx in N4 if g(o,y+dy,x+dx) in (0,)+GROEN]
        if nb==[(-1,0)] and g(o,y-1,x) in GROEN and any(kern.get((x+dx,y),(0,0))[1]==L for dx in (-1,1)): continue   # bovenrand naast de bovenschil: vrucht, geen rechte bovenlijn
        if not nb: continue
        o[y,x]=K if any(d in ((1,0),(0,1)) for d in nb) else L
    rest=[(x,y) for (x,y) in eigen if o[y,x] in (W,G) and (x,y) not in kern]
    for (x,y) in rest: o[y,x]=M if g(o,y,x+1)!=0 and g(o,y+1,x)!=0 else K   # oud wit buiten de nieuwe kern -> vrucht (of buitenlijn)
    print('oud wit opgevuld',rest)
    for p in eigen_wit:
        assert any(g(o,p[1]+dy,p[0]+dx)!=0 for dy,dx in N4)
    return o,o0
def verdeling(a):
    c=[(a==k).sum() for k in (L,S,M,H)]; t=sum(c); return t,[round(100*x/t,1) for x in c]
if __name__=='__main__':
    o,o0=maak('sprite_r12/guarana2_r12.png')
    print('r12',verdeling(o0),'r13',verdeling(o),'anders',int((o!=o0).sum()),'silhouet',int(((o>0)!=(o0>0)).sum()))
    opslaan(o,'sprite_r13/guarana2_r13.png'); open('sprite_r13/normal.pal','w').write(open('sprite_r12/normal.pal').read())
