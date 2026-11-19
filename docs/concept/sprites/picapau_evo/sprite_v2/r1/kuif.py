# Kuifslierten: middenlijn gemeten op het model (lijnkaart _ov_model.png, 24 px per spritecel), als polylijn in
# spritecoordinaten (x,y), fijn bemonsterd -> cellen -> verdunnen -> L-hoekjes weg. Krul en haakje zitten in de punten.
import numpy as np
U=[(16.4,6.4),(17.8,5.1),(19.3,4.1),(20.75,3.1),(22.4,2.3),(24.1,1.6),(24.5,1.3),(26.2,1.05),(28.7,1.0),(31.6,1.25),(33.7,1.6),(35.1,2.3),
   (36.6,3.1),(37.4,3.75),(38.2,4.8),(39.5,5.8),(40.75,6.5),(42,6.75),(43.7,6.7),(44.9,6.25),(46,5.4),(46.4,4.6),(46,3.9),
   (45.1,3.7),(44.4,4.2),(44.6,5.0)]
L=[(17,5.7),(19.5,5.5),(22.4,5.2),(24.5,4.7),(26.2,4.5),(28.7,4.25),(32.8,4.25),(34.5,4.5),(36.2,4.7),(37.4,5.1),(38.5,5.6),(39.3,6.7),
   (39.8,7.9),(40.3,9.0),(41,9.7),(41.7,9.5),(41.8,8.8),(41.4,8.6)]
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
