# r6 (op r5): bouwt mr_prime vanaf basis.npy (r4-keten ongewijzigd tot en met stap1_basis).
# Alles uit bestaande pixels: model r9 (natief raster / reductie), Mr. Rime front.png, of pixels van de sprite zelf
# verschoven/gespiegeld/omgekleurd. Tonen (index): 0=lijn 1..6 grijs, 7=wit (palet in palet.py).
import numpy as np; from PIL import Image
import hoed, opschoon, r3post
G='../../../../../graphics/pokemon/%s/%s.png'
RIME=np.asarray(Image.open(G%('mr_rime','front'))).astype(int)
MAGN=np.asarray(Image.open(G%('magnemite','anim_front_gba'))).astype(int)
EXTRA=2          # rijen voorhoofd erbij (hoed + haar 2 rijen omhoog)
DXV=7            # verre oog: Rime x23-25 -> x30-32 (r6: 2 witte kolommen tot de kopomtrek)
OOGVAR='B'       # omkleuring Rime-oog (zie RIME_OOG)
# Rime-oog omkleuren: a=wit, 7=oranje irisring, b=geel binnenring, 6=lichtblauw (bovenkant oogwit), 8=rood (rechterrand oog)
RIME_OOG={'A':{0xa:7,7:2,0xb:5,6:6,8:5,'mid':0},   # ring 64, binnenring 144, midden (Rime-glans) = pupil 16
          'B':{0xa:7,7:5,0xb:2,6:6,8:5,'mid':0},   # ring 144, binnenring 64, pupil 16
          'C':{0xa:7,7:2,0xb:0,6:6,8:5,'mid':7}}   # letterlijk: ring 64, geel -> pupil 16, glans wit
def bouw(log):
    C0=np.load('basis.npy'); C=C0.copy()
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    # 1. voorhoofd: kopkolommen (x>=26) rijen 0..15 EXTRA rijen omhoog, bovenste gezichtsrij (15) gedupliceerd
    for y in range(0,16):
        for x in range(26,64):
            v=C0[y+EXTRA,x] if y+EXTRA<=15 else C0[15,x]
            zet(y,x,v,'voorhoofd: modelrij 15 gedupliceerd (%d rijen)'%EXTRA)
    # 2. oogvlak leeg -> gezichtswit (rijen 13-20, binnen de kop)
    for y in range(12,21):
        for x in range(28,47):
            if C[y,x]!=-1 and not (y==20 and x<28): zet(y,x,7,'oogvlak leeg -> gezichtswit')
    # 3. monocle R1 (Magnemite-oogomtrek 7x7) 1 rij hoger dan r4: rijen 14-20, x36-42
    ring=[(y-29+14,x-30+36) for y in range(29,36) for x in range(30,37) if MAGN[y,x]==14]
    rs=set(ring)
    for (y,x) in ring: zet(y,x,2,'monocle R1 (Magnemite-omtrek)')
    binnen=set()
    for y in range(14,21):
        xs=[x for x in range(30,48) if (y,x) in rs]
        if len(xs)>=2: binnen|={(y,x) for x in range(min(xs)+1,max(xs)) if (y,x) not in rs}
    K=RIME_OOG[OOGVAR]
    def omk(y,x):
        v=RIME[y,x]
        if v==0xa and RIME[y-1,x]==0xb and RIME[y+1,x]==0xb: return K['mid']
        return K.get(v)
    # 4. nabije oog: Rime-rechteroog x30-34 rijen 16-20 -> x37-41 rijen 15-19 (binnen de ring), 1-op-1
    for y in range(16,21):
        for x in range(30,35):
            t=omk(y,x)
            if t is not None and (y-1,x+7) in binnen: zet(y-1,x+7,t,'Rime-oog nabij')
    # 5. verre oog: Rime-linkeroog x23-25 (r6: buitenste kolom x22 eraf, perspectief) rijen 17-21 -> x30-32 rijen 16-20
    for y in range(17,22):
        for x in range(23,26):
            t=omk(y,x)
            if t is not None: zet(y-1,x+DXV,t,'Rime-oog ver')
    # 6. r6: r4-neusstreepje vervalt (oogvlak is al wit); neus komt na de snor (neus())
    return C
def neus(C,log):
    """Neus uit het model: cellen met >=2 natieve neusomlijningspixels (150<=L<235, buiten de oogringen) in de tint van
    het model (gemiddeld ~210 -> 200, de lichte modelselout); binnenkant blijft gezichtswit."""
    a=np.asarray(Image.open('natief.png').convert('L')).astype(int); C=C.copy(); cnt={}
    for y in range(62,71):
        for x in range(84,100):
            if ((x-82.5)**2+(y-62.5)**2)**.5<=7.5 or ((x-104)**2+(y-63)**2)**.5<=9: continue
            if 150<=a[y,x]<235:
                k=(int((y-17.5)//2.5),int((x-7)//2.5)); cnt[k]=cnt.get(k,0)+1
    for (y,x),n in cnt.items():
        if n>=2 and C[y,x]!=6: C[y,x]=6; log['neus: modelomlijning (tint 200)']=log.get('neus: modelomlijning (tint 200)',0)+1
    return C
def hoed_haar(C,log):
    hoed.DY=1-EXTRA-2   # r4: -1; nu EXTRA hoger
    return hoed.variant(C,'A',log)
KOP_C=(101.0,65.0,26.0)   # modelkop r9: midden (x,y) en straal tot de lichte rand (links x75, rechts x127 op ooghoogte)
def kop_vorm(C,log):
    """Kopomtrek links en rechts naar de r9-modelomtrek, per spritekolom: rijen >=18 (rechts) / >=16 (links) gemeten op het
    natieve raster (lichte kop tegen achtergrond); erboven (onder haar/hoedrand verborgen) de modelcirkel door die metingen,
    in de 2 voorhoofdrijen verticaal 2 rijen opgerekt (het voorhoofd volgt dezelfde boog). Nieuwe pixels = de randpixels
    van die rij verschoven, tussenruimte gezichtswit; wat buiten valt wordt transparant."""
    from bgmask import bgmask
    a=np.asarray(Image.open('natief.png').convert('L')).astype(int)
    bg=bgmask(np.asarray(Image.open('natief.png').convert('RGB')))
    cx,cy,R=KOP_C; C=C.copy(); doel={}
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    for r in range(13,25):
        ys=[y for y in range(len(a)) if 17.5+2.5*r<=y+0.5<20+2.5*r]
        def cirkel(sign):
            rc=(cy-17.5)/2.5; dy=(rc-(r+0.5))
            ry=R/2.5+(EXTRA if dy>0 else 0)
            h=(R/2.5)*np.sqrt(max(0,1-(dy/ry)**2))
            return (cx-7)/2.5+sign*h
        if r>=18:
            xs=[max([x for x in range(95,135) if a[y,x]>=150 and not bg[y,x]] or [None]) for y in ys]
            xs=[x for x in xs if x]; xr=(np.mean(xs)+1-7)/2.5 if xs else cirkel(1)
        else: xr=cirkel(1)
        if 16<=r<=20:
            xs=[min([x for x in range(66,95) if a[y,x]>=150 and not bg[y,x]] or [None]) for y in ys]
            xs=[x for x in xs if x]; xl=(np.mean(xs)-7)/2.5 if xs else cirkel(-1)
        elif r<16: xl=cirkel(-1)
        else: xl=None
        cmax=int(np.floor(xr-0.5)); cmin=int(np.ceil(xl-0.5)) if xl is not None else None
        doel[r]=(cmin,cmax)
        # rechts: laatste lichte gezichtspixel voor de lijn
        xr0=max(x for x in range(36,56) if C[r,x] in (4,5,6,7) and C[r,x+1] in (-1,0))
        seg=[C[r,xr0-1],C[r,xr0]]
        if cmax>xr0:
            for x in range(xr0-1,cmax-1): zet(r,x,7,'kop rond: gezichtswit doorgetrokken')
        else:
            for x in range(cmax+1,xr0+2): zet(r,x,-1,'kop rond: buiten de modelomtrek -> transparant')
        zet(r,cmax-1,seg[0],'kop rond: randpixels verschoven'); zet(r,cmax,seg[1],'kop rond: randpixels verschoven')
        zet(r,cmax+1,0,'kop rond: lijn rechts')
        if cmin is not None:
            xl0=min(x for x in range(20,34) if C[r,x] in (4,5,6,7))
            if cmin>xl0:
                for x in range(xl0,cmin): zet(r,x,-1,'kop rond: buiten de modelomtrek -> transparant')
            else:
                for x in range(cmin,xl0+1): zet(r,x,7,'kop rond: gezichtswit doorgetrokken')
    # rij 25 (onderlijn snor + kaak): model x116 -> lichte kop t/m kolom 43, lijn op 44; de snorlijn rechts daarvan (45-46) was
    # de rechthoekige hoek -> transparant
    xs=[max([x for x in range(95,135) if a[y,x]>=150 and not bg[y,x]] or [0]) for y in range(80,83)]
    cmax=int(np.floor((np.mean(xs)+1-7)/2.5-0.5)); doel[25]=(None,cmax)
    for x in range(cmax+2,50):
        if C[25,x]==0 and x<=47: zet(25,x,-1,'kop rond: kaakhoek rij 25 -> transparant')
    zet(25,cmax+1,0,'kop rond: lijn rechts')
    return C, doel
def selout_links(C,doel,log):
    """Linkerrand van de kop (rij 13-20, lichte kant) in de seloutkleur van het gezicht (4), zoals elders op de kop."""
    C=C.copy()
    for r,(cmin,_) in doel.items():
        if cmin is not None and C[r,cmin] in (5,6,7) and C[r,cmin]!=4:
            C[r,cmin]=4; log['kop rond: selout links (gezichtsselout)']=log.get('kop rond: selout links (gezichtsselout)',0)+1
    return C
def snor_top(C,log):
    """Bovenrand snor per kolom naar de modelrand (r9 natief: eerste zwarte pixel boven het snorgrijs, per spritekolom
    gemiddeld en afgerond; pupillen van de ringen eruit). Daling: bovenlijn 1 omlaag (erboven gezichtswit);
    stijging: kolomstuk rij 21-23 1 omhoog."""
    a=np.asarray(Image.open('natief.png').convert('L')).astype(int); C=C.copy()
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    tops={}
    for x in range(66,128):
        for y in range(66 if x<76 else 68,84):   # x>=76: boven rij 68 liggen de pupillen van de ringen
            if a[y,x]<60:
                seg=a[y:y+5,x]; ok=False
                for k in range(1,5):
                    if 45<=seg[k]<140: ok=True; break
                    if seg[k]>=140: break
                if ok: tops[x]=y; break
    doel={}
    for c in range(24,44):
        ys=[tops[x] for x in tops if 7+2.5*c<=x+0.5<9.5+2.5*c]
        if ys: doel[c]=int(np.floor((np.mean(ys)-17.5)/2.5+0.5))
    D=C.copy()
    for c,t in doel.items():
        if not 25<=c<=42: continue
        u=21
        if D[u,c] not in (0,4,6): continue   # alleen kolommen met de r4-bovenlijn (of neus-/seloutpixel) op rij 21
        if t==u+1 and D[u,c] in (0,6):
            zet(u,c,7,'snor: bovenrand 1 omlaag (modelrand)'); zet(u+1,c,0,'snor: bovenrand 1 omlaag (modelrand)')
        elif t==u-1 and D[u-1,c]==7:
            for y in range(u-1,23): zet(y,c,D[y+1,c],'snor: kolom 1 omhoog (modelrand)')
    return C, doel
def maak(oogvar='A',log=None):
    global OOGVAR
    OOGVAR=oogvar; log={} if log is None else log
    import stok5, palet
    C=bouw(log); C,doel=kop_vorm(C,log); C=hoed_haar(C,log); C,_=snor_top(C,log); C=neus(C,log)
    C=opschoon.schoon(C,log); C=r3post.post(C,log); C=selout_links(C,doel,log)
    print('kopomtrek (rij: links, rechts)',doel)
    C,S=stok5.toepassen(C,log); C=palet.omzetten(C,S,log); C=palet.volume(C,log)
    return C
if __name__=='__main__':
    log={}; C=maak('A',log); print(log); np.save('r5_stap.npy',C)
