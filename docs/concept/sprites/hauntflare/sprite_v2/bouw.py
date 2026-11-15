# Hauntflare sprite v2 (maker, 15 nov). Basis = ../basis/basis_64.png (bevroren vorm, oppervlak-middeling van
# ../model/model_claude_natief.png). Niets getekend: elke pixel krijgt een paletkleur op zijn plek, gekozen uit de
# modelpixels die in die basispixel vallen. Uitzonderingen (opdracht): Haunters ogen 1-op-1 (Gen 3, frame 1) en de mond
# naar Haunters mond. Gebruik (vanuit de repo-root): python3 docs/concept/sprites/hauntflare/sprite_v2/bouw.py
import json
from PIL import Image; import numpy as np
from scipy import ndimage as nd
D='docs/concept/sprites/hauntflare/'; S=D+'sprite_v2/'
K4=[[0,1,0],[1,1,1],[0,1,0]]; K8=np.ones((3,3))
LOG={}
# ---------------- palet (zelfde als r1) ----------------
PAL=[(0x98,0xd0,0xa0),   # 0 transparant
 (0x24,0x16,0x1a),       # 1 omlijning (modelkleur)
 (0x5a,0x2a,0x33),       # 2 ring donker / Haunters donkere ooglijn
 (0x8a,0x4e,0x55),       # 3 ring midden (modelkleur)
 (0xb0,0x74,0x7a),       # 4 ring licht
 (0xc8,0x43,0x5b),       # 5 bol selout (modelkleur)
 (0xf0,0x44,0x82),       # 6 bol schaduw
 (0xfa,0x76,0xa2),       # 7 bol midden
 (0xf8,0xae,0xc2),       # 8 bol licht
 (0xf9,0xcc,0xd8),       # 9 bol glans
 (0x9a,0x2a,0x22),       # 10 donkerrood: vlam-/handselout, mond
 (0xd8,0x40,0x30),       # 11 vlam rood (kern), hand rood
 (0xf4,0x86,0x59),       # 12 vlam oranje (r4_a-rand)
 (0xf8,0xb8,0x50),       # 13 vlam geel-oranje
 (0xff,0xff,0xff),       # 14 oogwit
 (0xee,0x74,0x7c)]       # 15 hand licht (knokkels), mond licht
P=np.array(PAL)
def near(c,idx):
    idx=list(idx); return idx[int(((P[idx]-np.asarray(c))**2).sum(1).argmin())]
lum=lambda a:(a[...,:3]*[.299,.587,.114]).sum(-1)
# ---------------- model en de afbeelding model -> basis (zelfde als basis.py) ----------------
M=np.asarray(Image.open(D+'model/model_claude_natief.png').convert('RGB')).astype(float)
MW=M.min(2)>=0xe0
ys,xs=np.where(~MW); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
cw,ch=x1-x0,y1-y0; s=62/max(cw,ch); W,H=round(cw*s),round(ch*s); ox=(64-W)//2; oy=64-H-1
myy,mxx=np.mgrid[:M.shape[0],:M.shape[1]]
BX=ox+np.floor((mxx-x0+0.5)*W/cw).astype(int); BY=oy+np.floor((myy-y0+0.5)*H/ch).astype(int)
B=np.asarray(Image.open(D+'basis/basis_64.png')).astype(int)
OP=B[...,3]>0; BC=B[...,:3].copy()
yy,xx=np.mgrid[:64,:64]
# gat in de bol: de witte glans van het model viel bij basis.py als achtergrond weg (wit >= e0). Binnengaten in de
# bolellips worden weer bol (glans); de ringgaten blijven open. Buitensilhouet verandert niet.
GAT=nd.binary_fill_holes(OP)&~OP
GAT&=(((xx-29)/18)**2+((yy-32)/16.8)**2<=1)
lg,ng=nd.label(GAT); GAT=np.isin(lg,[i for i in range(1,ng+1) if (((xx[lg==i]-29)/18)**2+((yy[lg==i]-32)/16.8)**2).max()<0.8])
OP=OP|GAT; BC[GAT]=(0xf9,0xcc,0xd8)
# ---------------- stap 0: oud modelgezicht weg in het model (bolroze uit de buren, tintverloop) ----------------
ML=lum(M)
FBOX=(mxx>=25)&(mxx<=46)&(myy>=35)&(myy<=53)
mell=((mxx-38)/27.5)**2+((myy-41)/26)**2<=1          # binnenkant bol in modelcoordinaten (rand blijft)
donker=(ML<150)|((M[...,1]<0x58)&(M[...,2]<0x70))     # lijnen, mondrood
fz=FBOX&mell&donker&~MW
licht=FBOX&(M.min(2)>=0xd8)                           # oogwitten: licht en omsloten door de oude ooglijnen
oog=licht&nd.binary_fill_holes(nd.binary_dilation(fz,K8))&nd.binary_dilation(fz,K8,iterations=3)
FACE=(fz|oog)&mell
LOG['model_gezicht_px']=int(FACE.sum())
LOG['bolgat_gevuld']=[]
Mc=M.copy(); todo=FACE.copy(); Mc[todo]=np.nan
while todo.any():
    known=~np.isnan(Mc[...,0])
    acc=np.zeros_like(Mc); cnt=np.zeros(M.shape[:2])
    for dy in(-1,0,1):
        for dx in(-1,0,1):
            if not(dy or dx): continue
            sh=np.roll(np.roll(Mc,dy,0),dx,1); k=np.roll(np.roll(known,dy,0),dx,1)&np.roll(np.roll(~MW,dy,0),dx,1)
            acc+=np.where(k[...,None],np.nan_to_num(sh),0); cnt+=k
    fill=todo&(cnt>=3)
    if not fill.any(): fill=todo&(cnt>=1)
    Mc[fill]=acc[fill]/cnt[fill][:,None]; todo&=~fill
M=Mc; ML=lum(M)
Image.fromarray(np.where(MW[...,None],255,M).astype('uint8')).save(S+'model_zonder_gezicht.png')
# ---------------- modelklassen ----------------
MBORDER=(~MW)&nd.binary_dilation(MW,K4)
ZW=(~MW)&(ML<60)                                        # zwarte lijn
DR=(~MW)&~ZW&(M[...,0]<0xc4)&(M[...,0]>1.9*M[...,1])&(M[...,2]<0x40)&(ML<110)   # donkerrode lijn (ba3c26, 93241d, 6a2622 ...)
PR=(~MW)&~ZW&~DR&(np.abs(M[...,0]-0x55)<14)&(np.abs(M[...,1]-0x26)<12)&(np.abs(M[...,2]-0x30)<12)  # ring donker 552630
def fwd(mask):
    o=np.zeros((64,64),bool); o[BY[mask],BX[mask]]=True; return o&OP
# ---------------- groepen in de basis ----------------
lab,n=nd.label(OP)
sizes=[(lab==i).sum() for i in range(1,n+1)]; main=lab==1+int(np.argmax(sizes))
comps=[i for i in range(1,n+1) if not (lab==i).sum()==max(sizes)]
lhand=np.zeros((64,64),bool); rhand=np.zeros((64,64),bool)
for i in comps:
    cx=xx[lab==i].mean(); (lhand if cx<32 else rhand)[...]|=lab==i
r_,g_,b_=BC[...,0],BC[...,1],BC[...,2]
ringc=OP&(np.abs(r_-0x8a)<12)&(np.abs(g_-0x4e)<10)&(np.abs(b_-0x54)<10)
ell=((xx-29)/18)**2+((yy-32)/16.8)**2<=1
pinkc=OP&(r_>0xe8)&(b_>0x70)
# ring = ringbruin + donkerbruin dat eraan grenst (552630 / bijna zwart in de ringstrook)
dk=OP&(lum(BC)<80)
ring=ringc|(dk&nd.binary_dilation(ringc,K8)&~((ell|pinkc)&~nd.binary_dilation(ringc,K4)))
ring&=main
lr,nr=nd.label(ring,K8); rs=[(lr==i).sum() for i in range(1,nr+1)]
ring=np.isin(lr,[i+1 for i,v in enumerate(rs) if v>=20])      # losse ringbruine plekjes (oude gezichtslijnen) horen bij de bol
bol=main&~ring&(ell|pinkc)
rest=main&~ring&~bol
kuif=rest&(yy<30); staart=rest&(yy>=30)
# vlamkleuren binnen de ellips horen bij de kuif (kuifvoet bovenrechts)
vlamc=OP&~pinkc&(((r_>0xf0)&(g_>0x78)&(b_<0x78))|((r_<0xc0)&(r_>0xa0)&(g_<0x45)))
mv=bol&vlamc&(yy<24)&(xx>32); kuif|=mv; bol&=~mv
LOG['bolgat_gevuld']=[(int(x),int(y)) for y,x in zip(*np.where(GAT))]
GROEP=np.zeros((64,64),int); GROEP[bol]=1; GROEP[ring]=2; GROEP[kuif]=3; GROEP[staart]=4; GROEP[lhand|rhand]=5
LOG['groepen_px']={k:int((GROEP==v).sum()) for k,v in [('bol',1),('ring',2),('kuif',3),('staart',4),('hand',5)]}
LOG['niet_ingedeeld']=int((OP&(GROEP==0)).sum())
# ---------------- basisrand en lijnen ----------------
RAND=OP&nd.binary_dilation(~OP,K4)
out=np.zeros((64,64),int)
# 1) buitenlijn: kleur = de randkleur die het model hier heeft (modelrandpixels in en rond de voetafdruk)
def randklasse(bx,by,g):
    for rad in (0,1,2,3):
        sel=MBORDER&(np.abs(BX-bx)<=rad)&(np.abs(BY-by)<=rad)
        if sel.any(): break
    c=M[sel]; lc=lum(c)
    zw=(lc<60).sum(); dr=(DR[sel]).sum(); ov=len(c)-zw-dr
    if g==2: return 1 if zw>=dr+ov*0.5 or True else 1     # ring: model heeft overal zwart
    if g==1:
        return 1 if zw>max(dr,ov) else 5                   # bol: zwart of roze selout (cb435a)
    return 1 if zw>max(dr,ov) else 10                       # vlam/hand: zwart of donkerrood
for y,x in zip(*np.where(RAND)):
    out[y,x]=randklasse(x,y,GROEP[y,x])
# 2) binnenlijnen: modellijnpixels (niet op de modelrand) op hun plek doorgezet
LZ=fwd(ZW&~MBORDER)&~RAND; LD=fwd(DR&~MBORDER)&~RAND; LP=fwd(PR&~MBORDER)&~RAND
out[LP&(out==0)]=2; out[LD&(out==0)]=10; out[LZ]=1
# ---------------- vullingen: per basispixel uit de niet-lijn-modelpixels in de voetafdruk ----------------
VUL=(~MW)&~ZW&~DR&~PR
def voet(x,y,mask=VUL,rad=0):
    for r_ in range(rad,4):
        sel=mask&(np.abs(BX-x)<=r_)&(np.abs(BY-y)<=r_) if r_ else mask&(BX==x)&(BY==y)
        if sel.any(): return M[sel]
    return None
# vlammen: modelklassen -> warmer (zelfde verdeling als r1)
VL={(0xcb,0x43,0x5a):11,(0xe8,0x5f,0x80):12,(0xf8,0x85,0x6c):13}
HK={(0xe4,0x4c,0x56):11,(0xc9,0x40,0x51):5,(0xea,0x60,0x6c):15}
def mode_map(c,tab):
    k=np.array(list(tab.keys())); v=list(tab.values())
    cls=[v[int(((k-ci)**2).sum(1).argmin())] for ci in c]
    return max(set(cls),key=cls.count)
# ring: toonverdeling van de r4_c-ring (zelfde raster), helderheid per voetafdruk, 3x3 binnen de ring
RC=np.asarray(Image.open(D+'model/nat_r4_c.png').convert('RGB')).astype(float)
RCL=lum(RC); RCRING=(~(RC.min(2)>=0xe0))&(RCL>60)
rl=np.full((64,64),np.nan)
for y,x in zip(*np.where(ring)):
    sel=RCRING&(np.abs(BX-x)<=0)&(np.abs(BY-y)<=0)
    if not sel.any(): sel=RCRING&(np.abs(BX-x)<=1)&(np.abs(BY-y)<=1)
    if sel.any(): rl[y,x]=RCL[sel].mean()
w=(~np.isnan(rl)).astype(float); k3=np.ones((3,3))
rls=nd.convolve(np.nan_to_num(rl),k3,mode='constant')/np.maximum(nd.convolve(w,k3,mode='constant'),1)
vals=rls[ring&(w>0)]; t1,t2=np.percentile(vals,[15,80]); LOG['ring_drempels_r4c']=[float(t1),float(t2)]
for y,x in zip(*np.where(OP&(out==0))):
    g=GROEP[y,x]
    if g==2:
        v=rls[y,x]; out[y,x]=2 if v<t1 else (3 if v<t2 else 4); continue
    c=voet(x,y)
    if c is None: c=BC[y,x][None].astype(float)
    if g==1:
        out[y,x]=near(c.mean(0),[5,6,7,8,9])
    elif g in (3,4):
        out[y,x]=mode_map(c,VL)
    elif g==5:
        out[y,x]=mode_map(c,HK)
# ---------------- handen: kleurgebruik r4_a (oranje binnenrand van de bogen en onderranden), regel uit r1 ----------------
HANDORANJE=[]
for hm in (lhand,rhand):
    gat=np.zeros((64,64),bool)
    for y,x in zip(*np.where(out==0)):
        if 2<=y<62 and 2<=x<62 and hm[max(0,y-3):y,x].any() and hm[y,max(0,x-4):x].any() and hm[y,x+1:x+5].any():
            gat[y,x]=True
    lijn=nd.binary_dilation(gat,K4)&np.isin(out,[1,10])
    rim=nd.binary_dilation(lijn,K4)&hm&np.isin(out,[5,11,15])&~RAND
    for y,x in zip(*np.where(rim)): out[y,x]=12; HANDORANJE.append((int(x),int(y)))
    for y,x in zip(*np.where(hm&np.isin(out,[5,11,15])&~RAND)):
        if out[y+1,x] in (1,10): out[y,x]=12; HANDORANJE.append((int(x),int(y)))
LOG['hand_oranje']=HANDORANJE
np.save(S+'stap1_kleur.npy',out); np.save(S+'groep.npy',GROEP)
json.dump(LOG,open(S+'bouw_log.json','w'),indent=0)
print(json.dumps({k:v for k,v in LOG.items() if k!='hand_oranje'}),'hand-oranje',len(HANDORANJE))
# ================= stap 2: gezicht. Haunter Gen 3, frame 1, schaal 1,0 =================
HG=np.array(Image.open('graphics/pokemon/haunter/anim_front.png'))[:64].astype(int)
HX0,HX1,HY0,HY1=13,33,28,45            # Haunter-blok (ogen + mond), inclusief
GZ={}                                   # (x,y) Haunter -> paletindex
UIT={(15,38),(33,37)}                   # Haunters wang-/kaakomtrek (hoofdrand), geen oog- of mondlijn
import os
MOND9=int(os.environ.get('MOND9','10'))
KLEUR={0xf:14,0xe:1,0xd:2,0x5:2,0xa:10,0x9:MOND9}
for y in range(HY0,HY1+1):
    for x in range(HX0,HX1+1):
        v=HG[y,x]
        if (x,y) in UIT: continue
        if x<=14 and y>=38: continue                     # Haunters linkerhand steekt hier het blok in
        if y==45 and x not in (27,28): continue          # rij 45: alleen de mondlijn onder de mond (x27-28)
        if v in KLEUR: GZ[(x,y)]=KLEUR[v]
        # Haunters donkere huid (4) die als lijn tegen het smalle oogwit ligt -> donkere boltint
        elif v==4 and x<=17 and any(HG[y+dy,x+dx]==0xf for dy,dx in((0,1),(0,-1),(1,0),(-1,0))): GZ[(x,y)]=5
LOG['haunter_gezicht_px']=len(GZ)
# plaats: alle gezichtspixels op het binnenste van de bol (niet op een lijn/rand, >=1 px van ring en rand),
# >=2 px bolroze links van het linker oog; zo dicht mogelijk bij het oude modelgezicht
BOLIN=(GROEP==1)&~nd.binary_dilation((GROEP!=1)|RAND,K8)
fy,fx=np.where(fwd(FACE)); mcx,mcy=fx.mean(),fy.mean()
hx=np.array([k[0] for k in GZ]); hy=np.array([k[1] for k in GZ])
oogL=[(x,y) for (x,y),v in GZ.items() if x<=17]
kand=[]
for dy in range(-30,20):
    for dx in range(-20,30):
        px,py=hx+dx,hy+dy
        if px.min()<0 or py.min()<0 or px.max()>63 or py.max()>63: continue
        if not BOLIN[py,px].all(): continue
        ok=all((GROEP[y+dy,x+dx-1]==1 and GROEP[y+dy,x+dx-2]==1 and not RAND[y+dy,x+dx-2] and (x-1,y) not in GZ and (x-2,y) not in GZ) or (x-1,y) in GZ for x,y in oogL)
        if not ok: continue
        kand.append((float(np.hypot(px.mean()-mcx,py.mean()-mcy)),dx,dy))
kand.sort(); LOG['gezicht_kandidaten']=kand[:8]
GDX,GDY=kand[0][1],kand[0][2]; LOG['gezicht_offset']=[GDX,GDY]
LOG['modelgezicht_midden']=[float(mcx),float(mcy)]
GEZICHT=np.zeros((64,64),bool)
for (x,y),v in GZ.items():
    out[y+GDY,x+GDX]=v; GEZICHT[y+GDY,x+GDX]=True
np.save(S+'stap2_gezicht.npy',out)
print('gezicht offset',GDX,GDY,'kandidaten',kand[:5])
# ================= stap 3: opruimen (regels, geen handwerk) =================
VULT={1:[5,6,7,8,9,14],2:[2,3,4],3:[10,11,12,13],4:[10,11,12,13],5:[5,10,11,12,15]}
LIJN={1,2,10,5}
# 3a) losse tintvlakjes < 3 px (4-verbonden, binnen de groep, niet op de rand, niet in het gezicht) -> meest
#     voorkomende buurtint van dezelfde groep. Lijnpixels doen niet mee (die volgen het model).
INLIJN=np.zeros((64,64),bool)
INLIJN[LZ|LD|LP]=True
OPG=[]
for _ in range(8):
    n_=0
    for g,tones in VULT.items():
        gm=(GROEP==g)&~RAND&~GEZICHT&~INLIJN
        for t in tones:
            l,k=nd.label(gm&(out==t),K8)
            for i in range(1,k+1):
                cl=l==i
                if cl.sum()>=3 or (g==1 and t==14): continue
                nb=[]
                for y,x in zip(*np.where(cl)):
                    for ey,ex in((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                        v=out[y+ey,x+ex]
                        if v in tones and v!=t and gm[y+ey,x+ex]: nb.append(v)
                if nb:
                    nv=max(set(nb),key=nb.count); 
                    for y,x in zip(*np.where(cl)): OPG.append((int(x),int(y),int(t),int(nv)))
                    out[cl]=nv; n_+=int(cl.sum())
    if not n_: break
LOG['tintvlakjes_herkleurd']=OPG
# 3b) dubbele buitenlijn: een binnenlijnpixel die 4-buur is van een randlijn en verder alleen vulling raakt
#     (geen andere binnenlijn) is een verdikking van de buitenlijn -> vulling van de buren.
DUB=[]
for _ in range(2):
    for y,x in zip(*np.where(INLIJN&~RAND&~GEZICHT&np.isin(out,list(LIJN)))):
        n4=[(y+ey,x+ex) for ey,ex in((1,0),(-1,0),(0,1),(0,-1))]
        if not any(RAND[p] for p in n4): continue
        n8=[(y+ey,x+ex) for ey in(-1,0,1) for ex in(-1,0,1) if ey or ex]
        if any(INLIJN[p] and not RAND[p] and out[p] in LIJN for p in n8): continue
        f=[out[p] for p in n8 if out[p] in VULT.get(GROEP[y,x],[]) and out[p] not in LIJN]
        if f:
            nv=max(set(f),key=f.count); DUB.append((int(x),int(y),int(out[y,x]),int(nv))); out[y,x]=nv; INLIJN[y,x]=False
LOG['dubbele_lijn_weg']=DUB
# 3c) buitenrand: nooit zwart en donker om-en-om. Een losse randpixel waarvan beide randburen de andere lijnkleur
#     hebben, neemt die kleur over.
OMENOM=[]
for _ in range(3):
    for y,x in zip(*np.where(RAND&~GEZICHT)):
        v=out[y,x]
        nb=[out[y+ey,x+ex] for ey in(-1,0,1) for ex in(-1,0,1) if (ey or ex) and 0<=y+ey<64 and 0<=x+ex<64 and RAND[y+ey,x+ex]]
        if not nb or v in nb: continue
        nv=max(set(nb),key=nb.count); OMENOM.append((int(x),int(y),int(v),int(nv))); out[y,x]=nv
LOG['rand_om_en_om']=OMENOM
print('tintvlakjes',len(OPG),'dubbel',len(DUB),'om-en-om',len(OMENOM))
np.save(S+'stap3.npy',out); np.save(S+'gezicht_masker.npy',GEZICHT)
json.dump(LOG,open(S+'bouw_log.json','w'),indent=0)
# ================= opslaan =================
pim=Image.fromarray(out.astype('uint8'),'P')
pim.putpalette([c for p in PAL for c in p]+[0]*(768-3*len(PAL)))
pim.save(S+'hauntflare_v2.png',transparency=0)
rgb=P[out].astype('uint8'); rgb[out==0]=255
Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(S+'hauntflare_v2_8x.png')
