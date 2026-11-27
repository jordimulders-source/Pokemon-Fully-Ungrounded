# Guarana fase 2, r2 (r1 + benoemde reparaties coordinator, zie NOTITIES). Variant: ZWARTRAND=1 = oogrand rechts/onder zwart zoals fase 1.
# r1: Basis = kale reductie (kaal.py, TK 0,40) van het natieve model (natief.py). Daarna alleen regels, niets getekend:
#  1 lijnkleur: zwart binnenin -> donkerste eigen tint (rood 2 / groen 6); buitenlijn zwart alleen waar de achtergrond rechts/onder ligt,
#    aan de lichtkant (achtergrond links/boven) de eigen lijntint (selout). Vlakpixels op de buitenrand met een binnenbuur worden lijn
#    (zwart/selout volgens dezelfde regel); dunne delen (geen binnenbuur) blijven zoals de reductie.
#  2 ogen: het fase 1-oog (guarana/af/guarana.png y16-23 x16-22, Weepinbell-patroon) op de oogplekken van het model, pupil op de kijkkant.
import sys, os, numpy as np; sys.path.insert(0,'sprite_r5')
ZW=os.environ.get('ZWARTRAND')=='1'; UIT='sprite_r5/guarana2_r5_'+('B' if ZW else 'A')+'.png'
from gemeen2 import *; import kaal
o,F,FID,LD=kaal.reductie(); K0=o.copy()
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def ok(Y,X): return 0<=Y<64 and 0<=X<64
# --- 0. gaatjes van 1-2 px in de reductie (witte modelspleetjes tussen vruchten) dicht: zwart, wordt bij stap 1 binnenlijn ---
from collections import deque
bgm=np.zeros((64,64),bool); q=deque([(y,x) for y in range(64) for x in (0,63) if o[y,x]==0]+[(y,x) for x in range(64) for y in (0,63) if o[y,x]==0])
for y,x in q: bgm[y,x]=True
while q:
    y,x=q.popleft()
    for dy,dx in N4:
        yy,xx=y+dy,x+dx
        if ok(yy,xx) and o[yy,xx]==0 and not bgm[yy,xx]: bgm[yy,xx]=True; q.append((yy,xx))
gat=(o==0)&~bgm
from gemeen2 import *
GATEN=[]
seen=np.zeros((64,64),bool)
for y,x in zip(*np.where(gat)):
    if seen[y,x]: continue
    comp=[(y,x)]; seen[y,x]=True; i=0
    while i<len(comp):
        cy,cx=comp[i]; i+=1
        for dy,dx in N4:
            yy,xx=cy+dy,cx+dx
            if ok(yy,xx) and gat[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; comp.append((yy,xx))
    if len(comp)<=2:
        for cy,cx in comp: o[cy,cx]=1; GATEN.append((cx,cy))
# --- 0b. (r4) buitenrand glad (glad.py) ---
import glad; WEG,BIJ=glad.glad(o)
print('rand weg',WEG); print('rand bij',BIJ)
fg=o>0
def bgnb(Y,X): return [(dy,dx) for dy,dx in N4 if not ok(Y+dy,X+dx) or not fg[Y+dy,X+dx]]
def groep(Y,X):
    f,_=F[(X,Y)]
    if f[2]+f[4]>f[3]*1.0 and f[2]+f[4]>0.05: return 'R'
    if f[3]>0.05: return 'G'
    r=g=0
    for dy,dx in N8:
        if ok(Y+dy,X+dx): ff,_=F[(X+dx,Y+dy)]; r+=ff[2]+ff[4]; g+=ff[3]
    return 'R' if r>g else 'G'
LIJN={'R':2,'G':6}
tel={'gaatjes_dicht':len(GATEN),'rand_weg':len(WEG),'rand_bij':len(BIJ)}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
# --- 1. lijnen ---
v=o.copy()
for Y in range(64):
    for X in range(64):
        if not fg[Y,X]: continue
        nb=bgnb(Y,X)
        rand=bool(nb)
        schaduw=any(d in ((1,0),(0,1)) for d in nb)
        if v[Y,X]==1:
            if not rand: o[Y,X]=LIJN[groep(Y,X)]
            elif not schaduw: o[Y,X]=LIJN[groep(Y,X)]
        elif rand:
            binnen=any(ok(Y+dy,X+dx) and fg[Y+dy,X+dx] and not bgnb(Y+dy,X+dx) for dy,dx in N4)
            if binnen: o[Y,X]=1 if schaduw else LIJN[groep(Y,X)]
stap('lijnen',v,o)
pal_schrijven('sprite_r5/normal.pal')
# --- 1b. elke vrucht leesbaar: grens tussen twee vruchten (vrucht-id uit het natieve model) = 1 px lijnrood op de pixel met de meeste modellijn ---
RF={3,4,12,5}
v=o.copy()
for Y in range(64):
    for X in range(64):
        for dy,dx in ((0,1),(1,0)):
            Y2,X2=Y+dy,X+dx
            if not ok(Y2,X2): continue
            if v[Y,X] in RF and v[Y2,X2] in RF and FID[Y,X] and FID[Y2,X2] and FID[Y,X]!=FID[Y2,X2] and o[Y,X]!=2 and o[Y2,X2]!=2:
                if LD[Y,X]>=LD[Y2,X2]: o[Y,X]=2
                else: o[Y2,X2]=2
stap('vruchtgrenzen',v,o)
# --- 2. ogen: fase 1-oog (guarana/af/guarana.png, x16-22 y17-23) 1-op-1; O = lijnrood 2 (lichtkant), K = zwart, W = oogwit 10 ---
FASE1=['..OOO..','.OWWWK.','OWWWWWK','OWKKWWK','OWKKWWK','.KWWWK.','..KKK..']   # pupil links-onder (zoals fase 1)
# Oogplekken afgelezen op het natieve model met het spriteraster erover (rooster.py; positie = linkerbovenhoek van de oogrand in het model).
# Maat per oog = de maat in het model. Grote ogen (model 7x6 incl. rand) = het fase 1-oog min één pupilrij (pupil 2x2 blijft);
# kleinere ogen = hetzelfde oog ingekort tot hun modelmaat (Jordi: "pupillen ietsje kleiner en andere hoek is niet erg").
# Tekens als fase 1: O lijnrood (2) boven/links, K zwart rechts/onder + pupil, W oogwit (10).
# r3: pupil linksonder in elk oog (Jordi r2: "kijken de ogen eigenlijk vrijwel nergens echt naar linksonder"; "soms mag je afwijken van de
# 4 pixel pupil als dat beter past"; "Half dicht is prima, dan kan je makkelijker wegkomen met een kleiner pupil, overlap geen probleem").
# Tekens: O = geen lijn (vrucht), W wit, w grijs (oogwit-schaduw onder het lid, rond maken), K rand (lijnrood in A, zwart in B), P pupil (zwart).
# Witvorm = fase 1-oog (3-5-5-3 rond); pupil linksonder raakt de onderrand (overlap mag).
# r5: Jordi: "de ogen zien er nu niet goed uit omdat ze allemaal precies dezelfde richting hebben, kijk naar hoe de eerste fase het deed".
# Elk oog een eigen pupilplek (zoals fase 1: drie ogen, drie richtingen), uit de kijkrichting van dat oog in het model (kijkrichting.py);
# buren nooit gelijk. Witvorm en pupilgrootte zoals r4 (2x2 groot, L van 3 px middel, 1-2 px klein/half dicht).
STEMPEL={
 'groot':['..OOO..','.OwWwK.','OWWWWWK','OWWWWWK','.KWWWK.','..KKK..'],
 'middel':['.OOOO.','OWWWwK','OWWWWK','OWWWWK','.KKKK.'],
 'lid':['.LLLL.','LWWWWK','.KKKK.'],      # r4: ooglid = rode boog (L = schaduwrood 3, in A en B)
 'lidk':['.LLL.','LWWWK','.KKK.'],
 'klein':['.OO.','OWWK','OWWK','.KK.'],
}
def _v(c0,r0): return [(c0,r0),(c0+1,r0),(c0,r0+1),(c0+1,r0+1)]
PUPOPT={
 'groot':{'l':_v(1,2),'lo':_v(2,3),'lh':_v(2,1),'m':_v(2,2),'mo':_v(3,3),'r':_v(4,2),'rh':_v(3,1)},
 'middel':{'l':[(1,1),(1,2),(2,2)],'lo':[(1,2),(1,3),(2,3)],'lh':[(1,1),(2,1),(1,2)],'m':[(2,2),(3,2),(2,3)],
           'mo':[(2,3),(3,3),(2,2)],'r':[(4,1),(4,2),(3,2)],'ro':[(4,2),(4,3),(3,3)],'rh':[(3,1),(4,1),(4,2)]},
 'klein':{'lo':[(1,2)],'lh':[(1,1)],'ro':[(2,2)],'rh':[(2,1)]},
 'lid':{'l':[(1,1),(2,1)],'m':[(2,1),(3,1)],'r':[(3,1),(4,1)]},
 'lidk':{'l':[(1,1)],'m':[(2,1)],'r':[(3,1)]},
}
# kijkrichting per oog: gemeten offset pupil t.o.v. oogmidden in het model (dx, dy; + = rechts/onder), zie NOTITIES; '-' = niet meetbaar (half dicht/verstopt)
# Jordi (r5): "ja zorg dat er iets meer ogen naar linksonder kijken maar idd verschillende richtingen": 12 van 15 kijken links/linksonder/onder
# (in gradaties), 3 een andere kant op (M1 rechts, M2 midden, R1 rechtsboven = de modelrichting); buren nooit gelijk.
# Model gemeten (dx,dy): M1 -0,09/+0,06  M4 +0,31/+0,15  R1 +0,37/-0,23  L2 -0,04/-0,11  R2 +0,09/-0,03  L1 -0,39/+0,52  R3 -0,33/-1,00
#   R5 -0,19/+0,05  L4 +0,32/+0,05  R6 -0,32/+0,04  L5 +0,32/+0,05; L3, M2, M3, R4 niet meetbaar.
KIJK={'L1':'l','L2':'lo','L3':'lh','L4':'l','L5':'mo','M1':'r','M2':'m','M3':'l','M4':'lo',
      'R1':'rh','R2':'mo','R3':'lh','R4':'l','R5':'l','R6':'lo'}   # niet meetbaar: gevarieerd t.o.v. de buren
PUP={}
# naam: (soort, kijk, x, y)
OGEN={'L3':('klein','l',16,25),'R3':('klein','m',42,25),'M3':('lidk','l',20,19),'R4':('lidk','r',49,26),
      'L1':('lid','l',6,26),'M2':('lidk','l',24,16),
      'L2':('middel','r',12,22),'L4':('groot','r',12,28),'L5':('groot','rb',15,32),
      'M1':('middel','r',30,12),'M4':('groot','r',29,19),
      'R1':('middel','l',46,22),'R2':('middel','l',52,22),'R5':('groot','l',46,29),'R6':('groot','l',41,32)}
VOLG=['L3','R3','M3','R4','L1','M2','L2','L5','L4','M1','M4','R1','R2','R5','R6']   # achter -> voor (wat in het model ervoor ligt het laatst)
SKIP=set(sys.argv[1].split(',')) if len(sys.argv)>1 and sys.argv[1] else set()
v=o.copy(); OOG=np.zeros((64,64),bool); PUPIL=np.zeros((64,64),bool)
def stempel_ogen(o,OOG,PUPIL):
    for n in VOLG:
        if n in SKIP: continue
        soort,kijk,X,Y=OGEN[n]
        st=[list(r) for r in STEMPEL[soort]]
        for (pc,pr) in PUPOPT[soort][KIJK[n]]: st[pr][pc]='P'
        for dy,rij in enumerate(st):
            for dx,ch in enumerate(rij):
                if ch=='.' or not ok(Y+dy,X+dx) or not fg[Y+dy,X+dx]: continue   # silhouet bevroren: niets buiten de reductie
                if ch=='O':
                    if o[Y+dy,X+dx] not in RF|{14} and not bgnb(Y+dy,X+dx): o[Y+dy,X+dx]=4
                    continue
                if ch=='W': o[Y+dy,X+dx]=10
                elif ch=='w': o[Y+dy,X+dx]=11
                elif ch=='P': o[Y+dy,X+dx]=1; PUPIL[Y+dy,X+dx]=True
                elif ch=='L': o[Y+dy,X+dx]=3 if not bgnb(Y+dy,X+dx) else 2
                else: o[Y+dy,X+dx]=1 if ZW else 2
                OOG[Y+dy,X+dx]=True
    # oogwit dat zo op de buitenrand komt -> zwart (de oogrand schuift 1 px naar binnen, zoals fase 1 r4)
    for Y,X in zip(*np.where(OOG&np.isin(o,(10,11)))):
        nb=bgnb(Y,X)
        if nb: o[Y,X]=1 if any(d in ((1,0),(0,1)) for d in nb) else 2
    # oogpixels op de buitenrand: zwart alleen aan de schaduwkant (rechts/onder), anders lijnrood (r2: L1, R4)
    for Y,X in zip(*np.where(OOG&(o==1))):
        nb=bgnb(Y,X)
        if nb and not any(d in ((1,0),(0,1)) for d in nb): o[Y,X]=2
        elif nb: o[Y,X]=1
stempel_ogen(o,OOG,PUPIL)
stap('ogen',v,o)
# --- 3. oogwit/grijs buiten de ogen (gaatjes tussen vruchten en oogresten in de reductie) -> lijntint van de buren ---
v=o.copy()
for Y,X in zip(*np.where(np.isin(o,WIT)&~OOG)):
    nb=[o[Y+dy,X+dx] for dy,dx in N8 if ok(Y+dy,X+dx)]
    r=sum(k in ROOD for k in nb); g=sum(k in GROEN for k in nb)
    o[Y,X]=2 if r>=g else 6
stap('wit_buiten_ogen',v,o)
# --- 4. ruis: losse vultintpixel (geen 4-buur met dezelfde tint) -> meest voorkomende vultint van de 4-buren (alleen vultinten, lijnen/ogen niet) ---
# r2: tintvlakjes < 3 px (4-buren) van een vultint -> meest voorkomende vultint eromheen (zelfde kleurgroep); hooglicht rood (5) mag klein (glans)
VUL={3,4,12,5,7,13,8,9}
for ronde in range(3):
    v=o.copy(); seen=np.zeros((64,64),bool)
    for y in range(64):
        for x in range(64):
            k=v[y,x]
            if k not in VUL or k==5 or seen[y,x] or OOG[y,x]: continue
            comp=[(y,x)]; seen[y,x]=True; i=0
            while i<len(comp):
                cy,cx=comp[i]; i+=1
                for dy,dx in N4:
                    yy,xx=cy+dy,cx+dx
                    if ok(yy,xx) and v[yy,xx]==k and not seen[yy,xx]: seen[yy,xx]=True; comp.append((yy,xx))
            if len(comp)>=3: continue
            rond=[v[cy+dy,cx+dx] for cy,cx in comp for dy,dx in N4 if ok(cy+dy,cx+dx) and (cy+dy,cx+dx) not in comp]
            zelfde=[n for n in rond if n in VUL and ((n in ROOD)==(k in ROOD))]
            if zelfde:
                t=max(set(zelfde),key=zelfde.count)
                for cy,cx in comp: o[cy,cx]=t
    stap('ruis',v,o)
# --- 5. geen lichte tint op de buitenrand: dunne delen (rand zonder binnenbuur) houden hun vulkleur, maar midden/licht -> schaduwtint (selout) ---
v=o.copy()
for Y,X in zip(*np.where(fg)):
    if bgnb(Y,X) and o[Y,X] in (4,5,12,8,9,13): o[Y,X]=3 if o[Y,X] in (4,5,12) else 7
stap('selout_dun',v,o)
# --- 5b. (r2) dubbele binnenlijnen in de tros (vrucht | 2 | 2 | vrucht, in x of y): de lijnpixel met de minste modellijn (LD) wordt vrucht
#      (tint van de vrucht aan zijn kant); oogpixels blijven. Ook een lijnrode pixel met aan beide kanten vrucht van dezelfde vrucht-id -> vrucht.
RV={3,4,12,5}
for ronde in range(2):
    v=o.copy()
    for Y in range(64):
        for X in range(64):
            for dy,dx in ((0,1),(1,0)):
                p=[(Y+k*dy,X+k*dx) for k in range(4)]
                if not all(ok(*q) for q in p): continue
                a0,a1,a2,a3=[v[q] for q in p]
                if a0 in RV and a3 in RV and a1==2 and a2==2 and not OOG[p[1]] and not OOG[p[2]] and not bgnb(*p[1]) and not bgnb(*p[2]):
                    if LD[p[1]]<=LD[p[2]]: o[p[1]]=a0
                    else: o[p[2]]=a3
    stap('dubbele_lijn',v,o)
v=o.copy()
for Y in range(1,63):
    for X in range(1,63):
        if v[Y,X]!=2 or OOG[Y,X] or bgnb(Y,X): continue
        for (ay,ax),(by,bx) in (((Y,X-1),(Y,X+1)),((Y-1,X),(Y+1,X))):
            if v[ay,ax] in RV and v[by,bx] in RV and FID[ay,ax] and FID[ay,ax]==FID[by,bx] and FID[Y,X] in (0,FID[ay,ax]):
                o[Y,X]=v[ay,ax]; break
stap('lijn_in_vrucht',v,o)
# --- 6. (r2) binnenin geen zwart: zwart dat niet op de buitenrand ligt en geen pupil is (en niet de zwarte oogrand van de variant) -> eigen lijntint ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    if PUPIL[Y,X] or bgnb(Y,X) or (ZW and OOG[Y,X]): continue
    o[Y,X]=LIJN[groep(Y,X)]
stap('zwart_binnen',v,o)
# --- 7. (r3) volume: vulpixels per object opnieuw ingekleurd (schaduw.py) ---
import schaduw; log=[]
v=o.copy(); o,VUL,OBJ=schaduw.kleur(o,OOG,kaal.VL,kaal.GROOT,LD,log=log); stap('schaduw',v,o)
# --- 8. (r3) vruchten als ronde bollen (vrucht.py): ellips per modelvrucht, achter -> voor getekend binnen het r2-trosgebied, bol ingekleurd ---
import vrucht
v=o.copy(); o=vrucht.teken(o,OOG,fg,groep,ZW); stap('vruchten',v,o)
OOG[:]=False; PUPIL[:]=False; v=o.copy(); stempel_ogen(o,OOG,PUPIL); stap('ogen_opnieuw',v,o)
# --- 9. (r3) ruis in het groen: tintvlakjes < 3 px (4-buren) -> meest voorkomende groene vultint eromheen (glans 9 mag klein);
#      in rood alleen losse pixels zonder gelijke 8-buur (kleine bollen hebben kleine tintvlakjes, zoals Gen 3)
GV=[15,7,13,8,9]; RV3=[14,3,4,5,12]
for ronde in range(3):
    v=o.copy(); seen=np.zeros((64,64),bool)
    for y in range(64):
        for x in range(64):
            k=v[y,x]
            if k not in GV+RV3 or seen[y,x] or OOG[y,x] or k in (9,12): continue
            comp=[(y,x)]; seen[y,x]=True; i=0
            while i<len(comp):
                cy,cx=comp[i]; i+=1
                for dy,dx in N4:
                    yy,xx=cy+dy,cx+dx
                    if ok(yy,xx) and v[yy,xx]==k and not seen[yy,xx]: seen[yy,xx]=True; comp.append((yy,xx))
            if k in RV3:
                if len(comp)>1 or any(ok(y+dy,x+dx) and v[y+dy,x+dx]==k for dy,dx in N8): continue
            elif len(comp)>=3: continue
            fam=GV if k in GV else RV3
            rond=[v[cy+dy,cx+dx] for cy,cx in comp for dy,dx in N4 if ok(cy+dy,cx+dx) and (cy+dy,cx+dx) not in comp and v[cy+dy,cx+dx] in fam]
            if rond:
                t=max(set(rond),key=rond.count)
                for cy,cx in comp: o[cy,cx]=t
    stap('ruis_r3',v,o)
# --- 10. (r4) dubbele pixels in de diagonaal van de buitenlijn weg (DC-gids: lijn 1 px, ook schuin): een lijnpixel op de buitenrand met
#      achtergrond aan twee aangrenzende kanten, lijn aan de twee andere kanten en binnenvlak schuin ertegenover is een hoekpixel -> achtergrond.
LIJNK={1,2,3,6,7,14,15}
HOEK=[]
for ronde in range(2):
    f2=o>0
    def bgp(y,x): return not ok(y,x) or not f2[y,x]
    def rnd(y,x): return f2[y,x] and any(bgp(y+dy,x+dx) for dy,dx in N4)
    for Y,X in zip(*np.where(f2)):
        if o[Y,X] not in LIJNK or OOG[Y,X]: continue
        for (ay,ax),(by,bx) in (((-1,0),(0,-1)),((-1,0),(0,1)),((1,0),(0,-1)),((1,0),(0,1))):
            if bgp(Y+ay,X+ax) and bgp(Y+by,X+bx) and bgp(Y+ay+by,X+ax+bx):
                c1=(Y-ay,X-ax); c2=(Y-by,X-bx); dg=(Y-ay-by,X-ax-bx)
                if all(ok(*q) for q in (c1,c2,dg)) and o[c1] in LIJNK and o[c2] in LIJNK and rnd(*c1) and rnd(*c2) and f2[dg] and not rnd(*dg):
                    o[Y,X]=0; HOEK.append((int(X),int(Y))); break
print('hoekpixels weg',HOEK); tel['hoek_weg']=len(HOEK)
np.save('sprite_r5/oog.npy',OOG); np.save('sprite_r5/pupil.npy',PUPIL); opslaan(o,UIT); print(UIT,tel)
