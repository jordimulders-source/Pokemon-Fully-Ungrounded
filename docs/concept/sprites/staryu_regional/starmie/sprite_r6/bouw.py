# bouw.py r6: python3 sprite_r6/bouw.py licht|sterk|jordi   (vanuit starmie/)
# Jordi na r5: "de punten van de voorkant moeten ook minder puntig van starmie".
# licht/sterk: basis = r5_licht/r5_sterk (achterpunten al afgestompt); de vijf punten van de VOORSTE ster krijgen
#   dezelfde snede als stomp.py r5: loodrecht op de as (juweelmidden -> modeltip) afsnijden waar de punt voor het
#   eerst W px breed is (licht 4, sterk 5). Alleen weghalen.
# jordi: basis = r5 zonder afstompen; alle tien punten (voor en achter) afgestompt naar de twee Gen 3-punten die
#   Jordi aanwees ("meet desnoods de hoek van de originele starmie sprite op deze twee": de lichte punt naar rechts
#   'rl' en de donkere punt naar rechtsonder 'br', gereedschap/g3punten.py): snede waar de punt 4 px breed is
#   (plat eind ±4 px zoals beide Gen 3-tips), daarna per schijf (1 px dik, loodrecht op de as) de buitenste pixels
#   weg zolang de schijf breder is dan het Gen 3-doel (gemiddelde van rl en br): 4 / 5 / 5 / 6 px op 0/1/2/3 px
#   van de nieuwe tip. Alleen weghalen, binnen het modelsilhouet.
# Daarna: buitenlijn zoals r5 (rechts/onder zwart, links/boven koek donker), koekrand blijft: glazuurpixels die
# direct achter de nieuwe buitenlijn komen te liggen krijgen de koektint van de dichtstbijzijnde modelrand.
import sys, numpy as np; from PIL import Image
MODE=sys.argv[1]; W_={'licht':4.0,'sterk':5.0,'jordi':4.0}[MODE]
DOEL=[4.5,5.1,5.4,6.9]          # max. schijfbreedte op 0/1/2/3 px van de tip (Gen 3 rl/br gemiddeld 4,0/4,6/4,9/6,4 + 0,5), alleen bij jordi
BASIS={'licht':'sprite_r5/starmie_r5_licht.png','sterk':'sprite_r5/starmie_r5_sterk.png','jordi':'sprite_r5/starmie_r5.png'}[MODE]
im=Image.open(BASIS); PAL=im.getpalette(); o=np.array(im).astype(int); o0=o.copy()
PNAAM=np.load('sprite_r5/gereedschap/pnaam.npy')            # namen van de achterpunten ('' = voorste ster)
KERN=np.array([31.5,30.5])
VTIPS={'v_boven':(30.5,2.5),'v_links':(3.5,21.5),'v_rechts':(58.5,21.5),'v_linksonder':(14.5,54.5),'v_rechtsonder':(46.5,53.5)}
def hk(x,y): return np.degrees(np.arctan2(KERN[1]-y,x-KERN[0]))
voor=(o>0)&(PNAAM=='')
NAAM=np.full((64,64),'',object)
for y,x in zip(*np.where(voor)):
    h=hk(x+.5,y+.5); NAAM[y,x]=min(VTIPS,key=lambda n:abs((hk(*VTIPS[n])-h+180)%360-180))
for y,x in zip(*np.where((o>0)&(PNAAM!=''))): NAAM[y,x]=str(PNAAM[y,x])
log={}
def zet(x,y,k,stap):
    if o[y,x]!=k: o[y,x]=k; log.setdefault(stap,[]).append((int(x),int(y)))
def geom(nm):
    m=(NAAM==nm)&(o>0); ys,xs=np.where(m); p=np.stack([xs+.5,ys+.5],1)
    d=np.hypot(*(p-KERN).T); tip=p[np.argmax(d)]; ax=(tip-KERN)/np.linalg.norm(tip-KERN); pe=np.array([-ax[1],ax[0]])
    return xs,ys,(p-KERN)@ax,(p-KERN)@pe,ax
def meet(nm,ax,sc=None,n=4):
    """breedte per schijf van 1 px vanaf de tip, langs de vaste modelas ax; alleen pixels dicht bij de as (|s-sc|<6)."""
    m=(NAAM==nm)&(o>0); ys,xs=np.where(m); p=np.stack([xs+.5,ys+.5],1); pe=np.array([-ax[1],ax[0]])
    t=(p-KERN)@ax; s=(p-KERN)@pe
    if sc is None: sc=s[np.argmax(t)]
    loc=np.abs(s-sc)<6; T=t[loc].max(); out=[]
    for k in range(n):
        sl=loc&(t>T-k-1)&(t<=T-k); out.append(round(float(s[sl].max()-s[sl].min()+1),1) if sl.any() else 0)
    return out,round(float(T),1)
def spoor(nm):
    """1-px uitsteeksels (hoogstens 1 buur van 4) in de punt: weghalen (herhaald)."""
    n=0; ch=True
    while ch:
        ch=False
        for y,x in zip(*np.where((NAAM==nm)&(o>0))):
            if sum(o[y+j,x+i]>0 for j,i in ((-1,0),(1,0),(0,-1),(0,1)))<=1: zet(x,y,0,'uitsteeksel '+nm); n+=1; ch=True
    return n
INFO={}; HARTLIJN={}
PUNTEN=list(VTIPS)+['linksboven','rechtsboven','linksonder','rechtsonder','onder']
for nm in PUNTEN:
    xs,ys,t,s,ax=geom(nm); T=t.max(); cut=T; sc=s[np.argmax(t)]
    voor_prof,T0=meet(nm,ax,sc)
    weg=[]; n_trim=0
    if MODE=='jordi' or nm in VTIPS:
        loc=np.abs(s-sc)<6
        for k in np.arange(0,12,0.5):
            sl=loc&(t>T-k-1)&(t<=T-k)
            if sl.any() and s[sl].max()-s[sl].min()+1>=W_: cut=T-k; break
        weg=[(x,y) for x,y,tt in zip(xs,ys,t) if tt>cut]
        for x,y in weg: zet(x,y,0,'snede '+nm)
    if MODE=='jordi':
        # tipvorm naar de Gen 3-punten rl/br: per schijf vanaf de snede max. DOEL[k] px breed rond het midden van het platte eind
        ys,xs=np.where((NAAM==nm)&(o>0)); p=np.stack([xs+.5,ys+.5],1); pe=np.array([-ax[1],ax[0]])
        t=(p-KERN)@ax; s=(p-KERN)@pe
        loc=np.abs(s-sc)<6; Tn=t[loc].max()
        # tipvorm langs de eigen hartlijn van de punt (midden op 6 px -> midden van het eind), niet langs de straal uit de kern:
        # bij een punt die schuin op die straal staat (v_rechts) gaf de straal een kerf in de rand
        def mid(a,b):
            m=loc&(t>Tn-b)&(t<=Tn-a); i0=np.argmin(np.where(m,s,1e9)); i1=np.argmax(np.where(m,s,-1e9)); return (p[i0]+p[i1])/2
        m0=mid(0,1); m6=mid(5,7); ax2=(m0-m6)/np.linalg.norm(m0-m6)          # hartlijn: midden op 6 px -> midden van het platte eind
        pe2=np.array([-ax2[1],ax2[0]]); t=(p-m6)@ax2; s=(p-m6)@pe2; Tn=t[loc].max()
        s3=s[loc&(t>Tn-4)&(t<=Tn-3)]; c0=(s3.min()+s3.max())/2   # midden van de punt op 3 px
        HARTLIJN[nm]=round(float(np.degrees(np.arctan2(-ax2[1],ax2[0]))),1)
        # alleen randpixels (met een transparante buur), van buiten naar binnen, tot stabiel: geen gaten
        kand=sorted([(abs(ss-c0),x,y) for x,y,tt,ss,lc in zip(xs,ys,t,s,loc)
                     for k,mx in enumerate(DOEL) if lc and Tn-k-1<tt<=Tn-k and abs(ss-c0)>(mx-1)/2+0.01],reverse=True)
        ch=True
        while ch:
            ch=False
            for _,x,y in kand:
                if o[y,x]>0 and any(o[y+j,x+i]==0 for j,i in ((-1,0),(1,0),(0,-1),(0,1))):
                    zet(x,y,0,'tipvorm '+nm); n_trim+=1; ch=True
        # deuken: een weggehaalde pixel die nu aan 3+ kanten figuur heeft, of in zijn rij/kolom binnen 3 px aan beide kanten
        #         figuur heeft (kerf/haak in de rand) -> modelpixel terug
        ch=True
        while ch:
            ch=False
            for x,y in list(log.get('tipvorm '+nm,[])):
                brug=any(any(o[y+j*d,x+i*d]>0 for d in (1,2,3)) and any(o[y-j*d,x-i*d]>0 for d in (1,2,3)) for j,i in ((0,1),(1,0)))
                if o[y,x]==0 and (sum(o[y+j,x+i]>0 for j,i in ((-1,0),(1,0),(0,-1),(0,1)))>=3 or brug):
                    o[y,x]=o0[y,x]; log['tipvorm '+nm].remove((x,y)); n_trim-=1; ch=True
    n_sp=spoor(nm)
    na,T1=meet(nm,ax,sc)
    INFO[nm]=dict(richting=round(float(np.degrees(np.arctan2(-ax[1],ax[0]))),1),lengte_voor=T0,lengte_na=T1,
                  weg=len(weg)+n_trim+n_sp,snede=len(weg),tipvorm=n_trim,uitsteeksel=n_sp,breedte_voor=voor_prof,breedte_na=na)
# --- buitenlijn zoals r5: rand naar transparant rechts/onder = zwart, links/boven = koek donker
fg=o>0; nieuw=[]
for y,x in zip(*np.where(fg)):
    r=not fg[y,x+1]; b=not fg[y+1,x]; l=not fg[y,x-1]; t_=not fg[y-1,x]
    if not (r or b or l or t_) or o[y,x]==1: continue
    k=1 if (r or b) else 2
    if o[y,x]!=k: zet(x,y,k,'buitenlijn'); nieuw.append((x,y))
# --- koekrand: glazuur (paars, paarse lijn, wit, hagelslag) direct achter een nieuwe buitenlijnpixel -> koekrandtint
GLAZUUR={7,8,9,10,11,12,13,14}; KOEKT=(3,4,5,6)
rand=[(x,y) for x,y in np.argwhere(o0>0)[:,::-1] if NAAM[y,x] in VTIPS and o0[y,x] in KOEKT]
for x,y in nieuw:
    if NAAM[y,x] not in VTIPS: continue
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            X,Y=x+dx,y+dy
            if o[Y,X] in GLAZUUR and NAAM[Y,X] in VTIPS and all(o[Y+j,X+i]>0 for j,i in ((-1,0),(1,0),(0,-1),(0,1))):
                kx,ky=min(rand,key=lambda p:(p[0]-X)**2+(p[1]-Y)**2); zet(X,Y,int(o0[ky,kx]),'koekrand naar binnen')
# --- losse zwarte pixels -> koek donker
for y,x in zip(*np.where(o==1)):
    if all(o[y+dy,x+dx]!=1 for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): zet(x,y,2,'losse zwarte pixel')
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(PAL); p.save('sprite_r6/starmie_r6_%s.png'%MODE,transparency=0)
# --- rapport en controle
print('MODE',MODE,'basis',BASIS); print('hartlijn (jordi-tipvorm)',HARTLIJN)
for nm,v in INFO.items(): print(nm,v)
for k,v in log.items(): print(k,len(v),v if len(v)<=12 else '')
fg=o>0; yy,xx=np.where(fg); print('figuur x%d-%d y%d-%d %dx%d, %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
rnd=[(x,y) for y,x in zip(*np.where(fg)) if any(not fg[y+j,x+i] for j,i in ((-1,0),(1,0),(0,-1),(0,1)))]
print('kleuren',len(set(o.flatten())),'| lichte buitenrand',[p for p in rnd if o[p[1],p[0]] not in (1,2)],
      '| losse zwart',[(x,y) for y,x in zip(*np.where(o==1)) if all(o[y+j,x+i]!=1 for j in (-1,0,1) for i in (-1,0,1) if j or i)])
d=o!=o0; print('diff t.o.v. basis',int(d.sum()),'px; buiten de punten',int((d&(NAAM=='')).sum()),'; in de achterpunten',int((d&(PNAAM!='')).sum()))
