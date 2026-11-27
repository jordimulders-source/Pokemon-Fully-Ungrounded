# Ronde 6 = r2 precies zoals hij is (palet, stenen, gezicht, vacht) + alleen Jordi's vijf punten, elk gemeten op het
# natieve modelraster (natief.png, pitch 5,867; spritepixel = floor((cel+0,5-MX0)/F), zoals r1/r2).
# Gebruik vanuit sneeuwmonster_fase3: python3 sprite_r6/bouw.py [log]
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *; from gemeen import label; from klassen import klassen
r2=np.asarray(Image.open('sprite_r2/sauna_yeti_r2.png')).astype(int); o=r2.copy(); log=[]
def zet(X,Y,t,why):
    if o[Y,X]!=t: log.append((X,Y,CH[o[Y,X]]+'>'+CH[t],why)); o[Y,X]=t
a,c,Lk=klassen(); A=a.astype(float); L=A.mean(2)
idx=spriteindex(); ok=idx>=0; I=idx[ok]; n=np.maximum(np.bincount(I,minlength=4096),1)
def frac(m): return (np.bincount(I,up(m)[ok].astype(float),minlength=4096)/n).reshape(64,64)
def cellen(X,Y):
    xs=[x for x in range(240) if int(np.floor((x+0.5-MX0)/F))==X]; ys=[y for y in range(130) if int(np.floor((y+0.5-MY0)/F))==Y]
    return [(y,x) for y in ys for x in xs]
P=np.array(PAL,float)
def near(col,keus): return min(keus,key=lambda k:((P[k]-col)**2).sum())
def sneeuwtint(X,Y):   # mediaan van de lichte sneeuwcellen (geen lijncellen) -> s/m/h/w
    cs=[q for q in cellen(X,Y) if c[q]==2 and L[q]>=140]; return near(np.median([A[q] for q in cs],0),[3,4,5,6])
cov=1-frac(c==0)
ZONES={1:(29,41,11,12),2:(43,47,32,49),3:(16,30,54,56),4:(24,32,34,41),5:(27,41,15,19)}   # x0,x1,y0,y1 (incl.)

# 1. EMMERBOVENRAND (rij 11-12, X29-41): modeldekking rij 11 X32-35 = 44 % (bovenkant emmer = 11,56), rij 12 X29 57 %,
#    X38 88 %, X39 23 %. Met de drempel 40 % (i.p.v. 50 %) wordt de bolling van het model zichtbaar: X32-35 een rij hoger.
#    Nieuwe randpixels krijgen de randtint van r2 (#, donker hout); de pixel eronder wordt hout in de gemeten tint.
for X in range(29,42):
    if cov[11,X]>=0.40 and o[11,X]==0:
        zet(X,11,7,'1 rand: dekking %d%%'%(cov[11,X]*100))
        cs=[q for q in cellen(X,12) if c[q]==3]; zet(X,12,near(np.mean([A[q] for q in cs],0),[7,8,9]),'1 hout onder de rand (gemeten gem.)')
# 5. STALEN BAND 2 px: per kolom X27-41 het zwaartepunt (gem. y) van de bandcellen van het model; de band = de 2 rijen
#    die daar het dichtst bij liggen. Modelband = 4 cellen hoog = 1,6 spritepx. Kolommen met < 4 bandcellen (X30-31:
#    2 cellen, de band zit daar boven het lichte houten lipje, model 0,8 px dik) blijven 1 px zoals r2.
#    Buitenlijnpixels van de emmer blijven (X27 rij 16).
rand=np.zeros((64,64),bool)
for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): rand|=np.roll(np.roll(r2==0,dy,0),dx,1)
for X in range(27,42):
    ys=[(y+0.5-MY0)/F for (y,x) in sum([cellen(X,Y) for Y in range(12,22)],[]) if c[y,x]==4]
    if len(ys)<4: continue
    m=np.mean(ys)
    for Y in sorted(range(13,21),key=lambda Y:abs(Y+0.5-m))[:2]:
        if not (rand[Y,X] and r2[Y,X]>0) and r2[Y,X]!=0: zet(X,Y,10,'5 band: zwaartepunt %.2f (%d cellen)'%(m,len(ys)))
# 2. ARM-BINNENLIJN (X43-47, Y32-49): zwart waar het middelpunt van een zwarte modelcel (L<70) valt. Het model loopt
#    schuin in van linksboven (43,32)(44,33), staat op x 45,37 (rij 34-40), 45,78 (41-42), 46,18 (43-44), 46,59 (45-47)
#    en 46,99-47,40 (48). Bovenaan en onderaan werd de lijn in r2 de lichtere lijntint (l); nu zwart zoals het model.
for Y in range(32,50):
    for X in ((43,44,45) if Y<=42 else (45,46,47)):   # alleen de binnenlijn; de buitenste armcontour (46-48, 35-37) blijft r2
        if any(L[q]<70 for q in cellen(X,Y)) and o[Y,X] in (2,3,4,5,6): zet(X,Y,1,'2 zwarte modelcel')
# 3. ONDERKANT (X16-30, Y54-56): per kolom de zwarte contour op de rij van het gemiddelde y van de zwarte modelcellen.
#    Gemeten: X16 55,12; X17-24 54,3-54,7; X25-26 55,12; X27-30 55,5-55,9. r2 had X16-26 allemaal op rij 54.
for X in range(16,31):
    ys=[(y+0.5-MY0)/F for (y,x) in sum([cellen(X,Y) for Y in range(52,58)],[]) if L[y,x]<70]
    Yc=int(np.floor(np.mean(ys)))
    for Y in range(54,57):
        if Y==Yc: zet(X,Y,1,'3 contour %.2f'%np.mean(ys))
        elif Y<Yc and o[Y,X] in (0,1): zet(X,Y,sneeuwtint(X,Y),'3 binnen (sneeuw gemeten)')
        elif Y>Yc and o[Y,X]!=0: zet(X,Y,0,'3 buiten')
# 4. BOVENSTE BUIKSTEEN (X24-32, Y34-41): vorm = steenaandeel >=40 % (r2: 45 %); rand rood/oranje (r2-tint o) waar
#    >=40 % gloed, anders K; naad: binnenpixel met >=2 gloedcellen (de modelnaad is 1 cel = 0,4 px breed en komt met
#    een aandeel nooit boven 40 %; zelfde regel als de lijnen); geel waar >=1 geelcel op de naad ligt en het geelaandeel
#    het hoogst is; rest grijs facet (donkere steen L>=50) of steen. Tinten = die van de andere r2-stenen.
sf=frac(np.isin(c,[5,6,7])); gf=frac(np.isin(c,[6,7])); yf=frac(c==7)
Lst=(np.bincount(I,up(np.where(c==5,Lk,0))[ok],minlength=4096)/np.maximum(np.bincount(I,up(c==5)[ok].astype(float),minlength=4096),1)).reshape(64,64)
S={(Y,X) for Y in range(34,42) for X in range(24,33) if sf[Y,X]>=0.40}
for Y in range(34,42):
    for X in range(24,33):
        if (Y,X) not in S and o[Y,X] in (1,10,13,14,15): zet(X,Y,sneeuwtint(X,Y),'4 buiten steen')
naad=[]
for (Y,X) in sorted(S):
    rnd=any((Y+dy,X+dx) not in S for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
    ng=sum(1 for q in cellen(X,Y) if c[q] in (6,7))
    if rnd: zet(X,Y,14 if gf[Y,X]>=0.40 else 1,'4 rand gloed %d%%'%(gf[Y,X]*100))
    elif ng>=2: zet(X,Y,14,'4 naad %d gloedcellen'%ng); naad.append((yf[Y,X],Y,X))
    else: zet(X,Y,10 if Lst[Y,X]>=50 else 13,'4 steen L%d'%Lst[Y,X])
if naad:
    f,Y,X=max(naad)
    if f>0: zet(X,Y,15,'4 geel (hoogste geelaandeel op de naad %d%%)'%(f*100))

# alles buiten de vijf zones: diff 0 met r2
buiten=np.ones((64,64),bool)
for x0,x1,y0,y1 in ZONES.values(): buiten[y0:y1+1,x0:x1+1]=False
assert ((o!=r2)&buiten).sum()==0, 'diff buiten de zones'
opslaan(o,'sprite_r6/sauna_yeti_r6.png')
from collections import Counter
print('r2->r6',(o!=r2).sum(),'px',dict(Counter(l[3][0] for l in log)),'| buiten zones 0')
if len(sys.argv)>1:
    for l in log: print(l)

# ---------- vel.png: r6 | r2 | model 8x / vijf zones 12x: r6 | r2 | model (natief, exact dezelfde afbeelding als de meting) ----------
from PIL import ImageDraw
NAT=np.asarray(Image.open(NATIEF).convert('RGB'))
def rgbp(path,bg=(255,255,255)):
    im=Image.open(path); q=np.asarray(im)[:64,:64]; pl=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[q==k]=pl[k]
    return Image.fromarray(img)
def model(x0,y0,x1,y1,z):   # elke uitvoerpixel -> natieve cel floor(MX0+u*F), zelfde afbeelding als spriteindex()
    W,H=(x1-x0)*z,(y1-y0)*z; u=x0+(np.arange(W)+0.5)/z; v=y0+(np.arange(H)+0.5)/z
    cx=np.floor(MX0+u*F).astype(int); cy=np.floor(MY0+v*F).astype(int)
    out=np.full((H,W,3),255,'uint8'); okx=(cx>=0)&(cx<NAT.shape[1]); oky=(cy>=0)&(cy<NAT.shape[0])
    sub=NAT[np.clip(cy,0,NAT.shape[0]-1)][:,np.clip(cx,0,NAT.shape[1]-1)]; out[:]=sub; out[~oky]=255; out[:,~okx]=255
    return Image.fromarray(out)
def raster(im,z,kl=(215,215,215)):
    d=ImageDraw.Draw(im)
    for x in range(0,im.width,z): d.line([(x,0),(x,im.height)],fill=kl)
    for y in range(0,im.height,z): d.line([(0,y),(im.width,y)],fill=kl)
    return im
s6=rgbp('sprite_r6/sauna_yeti_r6.png'); s2=rgbp('sprite_r2/sauna_yeti_r2.png')
rijen=[[s6.resize((512,512),Image.NEAREST),s2.resize((512,512),Image.NEAREST),model(0,0,64,64,8)]]
for x0,x1,y0,y1 in ((27,44,9,22),(40,51,30,51),(10,35,51,58),(22,35,33,43)):   # emmer (rand + band), arm, onderkant, steen
    z=12; b=(x0,y0,x1+1,y1+1)
    rijen.append([raster(s6.crop(b).resize(((x1+1-x0)*z,(y1+1-y0)*z),Image.NEAREST),z),
                  raster(s2.crop(b).resize(((x1+1-x0)*z,(y1+1-y0)*z),Image.NEAREST),z),raster(model(x0,y0,x1+1,y1+1,z),z,(255,120,120))])
klein=[]
for bg in ((255,255,255),(248,248,232),(40,48,56),(24,24,24)):
    t=Image.new('RGB',(140,70),bg); t.paste(rgbp('sprite_r6/sauna_yeti_r6.png',bg),(2,3)); t.paste(rgbp('../sneeuwmonster_fase2/af/sneeuwmonster2.png',bg),(72,3)); klein.append(t)
rijen.append(klein)
Wd=max(sum(p.width+8 for p in r) for r in rijen); Hd=sum(max(p.height for p in r)+8 for r in rijen)
vel=Image.new('RGB',(Wd,Hd),'white'); y=0
for r in rijen:
    x=0
    for p in r: vel.paste(p,(x,y)); x+=p.width+8
    y+=max(p.height for p in r)+8
vel.save('sprite_r6/vel.png'); q=np.asarray(Image.open('sprite_r6/sauna_yeti_r6.png')); ys,xs=np.where(q>0)
print('vel',vel.size,'| kleuren',len(np.unique(q)),'bbox',xs.min(),xs.max(),ys.min(),ys.max())
