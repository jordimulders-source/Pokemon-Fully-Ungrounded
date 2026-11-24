# Capykart eindkeuring_dc: schaduw, kleurtinten en belijning op Dragonfly Cave-niveau.
# Silhouet en lijnposities uit eindkeuring_r17/capykart.png; vorm en tintverdeling uit model_r5 (helderheid per pixel)
# + volume per onderdeel (koepel, licht linksboven). Alleen tinten per pixel; oog/tanden/morrillo vast (alleen lijnkleur).
import sys, json; sys.path.insert(0,'eindkeuring_dc'); sys.path.insert(0,'sprite/r17')
import numpy as np; from PIL import Image
from scipy import ndimage as nd
from delen import delen, BESCHERMD, NAMEN, SRC
import gemeen as g
o,d=delen()
mos=np.asarray(g.model_op_schaal()).astype(float)        # model op spriteschaal (oppervlakgemiddelde, alleen om te METEN)
ML=mos@[.299,.587,.114]
# ---------- palet ----------
PAL=[(152,208,160),   # 0 transparant
 (24,17,28),          # 1 zwart (schaduwkant-lijn)
 (98,44,42),          # 2 B0 bruin lijn / selout (vacht + hout + rood)
 (158,62,54),         # 3 B1 vacht schaduw ; rood blok zijkant
 (190,102,64),        # 4 B2 vacht midden ; hout schaduw
 (216,134,78),        # 5 B3 vacht licht ; hout midden ; zijkant geel blok
 (238,174,104),       # 6 B4 hout licht ; slagschaduw onder dak op geel ; bovenkant rood
 (150,158,176),       # 7 hoepel licht ; bovenkant blauw blok
 (78,76,94),          # 8 hoepel donker ; morrillo ; tandschaduw
 (250,238,184),       # 9 creme: tanden ; glans geel blok
 (240,202,72),        # 10 geel
 (232,90,82),         # 11 rood
 (90,144,210),        # 12 blauw licht
 (58,94,164),         # 13 blauw donker
 (104,174,92),        # 14 groen licht
 (56,122,84)]         # 15 groen donker
K,B0,B1,B2,B3,B4,HL,HD,CR,GE,RO,BL,BD,GL,GD=range(1,16)
RAMP={1:[B2,B3,B4],2:[B1,B2,B3],3:[B1,B2,B3],4:[B1,B2,B3],5:[B1,B2,B3],6:[B1,B2,B3],7:[B1,B2,B3],8:[B0,B1,B2],9:[HD,HL]}
SEL={1:B0,2:B0,3:B0,4:B0,5:B0,6:B0,7:B0,8:B0,9:HD,10:B2,11:B0,12:BD,13:GD,14:B0}
LICHT=np.array([-1.0,-1.15,1.25]); LICHT/=np.linalg.norm(LICHT)
def koepel(mask,R):
    D=nd.distance_transform_edt(mask)
    t=np.clip(D/R,0,1); h=np.sqrt(np.clip(1-(1-t)**2,0,1))*R
    h=nd.gaussian_filter(h*mask,0.6)   # alleen de hoogtekaart (geometrie), niet de kleuren
    gy,gx=np.gradient(h)
    n=np.stack([-gx,-gy,np.ones_like(h)],-1); n/=np.linalg.norm(n,axis=-1,keepdims=True)
    return n@LICHT
# ---------- stap 1: volume per onderdeel (bruin + hoepel) ----------
fig=o!=0; zwart=o==1
ring=np.zeros_like(fig)
for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
    sh=np.zeros_like(fig); 
    ys,xs=np.where(fig)
    yy,xx=ys+dy,xs+dx; buiten=(yy<0)|(yy>63)|(xx<0)|(xx>63)
    t=np.zeros(len(ys),bool); t[buiten]=True
    ok=~buiten; t[ok]=~fig[yy[ok],xx[ok]]
    ring[ys[t],xs[t]]=True
QUANT={1:(.26,.22),2:(.50,.14),3:(.30,.25),4:(.38,.18),5:(.38,.20),6:(.36,.22),7:(.38,.20),8:(.55,.10),9:(.45,.55)}
GEWICHT={1:(.75,1.0),2:(.8,.7),3:(.55,1.0),4:(.9,.8),5:(.9,.7),6:(1.5,.45),7:(1.5,.45),8:(1,.5),9:(.6,1.0)}
STRAAL={1:6,2:4,3:6,4:4,5:4,6:4.5,7:4,8:2.5,9:1.5}
n=np.zeros((64,64),int)       # nieuw palet-index
niveau=np.full((64,64),-1)    # 0 schaduw,1 midden,2 licht
v_all=np.zeros((64,64))
hoepel=d==9
for p in [1,2,3,4,5,6,7,8,9]:
    m=d==p
    if not m.any(): continue
    ext=m.copy()
    if p==1: ext|=(d==14)
    # koepel door hoepel/binnenlijn heen (vorm loopt eronder door)
    door=(hoepel|(zwart&~ring)) if p!=9 else np.zeros_like(m)
    for _ in range(3): ext|=nd.binary_dilation(ext)&door
    lam=koepel(ext,STRAAL[p])
    Lm=ML.copy(); med=np.median(Lm[m]); sd=Lm[m].std()+1e-6
    z=(Lm-med)/sd
    a,b=GEWICHT[p]
    v=a*(lam-lam[m].mean())/(lam[m].std()+1e-6)+b*np.clip(z,-2,2)
    v_all[m]=v[m]
    qs,ql=QUANT[p]
    t1,t2=np.quantile(v[m],[qs,1-ql])
    lv=np.where(v<t1,0,np.where(v>t2,2,1))
    if p==9: lv=np.where(v<t1,0,1)
    niveau[m]=lv[m]
# ---------- stap 2: tintvlekjes < 3 px opruimen (meest voorkomende buurtint binnen hetzelfde onderdeel) ----------
def opruimen(niveau,maxn=2,ronden=3):
    for _ in range(ronden):
        veranderd=0
        for p in range(1,10):
            for lv in (0,1,2):
                m=(d==p)&(niveau==lv)
                lab,k=nd.label(m,structure=np.ones((3,3)))
                for i in range(1,k+1):
                    c=lab==i
                    if c.sum()>maxn: continue
                    rand_=nd.binary_dilation(c,structure=np.ones((3,3)))&~c&(d==p)&(niveau>=0)
                    vals=list(niveau[rand_])
                    if not vals: continue
                    niveau[c]=max(set(vals),key=vals.count); veranderd+=1
        if not veranderd: break
    return niveau
niveau=opruimen(niveau)
# ---------- stap 2b: nerf, plankranden, wielnaaf: alleen waar het model ze heeft (r17-index 2 = modeldonker L<96) ----------
detail=np.zeros((64,64),int)   # 1 = een tintstap donkerder, 2 = naad (B0)
lc=ML-nd.median_filter(ML,size=5)
for y in range(64):
    for x in range(64):
        p=d[y,x]
        if p not in (1,2,3,4,5,6,7,8) or ring[y,x]: continue
        if o[y,x]==2 or lc[y,x]<-28:
            detail[y,x]=2 if (ML[y,x]<78 and p in (3,4,5)) else 1
# losse detailpixels (geen lijn van >=2) vervallen
lab,k=nd.label(detail>0,structure=np.ones((3,3)))
for i in range(1,k+1):
    c=lab==i; ys,xs=np.where(c)
    lang=max(ys.max()-ys.min(),xs.max()-xs.min())+1
    if c.sum()<2 or (np.isin(d[c],[3,4,5]).any() and lang<3): detail[c]=0   # hout: alleen nerf als streep van >= 3 px
for p in RAMP:
    m=(d==p)&(niveau>=0)
    for lv,k in enumerate(RAMP[p]): n[m&(niveau==lv)]=k
    r=RAMP[p]
    for y,x in zip(*np.where(m&(detail>0))):
        lv=niveau[y,x]
        if detail[y,x]==2: n[y,x]=B0
        elif p in (1,2) and lv==0: pass          # vacht: nerf niet onder de schaduwtint
        else: n[y,x]=r[lv-1] if lv>0 else (B1 if r[0]==B2 else B0)
# ---------- stap 3: blokken en dak (vlakken uit het model / r17, drie tinten per kubus) ----------
for y in range(64):
    for x in range(64):
        k=o[y,x]; p=d[y,x]
        if p==13: n[y,x]=GL if k==13 else GD
        elif p==10:
            if k==8: n[y,x]=GE
            elif k in (4,5,3): n[y,x]=B3
            else: n[y,x]=B2
        elif p==11:
            n[y,x]=RO if k==9 else B1
        elif p==12:
            n[y,x]=BL if k==11 else BD
        elif p==14:
            n[y,x]={1:K,2:B0,6:HL,7:HD,15:CR}[k]
n[zwart]=K
# toren: slagschaduw en bovenvlakken (vlakken die het model toont)
n[11,45:51]=B4                      # slagschaduw onder het dak op de gele voorkant
n[11,51:55]=B2                      # idem op de zijkant
n[18,48:55]=B1                      # bovenkant rood in de schaduw van het gele blok
n[26,46:54]=B0                      # onderrand rood blok
n[26,44:46]=HL                      # bovenkant blauw blok (model: lichtblauwe strook)
# ---------- stap 4: belijning ----------
L2=np.array([-.66,-.75])
def deel_van(y,x):
    if d[y,x]>0: return d[y,x]
    c=[d[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if 0<=yy<64 and 0<=xx<64 and d[yy,xx]>0]
    return max(set(c),key=c.count) if c else 1
cy_deel={p:np.where(d==p)[0].mean() for p in range(1,15) if (d==p).any()}
lijnlog=[]
for y,x in zip(*np.where(ring)):
    if (x,y) in BESCHERMD: continue
    v=np.zeros(2)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            yy,xx=y+dy,x+dx
            if (dy or dx) and (not(0<=yy<64 and 0<=xx<64) or not fig[yy,xx]): v+=(dx,dy)
    if not v.any(): continue
    v/=np.linalg.norm(v); p=deel_van(y,x)
    licht=v@L2>0.3
    if licht and abs(v[0])>abs(v[1])*1.5 and y>cy_deel.get(p,0): licht=False   # links: alleen bovenhelft
    n[y,x]=SEL[p] if licht else K
# binnenlijnen: zwart, behalve waar de lijn tussen lichte vlakken ligt -> eigen donkerste tint
LICHTE={B3,B4,GE,RO,BL,GL,CR,HL}
for y,x in zip(*np.where(zwart&~ring)):
    if (x,y) in BESCHERMD: continue
    nb=[(n[yy,xx],d[yy,xx]) for yy in range(y-1,y+2) for xx in range(x-1,x+2) if (yy,xx)!=(y,x) and n[yy,xx] not in (0,K)]
    if len(nb)>=4 and sum(1 for k,_ in nb if k in LICHTE)>=0.7*len(nb):
        ps=[q for _,q in nb]; q=max(set(ps),key=ps.count)
        if q in (1,2,3,4,5,6,7,8): n[y,x]=SEL[q]        # alleen hout/vacht; toren en hoepel houden zwart
# ---------- stap 5: laatste vlekjesronde (hout/vacht, binnen de lijn): tintvlek < 3 px -> meest voorkomende buurtint van hetzelfde onderdeel ----------
BR=(B0,B1,B2,B3,B4)
vlek_log=[]
for _ in range(4):
    gedaan=0
    for k in BR:
        lab,c=nd.label(n==k,structure=np.ones((3,3)))
        for i in range(1,c+1):
            m=lab==i
            if m.sum()>=3: continue
            pts=[(y,x) for y,x in zip(*np.where(m))]
            if any(ring[y,x] or (x,y) in BESCHERMD or d[y,x] not in (1,2,3,4,5,6,7,8) for y,x in pts): continue
            buur=[n[yy,xx] for y,x in pts for yy in range(y-1,y+2) for xx in range(x-1,x+2)
                  if 0<=yy<64 and 0<=xx<64 and not m[yy,xx] and n[yy,xx] in BR and d[yy,xx]==d[y,x] and not ring[yy,xx]]
            if not buur: continue
            t=max(set(buur),key=buur.count)
            for y,x in pts: vlek_log.append((x,y,k,t)); n[y,x]=t
            gedaan+=1
    if not gedaan: break
def toon(a,y0=0,y1=64):
    CH='.K0123456hHcYrbBgG'
    CH='.KabcdeLDcYrPQgG'
    print('   '+''.join(str(x%10) for x in range(64)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in a[y]))
if __name__=='__main__':
    tmp=n.copy(); tmp[zwart]=1; toon(tmp)
def rgb(a,bg=None):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg if bg else PAL[0]
    for k in range(1,16): img[a==k]=PAL[k]
    return Image.fromarray(img)
if __name__=='__main__' and len(sys.argv)>1:
    rgb(n).resize((512,512),Image.NEAREST).save(sys.argv[1])
def opslaan(a,path):
    p=Image.fromarray(a.astype('uint8'),'P'); fl=[v for c in PAL for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save(path,transparency=0)
if __name__=='__main__' and len(sys.argv)==1:
    assert ((n==0)==(o==0)).all(), 'silhouet gewijzigd'
    opslaan(n,'eindkeuring_dc/capykart.png'); np.save('eindkeuring_dc/_n.npy',n)
    rgb(n,(255,255,255)).resize((512,512),Image.NEAREST).save('eindkeuring_dc/capykart_8x.png')
    print('silhouet-diff', int(((n==0)!=(o==0)).sum()), 'kleuren', len(set(n.ravel())))
