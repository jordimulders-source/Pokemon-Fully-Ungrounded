# r6-palet: koel blauwgrijs zoals Alphyena (mightyena_evo/af), wit blijft wit. Pak/hoed/haar/benen 1 tint lichter dan r4
# (r4 16/32/64/96 -> lijn 16, schaduw 40, basis 66, licht 100; bolling 128 alleen in de ellipsen).
import numpy as np
PAL5=[(16,16,24),(40,40,54),(66,70,92),(100,106,132),(128,124,146),(164,162,178),(200,200,212),(248,248,248)]
GEZICHT=lambda y,x: 13<=y<=26 and 22<=x<=50     # gezicht + snor + neus + ogen: tonen 1-op-1 (geen verschuiving)
DONKER={1:1,2:1,3:2,4:3}   # r4 32->40 schaduw, 64->40, 96 (basis)->66, 112 (hooglichtband)->100
def omzetten(C,STOK,log):
    """C (r4-indexen 0..7, -1 transparant) -> r5-indexen 0..7 in PAL5. Donkere delen (pak, benen, hoed, haar) 1 tint
    lichter (1->2, 2->3, 3->4, 4->5); zwarte pixels binnen een donker vlak (geen transparante buur) -> 1 (lijn in de
    donkerste eigen tint), zodat zwart 16 alleen de omlijning is. Stok (STOK-masker) heeft al eigen tinten."""
    H,W=C.shape; O=C.copy()
    def zet(y,x,v,zone):
        if O[y,x]!=v: O[y,x]=v; log[zone]=log.get(zone,0)+1
    for y in range(H):
        for x in range(W):
            v=C[y,x]
            if v<0 or STOK[y,x] or GEZICHT(y,x): continue
            nb=[C[yy,xx] if 0<=yy<H and 0<=xx<W else -1 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
            if v==4 and -1 in nb and any(t in (5,6,7) for t in nb): continue   # selout van een licht deel (hand, schoen, V) blijft 112-rol
            if 1<=v<=4: zet(y,x,DONKER[v],'pak/hoed/haar/benen: r4-tint -> r6 (1 tint lichter dan r4)')
            elif False and v==0:
                nb=[C[yy,xx] if 0<=yy<H and 0<=xx<W else -1 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
                if -1 not in nb and any(1<=t<=4 for t in nb) and not any(STOK[yy,xx] for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if 0<=yy<H and 0<=xx<W):
                    zet(y,x,1,'binnenlijn in donker vlak -> donkerste eigen tint (40)')
    return O
def rgb(C,bg=(152,208,160)):
    img=np.zeros(C.shape+(3,),'uint8'); img[:]=bg
    for i,t in enumerate(PAL5): img[C==i]=t
    return img
def volume(C,log):
    """Volume per vorm zoals Alphyena: bolling = 1 tint lichter (4->5) in een ellips per vorm, minstens 1 px van een lijn;
    donkere benen: lichte kant (2->3) direct rechts van de linkeromlijning. Alleen tinten."""
    C=C.copy(); H,W=C.shape
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    D=C.copy()
    def ellips(cy,cx,ry,rx,naam):
        for y in range(int(cy-ry),int(cy+ry)+1):
            for x in range(int(cx-rx),int(cx+rx)+1):
                d=((y-cy)/ry)**2+((x-cx)/rx)**2
                if d<=1 and D[y,x] in (2,3):
                    if all(D[yy,xx] not in (0,1,-1) for yy in range(y-1,y+2) for xx in range(x-1,x+2)):
                        zet(y,x,4 if d<=0.36 else 3,naam)   # kern 128, rand 100
    for args in ELLIPSEN: ellips(*args)
    for (y0,y1,x0,x1,naam) in LICHTE_KANT:
        for y in range(y0,y1+1):
            xs=[x for x in range(x0,x1+1) if D[y,x] in (0,1)]
            for x in range(x0,x1+1):
                if D[y,x] in (0,1) and x+1<=x1 and D[y,x+1]==2: zet(y,x+1,3,naam); break
    return C
# (cy,cx,ry,rx,naam): bolling per vorm (tint 4 -> 5), Alphyena-werkwijze
ELLIPSEN=[(34,41,4.5,4,'bolling rechterpand'),(34.5,28.5,4,1.8,'bolling linkerpand'),
          (48,47.5,1.2,3,'bolling achterdij'),(34,51,2.5,1.5,'bolling rechterarm'),(6,38,1.5,4,'bolling hoedkruin')]
# (y0,y1,x0,x1,naam): lichte kant donkere benen (eerste pixel rechts van de linkerlijn 2 -> 3)
LICHTE_KANT=[(49,55,22,31,'lichte kant voorbeen (onder)'),(49,53,43,58,'lichte kant achterbeen')]
