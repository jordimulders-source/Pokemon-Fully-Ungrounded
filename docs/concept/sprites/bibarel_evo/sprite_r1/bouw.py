# bouw.py: gezicht2.png -> sprite.png (+ tuinbroekvarianten). Alleen technische reparaties en Jordi's toegestane afwijkingen.
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from scipy import ndimage
o=laad('sprite_r1/gezicht2.png').copy()
log=[]
def zet(x,y,v,waarom):
    if o[y,x]!=v: o[y,x]=v; log.append((x,y,waarom))
# 1. neus: modelkleur oranje/oranje-donker (model 'bb/cc'); index 15 vrij voor een derde cremetint
zet(24,19,11,'neus'); zet(25,19,12,'neus')
# 2. potloodpunt: grafiet grijs zoals het model (x0-4, y22-25: a boven, 9 onder), zwarte omlijning
for x,y,v in [(3,22,1),(4,22,1),(1,23,1),(2,23,1),(3,23,10),(4,23,10),(0,24,1),(1,24,9),(2,24,9),(3,24,9),(4,24,9),
              (1,25,1),(2,25,1),(5,24,7),(6,24,7),(7,24,7)]:
    zet(x,y,v,'potloodpunt')
# 3. ruis: tintclusters <3 px (4-buren) buiten gezicht en lijnen -> meest voorkomende buurtint uit dezelfde groep
GROEP={3:'b',4:'b',5:'b',6:'c',7:'c',9:'d',10:'d',11:'o',12:'o',13:'w',14:'w'}
gez=np.zeros_like(o,bool); gez[14:28,20:35]=True; gez[22:26,0:8]=True
for k in GROEP:
    lab,n=ndimage.label(o==k)
    for i in range(1,n+1):
        pts=np.argwhere(lab==i)
        if len(pts)>=3 or any(gez[y,x] for y,x in pts): continue
        nb={}
        for y,x in pts:
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                Y,X=y+dy,x+dx
                if 0<=Y<64 and 0<=X<64 and lab[Y,X]!=i and GROEP.get(o[Y,X])==GROEP[k]: nb[o[Y,X]]=nb.get(o[Y,X],0)+1
        if nb:
            q=max(nb,key=nb.get)
            for y,x in pts: zet(x,y,q,'ruis')
np.save('sprite_r1/voor_selout.npy',o)
LIJN={'b':2,'c':15,'d':8,'o':12,'w':14}
G2={**GROEP,2:'b',15:'c',8:'d'}
def selout(o):
    o=o.copy(); n=0
    P=np.pad(o,1)
    for y in range(64):
        for x in range(64):
            if o[y,x]!=1: continue
            bg=lambda dy,dx: P[y+1+dy,x+1+dx]==0
            if not (bg(-1,0) or bg(0,-1)) or bg(1,0) or bg(0,1): continue
            # alleen lichtkant: buitenkant ligt boven/links; binnenbuur onder/rechts bepaalt de groep
            g=[G2.get(P[y+1+dy,x+1+dx]) for dy,dx in ((1,0),(0,1),(1,1))]
            g=[q for q in g if q]
            if not g: continue
            # niet langs de schaduwkant: alleen in de bovenste-linker helft van elk onderdeel (y-gradient), hier: richting
            o[y,x]=LIJN[max(set(g),key=g.count)]; n+=1
    return o,n
TUIN={5:7,4:7,3:6,2:15}
def tuinbroek(o,ymax):
    o=o.copy(); n=0
    for y in range(42,ymax+1):
        for x in range(64):
            if y<48 and x>=43: continue      # rechterarm/hand blijft bruin
            if o[y,x] in TUIN: o[y,x]=TUIN[o[y,x]]; n+=1
    return o,n
def losse_zwart(o):
    # losse zwarte pixels (geen zwart/achtergrond in de 8 buren) buiten het gezicht -> donkere eigen tint van de omgeving
    o=o.copy(); n=[]
    P=np.pad(o,1)
    for y,x in zip(*np.where(o==1)):
        if gez[y,x]: continue
        nb=[P[y+1+dy,x+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
        if any(v in (0,1) for v in nb): continue
        g=[G2[v] for v in nb if v in G2]
        if g: o[y,x]=LIJN[max(set(g),key=g.count)]; n.append((int(x),int(y)))
    return o,n
base=o
for naam,ymax in (('A_enkels',63),('B_halve_dij',51)):
    t,nt=tuinbroek(base,ymax); t,ns=selout(t); s,nl=losse_zwart(t)
    opslaan(s,f'sprite_r1/sprite_{naam}.png',8)
    print(naam,'losse zwart',len(nl),'tuinbroek px',nt,'selout px',ns,'kleuren',len(set(s.ravel())))
import collections; print(collections.Counter(w for _,_,w in log))
# Voorstel Claude (niet van Jordi): klep in kleur laten contrasteren met de vachtkraag (zelfde vorm, alleen tint).
# Klepvlak = y11-13, x20-34 (onder de koepel, boven de lijn op y14): 3->4, 4->5 (een tint lichter).
s=laad('sprite_r1/sprite_A_enkels.png').copy(); n=0
for y in range(11,14):
    for x in range(20,35):
        if s[y,x] in (3,4): s[y,x]+=1; n+=1
opslaan(s,'sprite_r1/sprite_A_klepvoorstel.png',8); print('klepvoorstel px',n)
import shutil
shutil.copy('sprite_r1/sprite_A_enkels.png','sprite_r1/sprite.png'); shutil.copy('sprite_r1/sprite_A_enkels_8x.png','sprite_r1/sprite_8x.png')
