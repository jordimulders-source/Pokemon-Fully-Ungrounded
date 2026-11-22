# Pinsir-evolutie r6: pitahaya fase 3 / spooktrein-methode. Geen opgelapte celreductie meer, maar:
# 1. SEGMENTEREN op modelresolutie: de zwarte modellijnen (L < 22) verdelen het model in vlakken; vlakken >= 600 modelpx zijn
#    onderdelen/platen (37 stuks, met de hand benoemd in VLAKKEN), kleinere snippers en de lijnen zelf gaan naar het
#    dichtstbijzijnde grote vlak. Elke spritepixel krijgt het vlak met de meeste niet-lijnpixels in het midden van zijn cel.
# 2. LIJNEN: alleen grenzen tussen twee vlakken die in de sprite >= 3 px lang zijn (= modellijn >= ±45 modelpx) worden een
#    binnenlijn: doorlopend, 1 px, aan de kant van het vlak dat ACHTER ligt (DIEPTE; bij gelijke diepte de kant met de
#    meeste modellijn), zodat smalle voorste delen (arm) hun vulling houden; ellebogen weg. Kleur: de donkere gekleurde
#    lijntint van het onderdeel (selout), geen zwart. Korte lijnstukjes en textuurlijntjes vervallen.
#    Buitenrand: zwart aan de schaduwkant (achtergrond rechts/onder), lijntint van het onderdeel aan de lichtkant
#    (achtergrond alleen links/boven).
# 3. VULLING per vlak: basistint uit de mediane modeltoon van het vlak (toonvolgorde = model; < 45 schaduw, < 72 midden,
#    anders licht), daarbinnen de gladgestreken modeltoon met drempels op de eigen verdeling (-1 / +1 / glans +2); waar het
#    model vlak is: rand rechtsonder -1, linksboven +1. Verre ledematen -1, nabije arm/been +1. Tintvlekjes < 3 px weg.
#    Dekschild: modeltekening (vlek/midden/licht) per cel, met dezelfde licht/schaduwregel.
# 4. BEVROREN uit r5: oog A (x14-25, y26-28), mond (x16-22, y28-35), kaken (alle kaakpixels + hun zwarte omlijning) en
#    het silhouet (diff 0 met r5).
# Bouwen: cd pinsir_evo && python3 sprite_r6/bouw.py [raster]
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from model import klassen
from PIL import Image; from scipy import ndimage
UIT='sprite_r6'
PROEF=False
MODUS='model+rand'   # licht/schaduw uit de modeltoon binnen het vlak; waar het model vlak is: sikkel rechtsonder / licht linksboven
R5=np.asarray(Image.open('sprite_r5/pinsir_evo_r5.png')).astype(int)
H=W=64; yy,xx=np.mgrid[:H,:W]
PAL=[(120,200,160),(18,14,14),
     (46,36,32),                                            # 2 lijf lijn (selout)                38
     (78,64,54),(116,98,80),(158,136,108),(204,182,148),    # 3-6 lijf schaduw 65, midden 98, licht 134, glans 178
     (72,28,22),(118,52,38),(162,84,58),(206,130,94),       # 7-10 kaak (r5, bevroren)
     (66,36,18),(104,62,30),(156,110,66),(210,166,110),     # 11-14 dekschild lijn, vlek, midden, licht
     (236,222,206)]                                         # 15 oog/tand crème
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def nb(arr,Y,X,nbs=N4,fill=0):
    return [arr[Y+dy,X+dx] if 0<=Y+dy<H and 0<=X+dx<W else fill for dy,dx in nbs]
SIL=R5>0
# ---------- bevroren ----------
OOG=(xx>=14)&(xx<=25)&(yy>=26)&(yy<=28); MOND=(xx>=16)&(xx<=22)&(yy>=28)&(yy<=35)
KAAK=np.isin(R5,[7,8,9,10])
KAAKRAND=np.zeros_like(KAAK)
for Y,X in zip(*np.where(R5==1)):
    n8=nb(R5,Y,X,N8)
    if any(v in (7,8,9,10) for v in n8) and (0 in n8 or X<=13): KAAKRAND[Y,X]=True
VAST=OOG|MOND|KAAK|KAAKRAND
# ---------- 1. segmentatie op modelresolutie ----------
a,c,fg=klassen(); L=a.mean(2)
LIJN=fg&(L<22)
lab,n=ndimage.label(fg&~LIJN)
sz=ndimage.sum(np.ones_like(L),lab,range(n+1)); sz[0]=0
groot=sz>=600; groot[0]=False
idx=ndimage.distance_transform_edt(~groot[lab],return_indices=True)[1]
LAB=lab[idx[0],idx[1]]*fg                                # elke modelpixel -> dichtstbijzijnd groot vlak
# vlak -> (onderdeel, diepte); hogere diepte = meer vooraan. Ids met de hand uit het genummerde model (L<22, >= 600 px).
VLAKKEN={12:('kopschild',9),1:('rug',4),2:('rug',4),7:('rug',4),24:('rug',4),39:('rug',4),
         46:('kop',10),
         50:('romp',5),55:('romp',5),60:('romp',5),92:('romp',5),99:('romp',5),179:('romp',5),
         69:('arm',8),87:('arm',8),135:('arm',8),247:('arm',8),275:('arm',8),297:('arm',8),
         159:('been',7),237:('been',7),300:('been',7),114:('been',7),
         35:('schild',7.5),
         185:('been_ver',5.5),217:('been_ver',5.5),243:('been_ver',5.5),
         100:('arm_ver',5.6),107:('arm_ver',5.6),221:('arm_ver',5.6),252:('arm_ver',5.6),
         193:('staart',3),209:('staart',3),206:('staart',3),213:('staart',3),166:('staart',3),169:('staart',3)}
grote=set(np.where(groot)[0]); assert grote==set(VLAKKEN),(sorted(grote-set(VLAKKEN)),sorted(set(VLAKKEN)-grote))
MED={v:float(np.median(L[(lab==v)])) for v in VLAKKEN}
# dunne nekplaatjes (60 grijze strook, ±3 spritepx breed) samen met de nekkraag 55: anders worden het 1-px strepen tussen twee
# lijnen (strepenpatroon); de lange modellijn tussen kraag en borst (55|50) en kaak blijft
ALIAS={60:55}
for k,v in ALIAS.items(): LAB[LAB==k]=v
SCHILDM=np.isin(c,(9,10,11)); VLEK=c==9
CEL=974/64; MX0,MY0=31,134; DY=13
def cel(X,Y,k=0.0):
    ya,yb=MY0+(Y-DY)*CEL,MY0+(Y-DY+1)*CEL; xa,xb=MX0+X*CEL,MX0+(X+1)*CEL
    ya,yb,xa,xb=ya+k*CEL,yb-k*CEL,xa+k*CEL,xb-k*CEL
    return slice(max(int(round(ya)),0),max(int(round(yb)),0)),slice(max(int(round(xa)),0),max(int(round(xb)),0))
SL=np.zeros((H,W),int); MT=np.full((H,W),np.nan); ZW=np.zeros((H,W)); VL=np.zeros((H,W))
for Y in range(H):
    for X in range(W):
        s=cel(X,Y); f=fg[s]; li=LIJN[s]
        if f.size==0: continue
        ZW[Y,X]=li.mean()
        sm=cel(X,Y,0.2); l=LAB[sm]; k=l[fg[sm]&~LIJN[sm]]          # midden van de cel: smalle delen blijven
        if k.size==0: k=LAB[s][f&~li]
        if k.size==0: k=LAB[s][f]
        if k.size: SL[Y,X]=np.bincount(k).argmax()
        if (f&~li).sum()>=6: MT[Y,X]=L[s][f&~li].mean()
        ms=f&SCHILDM[s]
        VL[Y,X]=VLEK[s][ms].mean() if ms.any() else 0
m=(SL>0)&SIL
ii=ndimage.distance_transform_edt(~m,return_indices=True)[1]
SL=np.where(SIL,SL[ii[0],ii[1]],0)
DEEL=np.vectorize(lambda v: VLAKKEN[v][0] if v in VLAKKEN else '')(SL)
DIEP=np.vectorize(lambda v: VLAKKEN[v][1] if v in VLAKKEN else 0)(SL)
MATR=np.where(DEEL=='schild','schild','lijf')
VER=np.isin(DEEL,['arm_ver','been_ver'])
GROOTTE={v:int((SL==v).sum()) for v in np.unique(SL)}
# ---------- 2. binnenlijnen ----------
paren={}
for Y,X in zip(*np.where(SIL)):
    for dy,dx in ((0,1),(1,0)):
        Y2,X2=Y+dy,X+dx
        if Y2<H and X2<W and SIL[Y2,X2] and SL[Y2,X2]!=SL[Y,X]:
            k=tuple(sorted((SL[Y,X],SL[Y2,X2]))); paren.setdefault(k,[]).append(((Y,X),(Y2,X2)))
lijn=np.zeros((H,W),bool); nlijnen=0
for (A,B),ps in paren.items():
    if len(ps)<3: continue                                     # korte modellijn: vervalt
    dA,dB=VLAKKEN.get(A,(0,0))[1],VLAKKEN.get(B,(0,0))[1]
    if dA!=dB: kant=A if dA<dB else B                          # lijn in het vlak dat achter ligt
    else:
        za=sum(ZW[p if SL[p]==A else q] for p,q in ps); zb=sum(ZW[q if SL[q]==B else p] for p,q in ps)
        kant=A if za>=zb else B
    for p,q in ps: lijn[p if SL[p]==kant else q]=True
    nlijnen+=1
for _ in range(2):                                             # ellebogen weg (L-hoek zonder derde buur)
    for Y,X in zip(*np.where(lijn)):
        u,d,l_,r=[lijn[Y+dy,X+dx] if 0<=Y+dy<H and 0<=X+dx<W else False for dy,dx in N4]
        if u+d+l_+r!=2 or (u and d) or (l_ and r): continue
        if sum(lijn[Y+dy,X+dx] for dy,dx in N8 if 0<=Y+dy<H and 0<=X+dx<W)==2: lijn[Y,X]=False
# 2b. lange modellijnen BINNEN een vlak (buiksegmenten, schoudernaad): skelet van de modellijn op >= 5 modelpx van een
#     ander vlak, componenten >= 80 modelpx (kortere: dijstrepen, textuur), geprojecteerd op de sprite; alleen stukken van >= 3 spritepx blijven.
from skimage.morphology import skeletonize
grens=np.zeros(L.shape,bool)
grens[:,1:]|=LAB[:,1:]!=LAB[:,:-1]; grens[1:,:]|=LAB[1:,:]!=LAB[:-1,:]
dgr=ndimage.distance_transform_edt(~grens)
sk=skeletonize(LIJN)&(dgr>=5)
lb,nn=ndimage.label(sk,structure=np.ones((3,3)))
szs=ndimage.sum(sk,lb,range(nn+1))
skl=np.isin(lb,np.where(szs>=80)[0])&(lb>0)
cnt=np.zeros((H,W))
for my,mx in zip(*np.where(skl)):
    X=int((mx-MX0)//CEL); Y=int((my-MY0)//CEL+DY)
    if 0<=X<W and 0<=Y<H: cnt[Y,X]+=1
intl=(cnt>=8)&SIL&(MATR!='schild')&(DEEL!='kop')                           # lijn loopt echt door de cel; schildtekening = textuur, geen lijn
lb2,n2=ndimage.label(intl,structure=np.ones((3,3)))
for i in range(1,n2+1):
    if (lb2==i).sum()<3: intl[lb2==i]=False
intl&=~lijn
lijn|=intl
# grens lijf | bevroren kaak: in het model een zwarte omlijning om de kaak; hier de lijntint aan de lijfkant (geen zwart)
for Y,X in zip(*np.where(SIL&~VAST)):
    if any(KAAK[Y+dy,X+dx] for dy,dx in N4 if 0<=Y+dy<H and 0<=X+dx<W): lijn[Y,X]=True
# lijnklonten (2-3 px dik waar twee grenzen of een grens en een binnenlijn tegen elkaar liggen) uitdunnen tot 1 px
from skimage.morphology import thin
lijn=thin(lijn)
# ---------- 3. vulling ----------
def zelfde(Y,X,dy,dx):
    Y2,X2=Y+dy,X+dx
    return 0<=Y2<H and 0<=X2<W and SIL[Y2,X2] and SL[Y2,X2]==SL[Y,X] and not lijn[Y2,X2]
# modeltoon binnen elk vlak gladstrijken (zonder lijnpixels), daarna per vlak drempels op de eigen toonverdeling
ZONE=SIL&~lijn
mt=MT.copy()
for v in np.unique(SL[SIL]):
    mm=(SL==v)&ZONE; mt[mm&~np.isfinite(mt)]=MED.get(v,40)
for _ in range(2):
    nm=mt.copy()
    for Y,X in zip(*np.where(ZONE)):
        vals=[mt[Y,X]]*2+[mt[Y+dy,X+dx] for dy,dx in N8 if 0<=Y+dy<H and 0<=X+dx<W and ZONE[Y+dy,X+dx] and SL[Y+dy,X+dx]==SL[Y,X]]
        nm[Y,X]=np.mean(vals)
    mt=nm
OFF=np.zeros((H,W),int)
for v in np.unique(SL[SIL]):
    mm=(SL==v)&ZONE
    if mm.sum()<10: continue
    q1,q2,q9=np.percentile(mt[mm],[33,75,92]); md=MED.get(v,40)
    OFF[mm&(mt<min(q1,md-6))]=-1; OFF[mm&(mt>=max(q2,md+10))]=1     # alleen waar het model echt lichter/donkerder is
    OFF[mm&(mt>=max(q9,105))]=2                                      # modelglans
o=np.zeros((H,W),int)
for Y,X in zip(*np.where(SIL)):
    v=SL[Y,X]; med=MED.get(v,40); t=MT[Y,X] if np.isfinite(MT[Y,X]) else med
    ul=not zelfde(Y,X,-1,-1) or (not zelfde(Y,X,-1,0) and not zelfde(Y,X,0,-1))
    lr=not zelfde(Y,X,1,1) or (not zelfde(Y,X,1,0) and not zelfde(Y,X,0,1))
    opp=GROOTTE[v]
    if MATR[Y,X]=='schild':
        b=1 if t<70 else 2 if t<118 else 3                     # vlek / midden / licht (modeltekening per cel)
        if VL[Y,X]>0.38: b=1
    else:
        b=0 if med<45 else 1 if med<72 else 2                  # basistint per vlak uit de modelmediaan
        if MODUS=='rand':
            if t>=med+22: b+=1                                  # modelglans binnen het vlak
        else:
            b+=OFF[Y,X]                                         # licht/schaduw zoals het model binnen het vlak
    if MODUS=='rand' or (MODUS=='model+rand' and OFF[Y,X]==0 and MATR[Y,X]=='lijf'):
        if lr and opp>=12: b-=1                                 # schaduwsikkel rechtsonder
        elif ul and opp>=20: b+=1                               # licht linksboven
    if VER[Y,X]: b-=1
    if DEEL[Y,X] in ('arm','been') and med>=45: b+=1           # nabije ledematen een stap lichter dan de romp (model: lichtere platen)
    if MATR[Y,X]=='schild': o[Y,X]=12+min(max(b-1,0),2)
    else: o[Y,X]=3+min(max(b,0),3)
LIJNT={'lijf':2,'schild':11}
for Y,X in zip(*np.where(lijn)): o[Y,X]=LIJNT[MATR[Y,X]]
# ---------- buitenrand ----------
P=np.pad(SIL,1)
for Y,X in zip(*np.where(SIL)):
    u,d,l_,r=[not P[Y+1+dy,X+1+dx] for dy,dx in N4]
    if not (u or d or l_ or r): continue
    o[Y,X]=1                                                    # buitenrand zwart (model: zwarte omlijning rondom)
# ---------- bevroren delen terug ----------
o[VAST]=R5[VAST]
# ---------- opruimen: tintvlekjes < 3 px ----------
def opruimen(o,groep,minpx=3):
    for _ in range(6):
        ch=0
        for k in groep:
            lb,nn=ndimage.label(o==k)
            for i in range(1,nn+1):
                pts=np.argwhere(lb==i)
                if len(pts)>=minpx or any(VAST[Y,X] for Y,X in pts): continue
                bb={}
                for Y,X in pts:
                    for v in nb(o,Y,X):
                        if v in groep and v!=k: bb[v]=bb.get(v,0)+1
                if bb:
                    nv=max(bb,key=bb.get)
                    for Y,X in pts: o[Y,X]=nv
                    ch+=1
        if not ch: break
    return o
o=opruimen(o,[3,4,5,6]); o=opruimen(o,[12,13,14])
# ingesloten restjes (8-samenhangend < 3 px, geen vulbuur in 4 richtingen): tint van de meeste vulburen schuin ernaast,
# anders de meeste vultint binnen 2 px (geen lijnklonten)
for _ in range(2):
    for grp,lt in (([3,4,5,6],2),([12,13,14],11)):
        for k in grp:
            lb,nn=ndimage.label(o==k,structure=np.ones((3,3)))
            for i in range(1,nn+1):
                pts=np.argwhere(lb==i)
                if len(pts)>=3 or any(VAST[Y,X] for Y,X in pts): continue
                bb={}
                for Y,X in pts:
                    for v in nb(o,Y,X,N8):
                        if v in grp and v!=k: bb[v]=bb.get(v,0)+1
                if not bb:                                       # binnen 2 px zoeken; geen lijnklont maken
                    for Y,X in pts:
                        for dy in range(-2,3):
                            for dx in range(-2,3):
                                if 0<=Y+dy<H and 0<=X+dx<W and o[Y+dy,X+dx] in grp and o[Y+dy,X+dx]!=k and lb[Y+dy,X+dx]!=i:
                                    bb[o[Y+dy,X+dx]]=bb.get(o[Y+dy,X+dx],0)+1
                if not bb: continue
                nv=max(bb,key=bb.get)
                for Y,X in pts: o[Y,X]=nv
# ---------- handwerk (alleen benoemde reparaties, met assert op de oude waarde) ----------
HAND=[]
for Y,X,oud,nieuw in HAND:
    assert o[Y,X]==oud,(Y,X,o[Y,X],oud); o[Y,X]=nieuw
# ---------- opslaan + controles ----------
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for cc in PAL for v in cc]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
opslaan(o,UIT+'/pinsir_evo_r6.png')
def binnenzwart(q):
    P=np.pad(q,1); return int(sum(1 for Y,X in zip(*np.where(q==1)) if all(P[Y+1+dy,X+1+dx]>0 for dy,dx in N8)))
def vlekjes(q,ks,st=None):
    t=0
    for k in ks:
        lb,nn=ndimage.label(q==k,structure=st); t+=sum(1 for i in range(1,nn+1) if (lb==i).sum()<3)
    return t
FILL=[3,4,5,6,8,9,10,12,13,14]
print('silhouet-diff met r5:',int(((o>0)!=SIL).sum()),'| bevroren diff:',int((o[VAST]!=R5[VAST]).sum()),'| kleuren incl. transp.:',len(set(o.ravel())))
print('zwart %.1f%% (r5 %.1f%%) | zwarte binnenpixels (8 buren in de figuur): r6 %d, r5 %d'%(100*(o==1).sum()/SIL.sum(),100*(R5==1).sum()/SIL.sum(),binnenzwart(o),binnenzwart(R5)))
print('tintvlekjes < 3 px (vulling, 4-samenhang): r6 %d, r5 %d | 8-samenhang: r6 %d, r5 %d | binnenlijnen: %d grenzen, %d px'%(vlekjes(o,FILL),vlekjes(R5,FILL),vlekjes(o,FILL,np.ones((3,3))),vlekjes(R5,FILL,np.ones((3,3))),nlijnen,int(lijn.sum())))
for nm,g in (('lijf',[2,3,4,5,6]),('kaak',[7,8,9,10]),('schild',[11,12,13,14])):
    print('%-6s'%nm,[(k,round(sum(PAL[k])/3),int((o==k).sum())) for k in g])
if 'raster' in sys.argv:
    CH='.KL2345pqrsuvwxT'
    print('   '+''.join(str(x%10) for x in range(64)))
    for Y in range(12,62): print('%2d '%Y+''.join(CH[v] for v in o[Y]))
if 'detail' in sys.argv:
    P8=np.pad(o,1)
    bz=[(X,Y) for Y,X in zip(*np.where(o==1)) if all(P8[Y+1+dy,X+1+dx]>0 for dy,dx in N8)]
    print('zwarte binnenpixels buiten bevroren:',[p for p in bz if not VAST[p[1],p[0]]])
    for k in FILL:
        lb,nn=ndimage.label(o==k)
        for i in range(1,nn+1):
            pts=np.argwhere(lb==i)
            if len(pts)<3: print(' vlekje tint',k,[(int(x),int(y)) for y,x in pts],'bevroren' if any(VAST[y,x] for y,x in pts) else '')
# ---------- vel: r6 | r5 | model op 8x; segmentkaart; 1x naast Gen 3 op wit en donker ----------
if not PROEF:
    from PIL import ImageDraw
    sys.path.insert(0,'gereedschap'); from vel import rgbp, model_op_schaal
    def gen3(sp,bg):
        im=Image.open(f'../../../../graphics/pokemon/{sp}/anim_front.png'); q=np.asarray(im)[:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
        img=np.zeros((64,64,3),'uint8'); img[:]=bg
        for k in range(1,16): img[q==k]=pal[k]
        return Image.fromarray(img)
    rng=np.random.RandomState(3); kl=rng.randint(80,250,(SL.max()+1,3)); kl[0]=255
    seg=kl[SL].astype('uint8'); seg[np.isin(o,[1])]=(0,0,0); seg[np.isin(o,[2,11])]=(90,90,90)
    seg=Image.fromarray(seg).resize((512,512),Image.NEAREST); d=ImageDraw.Draw(seg)
    for dl in sorted(set(DEEL[SIL])):
        if not dl: continue
        Yp,Xp=np.where(DEEL==dl); d.text((Xp.mean()*8-12,Yp.mean()*8-5),dl,fill=(0,0,0))
    v=Image.new('RGB',(4*520,14+512+24+150),'white'); d=ImageDraw.Draw(v)
    for i,(nm,im) in enumerate((('r6',rgbp(UIT+'/pinsir_evo_r6.png')),('r5',rgbp('sprite_r5/pinsir_evo_r5.png')),('model',model_op_schaal()))):
        v.paste(im.resize((512,512),Image.NEAREST),(i*520,14)); d.text((i*520+2,0),nm+' 8x',fill=(0,0,0))
    v.paste(seg,(3*520,14)); d.text((3*520+2,0),'segmentkaart r6 (vlakken uit de modellijnen; zwart = buitenrand, grijs = binnenlijn)',fill=(0,0,0))
    y=14+512+24
    refs=('pinsir','heracross','tyranitar','aggron')
    for j,bg in enumerate(((255,255,255),(40,48,56))):
        for i,im in enumerate([rgbp(UIT+'/pinsir_evo_r6.png',bg),rgbp('sprite_r5/pinsir_evo_r5.png',bg)]+[gen3(sp,bg) for sp in refs]):
            v.paste(im,(i*70,y+j*70))
        for i,im in enumerate([rgbp(UIT+'/pinsir_evo_r6.png',bg),rgbp('sprite_r5/pinsir_evo_r5.png',bg)]+[gen3(sp,bg) for sp in refs]):
            v.paste(im.resize((128,128),Image.NEAREST),(470+i*132,y-10+j*0)) if j==0 else None
    d.text((2,y-14),'1x: r6 | r5 | Gen 3 Pinsir, Heracross, Tyranitar, Aggron (wit / donker)          2x op wit:',fill=(0,0,0))
    v.save(UIT+'/vel.png'); print('vel',v.size)
