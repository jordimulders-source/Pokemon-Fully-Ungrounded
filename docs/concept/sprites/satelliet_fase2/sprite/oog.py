# Oog: ringbewuste bemonstering van het model (de ringen van het model zijn concentrisch; een blokreductie maakt ze kapot).
# Ringen op hele pixels rond het gemeten oogmidden (model 340,492.5 = sprite 20,2/24,0 -> 20,0/24,0), diameters naar het model:
# pupil 2 (model 2,5) | iris 4 (4,9) | donkere ring 6 (6,9) | paarse ring 8 (9,7) | omlijning 10 (10,5) | witte ring 12 (12,4).
# Kleur per pixel = meest voorkomende modelklasse in dezelfde modelband binnen +-30 graden van de pixelhoek (alleen klassen van die ring).
# Glans = pixel met het zwaartepunt van de modelglans (sprite 21,2/22,7).
import numpy as np, sys
k=np.load('klassen2.npy'); s=14.5625
CX,CY=20.0,24.0
DK=0.22  # drempel donkere lijn buiten de lensboog
# lensboog (donkere boog rond de witte lensring, rechterkant): cirkel gefit op 20 gemeten modelpunten (straal per hoek, zie verslag)
C2=(20.60,24.30,7.23)
# buitenste lensboog (zwart), cirkel gefit op 11 gemeten modelpunten, alleen het gemeten hoekbereik
C3=(23.09,24.75,6.57)
boog=[];boog3=[]
WIN=50   # hoekvenster (graden); r1: 30 gaf flikkerende tinten in de ringen
R=[1.25,2.35,3.25,4.3,5.35,6.3]   # pixelstralen (middelpunt-afstand) voor de 6 ringen
MB=[(0,1.25),(1.25,2.45),(2.45,3.45),(3.45,4.85),(4.85,5.25),(5.25,6.2)]
KL=[[9],[12,13,14],[9,8,15,14],[6,7,8],[1],[2,3,4]]
yy,xx=np.mgrid[0:1024,0:1024]; mr=np.hypot(xx-340,yy-492.5)/s; ma=np.degrees(np.arctan2(yy-492.5,xx-340))
def eye(o):
    o=o.copy()
    for j in range(16,33):
        for i in range(12,30):
            d=np.hypot(i+.5-CX,j+.5-CY); b=sum(d>=x for x in R)
            if b>=6: continue
            if len(KL[b])==1: o[j,i]=KL[b][0]; continue
            a=np.degrees(np.arctan2(j+.5-CY,i+.5-CX)); da=np.abs((ma-a+180)%360-180)
            m=(mr>=MB[b][0])&(mr<MB[b][1])&(da<=(25 if b==1 else WIN))   # iris: smaller venster zodat de lichte bovenkant (12) blijft
            c=np.bincount(k[m],minlength=16); o[j,i]=KL[b][int(np.argmax(c[KL[b]]))]
    o[22,21]=2
    # lenshuis (ringen rond de irisschijf, dunner dan 1 spritepx): donkere lijn als donker (1/8/9) >= 0,22 van het blok,
    # anders meest voorkomende lichte/paarse klasse. Alleen buiten de irisschijf, binnen 9,5 px, niet in het kleine paneel.
    X0,Y0=46,143
    for j in range(12,36):
        for i in range(10,34):
            d=np.hypot(i+.5-CX,j+.5-CY)
            if d<R[5] or d>10.6: continue
            y0,y1=int(round(Y0+j*s)),int(round(Y0+(j+1)*s)); x0,x1=int(round(X0+i*s)),int(round(X0+(i+1)*s))
            b=k[y0:y1,x0:x1].ravel(); c=np.bincount(b,minlength=16)/b.size
            if c[0]>=0.5 or c[[15,10]].sum()>0.3 or c[[9]].sum()>0.5: continue   # achtergrond / klein paneel
            if c[[11]].sum()>0.2: continue
            dk=c[1]+c[8]+c[9]
            d2=np.hypot(i+.5-C2[0],j+.5-C2[1]); a2=np.degrees(np.arctan2(j+.5-C2[1],i+.5-C2[0]))
            if abs(d2-C2[2])<=0.5 and -125<=a2<=115:
                o[j,i]=8; boog.append((i,j+7)); continue   # boog in een kleur (r3: zwart/donkerpaars wisselde)
            d3=np.hypot(i+.5-C3[0],j+.5-C3[1]); a3=np.degrees(np.arctan2(j+.5-C3[1],i+.5-C3[0]))
            if abs(d3-C3[2])<=0.55 and -61<=a3<=79 and d2>C2[2]+0.5:
                o[j,i]=1; boog3.append((i,j+7)); continue
            if d2<C2[2]+1.5 and -125<=a2<=115: dk=0      # tussen witte ring en boog / band erbuiten: geen losse donkere pixels
            if dk>=DK: o[j,i]=1 if c[1]>=c[8]+c[9] else 8
            else:
                q=[2,3,4,5,6,7]; o[j,i]=q[int(np.argmax(c[q]))]
    return o
if __name__=='__main__':
    o=np.load(sys.argv[1]); np.save(sys.argv[2],eye(o))
