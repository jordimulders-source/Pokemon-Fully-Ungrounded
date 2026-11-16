# Ronde 6: reparaties keuring r5 (punten 1-7). Basis r5. Niets getekend: elke tint komt uit een modelmeting
# (modelstats.npy = gem/p15/min natief per spritepixel, tones.npy = aandelen modeltonen, clsfrac.npy = modelklassen).
import numpy as np; from PIL import Image
src=Image.open('r5.png'); pal=src.getpalette(); o=np.asarray(src).astype(int).copy(); r5=o.copy()
MS=np.load('modelstats.npy'); MG=MS[0]
T=np.load('tones.npy'); C=np.load('clsfrac.npy')
GH=(2,3,4,5,6)
FACE=np.zeros((64,64),bool); FACE[9:27,25:42]=True        # x25-41, y9-26 bevroren
WIEL=np.zeros((64,64),bool); WIEL[45:57,20:32]=True       # spookwiel x20-31, y45-56
WHEEL=np.zeros((64,64),bool); WHEEL[39:45,0:5]=True; WHEEL[39:45,14:20]=True
log={}
def mark(pt,x,y,v):
    assert not FACE[y,x], (pt,x,y)
    if o[y,x]!=v: log.setdefault(pt,[]).append((x,y,int(o[y,x]),int(v))); o[y,x]=v
def fg(y,x): return 0<=y<64 and 0<=x<64 and o[y,x]>0
def edge(y,x): return o[y,x]>0 and any(not fg(y+dy,x+dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
def normal(y,x):
    nx=ny=0
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if (dx or dy) and not fg(y+dy,x+dx): nx+=dx; ny+=dy
    return nx,ny
def light_side(y,x):
    nx,ny=normal(y,x); s=nx+ny
    return s<0 or (s==0 and ny<0)
# modeltoon van het vlak (zonder wit en zonder lijn): gemiddelde van natieve pixels 60-240
s_,X0,Y0,oy,XC,k=[float(v) for v in open('../sprite_r2/sprite.meta').read().split()]
na=np.asarray(Image.open('../sprite_r5/natief.png').convert('RGB')).astype(float); NL=na@[0.3,0.59,0.11]
def nxo(mx): return mx if mx<XC else XC+(mx-XC)/k
def vlak(x,y):
    ya,yb=Y0+(y-oy)/s_,Y0+(y+1-oy)/s_; xa,xb=nxo(X0+x/s_),nxo(X0+(x+1)/s_); sw=sv=0
    for yy in range(int(ya),int(np.ceil(yb))):
        for xx in range(int(xa),int(np.ceil(xb))):
            w=(min(yy+1,yb)-max(yy,ya))*(min(xx+1,xb)-max(xx,xa)); v=NL[yy,xx]
            if w>0 and 60<=v<=240: sw+=w; sv+=w*v
    return sv/sw if sw else None
def gtone(v): return 2 if v>=205 else 3 if v>=182 else 4 if v>=120 else 5

def comps(mask,conn8=True):
    seen=np.zeros((64,64),bool); out=[]
    nb=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (conn8 or abs(dy)+abs(dx)==1)]
    for y,x in zip(*np.where(mask)):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; cur=[]
        while st:
            cy,cx=st.pop(); cur.append((cy,cx))
            for dy,dx in nb:
                yy,xx=cy+dy,cx+dx
                if 0<=yy<64 and 0<=xx<64 and mask[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
        out.append(cur)
    return out
# ---------- punt 1: vuist, lichtkant selout groen 5, zwart alleen rechts/onder; geen 9 op de geestrand
FIST=np.zeros((64,64),bool); FIST[4:17,48:58]=True
for y,x in zip(*np.where(FIST)):
    if edge(y,x) and o[y,x] in (1,9,2,3,4,5):
        mark('1 vuist rand',x,y,5 if light_side(y,x) else 1)
# overige 9 op de geestrand (geen hout eromheen): zelfde regel
for y,x in zip(*np.where(o==9)):
    gn=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and fg(y+dy,x+dx)]
    if edge(y,x) and not FACE[y,x] and sum(v in GH for v in gn)>len(gn)/2:
        mark('1 vuist rand',x,y,5 if light_side(y,x) else 1)

# ---------- punt 6: vuist rij 7 x51-54 naar de modeltoon
for x in range(51,55):
    v=vlak(x,7); mark('6 vuist rij 7',x,7,gtone(v))

# ---------- punt 5: schaduwkant geest (kop rechts, arm, vuist): binnenpixels naar de modeltoon
#   model: licht 220 -> 2, overgang licht/schaduw (182-200) -> 3, schaduwband 165 -> 4, diep 100 -> 5; lijn (>=30% natief <60) -> 5
Z5=np.zeros((64,64),bool); Z5[6:22,42:47]=True; Z5[15:23,44:51]=True; Z5[4:17,49:58]=True
for y,x in zip(*np.where(Z5)):
    if FACE[y,x] or o[y,x] not in (2,3,4,5) or edge(y,x): continue
    if (x,y) in [(a,7) for a in range(51,55)]: continue
    if T[4,y,x]/max(T[1:,y,x].sum(),1e-9)>=0.3: mark('5 schaduwkant geest',x,y,5); continue
    v=vlak(x,y)
    if v is not None: mark('5 schaduwkant geest',x,y,gtone(v))

for it in range(3):
    for v in (2,3,4):
        for cp in comps((o==v)&Z5&~FACE,conn8=False):
            if len(cp)>=3: continue
            for (y,x) in cp:
                if edge(y,x): continue
                nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if fg(y+dy,x+dx) and o[y+dy,x+dx] in (2,3,4) and o[y+dy,x+dx]!=v]
                if nb:
                    u,c=np.unique(nb,return_counts=True); mark('5 schaduwkant geest',x,y,int(u[c.argmax()]))
# ---------- punt 2: wagen, per vlak <=3 houttinten, stappen >=30 (gemeten modeltoon)
#   front (x3-23): 7 licht (model 131), 10 midden (roest 116 + naden 99 -> samen 102), 9 donker/ijzer (13: model 75)
#   flank + onderkant: 7 glans, 8 basis (model 90; roest 10 = model 94 -> 8), 9 ijzer (13: model 66, 9: 63 -> 9)
WAG=np.zeros((64,64),bool); WAG[22:51,3:57]=True
WOOD=(7,8,9,10,13)
for y,x in zip(*np.where(WAG)):
    if FACE[y,x] or WHEEL[y,x] or o[y,x] not in WOOD: continue
    v=o[y,x]; front= x<=23 and y<=43
    if front:
        if v==8:   # dichtstbijzijnde fronttint op de modelhelderheid (7=138, 10=108, 9=56)
            nv=min((7,10,9),key=lambda t:abs({7:138,10:108,9:56}[t]-MG[y,x]))
        elif v==13: nv=9
        elif v==9 and not edge(y,x): nv=min((7,10,9),key=lambda t:abs({7:137,10:107,9:55}[t]-MG[y,x]))
        else: nv=v
    else:
        nv={10:8,13:9}.get(v,v)
    mark('2 wagen tinten',x,y,nv)

# ---------- punt 3: spikkels <3 px (8-verbonden) in de wagen weg, tenzij het model daar een vorm >=3 px heeft
# modelvorm in dezelfde tintindeling: dominante modelklasse per pixel, vertaald zoals hierboven
def modeltint(y,x):
    c=C[:,y,x]; front= x<=23 and y<=43
    wood={7:c[7],10:c[10]+(c[8] if front else 0),8:(0 if front else c[8]+c[10]),9:c[9]+c[13]+c[1]}
    t=max(wood,key=wood.get); return t if wood[t]>=0.35 else None
MT=np.zeros((64,64),int)
for y,x in zip(*np.where(WAG)): MT[y,x]=modeltint(y,x) or 0
for it in range(4):
    ch=0
    for v in (7,10,8,9):
        for cp in comps((o==v)&WAG&~FACE&~WHEEL):
            if len(cp)>=3: continue
            # vorm in het model >=3 px op deze plek?
            mm=comps(MT==v)
            keep=any(len(m)>=3 and any(p in m for p in cp) for m in mm)
            if keep: continue
            for (y,x) in cp:
                if edge(y,x): continue
                nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and fg(y+dy,x+dx) and o[y+dy,x+dx] in (7,8,9,10) and o[y+dy,x+dx]!=v]
                if not nb: continue
                u,c=np.unique(nb,return_counts=True); mark('3 spikkels wagen',x,y,int(u[c.argmax()])); ch+=1
    if not ch: break
# rest: spikkels 7/10 in de front die het model niet als vorm >=3 toont (frame x4, rand rij 23) opgaan in de buren
for v in (7,10):
    for cp in comps((o==v)&WAG&~FACE&~WHEEL):
        if len(cp)>=3: continue
        for (y,x) in cp:
            nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if fg(y+dy,x+dx) and o[y+dy,x+dx] in (7,8,9,10) and o[y+dy,x+dx]!=v]
            if nb: u,c=np.unique(nb,return_counts=True); mark('3 spikkels wagen',x,y,int(u[c.argmax()]))
# losse zwarte pixel (39,47) en andere losse 1 in de wagen (niet op de rand, geen lijn >=3)
for cp in comps((o==1)&WAG&~FACE&~WHEEL):
    if len(cp)<3:
        for (y,x) in cp:
            if edge(y,x): continue
            nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and fg(y+dy,x+dx) and o[y+dy,x+dx] in (7,8,9,10)]
            if nb: u,c=np.unique(nb,return_counts=True); mark('3 losse zwarte pixel',x,y,int(u[c.argmax()]))

# ---------- punt 4: wolk, schaduwkant (onder/rechts) buitenlijn zwart, lichtkant groen 5; nooit om en om
CLOUD=np.zeros((64,64),bool); CLOUD[44:64,:]=True
for y,x in zip(*np.where(CLOUD)):
    if o[y,x] in GH and edge(y,x):
        mark('4 wolk buitenlijn',x,y,5 if light_side(y,x) else 1)
mark('4 wolk buitenlijn',52,42,1)

# ---------- punt 7: losse groene snippers (opgaan in het vlak; in een scheur: de scheurtint)
for (x,y) in ((12,24),(62,56),(31,47),(36,50),(45,60),(8,29),(11,29)):
    v=o[y,x]
    nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if fg(y+dy,x+dx) and o[y+dy,x+dx]!=v and o[y+dy,x+dx]!=1]
    if any(n in GH for n in nb) and (x,y)!=(8,29): nb=[n for n in nb if n in GH]
    u,c=np.unique(nb,return_counts=True); mark('7 groene snippers',x,y,int(u[c.argmax()]))

np.save('r6.npy',o)
pal[4*3:4*3+3]=[97,172,106]   # tint 4 donkerder: 148 -> 142, stap 3-4 = 32 (punt 5)
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im.save('sprite.png',transparency=0)
for k_ in sorted(log): print(k_, len(log[k_]), log[k_][:40])
print('totaal',sum(len(v) for v in log.values()))
print('FACE diff',int((o!=r5)[FACE].sum()),' WIEL-binnen diff',int(((o!=r5)&WIEL&~np.array([[edge(y,x) for x in range(64)] for y in range(64)])).sum()))
