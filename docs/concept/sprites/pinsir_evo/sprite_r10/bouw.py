# Pinsir-evolutie r10. Jordi bij r9 (letterlijk): "het hoofd is gewoon nog steeds niet zoals het model en hij kijkt scheel".
# Eerder: "gewoon het model volgen", "je moest alleen de ogen een paar pixels aanpassen", "lekker opnieuw tekenen want dat kan je zo goed".
# r10: ALLEEN DE KOP (kopschild met stekels, achterkam met kegels binnen de r9-kopzone, gezicht met ogen) opnieuw als VERKLEINING
#      VAN HET MODEL. Alles daarbuiten (kaken, mond, romp, dekschild, rugdoorns, poten, staart) = sprite_r9/pinsir_evo_r9_A_A.png.
# Werkwijze (niets tekenen, alleen meten):
#   1. per spritecel (974/64 = 15,22 modelpx, registratie van sprite_r1/kaal.png: x31, y134, rij 13) uit het bevroren model:
#      dekking (voorgrond), lijnaandeel (modelzwart L<25 binnen de voorgrond) en de mediaantoon van de niet-zwarte modelpixels.
#   2. silhouet = cel met dekking >= 0,35 (drempel van r1); rand van het silhouet = zwart (zoals de rest van de sprite).
#   3. binnencel met lijnaandeel >= 0,35 = lijntint L (gekleurde lijn, geen extra zwart); anders de modeltoon in de r9-lijftinten:
#      <38 L, <54 a, <78 b, <128 c, anders d (modeltonen 62 / 85-125 / >125 -> b / c / d; kleur mag van het model afwijken).
#   4. benoemde opschoning (stekeltips, 1 vlekje) en het gezicht (ogen, wenkbrauw-V) per pixel naar het model.
# Bouwen: cd pinsir_evo && python3 sprite_r10/bouw.py [raster]
import sys, numpy as np
from PIL import Image
UIT='sprite_r10'
CH='.KLabcdopqrsvwxT'; C={c:i for i,c in enumerate(CH)}
R9P='sprite_r9/pinsir_evo_r9_A_A.png'
R9=np.asarray(Image.open(R9P)).astype(int); PAL=Image.open(R9P).getpalette()[:48]
CEL=974/64; MX0,MY0,DY=31,134,13
H=W=64; yy,xx=np.mgrid[:H,:W]
# ---- kopzone: de r9-kopzone (sprite_r9/bouw.py) zonder kaak- en dekschildpixels, en zonder kolom 45 (naad met de r8-rugdoorn blijft r9) ----
DEEL=np.load('sprite_r8/r7_delen.npy')
KOP9=((yy<=23)&(xx<=45)) | ((yy>=24)&(yy<=28)&(xx<=44)&(DEEL!='schild'))
ZONE=KOP9 & ~np.isin(R9,range(7,15)) & (xx<=44)
# ---- 1. meting per cel ----
a=np.asarray(Image.open('referenties/gemini_gekozen_r4B.png').convert('RGB')).astype(float)
L=a.mean(2); fg=a.min(2)<215
cov=np.zeros((H,W)); lijn=np.zeros((H,W)); toon=np.zeros((H,W))
for j,i in zip(*np.where(ZONE)):
    ya,yb=int(round(MY0+(j-DY)*CEL)),int(round(MY0+(j+1-DY)*CEL)); xa,xb=int(round(MX0+i*CEL)),int(round(MX0+(i+1)*CEL))
    ya,xa=max(ya,0),max(xa,0)
    if yb<=ya or xb<=xa: continue
    f=fg[ya:yb,xa:xb]; l=L[ya:yb,xa:xb]; cov[j,i]=f.mean()
    if f.sum()==0: continue
    lijn[j,i]=(l[f]<25).sum()/f.sum()
    nb=f&(l>=25); toon[j,i]=np.median(l[nb]) if nb.sum()>=6 else 0
def tint(v): return C['L'] if v<38 else C['a'] if v<54 else C['b'] if v<78 else C['c'] if v<128 else C['d']
# ---- 2/3. kale reductie van de kop ----
kaal=R9.copy()
for j,i in zip(*np.where(ZONE)):
    kaal[j,i]=0 if cov[j,i]<0.35 else C['L'] if (lijn[j,i]>=0.35 or toon[j,i]==0) else tint(toon[j,i])
f=kaal>0
for j,i in zip(*np.where(ZONE&f)):
    if any(not f[j+dy,i+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): kaal[j,i]=C['K']
# ---- 4. benoemde stappen: (x, y): teken, met reden ----
STAP={
 'stekeltips': {   # punt gemeten op de modelomtrek; de vlakdrempel 0,35 snijdt een smalle punt af die >= 1/3 rij in de cel steekt
   (15,19):'K',    # kleine voorste stekel: modelpunt x15,1-15,9, y19,6 (dekking 0,30)
   (23,16):'K',    # stekel op de voorrand: modelpunt x23,5-23,9, y16,6
   (26,15):'K',    # stekel achter het schild: modelpunt x26,2-27,0, y15,6 (dekking 0,30)
   (38,13):'K'},   # grote rugstekel rechts: modelpunt x38,3-38,7, y13,6 (zelfde hoogte als de linker, x32-33 y13,3)
 'vlekje': {
   (20,20):'c'},   # losse b tussen c-pixels; model '=---' (75 % licht), mediaan 74 lag op de grens b/c
 'gezicht': {      # gemeten op het model per kwart pixel (sprite_r10/NOTITIES.md): de onderrand van het schild is een zwarte V:
                   # boven het verre oog op rij 26, zakt tussen de ogen naar rij 28 (x18-20) en loopt boven het nabije oog op rij 27
   (15,26):'K',(16,26):'K',            # V links: modellijn x14-16,5 y26-26,7 (reductie gaf L)
   (17,26):'d',                        # lichte schildrand boven het verre oog (model '...=' / '-.-=', ongewijzigd t.o.v. kaal)
   (14,27):'c',                        # wangplaat links van het verre oog (model '----')
   (15,27):'K',                        # zwarte rand links van het verre oog (modellijn x15,75-16)
   (16,27):'T',                        # VER OOG, buitenkant (model: lichte spleet x16,1-16,8, y26,7-28,0)
   (17,27):'K',                        # V links: model '@#--/@@..' (zwart links in de cel)
   (18,27):'c',(19,27):'c',(20,27):'c',# lichte tong van het schild tussen de ogen (model '-.==', '===-', '----')
   (21,27):'K',(22,27):'K',(23,27):'K',(24,27):'K',  # wenkbrauw boven het nabije oog: model zwart y27,5-27,9 x21-27
   (15,28):'b',                        # wang onder links (model '=--=')
   (16,28):'T',(17,28):'T',            # VER OOG, binnenkant omlaag naar het midden (model: staartje x17,1-17,4 y27,9-28,2)
   (18,28):'K',(19,28):'K',(20,28):'K',# onderkant van de V tussen de ogen: model '@@@@' y28,0-28,7
   (21,28):'T',(22,28):'T',(23,28):'T',# NABIJ OOG (model: x20,8-23,9, y27,7-28,8; binnenkant x21 iets lager)
   (24,28):'b'},                       # gezicht rechts van het nabije oog (model '====')
}
OOG_A={(23,27):'T',(23,26):'K'}   # variant A: buitenkant van het nabije oog 1 rij hoger (gespiegeld aan het verre oog, even hoog: rij 27-28);
                                  # de wenkbrauw schuift daar 1 rij mee omhoog. Model: wenkbrauw vlak op y27,5 -> variant B.
def bouw(variant):
    q=kaal.copy(); tel={}
    for n,d in list(STAP.items())+([('oog A',OOG_A)] if variant=='A' else []):
        v=q.copy()
        for (X,Y),ch in d.items(): assert ZONE[Y,X],(X,Y); q[Y,X]=C[ch]
        tel[n]=int((q!=v).sum())
    return q,tel
def opslaan(q,path):
    p=Image.fromarray(q.astype('uint8'),'P'); p.putpalette(PAL+[0]*(768-len(PAL))); p.save(path,transparency=0)
VAR={}
for v,naam in (('A','pinsir_evo_r10.png'),('B','pinsir_evo_r10_oogB.png')):
    q,tel=bouw(v); VAR[v]=q; opslaan(q,UIT+'/'+naam)
    im=Image.open(UIT+'/'+naam); assert im.info.get('transparency')==0 and (np.asarray(im)==q).all()
    buiten=int((q[~ZONE]!=R9[~ZONE]).sum())
    print('%s (%s): kleuren %d | diff buiten de kopzone met r9_A_A: %d | kop: %d px in de zone, anders dan r9: %d'%(
        v,naam,len(set(q.ravel())),buiten,int((ZONE&(q>0)).sum()),int((q[ZONE]!=R9[ZONE]).sum())))
    assert buiten==0 and len(set(q.ravel()))<=16
    print('   pixels anders dan de kale modelreductie, per stap:',tel,'| totaal',int((q!=kaal).sum()))
    sil=(q>0)&ZONE; msk=(cov>=0.35)&ZONE
    print('   silhouet anders dan het modelmasker:',[(int(x),int(y)) for y,x in np.argwhere(sil!=msk)])
    print('   zwart in de kop: %d (r9: %d)'%(int(((q==1)&ZONE).sum()),int(((R9==1)&ZONE).sum())))
np.save(UIT+'/zone.npy',ZONE); opslaan(kaal,UIT+'/kaal_kop.png')
if 'raster' in sys.argv:
    for v in 'AB':
        q=VAR[v]; print(v+'   '+''.join(str(x%10) for x in range(9,46)))
        for Y in range(12,30): print('%2d   '%Y+''.join((CH[q[Y,X]] if ZONE[Y,X] else CH[q[Y,X]].upper().replace('.','_')) for X in range(9,46)))
# ---- vel: kop 16x r10 | r9 | model met spriteraster; kop 16x r10-B en r10 met modelmasker (rood); hele sprite 8x r10 | model; 1x wit/donker ----
if 'raster' not in sys.argv:
    sys.path.insert(0,'gereedschap')
    from PIL import ImageDraw
    from vel import rgbp, model_crop
    MSK=cov>=0.35
    bx=(9,12,46,31); z=16; bw,bh=(bx[2]-bx[0])*z,(bx[3]-bx[1])*z
    def raster(im,al=0.25,kleur=(0,120,255)):
        g=np.asarray(im).astype(float)
        for x in range(0,g.shape[1],z): g[:,x]=g[:,x]*(1-al)+np.array(kleur)*al
        for y in range(0,g.shape[0],z): g[y,:]=g[y,:]*(1-al)+np.array(kleur)*al
        im=Image.fromarray(g.astype('uint8')); d=ImageDraw.Draw(im)
        for X in range(bx[0],bx[2],2): d.text(((X-bx[0])*z+2,1),str(X),fill=(255,0,255))
        for Y in range(bx[1],bx[3]): d.text((1,(Y-bx[1])*z+2),str(Y),fill=(255,0,255))
        return im
    def kop(p): return raster(rgbp(p).crop(bx).resize((bw,bh),Image.NEAREST))
    def masker(im):
        dd=ImageDraw.Draw(im)
        for Y in range(bx[1],bx[3]):
            for X in range(bx[0],bx[2]):
                if not (MSK[Y,X] and ZONE[Y,X]): continue
                px,py=(X-bx[0])*z,(Y-bx[1])*z
                for (dy,dx),ln in (((-1,0),(px,py,px+z,py)),((1,0),(px,py+z-1,px+z,py+z-1)),((0,-1),(px,py,px,py+z)),((0,1),(px+z-1,py,px+z-1,py+z))):
                    if not (MSK[Y+dy,X+dx] and ZONE[Y+dy,X+dx]): dd.line(ln,fill=(255,0,0),width=2)
        return im
    A,B=UIT+'/pinsir_evo_r10.png',UIT+'/pinsir_evo_r10_oogB.png'
    v=Image.new('RGB',(3*bw+16,2*bh+28+512+14+150),'white'); d=ImageDraw.Draw(v); y=0
    d.text((4,y),'kop 16x: r10 (oog A) | r9 A_A | model met spriteraster',fill=(0,0,0)); y+=12
    for i,im in enumerate((kop(A),kop(R9P),raster(model_crop(*bx,z)))): v.paste(im,(i*(bw+8),y))
    y+=bh+4; d.text((4,y),'kop 16x: r10 oog B | r10 oog A met modelmasker (rode omtrek, dekking >= 0,35) | kale modelreductie (zonder opschoning/gezicht)',fill=(0,0,0)); y+=12
    for i,im in enumerate((kop(B),masker(kop(A)),kop(UIT+'/kaal_kop.png'))): v.paste(im,(i*(bw+8),y))
    y+=bh+4; d.text((4,y),'hele sprite 8x: r10 oog A | model op dezelfde maat',fill=(0,0,0)); y+=12
    v.paste(rgbp(A).resize((512,512),Image.NEAREST),(0,y)); v.paste(model_crop(0,0,64,64,8),(520,y)); y+=520
    d.text((4,y),'1x en 2x: r10 A, r10 B, r9 op wit en donker',fill=(0,0,0)); y+=12; x=0
    for p in (A,B,R9P):
        for bg in ((255,255,255),(40,48,56)):
            v.paste(rgbp(p,bg),(x,y)); v.paste(rgbp(p,bg).resize((128,128),Image.NEAREST),(x+68,y)); x+=204
    v=v.crop((0,0,v.width,y+130)); v.save(UIT+'/vel.png'); print('vel',v.size)
