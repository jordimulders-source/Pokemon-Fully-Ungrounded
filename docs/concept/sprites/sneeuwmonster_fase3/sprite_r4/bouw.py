# Ronde 4 = r2 (gezicht en vacht) + uit r3 ALLEEN palet en stenen; daarna gezicht per spritepixel GEMETEN uit het model.
# Gebruik vanuit sneeuwmonster_fase3: python3 sprite_r4/bouw.py [log]
# Geen gladstrijken: elke gewijzigde gezichtspixel komt uit een meting van de natieve modelcellen (pitch 5,867)
# waarvan het middelpunt in die spritepixel valt (±6 cellen per spritepixel).
import sys, numpy as np; from PIL import Image; from collections import Counter, defaultdict
sys.path.insert(0,'gereedschap'); from gemeen import *; from gemeen import label; from klassen import klassen
r2=np.asarray(Image.open('sprite_r2/sauna_yeti_r2.png')).astype(int)
r3=np.asarray(Image.open('sprite_r3/sauna_yeti_r3.png')).astype(int)
o=r2.copy(); log=[]
def zet(X,Y,t,why):
    if o[Y,X]!=t: log.append((int(X),int(Y),CH4[o[Y,X]]+'>'+CH4[t],why)); o[Y,X]=t
# ---------- uit r3: palet (P) ----------
PAL4=list(PAL); PAL4[11]=(112,151,164); PAL4[12]=(216,72,32)   # 1 handtint (gemeten gem. vlakke handcellen) + rood terug
CH4=CH[:12]+'r'+CH[13:]
for Y,X in zip(*np.where(o==12)): zet(X,Y,11,'P')              # handlicht -> de ene handtint
# ---------- uit r3: stenen (S), zelfde steenmasker als r3 ----------
a,c,Lk=klassen(); idx=spriteindex(); ok=idx>=0; I=idx[ok]; n=np.maximum(np.bincount(I,minlength=4096),1)
stf=(np.bincount(I,up(np.isin(c,[5,6,7]))[ok].astype(float),minlength=4096)/n).reshape(64,64)
st=(stf>=0.45)&(r2>0)
for Y,X in zip(*np.where(st)): zet(X,Y,r3[Y,X],'S')
na_r3=o.copy()
# ---------- gezicht: meting per spritepixel ----------
A=a.astype(float); L=.299*A[...,0]+.587*A[...,1]+.114*A[...,2]
cel=defaultdict(list)
for y in range(A.shape[0]):
    for x in range(A.shape[1]):
        X=int(np.floor((x+0.5-MX0)/F)); Y=int(np.floor((y+0.5-MY0)/F))
        if 0<=X<64 and 0<=Y<64: cel[(X,Y)].append((y,x))
P=np.array(PAL4,float)
def near(col,keus): return min(keus,key=lambda k:((P[k]-col)**2).sum())
LIJN=150; ZWART=60
# zwart (K): per samenhangende groep modelcellen L<60 (pupillen, zwaar lid, neus, mondhaak) 1 spritepixel op het
# zwaartepunt van de groep (groep van <=7 cellen = <=1 spritepixel). Zo verdubbelt een groep op een pixelgrens niet.
zwm=L<ZWART; zwm[:, :95]=False; zwm[:,140:]=False; zwm[:28,:]=False; zwm[50:,:]=False   # alleen het gezicht
lab,nz=label(zwm); KSET={}
for i in range(1,nz+1):
    ys,xs=np.where(lab==i); cx,cy=xs.mean(),ys.mean()
    K_=(int(np.floor((cx+0.5-MX0)/F)),int(np.floor((cy+0.5-MY0)/F))); KSET[K_]='zwart: groep %d cellen, zwaartepunt natief (%.1f,%.1f)'%(len(xs),cx,cy)
def meet(X,Y):
    """zwart als het zwaartepunt van een zwarte modelgroep in deze pixel valt; anders lijnpixel als >=2 modelcellen L<150
    (een 1-cel-lijn van het model raakt zo 2-3 cellen per spritepixel), tint = gemiddelde van die lijncellen -> l of s;
    anders vlak: mediaan van de niet-lijncellen -> s/m/h/w."""
    if (X,Y) in KSET: return 1,KSET[(X,Y)]
    cs=cel[(X,Y)]; ln=[q for q in cs if L[q]<LIJN]; fl=[q for q in cs if L[q]>=LIJN]
    if len(ln)>=2: return near(np.mean([A[q] for q in ln],0),[2,3]),'lijn %d/%d'%(len(ln),len(cs))
    return near(np.median([A[q] for q in fl],0),[3,4,5,6]),'vlak'
ZY=range(20,33); ZX=range(23,41)          # gezichtsgebied incl. wenkbrauw, wangvacht en kin
for Y in ZY:
    for X in ZX:
        v=o[Y,X]
        if st[Y,X] or v in (0,7,8,9,10,11,13,14,15): continue   # stenen, emmer, buitenlijn blijven
        if v==1 and not (25<=X<=36 and 22<=Y<=28): continue      # zwarte omlijning buiten de gezichtskern blijft
        rand=any(o[Y+dy,X+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
        if rand: continue
        t,why=meet(X,Y); zet(X,Y,t,'G '+why)
# AFWIJKING van de meting (1 px): bovenkant van de mondhaak. In (33,26) valt 1 lijncel (natief x123,y43, het
# opgaande eind van de glimlach), onder de drempel van 2. Zonder deze pixel is de haak een plat eindje; lijntint l.
zet(33,26,2,'AFW haak')
opslaan(o,'sprite_r4/sauna_yeti_r4.png',PAL4)
cnt=Counter(l[3].split()[0] for l in log)
print('r2->r4',(o!=r2).sum(),'px',dict(cnt),'| gezicht t.o.v. r2:',sum(1 for l in log if l[3].startswith('G')))
print('t.o.v. r3:',(o!=r3).sum(),'px')
if len(sys.argv)>1:
    for l in log: print(l)
    toon(o,18,34,21,42)

# ---------- vel.png: r4 | r2 | model 8x / gezicht 16x (sprite | model natief, zelfde uitsnede) / stenen 12x / 1x ----------
from PIL import ImageDraw
def rgbp(path,bg=(255,255,255)):
    im=Image.open(path); q=np.asarray(im)[:64,:64]; pl=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[q==k]=pl[k]
    return Image.fromarray(img)
NAT=Image.open(NATIEF).convert('RGB'); MOD=Image.open(MODEL).convert('RGB')
def mod(x0,y0,x1,y1,size,nat=False):
    a0,b0=s2n(x0,y0); a1,b1=s2n(x1,y1)
    if nat: return NAT.transform(size,Image.EXTENT,(a0,b0,a1,b1),Image.NEAREST,fillcolor=(255,255,255))
    Pm=1408/240; return MOD.transform(size,Image.EXTENT,(a0*Pm+4.5-Pm,b0*Pm+5.0-Pm,a1*Pm+4.5-Pm,b1*Pm+5.0-Pm),Image.BICUBIC,fillcolor=(255,255,255))
def raster(im,z,kl=(220,220,220)):
    d=ImageDraw.Draw(im)
    for x in range(0,im.width,z): d.line([(x,0),(x,im.height)],fill=kl)
    for y in range(0,im.height,z): d.line([(0,y),(im.width,y)],fill=kl)
    return im
s4=rgbp('sprite_r4/sauna_yeti_r4.png'); s2=rgbp('sprite_r2/sauna_yeti_r2.png')
rijen=[[s4.resize((512,512),Image.NEAREST),s2.resize((512,512),Image.NEAREST),mod(0,0,64,64,(512,512))]]
x0,y0,x1,y1=21,18,42,34; z=16; sz=((x1-x0)*z,(y1-y0)*z)
rijen.append([raster(s4.crop((x0,y0,x1,y1)).resize(sz,Image.NEAREST),z),raster(mod(x0,y0,x1,y1,sz,True),z,(255,90,90))])
for (a0,b0,a1,b1) in ((10,16,26,28),(42,16,58,30),(10,33,47,51)):
    z=12; sz=((a1-a0)*z,(b1-b0)*z)
    rijen.append([raster(s4.crop((a0,b0,a1,b1)).resize(sz,Image.NEAREST),z),mod(a0,b0,a1,b1,sz)])
f2='../sneeuwmonster_fase2/af/sneeuwmonster2.png'; klein=[]
for bg in ((255,255,255),(248,248,232),(40,48,56),(24,24,24)):
    t=Image.new('RGB',(140,70),bg); t.paste(rgbp('sprite_r4/sauna_yeti_r4.png',bg),(2,3)); t.paste(rgbp(f2,bg),(72,3)); klein.append(t)
klein.append(mod(0,0,64,64,(64,64)))
rijen.append(klein)
Wd=max(sum(p.width+8 for p in r) for r in rijen); Hd=sum(max(p.height for p in r)+8 for r in rijen)
vel=Image.new('RGB',(Wd,Hd),'white'); y=0
for r in rijen:
    x=0
    for p in r: vel.paste(p,(x,y)); x+=p.width+8
    y+=max(p.height for p in r)+8
vel.save('sprite_r4/vel.png'); print('vel',vel.size)
# controle
q=np.asarray(Image.open('sprite_r4/sauna_yeti_r4.png')); ys,xs=np.where(q>0)
print('kleuren',len(np.unique(q)),'bbox',xs.min(),xs.max(),ys.min(),ys.max())
