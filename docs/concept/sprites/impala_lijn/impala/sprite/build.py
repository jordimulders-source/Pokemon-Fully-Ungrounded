# Volgorde: fg.py -> seg.py -> reduce.py -> build.py rN -> controle.py rN -> vel.py rN -> log.py rN
# Bouwt rN uit de kale reductie (kaal_mode_lab = per cel meest voorkomende modelkleur; kaal_zone = zone uit seg.py)
# 1 omkleuren per zone naar Gen 3-tinten (zilveren vacht, gepolijst staal)  = "kaal gemapt" (basis voor de telling)
# 2 strepen op de bil weg: cellen opnieuw uit het model gelezen zonder de streeppixels (meest voorkomende vachtkleur)
# 3 ontkorrelen (<3 px), 4 binnenlijnen (modellijn binnen het silhouet -> donkerste eigen tint), 5 buitenlijn + selout,
# 6 benoemde reparaties (extra_rN.json) en Jordi's strepen (staart, achterrand dij) als bovenlaag. Alles geteld per zone.
import numpy as np, sys, json
from collections import Counter
from PIL import Image
RN=sys.argv[1] if len(sys.argv)>1 else 'r1'
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#1C1A22'),
     'D':hx('#4A5260'),'S':hx('#6C7686'),'M':hx('#8C98A8'),'N':hx('#AAB4C2'),'L':hx('#C8D2DE'),'W':hx('#F4F7FA'),  # zilveren vacht
     '1':hx('#262C38'),'3':hx('#5E6C80'),'4':hx('#A0B0C4'),'5':hx('#DCE6F0')}                                     # gepolijst staal (+D, W)
ORDER=list(PAL)
L=np.load('kaal_lab.npy'); Z=np.load('kaal_zone.npy'); H,W=L.shape
LF=np.load('kaal_lf.npy'); NLA=np.load('kaal_nla.npy'); LUM=(NLA*[.299,.587,.114]).sum(2)
meta=json.load(open('kaal_meta.json'))
ZN={0:'vacht',1:'staal',2:'kuif',3:'oog',4:'neus',5:'lijn'}
# tint = modelhelderheid van het vlak onder de lijn (per cel), drempels per zone
def tint(z,l):
    if z=='neus': return 'D' if l<140 else 'N'
    if z=='staal': return '1' if l<80 else 'D' if l<115 else '3' if l<150 else '4' if l<190 else '5' if l<225 else 'W'
    return 'D' if l<96 else 'S' if l<128 else 'M' if l<152 else 'N' if l<176 else 'L' if l<222 else 'W'
VACHT={k:('0' if k<=1 else None) for k in range(16)}
g=[['.']*W for _ in range(H)]; zone=[['']*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        v=L[y,x]
        if v<0: continue
        z=ZN[Z[y,x]]; zone[y][x]=z
        g[y][x]='0' if (LF[y,x]>=0.5 or z=='lijn') else tint(z,LUM[y,x])
kaal=[r[:] for r in g]
log=[]
def put(zn,x,y,c,why):
    old=g[y][x]
    if old!=c: g[y][x]=c; log.append((zn,x,y,old,c,why))
OOG=(8,20,15,26)    # oogzone lokaal x0,y0,x1,y1 (beschermd; wordt later vervangen door een Gen 3-oog)
NEUS=(2,26,6,29)
def prot(x,y): return any(a<=x<=c and b<=y<=d for a,b,c,d in (OOG,NEUS))
# --- 2 strepen op de bil weg: cel opnieuw uit het model, zonder de zwarte streeppixels ---
a=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(float)
C=np.load('model_pal.npy'); seg=np.load('seg.npz')['a']; x0,y0,p=meta['x0'],meta['y0'],meta['p']
STREEP=(640,545,775,700)    # modelvak met de vier bilstrepen (x0,y0,x1,y1)
for y in range(H):
    for x in range(W):
        if g[y][x]!='0': continue
        xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
        if not (STREEP[0]<=(xa+xb)/2<=STREEP[2] and STREEP[1]<=(ya+yb)/2<=STREEP[3]): continue
        blk=a[ya:yb,xa:xb]; s=seg[ya:yb,xa:xb]
        ok=(s==685)                      # alleen vachtpixels van het lijf (streep = lijn, valt erbuiten)
        if not ok.any() or any(not (0<=x+dx<W and 0<=y+dy<H) or g[y+dy][x+dx]=='.' for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): continue  # buitenrand laten
        l=(blk[ok].mean(0)*[.299,.587,.114]).sum()
        put('strepen_weg',x,y,tint('vacht',l),'bilstreep weg -> vachttint uit het model (vlak naast de streep)')
# --- 3 ontkorrelen: tintvlakjes <3 px (vacht/kuif) nemen de meest voorkomende buurtint uit dezelfde zone ---
def comps():
    seen=set(); res=[]
    for y in range(H):
        for x in range(W):
            if (x,y) in seen or g[y][x] in '.0': continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); cc=[]
            while st:
                cx,cy=st.pop(); cc.append((cx,cy))
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<W and 0<=ny<H and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            res.append((v,cc))
    return res
for _ in range(3):
    for v,cc in comps():
        if len(cc)>=3 or any(prot(x,y) or zone[y][x]=='staal' for x,y in cc): continue
        nb=Counter(g[y+dy][x+dx] for x,y in cc for dx,dy in((1,0),(-1,0),(0,1),(0,-1))
                   if 0<=x+dx<W and 0<=y+dy<H and g[y+dy][x+dx] not in '.0' and zone[y+dy][x+dx]!='staal' and g[y+dy][x+dx]!=v)
        if nb:
            for x,y in cc: put('ontkorrel',x,y,nb.most_common(1)[0][0],'tintvlakje <3 px naar buurtint')
# --- 4 binnenlijnen: modellijn binnen het silhouet -> donkerste eigen tint (geen zwart) ---
def opaque(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
def buurzone(x,y):
    c=Counter(zone[y+dy][x+dx] for dx in(-1,0,1) for dy in(-1,0,1) if opaque(x+dx,y+dy) and g[y+dy][x+dx]!='0' and zone[y+dy][x+dx] not in('lijn',''))
    return c.most_common(1)[0][0] if c else 'vacht'
DARK={'vacht':'D','kuif':'D','staal':'1','oog':'0','neus':'0'}
inner=[]
for y in range(H):
    for x in range(W):
        if g[y][x]!='0' or prot(x,y): continue
        if all(opaque(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1))): inner.append((x,y))
for x,y in inner: put('binnenlijn',x,y,DARK[buurzone(x,y)],'binnenlijn in donkerste eigen tint')
pre=[r[:] for r in g]   # tinten vóór de buitenlijn (voor selout op dunne delen)
# --- 4b grens hoorn/kop: de modellijn tussen hoorn en kuif/kop valt bij de reductie weg (dunner dan een halve cel);
#     zone-overgang uit de modelsegmentatie -> lijn in de donkerste tint van het onderdeel dat vóór ligt
#     (rechterhoorn ligt vóór de kop: hoornpixel -> '1'; linkerhoorn ligt achter de kuif: kuif/kop-pixel -> 'D')
grens=[]
for y in range(H):
    for x in range(W):
        if g[y][x] in '.0': continue
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if not opaque(nx,ny) or g[ny][nx]=='0': continue
            a_s=zone[y][x]=='staal'; b_s=zone[ny][nx]=='staal'
            if a_s==b_s or zone[y][x]=='lijn' or zone[ny][nx]=='lijn': continue
            if a_s and x>=12: grens.append((x,y,'1'))
            if (not a_s) and b_s and nx<12 and zone[y][x] in ('kuif','vacht'): grens.append((x,y,'D'))
for x,y,c in set(grens): put('hoorngrens',x,y,c,'lijn hoorn/kop uit de zonegrens van het model')
# --- 5 buitenlijn dicht + gekleurde selout aan de lichtkant (boven/links) ---
for y in range(H):
    for x in range(W):
        if g[y][x]=='.' or (prot(x,y) and not (NEUS[0]<=x<=NEUS[2] and NEUS[1]<=y<=NEUS[3])): continue
        if any(not opaque(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) and g[y][x]!='0':
            put('lijn',x,y,'0','buitenlijn dicht')
SELV={'W':'N','L':'M','N':'M','M':'S','S':'D','D':'D','0':'D'}
SELS={'W':'3','5':'3','4':'3','3':'1','1':'1','D':'1','0':'1'}
for y in range(H):
    for x in range(W):
        if g[y][x]!='0' or (prot(x,y) and not (NEUS[0]<=x<=NEUS[2] and NEUS[1]<=y<=NEUS[3])): continue
        # randnormaal uit de transparante buren in een 5x5-venster; selout waar de rand naar boven/linksboven wijst
        tv=[(dx,dy) for dx in range(-2,3) for dy in range(-2,3) if (dx or dy) and not opaque(x+dx,y+dy)]
        if not tv: continue
        nx_=sum(d[0] for d in tv); ny_=sum(d[1] for d in tv); nn=(nx_**2+ny_**2)**.5 or 1
        if not (ny_/nn< -0.35 and nx_/nn<=0.3): continue
        if not opaque(x,y+1) and not opaque(x+1,y): continue
        nb=[(x+dx,y+dy) for dx,dy in((1,0),(0,1),(1,1)) if opaque(x+dx,y+dy) and g[y+dy][x+dx]!='0']
        z=zone[y][x] if zone[y][x] in ('staal','vacht','kuif') else buurzone(x,y)
        if nb: nx,ny=nb[0]; t=g[ny][nx]
        elif pre[y][x]!='0': t=pre[y][x]          # dun deel (hoornpunt): eigen modeltint van de cel
        else: continue
        put('lijn',x,y,(SELS if z=='staal' else SELV).get(t,'D'),'selout lichtkant')
# --- 6 benoemde reparaties + Jordi's strepen (bovenlaag) ---
try: extra=json.load(open(f'extra_{RN}.json'))
except FileNotFoundError: extra=[]
for zn,x,y,c,why in extra: put(zn,x,y,c,why)
OX=(64-W)//2; OY=64-H
img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=[]
for k in ORDER: pal+=PAL[k]
pal+=[0,0,0]*(16-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal)
im.save(f'{RN}/impala_{RN}.png',transparency=0)
im2=Image.open(f'{RN}/impala_{RN}.png').convert('RGBA'); im2.resize((512,512),Image.NEAREST).save(f'{RN}/impala_{RN}_8x.png')
# kaal (gemapt, zonder stappen 2-6) als png
imk=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(W): imk[OY+y,OX+x]=ORDER.index(kaal[y][x])
ik=Image.fromarray(imk,'P'); ik.putpalette(pal); ik.save(f'{RN}/kaal_gemapt.png',transparency=0)
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal]},open(f'{RN}/grid.json','w'),indent=0)
cnt=Counter(z for z,*_ in log)
print(RN,'afwijkingen per zone:',dict(cnt),'totaal',len(log),'van',sum(c!='.' for r in g for c in r),'px; kleuren',len(set(c for r in g for c in r)))
with open(f'{RN}/wijzigingen.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
import sys as _s
if '-q' not in _s.argv: print('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(g)))
