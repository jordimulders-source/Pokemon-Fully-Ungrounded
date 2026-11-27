# Staryu-koekje r4: NIEUW MODEL gemini/r4_staryu.png (driekwart, gekantelde ster; Jordi: "staryu r4 is uitstekend ja").
# Zelfde werkwijze als r1/r2/r3: natief raster 99x99 (pitch 10,24) -> exacte 2x2-reductie (schaal 0,50), figuur vanaf x11, y12.
# Oppervlakteweging per spritepixel; kleine kenmerken (chips, juweel, glans) winnen vanaf een drempel. Daarna alleen technische opschoning
# en reparaties naar het model; lessen keuring r1 + eindkeuring r3 meteen toegepast. Elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap_r4'); from klassen import klassen; from gemeen import *
a,c,L=klassen(r2=True)
UIT='sprite_r4'
H,W=c.shape
# --- voorbewerking klassen (alleen indelen): zwart dat niet aan de achtergrond grenst is een binnenlijn van chip of juweel (model: zwarte onderrand van de chips)
c2=c.copy(); rimm=np.zeros(c.shape,bool)
for v,u in zip(*np.where(c==1)):
    nb=c[max(0,v-1):v+2,max(0,u-1):u+2]
    if (nb==0).any(): continue
    n5=c[max(0,v-2):v+3,max(0,u-2):u+3]
    c2[v,u]=4 if (n5==4).sum()>(n5==2).sum() else 2 if (n5==2).any() else 3
    rimm[v,u]=True
# juweelglans (lichtroze) valt in de chipklasse door lage verzadiging: binnen het juweelvak -> juweel
for v in range(JVAK[0],JVAK[1]+1):
    for u in range(JVAK[2],JVAK[3]+1):
        if c2[v,u]==2 and (c2[max(0,v-2):v+3,max(0,u-2):u+3]==4).sum()>=4: c2[v,u]=4
c=c2; C0J=c2
# toonkaart deeg (r4): het model heeft één vlakke hoofdtint (L 193) met schaduwvlakken (148) en barsten (90-120). Deegtint per spritepixel
# uit de gladgestreken modelhelderheid (5x5, alleen deegpixels), drempels uit de eigen verdeling: zo komt het volume uit het model.
def glad(L,m,r=2):
    p=np.pad(np.where(m,L,0.),r); q=np.pad(m.astype(float),r); H_,W_=L.shape
    s_=sum(p[r+dy:r+dy+H_,r+dx:r+dx+W_] for dy in range(-r,r+1) for dx in range(-r,r+1))
    n_=sum(q[r+dy:r+dy+H_,r+dx:r+dx+W_] for dy in range(-r,r+1) for dx in range(-r,r+1))
    return s_/np.maximum(n_,1)
LG=glad(L,c==3)
def tnD(l): return 3 if l<140 else 4 if l<188 else 5
def tnC(l): return 6 if l<75 else 7
def tnJ(l): return 9 if l<20 else 10 if l<60 else 11 if l<120 else 12 if l<185 else 13   # r4-juweel gemeten: rand 0-3, donkerrood 33-45, rood 80-88, roze 146-155, glans 200
TC=0.35; TJ=0.35; TCH=0.18; TJG=0.20; TK=0.30
o=np.zeros((64,64),int); LGS=np.zeros((64,64))
for Y in range(64):
    for X in range(64):
        f=np.zeros(5); lum=np.zeros(5); fch=0; fjg=0; frim=0; fj={}
        for u,v,w in overlap(X,Y,W,H):
            k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
            if k==2 and L[v,u]>=140: fch+=w
            if k==2 and (rimm[v,u] or L[v,u]<30): frim+=w
            if k==4: t=tnJ(L[v,u]); fj[t]=fj.get(t,0)+w
        tot=f[1:].sum()
        if tot<0.5: continue
        if f[1]>=TK: o[Y,X]=1; continue
        if f[4]>=TJ:
            o[Y,X]=max(fj,key=fj.get); continue   # juweel: meest voorkomende modeltint (geen gemiddelde, anders mengen de strepen)
        if f[2]>=TC:
            o[Y,X]=8 if fch>=TCH else 6 if frim/f[2]>=0.40 else 7; continue
        o[Y,X]=-1; LGS[Y,X]=sum(w*LG[v,u] for u,v,w in overlap(X,Y,W,H) if c[v,u]==3)/max(f[3],1e-9)
dg=o==-1; T5,T3=np.percentile(LGS[dg],[70,22])
o[dg]=np.where(LGS[dg]>=T5,5,np.where(LGS[dg]<T3,3,4))
print('toonkaart drempels: licht >= %.0f, schaduw < %.0f'%(T5,T3))
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if len(sys.argv)>1 and sys.argv[1]=='kaal':
    toon(o,8,60,6,58); sys.exit()

tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
GRP={k:(DEEG if k in DEEG else CHOC if k in CHOC else JUW) for k in range(2,14)}
# --- 1. chipglans: per glanscluster van het model (lichtroze in de chip) precies één glanspixel op de gemeten plek; reductieglans elders -> chipmidden ---
v=o.copy()
o[o==8]=7
A,C0,L0=klassen(r2=True)
lab,n=label((C0==2)&(L0>=140))
for i in range(1,n+1):
    pts=np.argwhere(lab==i); vv,uu=pts.mean(0)
    if JVAK[2]<=uu<=JVAK[3] and JVAK[0]<=vv<=JVAK[1]: continue   # juweelglans, niet een chip
    X=int((uu+.5-U0)*S+X0); Y=int((vv+.5-V0)*S+Y0)
    kand=[(abs(dx)+abs(dy),Y+dy,X+dx) for dy in (-1,0,1) for dx in (-1,0,1) if o[Y+dy,X+dx] in (6,7)]
    if kand: _,yy,xx=min(kand); o[yy,xx]=8
stap('chipglans',v,o)
# --- 1b. juweelrand: het model heeft een gesloten donkere ring (boven/links donkerrood, onder/rechts donkerst); reductie liet gaten ---
v=o.copy()
for Y,X in zip(*np.where(np.isin(o,list(JUW)))):
    nb=lambda dy,dx: o[Y+dy,X+dx] not in JUW
    if nb(1,0) or nb(0,1): o[Y,X]=9
    elif nb(-1,0) or nb(0,-1): o[Y,X]=10 if v[Y,X]!=9 else 9
stap('juweelrand',v,o)
# --- 1c. binnenring juweel: het model heeft een 1-px donkere concentrische ring (L<60, niet aan de rand); bij 0,50x valt hij weg.
#     Elke ringpixel naar zijn spritepixel geprojecteerd -> 10, alleen op rood/roze binnen het juweel (rand en glans niet). ---
v=o.copy()
for vv,uu in zip(*np.where((C0J==4)&(L<60))):
    if not (JVAK[0]<=vv<=JVAK[1] and JVAK[2]<=uu<=JVAK[3]): continue
    if (C0J[vv-2:vv+3,uu-2:uu+3]!=4).any(): continue   # buitenrand van het juweel telt niet
    X=int((uu+.5-U0)*S+X0); Y=int((vv+.5-V0)*S+Y0)
    if o[Y,X] in (11,12): o[Y,X]=10
stap('juweel binnenring',v,o)
# --- 2. buitenlijn: geen open of lichte rand. Achtergrond rechts/onder = zwart (schaduwkant); lichtkant = selout 2. Zwart uit het model blijft zwart. ---
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg)):
        k=o[Y,X]
        if k==1: continue
        bgL=not fg[Y,X-1]; bgR=not fg[Y,X+1]; bgU=not fg[Y-1,X]; bgD=not fg[Y+1,X]
        if not(bgL or bgR or bgU or bgD): continue
        n=1 if (bgR or bgD) else 2
        if n!=k: uit.append((Y,X,n))
    for Y,X,k in uit: o[Y,X]=k
v=o.copy(); rand(o); stap('buitenlijn',v,o)
# --- 3. ontkorrelen deeg: tintvlekjes < 3 px (lichtste < 2) nemen de meest voorkomende deegbuurtint aan; chips, juweel en lijnen niet ---
def ontkorrel(o):
    for k,minim in ((3,3),(4,3),(5,3)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim: continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in (3,4,5) and o[Y+dy,X+dx]!=k]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen deeg',v,o)
# --- 3b. barstjes: de 1-px barstlijnen in het deeg vallen bij 0,56x weg. Elke dunne donkere deegpixel van het model (L<135, weinig donker deeg
#     in zijn 5x5-buurt, >=3 natieve px van de rand) wordt naar zijn spritepixel geprojecteerd en daar deegschaduw (alleen op midden/licht deeg). ---
v=o.copy()
def buren(m,r):
    p=np.pad(m.astype(int),r); return sum(p[r+dy:r+dy+m.shape[0],r+dx:r+dx+m.shape[1]] for dy in range(-r,r+1) for dx in range(-r,r+1))
donker=(C0==3)&(L0<135)
dicht=buren(donker,2)
barst=donker&(dicht<=11)&(buren(C0==0,3)==0)
lb,nb=label(barst)
for i in range(1,nb+1):
    if (lb==i).sum()<6: barst[lb==i]=False   # alleen echte lijnen (>= 6 natieve px), geen losse vlekjes
for vv,uu in zip(*np.where(barst)):
    X=int((uu+.5-U0)*S+X0); Y=int((vv+.5-V0)*S+Y0)
    if o[Y,X] in (4,5): o[Y,X]=3
stap('barstjes',v,o)
# --- 3c. tweede ontkorrelronde alleen voor midden/licht deeg (barstlijnen bevroren): splinters < 3 px tussen barst en licht nemen de buurtint 4/5 aan ---
v=o.copy()
for k in (4,5):
    lab,n=label(o==k,acht=False)
    for i in range(1,n+1):
        m=lab==i
        if m.sum()>=3: continue
        buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in (4,5) and o[Y+dy,X+dx]!=k]
        if buur: o[m]=buur[0]
stap('ontkorrelen na barstjes',v,o)
# --- 4. losse zwarte pixels binnen de figuur -> deegschaduw ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    if all(o[Y+dy,X+dx]!=0 for dy in (-1,0,1) for dx in (-1,0,1)) and not any(o[Y+dy,X+dx]==1 for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): o[Y,X]=3
stap('losse zwarte pixel',v,o)
# --- 5. geen om-en-om zwart/selout op de buitenlijn (les keuring r1 / eindkeuring r3): een lijnpixel waarvan beide lijnburen
#     (8-buren op de rand) de andere lijnkleur hebben, krijgt die kleur. Herhaald tot stabiel. ---
v=o.copy()
def randpix(o):
    fg=o>0; return {(Y,X) for Y,X in zip(*np.where(fg)) if o[Y,X] in (1,2) and (not fg[Y,X-1] or not fg[Y,X+1] or not fg[Y-1,X] or not fg[Y+1,X])}
for _ in range(5):
    R=randpix(o); w=[]
    for Y,X in R:
        nb=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (Y+dy,X+dx) in R]
        if len(nb)==2 and nb[0]==nb[1]!=o[Y,X]: w.append((Y,X,nb[0]))
    for Y,X,k in w: o[Y,X]=k
    if not w: break
stap('om-en-om lijn',v,o)
# --- 6. outline highlights (gids r. 452-456, eindkeuring r3): op de lichtste selout-pixels volgens het model (gem. deeg-L >= 185),
#     binnenbuur licht deeg (5), >= 2 px van zwart -> deegschaduw 3 als lichtere lijn. ---
v=o.copy(); OH=[]; GEMS=[]; TOH=145
for Y,X in zip(*np.where(o==2)):
    ws=[(u,vv,w) for u,vv,w in overlap(X,Y,W,H) if c[vv,u]==3]
    if not ws: continue
    gem=sum(w*L[vv,u] for u,vv,w in ws)/sum(w for *_,w in ws)
    binnen=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] not in (0,1,2)]
    GEMS.append(round(gem))
    if gem>=TOH and 5 in binnen and not (o[max(0,Y-2):Y+3,max(0,X-2):X+3]==1).any(): OH.append((X,Y,round(gem)))
for X,Y,_ in OH: o[Y,X]=3
stap('outline highlights',v,o)
if __name__=='__main__':
    print('outline highlights:',OH); print('selout gem-L:',sorted(GEMS))
    toon(o,8,60,6,58); print(tel, 'totaal',sum(tel.values()))
    opslaan(o,UIT+'/staryu_r4.png')
