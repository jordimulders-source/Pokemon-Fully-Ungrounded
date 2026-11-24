# Claydol-regional r2. Onderlaag = kale reductie van het r2-model (kaal2.py). Stappen, elk met telling:
#  1 tintvlakken (Jordi: "veel pixelblur"): per vlak de modelhelderheid zacht gemiddeld (gauss, alleen binnen het vlak, lijnen tellen
#    niet mee) en op de dichtstbijzijnde paletstap van dat vlak gezet (+8 helderheid: lijf/kopo nderkant waren een tint te donker);
#    daarna tintvlakjes < 3 px opgelost in de buurtint. Lijnen (zwart), rood, streepjes en stipjes blijven staan.
#  2 krans (Jordi: "consistentere vorm, teveel rechte lijnen"): elk bolletje = één asset uit het model (R4-bolletje, natief, het rondste;
#    stipjesversie uit r6, streepjesversie uit r5 op dezelfde plek), achter de kop geplaatst op het midden van het oude bolletje.
#  3 buitenlijn + selout (zoals r1), keurderpunten, staven 1 px naar binnen.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'claydol_sprite_r2'); sys.path.insert(0,'claydol_sprite_r1')
from kaal2 import kaal, RIJEN, KOLOMMEN
from klassen import klasse, PAL
SCHUIF=int(sys.argv[1]) if len(sys.argv)>1 else 2
S,A,NY,NX=kaal(SCHUIF); KAAL=S.copy()
PL=np.array(PAL).mean(1)
LM=A.mean(2)+8
log={}
def tel(n,y,x,o,v): log.setdefault(n,[]).append((x,y,o,v))
# ---- vlakken (natieve coördinaten) ----
hd=((NX-48)/24.0)**2+((NY-40)/15.5)**2
def doog(cx,cy,rx,ry): return np.sqrt(((NX-cx-SCHUIF)/rx)**2+((NY-cy)/ry)**2)
d1=doog(32.0,40.5,6.0,6.5); d2=doog(50.5,41.5,6.5,6.5)
V=np.full((64,64),'',dtype='<U10'); op=S>0
V[op]='kop'
V[op&(NY<=26)&(NX>=41)&(NX<=52)&(hd>1.0)]='punt'
V[op&(NY>=56)&(NX>=30)&(NX<=68)]='lijf'
V[op&(NY>=49)&((NX<=29)|(NX>=75))&(hd>1.0)]='staf'
V[op&(NY>=51)&(NX>=68)&(NX<=85)&(hd>1.0)&~((NX<=75)&(NY<=55))]='staf'
V[op&(NY>=56)&(NX>=66)]='staf'
V[op&(np.minimum(d1,d2)>0.95)&(np.minimum(d1,d2)<=1.5)&(hd<1.0)&(NY>=33)]='ring'
V[op&(NX>=38+SCHUIF)&(NX<=44+SCHUIF)&(NY>=33)&(NY<=51)]='neus'
V[op&((d1<0.95)|(d2<0.95))]='oog'
KR={'K1':(38.5,17.5,34,41,13,23,'.'),'K2':(30.5,22.5,26,36,18,28,'-'),'K3':(22.5,31.5,17,28,26,37,'.'),'K4':(20.5,40.5,15,25,35,46,'-'),
    'K5':(26.0,50.0,23,30,46,56,'.'),'R1':(58.5,17.5,53,63,12,23,'.'),'R2':(66.5,22.5,61,73,17,28,'-'),'R3':(75.5,31.5,69,82,25,37,'.'),
    'R4':(76.5,40.5,70,83,35,47,'-'),'R5':(71.0,50.0,65,75,45,55,'.')}
for n,(cx,cy,x0,x1,y0,y1,t) in KR.items():
    m=op&(NX>=x0)&(NX<=x1)&(NY>=y0)&(NY<=y1)&(hd>1.0)&(np.hypot(NX-cx,NY-cy)<=5.2)&(V!='punt')
    V[m]='krans_'+n
# ---- 1) tintvlakken ----
STAF=[4,5,6,7,9]   # staven: dun (2-3 px), niet gladstrijken; alleen vlakjes < 3 px
TOON={'kop':[4,5,6,7,8,9],'punt':[4,5,6,7,8],'lijf':[4,5,6,7,8,9],'ring':[5,6,7,9],'neus':[5,6,7,8],'oog':[2,3,4]}
vast=(S==10)|(S>=11)
lijnig=np.zeros((64,64),bool)          # streepjes/stipjes/oogomlijning/neuslijnen: donkere pixel die als lijn in het model staat
for y in range(64):
    for x in range(64):
        if S[y,x] in (9,10) and V[y,x] in ('oog','ring','neus'): lijnig[y,x]=True
        if S[y,x]==9 and V[y,x] in ('kop','lijf','staf','punt') and not(V[y,x]=='kop' and NY[y,x]>52):  # binnenlijn (niet de schaduwband onder de kop)
            b=[S[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<64 and 0<=x+dx<64]
            if sum(v in (9,10) for v in b)<=2 and sum(v in (4,5,6) for v in b)>=2: lijnig[y,x]=True
# lijnen op contrast (lijfpatroon, kopreliëf): modelpixel >= 28 donkerder dan zijn omgeving en dun
for y in range(64):
    for x in range(64):
        if S[y,x]==0 or V[y,x] in ('','staf') or V[y,x].startswith('krans') or S[y,x]>=10: continue
        y0,y1,x0,x1=max(0,y-2),min(64,y+3),max(0,x-2),min(64,x+3); w=(S[y0:y1,x0:x1]>0)&(S[y0:y1,x0:x1]<10)
        omg=np.median(LM[y0:y1,x0:x1][w])
        if LM[y,x]<=omg-28:
            b=[LM[y+dy,x+dx]<=omg-28 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<64 and 0<=x+dx<64]
            if sum(b)<=2: lijnig[y,x]=True
vast|=lijnig
g=np.exp(-0.5*(np.arange(-3,4)/1.1)**2); G2=np.outer(g,g)
T=S.copy()
for reg,tonen in TOON.items():
    m=(V==reg)&~vast
    for y,x in zip(*np.where(m)):
        y0,y1,x0,x1=max(0,y-3),min(64,y+4),max(0,x-3),min(64,x+4)
        w=G2[y0-y+3:y1-y+3,x0-x+3:x1-x+3]*m[y0:y1,x0:x1]
        l=(LM[y0:y1,x0:x1]*w).sum()/w.sum()
        v=tonen[int(np.argmin([abs(PL[t]-l) for t in tonen]))]
        if v!=S[y,x]: T[y,x]=v; tel('tintvlak',y,x,S[y,x],v)
S=T
# kleine tintvlakjes (<3 px) oplossen in de meest voorkomende buurtint van hetzelfde vlak
for ronde in range(3):
    T=S.copy(); seen=np.zeros((64,64),bool)
    for y in range(64):
        for x in range(64):
            if seen[y,x] or S[y,x]==0 or vast[y,x] or V[y,x].startswith('krans'): continue
            v=S[y,x]; comp=[]; st=[(y,x)]
            while st:
                a,b=st.pop()
                if 0<=a<64 and 0<=b<64 and not seen[a,b] and S[a,b]==v and not vast[a,b] and V[a,b]==V[y,x]:
                    seen[a,b]=True; comp.append((a,b)); st+=[(a+1,b),(a-1,b),(a,b+1),(a,b-1)]
            if len(comp)>=3: continue
            nb=[S[a+dy,b+dx] for a,b in comp for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=a+dy<64 and 0<=b+dx<64
                and (a+dy,b+dx) not in comp and S[a+dy,b+dx] in (TOON.get(V[y,x]) or (STAF if V[y,x]=='staf' else [])) and V[a+dy,b+dx]==V[y,x]]
            if nb:
                vals,c=np.unique(nb,return_counts=True); nv=vals[c.argmax()]
                for a,b in comp: T[a,b]=nv; tel('vlakje<3',a,b,v,nv)
    S=T
np.save('claydol_sprite_r2/na_tint.npy',S)
# ---- 2) krans-assets ----
from kopmasker import kopmasker
kn,_=klasse('claydol_sprite_r2/model_r2_s%d.png'%SCHUIF); KOPN=kopmasker(kn)
KOP=np.zeros((64,64),bool); ok=NY>=0; KOP[ok]=KOPN[NY[ok],NX[ok]]
HDN=((NX-48.5)/24.0)**2+((NY-39.75)/16.5)**2
k5,_=klasse('claydol_model/natief_r5.png'); k6,_=klasse('claydol_model/natief_r6.png')
def asset(kk):
    # (omlijning gesloten: elke rechte buur van de vulling wordt zwart; boven de top '678' had het model geen lijn = technische buitenlijn)
    # R4-bolletje (natief x72-82, y35-44), het rondste bolletje van het model: vulling = vloedvulling vanaf het midden over niet-zwart,
    # omlijning = de zwarte modelpixels die recht tegen die vulling liggen
    # (diagonaal erbij gaf linksboven een dubbele lijn: daar lag de kopomlijning van het model).
    b=kk[35:45,72:83].copy(); keep=np.zeros_like(b,bool); st=[(5,5)]
    while st:
        y,x=st.pop()
        if 0<=y<b.shape[0] and 0<=x<b.shape[1] and not keep[y,x] and b[y,x] not in (0,10):
            keep[y,x]=True; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    # 10x10 natief is 12% groter dan de rest van de sprite (die is geschrapt): ook het bolletje 1 rij en 1 kolom schrappen, door het
    # rechte stuk (vulling-rij 4 en -kolom 7 van het blok), zodat de bolletjes net als in het model los van elkaar blijven.
    ys,xs=np.where(keep); r_=ys.min()+3; c_=xs.min()+6
    b=np.delete(np.delete(b,[r_],0),[c_],1); keep=np.delete(np.delete(keep,[r_],0),[c_],1)
    b=np.pad(b,1); keep=np.pad(keep,1)
    rand=np.zeros_like(keep)
    for y,x in zip(*np.where(keep)):
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            if not keep[y+dy,x+dx]: rand[y+dy,x+dx]=True
    b[rand]=10; b[~(keep|rand)]=0; ys,xs=np.where(b>0); return b[ys.min():ys.max()+1,xs.min():xs.max()+1]
def belicht(b):
    # herbelichten (voorstel Claude, alleen kleur, vorm blijft): licht linksboven, basis 3, hooglicht 2, sikkel 5 rechtsonder (3 tinten);
    # stip/streep (9) blijven. Het model-bolletje lag rechts van de kop en was van links donker (9 linksboven).
    f=(b>0)&(b!=10); ys,xs=np.where(f); cy,cx=ys.mean(),xs.mean(); r=np.hypot(ys-cy,xs-cx).max()+0.5
    o=b.copy()
    for y,x in zip(ys,xs):
        dx,dy=(x-cx)/r,(y-cy)/r; u=-(dx+dy)/1.414; d=np.hypot(dx,dy)
        if b[y,x]==9 and all(b[y+a,x+c] not in (0,10) for a,c in ((-1,0),(1,0),(0,-1),(0,1))): continue   # stip/streep
        if u<-0.20 and d>0.50: t=5
        elif u>0.18 and 0.12<d<0.5: t=2
        else: t=3
        o[y,x]=t
    return o
AST={'.':belicht(asset(k6)),'-':belicht(asset(k5))}
np.save('claydol_sprite_r2/asset_stip.npy',AST['.']); np.save('claydol_sprite_r2/asset_streep.npy',AST['-'])
def sp(cx,cy):                       # natieve coördinaat -> spritecoördinaat (via de bewaarde rijen/kolommen)
    sx=np.interp(cx,NX[NY>=0].ravel()[np.argsort(NX[NY>=0].ravel())],np.where(NY>=0)[1][np.argsort(NX[NY>=0].ravel())])
    sy=np.interp(cy,NY[NY>=0].ravel()[np.argsort(NY[NY>=0].ravel())],np.where(NY>=0)[0][np.argsort(NY[NY>=0].ravel())])
    return sx,sy
oud=S.copy(); vrij=np.zeros((64,64),bool)
for n,(cx,cy,x0,x1,y0,y1,t) in KR.items():
    m=(S>0)&~KOP&(np.hypot(NX-cx,NY-cy)<=6.2)&(V!="punt")&(V!="staf")
    S[m]=0; vrij|=m
for n,(cx,cy,x0,x1,y0,y1,t) in KR.items():
    a=AST[t]; h,w=a.shape; sx,sy=sp(cx,cy); oy=int(round(sy-(h-1)/2)); ox=int(round(sx-(w-1)/2))
    for j in range(h):
        for i in range(w):
            y,x=oy+j,ox+i
            if a[j,i]==0 or not(0<=y<64 and 0<=x<64): continue
            if KOP[y,x] or V[y,x] in ('punt',) or (S[y,x]>0 and not vrij[y,x] and V[y,x]=='staf'): continue   # achter kop, punt en staf
            S[y,x]=a[j,i]; vrij[y,x]=True       # volgorde K1..K5, R1..R5: een later bolletje ligt over het vorige, met zijn eigen lijn
    log.setdefault('krans_plek',[]).append((n,oy,ox))
# vrijgemaakte pixels die geen asset kregen maar bij de kop horen (binnen de kopellips of buiten de oude bolletjes): terug
terug=(S==0)&(oud>0)&((HDN<1.12)|((V=='kop')&(HDN<1.3)))
S[terug]=oud[terug]; log['kop terug']=list(zip(*np.where(terug)))
np.save('claydol_sprite_r2/na_krans.npy',S)
# ---- 3) staven 1 px naar binnen (Claude: 1 px vrij aan beide kanten) ----
for kant,dx in (('L',1),('R',-1)):
    m=(V=='staf')&(S>0)&((NX<=40) if kant=='L' else (NX>=56))
    T=S.copy(); ys,xs=np.where(m)
    for y,x in zip(ys,xs): T[y,x]=0
    for y,x in zip(ys,xs):
        if T[y,x+dx]==0 or (V[y,x+dx]=='staf'): T[y,x+dx]=S[y,x]
    S=T
# ---- keurder: losse lichtroze (12) in een rode band/haak -> 13 ----
for y,x in zip(*np.where(S==12)):
    b=[S[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<64 and 0<=x+dx<64]
    if 12 not in b: S[y,x]=13; tel('roze->13',y,x,12,13)
# ---- gaatjes van 1 px tussen bolletjes en kop (transparant met >=3 dichte buren) -> omlijning ----
for y in range(1,63):
    for x in range(1,63):
        if S[y,x]==0 and sum(S[y+a,x+c]>0 for a,c in ((-1,0),(1,0),(0,-1),(0,1)))>=3: S[y,x]=10; tel('gaatje dicht',y,x,0,10)
# ---- 4) buitenlijn + selout ----
G={2:'L',3:'L',4:'L',5:'M',6:'M',7:'M',8:'D',9:'D',10:'K',11:'R',12:'R',13:'R'}
T=S.copy()
for y in range(64):
    for x in range(64):
        v=S[y,x]
        if v==0: continue
        rand=[(dy,dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if not(0<=y+dy<64 and 0<=x+dx<64) or S[y+dy,x+dx]==0]
        if not rand: continue
        bl=all(d in ((-1,0),(0,-1)) for d in rand)
        doel=13 if G[v]=='R' else (7 if bl else 10)
        if bl and v in (6,7,8,9): continue
        if v!=doel: T[y,x]=doel; tel('buitenlijn',y,x,v,doel)
S=T
SUF='' if SCHUIF==2 else '_s%d'%SCHUIF
np.save('claydol_sprite_r2/sprite%s.npy'%SUF,S); np.save('claydol_sprite_r2/vlakken%s.npy'%SUF,V); np.save('claydol_sprite_r2/kaal%s.npy'%SUF,KAAL)
im=Image.fromarray(S.astype('uint8'),'P'); pal=[c for p in PAL for c in p]; pal+=[0]*(48-len(pal)); im.putpalette(pal)
im.save('claydol_sprite_r2/claydol_r2%s.png'%SUF,transparency=0)
for n,l in log.items(): print(n,len(l))
ys,xs=np.where(S>0); print('bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'kleuren',sorted(set(S.ravel())))
