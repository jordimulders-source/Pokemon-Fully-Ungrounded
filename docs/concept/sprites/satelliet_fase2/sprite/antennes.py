# Antennes en staafje: in het model 1,4 spritepx dik (20 modelpx) -> blokreductie geeft ruis. Hier op de GEMETEN middenlijn
# (per modelkolom het midden van de staaf, zie meetuitvoer in het verslag) als 2 px verticale streep: kern (modelkleur van de staaf)
# boven, omlijning eronder. Bolletjes: pixels binnen de gemeten straal rond het gemeten middelpunt (afstandstransformatie).
import numpy as np, sys
# middenlijnen in spritecoordinaten (x, y), gemeten op het model
L=[(25.68,8.48),(26.64,7.59),(27.61,6.70),(28.57,5.60),(29.53,4.64),(30.49,3.88),(31.45,3.16),(32.41,2.64),(33.37,1.75)]
R=[(31.52,8.17),(32.48,7.62),(33.44,7.04),(34.40,6.35),(35.36,5.97),(36.33,5.29),(37.29,4.77),(38.25,4.53),(39.21,4.09),
   (40.17,3.85),(41.13,3.67),(42.09,3.33),(43.06,3.33),(44.02,3.16),(44.50,3.16)]
S=[(39.76,10.71),(40.72,10.37),(41.68,9.99),(42.64,9.65),(43.61,9.68),(44.57,9.51)]
# bollen: middelpunt, straal (incl. omlijning, gemeten), vulkleur, glans. A/B = antennebolletjes, J = kogelgewrichten
BALLS=[((34.78,1.41),1.33,8,7),((46.56,2.95),1.58,7,6)]
JOINTS=[((29.84,10.16),2.06,7,6),((38.08,12.53),1.5,7,6)]
def yc(P,x):
    xs=[p[0] for p in P]; ys=[p[1] for p in P]; return np.interp(x,xs,ys)
def rods(o,Zs):
    o=o.copy()
    H,W=o.shape
    # 1) wissen: alles van de blokreductie binnen 1,8 px van een staaf/bol (buiten paneel/lijf/gewricht-zone Zs)
    for j in range(0,12):
        for i in range(24,50):
            if Zs[j,i]: continue
            x=i+.5; y=j+.5; d=9
            for P in (L,R,S):
                if P[0][0]-0.5<=x<=P[-1][0]+0.5: d=min(d,abs(yc(P,x)-y))
            for (cx,cy),r,_,_ in BALLS: d=min(d,np.hypot(x-cx,y-cy)-r+0.6)
            if d<1.8: o[j,i]=0
    # 2) staven: per kolom 2 px: rij round(yc-1) = kern, rij eronder = omlijning
    for P,core in ((L,8),(R,7),(S,7)):
        for i in range(int(np.floor(P[0][0])),int(np.ceil(P[-1][0]))):
            x=i+.5
            if not (P[0][0]-0.3<=x<=P[-1][0]+0.3): continue
            r=int(round(yc(P,x)-1))
            for jj,v in ((r,core),(r+1,1)):
                if not Zs[jj,i]: o[jj,i]=v
    # 3) bollen: rand aan de schaduwkant (rechtsonder van het middelpunt) zwart, aan de lichtkant donkerpaars (gekleurde selout),
    #    binnen vulkleur, glans op de binnenpixel linksboven (herbelicht: model heeft de glans rechtsboven, gespiegeld)
    for (cx,cy),rad,col,gl in BALLS+JOINTS:
        pix=[(j,i) for j in range(0,16) for i in range(24,50) if np.hypot(i+.5-cx,j+.5-cy)<=rad+0.25]
        S_=set(pix)
        binnen=[p for p in pix if all(q in S_ for q in ((p[0]-1,p[1]),(p[0]+1,p[1]),(p[0],p[1]-1),(p[0],p[1]+1)))]
        for j,i in pix:
            if (j,i) in binnen: o[j,i]=col
            else: o[j,i]=1 if (i+.5-cx)+(j+.5-cy)>-0.3 else 8
        if binnen:
            lo=min(binnen,key=lambda p:p[0]+p[1]); o[lo]=gl
    return o
