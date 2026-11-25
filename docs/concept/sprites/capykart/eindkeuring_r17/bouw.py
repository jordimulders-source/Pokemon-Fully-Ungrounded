# Capykart eindkeuring r17 (Dragonfly Cave): alleen lijnkleur en pixels terug naar de modeltoon.
# Draaien vanuit capykart/: python3 eindkeuring_r17/bouw.py
import sys, math; sys.path.insert(0,'sprite/r17')
from gemeen import overlap
import numpy as np; from PIL import Image
SRC='sprite/r17b/capykart.png'; OUT='eindkeuring_r17/'
im=Image.open(SRC); a0=np.array(im); a=a0.copy(); pal=np.array(im.getpalette()[:48]).reshape(16,3)
CH='.KbsLHgGYrRuUnNW'; IDX={c:i for i,c in enumerate(CH)}
nat=np.asarray(Image.open('sprite/r17/natief.png').convert('RGB')).astype(float)
Z=np.load(OUT+'_zwart.npy')   # aandeel modelzwart per spritepixel (zelfde overlap als kaal.py)
H=W=64; log=[]
def k4(x,y): return [(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if 0<=x+dx<W and 0<=y+dy<H]
def k8(x,y): return [(x+dx,y+dy) for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and 0<=x+dx<W and 0<=y+dy<H]
def rand(x,y): return any(a[v,u]==0 for u,v in k4(x,y)) or x in(0,63) or y in(0,63)
def beschermd(x,y):
    return ((28<=x<=33 and 16<=y<=22) or (18<=x<=23 and 32<=y<=35) or (x,y) in {(16,23),(20,23),(18,29),(20,30)}
            or (21<=x<=24 and 15<=y<=16))
GROEP={2:'B',3:'B',4:'B',5:'B',6:'H',7:'H',8:'Y',9:'R',10:'R',11:'U',12:'U',13:'N',14:'N',15:'W'}
def modeltoon(x,y):
    acc=np.zeros(3); tw=0
    for u,v,w in overlap(x,y):
        c=nat[v,u]
        if c.mean()>=50 and c.min()<245: acc+=w*c; tw+=w
    c=acc/tw
    toren=(x>=42 and y<=33)
    ks=[k for k in range(2,15) if toren or GROEP[k] in('B','H')]
    k=min(ks,key=lambda k:((pal[k]-c)**2).sum()); return k, tuple(int(t) for t in c)
def simpel(x,y):
    # zwarte 8-buren blijven na weghalen één 8-samenhangend geheel
    nb=[(u,v) for u,v in k8(x,y) if a[v,u]==1]
    if len(nb)<3: return False
    s=set(nb); st=[nb[0]]; seen={nb[0]}
    while st:
        p=st.pop()
        for q in k8(*p):
            if q in s and q not in seen: seen.add(q); st.append(q)
    return len(seen)==len(s)
def zet(x,y,k,stap,cit):
    log.append('%-22s (%2d,%2d) %s -> %s  %s'%(stap,x,y,CH[a[y,x]],CH[k],cit)); a[y,x]=k

C1='DC: "remove the clusters so that the outline is always one pixel wide"'
# --- stap 1: dubbele zwarte lijnen dun maken (reductie "zwart wint vanaf 30%" maakte 2 px waar het model 1 lijn heeft)
# alleen binnenpixels met < 45 % modelzwart, die een lijn niet breken (simpel punt) en die aan hun eigen vlak grenzen
for it in range(3):
    kand=sorted([(Z[y,x],x,y) for y in range(H) for x in range(W)
                 if a[y,x]==1 and not rand(x,y) and not beschermd(x,y) and Z[y,x]<0.45])
    n=0
    for z,x,y in kand:
        if a[y,x]!=1 or not simpel(x,y): continue
        if not any(a[v,u] not in(0,1) for u,v in k4(x,y)): continue
        k,c=modeltoon(x,y)
        zet(x,y,k,'1 dunner (%.0f%% zwart)'%(z*100),'model %s; '%(c,)+C1); n+=1
    if not n: break
# losse zwarte binnenpixels zonder zwarte 4-buur (binnenlijn rechteroor): eigen donkerste tint
C2='DC: binnenlijnen in de eigen donkerste tint, niet zwart ("take the base outlining shade for every color")'
for y in range(H):
    for x in range(W):
        if a[y,x]==1 and not rand(x,y) and not beschermd(x,y) and not any(a[v,u]==1 for u,v in k4(x,y)) and Z[y,x]<0.45:
            k,c=modeltoon(x,y); zet(x,y,k,'1b losse zwarte px','model %s; '%(c,)+C2)

# hoekpixel motorkap (9,39): 2x2-zwart in de hoek, simpel punt; model 50 % zwart, rest hout
k,c=modeltoon(9,39); zet(9,39,k,'1c hoek motorkap','model %s (50%% zwart, rest hout); '%(c,)+C1)
# (11,38): laatste 2x2-zwart buiten oog/hoepelknoop; model 48 % zwart, 52 % hoepelgrijs (107,101,108) -> hoepel-donker (r17: L<110 donker)
zet(11,38,7,'1e 2x2 hoepeleind','model 52%% grijs (107,101,108); '+C1)
# (50,11): voorrand geel blok = olijfrand, in r17 overal bruin-lijn (kolom 50, y12-16)
zet(50,11,2,'1d olijfrand geel blok','r17-mapping olijfrand -> bruin-lijn, zoals (50,12..16)')
veranderd=set(zip(*np.where(a!=a0)))
# --- stap 2: ontkorrelen van de teruggezette pixels (zelfde regel als r17 bouw.py stap 2)
C3='SPRITE_KERN: geen tintvlakjes < 3 px; r17-regel: neemt de meest voorkomende buurtint uit dezelfde groep'
LIJN={2,7}
def cluster(x,y):
    k=a[y,x]; st=[(x,y)]; seen={(x,y)}
    while st and len(seen)<3:
        p=st.pop()
        for q in k4(*p):
            if a[q[1],q[0]]==k and q not in seen: seen.add(q); st.append(q)
    return len(seen)
for (y,x) in sorted(veranderd):
    k=a[y,x]
    if k in LIJN or k in(0,1) or cluster(x,y)>=3: continue
    nb=[a[v,u] for u,v in k8(x,y) if a[v,u] not in(0,1) and a[v,u]!=k and GROEP.get(a[v,u])==GROEP[k] and (a[v,u] not in LIJN or GROEP[k]=='H')]
    if nb:
        n=max(set(nb),key=nb.count); zet(x,y,n,'2 ontkorrelen',C3)

# --- stap 3: buitenlijn aan de lichtkant (boven / linksboven / linksbovenhelft) in de eigen donkerste tint
C4=('DC: "take the base outlining shade for every color and color all of the outline except the shadows in that color"; '
    '"outline shadows are always black"; SPRITE_KERN: zwart alleen aan de schaduwkant')
SEL={'B':2,'H':7,'Y':2,'R':10,'U':12,'N':14}
def normaal(x,y):
    nx=ny=0
    for dy in(-1,0,1):
        for dx in(-1,0,1):
            if (dx or dy) and (not(0<=x+dx<W and 0<=y+dy<H) or a[y+dy,x+dx]==0): nx+=dx; ny+=dy
    return math.degrees(math.atan2(-ny,nx))%360
# helft van het onderdeel voor linkse randen: kop y11-33 (midden 22), auto y36-62 (midden 49), blauw blok y26-33
def bovenhelft(x,y):
    if x<=20 and y>=36: return y<49
    if 15<=x<=30 and y<=33: return y<22
    return True
snap=a.copy(); besluit=[]
for y in range(H):
    for x in range(W):
        if snap[y,x]!=1 or not rand(x,y): continue
        if 14<=x<=24 and 30<=y<=36: continue        # kader Bibarel-tanden / kin: linksonder van de kop, blijft zwart
        ang=normaal(x,y)
        if not (67.5<=ang<202.5): continue          # boven, linksboven, links
        if ang>=157.5 and not bovenhelft(x,y): continue
        inn=[snap[v,u] for u,v in k4(x,y) if snap[v,u] not in(0,1)]
        if not inn: continue
        gs=[GROEP[k] for k in inn]; g=max(set(gs),key=gs.count)
        if g in('H','W'): continue                          # hoepel: donker metaal, lijn blijft zwart (model)
        sel=SEL[g]
        if sel in inn: continue                      # binnenkant al de donkerste tint: zwart houden, anders open rand
        besluit.append((x,y,sel,ang))
besluit=[b for b in besluit if (b[0],b[1])!=(59,33)]   # bovenhoek achterblok rechts: buur (58,33) is schaduwkant-zwart -> anders om en om
for x,y,sel,ang in besluit: zet(x,y,sel,'3 lichtkant (%d gr)'%ang,C4)
# stap 3b: zwart enkel tussen twee lijnkleur-pixels op de lichtkant -> lijnkleur
C5='SPRITE_KERN: "nooit zwart en donkerlila om en om op één rand" (hier: zwart/bruin-lijn)'
zet(32,14,2,'3b om en om','(31,14) en (33,15) zijn bruin-lijn; '+C5)
zet(4,41,2,'3b om en om','(5,41) en (3,42) zijn bruin-lijn; '+C5)

# --- controle + opslaan
assert ((a!=0)==(a0!=0)).all(), 'silhouet veranderd'
from PIL import Image as I
p=I.fromarray(a.astype('uint8'),'P'); p.putpalette(im.getpalette()); p.save(OUT+'capykart.png',transparency=0)
open(OUT+'_wijzigingen.txt','w').write('\n'.join(log)+'\n')
print(len(log),'regels;',int((a!=a0).sum()),'px anders dan r17b')
