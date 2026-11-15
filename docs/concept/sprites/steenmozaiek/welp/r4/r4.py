# Ronde 4: alleen rug (punt eruit, één boog) + belijning/schaduw/kleurgebruik zoals Krassault. Patronen niet herontworpen.
# Basis: ../r3/welp_r3_A_oog1.npy (Jordi: heup A, oog 1 px links). Silhouet bevroren behalve de rug (bewaak.py).
import numpy as np, math, json
a=np.load('welp_r3_A_oog1.npy'); r3=a.copy(); H,Wd=a.shape
_,K,d,S,M,L,P,Q,R,g_,W,C,T,G=range(14)
BR={S,M,L}; LIJN={K,d}
log={}
# ---------- 1. rug: één doorlopende boog nek -> heup (horizontale runs 2,2 dan 1-1-..., verticale runs 2,3,3)
EDGE={12:25,13:27,14:29,15:30,16:31,17:32,18:33,19:34,20:35,21:36,22:37,23:38,24:39,25:40,26:41,27:41,
      28:42,29:42,30:42,31:43,32:43,33:43}
for y,e in EDGE.items():
    xs=np.where(a[y,:44]>0)[0]; old=xs.max()+1
    fillc=M
    for x in range(min(old,e)-1,max(old,e)+1):
        if x>=e: a[y,x]=0
        elif a[y,x] in (0,K) and x<e-1: a[y,x]=fillc
    a[y,e-1]=K
rug_px=int(((a>0)!=(r3>0)).sum()); log['rug_silhouet_px']=rug_px
# ---------- 2. vormen (vlakken die elk hun eigen licht/schaduw krijgen), uit de anatomie van het model
FORM=np.zeros((H,Wd),'U8')
HX={13:20,14:20,15:19,16:18,17:17,18:13,19:12,20:11,21:11,22:11}
cx,cy,rx,ry=35.9,33.4,5.7,5.1
def inell(x,y,sh=0): return ((x+.5-cx)/(rx-sh))**2+((y+.5-cy)/(ry-sh))**2<=1
for y in range(H):
    for x in range(Wd):
        if a[y,x]==0: continue
        if y<=12 or (y in HX and x<=HX[y]): f='kop'
        elif (23<=y<=31 and x<=15) or (32<=y<=33 and x<=13): f='voorp'
        elif y>=30 and 17<=x<=26 and not (y<=31 and x>=24): f='been'
        elif y>=39 and 15<=x<=24: f='been'
        elif 31<=y<=39 and 27<=x<=29 and not inell(x,y): f='gat'      # donkere spleet tussen voorpoot en dij
        elif inell(x,y) or (y>=37 and 30<=x<=41): f='dij'
        elif x>=43 and y>=31: f='staart'
        else: f='romp'
        FORM[y,x]=f
# ---------- 3. bevroren kenmerken (uit het model / eerdere rondes): oog, neus, mond/tanden/tong, oorbinnenkant, patronen, teenlijnen
frozen=np.zeros((H,Wd),bool)
frozen[8:12,8:15]=True                     # oog (oog 1 px links)
frozen[13:17,1:7]=True                     # neus
frozen[16:24,3:14]&=True
for y in range(16,24):
    for x in range(2,14):
        if FORM[y,x]=='kop': frozen[y,x]=True   # mond, tanden, tong, kin
for (x0,x1,y0,y1) in ((4,10,0,6),(17,25,0,9)):  # oren: binnenkant en oorlijnen zoals het model
    for y in range(y0,y1):
        for x in range(x0,x1):
            if a[y,x] in (S,K,d) and not (y==0 or a[y-1,x]==0): frozen[y,x]=True
PAT=np.isin(a,[P,Q,R,C])
frozen|=PAT
for y in range(17,33):                      # schouderspiraal: hele schijf incl. bruin en lijnen
    for x in range(16,32):
        if (x+.5-24)**2+(y+.5-25)**2<=6.6**2 and a[y,x]!=0 and a[y,x]!=K: frozen[y,x]=True
for (x,y) in ((20,41),(19,42),(19,43),(32,41),(32,42),(35,41),(35,42)): frozen[y,x]=True
frozen[0:8,4:17]|=np.isin(a[0:8,4:17],[P,Q,R])
# ---------- 4. belijning: silhouetrand zwart aan de schaduwkant, lijnbruin (selout) aan de lichtkant;
#             binnenlijnen alleen tussen twee vormen (in lijnbruin), lijnen binnen één vlak verdwijnen in de vulling
def bgnb(y,x): return [(dy,dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if not(0<=y+dy<H and 0<=x+dx<Wd) or a[y+dy,x+dx]==0]
edge=np.zeros((H,Wd),bool)
for y in range(H):
    for x in range(Wd):
        if a[y,x] and bgnb(y,x): edge[y,x]=True
n_lijn_weg=0; n_lijn_kleur=0
b=a.copy()
for y in range(H):
    for x in range(Wd):
        if a[y,x]==0: continue
        if edge[y,x]:
            if a[y,x] in (W,T,G,g_) : continue
            nb=bgnb(y,x)
            v=K if any(t in nb for t in ((1,0),(0,1))) else d
            if b[y,x]!=v: b[y,x]=v; n_lijn_kleur+=1
            continue
        if a[y,x] in LIJN and not frozen[y,x]:
            run=1; yy=y-1
            while yy>=0 and a[yy,x] in LIJN: run+=1; yy-=1
            yy=y+1
            while yy<H and a[yy,x] in LIJN: run+=1; yy+=1
            if FORM[y,x]=='voorp' or (FORM[y,x]=='been' and run>=4):
                if b[y,x]!=d: b[y,x]=d; n_lijn_kleur+=1
            else:
                b[y,x]=0xFF; n_lijn_weg+=1          # wordt vulling
ORDER={'voorp':0,'kop':1,'been':2,'dij':3,'romp':4,'staart':5,'gat':9}
n_grens=0
for y in range(H):
    for x in range(Wd):
        if b[y,x]==0 or edge[y,x] or frozen[y,x] or b[y,x] in (K,d): continue
        F=FORM[y,x]
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<Wd and b[yy,xx]!=0 and FORM[yy,xx] and ORDER[FORM[yy,xx]]<ORDER[F] and b[yy,xx]!=d and not (F=='gat' and FORM[yy,xx]!='been') and not (FORM[yy,xx]=='kop' and F=='romp' and x>=21):
                b[y,x]=d; n_grens+=1; break
log['vormgrens_lijn']=n_grens
a=b; log['lijn_weg']=n_lijn_weg; log['lijn_omgekleurd']=n_lijn_kleur
# dubbele binnenlijnen (2 px dik) dunnen: een lijnpixel die zelf niet aan vulling van zijn eigen vorm grenst
# aan beide kanten en een lijnbuur loodrecht heeft, wordt vulling (houdt de lijn aan de voorste vorm)
n_dun=0
for it in range(2):
    for y in range(1,H-1):
        for x in range(1,Wd-1):
            if a[y,x]!=d or edge[y,x] or frozen[y,x]: continue
            for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
                y2,x2=y+dy,x+dx
                if a[y2,x2] in LIJN and not edge[y2,x2]:
                    # lijn is 2 dik in richting (dy,dx) als aan de overkant van beide vulling ligt
                    yb,xb=y-dy,x-dx; yc,xc=y2+dy,x2+dx
                    if 0<=yc<H and 0<=xc<Wd and a[yb,xb] not in LIJN and a[yb,xb]!=0 and a[yc,xc] not in LIJN and a[yc,xc]!=0:
                        a[y,x]=0xFF; n_dun+=1; break
log['lijn_gedund']=n_dun
# spirallijnen in de schouder: lijnbruin -> schaduwbruin (Jordi: de dikke belijning maakt het niet beter); vorm ongewijzigd
for y in range(17,33):
    for x in range(16,32):
        if frozen[y,x] and a[y,x]==d and (x+.5-24)**2+(y+.5-25)**2<=5.6**2: a[y,x]=S
# ---------- 5. schaduw per vorm: licht linksboven, sikkel rechtsonder die de vorm volgt, hooglicht op de bovenvlakken
WID={'gat':(9,0),'kop':(2,2),'romp':(2,2),'voorp':(2,2),'been':(2,1),'dij':(2,2),'staart':(1,1)}
def inF(y,x,f): return 0<=y<H and 0<=x<Wd and a[y,x]!=0 and FORM[y,x]==f and not (edge[y,x])
n_vul=0
new=a.copy()
for y in range(H):
    for x in range(Wd):
        v=a[y,x]
        if v==0 or edge[y,x] or frozen[y,x] or (v in LIJN): continue
        f=FORM[y,x]; ws,wl=WID[f]
        def near(dirs,w):
            for k in range(1,w+1):
                for dy,dx in dirs:
                    yy,xx=y+dy*k,x+dx*k
                    if not(0<=yy<H and 0<=xx<Wd) or a[yy,xx]==0 or FORM[yy,xx]!=f or edge[yy,xx]:
                        return True
            return False
        if near(((1,1),(1,0),(0,1)),ws): t=S
        elif near(((-1,-1),(-1,0),(0,-1)),wl): t=L
        else: t=M
        if t!=v: n_vul+=1
        new[y,x]=t
a=new; log['vul_herschaduwd']=n_vul
# ---------- 6. ontkorrelen (Krassault): bruine vulclusters < 4 px naar de buurtint, kenmerken/patronen bevroren
n_korrel=0
for it in range(3):
    seen=np.zeros_like(a,bool)
    for j in range(H):
        for i in range(Wd):
            if seen[j,i] or a[j,i] not in BR: continue
            c=a[j,i]; st=[(j,i)]; cl=[]; seen[j,i]=True
            while st:
                y,x=st.pop(); cl.append((y,x))
                for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                    if 0<=yy<H and 0<=xx<Wd and not seen[yy,xx] and a[yy,xx]==c: seen[yy,xx]=True; st.append((yy,xx))
            if len(cl)<4 and not any(frozen[y,x] for y,x in cl):
                cnt={}
                for y,x in cl:
                    for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                        if 0<=yy<H and 0<=xx<Wd and a[yy,xx] in BR and a[yy,xx]!=c and FORM[yy,xx]==FORM[y,x]: cnt[a[yy,xx]]=cnt.get(a[yy,xx],0)+1
                if cnt:
                    v=max(cnt,key=cnt.get)
                    for y,x in cl: a[y,x]=v; n_korrel+=1
log['ontkorreld']=n_korrel
assert not (a==0xFF).any()
np.save('welp_r4.npy',a); np.save('form.npy',FORM)
fig=(a>0).sum(); fig3=(r3>0).sum()
log['zwart_voor_%']=round(100*(r3==K).sum()/fig3,1); log['zwart_na_%']=round(100*(a==K).sum()/fig,1)
log['lijnbruin_voor_%']=round(100*(r3==d).sum()/fig3,1); log['lijnbruin_na_%']=round(100*(a==d).sum()/fig,1)
print(log)
