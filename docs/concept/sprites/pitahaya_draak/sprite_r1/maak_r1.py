# Pitahaya-draak r1: kale reductie (python3 half3.py kaal.png 0 1 78 2 3; fase gekozen uit 9 op ogen + mond)
# -> alleen technische opschoning. Niets getekend.
#  B buitenlijn 1 px: zwart aan de schaduwkant (buitennormaal onder/rechts), selout aan de lichtkant
#    (roze/mauve/amber/wit -> donkerste roze 2, groen -> donkerste groen 8; beide modelkleuren van de dunne lijnen)
#  C ruis: losse vulpixels (cluster van 1, 8-verbonden) in de vultinten nemen de meest voorkomende buurtint
#    uit dezelfde kleurgroep aan; lijnen (1, 2, 8), amber, wit bevroren
#  D gerichte reparaties per pixel naar het model (lijst REP, elk met modelmeting)
import numpy as np; from PIL import Image; from collections import Counter
K=Image.open('kaal.png'); kaal=np.asarray(K).astype(int); pal=K.getpalette()
o=kaal.copy(); log=[]
def zet(y,x,v,stap):
    if o[y,x]!=v: log.append((stap,y,x,o[y,x],v)); o[y,x]=v
GRP={**{i:'roze' for i in (2,3,4,5)},6:'mauve',7:'mauve',**{i:'groen' for i in (8,9,10,11)},12:'amber',13:'amber',14:'wit',1:'zwart'}
# B
m=o>0; pad=np.pad(m,1)
rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
keus={}
for y,x in zip(*np.where(rand)):
    ny=sum(dy for dy in (-1,0,1) for dx in (-1,0,1) if not m[y+dy,x+dx])
    nx=sum(dx for dy in (-1,0,1) for dx in (-1,0,1) if not m[y+dy,x+dx])
    if (ny+0.6*nx)>0: keus[(y,x)]=1
    else: keus[(y,x)]=8 if GRP[o[y,x]]=='groen' else (2 if o[y,x]!=1 else 1)
for (y,x),v in list(keus.items()):   # los stukje van 1 randpixel tussen buren van de andere soort (zwart vs selout)
    nb=[keus[(y+dy,x+dx)] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (y+dy,x+dx) in keus]
    if nb and all((b==1)!=(v==1) for b in nb): keus[(y,x)]=Counter(nb).most_common(1)[0][0]
for (y,x),v in keus.items(): zet(y,x,v,'B')
# C
VUL={3,4,5,6,7,9,10,11}
seen=np.zeros_like(m)
for y0,x0 in zip(*np.where(m)):
    if seen[y0,x0] or o[y0,x0] not in VUL: continue
    v=o[y0,x0]; st=[(y0,x0)]; cl=[]; seen[y0,x0]=1
    while st:
        y,x=st.pop(); cl.append((y,x))
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy,xx=y+dy,x+dx
                if 0<=yy<64 and 0<=xx<64 and not seen[yy,xx] and o[yy,xx]==v: seen[yy,xx]=1; st.append((yy,xx))
    if len(cl)<2:
        for y,x in cl:
            nb=Counter(o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and o[y+dy,x+dx] in VUL and GRP[o[y+dy,x+dx]]==GRP[v] and o[y+dy,x+dx]!=v)
            if nb: zet(y,x,nb.most_common(1)[0][0],'C')
# C2 vlakjes < 3 px (4-verbonden) in de middentinten (roze 3/4, groen 9/10) nemen de meest voorkomende 4-buur
#    uit dezelfde kleurgroep aan (Krassault-ontkorrelen; lichtste tinten 5/11 = glans, lijnen en ogen bevroren)
import sys
if '--zonder-c2' not in sys.argv:
    V2={3,4,9,10}
    seen=np.zeros_like(m)
    for y0,x0 in zip(*np.where(m)):
        if seen[y0,x0] or o[y0,x0] not in V2: continue
        v=o[y0,x0]; st=[(y0,x0)]; cl=[]; seen[y0,x0]=1
        while st:
            y,x=st.pop(); cl.append((y,x))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=y+dy,x+dx
                if 0<=yy<64 and 0<=xx<64 and not seen[yy,xx] and o[yy,xx]==v: seen[yy,xx]=1; st.append((yy,xx))
        if len(cl)<3:
            for y,x in cl:
                nb=Counter(o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx] in VUL and GRP[o[y+dy,x+dx]]==GRP[v] and o[y+dy,x+dx]!=v)
                if nb: zet(y,x,nb.most_common(1)[0][0],'C2')
# D
REP=[(25,30,12,"nabije oog, iris links: lijnregel (3 zwarte modelpx = rand van het ooglid) maakte hem zwart; blok heeft 6 amber px, gemiddeld (184,126,76) -> donker amber"),
     (25,33,12,"nabije oog, iris rechts van de pupil: 2 zwarte modelpx (pupilrand, < 1 spritepx breed) maakten hem zwart; 4 amber px, gemiddeld (200,140,86) -> donker amber"),
     (25,31,14,"nabije oog, glans: model heeft daar een witte glanspixel (255,241,223) linksboven de pupil; viel onder de drempel van 2"),
     (32,28,2,"mondlijn: dunne diagonale modellijn (1 px lum 41 in het blok) viel weg, waardoor de lijn brak tussen (27,32) en (29,31); donkerste roze = modelkleur van de mondlijn")]
for y,x,v,r in REP: zet(y,x,v,'D:'+r)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(sys.argv[sys.argv.index('-o')+1] if '-o' in sys.argv else 'pitahaya_r1.png',transparency=0)
def zone(y,x,v):
    if y<=36: return 'schubpunten' if GRP.get(v)=='groen' else 'hoofd/gezicht'
    if y>=48 and 19<=x<=44: return 'poten'
    if x<=22 or x>=39: return 'armen'
    return 'lijf'
cnt=Counter((s.split(':')[0],zone(y,x,a)) for s,y,x,a,b in log)
for k,v in sorted(cnt.items()): print(k,v)
print('totaal gewijzigd',len(log),'van',(o>0).sum(),'kleuren',len(set(o.ravel()))-1)
open('afwijkingen.txt','w').write('\n'.join(f'{s}\t({x},{y})\t{a}->{b}\t{zone(y,x,a)}' for s,y,x,a,b in log)+'\n')
