# Vileplume r18: alleen de poten (y42-62) opnieuw uit het natieve model; rest = r17 pixel voor pixel.
# Per spriterij: pad = gewogen midden van de poot in het natieve raster (gereedschap/natief.png, cellen per 2),
# opbouw [linkerrand | licht | rechterrand] met de tinten van de dominante modelrij op die hoogte
# (dichtstbijzijnde paletkleur in RGB). Draaien vanuit vileplume_sprite/: python3 r18/bouw.py
import sys; sys.path.insert(0,'gereedschap')
from gemeen import *

P={1:(24,5,4),6:(44,64,68),7:(124,154,155),8:(162,191,191),9:(194,216,214),10:(232,243,235)}
def near(c): return min(P,key=lambda k:sum((a-b)**2 for a,b in zip(P[k],c)))
nat=np.array(Image.open('gereedschap/natief.png').convert('RGB')).astype(float); Lum=nat.mean(2)

def meet(u0,u1,y):
    # gewogen randen (spritecoord) en tinten van de dominante modelrij voor spriterij y
    va=V0+(y-Y0)/S; vb=va+1/S; W=XL=XR=0; best=None
    for mv in range(int(va)//2*2,int(np.ceil(vb)),2):
        w=max(0,min(vb,mv+2)-max(va,mv)); g=[u for u in range(u0,u1,2) if Lum[mv,u]<250]
        if w<=0 or not g: continue
        W+=w; XL+=w*(X0+(g[0]-U0)*S); XR+=w*(X0+(g[-1]+2-U0)*S)
        if best is None or w>best[0]: best=(w,mv,[near(nat[mv,u]) for u in g])
    return XL/W,XR/W,best[1],best[2]

# Tabel per poot: y -> (eerste x, tinten links->rechts). Breedte 3 (rand|licht|rand); x = round(midden-1,5).
# Uitzonderingen (zie NOTITIES): aanzet rechterpoot y42-44 breder zoals het model (4,3-4,5 px);
# voet = 2 px zwart; rechterpoot y45-46 rechterrand 7 -> 6 (lichte pixel op de schaduwkant);
# linkerpoot y42 rechterrand 6 -> 1 (losse pixel boven de zwarte y43-44);
# rechterpoot y45 op x35 i.p.v. x34 (midden 35,82 rondt naar 34, maar dan springt de rechterrand x37->36->37: inkeping).
LINKS={42:(25,[7,8,1]),43:(24,[7,10,1]),44:(24,[7,10,1]),45:(23,[7,10,6]),46:(23,[7,10,6]),
       47:(23,[6,9,6]),48:(23,[6,9,6]),49:(24,[7,9,6]),50:(24,[7,9,6]),51:(24,[7,9,6]),
       52:(24,[6,9,1]),53:(24,[6,9,1]),54:(24,[6,9,1]),55:(24,[6,9,1]),
       56:(24,[6,8,1]),57:(24,[6,8,1]),58:(24,[6,8,1]),59:(25,[1,1])}
RECHTS={42:(33,[1,8,8,8,1]),43:(33,[1,8,8,8,1]),44:(34,[6,8,8,1]),45:(35,[6,10,6]),46:(35,[6,10,6]),
        47:(35,[6,10,6]),48:(35,[6,10,6]),49:(36,[7,10,6]),50:(36,[7,9,6]),51:(36,[7,9,6]),52:(36,[7,9,6]),
        53:(37,[6,9,6]),54:(37,[6,9,6]),55:(37,[6,9,6]),56:(37,[6,9,6]),57:(37,[6,9,6]),58:(37,[6,9,6]),
        59:(38,[6,9,6]),60:(38,[6,8,1]),61:(38,[6,8,1]),62:(39,[1,1])}

if __name__=='__main__':
    src=Image.open('r17/vileplume_r17.png'); pal=src.getpalette()[:48]; PAL=[tuple(pal[i*3:i*3+3]) for i in range(16)]
    a17=np.array(src); o=a17.copy(); o[42:63]=0
    for T in (LINKS,RECHTS):
        for y,(x,t) in T.items(): o[y,x:x+len(t)]=t
    assert (o[:42]==a17[:42]).all() and (o[63:]==a17[63:]).all(), 'buiten de poten veranderd'
    assert not np.where(a17[42:63])[1].min()<23 and not np.where(a17[42:63])[1].max()>40
    opslaan(o,PAL,'r18/vileplume_r18.png')
    # verslag: model per rij naast de keuze
    for nm,(u0,u1),T in [('L',(78,94),LINKS),('R',(102,124),RECHTS)]:
        for y in range(42,63):
            if y not in T: continue
            xl,xr,mv,tt=meet(u0,u1,y); x,t=T[y]
            print(f'{nm} y{y} model v{mv} x{xl:.1f}-{xr:.1f} midden {(xl+xr)/2:.2f} tinten {tt} -> x{x}-{x+len(t)-1} {t}')
    d=(o!=a17); print('pixels anders dan r17:',d.sum(),'rijen',sorted(set(np.where(d)[0])))
    # vellen
    Z=12; x0,y0,x1,y1=20,38,44,64
    def uit(a,z):
        return rgb(a,PAL).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
    a14=np.array(Image.open('r14/vileplume_r14.png'))
    tegels=[('r18',uit(o,Z)),('r17',uit(a17,Z)),('r14',uit(a14,Z)),('model',model_crop(x0,y0,x1,y1,Z))]
    from PIL import ImageDraw
    w=(x1-x0)*Z; vel=Image.new('RGB',(4*w+3*12,(y1-y0)*Z+18),'white'); dr=ImageDraw.Draw(vel)
    for i,(nm,t) in enumerate(tegels): vel.paste(t,(i*(w+12),18)); dr.text((i*(w+12),3),nm,fill='black')
    vel.save('r18/poten_12x.png')
    rgb(o,PAL).resize((512,512),Image.NEAREST).save('r18/r18_8x.png')
