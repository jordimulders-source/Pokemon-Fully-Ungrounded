# v6 = v5 + Jordi (15 nov): "de ogen zijn echt extreem lelijk, pupillen op willekeurige posities, dat kan echt niet"
# · "de mond is ook slordig" · eerder: "lijkt net alsof ze indeuken".
# 1) oud modelgezicht (oog-, pupil-, tand- en lippixels) weg; gaten gevuld met de omliggende lijftinten van v5.
# 2) band in de gezichtszone één tint lichter (b->m), lichte wig tussen de ogen (l/u) vlak met de band (m).
# 3) ogen en grijns = Gengars Gen 3-pixels 1-op-1 (graphics/pokemon/gengar/anim_front.png), middelpunten op de v5-plek:
#    ogen dx -5, dy +3 (als paar, onderlinge stand blijft Gengar), grijns dx -5, dy +6.
# Alleen in de zone x 8-33, y 28-47. Tinten: zie pal.py (E/R/W nu exact Gengars 6/5/1).
import os
import numpy as np
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))+'/'
R=[list(l.rstrip('\n')) for l in open(D+'../sprite_v5/raster.txt')][:64]
V5=[r[:] for r in R]
log=[]
def inzone(x,y): return 8<=x<=33 and 28<=y<=47
def zet(x,y,c,reden):
    assert inzone(x,y),(x,y)
    if R[y][x]!=c: log.append(f'({x},{y}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
# 1) oud gezicht: lijn/rood/tand-pixels binnen de kaders van ogen en grijns
kaders=[(12,18,29,36),(23,32,29,37),(13,32,37,46)]   # x0,x1,y0,y1 (incl.)
gat=set()
for x0,x1,y0,y1 in kaders:
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if R[y][x] in 'KERWHa': gat.add((x,y))
# 2) band één tint lichter (rij 29-40) + overgang bovenaan (rij 28 x24-25) ; wig vlak
for y in range(28,41):
    for x in range(8,34):
        if (x,y) in gat: continue
        c=R[y][x]
        if y==28:
            if x in (24,25) and c=='b': zet(x,y,'m','overgang band: onderrand loopt rond op naar links')
            continue
        if (x,y)==(33,29): continue            # band raakt hier de zonegrens (34,29 = b): geleidelijke rand
        if x==8:
            if c=='a': zet(x,y,'b','randschaduw links één tint lichter (a->b)')
            continue
        if c=='b': zet(x,y,'m','band één tint lichter')
        elif c=='u': zet(x,y,'m','lichte wig/ring vlak met de band')
        elif c=='l' and 19<=x<=26 and y<=34: zet(x,y,'m','lichte wig tussen de ogen vlak met de band')
        elif c=='a' and (x,y)==(10,37): zet(x,y,'m','losse schaduwpixel in de band')
# 3) gaten vullen met de omliggende lijftinten (meerderheid van de buren die geen gat zijn), van buiten naar binnen
open_=set(gat)
while open_:
    nieuw={}
    for (x,y) in open_:
        buren=[R[y+dy][x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and (x+dx,y+dy) not in open_ and R[y+dy][x+dx] in 'mblu']
        if buren: nieuw[(x,y)]=max(set(buren),key=lambda c:(buren.count(c),c=='m'))
    assert nieuw
    for (x,y),c in nieuw.items(): zet(x,y,c,'oud gezicht weg, lijftint van de buren'); open_.discard((x,y))
# 4) Gengar-gezicht 1-op-1
g=np.array(Image.open(D+'../../../../../graphics/pokemon/gengar/anim_front.png'))[:64]
MAP={1:'W',2:'H',3:'G',5:'R',6:'E',7:'H',13:'b',14:'a',15:'K'}   # 1 wit, 2/7 tandschaduw, 3 tandlijn, 5/6 rood, d/e/f
FACE={1,2,3,4,5,6,7,14,15}
delen=[('linkeroog',18,23,28,32,-5,3),('rechteroog',28,36,26,31,-5,3),('grijns',18,38,32,40,-5,6)]
for nm,x0,x1,y0,y1,dx,dy in delen:
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            v=int(g[y,x]); nb=g[y-1:y+2,x-1:x+2].flatten()
            if v in FACE or (v==13 and any(int(n) in {1,2,3,4,5,6,7} for n in nb)):
                if nm=='grijns' and y==32 and x<30: continue   # (20,32),(22,32) horen bij het linkeroog
                zet(x+dx,y+dy,MAP[v],f'Gengar {nm} ({x},{y}) idx {v:x}')
open(D+'raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
open(D+'raster.txt.log','w').write('\n'.join(log)+'\n')
buiten=[(x,y) for y in range(64) for x in range(64) if V5[y][x]!=R[y][x] and not inzone(x,y)]
print(len(log),'wijzigingen; pixels anders dan v5 buiten de zone x8-33,y28-47:',len(buiten))
