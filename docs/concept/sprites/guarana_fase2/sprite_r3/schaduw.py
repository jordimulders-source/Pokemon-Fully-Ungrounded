# Guarana fase 2, r3: volume/schaduw (Jordi r2: "volledig 2d", "niet goed ingekleurd, geen enkele schaduw").
# Werkt op de r2-opbouw (silhouet, lijnen, vruchtgrenzen, ogen) en kleurt alleen de VULPIXELS opnieuw in:
#  - objecten uit het natieve model: elke vrucht (vrucht-id, kaal.py) en elk groen deel (groene cellen L>=85, gescheiden door de donkere
#    modellijnen/nerven: lussen, bladclusters, getwijnde strengen, grijpranken) = OBJ per spritepixel (meeste dekking).
#  - per object een toonwaarde t = A*licht (vorm: normaal uit het vervaagde objectmasker, licht linksboven) + B*model (modelhelderheid
#    per spritepixel, gestandaardiseerd binnen het object) -> per object gekwantiseerd op een tintramp (hooglicht linksboven,
#    schaduwsikkel rechtsonder). Geen tinten getekend: de grenzen volgen de vorm (gebogen) en de modelhelderheid.
#  - diepte: de achter geplakte trossen (verdubbeling, BRON uit natief_model vs natief_r10) en donkere objecten (gemiddelde
#    modelhelderheid laag) krijgen een ramp die een stap donkerder begint.
import numpy as np
from gemeen2 import *
from klassen2 import klassen
from PIL import Image
a,c,L=klassen(NATIEF)
H,W=c.shape
r10=np.asarray(Image.open('sprite_r1/natief_r10.png').convert('RGB')).astype(int)
BACK=np.abs(a-r10).sum(2)>30
def label(m):
    lab=np.zeros(m.shape,int);k=0
    for y,x in zip(*np.where(m)):
        if lab[y,x]: continue
        k+=1; st=[(y,x)]; lab[y,x]=k
        while st:
            cy,cx=st.pop()
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=cy+dy,cx+dx
                if 0<=yy<H and 0<=xx<W and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=k; st.append((yy,xx))
    return lab,k
GLAB,_=label((c==3)&(L>=85)); gsz=np.bincount(GLAB.ravel())
def gauss(m,s):
    r=int(np.ceil(3*s)); k=np.exp(-np.arange(-r,r+1)**2/(2*s*s)); k/=k.sum()
    p=np.pad(m.astype(float),r,mode='constant')
    p=np.apply_along_axis(lambda v:np.convolve(v,k,'same'),0,p)
    p=np.apply_along_axis(lambda v:np.convolve(v,k,'same'),1,p)
    return p[r:-r,r:-r]
def info(VL,GROOT):
    OBJ={}; LUM=np.full((64,64),np.nan); BK=np.zeros((64,64))
    for Y in range(64):
        for X in range(64):
            w={}; ls=0; lw=0; bk=0
            for u,v,ww in overlap(X,Y):
                if c[v,u] in (2,3):
                    ls+=ww*L[v,u]; lw+=ww; bk+=ww*BACK[v,u]
                if c[v,u]==2 and VL[v,u] in GROOT: k=('F',VL[v,u])
                elif c[v,u]==3 and GLAB[v,u] and gsz[GLAB[v,u]]>=20: k=('G',GLAB[v,u])
                else: continue
                w[k]=w.get(k,0)+ww
            if w: OBJ[(Y,X)]=max(w,key=w.get)
            if lw: LUM[Y,X]=ls/lw; BK[Y,X]=bk/lw
    return OBJ,LUM,BK
# tintrampen (donker -> licht) en aandelen
RAMP={'F':([3,4,12,5],[.30,.32,.24,.14]), 'Fb':([14,3,4],[.40,.40,.20]),
      'G':([7,13,8,9],[.26,.30,.30,.14]), 'Gb':([15,7,13,8],[.30,.30,.28,.12])}
VULR={3,4,12,5,14}; VULG={7,13,8,9,15}
LICHT=np.array([-1.0,-1.25,1.1]); LICHT/=np.linalg.norm(LICHT)
SM=0.9
NERF_BUREN=int(__import__('os').environ.get('NERF_BUREN','3'))
GROEN_NERF=__import__('os').environ.get('NERF','0')=='1'
DREMPEL=[0.30,0.70,0.90]
BW={'F':0.10,'G':float(__import__('os').environ.get('BWG','0.35'))}
RAMP4={'F':[3,4,5,12],'Fb':[14,3,4,4],'G':[7,13,8,9],'Gb':[15,7,13,8]}
def kleur(o,OOG,VL,GROOT,LD,A=0.75,B=0.25,log=None):
    OBJ,LUM,BK=info(VL,GROOT)
    fg=o>0
    def rand(Y,X): return any(not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
    # vulpixels (de pixels die opnieuw ingekleurd worden): vultinten + groene 'lijn' midden in een object zonder modellijn (nerven, donker groen)
    VUL=np.zeros((64,64),bool)
    for Y,X in zip(*np.where(fg)):
        if OOG[Y,X] or rand(Y,X): continue
        k=o[Y,X]
        if k in VULR|VULG: VUL[Y,X]=True
        elif GROEN_NERF and k==6 and LD[Y,X]<0.30 and (Y,X) in OBJ and OBJ[(Y,X)][0]=='G':
            same=sum(OBJ.get((Y+dy,X+dx))==OBJ[(Y,X)] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
            if same>=NERF_BUREN: VUL[Y,X]=True
    # lijnrood binnen een vrucht (geen grens met een andere vrucht of met groen, alleen dezelfde vrucht eromheen) -> vul (wordt bol ingekleurd)
    LOS=0
    for Y,X in zip(*np.where(o==2)):
        if OOG[Y,X] or rand(Y,X) or (Y,X) not in OBJ or OBJ[(Y,X)][0]!='F': continue
        nb=set()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(Y+dy,X+dx)
            if o[q]==2 and not OOG[q]: continue
            nb.add(OBJ.get(q,('?',0)))
        if nb=={OBJ[(Y,X)]}: VUL[Y,X]=True; LOS+=1
    # vruchtgrenzen: twee aangrenzende vulpixels van verschillende vruchten -> de pixel van de achterste vrucht wordt lijnrood (1 px),
    # achter = geplakte achtertros (BK) of anders de pixel met de meeste modellijn (LD), zoals r2 stap 1b
    nieuw0=o.copy(); GRENS=0
    for Y in range(64):
        for X in range(64):
            for dy,dx in ((0,1),(1,0)):
                Y2,X2=Y+dy,X+dx
                if Y2>63 or X2>63: continue
                a1,a2=OBJ.get((Y,X)),OBJ.get((Y2,X2))
                if not(a1 and a2 and a1[0]==a2[0] and a1!=a2): continue
                if not(VUL[Y,X] and VUL[Y2,X2]): continue
                if nieuw0[Y,X] in (2,6) or nieuw0[Y2,X2] in (2,6): continue
                s1=BK[Y,X]*2+LD[Y,X]; s2=BK[Y2,X2]*2+LD[Y2,X2]
                q=(Y,X) if s1>=s2 else (Y2,X2)
                nieuw0[q]=2 if a1[0]=='F' else 6; VUL[q]=False; GRENS+=1
    o=nieuw0
    ids={}
    for (Y,X),k in OBJ.items():
        if fg[Y,X]: ids.setdefault(k,[]).append((Y,X))
    nieuw=o.copy(); stat=[]
    for k,pts in ids.items():
        M=np.zeros((64,64),bool)
        for p in pts: M[p]=True
        if k[0]=='F': M|=False
        vp=[p for p in pts if VUL[p]]
        if not vp: continue
        n=M.sum()
        if k[0]=='F':
            # vrucht = glanzende bol: normaal uit een ellips om de hele vrucht (incl. oog en eigen lijn), licht linksboven
            ys,xs=np.where(M); cy,cx=ys.mean(),xs.mean(); ry=max(1.6,2.0*ys.std()+0.6); rx=max(1.6,2.0*xs.std()+0.6)
            lam=[]
            for p in vp:
                ex,ey=(p[1]-cx)/rx,(p[0]-cy)/ry; r2=ex*ex+ey*ey
                nv=np.array([ex,ey,np.sqrt(max(0.08,1-r2))]); nv/=np.linalg.norm(nv); lam.append(nv@LICHT)
        else:
            s=float(np.clip(np.sqrt(n)/3.2,1.0,2.6)); Bm=gauss(M,s); gy,gx=np.gradient(Bm); nz=0.35/s; lam=[]
            for p in vp:
                nv=np.array([-gx[p],-gy[p],nz]); nv/=np.linalg.norm(nv); lam.append(nv@LICHT)
        lam=np.array(lam)
        Lm=np.where(M&~np.isnan(LUM),np.nan_to_num(LUM),0.); Wm=(M&~np.isnan(LUM)).astype(float)
        Ls=gauss(Lm,SM)/np.maximum(gauss(Wm,SM),1e-6)
        lum=np.array([Ls[p] for p in vp]); lz=(lum-lum.mean())/(lum.std()+1e-6) if len(vp)>1 else lum*0
        bk=np.mean([BK[p] for p in vp]); ml=np.nanmean(LUM[M])
        if k[0]=='F': soort='Fb' if bk>0.5 else 'F'
        else: soort='Gb' if ml<108 else 'G'
        tints=RAMP4[soort]
        t=lam+BW[k[0]]*lz
        band=np.searchsorted(DREMPEL,t)
        # minstens 3 tinten per object met >= 6 vulpixels: anders op rang verdelen (zelfde volgorde als t)
        if len(vp)>=6 and len(set(band))<3:
            q=(np.argsort(np.argsort(t))+0.5)/len(vp); band=np.searchsorted([.33,.7,.9],q)
        for p,b in zip(vp,band): nieuw[p]=tints[b]
        # losse tintpixels (geen 4-buur met dezelfde tint binnen het object) -> meest voorkomende tint van de objectburen (hooglicht mag 1-2 px)
        for _ in range(2):
            for p in vp:
                Y,X=p; nb=[nieuw[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=Y+dy<64 and 0<=X+dx<64 and VUL[Y+dy,X+dx] and OBJ.get((Y+dy,X+dx))==k]
                if nb and nieuw[p] not in nb and nieuw[p] not in (5,9):
                    nieuw[p]=max(set(nb),key=nb.count)
        stat.append((k,soort,len(vp),round(bk,2),round(ml,1)))
    if log is not None: log.extend(stat); log.append(('vruchtgrens_px',GRENS)); log.append(('lijn_naar_vul',LOS))
    return nieuw,VUL,OBJ
