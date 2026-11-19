# Kuifslierten: middenlijn gemeten op het model (lijnkaart _ov_model.png, 24 px per spritecel), als polylijn in
# spritecoordinaten (x,y), fijn bemonsterd -> cellen -> verdunnen -> L-hoekjes weg. Krul en haakje zitten in de punten.
import numpy as np
# r2: opnieuw gemeten op lijnkaarten van 40 px per spritecel (_tmp/ovA.png, ovB.png); krul en haakje apart in repareer.py
U=[(17.2,6.2),(17.75,5.4),(18.75,4.25),(19.75,3.5),(20.75,2.9),(21.75,2.4),(22.75,2.0),(24,1.5),(25,1.25),(26,1.1),(28,1.1),
   (30,1.1),(31.5,1.25),(33,1.6),(34.5,2.1),(35.75,2.75),(36.75,3.4),(37.75,4.0),(38.75,4.6),(39.5,5.25),(40.5,6.0),(41.5,6.6),
   (42.5,6.8),(44.9,6.8)]
L=[(23.2,5.4),(24.5,4.75),(25.5,4.5),(26.5,4.25),(27.5,4.0),(29,3.9),(31.4,3.95),(33.5,4.1),(35,4.5),(36.5,4.9),(37.5,5.25),
   (38.5,5.75),(39.25,6.25),(39.9,7.0)]
def cells(P):
    s=set()
    for (x0,y0),(x1,y1) in zip(P,P[1:]):
        for t in np.linspace(0,1,40): s.add((int(y0+(y1-y0)*t),int(x0+(x1-x0)*t)))
    return s
def pp(S):  # pixel-perfect: verwijder hoekpixel waarvan de twee 4-buren elkaar diagonaal raken en die precies 2 buren heeft
    S=set(S); ch=True
    while ch:
        ch=False
        for (y,x) in sorted(S):
            nb=[(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (y+dy,x+dx) in S]
            if len(nb)!=2: continue
            a,b=nb
            if abs(a[0]-b[0])==1 and abs(a[1]-b[1])==1 and (a[0]==y or a[1]==x) and (b[0]==y or b[1]==x):
                S.discard((y,x)); ch=True; break
    return S
if __name__=='__main__':
    for n,P in (('U',U),('L',L)):
        S=pp(cells(P)); print(n,len(S))
        np.save('_kuif_%s.npy'%n,np.array(sorted(S)))
