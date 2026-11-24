# r3/r4: reparaties na bouw (hoed B, oog E2r3, opschoning). Alleen omkleuren van bestaande pixels; vormen komen uit
# het model (r9), Mr. Rime of de modusreductie. Tonen (toon.py, r4): 0=16 1=32 2=64 3=96 4=112 5=144 6=208 7=248.
import numpy as np; from PIL import Image
K=np.load('kaal_idx.npy'); OY=3
def kaal(y,x): return K[y-OY,x] if 0<=y-OY<K.shape[0] else -1
NAT=np.asarray(Image.open('natief_kop.png').convert('L')).astype(float)
def model_l(y,x):   # gemiddelde modelhelderheid in het vlak van spritecel (y,x) (zelfde raster als de reductie)
    y0=16.5+2.5*y; x0=7+2.5*x
    return NAT[int(y0):int(y0+2.5), int(x0):int(x0+2.5)].mean()
def post(C,log):
    C=C.copy()
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    # 1. voorhoofd: de overgebleven gedupliceerde rij (y15, onder de rand) -> gezichtswit
    pass   # r5: voorhoofd/oogvlak al wit in r5.py (rij 15 bevat nu het Rime-oog)
    # 5. volume lijf: hooglicht (r4: index 4 = 112, 1 stap boven pak 96) op tint 3, in een band van 1-2 px langs de linker-/bovenrand van
    #    elke lob, binnen de vakken van de keurder; voorbeen: cellen die in het model lichter zijn (>=78 tegen 75).
    def lob(x0,x1,y0,y1,naam):
        D=C.copy()
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                if D[y,x]!=3: continue
                rand=[D[y-1,x],D[y,x-1],D[y-2,x],D[y,x-2],D[y-1,x-1]]
                if any(t not in (1,2,3) for t in rand): zet(y,x,4,naam)
    lob(36,42,30,35,'hooglicht rechterlob (randband linksboven)')
    lob(26,29,30,34,'hooglicht linkerlob (randband linksboven)')
    for y in range(46,53):
        for x in range(22,30):
            if C[y,x]==3 and model_l(y,x)>=78: zet(y,x,4,'hooglicht voorbeen (lichter in model r9)')
    # 7. hoedkruin: hooglicht waar de r9-bol (kale reductie) tint 5 heeft, r9-bol (rij 3, x30) uitgelijnd op de
    #    binnenkant van de Rime-kruin (bovenste rij met tint 3, meest linkse kolom daarvan)
    ys=[y for y in range(0,12) if (C[y,28:46]==3).any()]; yt=ys[0]
    xl=min(x for y in ys[:3] for x in range(28,46) if C[y,x]==3)
    for y in range(3,8):
        for x in range(28,46):
            if kaal(y,x)==5:
                yy,xx=y-3+yt,x-30+xl
                if C[yy,xx]==3: zet(yy,xx,4,'hoedkruin hooglicht (r9-bol)')
    # 9. stok over de hand: stokpixels (tint 0-3) uit de reductie van natief_kop_stok.png (stok verbreed en over de
    #    hand, zoals in het model) binnen 1,5 px van de stokas (breder dekt de handschoen te veel af), rijen 26-33
    KS=np.load('kaal_stok_idx.npy')
    for y in range(26,34):
        ax=12.5+0.75*(y-27)
        for x in range(8,22):
            v=KS[y-OY,x]
            if abs(x-ax)<=1.5 and 0<=v<=3: zet(y,x,v,'stok over de hand (reductie met stok)')
    # 10. losse lichte pixel (45,45) -> 48; gat (21,28) in de linker snorkrul -> zwart (model heeft daar 1 gat)
    if C[45,45]>=5: zet(45,45,1,'losse lichte pixel (45,45) -> 48')
    # r5: (21,28) niet meer: de snorbovenrand volgt nu de modelrand (r5.snor_top)
    return C
