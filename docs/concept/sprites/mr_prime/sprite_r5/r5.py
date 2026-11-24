# r5: bouwt mr_prime vanaf basis.npy (r4-keten ongewijzigd tot en met stap1_basis).
# Alles uit bestaande pixels: model r9 (natief raster / reductie), Mr. Rime front.png, of pixels van de sprite zelf
# verschoven/gespiegeld/omgekleurd. Tonen (index): 0=lijn 1..6 grijs, 7=wit (palet in palet.py).
import numpy as np; from PIL import Image
import hoed, opschoon, r3post
G='../../../../../graphics/pokemon/%s/%s.png'
RIME=np.asarray(Image.open(G%('mr_rime','front'))).astype(int)
MAGN=np.asarray(Image.open(G%('magnemite','anim_front_gba'))).astype(int)
EXTRA=2          # rijen voorhoofd erbij (hoed + haar 2 rijen omhoog)
DXV=7            # verre oog: Rime x22-25 -> x29-32 (1 witte kolom tot de kopomtrek)
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
    # 5. verre oog: Rime-linkeroog x22-25 rijen 17-21 -> x28-31 rijen 16-20 (rij 22 valt onder de snor)
    for y in range(17,22):
        for x in range(22,26):
            t=omk(y,x)
            if t is not None: zet(y-1,x+DXV,t,'Rime-oog ver')
    # 6. neus (r4): wit bolletje + modelselout
    for (y,x) in ((20,33),(20,34)): zet(y,x,7,'neus wit (r4)')
    for (y,x) in ((19,33),(19,34),(20,32),(20,35)): zet(y,x,4,'neus selout (r4)')
    return C
def hoed_haar(C,log):
    hoed.DY=1-EXTRA-2   # r4: -1; nu EXTRA hoger
    return hoed.variant(C,'A',log)
def kop_rechts(C,log):
    """Kop rechtsboven rond: per rij (13-19) de rechterrand van het gezicht (laatste 2 pixels) naar rechts geschoven tot de
    gespiegelde linkeromtrek (as tussen linkerrand x27 en rechterrand x47 van rij 20 = modelomtrek); tussenruimte =
    kopie van de witte gezichtspixel ernaast. Geen pixels getekend, alleen verschoven/gekopieerd."""
    C=C.copy()
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    for y in range(13,20):
        xl=min(x for x in range(20,40) if C[y,x] in (4,5,6,7) and x>=27)
        xr=max(x for x in range(30,52) if C[y,x] in (4,5,6,7) and (C[y,x+1]==-1 or C[y,x+1] in (0,1,3)) and x<=47)
        doel=27+47-xl
        if doel<=xr: continue
        seg=[C[y,xr-1],C[y,xr]]; wit=C[y,xr-2] if C[y,xr-2]==7 else 7
        for x in range(xr-1,doel-1): zet(y,x,wit,'kop rechts: wit doorgetrokken')
        zet(y,doel-1,seg[0],'kop rechts: randpixels verschoven'); zet(y,doel,seg[1],'kop rechts: randpixels verschoven')
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
    C=bouw(log); C=hoed_haar(C,log); C=kop_rechts(C,log); C,_=snor_top(C,log)
    C=opschoon.schoon(C,log); C=r3post.post(C,log)
    C,S=stok5.toepassen(C,log); C=palet.omzetten(C,S,log); C=palet.volume(C,log)
    return C
if __name__=='__main__':
    log={}; C=maak('A',log); print(log); np.save('r5_stap.npy',C)
