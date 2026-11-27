# Ronde 4 (verse maker): start vanaf r3 (r3/grid.json), alles uit model A3 (r3/model_A3.png) gemeten.
# 1 nek/hals: zones per modelpixel op KLEUR (haar = b < 0,31 r; vacht = goud met b hoger), niet meer met de rechthoek
#   uit zones.py (die maakte de onderkant van de wang tot manen: kop en hals liepen in elkaar over).
# 2 manen: modelgoud (iets donkerder dan de vacht, niet bruin), toon per cel = meerderheid van de modelhaartonen.
# 3 hoorns: neutraal staal; tint per pixel uit het model.  4 flank: vachttint per cel uit de modelhelderheid.
# 5 oog: zwart oog (zie oog4.py), wisselen met argument.  6 buitenlijn/selout opnieuw.
import sys, json, math, numpy as np
from collections import Counter
from PIL import Image
from scipy import ndimage as nd
HOOFD='B'   # oogvariant in kudu_r4 (Ponyta + lid uit het model); wisselen: python3 r4.py A|B|C|D
RN='r4'; OOGVAR=sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('-') else HOOFD
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#302418'),
     'L':hx('#F8D888'),'M':hx('#D8A850'),'D':hx('#A07030'),
     'l':hx('#D8AC30'),'m':hx('#B08824'),'d':hx('#7C5A10'),
     'A':hx('#4A4A52'),'3':hx('#8A8A92'),'4':hx('#C8C8CC'),'W':hx('#FFFFFF'),
     'R':hx('#E0A090'),'r':hx('#B06A58'),'K':hx('#5C4434')}
ORDER=list(PAL)
H,W=64,51; x0,y0,p=91,0,16
J=json.load(open('r3/grid.json')); g=[list(r) for r in J['grid']]; kaal=[list(r) for r in J['kaal']]
r3=[r[:] for r in g]
Am=np.asarray(Image.open('r3/model_A3.png').convert('RGB')).astype(int)
R_,G_,B_=Am[...,0],Am[...,1],Am[...,2]; lum=Am@[.299,.587,.114]
LIJN=lum<70
HAAR=(B_<R_*0.31)&(R_>=110)&~LIJN&(lum<200)
VACHT=(~HAAR)&~LIJN&(lum<200)&(R_-B_>60)
WIT=(lum>=200)&(Am.min(2)<250)
def cel(x,y): return slice(y*p,(y+1)*p),slice(x0+x*p,x0+(x+1)*p)
log=[]
def put(zn,x,y,c,why):
    if g[y][x]!=c: log.append((zn,x,y,g[y][x],c,why)); g[y][x]=c
def op(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
N4=((1,0),(-1,0),(0,1),(0,-1)); N8=[(a,b) for a in(-1,0,1) for b in(-1,0,1) if a or b]
def rand(x,y): return any(not op(x+a,y+b) for a,b in N4)
ZONE=[['']*W for _ in range(H)]
# ---------- 1+2+4: hals, manen, vacht (rijen 23-49, alleen pixels binnen het silhouet; oog/oor/neus/gezichtswit blijven) ----------
OOGBOX=(9,20,15,25)
TL,TD=140,108   # modelhaar: licht 204,168,48 / 192,156,36 / 180,144,36 (lum 142-164), midden 156,120,24 en 144,108,12 (113-121), streng 84,60,0
def haartoon(x,y):
    s=cel(x,y); m=HAAR[s]; l=lum[s][m]
    c=[(l>=TL).sum(),((l>=TD)&(l<TL)).sum(),(l<TD).sum()]
    return 'lmd'[int(np.argmax(c))]
HALO=nd.binary_dilation(lum>=200,iterations=4)     # lichte rand rond de witte strepen telt niet mee (gaf L-vlekken tussen de strepen)
def vachttoon(x,y):
    s=cel(x,y); m=VACHT[s]&~HALO[s]
    if m.sum()<30: m=VACHT[s]
    l=lum[s][m].mean()
    return 'L' if l>=181 else 'M' if l>=160 else 'D'
for y in range(23,50):
    for x in range(W):
        if not op(x,y) or rand(x,y): continue
        if y>=46 and r3[y][x] in 'LMD': continue          # poten: Kirlia-tinten uit r3 blijven (schaduw daar is geen haar)
        if g[y][x] in 'RrK' or (OOGBOX[0]<=x<=OOGBOX[2] and OOGBOX[1]<=y<=OOGBOX[3]): continue
        if g[y][x]=='W': ZONE[y][x]='wit'; continue          # gezichtswit en flankstrepen (r3: doorlopende lijnen) blijven
        s=cel(x,y); nh,nv,nl=HAAR[s].sum(),VACHT[s].sum(),LIJN[s].sum(); tot=float(s[0].stop-s[0].start)*16
        if nl>=0.3*tot:
            # modellijn: in het haar een streng (d), in de vacht een binnenlijn (D); keuze op de meerderheid van de buren
            ZONE[y][x]='haarlijn' if nh>=nv else 'vachtlijn'; continue
        if nh>=nv and nh>=40: ZONE[y][x]='manen'; put('manen',x,y,haartoon(x,y),'haartoon = meerderheid modelhaar in de cel')
        elif nv>=40: ZONE[y][x]='vacht'; put('vacht',x,y,vachttoon(x,y),'vachttoon uit modelhelderheid (L>=181, M>=150)')
for y in range(23,50):
    for x in range(W):
        if ZONE[y][x]=='haarlijn': put('manen',x,y,'d','modellijn in het haar: streng/lokgrens (donkerste haartint)'); ZONE[y][x]='manen'
        elif ZONE[y][x]=='vachtlijn':
            nb=Counter(ZONE[y+b][x+a] for a,b in N8 if 0<=y+b<H and 0<=x+a<W)
            if nb['manen']>nb['vacht']: put('manen',x,y,'d','modellijn: rand van een lok over de vacht (d)'); ZONE[y][x]='manen'
            else: put('vacht',x,y,'D','modellijn in de vacht: binnenlijn donkerste eigen tint'); ZONE[y][x]='vacht'
# ---------- 2b: strengen = skelet van de zwarte modellijnen in het haar (4x verkleind, Zhang-Suen), componenten >= 4 cellen hoog ----------
from hoorn import thin
yy,xx=np.mgrid[:1024,:1024]
hz=nd.binary_dilation(HAAR,iterations=6)
lm=(lum<80)&hz&(yy>=23*16)&(yy<46*16)&(xx<x0+34*16)
sk=thin(lm.reshape(256,4,256,4).max((1,3))); lab,n=nd.label(sk,structure=np.ones((3,3)))
STR={}; PRIO={}
for k in range(1,n+1):
    ys,xs=np.nonzero(lab==k)
    if ys.max()-ys.min()<16: continue
    for yv,xv in zip(ys,xs):
        c=((xv*4+2-x0)//p,(yv*4+2)//p); STR[c]=STR.get(c,0)+1; PRIO[c]=max(PRIO.get(c,0),len(ys))
# per rij: strengcellen op prioriteit (lengte van de modellijn, dan hoeveelheid skelet in de cel); een cel binnen 2 kolommen
# van een al gekozen streng valt af, zodat elke lok tussen twee strengen >= 2 px breed is (r2/r3: "dldld"-zebra)
STRENG=set()
for y in range(H):
    kand=[(x,yy_) for (x,yy_) in STR if yy_==y and 0<=x<W and ZONE[y][x]=='manen' and STR[(x,yy_)]>=2]
    kand.sort(key=lambda c:(-PRIO[c],-STR[c]))
    for c in kand:
        if any((c[0]+a,y) in STRENG for a in (-2,-1,1,2)): continue
        STRENG.add(c)
for y in range(H):
    for x in range(W):
        if ZONE[y][x]=='manen' and g[y][x]=='d' and (x,y) not in STRENG and not rand(x,y):
            # d zonder skelet: haartoon terug (alleen het skelet is lijn)
            put('manen',x,y,haartoon(x,y) if HAAR[cel(x,y)].sum()>=20 else 'm','geen strengskelet: haartoon')
for (x,y) in STRENG: put('manen',x,y,'d','streng: skelet van de modellijn')
# lokken: per rij is elk stuk haar tussen twee strengen (of streng en buitenlijn) een lok; licht komt van links, dus per lok
# links l, rechts m (breedte 1: m, 2: l m, 3: l l m, 4: l l m m). Per rij uit het model gemeten gaf speckle (r3: "bruine blokken").
for y in range(23,47):
    seg=[];cur=[]
    for x in range(W):
        if ZONE[y][x]=='manen' and (x,y) not in STRENG and g[y][x] in 'lmd' and not rand(x,y): cur.append(x)
        else:
            if cur: seg.append(cur)
            cur=[]
    if cur: seg.append(cur)
    for sg in seg:
        n_=len(sg); nl=(n_+1)//2 if n_!=1 else 0
        if n_>=4: nl=n_//2
        for i,x in enumerate(sg): put('lok',x,y,'l' if i<nl else 'm','lok: licht links (l), donker rechts (m)')
# kam over de rug (x >= 21, rij 25-31): in het model liggen de lokken daar liggend/schuin naar rechts (lijnen naar rechtsonder),
# dus de lokregel gaat per KOLOM: strengen = skelet van de modellijnen (per kolom 1 cel binnen 2 rijen), tussen twee strengen
# boven l (licht van boven), onder m.
KAM=lambda x,y: x>=21 and 25<=y<=31 and ZONE[y][x]=='manen'
for (x,y) in list(STRENG):
    if KAM(x,y): STRENG.discard((x,y)); put('kam',x,y,'m','kam: eerst terug naar haartint')
kk=[(x,y) for (x,y) in STR if 0<=x<W and 0<=y<H and KAM(x,y) and STR[(x,y)]>=2]
kk.sort(key=lambda c:(-PRIO[c],-STR[c]))
for c in kk:
    if any((c[0],c[1]+b) in STRENG for b in (-2,-1,1,2)): continue
    STRENG.add(c); put('kam',c[0],c[1],'d','kam: streng = skelet modellijn (liggende lok)')
for x in range(21,W):
    seg=[];cur=[]
    for y in range(25,32):
        if KAM(x,y) and (x,y) not in STRENG and not rand(x,y): cur.append(y)
        else:
            if cur: seg.append(cur)
            cur=[]
    if cur: seg.append(cur)
    for sg in seg:
        n_=len(sg); nl=0 if n_==1 else (n_+1)//2 if n_<4 else n_//2
        for i,y in enumerate(sg): put('kam',x,y,'l' if i<nl else 'm','kam: lok licht boven (l), donker onder (m)')
# ---------- 1b: grenzen die de hals laten lezen (lijnkaart: r4/lijnkaart_hals.png) ----------
# a) rand van de manen over de vacht (schouder, lokpunten op de borst): haarcel met een vachtbuur waar het model een zwarte
#    lijn heeft (>= 12% lijnpixels in het venster van 1,5 cel rond de cel) -> d
GRENS=[]
def lijnvenster(x,y):
    ya,yb=max(0,int((y-0.25)*p)),int((y+1.25)*p); xa,xb=int(x0+(x-0.25)*p),int(x0+(x+1.25)*p)
    return LIJN[ya:yb,xa:xb].mean()
for y in range(26,47):
    for x in range(W):
        if ZONE[y][x]!='manen' or (x,y) in STRENG or rand(x,y): continue
        if any(0<=y+b<H and 0<=x+a<W and ZONE[y+b][x+a]=='vacht' and g[y+b][x+a] in 'LM' for a,b in N4) and lijnvenster(x,y)>=0.12:
            put('grens',x,y,'d','manenrand over de vacht: modellijn (donkerste haartint)'); GRENS.append((x,y,'manen/vacht'))
# b) kaaklijn: onderrand van de wang die over de hals valt (model: zwarte lijn van (8,28.5) via (13,27.5) naar (14.5,23)),
#    binnenlijn in de donkerste vachttint D; mond: wit lip (7,28), rest uit r3
KAAK=[(8,28),(9,28),(10,28),(11,28),(12,28),(13,27),(14,26),(14,25),(14,24)]
for x,y in KAAK: put('kaak',x,y,'D','kaaklijn: onderrand wang over de hals (modellijn), donkerste vachttint'); ZONE[y][x]='vacht'; GRENS.append((x,y,'kaak'))
for x,y in [(13,28),(14,27),(15,26),(15,25),(15,24),(15,23),(14,28)]:
    if ZONE[y][x]!='manen' and g[y][x] in 'LMD':
        hk=haartoon(x,y) if HAAR[cel(x,y)].sum()>=20 else 'm'; put('kaak',x,y,hk,'onder/achter de kaaklijn: haar (model)'); ZONE[y][x]='manen'
for x in range(9,13):
    if ZONE[29][x]!='manen' or g[29][x]=='D':
        hk=haartoon(x,29) if HAAR[cel(x,29)].sum()>=20 else 'm'; put('kaak',x,29,hk,'onder de kaaklijn: haar (model)'); ZONE[29][x]='manen'
put('mond',4,28,r3[28][4],'mond: r3 terug'); put('mond',7,28,'W','lip: wit in het model')
json.dump({'g':[''.join(r) for r in g]},open(f'{RN}/_stap1.json','w'))
# ---------- 3: hoorns. Vorm (band) uit r3; binnenkant per pixel = meerderheid van de modelstaaltonen in de cel:
# wit (lum >= 215: voorkant van de draai / slijprand) -> W, lichtgrijs (165-215) -> 4, grijs (< 165: achterkant) -> 3.
# Zo leest de spiraal zoals in het model: per draai een wit stuk en een grijs stuk (r3: W/4/3 door elkaar per pixel).
SAT=Am.max(2)-Am.min(2)
from reduce import fgmask
FG=fgmask(np.asarray(Image.open('../referenties/model_r3b.png').convert('RGB')))
HOORNPX=[]
for y in range(0,19):
    for x in range(W):
        if g[y][x] not in '34W' or (y>=12 and x<6 and g[y][x]=='W' and False): continue
        sl=cel(x,y); l=lum[sl]; st=(SAT[sl]<30)&(l>=70)&FG[sl]
        if st.sum()<10: continue
        v=l[st]; cnt=[(v>=215).sum(),((v>=165)&(v<215)).sum(),(v<165).sum()]
        HOORNPX.append((x,y)); put('hoorn',x,y,'W43'[int(np.argmax(cnt))],'hoorn: meerderheid modelstaal (wit/lichtgrijs/grijs)')
# losse hoornpixels (geen 4-buur met dezelfde tint binnen de hoorn) naar de buurtint die het vaakst voorkomt
for _ in range(2):
    for x,y in HOORNPX:
        c=g[y][x]; nb=[g[y+b][x+a] for a,b in N8 if 0<=y+b<H and 0<=x+a<W and g[y+b][x+a] in '34W']
        if nb and not any(0<=y+b<H and 0<=x+a<W and g[y+b][x+a]==c for a,b in N4):
            put('hoorn',x,y,Counter(nb).most_common(1)[0][0],'hoorn: losse pixel naar buurtint')
# hoornbult: rij 8 van de linkerhoorn steekt 1 px uit (model: hoorn x 7,7-9,6 incl. lijn) -> rechterlijn op x10 zoals rij 7 en 9
put('hoorn',11,8,'.','hoornbult weg: rechterrand gelijk aan rij 7/9 (model)'); put('hoorn',10,8,'0','hoornrand')
# ---------- 5: oog ----------
import oog4
for y in range(21,27):
    for x in range(9,15):
        if g[y][x] in '0WKLD' and not rand(x,y) and not (x<10 and g[y][x]=='W'):
            s_=cel(x,y); wf=(lum[s_]>=215).mean()
            put('oog',x,y,'W' if wf>=0.3 else vachttoon(x,y),'oogvlak leeg: r3-oog (impala) weg, vacht/wit uit het model')
for x,y,c,why in oog4.variant(OOGVAR): put('oog',x,y,c,why)
# ---------- ontkorrelen: tintvlakjes < 3 px in vacht/manen naar de buurtint (niet op strengen/grenzen/oog) ----------
VAST=set(STRENG)|{(x,y) for x,y,_ in GRENS}|{(x,y) for x,y,*_ in oog4.variant(OOGVAR)}
def comps():
    seen=set(); res=[]
    for y in range(H):
        for x in range(W):
            if (x,y) in seen or g[y][x] not in 'LMDlm': continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); cc=[]
            while st:
                cx,cy=st.pop(); cc.append((cx,cy))
                for dx,dy in N4:
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<W and 0<=ny<H and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            res.append((v,cc))
    return res
for _ in range(2):
    for v,cc in comps():
        if len(cc)>=3 or any(c in VAST for c in cc): continue
        grp='LMD' if v in 'LMD' else 'lm'
        if grp=='lm': continue      # lokken: l/m-paren per rij zijn bewust (licht links, donker rechts)
        nb=Counter(g[y+b][x+a] for x,y in cc for a,b in N4 if op(x+a,y+b) and g[y+b][x+a] in grp and g[y+b][x+a]!=v)
        if nb:
            for x,y in cc: put('ontkorrel',x,y,nb.most_common(1)[0][0],'tintvlakje < 3 px naar buurtint')
# ---------- 6: buitenlijn + selout opnieuw (licht linksboven): rand die naar boven of links wijst = selout in de donkerste
# eigen tint, de rest zwart (lijnkleur 0). Hoeven blijven zoals r3 (zwart rechts/onder, K binnen).
def zone_van(c,y):
    if c in 'LMD': return 'vacht'
    if c in 'lmd': return 'manen'
    if c in '34A' or (c=='W' and y<19): return 'staal'
    if c in 'Rr': return 'roze'
    if c=='K': return 'donker'
    return 'vacht'
SEL={'vacht':'D','manen':'d','staal':'A','roze':'r','donker':'0'}
for y in range(H):
    for x in range(W):
        if g[y][x]=='.' or not rand(x,y): continue
        if g[y][x] not in '0'+''.join(SEL.values()): continue
        if y>=58 and g[y][x] in '0K': continue
        tv=[(a,b) for a in range(-2,3) for b in range(-2,3) if (a or b) and not op(x+a,y+b)]
        nx_=sum(d[0] for d in tv); ny_=sum(d[1] for d in tv); nn=math.hypot(nx_,ny_) or 1; nx_/=nn; ny_/=nn
        bin_=[g[y+b][x+a] for a,b in N8 if op(x+a,y+b) and not rand(x+a,y+b) and g[y+b][x+a] not in '0']
        z=zone_van(Counter(bin_).most_common(1)[0][0],y) if bin_ else 'vacht'
        licht=(ny_<-0.35 and nx_<=0.3) or (nx_<-0.6 and ny_<=0.2)
        c=SEL[z] if (licht and bin_) else '0'
        if c!='0' and Counter(bin_).most_common(1)[0][0]==c: c='0'     # binnen al de donkerste tint (verre poot): zwart, anders open rand
        put('lijn',x,y,c,'selout lichtkant (donkerste eigen tint)' if c!='0' else 'buitenlijn schaduwkant zwart')
OX=(64-W)//2; OY=64-H
def png(G,pad,schaal=1):
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(G[y][x])
    pal=[v for k in ORDER for v in PAL[k]]; pal+=[0]*(48-len(pal))
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(pad,transparency=0)
if '-1' in sys.argv:
    png(g,f'{RN}/_stap.png')
    print('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(g))); sys.exit()

# losse zwarte pixel tussen selout op dezelfde rand (SPRITE_KERN: nooit om en om): keelfranje (9,37), voorpoot (24,53)
put('lijn',9,37,'d','selout doorlopend: losse zwarte pixel tussen d-selout'); put('lijn',24,53,'D','selout doorlopend: losse zwarte pixel tussen D-selout')
# ---------- uitvoer ----------
naam=f'kudu_{RN}' if OOGVAR==HOOFD else f'kudu_{RN}_oog{OOGVAR}'
png(g,f'{RN}/{naam}.png')
from PIL import Image as _I
im=_I.open(f'{RN}/{naam}.png'); im.convert('RGBA').resize((512,512),_I.NEAREST).save(f'{RN}/{naam}_8x.png')
if OOGVAR==HOOFD:
    json.dump({'streng':[[int(a),int(b)] for a,b in sorted(STRENG)],'grens':[[int(a),int(b),t] for a,b,t in GRENS]},open(f'{RN}/lijnen.json','w'))
    png(kaal,f'{RN}/kaal_gemapt.png')
    json.dump({'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal]},open(f'{RN}/grid.json','w'))
    with open(f'{RN}/wijzigingen.txt','w') as f:
        for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
    def zk(x,y):
        c=g[y][x] if g[y][x]!='.' else kaal[y][x]
        if y<19 and c in '34WA0': return 'staal'
        if (x,y) in VAST and (x,y) in {(a,b) for a,b,*_ in oog4.variant(OOGVAR)}: return 'oog'
        return zone_van(c,y) if c!='0' else 'lijn'
    eind=Counter(); r3d=Counter()
    for y in range(H):
        for x in range(W):
            if g[y][x]!=kaal[y][x]: eind[zk(x,y)]+=1
            if g[y][x]!=r3[y][x]: r3d[zk(x,y)]+=1
    with open(f'{RN}/telling.txt','w') as f:
        f.write('Pixels anders dan de kale reductie van model A3 (kaal gemapt), per zone: %s, totaal %d van %d\n'%(dict(eind),sum(eind.values()),sum(c!='.' for r in g for c in r)))
        f.write('Pixels anders dan r3, per zone: %s, totaal %d\n'%(dict(r3d),sum(r3d.values())))
        f.write('Per stap (log): %s\n'%dict(Counter(z for z,*_ in log)))
        f.write('Strengen: %d cellen; grenscellen: %d\n'%(len(STRENG),len(GRENS)))
    print(open(f'{RN}/telling.txt').read())
print('kleuren',len(set(c for r in g for c in r)))
if '-v' in sys.argv: print('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(g)))
