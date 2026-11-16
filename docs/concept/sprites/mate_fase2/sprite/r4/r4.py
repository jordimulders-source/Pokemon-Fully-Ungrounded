# r4 = r4/bouw4.py (zelfde opbouw als r1-r3 op het nieuwe schrapwerk) + keuringsreparaties, alles uit het model:
#  2. neusgat en verre kano-oog: kale reductie (dichtstbijzijnde kleur uit omlijning+bruin) op de modelpixels
#  4. waterval: waterpixels op de buitenrand -> donkere modelrand (nieuwe tint 15 = mediaan van de modelrandpixels),
#     schuim = modelpixels L>=205 in de waterval -> wit
#  5. losse 1-px tintspikkels (midden/licht groen, geen 4-buur met dezelfde tint) in het bladhoofd boven het gezicht
#  (r2) twee grijze anti-aliaspixels naast de bladkop -> transparant
# Palet = r3-palet + tint 15.
from PIL import Image; import numpy as np, subprocess
D='docs/concept/sprites/mate_fase2/sprite/'
subprocess.run(['python3',D+'r4/bouw4.py'],check=True,capture_output=True)
idx=np.load(D+'r4/idx.npy'); base=idx.copy()
g=np.asarray(Image.open(D+'r4/geschrapt.png').convert('RGB')).astype(int); H,W,_=g.shape
L=.3*g[...,0]+.59*g[...,1]+.11*g[...,2]
r3=Image.open(D+'r3/mate2.png'); pal=np.array(r3.getpalette()[:45]).reshape(15,3)
kept=[x for x in range(11,85) if x not in (16,18,74,75,76,77,79,80,82,83)]
lx=lambda nx: kept.index(nx); ly=lambda ny: ny-29
log={}
def zet(n,y,x,v):
    if idx[y,x]!=v: log.setdefault(n,[]).append((x,y+15,int(idx[y,x]),int(v))); idx[y,x]=v
# 2. neusgat (natief x11-15, y64-69) en verre oog (natief x19-22, y56-62): kale reductie
for nm,(nx0,nx1,ny0,ny1) in {'neusgat':(11,15,64,69),'verre oog':(19,22,56,62)}.items():
    for ny in range(ny0,ny1+1):
        for nx in range(nx0,nx1+1):
            y,x=ly(ny),lx(nx)
            if idx[y,x]==0: continue
            zet(nm,y,x,int(np.abs(pal[1:6]-g[y,x]).sum(1).argmin())+1)
# (r2) anti-alias naast de bladkop
for nx,ny in [(50,32),(62,32)]:
    y,x=ly(ny),lx(nx)
    if idx[y,x] in (10,11,12): zet('anti-alias',y,x,0)
# 4. waterval
rand=[(58+0,0)]
randpix=[]
for y in range(13,27):
    for x in range(56,64):
        if idx[y,x] in (13,14) and any(not(0<=y+dy<H and 0<=x+dx<W) or idx[y+dy,x+dx]==0 for dy,dx in((1,0),(-1,0),(0,1),(0,-1))):
            randpix.append((y,x))
modelrand=[(84,51),(84,52),(84,53),(81,45),(82,47),(83,48),(83,49),(83,50)]   # donkere watervalrand in het natieve model
nat=np.asarray(Image.open(D+'r1/natief.png').convert('RGB')).astype(int)
c15=tuple(int(t) for t in np.median([nat[ny,nx] for nx,ny in modelrand],axis=0))
for y,x in randpix: zet('waterrand',y,x,15)
for y in range(13,27):
    for x in range(58,64):
        if idx[y,x] in (13,14) and L[y,x]>=205: zet('schuim',y,x,12)
# 5. spikkels in het bladhoofd boven het gezicht (lokaal rij 0-9, x 33-55), alleen tinten 7-9
for y in range(0,10):
    for x in range(33,56):
        i=idx[y,x]
        if i not in (7,8,9): continue
        n4=[idx[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1))]
        if i in n4: continue
        same=[j for j in n4 if 6<=j<=9]
        zet('spikkel',y,x,max(set(same),key=same.count))
# 3. selout neusrug: bruine randpixels van de punt (lokaal x<16) houden hun eigen modeltoon (de losse-pixelfilter
#    in bouw4 had ze weer licht gemaakt); dichtstbijzijnde bruine tint op de modelhelderheid
cb=np.array([60,86,120,172])
for y in range(H):
    for x in range(16):
        if 2<=idx[y,x]<=5 and any(not(0<=y+dy<H and 0<=x+dx<W) or idx[y+dy,x+dx]==0 for dy,dx in((-1,0),(0,-1))):
            zet('neusrug',y,x,int(np.abs(cb-L[y,x]).argmin())+2)
# bevriezing (keuring r3: ventje, gezicht, rand+bladhoop en bombilla's goed): in die zones r3 1-op-1 terugzetten,
# behalve de bedoelde reparaties (spikkels, schuim). Afbeelding r3 -> r4: x+1, y-4 (natief x22-73, y29-65).
a3=np.asarray(r3).astype(int); bedoeld={(x,y) for k in ('spikkel','schuim') for x,y,_,_ in log.get(k,[])}
for ny in range(29,66):
    for nx in range(22,74):
        x,y=nx-13,ny-29
        if (x,y+15) in bedoeld: continue
        v=a3[ny-10,nx-14]
        if idx[y,x]!=v: zet('terug naar r3',y,x,int(v))
for k,v in log.items(): print(k,len(v),v)
full=np.zeros((64,64),int); full[15:15+H,0:W]=idx
P=[c for t in pal for c in t]+list(c15)
im=Image.fromarray(full.astype('uint8'),'P'); im.putpalette(P+[0]*(768-len(P))); im.save(D+'r4/mate2.png',transparency=0)
print('tint 15 (waterrand):',c15)
