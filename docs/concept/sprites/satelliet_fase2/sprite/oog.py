# Oog: ringbewuste bemonstering van het model (de ringen van het model zijn concentrisch; een blokreductie maakt ze kapot).
# Ringen op hele pixels rond het gemeten oogmidden (model 340,492.5 = sprite 20,2/24,0 -> 20,0/24,0), diameters naar het model:
# pupil 2 (model 2,5) | iris 4 (4,9) | donkere ring 6 (6,9) | paarse ring 8 (9,7) | omlijning 10 (10,5) | witte ring 12 (12,4).
# Kleur per pixel = meest voorkomende modelklasse in dezelfde modelband binnen +-30 graden van de pixelhoek (alleen klassen van die ring).
# Glans = pixel met het zwaartepunt van de modelglans (sprite 21,2/22,7).
import numpy as np, sys, os
from cfg import T, F, X0 as GX0, Y0 as GY0, s as GS, TOP, MODEL
k=np.load('klassen2.npy'); s=14.5625          # s hier = oude eenheid voor de modelbanden MB (modelgeometrie, schaalt niet)
OUD=MODEL.endswith('/model.png')
VAR=os.environ.get('SAT_OOG','a')              # r5: a = alle ringen (model), b = donkere ring tussen iris en paars weg
if OUD: CX,CY=20.0,24.0
else:
    from cfg import EYE; CX,CY=EYE[0],EYE[1]   # r5: gemeten oogmidden, afgerond op een pixelhoek (even diameters)
DK=0.22  # drempel donkere lijn buiten de lensboog
# lensboog (donkere boog rond de witte lensring, rechterkant): cirkel gefit op 20 gemeten modelpunten (straal per hoek, zie verslag)
C2=(20.60,24.30,7.23)
if not OUD: C2=(*T(C2[0],C2[1]),C2[2]*F)
# buitenste lensboog (zwart), cirkel gefit op 11 gemeten modelpunten, alleen het gemeten hoekbereik
C3=(23.09,24.75,6.57)
if not OUD: C3=(*T(C3[0],C3[1]),C3[2]*F)
boog=[];boog3=[]
WIN=50   # hoekvenster (graden); r1: 30 gaf flikkerende tinten in de ringen
R=[1.25,2.0,3.25,4.3,5.35,6.3]   # r4: iris-buitenstraal 2,35 -> 2,0: hoekpixels van de 4x4 naar de donkere ring (ronde iris)   # pixelstralen (middelpunt-afstand) voor de 6 ringen
MB=[(0,1.25),(1.25,2.45),(2.45,3.45),(3.45,4.85),(4.85,5.25),(5.25,6.2)]
KL=[[9],[12,13,14],[9,8,15,14],[6,7,8],[1],[2,3,4]]
if not OUD:
    # r5: ronde pixelschijven met even diameters: pupil 2 | iris 6 | donkere ring 8 | paars 10 | omlijning 12 | wit 14
    # (model x F = 2,7 | 5,4 | 7,6 | 10,7 | 11,5 | 13,6 bij 85 %; 2,9 | 5,8 | 8,1 | 11,4 | 12,3 | 14,6 bij 75 %)
    R=[1.25,3.0,4.0,5.0,6.0,7.0]
    if VAR=='b':   # donkere ring weg: paars wordt 2 px (binnen = binnenhelft modelband, buiten = buitenhelft)
        MB=[(0,1.25),(1.25,2.45),(3.45,4.15),(4.15,4.85),(4.85,5.25),(5.25,6.2)]
        KL=[[9],[12,13,14],[6,7,8],[6,7,8],[1],[2,3,4]]
yy,xx=np.mgrid[0:1024,0:1024]; mr=np.hypot(xx-340,yy-492.5)/s; ma=np.degrees(np.arctan2(yy-492.5,xx-340))
def eye(o):
    o=o.copy()
    for j in range(o.shape[0]):
        for i in range(o.shape[1]):
            d=np.hypot(i+.5-CX,j+.5-CY); b=sum(d>=x for x in R)
            if b>=6: continue
            if len(KL[b])==1: o[j,i]=KL[b][0]; continue
            a=np.degrees(np.arctan2(j+.5-CY,i+.5-CX)); da=np.abs((ma-a+180)%360-180)
            m=(mr>=MB[b][0])&(mr<MB[b][1])&(da<=(25 if b==1 else WIN))   # iris: smaller venster zodat de lichte bovenkant (12) blijft
            c=np.bincount(k[m],minlength=16); o[j,i]=KL[b][int(np.argmax(c[KL[b]]))]
    if OUD:
        o[22,19]=12  # r4: lichte iristint bovenaan, gemeten: modelsector -90 graden is 12 (147) > 3 (105) > 13
        o[22,20]=2   # r4: glans op de dichtstbijzijnde irispixel bij het modelzwaartepunt (21,2/22,7); (21,22) is nu donkere ring
    else:
        # r5: glans = irispixel het dichtst bij het zwaartepunt van de modelglans (354,8/474,1);
        #     lichte iristint (12) = irispixel het dichtst bij het zwaartepunt van de lichtturquoise modelpixels in de iris
        iris=[(j,i) for j in range(o.shape[0]) for i in range(o.shape[1]) if R[0]<=np.hypot(i+.5-CX,j+.5-CY)<R[1]]
        tosp=lambda x,y:((x-GX0)/GS,(y-GY0)/GS)
        gx,gy=tosp(354.8,474.1); g=min(iris,key=lambda p:np.hypot(p[1]+.5-gx,p[0]+.5-gy)); o[g]=2
        m12=(k==12)&(np.hypot(xx-340,yy-492.5)<45); ly,lx=np.where(m12); lx,ly=tosp(lx.mean(),ly.mean())
        l=min([p for p in iris if p!=g],key=lambda p:np.hypot(p[1]+.5-lx,p[0]+.5-ly)); o[l]=12
        print('oog: midden',CX,CY,'glans',g[1],g[0]+TOP,'licht',l[1],l[0]+TOP,'variant',VAR)
    # lenshuis (ringen rond de irisschijf, dunner dan 1 spritepx): donkere lijn als donker (1/8/9) >= 0,22 van het blok,
    # anders meest voorkomende lichte/paarse klasse. Alleen buiten de irisschijf, binnen 9,5 px, niet in het kleine paneel.
    from cfg import blok
    for j in range(o.shape[0]):
        for i in range(o.shape[1]):
            d=np.hypot(i+.5-CX,j+.5-CY)
            if d<R[5] or d>10.6*F: continue
            y0,y1,x0,x1=blok(j,i)
            b=k[y0:y1,x0:x1].ravel(); c=np.bincount(b,minlength=16)/b.size
            if c[0]>=0.5 or c[[15,10]].sum()>0.3 or c[[9]].sum()>0.5: continue   # achtergrond / klein paneel
            if c[[11]].sum()>0.2: continue
            dk=c[1]+c[8]+c[9]
            d2=np.hypot(i+.5-C2[0],j+.5-C2[1]); a2=np.degrees(np.arctan2(j+.5-C2[1],i+.5-C2[0]))
            if abs(d2-C2[2])<=0.5 and -125<=a2<=115:
                o[j,i]=8; boog.append((i,j+TOP)); continue   # boog in een kleur (r3: zwart/donkerpaars wisselde)
            d3=np.hypot(i+.5-C3[0],j+.5-C3[1]); a3=np.degrees(np.arctan2(j+.5-C3[1],i+.5-C3[0]))
            if abs(d3-C3[2])<=0.55 and -61<=a3<=79 and d2>C2[2]+0.5:
                o[j,i]=1; boog3.append((i,j+TOP)); continue
            if d2<C2[2]+1.5 and -125<=a2<=115: dk=0      # tussen witte ring en boog / band erbuiten: geen losse donkere pixels
            if dk>=DK: o[j,i]=1 if c[1]>=c[8]+c[9] else 8
            else:
                q=[2,3,4,5,6,7]; o[j,i]=q[int(np.argmax(c[q]))]
    return o
if __name__=='__main__':
    o=np.load(sys.argv[1]); np.save(sys.argv[2],eye(o))
