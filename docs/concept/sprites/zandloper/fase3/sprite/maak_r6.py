# Ronde 6 op r5 (indexbeeld r5/zandloper_fase3.png), alleen per pixel: weghalen, verschuiven, tint uit het r5-palet.
# 1 brein: r8-windingen (natief raster natief_r8_5.png) geschaald naar het r5-hoofd, 1 px in de donkerste zandtint (idx 2)
# 2 gezicht rechts: schaduw als sikkel langs de rand  3 ogen: Gen 3-ogen pixel voor pixel  4/5/6 hand, randen, linkerarm.
import numpy as np; from PIL import Image; import schoon
R5=np.asarray(Image.open('r5/zandloper_fase3.png')).astype(int)
PAL=Image.open('r5/zandloper_fase3.png').getpalette()
T,ZW,S0,S1,S2,S3,S4,WIT=0,1,2,3,4,5,6,14          # idx: transparant, zwart, zand donker..licht, oogwit
ZAND=(S1,S2,S3,S4)
LOG={}
def log(k,v): LOG.setdefault(k,[]).extend(v if isinstance(v,list) else [v])
def zet(A,p,v,k):
    if A[p]!=v: log(k,[(p,int(A[p]),v)]); A[p]=v
# hoofdmasker van r5 (maak_r5.basis, opgeslagen omdat basis() de hele r4-keten draait)
try: H=np.load('r6/H.npy')
except FileNotFoundError:
    import maak_r5; H=maak_r5.basis()[1]; np.save('r6/H.npy',H)
def binnen(p): return H[p] and all(H[p[0]+dy,p[1]+dx] for dy,dx in schoon.N4)
def zandbuur(A,p,uit=()):
    c={}
    for dy,dx in schoon.N8:
        q=(p[0]+dy,p[1]+dx)
        if A[q] in ZAND and q not in uit: c[A[q]]=c.get(A[q],0)+1
    return max(c,key=c.get) if c else S2
# ---------- 1 brein ----------
R8=np.asarray(Image.open('natief_r8_5.png').convert('RGB')).astype(float); L8=R8@[.299,.587,.114]
def r8_comps():
    m=(L8<150)&(L8>45); z=np.zeros_like(m); z[38:54,80:116]=True
    return sorted(schoon.comps(m&z),key=len,reverse=True)
# A = linker "(" (alleen het binnenstuk; het buitenstuk van comp A is de r8-hoofdomtrek), B = middelste groeve,
# C+G = spiraal, D(+E) = rechter boog. Alles in natieve r8-coördinaten, zoals het model ze heeft.
def windingen():
    cs=r8_comps(); A,B,C,D,E,F,G,Hh=cs[:8]
    Ain=[(y,x) for y,x in A if (y>=42 and x>=83 and not (y>=45 and x<=82)) and not (y==45 and x<=84 and x>=82)]
    return {'A':Ain,'B':B,'C':C+G,'D':D}
# Windingen per pixel: posities = r8-componenten via naar_sprite (schaal 0,52, zie rapport), daarna alleen
# verschoven tot één doorlopende 1-px-lijn (8-samenhangend, geen 4-hoekjes).
SCH,Y0=0.52,7.6
def naar_sprite(pix):
    return {(int(np.floor(Y0+(y-38+0.5)*SCH)),int(np.floor(29.5+(x-98+0.5)*SCH))) for y,x in pix}
WIND={'A':[(9,25),(10,24),(11,23),(12,23),(13,24)],                       # linker "(" (r8 comp A, binnenstuk)
      'B':[(7,29),(8,28),(9,27),(10,26),(11,26),(12,25)],                # middelste groeve (r8 comp B; onderste 2 px weg, raakten de wenkbrauw)
      'C':[(12,29),(11,29),(10,30),(10,31),(10,32),(11,33),(12,32)],        # spiraal (r8 comp C + haakje G)
      'D':[(11,35),(12,35),(12,34)]}                                        # rechter boog (r8 comp D, 1 px omhoog; onderste px naast de wenkbrauw 1 px opgeschoven)
KRUL_R5=[(8,27),(9,27),(9,34),(9,35),(10,26),(10,33),(10,36),(11,26),(11,32),(11,37),(12,25)]
def brein(A,keuze):
    for p in KRUL_R5:
        if A[p]==S0: zet(A,p,zandbuur(A,p,set(KRUL_R5)),'r5-krul weg')
    for k in keuze:
        for p in WIND[k]:
            assert binnen(p),p
            zet(A,p,S0,'winding r8 '+k)
    return A
# ---------- 2 schaduw rechts als sikkel ----------
def afstand_rand(p):
    for d in range(1,6):
        for dy in range(-d,d+1):
            for dx in range(-d,d+1):
                q=(p[0]+dy,p[1]+dx)
                if not H[q]: return d
    return 6
def gezicht(A):
    for y in range(13,22):
        for x in range(29,40):
            p=(y,x)
            if not H[p] or A[p] not in (S1,S2): continue
            d=afstand_rand(p)
            zet(A,p,S1 if d<=3 else S2,'gezicht sikkel (tint)')
    return A
# ---------- 3 ogen ----------
GEN3='../../../../../../graphics/pokemon/%s/anim_front_gba.png'
OGEN={  # naam: (links-box, rechts-box, {bronindex: 'w'/'p'}) ; box = (y0,x0,y1,x1) inclusief
 'machoke':   ((17,23,20,24),(17,33,20,35),{1:'w',10:'w',8:'p',9:'p'}),
 'granbull':  ((14,24,15,27),(14,29,15,32),{15:'w',11:'p',9:'p',10:'p'}),
 'hitmonchan':((19,26,22,28),(20,32,23,37),{1:'w',15:'p'}),
 'machop':    ((19,23,23,23),(19,30,23,32),{1:'w',10:'w',7:'p',8:'p',9:'p'}),
}
DOEL={'L':(17.5,23.5),'R':(17.5,30.0)}
def oog_pixels(naam):
    a=np.asarray(Image.open(GEN3%naam))[:64]; bl,br,mp=OGEN[naam]; uit={}
    for kant,(y0,x0,y1,x1) in (('L',bl),('R',br)):
        px=[(y,x,mp[int(a[y,x])]) for y in range(y0,y1+1) for x in range(x0,x1+1) if int(a[y,x]) in mp]
        cy=np.mean([p[0] for p in px]); cx=np.mean([p[1] for p in px])
        ty,tx=DOEL[kant]; dy=int(round(ty-cy)); dx=int(round(tx-cx))
        uit[kant]=[(y+dy,x+dx,k) for y,x,k in px]
    return uit
OOGZONE=[(y,x) for y in range(15,20) for x in range(20,34)]
BROW_R5=[(15,22),(15,23),(16,24),(15,31),(15,32),(16,30)]
def ogen(A,naam):
    # r5-ogen (oogwit + pupil) en r5-wenkbrauwen weg -> lichte zandtint; wenkbrauwen worden daarna verschoven
    for p in OOGZONE:
        if A[p] in (WIT,ZW) and binnen(p): zet(A,p,S3,'r5-oog weg')
    for p in BROW_R5:
        if A[p]==S0: zet(A,p,S3,'r5-wenkbrauw weg (wordt verschoven)')
    o=oog_pixels(naam); gez=[]
    for kant in 'LR':
        for y,x,k in o[kant]: zet(A,(y,x),WIT if k=='w' else ZW,'oog %s'%naam); gez.append((y,x))
    g=set(gez)
    # vrij in lichte zandtint: zandpixels direct rond het oog
    for y,x in gez:                                   # alleen de 4-buren: geen lichte band over het gezicht
        for dy,dx in schoon.N4:
            q=(y+dy,x+dx)
            if q not in g and A[q] in (S1,S2) and binnen(q): zet(A,q,S3,'oog vrij (tint)')
    # wenkbrauwen (de r5-pixels, verschoven): kort en schuin boven het eigen oog, binnenkant laag (boos)
    for kant in 'LR':
        ys=[p[0] for p in o[kant]]; xs=[p[1] for p in o[kant]]; t=min(ys); x0,x1=min(xs),max(xs)
        if kant=='L': br=[(t-2,x0-1),(t-2,x0),(t-1,x1+ (0 if x1>x0 else 1))]
        else:         br=[(t-1,x0- (0 if x1>x0 else 1)),(t-2,x1),(t-2,x1+1)]
        for p in br: zet(A,p,S0,'wenkbrauw verschoven')
    return A
WINDSET=set()
# ---------- 6 linkerarm sluit aan op de schouder; 5 randen: selout aan de lichtkant ----------
def linkerarm(A):
    zet(A,(16,14),T,'arm: uitsteeksel rand weg')         # rand rij 16 springt 2 px uit
    zet(A,(16,15),S0,'arm: rand (selout)')
    zet(A,(17,16),S0,'arm: rand verschoven (17,17)->(17,16)')
    zet(A,(17,17),S3,'arm: rand verschoven (17,17)->(17,16)')
    return A
def selout_links(A):
    """Linker buitenrand (lichtkant, rij 16-30): zwart -> selout (S0), zodat zwart en selout niet om en om staan."""
    for y in range(16,31):
        xs=[x for x in range(0,24) if A[y,x]!=T]
        if not xs: continue
        p=(y,xs[0])
        if A[p]==ZW: zet(A,p,S0,'selout links (tint)')
    return A
# ---------- 4/5 handen en kleine dingen: vlekjes van 1-2 px weg (buurtint), losse binnenlijnstukjes van 1-2 px weg ----------
def vlekjes(A,zone,minpx=3,beschermd=()):
    y0,x0,y1,x1=zone; Z=np.zeros((64,64),bool); Z[y0:y1+1,x0:x1+1]=True
    for p in beschermd: Z[p]=False
    for t in ZAND:
        for c in schoon.comps4((A==t)&Z):
            if len(c)>=minpx: continue
            s=set(c)
            for p in c:
                n=zandbuur(A,p,s)
                if n!=t: zet(A,p,n,'vlekje %d px (tint)'%len(c))
    for c in schoon.comps((A==S0)&Z):
        if len(c)>=minpx: continue
        if any(A[p[0]+dy,p[1]+dx] in (T,ZW) or 7<=A[p[0]+dy,p[1]+dx]<=13 for p in c for dy,dx in schoon.N8): continue   # aan rand/glas/hout: lijn blijft
        s=set(c)
        for p in c: zet(A,p,zandbuur(A,p,s),'los lijnstukje %d px weg'%len(c))
    return A
