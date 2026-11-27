# Guarana fase 2, r12 (start r11): roodverdeling naar fase 1 (lijnrood/schaduw/midden/licht ±40/15/35/10).
# Jordi: "fase 2 is toch nog iets anders in kleurtinten" ... "ja, maar zorg ervoor dat het geen blur wordt".
# Stap 1 (S->M): schaduwrood blijft alleen als sikkel: de pixel rechts of onder is een grens (lijn, zwart, achtergrond, groen, oog).
# Stap 1b: sikkel 1 px dik (schaduw met schaduw rechts/onder ervan -> midden, behalve in een hoek met lijn links en boven).
# Stap 2 (L->S): binnennaad lijnrood -> schaduwrood, behalve buitenrand (aan achtergrond/groen), schil om het oog (raakt wit/pupil),
#   en naden waarvan beide kanten (links/rechts of boven/onder) al schaduw of donkerder zijn (dan verdwijnt de grens).
# Stap 3: losse schaduwpixel (geen 8-buur schaduw) krijgt zijn oude schaduwbuur links/boven terug (sikkel van 2 px i.p.v. een stip).
# Groen, ogen, silhouet: niet aangeraakt (assert). Vanuit guarana_fase2/: python3 sprite_r12/bouw12.py
import sys; sys.path.insert(0,'sprite_r9'); import numpy as np; from PIL import Image; from gemeen2 import *; from hulp import *
K,L,S,M,H=1,2,3,4,5; W,G=10,11; GROEN=(6,7,8,9)
HAND={}   # (x,y): kleur, handcorrecties na de regels (zie NOTITIES)
def g(o,y,x): return o[y,x] if ok(y,x) else 0
def grens(v): return v in (0,K,L,W,G)+GROEN
def maak(src):
    o=np.array(Image.open(src)).astype(int); o0=o.copy()
    # stap 1
    for y in range(64):
        for x in range(64):
            if o0[y,x]==S and not (grens(g(o0,y,x+1)) or grens(g(o0,y+1,x))): o[y,x]=M
    # stap 1b: sikkel 1 px dik: een schaduwpixel waarvan de pixel rechts of onder ook (oude) schaduw is, wordt midden
    o1=o.copy()
    for y in range(64):
        for x in range(64):
            if o1[y,x]==S and (g(o1,y,x+1)==S or g(o1,y+1,x)==S) and not (g(o1,y,x-1) in (K,L) and g(o1,y-1,x) in (K,L)): o[y,x]=M
    o1=o.copy()
    # stap 2
    for y in range(64):
        for x in range(64):
            if o1[y,x]!=L: continue
            nb=[g(o1,y+dy,x+dx) for dy,dx in N8]
            if any(v in (0,W,G)+GROEN for v in nb): continue          # buitenrand / tegen blad / schil om het oog
            if any(g(o1,y+dy,x+dx)==K for dy,dx in N4): continue      # tegen pupil of zwarte lijn
            d=lambda v: v in (K,L,S)
            if (d(g(o1,y,x-1)) and d(g(o1,y,x+1))) and (d(g(o1,y-1,x)) and d(g(o1,y+1,x))): continue
            lr=d(g(o1,y,x-1)) and d(g(o1,y,x+1)); ud=d(g(o1,y-1,x)) and d(g(o1,y+1,x))
            # naad horizontaal (boven/onder vrucht) of verticaal (links/rechts vrucht): grens moet blijven
            vert=g(o1,y-1,x) in (L,) or g(o1,y+1,x) in (L,)
            sides=(g(o1,y,x-1),g(o1,y,x+1)) if vert else (g(o1,y-1,x),g(o1,y+1,x))
            if all(v in (K,L,S) for v in sides): continue
            o[y,x]=S
    # stap 3: geen losse schaduwpixels: een schaduwpixel zonder 8-buur schaduw krijgt zijn (r11-)schaduwbuur links/boven terug
    for y in range(64):
        for x in range(64):
            if o[y,x]==S and not any(g(o,y+dy,x+dx)==S for dy,dx in N8):
                if o0[y,x]==L: o[y,x]=L; continue   # losse naadpixel: lijnrood houden
                for dy,dx in ((0,-1),(-1,0),(-1,-1),(1,-1),(-1,1),(0,1),(1,0)):
                    if g(o0,y+dy,x+dx)==S and o[y+dy,x+dx]==M: o[y+dy,x+dx]=S; break
    for (x,y),v in HAND.items(): o[y,x]=v
    assert ((o0>0)==(o>0)).all() and (o[(o0<2)|(o0>5)]==o0[(o0<2)|(o0>5)]).all()
    return o,o0
def verdeling(a):
    c=[(a==k).sum() for k in (L,S,M,H)]; t=sum(c); return t,[round(100*x/t,1) for x in c]
if __name__=='__main__':
    o,o0=maak('sprite_r11/guarana2_r11.png')
    print('r11',verdeling(o0),'r12',verdeling(o),'anders',int((o!=o0).sum()))
    opslaan(o,'sprite_r12/guarana2_r12.png'); open('sprite_r12/normal.pal','w').write(open('sprite_r11/normal.pal').read())
