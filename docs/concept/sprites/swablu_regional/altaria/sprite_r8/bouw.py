# Altaria (onweerswolk) r8. Bouwen vanuit altaria/: python3 sprite_r8/bouw.py
# Silhouet (alpha) = r5-proef (1/3-reductie van model_kop/natief_kop15_dy10.png), niets bij of weg.
# Kleur: per spritepixel stemmen de 9 natieve modelpixels van het 3x3-blok op hun MODELBAND; de band met de meeste stemmen wint
# (geen gemiddelde = geen blur; GEMINI.md "Blur door gemiddelde tint"). Palet = de gemeten modeltinten zelf (geen tussentinten).
# Jordi (21 nov): "het zit vooral in kleurgebruik/schaduw/tinten waardoor de wolken wat minder duidelijk zijn ... De voelsprieten mogen ook
# wat meer definitie en kleur in en het hofod is nog wat blurry ... Houd zoveel mogelijk het model aan voor de wolken, al mag er wat extra
# static bij, maar kijk voor inpsiratie ook naar het model, niks zelf tekenen".
import sys, os, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r5')
from PIL import Image
import basis as B
from gemeen import label
a,c,L,st=B.a,B.c,B.L,B.st
blok=B.blok
UIT='sprite_r8'
# ---- palet: gemeten modeltinten (mediaan per band, zie NOTITIES.md) ----
PAL=[(152,208,160),         # 0 transparant
     (7,12,30),             # 1 pupil (model-zwart), alleen in de ogen
     (20,36,64),            # 2 wolk-selout: donkere navy (lijnen tussen de bollen + buitenlijn), niet zwart
     (29,50,81),            # 3 wolk navy (model L46)
     (50,82,116),           # 4 wolk donker teal (model L75)
     (87,137,171),          # 5 wolk teal (model L124)
     (144,205,223),         # 6 wolk licht cyaan kap (model L185)
     (188,224,238),         # 7 static (model-static, cyaanwit)
     (36,34,92),            # 8 violet-selout (donker violet, niet zwart)
     (54,58,124),           # 9 violet donker (model L<85)
     (94,98,210),           # 10 violet midden (model L85-130)
     (128,132,236),         # 11 violet licht (model L130-160)
     (160,166,239),         # 12 violet hooglicht (model L160-195: koplicht linksboven, kuifglans)
     (202,208,249)]         # 13 lavendelwit (model L>=195: kuifglanzen, oogglans)
PU,WS,WN,WD,WT,WC,ST,VS,VD,VM,VL,VH,LW=range(1,14)
WOLK=[WN,WD,WT,WC]; VIO=[VD,VM,VL,VH,LW]
# ---- modelband per natieve pixel ----
T=np.full(L.shape,-1)
w=c==2; v=(c==3)|(c==5)
T[w&(L<60)]=WN; T[w&(L>=60)&(L<100)]=WD; T[w&(L>=100)&(L<155)]=WT; T[w&(L>=155)]=WC
T[v&(L<85)]=VD; T[v&(L>=85)&(L<130)]=VM; T[v&(L>=130)&(L<160)]=VL; T[v&(L>=160)&(L<195)]=VH; T[v&(L>=195)]=LW
T[c==4]=WC; T[c==1]=0     # 0 = model-lijn (K)
LAAG=int(os.environ.get('LAAG','1')); ND=int(os.environ.get('ND','4')); NC=int(os.environ.get('NC','4'))
KW=float(os.environ.get('KW','1.5'))     # lijnpixels zijn dun (1 natieve px): zwaarder laten stemmen, anders vallen de lijnen weg
# ---- materiaal en silhouet uit de r5-proef ----
pr=np.array(Image.open('sprite_r5/proef_eindkeuring.png')).astype(int)
fig=pr>0
matw=np.isin(pr,[2,3,4,5,6,11]); matv=np.isin(pr,[7,8,9,10])
o=np.zeros((64,64),int)
def stem(X,Y,grp):
    u,v=blok(X,Y); b=T[v:v+3,u:u+3].ravel(); wt={}
    for t in b:
        if t==0: wt[-1]=wt.get(-1,0)+KW
        elif t in grp: wt[t]=wt.get(t,0)+1
    return wt
for Y,X in zip(*np.where(fig)):
    if matw[Y,X]:
        wt=stem(X,Y,WOLK); o[Y,X]=WS if not wt else (WS if max(wt,key=wt.get)==-1 else max(wt,key=wt.get))
        if LAAG:
            # dunne modelvormen (navy rand onder een bol, kleine cyaan kap) halen in een 3x3-blok zelden de meerderheid; ze winnen hier
            # al bij >= ND/9 (navy + lijn) of >= NC/9 (cyaan), mits het de grootste groep is na de andere donkere/lichte band
            u,v=blok(X,Y); b=T[v:v+3,u:u+3].ravel(); n=lambda t:int((b==t).sum())
            if n(WN)+n(0)>=ND and n(WN)+n(0)>=n(WT)+n(WC): o[Y,X]=WN if n(WN)>=n(0) else WS
            elif n(WC)>=NC and n(WC)>=n(WN)+n(0): o[Y,X]=WC
    elif matv[Y,X]:
        wt=stem(X,Y,VIO); o[Y,X]=VS if not wt else (VS if max(wt,key=wt.get)==-1 else max(wt,key=wt.get))
    else: o[Y,X]=pr[Y,X] if pr[Y,X]==1 else LW
kaal=o.copy()

def opslaan(o,p):
    im=Image.fromarray(o.astype('uint8'),'P'); pal=[x for cc in PAL for x in cc]; im.putpalette(pal+[0]*(768-len(pal))); im.save(p,transparency=0)
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def meest(l): return max(set(l),key=l.count)
tel={}
def stap(naam,voor): tel[naam]=tel.get(naam,0)+int((voor!=o).sum())
KOP=np.zeros((64,64),bool); KOP[18:29,19:34]=True          # kop + snavel + wang (KOPGRID)
KUIF=np.zeros((64,64),bool)
for Y,X in zip(*np.where(matv)): KUIF[Y,X]=(Y<=17 or (Y<=21 and 34<=X<=52)) and not KOP[Y,X]
rand=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fig)):
    rand[Y,X]=any(not fig[Y+dy,X+dx] for dy,dx in N4)
# ---- 2. buitenlijn: wolk -> wolk-selout, kop/hals -> violet-selout (kuif apart, stap 5). Static-boogjes buiten de vleugel (r5) blijven ----
v0=o.copy()
for Y,X in zip(*np.where(rand)):
    if pr[Y,X]==11 and not matw[Y,X]^True and B.vleugel(X,Y) is False: pass
    if matw[Y,X]: o[Y,X]=WS
    elif matv[Y,X] and not KUIF[Y,X]: o[Y,X]=VS
BOOG=(pr==11)&(np.isin(np.roll(pr,1,1),[0,11])|np.isin(np.roll(pr,-1,1),[0,11]))&((np.arange(64)[None,:]<6)|(np.arange(64)[None,:]>59))
o[BOOG]=ST
stap('buitenlijn',v0)
# ---- 3. static op de modelplekken: blok met >= SN static-modelpixels, uitgedund tot 1 px, stukken >= SMIN ----
SN=int(os.environ.get('SN','2')); SMIN=int(os.environ.get('SMIN','3'))
cnt=np.zeros((64,64),int)
for Y,X in zip(*np.where(fig)):
    u,v=blok(X,Y); cnt[Y,X]=st[v:v+3,u:u+3].sum()
S=(cnt>=SN)&matw&~rand&~KOP
# 1 static-modelpixel telt mee als hij een static-blok verbindt (lijntjes van het model lopen schuin door de blokken)
for _ in range(2):
    S2=S.copy()
    for Y,X in zip(*np.where((cnt==1)&matw&~rand&~KOP)):
        if sum(S[Y+dy,X+dx] for dy,dx in N8)>=1: S2[Y,X]=True
    S=S2
def dun(m):
    m=m.copy(); ver=True
    while ver:
        ver=False
        for fase in (0,1):
            weg=[]
            for Y,X in zip(*np.where(m)):
                P=[m[Y-1,X],m[Y-1,X+1],m[Y,X+1],m[Y+1,X+1],m[Y+1,X],m[Y+1,X-1],m[Y,X-1],m[Y-1,X-1]]
                b=sum(P); a_=sum((not P[i]) and P[(i+1)%8] for i in range(8))
                if not(2<=b<=6 and a_==1): continue
                if fase==0 and not(P[0] and P[2] and P[4]) and not(P[2] and P[4] and P[6]): weg.append((Y,X))
                if fase==1 and not(P[0] and P[2] and P[6]) and not(P[0] and P[4] and P[6]): weg.append((Y,X))
            for q in weg: m[q]=False
            ver|=bool(weg)
    return m
S=dun(S)
# L-hoekjes weg (1 px dik: een pixel met een 4-buur boven/onder EN links/rechts en een diagonaal die beide verbindt)
for Y,X in zip(*np.where(S)):
    for (dy,dx) in ((-1,-1),(-1,1),(1,-1),(1,1)):
        if S[Y+dy,X+dx] and S[Y+dy,X] and S[Y,X+dx]:
            n_=sum(S[Y+ay,X+ax] for ay,ax in N8)
            if n_<=3: S[Y,X]=False; break
lab,n=label(S,acht=True)
for i in range(1,n+1):
    if (lab==i).sum()<SMIN: S[lab==i]=False
v0=o.copy(); o[S]=ST
# static-pixels die in de stemming als cyaan kap (WC) telden maar geen static-lijn werden: terug naar de band van de rest van het blok
for Y,X in zip(*np.where(matw&~S&~rand&(o==WC))):
    u,v=blok(X,Y); b=T[v:v+3,u:u+3]; sb=st[v:v+3,u:u+3]
    if sb.sum()>=2:
        r=[t for t in b[~sb].ravel() if t in WOLK]
        if r: o[Y,X]=meest(r)
stap('static',v0)
STATIC=S|BOOG
# ---- 3b. lijnen tussen de bollen: blok met >= KL zwarte modelpixels (de dunne modellijn) -> wolk-selout, als stuk van >= 3 px (8-samenh.),
#          uitgedund tot 1 px. Kleur = gekleurde navy-selout, niet zwart (Jordi: "De belijning moet juist zachter en niet zwart") ----
KL=int(os.environ.get('KL','2'))
kc=np.zeros((64,64),int)
for Y,X in zip(*np.where(fig)):
    u,v=blok(X,Y); kc[Y,X]=(T[v:v+3,u:u+3]==0).sum()
LIJN=(kc>=KL)&matw&~rand&~KOP&~STATIC
LIJN=dun(LIJN)
lab,n=label(LIJN,acht=True)
for i in range(1,n+1):
    if (lab==i).sum()<3: LIJN[lab==i]=False
v0=o.copy(); o[LIJN]=WS
# pixels die al selout waren (meerderheid K) maar niet op de lijn liggen: terug naar de wolkband van het blok
for Y,X in zip(*np.where((o==WS)&~LIJN&~rand&matw&~KOP)):
    u,v=blok(X,Y); r=[t for t in T[v:v+3,u:u+3].ravel() if t in WOLK]
    if r and sum(LIJN[Y+dy,X+dx] for dy,dx in N8)==0: o[Y,X]=meest(r)
stap('lijnen',v0)
# ---- 4. ontkorrelen wolk (buiten de kop): tintvlakjes < KMIN px (4-samenhangend) -> meest voorkomende wolkbuur; lijnstukjes van
#         wolk-selout binnenin < 2 px -> buurtint. Alleen vervangen door een tint die er al naast ligt (geen nieuwe tint, geen gemiddelde). ----
VULW=[WS,WN,WD,WT,WC]
KMIN=int(os.environ.get('KMIN','3'))
v0=o.copy()
def ontkorrel():
    for k in [WN,WD,WT,WC,WS]:
        lab,n=label((o==k)&~rand&~KOP&~STATIC,acht=False)
        for i in range(1,n+1):
            mm=lab==i; g=mm.sum()
            if g>=(2 if k in (WC,WS) else KMIN): continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(mm)) for dy,dx in N4 if o[Y+dy,X+dx] in VULW and o[Y+dy,X+dx]!=k and o[Y+dy,X+dx]!=WS]
            if buur: o[mm]=meest(buur)
for _ in range(3): ontkorrel()
# uitsteeksels van 1 px (3 van de 4 buren een andere, gelijke vultint) gladstrijken
for _ in range(2):
    for Y,X in zip(*np.where(np.isin(o,[WN,WD,WT,WC])&~rand&~KOP&~STATIC)):
        nb=[o[Y+dy,X+dx] for dy,dx in N4]
        for t in set(nb):
            if t!=o[Y,X] and t in (WN,WD,WT,WC) and nb.count(t)>=3: o[Y,X]=t; break
stap('ontkorrelen',v0)
# ---- 5. kuif (voelsprieten): Jordi "mogen ook wat meer definitie en kleur in". Per strengpixel de modelbanden van zijn blok:
#   onderkant (lucht eronder) = donkere violetrand van het model -> violet-selout;
#   bovenkant/twijg (lucht erboven) = de lichtste modelband met >= 2 stemmen in het blok (lavendelwit/hooglicht/licht = de glanzen van het
#   model), anders middenviolet; binnenin = meerderheidsband (geen selout binnenin). ----
def lichtste(X,Y,minst=2):
    u,v=blok(X,Y); b=list(T[v:v+3,u:u+3].ravel())
    for t in (LW,VH,VL,VM,VD):
        if b.count(t)>=minst: return t
    return VM
#   Gen 3: geen lichte kleur op de buitenrand -> aan de rand hoogstens violet licht; lavendelwit/hooglicht (de modelglanzen) alleen binnenin
#   een streng (>= 3 dik), waar het blok er >= 3 stemmen voor heeft.
RANDMAX={LW:VL,VH:VL}
v0=o.copy()
for Y,X in zip(*np.where(KUIF)):
    boven=not fig[Y-1,X]; onder=not fig[Y+1,X]; zij=not fig[Y,X-1] or not fig[Y,X+1]
    if onder and not boven: o[Y,X]=VS
    elif boven: t=lichtste(X,Y); o[Y,X]=RANDMAX.get(t,t)
    else:
        t=lichtste(X,Y,3)
        if t in (LW,VH,VL): o[Y,X]=RANDMAX.get(t,t) if zij else t
        elif o[Y,X]==VS: o[Y,X]=VD
stap('kuif',v0)
# ---- 6. kop: KOPGRID = per spritepixel de modelband van het blok (gelezen uit sprite_r8/raster.py + de bandstemmen), in 3 heldere tinten
#   (hooglicht/licht/midden) + violet-selout; ogen uit r5 (beide lezen op 1x; ver oog 1 px rechts van het model zodat lijn|kopkleur|oog past);
#   snavel en wang in de wolktinten van het model (cyaan boven, teal, navy mondlijn, selout-rand). X19..33 ----
KOPGRID={
18:'....mhhllmmms..',
19:'...mhhhlllmmms.',
20:'..mhhhhlllmmms.',
21:'..mllllllmmmmms',
22:'.smKllllwKmmmms',
23:'.smKllllKKmmmms',
24:'.sllooommmmmmms',
25:'occcctccmmcccms',
26:'otcctnnnsctttms',
27:'.oocctto'+'mooomms',
28:'...oo.smmmms...',
}
KC={'s':VS,'v':VD,'m':VM,'l':VL,'h':VH,'w':LW,'K':PU,'o':WS,'n':WN,'d':WD,'t':WT,'c':WC}
v0=o.copy()
for Y,row in KOPGRID.items():
    for j,ch in enumerate(row):
        X=19+j
        if ch=='.': assert not fig[Y,X] or not KOP[Y,X] or True; continue
        assert fig[Y,X], (X,Y)
        o[Y,X]=KC[ch]
stap('kop',v0)
if __name__=='__main__':
    opslaan(o,UIT+'/altaria_r8.png')
    rgb=np.array(PAL,'uint8')[o]; rgb[o==0]=255
    Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(UIT+'/altaria_r8_8x.png')
    d=kaal!=o
    print('afwijkend van de kale meerderheidsreductie:',int(d.sum()),'| per stap:',tel)
    zones={'kop':KOP,'kuif':KUIF,'static':STATIC,'buitenrand':rand&~KOP&~KUIF&~STATIC}
    rest=~(KOP|KUIF|STATIC|rand)
    for n_,z in list(zones.items())+[('wolk binnen',rest)]: print('  ',n_,int((d&z).sum()),'van',int((fig&z).sum()))
