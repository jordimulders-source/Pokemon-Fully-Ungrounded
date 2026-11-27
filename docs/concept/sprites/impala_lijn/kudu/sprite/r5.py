# Ronde 5: start vanaf r4 (r4/grid.json, oog B). Reparaties uit de keuring van r4, in volgorde (alles uit model A3).
# Coordinaten hieronder zijn RASTERcoordinaten (spritebeeld x = raster x + 6; y gelijk).
import sys, json, math, numpy as np
from collections import Counter
from PIL import Image
from scipy import ndimage as nd
from reduce import fgmask
HOOFD='B'; OOGVAR=sys.argv[1] if len(sys.argv)>1 and sys.argv[1] in 'ABCD' else HOOFD
RN='r5'; H,W=64,51; x0,p=91,16
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#302418'),
     'L':hx('#F8D888'),'M':hx('#D8A850'),'D':hx('#A07030'),
     'l':hx('#D8AC30'),'m':hx('#B08824'),'d':hx('#7C5A10'),
     'A':hx('#4A4A52'),'3':hx('#8A8A92'),'4':hx('#C8C8CC'),'W':hx('#FFFFFF'),
     'R':hx('#E0A090'),'r':hx('#B06A58'),'K':hx('#5C4434')}
ORDER=list(PAL)
J=json.load(open('r4/grid.json')); g=[list(r) for r in J['grid']]; kaal=[list(r) for r in J['kaal']]; r4=[r[:] for r in g]
LJ=json.load(open('r4/lijnen.json')); GRENS={(x,y) for x,y,t in LJ['grens']}
Am=np.asarray(Image.open('r3/model_A3.png').convert('RGB')).astype(int)
R_,G_,B_=Am[...,0],Am[...,1],Am[...,2]; lum=Am@[.299,.587,.114]; SAT=Am.max(2)-Am.min(2)
LIJN=lum<70
HAAR=(B_<R_*0.31)&(R_>=110)&~LIJN&(lum<200)
VACHT=(~HAAR)&~LIJN&(lum<200)&(R_-B_>60)
HALO=nd.binary_dilation(lum>=200,iterations=4)
FGA=fgmask(Am.astype(np.uint8)); FG=fgmask(np.asarray(Image.open('../referenties/model_r3b.png').convert('RGB')))
def cel(x,y): return slice(y*p,(y+1)*p),slice(x0+x*p,x0+(x+1)*p)
log=[]
def put(zn,x,y,c,why):
    if g[y][x]!=c: log.append((zn,x,y,g[y][x],c,why)); g[y][x]=c
def op(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
N4=((1,0),(-1,0),(0,1),(0,-1)); N8=[(a,b) for a in(-1,0,1) for b in(-1,0,1) if a or b]
def rand(x,y): return any(not op(x+a,y+b) for a,b in N4)
def vachttoon(x,y,TD=160):
    s=cel(x,y); m=VACHT[s]&~HALO[s]
    if m.sum()<30: m=VACHT[s]
    l=lum[s][m].mean(); return 'L' if l>=181 else 'M' if l>=TD else 'D'
# ---------- 1 manen: tint per cel = box-reductie van de modelhelderheid van het haar (gemiddelde zonder lijnpixels);
# strenglijn d alleen waar het model een lijn heeft (lijnfractie in de cel >= LT). De lok-/kamregel van r4 vervalt.
TL,TD_,LT=135,112,0.28
KANAAL=set()
LIJNKANAAL=[(13,28),(13,29),(13,30),(13,31),(13,32),(13,33),(13,34),(14,35),(14,36),(15,37),(15,38)]   # zie punt 2
for y in range(28,39):
    for x in range(12,17):
        if r4[y][x]=='D' and not rand(x,y) and (x,y) not in GRENS: KANAAL.add((x,y))
# strenglijnen: cellen met >= LT modellijn die samen een lijn van >= 3 cellen vormen (8-buren); losse lijncellen = haartint
KAND=set()
for y in range(25,47):
    for x in range(9,30):
        if op(x,y) and not rand(x,y) and (x,y) not in GRENS and r4[y][x] in 'lmdD':
            s=cel(x,y)
            if LIJN[s].mean()>=LT and HAAR[s].sum()+LIJN[s].sum()>VACHT[s].sum(): KAND.add((x,y))
STRENGEN=set(); _seen=set()
for c0 in KAND:
    if c0 in _seen: continue
    st=[c0]; cc=[]; _seen.add(c0)
    while st:
        c=st.pop(); cc.append(c)
        for a,b in N8:
            n_=(c[0]+a,c[1]+b)
            if n_ in KAND and n_ not in _seen: _seen.add(n_); st.append(n_)
    if len(cc)>=3: STRENGEN|=set(cc)
HAARCEL=set()
for y in range(25,47):
    for x in range(9,30):
        if not op(x,y) or rand(x,y) or (x,y) in GRENS: continue
        s=cel(x,y); nh,nv,nl=HAAR[s].sum(),VACHT[s].sum(),LIJN[s].mean()
        if not ((nh>=nv and nh>=40) or (x,y) in KANAAL): continue
        if r4[y][x] not in 'lmdD': continue
        HAARCEL.add((x,y))
        if (x,y) in STRENGEN and (x,y) not in KANAAL: put('manen',x,y,'d','streng: modellijn in de cel (lijnfractie %.2f)'%nl); continue
        m=HAAR[s] if nh>=20 else (VACHT[s]|HAAR[s])
        l=lum[s][m].mean()
        put('manen',x,y,'l' if l>=TL else 'm' if l>=TD_ else 'd','haartint: box-reductie modelhelderheid %.0f'%l)
# netheid (SPRITE_KERN): tintvlakjes < 3 px in het haar naar de meest voorkomende buurtint (geen middeling)
def comps(cells):
    seen=set(); res=[]
    for c0 in cells:
        if c0 in seen: continue
        v=g[c0[1]][c0[0]]; st=[c0]; seen.add(c0); cc=[]
        while st:
            cx,cy=st.pop(); cc.append((cx,cy))
            for dx,dy in N4:
                n_=(cx+dx,cy+dy)
                if n_ in cells and n_ not in seen and g[n_[1]][n_[0]]==v: seen.add(n_); st.append(n_)
        res.append((v,cc))
    return res
# 1-px-wisseling l|m|l in een rij (fijne modeltextuur smaller dan 2 spritepx) leest als streepjescode: de middelste pixel
# neemt de tint van zijn beide buren over (poedelmot-les: minder, grotere vormen op de modelplekken)
G0=[r[:] for r in g]
for y in range(25,47):
    for x in range(10,29):
        if (x,y) in HAARCEL and (x-1,y) in HAARCEL and (x+1,y) in HAARCEL and (x,y) not in STRENGEN:
            a,b,c=g[y][x-1],g[y][x],g[y][x+1]
            if a==c and a in 'lm' and b in 'lm' and b!=a: put('streep',x,y,a,'1-px-wisseling: tint van beide buren')
for _ in range(3):
    for v,cc in comps(HAARCEL):
        if len(cc)>=3 or any(c in STRENGEN for c in cc): continue
        nb=Counter(g[y+b][x+a] for x,y in cc for a,b in N4 if (x+a,y+b) in HAARCEL and g[y+b][x+a]!=v)
        if nb:
            for x,y in cc: put('ontkorrel',x,y,nb.most_common(1)[0][0],'haar: tintvlakje < 3 px naar buurtint')
# ---------- 2 hals: smalle schuine vachtlijn (keurder: (185,145,63) op (13,28),(13,32),(14,36)); per rij de linkerste kolom
# met >= 75% modelvacht -> M (1 px); de rest van het kanaal kreeg in stap 1 de haartint uit het model.
for x,y in LIJNKANAAL: put('hals',x,y,'M','hals: vachtlijn uit het model (1 px, lum 147 -> M)')
# ---------- 3 flank tussen de strepen (x35-41, rij 32-41): L alleen in de bovenrand (rij 32-33) als het model >= 181 geeft
for y in range(32,42):
    for x in range(35,42):
        if g[y][x]=='L' and not (y<=33 and vachttoon(x,y)=='L'): put('flank',x,y,'M','flank: vachttint 3 (M) zoals het model; L alleen bovenrand')
# ---------- 4 kam: puntige lokken uit de modelomtrek: cellen met >= 25% model-voorgrond aan de rugrand erbij (tips)
# model op halve cellen: punten op (25-26,25), (27-28,26), (29,27) met inkepingen ertussen (kleiner dan 1 px);
# (29,27) en (29,28) hebben 28% / 75% voorgrond en ontbraken -> erbij. Onder elke punt loopt in het model een lijn
# terug de massa in: (25,26) 50%, (27,27) 38%, (28,27) 27% lijn -> d (te kort voor de strengregel van >= 3 cellen).
for x,y in [(29,27),(29,28)]:
    if g[y][x]=='.': put('kam',x,y,'d','kampunt uit de modelomtrek (voorgrond %d%%)'%(FGA[cel(x,y)].mean()*100))
for x,y in [(25,26),(27,27)]:
    put('kam',x,y,'d','lijn onder een kampunt (modellijn %d%%)'%(LIJN[cel(x,y)].mean()*100))
# ---------- 5 buiksikkel (rij 43-45, x28-39): schaduwgrens uit het model met grens 150 i.p.v. 160 -> gebogen bovengrens
for y in range(43,46):
    for x in range(28,40):
        if g[y][x] in 'MD' and not rand(x,y): put('buik',x,y,vachttoon(x,y,150),'buiksikkel: vachttint uit model (D < 150)')
# ---------- 8 linkerhoorn middenstuk: lichte voorkant uit de modeltonen (lichtfractie >= 20%, gemeten): rij 6-9 rechts
# (model: licht in kolom 9-10), rij 10-11 links (model: licht in kolom 6-7) -> 4
for x,y in [(9,7),(9,8),(9,9),(7,10),(6,11)]:
    if g[y][x]=='3': put('hoorn',x,y,'4','hoorn: lichte voorkant van de draai (modellichtfractie)')
# ---------- 7 oog: wisselen (alle variantpixels eerst terug naar vacht/wit uit het model, dan de gekozen variant)
import oog4
for v in 'ABCD':
    for x,y,c,_ in oog4.variant(v):
        s_=cel(x,y); wf=(lum[s_]>=215).mean()
        put('oog',x,y,'W' if wf>=0.3 else vachttoon(x,y),'oogvlak leeg')
for x,y,c,why in oog4.variant(OOGVAR): put('oog',x,y,c,why)
# ---------- 6 belijning: buitenlijn opnieuw voor de veranderde stukken (kam, oren); oorrand lichtkant goud (D) i.p.v. roze
def zone_van(c,y):
    if c in 'LMD': return 'vacht'
    if c in 'lmd': return 'manen'
    if c in '34A' or (c=='W' and y<19): return 'staal'
    if c in 'Rr': return 'roze'
    if c=='K': return 'donker'
    return 'vacht'
SEL={'vacht':'D','manen':'d','staal':'A','roze':'D','donker':'0'}     # roze: oorrand in modelgoud (keurder)
for y in range(H):
    for x in range(W):
        if g[y][x]=='.' or not rand(x,y): continue
        if g[y][x] not in '0Ddr': continue
        if not (y<=31 and x>=20) and not (14<=y<=22 and (x<=6 or 17<=x<=23)): continue   # alleen kam en oren opnieuw
        if (x,y) in GRENS: continue
        tv=[(a,b) for a in range(-2,3) for b in range(-2,3) if (a or b) and not op(x+a,y+b)]
        nx_=sum(d[0] for d in tv); ny_=sum(d[1] for d in tv); nn=math.hypot(nx_,ny_) or 1; nx_/=nn; ny_/=nn
        bin_=[g[y+b][x+a] for a,b in N8 if op(x+a,y+b) and not rand(x+a,y+b) and g[y+b][x+a] not in '0']
        z=zone_van(Counter(bin_).most_common(1)[0][0],y) if bin_ else 'vacht'
        licht=(ny_<-0.35 and nx_<=0.3) or (nx_<-0.6 and ny_<=0.2)
        c=SEL[z] if (licht and bin_) else '0'
        if c!='0' and Counter(bin_).most_common(1)[0][0]==c: c='0'
        put('lijn',x,y,c,'buitenlijn opnieuw (lichtkant selout, oorrand goud)')
# linkerrand linkeroor (1,20),(1,21): wijst naar linksonder, maar de lijngenoot (impala) zet de hele linkerkant in selout;
# keurder: selout i.p.v. zwart -> oorrand goud D. De onderrand van het oor (rij 22, x2-5) wijst recht omlaag: blijft zwart.
for x,y in [(1,20),(1,21)]: put('lijn',x,y,'D','linkerrand oor: selout in modelgoud (keurder)')
# ---------- uitvoer ----------
OX=(64-W)//2; OY=64-H
def png(G,pad):
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(G[y][x])
    pal=[v for k in ORDER for v in PAL[k]]; pal+=[0]*(48-len(pal))
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(pad,transparency=0)
naam=f'kudu_{RN}' if OOGVAR==HOOFD else f'kudu_{RN}_oog{OOGVAR}'
png(g,f'{RN}/{naam}.png'); Image.open(f'{RN}/{naam}.png').convert('RGBA').resize((512,512),Image.NEAREST).save(f'{RN}/{naam}_8x.png')
if OOGVAR==HOOFD:
    json.dump({'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal]},open(f'{RN}/grid.json','w'))
    with open(f'{RN}/wijzigingen.txt','w') as f:
        for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
    OOGPX={(a,b) for v in 'ABCD' for a,b,*_ in oog4.variant(v)}
    def zk(x,y):
        c=g[y][x] if g[y][x]!='.' else kaal[y][x]
        if (x,y) in OOGPX: return 'oog'
        if y<19 and c in '34WA0': return 'staal'
        return zone_van(c,y) if c!='0' else 'lijn'
    eind=Counter(); r4d=Counter()
    for y in range(H):
        for x in range(W):
            if g[y][x]!=kaal[y][x]: eind[zk(x,y)]+=1
            if g[y][x]!=r4[y][x]: r4d[zk(x,y)]+=1
    with open(f'{RN}/telling.txt','w') as f:
        f.write('Pixels anders dan de kale reductie van model A3, per zone: %s, totaal %d van %d\n'%(dict(eind),sum(eind.values()),sum(c!='.' for r in g for c in r)))
        f.write('Pixels anders dan r4, per zone: %s, totaal %d\n'%(dict(r4d),sum(r4d.values())))
        f.write('Per stap (log): %s\n'%dict(Counter(z for z,*_ in log)))
    print(open(f'{RN}/telling.txt').read())
print('kleuren',len(set(c for r in g for c in r)))
if '-v' in sys.argv: print('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(g)))
