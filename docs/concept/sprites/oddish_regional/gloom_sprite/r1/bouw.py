# Gloom r1: model overnemen. Natief raster (149x149, pitch 6,83; figuur 106x102) -> schaal 42/102 (0,412), y11-52, x9-52.
# Verkleinen = oppervlakteweging per spritepixel; gloed wint waar het model een kier/kwijl heeft; daarna alleen technische opschoning, elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen()
c[:20]=0; c[122:]=0; c[:,:21]=0; c[:,127:]=0   # alleen de figuur-bbox (rand van het Gemini-plaatje telt niet)
TG=float(sys.argv[1]) if len(sys.argv)>1 else 0.25; TK=float(sys.argv[2]) if len(sys.argv)>2 else 0.30
UIT=sys.argv[3] if len(sys.argv)>3 else 'r1'
TD=float(sys.argv[4]) if len(sys.argv)>4 else 0.18
def toonvan(grp,l,f):
    if grp==2: return 2 if l<52 else 3 if l<74 else 4   # modeltonen steen 39/65/105 -> drempels ertussen
    if grp==3: return 5 if l<52 else 6 if l<88 else (8 if f>=0.35 else 7)
    if grp==4: return 9 if l<128 else 10 if l<162 else 11
    if grp==5: return 12 if l<88 else 13 if l<126 else 14
# --- 1. kale reductie ---
o=np.zeros((64,64),int)
for Y in range(0,64):
    for X in range(0,64):
        f=np.zeros(6); lum=np.zeros(6); licht=0
        for u,v,w in overlap(X,Y):
            k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
            if k==3 and L[v,u]>=112: licht+=w
        if f[1:].sum()<0.5: continue          # minder dan een halve pixel figuur = achtergrond
        mond=(32<=Y<=41 and 18<=X<=34)
        if mond:   # mondring: dunne donkere modellijnen (zwart + donker bordeaux, L<55) winnen vanaf TD (ijskomeet-regel "donkerste wint")
            fz=fd=0
            for u,v,w in overlap(X,Y):
                if c[v,u] in (1,3) and L[v,u]<55: fd+=w; fz+=w*(c[v,u]==1)
            if fd>=TD: o[Y,X]=1 if fz>=fd/2 else 5; continue
        if f[4]>=TG: o[Y,X]=toonvan(4,lum[4]/f[4],0); continue      # gloed wint
        if f[1]>=TK: o[Y,X]=1; continue
        g=2+int(np.argmax(f[2:])); o[Y,X]=toonvan(g,lum[g]/f[g],licht/max(f[3],1e-9))
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')

tel={}
MOND=(slice(32,42),slice(18,35)); inmond=np.zeros((64,64),bool); inmond[MOND]=True
GROOT=(slice(30,48),slice(16,37)); ingroot=np.zeros((64,64),bool); ingroot[GROOT]=True
def stap(n,o_voor,o): tel[n]=tel.get(n,0)+int((o_voor!=o).sum())
# --- 2. lijf buiten het hoofdlijf (verschroeide kelp is roodbruin in het model) -> kelpbruin; steen buiten de lavabrok -> verbrande kelppunt ---
v=o.copy()
lab,n=label(np.isin(o,list(LIJF)),acht=False); hoofd=np.argmax([(lab==i).sum() for i in range(n+1)][1:])+1
for i in range(1,n+1):
    if i==hoofd: continue
    m=lab==i; ys,xs=np.where(m)
    buren=[o[y+dy,x+dx] for y,x in zip(ys,xs) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    if (m&inmond).any(): continue                 # mondring blijft lijf
    if any(b in KELP for b in buren): o[m]=12      # roodbruin ín de kelp (verschroeid) -> kelpbruin
    elif m.sum()<4 and any(b in STEEN|GLOED for b in buren): o[m]=10   # roodoranje kierrand in de steen -> kier (gloed wint)
    elif m.sum()<4: o[m]=12                        # verbrande kelppunt
lab,n=label(np.isin(o,list(STEEN))|((o==1)&False),acht=True); groot=np.argmax([(lab==i).sum() for i in range(n+1)][1:])+1
los=np.isin(o,list(STEEN))&(lab!=groot)
o[los&(o==4)]=3     # houtskoolpunt: geen lichtgrijs
stap('kelp: rood/steen in kelp',v,o)
# --- 3. kieren en kelpranden: één felle gloedtint (oranje), mond houdt zijn tinten ---
v=o.copy(); o[np.isin(o,list(GLOED))&~ingroot]=10; stap('gloed: kieren één tint',v,o)

# --- 4. buitenlijn: geen open of lichte rand. bg rechts/onder = zwart (schaduwkant); lichtkant = selout van de groep; steen altijd zwart; gloedrand blijft (kelppunten) ---
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg)):
        k=o[Y,X]
        if k==1 or k in GLOED: continue
        bgL=not fg[Y,X-1]; bgR=not fg[Y,X+1]; bgU=not fg[Y-1,X]; bgD=not fg[Y+1,X]
        if not(bgL or bgR or bgU or bgD): continue
        if k in STEEN or bgR or bgD: n=1
        else: n=5 if k in LIJF else 12
        if n!=k: uit.append((Y,X,n))
    for Y,X,k in uit: o[Y,X]=k
v=o.copy(); rand(o); stap('buitenlijn',v,o)
# --- 5. ontkorrelen: tintvlekjes < 3 px (hooglicht < 2) nemen de meest voorkomende buurtint van dezelfde groep aan ---
def ontkorrel(o):
    for k,minim in ((2,3),(3,3),(4,2),(6,3),(7,3),(8,2),(13,3),(14,2)):
        lab,n=label(o==k,acht=False)
        grp=STEEN if k in STEEN else LIJF if k in LIJF else KELP
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim: continue
            buur=[]
            for Y,X in zip(*np.where(m)):
                for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                    w=o[Y+dy,X+dx]
                    if w in grp and w!=k and w not in (5,): buur.append(w)
            if k==2 and not (m&inlava).any(): continue     # houtskool kelppunten blijven
            if buur: o[m]=max(set(buur),key=buur.count)
lab,n=label(np.isin(o,list(STEEN|GLOED)),acht=True); inlava=lab==np.argmax([(lab==i).sum() for i in range(n+1)][1:])+1
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)
# --- 6. losse zwarte pixel midden in een vlak (geen zwarte 8-buur, geen achtergrond) -> buurtint ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    nb=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    nb8=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
    if 0 not in nb8 and 1 not in nb8: o[Y,X]=max(set(nb),key=nb.count)
stap('losse zwarte pixels',v,o)

# --- 6b. losse tintpixels die nergens bij horen: steenmiddentint zonder steenbuur -> zwart (rand brok/kelp); 1 px lijfmidden tussen mondring en gloed -> ringlijn; losse diepe gloedpixel aan de kwijlrand -> oranje ---
v=o.copy()
for Y,X in zip(*np.where(o>0)):
    nb=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    if o[Y,X]==3 and not any(n in STEEN for n in nb): o[Y,X]=1
    if inmond[Y,X] and o[Y,X]==7 and not any(n in (7,8) for n in nb): o[Y,X]=5
lab,n=label(o==9,acht=True)
for i in range(1,n+1):
    m=lab==i
    if m.sum()<3 and not (m[34:37]).any(): o[m]=10
stap('losse tintpixels',v,o)
# --- 7. volume (kleur, geen vorm): klein hooglicht op de bolling linksboven van de kop (model is daar vlak middenrood; licht linksboven, Gen 3) ---
v=o.copy()
for X,Y in ((19,27),(20,27),(21,27),(19,28),(20,28)):
    assert o[Y,X]==7,(X,Y,o[Y,X]); o[Y,X]=8
stap('hooglicht (kleur)',v,o)
NAAM=UIT+'/gloom_'+UIT.split('/')[-1]+'.png'
opslaan(o,NAAM); toon(o,10,53,3,55)
print('stappen',tel); print('totaal anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren (excl. transp.)',len(set(o.ravel()))-1,'| figuur px',(o>0).sum())
yy,xx=np.where(o>0); print('bbox x%d-%d y%d-%d'%(xx.min(),xx.max(),yy.min(),yy.max()))
