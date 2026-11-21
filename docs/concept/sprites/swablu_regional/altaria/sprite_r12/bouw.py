# Altaria r12: kop + hals van r11A als één laag 2 px naar rechts. Bouwen vanuit altaria/: python3 sprite_r12/bouw.py
# Jordi (21 nov): "a is perfect, zou je alleen het hele hoofd + nek 2 pixels naar rechts kunnen schuiven en mij dan een vergelijking kunnen laten zien?"
# K1: kuif blijft staan; K2: kuif schuift mee (2 px rechts). Pixels verplaatsen, niets hertekenen.
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'sprite_r12'); from laag import o, PALI, LAAG, KUIF, HALS, RAND, KOP
PU,WS,WN,WD,WT,WC,ST,VS,VD,VM,VL,VH,LW=range(1,14)
r9=np.array(Image.open('sprite_r9/altaria_r9.png')).astype(int)
WOLK=[WS,WN,WD,WT,WC,ST]; VUL=[WN,WD,WT,WC]
def schuif(m,dx=2):
    s=np.zeros_like(m); s[:,dx:]=m[:,:-dx]; return s
C='.KSndtcz=vmlhw'
def vul(o,vrij,laag):
    # vrijgekomen pixels: (1) r9 had daar wolk (die de r10/r11-kop bedekte) -> precies die bevroren r9-wolkpixel (selout = de randlijn die doorloopt);
    # (2) r9 had daar lucht -> lucht; (3) r9 had daar kop/hals of het was de halsrand -> de wolkband van de dichtstbijzijnde wolkpixel links in
    # dezelfde rij (geen selout, geen static)
    log=[]
    for Y,X in sorted(zip(*np.where(vrij))):
        if r9[Y,X] in WOLK and not RAND[Y,X]: v=r9[Y,X]; w='r9-wolk'
        elif r9[Y,X]==0: v=0; w='r9-lucht'
        else:
            # eerste niet-laagpixel links (in het nieuwe beeld): lucht -> lucht; wolkvultint -> die band; selout van de vleugelrand
            # (kop-rijen <= 29) -> lucht (de vleugel houdt zijn eigen rand, geen dubbele lijn); halsrijen: verder naar links tot een vultint
            x=X-1
            while laag[Y,x] and not vrij[Y,x]: x-=1
            t=o[Y,x]
            if t==0 or (t==WS and Y<=29): v=0; w='lucht (links (%d,%d) = %s)'%(x,Y,C[t])
            else:
                while o[Y,x] not in VUL: x-=1
                v=o[Y,x]; w='band links (%d,%d)'%(x,Y)
        o[Y,X]=v; log.append((int(X),int(Y),C[v],w))
    return log
def maak(kuifmee):
    L=LAAG|(KUIF if kuifmee else np.zeros_like(LAAG))
    n=o.copy(); SL=schuif(L)
    vrij=L&~SL
    log=vul(n,vrij,L)
    n[SL]=schuif(np.where(L,o,0))[SL]
    # diff 0 buiten de laag, de vrijgekomen pixels en de nieuwe plek van de laag
    assert ((n!=o)&~(vrij|SL)).sum()==0
    return n,log,vrij,SL
def opslaan(a,p):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PALI); im.save(p,transparency=0)
PAL=[tuple(PALI[3*k:3*k+3]) for k in range(14)]
if __name__=='__main__':
    for naam,mee in (('K1',False),('K2',True)):
        n,log,vrij,SL=maak(mee)
        opslaan(n,'sprite_r12/altaria_r12_%s.png'%naam)
        rgb=np.array(PAL,'uint8')[n]; rgb[n==0]=255
        Image.fromarray(rgb).resize((512,512),Image.NEAREST).save('sprite_r12/altaria_r12_%s_8x.png'%naam)
        print(naam,'diff met r11A:',int((n!=o).sum()),'| vulpixels',len(log),'| kleuren',len(set(n.ravel())),'| pupillen',int((n==PU).sum()))
        for l in log: print('  ',l)
