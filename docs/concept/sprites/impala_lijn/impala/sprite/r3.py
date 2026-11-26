# r3: reparaties uit de keuring van r2 (r2/keuring/rapport.md, punten 1-10), bovenop r2. Hieronder de r2-beschrijving;
# r3-wijzigingen staan bij de stappen gemarkeerd met 'r3'.
# r2: benoemde reparaties op r1 (opdracht Claude na vergelijking met model/Stantler/maatstaf). Alles uit het model:
# 1 drieslag + volume: per cel de meerderheids-toonklasse van het model (cel-shading -> harde grenzen; celklas.py);
#   binnen de flank de relatieve helderheid van alleen de flankpixels (kaal_flum: <p20 = N, >p85 = H), dus volume
#   alleen waar het model lichter/donkerder is (schouder, bil, onder de kaak, buiklijn). Nieuwe tint H (hooglicht flank).
# 2 hoorns: doorlopende band langs de middellijn van de modelhoorn (hoornskelet.json): 2 px staal (taps naar de punt)
#   + 1 px lijn; lichte strook aan de lichtkant (normaal naar boven/links), donkere reflectie aan de andere kant;
#   witte glinster waar het model op die plek wit is.
# 3 kuif uit de modelzones (toonklassen D/S/M), lijn hoorn/kuif uit de zonegrens; binnenoor uit de modelklassen.
# 4 selout op alle randen die naar boven/links wijzen (donkerste eigen tint), zwart naar rechts/onder.
# 5 strepen 1 px van de buitenlijn af; 6 plukjes uit het model (aandeel zwart in de cel); 7 oogpixels uit r1 bevroren.
import numpy as np, sys, json, math
from collections import Counter
from PIL import Image
RN='r3'
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#1C1A22'),     # r3: vacht ±30 helderheid per stap en neutraler grijs; staal koel blauw + harde witte glans
     'D':hx('#3E434E'),'S':hx('#5B616C'),'M':hx('#787F8A'),'N':hx('#969DA8'),'L':hx('#B5BBC4'),'H':hx('#D5DAE0'),'W':hx('#F5F7F9'),
     '1':hx('#1C2436'),'3':hx('#465A78'),'4':hx('#8A9CBA'),'5':hx('#C6D4E8')}
ORDER=list(PAL)
Z=np.load('kaal_zone.npy'); H,W=Z.shape
LF=np.load('kaal_lf.npy'); CEL=np.load('kaal_cel.npy'); FL=np.load('kaal_flum.npy'); SF=np.load('kaal_sf.npy'); DK=np.load('kaal_dk.npy')
NLA=np.load('kaal_nla.npy'); LUM=(NLA*[.299,.587,.114]).sum(2)
km=json.load(open('kaal_meta.json'))
ZN={0:'vacht',1:'staal',2:'kuif',3:'oog',4:'neus',5:'lijn'}
flank=(Z==0)&(LF<.5)&np.isin(CEL,[3,4])
P20,P85=np.percentile(FL[flank],[20,85])
g=[['.']*W for _ in range(H)]; zone=[['']*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if Z[y,x]<0: continue
        z=ZN[Z[y,x]]; zone[y][x]=z
        if LF[y,x]>=0.5 or z=='lijn': g[y][x]='0'; continue
        c=CEL[y,x]
        if z=='staal': g[y][x]='1' if LUM[y,x]<80 else 'D' if LUM[y,x]<115 else '3' if LUM[y,x]<150 else '4' if LUM[y,x]<190 else '5' if LUM[y,x]<225 else 'W'
        elif z=='kuif': g[y][x]='DSMNNN'[c]
        elif z=='neus': g[y][x]='D' if c<=1 else 'N'
        elif c in (3,4) and z=='vacht': g[y][x]='N' if FL[y,x]<P20 else 'H' if FL[y,x]>P85 else 'L'
        else: g[y][x]='DSMNLW'[c]
kaal=[r[:] for r in g]          # "kaal gemapt": basis voor de telling
log=[]
def put(zn,x,y,c,why):
    old=g[y][x]
    if old!=c: g[y][x]=c; log.append((zn,x,y,old,c,why))
# r3: silhouet uit de modeldekking per cel (kaal_alpha) met een strengere drempel op plekken waar 0,45 de modelvorm afvlakt
AL=np.load('kaal_alpha.npy')
for y in range(35,46):                     # punt 5: bolle bilcurve (achterrand bil, rijen 35-45)
    xs=[x for x in range(33,40) if g[y][x]!='.']
    if xs and AL[y,max(xs)]<0.85: put('bilcurve',max(xs),y,'.','bilrand: modeldekking <85% -> buiten (bolle curve uit het model)')
for y in range(22,32):                     # punt 9: plukjes in de manen (modeldekking <75% -> inkeping)
    xs=[x for x in range(17,24) if g[y][x]!='.']
    if xs and AL[y,max(xs)]<0.75: put('manen',max(xs),y,'.','manenrand: modeldekking <75% -> inkeping (plukje uit het model)')
if AL[17,0]>=0.4 and g[17][0]=='.':        # punt 4: spitse oorpunt links (modeldekking 43%)
    zone[17][0]='vacht'; put('oor',0,17,'S','oorpunt uit het model (dekking 43%)')
for y in range(55,59):                     # punt 7: tussenruimte verre achterhoef / nabije voorpoot
    if g[y][25]!='.' and AL[y,25]<0.9: put('hoef',25,y,'.','tussenruimte hoef/voorpoot (modeldekking <90%)')
# r3 punt 4: oren - toon uit de helderheid van het meerderheidssegment in het model (licht buitenvlak, donkere binnenkant)
segm=np.load('seg.npz')['a']; amod=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(float); lm=(amod*[.299,.587,.114]).sum(2)
def celseg(i,j):
    xa,xb=int(round(km['x0']+i*km['p'])),int(round(km['x0']+(i+1)*km['p'])); ya,yb=int(round(km['y0']+j*km['p'])),int(round(km['y0']+(j+1)*km['p']))
    return segm[ya:yb,xa:xb],lm[ya:yb,xa:xb]
for (bx0,by0,bx1,by1) in ((0,16,6,22),(16,17,23,21)):
    for y in range(by0,by1+1):
        for x in range(bx0,bx1+1):
            if g[y][x] in '.0' or zone[y][x]!='vacht': continue
            sg,ll=celseg(x,y); ok=sg>=0
            if not ok.any(): continue
            ids,c=np.unique(sg[ok],return_counts=True); k=ids[c.argmax()]
            if k==685 and bx0==0: continue
            l=ll[ok&(sg==k)].mean()
            put('oor',x,y,'S' if l<135 else 'M' if l<165 else 'N' if l<190 else 'L','oortint uit de modelhelderheid van het oorsegment')
# r3 punt 6: staart - tinten uit het staartvlak van het model (grijze bovenkant, witte onderkant/punt)
for y in range(28,35):
    for x in range(33,40):
        if g[y][x] in '.0': continue
        sg,ll=celseg(x,y); m=sg==912
        if m.mean()<0.2: continue
        l=ll[m].mean(); wf=(ll[m]>235).mean()
        put('staart',x,y,'W' if wf>=0.35 else 'S' if l<115 else 'M' if l<150 else 'N' if l<200 else 'L','staarttint uit het model')
def opaque(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
r1=json.load(open('r1/grid.json'))['grid']
OOGPX=[(x,y) for y in range(21,26) for x in range(9,14) if r1[y][x] in '0D']   # eigenlijke oogpixels (lokaal) uit r1
OOG=(8,20,15,26); NEUS=(2,26,6,29)
def inbox(b,x,y): return b[0]<=x<=b[2] and b[1]<=y<=b[3]
# --- bilstrepen weg (zoals r1): cel opnieuw uit het model zonder de streeppixels ---
a=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(float)
seg=np.load('seg.npz')['a']; x0,y0,p=km['x0'],km['y0'],km['p']
lumm=(a*[.299,.587,.114]).sum(2)
for y in range(H):
    for x in range(W):
        if g[y][x]!='0': continue
        xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
        if not (640<=(xa+xb)/2<=775 and 545<=(ya+yb)/2<=700): continue
        ok=(seg[ya:yb,xa:xb]==685)
        if not ok.any() or any(not opaque(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): continue
        l=lumm[ya:yb,xa:xb][ok]; l=l[(l>=170)&(l<226)]
        t='L' if not len(l) else 'N' if l.mean()<P20 else 'H' if l.mean()>P85 else 'L'
        put('strepen_weg',x,y,t,'bilstreep weg -> flanktint uit het model naast de streep')
# --- plukjes boven de achterhoeven: cellen in de plukvakken met >=45% zwart in het model -> zwart (ook buiten het silhouet) ---
for (bx0,by0,bx1,by1) in ((785,820,845,900),(630,810,690,890)):     # modelvakken: nabije en verre achterpoot
    for y in range(H):
        for x in range(W):
            cx,cy=x0+(x+.5)*p,y0+(y+.5)*p
            if bx0<=cx<=bx1 and by0<=cy<=by1 and DK[y,x]>=0.45:
                if g[y][x]=='.': zone[y][x]='vacht'
                put('plukjes',x,y,'0','plukje uit het model (aandeel zwart in de cel)')
PLUK=set((x,y) for zn,x,y,*_ in log if zn=='plukjes')
# --- ontkorrelen <3 px (vacht/kuif; niet oog/neus/hoorns) ---
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
        if len(cc)>=3 or any(inbox(OOG,x,y) or inbox(NEUS,x,y) or zone[y][x]=='staal' for x,y in cc): continue
        if any(inbox((0,16,6,22),x,y) or inbox((16,17,23,21),x,y) or inbox((33,28,39,34),x,y) for x,y in cc): continue   # r3: oren/staart (modeldetail, niet wegpoetsen)
        nb=Counter(g[y+dy][x+dx] for x,y in cc for dx,dy in((1,0),(-1,0),(0,1),(0,-1))
                   if 0<=x+dx<W and 0<=y+dy<H and g[y+dy][x+dx] not in '.0' and zone[y+dy][x+dx]!='staal' and g[y+dy][x+dx]!=v)
        if nb:
            for x,y in cc: put('ontkorrel',x,y,nb.most_common(1)[0][0],'tintvlakje <3 px naar buurtint')
# --- binnenlijnen ---
def buurzone(x,y):
    c=Counter(zone[y+dy][x+dx] for dx in(-1,0,1) for dy in(-1,0,1) if opaque(x+dx,y+dy) and g[y+dy][x+dx]!='0' and zone[y+dy][x+dx] not in('lijn',''))
    return c.most_common(1)[0][0] if c else 'vacht'
DARK={'vacht':'D','kuif':'1','staal':'1','oog':'0','neus':'0'}
inner=[(x,y) for y in range(H) for x in range(W) if g[y][x]=='0' and not inbox(OOG,x,y) and not inbox(NEUS,x,y) and (x,y) not in PLUK
       and all(opaque(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)))]
for x,y in inner: put('binnenlijn',x,y,DARK[buurzone(x,y)],'binnenlijn in donkerste eigen tint')
# --- hoorns als band langs de modelmiddellijn ---
SK=json.load(open('hoornskelet.json'))
def nearest(P,px,py):
    best=(1e9,0,0,0,0,0)
    for k in range(len(P)-1):
        ax,ay=P[k]; bx,by=P[k+1]; dx,dy=bx-ax,by-ay; L2=dx*dx+dy*dy or 1e-9
        t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/L2)); qx,qy=ax+t*dx,ay+t*dy; d=math.hypot(px-qx,py-qy)
        if d<best[0]: best=(d,k+t,px-qx,py-qy,dx,dy)
    return best
# r3 punten 1-3: breedte per punt uit de modelhoorn (hw = halve breedte incl. lijn, gladgemaakt): binnenstraal = hw - 1
#   (1 px lijn eromheen), minstens 0,5 (1 px staal) zolang hw >= 1; smaller (punt): alleen lijnpixels.
def straal(HW,i):
    k=int(i); f=i-k; h=HW[k]*(1-f)+HW[min(k+1,len(HW)-1)]*f
    return 0.0 if h<1.0 else max(0.5,h-1.0)
for naam in ('links','rechts'):
    P=SK[naam]['pts']; HW0=SK[naam]['hw']
    HW=[float(np.mean(HW0[max(0,k-2):k+3])) for k in range(len(HW0))]
    band={}; ring={}
    for y in range(H):
        for x in range(W):
            d,i,ox,oy,dx,dy=nearest(P,x+.5,y+.5)
            r=straal(HW,i)
            nx_,ny_=-dy,dx
            if nx_+ny_>0: nx_,ny_=-nx_,-ny_
            nn=math.hypot(nx_,ny_) or 1; proj=(ox*nx_+oy*ny_)/nn
            if r>0 and d<=r: band[(x,y)]=(i,proj,r)
            elif d<=r+1.0 and d>r: ring[(x,y)]=(i,proj,r)
    # mag hier hoorn komen? niet waar de kop/kuif in het model vóór de hoorn ligt (linkerhoorn achter de kuif)
    def vrij(x,y):
        if not (0<=x<W and 0<=y<H): return False
        return Z[y,x]<0 or Z[y,x] in (1,5) or SF[y,x]>=0.15 or (naam=='rechts' and Z[y,x]!=2)
    for (x,y),(i,proj,r) in band.items():
        if not vrij(x,y): continue
        zone[y][x]='staal'
        t=proj/max(r,0.5)
        xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
        hm=np.isin(seg[ya:yb,xa:xb],[14,49]); glim=hm.any() and (lumm[ya:yb,xa:xb][hm]>240).mean()>0.35
        c=('W' if glim else '5') if t>0.3 else '3' if t<-0.3 else ('W' if glim else '4')
        put('hoorn',x,y,c,'hoornband langs de modelmiddellijn (lichtkant 5/glans W, midden 4, schaduwkant 3)')
    for (x,y),(i,proj,r) in ring.items():
        if (x,y) in band and vrij(x,y): continue
        if r==0 and vrij(x,y) and not any((x+dx,y+dy) in band and vrij(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))):
            zone[y][x]='staal'; put('hoorn',x,y,'0','hoornpunt: alleen lijn (taps uit het model)'); continue
        if not vrij(x,y):
            # hoorn achter de kop: lijn op de grens hoort bij de kuif/kop (donkerste eigen tint), alleen waar hij aan de band raakt
            if g[y][x] not in '.0' and any((x+dx,y+dy) in band and vrij(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
                put('hoorngrens',x,y,'1' if zone[y][x]=='kuif' else 'D','lijn hoorn/kuif uit de zonegrens')
            continue
        if any((x+dx,y+dy) in band and vrij(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))):
            if zone[y][x]!='staal' and g[y][x] not in '.0' and naam=='rechts':
                put('hoorngrens',x,y,'1','lijn rechterhoorn over de kop (hoorn ligt voor)'); zone[y][x]='staal'
            else:
                zone[y][x]='staal'; put('hoorn',x,y,'0','hoornband: lijn')
    # resten van de oude hoornreductie buiten band+ring weg (alleen hoorn-/lijncellen dicht bij deze hoorn, boven de kop)
    #   alleen vanaf de rand naar binnen (geen gaten in het silhouet)
    for _ in range(4):
        for y in range(H):
            for x in range(W):
                if g[y][x]=='.' or (x,y) in band or (x,y) in ring: continue
                if not any(not opaque(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): continue
                if Z[y,x] in (1,5) or (Z[y,x]==0 and SF[y,x]>0.05 and y<17):
                    d=nearest(P,x+.5,y+.5)[0]
                    if d<3.2 and (Z[y,x]==1 or y<16): put('hoorn',x,y,'.','oude hoornrest buiten de band weg')
# --- buitenlijn + selout (randen die naar boven/links wijzen) ---
for y in range(H):
    for x in range(W):
        if g[y][x]=='.' or (x,y) in OOGPX: continue
        if any(not opaque(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) and g[y][x]!='0':
            put('lijn',x,y,'0','buitenlijn dicht')
SELV={'kuif':'1','staal':'3'}
for y in range(H):
    for x in range(W):
        if g[y][x]!='0' or (x,y) in PLUK or inbox(NEUS,x,y): continue
        if all(opaque(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): continue
        tv=[(dx,dy) for dx in range(-2,3) for dy in range(-2,3) if (dx or dy) and not opaque(x+dx,y+dy)]
        nx_=sum(d[0] for d in tv); ny_=sum(d[1] for d in tv); nn=(nx_**2+ny_**2)**.5 or 1
        if (nx_+ny_)/nn > -0.25: continue                       # wijst naar rechts/onder -> zwart
        if not any(opaque(x+dx,y+dy) and g[y+dy][x+dx]!='0' for dx,dy in((1,0),(0,1),(1,1),(-1,0),(0,-1))) and zone[y][x]!='staal': continue
        z=zone[y][x] if zone[y][x] in ('staal','vacht','kuif') else buurzone(x,y)
        if z=='kuif': continue      # donkere manen/kuif: lijn blijft zwart (selout '1' zou om en om met zwart staan)
        put('lijn',x,y,SELV.get(z,'D'),'selout lichtkant (donkerste eigen tint)')
# --- r3 punt 8: voorkant kop (lokaal x2-6, y20-26) en de oorpunt links (x0-1, y16-18) is lichtkant: buitenlijn daar selout D, zwart alleen onder neus/kin ---
for y in list(range(16,19))+list(range(20,27)):
    for x in (range(0,2) if y<19 else range(2,7)):
        if g[y][x]=='0' and not opaque(x-1,y) and (x,y) not in OOGPX: put('lijn',x,y,'D','selout voorkant kop (lichtkant)')
# --- zwarte pixels die na de hoornband binnen het silhouet liggen (geen transparante 8-buur) -> binnenlijn, donkerste eigen tint ---
for y in range(H):
    for x in range(W):
        if g[y][x]!='0' or (x,y) in PLUK or inbox(NEUS,x,y) or inbox(OOG,x,y): continue
        vier=all(opaque(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
        los=not any(g[y+dy][x+dx]=='0' for dx in(-1,0,1) for dy in(-1,0,1) if (dx or dy) and opaque(x+dx,y+dy))
        if all(opaque(x+dx,y+dy) for dx in(-1,0,1) for dy in(-1,0,1)) or (vier and los):
            z=zone[y][x] if zone[y][x] in ('staal','vacht','kuif') else buurzone(x,y)
            put('binnenlijn',x,y,{'staal':'1','kuif':'1'}.get(z,'D'),'binnenlijn (na hoornband) in donkerste eigen tint')
# --- Jordi's strepen (bovenlaag, 1 px van de buitenlijn af) en het r1-oog ---
def rand_x(y):   # buitenste zwarte lijnpixel rechts in rij y (lijf)
    xs=[x for x in range(W) if g[y][x]=='0' and not opaque(x+1,y)]
    return max(xs) if xs else None
extra=[]
for y in range(36,43):
    rx=rand_x(y)
    if rx: extra.append(('streep_dij',rx-2,y))
json.dump(extra,open(f'extra_{RN}.json','w'))
for zn,x,y in extra: put(zn,x,y,'0','Jordi: zwarte streep langs de achterrand van de dij (1 px van de lijn af, volgt de bilcurve)')
for zn,x,y in extra:
    if g[y][x+1] in 'LH': put('dijschaduw',x+1,y,'N','pixel tussen dijstreep en buitenlijn -> schaduwtint dij (keuring punt 5)')
for x,y in OOGPX: put('oog',x,y,r1[y][x],'oogpixel uit r1 (bevroren)')
# staartstreep: middellijn van de staart, alleen pixels die niet aan een lijn of de rand raken
STAART=[(36,31),(36,32)]
for x,y in STAART:
    assert all(opaque(x+dx,y+dy) and (g[y+dy][x+dx]!='0' or (x+dx,y+dy) in STAART) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))), (x,y)
for x,y in STAART:
    put('streep_staart',x,y,'0','Jordi: zwarte streep midden in de staart (raakt de buitenlijn niet)')
extra+= [('streep_staart',x,y) for x,y in STAART]
json.dump(extra,open(f'extra_{RN}.json','w'))
OX=(64-W)//2; OY=64-H
pal=[]
for k in ORDER: pal+=PAL[k]
pal+=[0,0,0]*(16-len(ORDER))
def save(G,fn):
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(G[y][x])
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(fn,transparency=0)
import os; os.makedirs(RN,exist_ok=True)
save(g,f'{RN}/impala_{RN}.png'); save(kaal,f'{RN}/kaal_gemapt.png')
Image.open(f'{RN}/impala_{RN}.png').convert('RGBA').resize((512,512),Image.NEAREST).save(f'{RN}/impala_{RN}_8x.png')
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal]},open(f'{RN}/grid.json','w'),indent=0)
with open(f'{RN}/wijzigingen.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
print(RN,dict(Counter(z for z,*_ in log)),'kleuren',len(set(c for r in g for c in r))-1,'+ transparant; P20/P85 flank',round(P20,1),round(P85,1))
print('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(g)))
