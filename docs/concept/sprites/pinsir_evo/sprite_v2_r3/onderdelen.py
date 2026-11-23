# Onderdelen van de sprite (spritecoordinaten x,y), afgelezen op het model op spritemaat (vergelijk.py, 20-24x met raster).
# Alleen om per onderdeel licht/schaduw te kunnen zetten; de grenzen in de sprite zijn de modellijnen zelf.
import numpy as np
from skimage.measure import points_in_poly
# volgorde = prioriteit (eerste wint bij overlap)
import math
def ellips(cx,cy,rx,ry,n=24): return [(cx+rx*math.cos(2*math.pi*i/n),cy+ry*math.sin(2*math.pi*i/n)) for i in range(n)]
POLY={
 # kniecirkel: ring in het model natief kol 56-65 / rij 71-78 (gemeten op de celmiddens van het 1024-model) -> sprite x 36-42, y 51-56
 'knie':        ellips(39.2,53.6,3.6,3.1),
 # schouderkoepel: licht rond vlak, natief kol 50-58 / rij 40-48 -> sprite x 31-37, y 29-35
 'schouderkoepel': ellips(34.4,32.2,3.5,3.5),
 'kopschild':   [(6,19),(9,16),(13,14),(14,10),(17,12),(19,8),(21,11),(26,12),(28,9),(31,14),(35,16),(38,19),(31,21),(24,21),(20,20.5),(10,21)],
 'nabije_arm':  [(30,44),(31,41),(33,37),(36,35),(40,36),(42,39),(41,43),(38,46.5),(33,46.5)],
 'verre_arm':   [(6,44),(9,40),(13,39),(18,39),(20,41),(16,45),(12,47),(10,50),(7,48)],
 'nabije_dij':  [(31,49),(33,46.5),(38,46.5),(42,44),(46,45),(47.5,49),(47,56),(41,56.5),(35,56),(32,53)],
 'nabije_voet': [(33,56),(41,56.5),(47,56),(48,64),(33,64)],
 'verre_been':  [(12,47),(18,45.5),(22,46),(26,49),(27,56),(26,64),(11,64),(12,55)],
 'staart':      [(45,49),(49,46),(53,44),(57,41),(60,37),(64,31),(64,54),(56,56),(48,57)],
 'schouder':    [(25,21),(31,21),(36,23),(39,28),(39,34),(36,35),(32,37),(29,35),(25,30)],
 'rug':         [(30,17),(38,18),(46,20),(54,24),(60,32),(60,38),(56,42),(50,45),(46,46),(42,43),(40,36),(39,28),(36,22)],
}
def masker(naam,shape=(64,64)):
    yy,xx=np.mgrid[0:shape[0],0:shape[1]]
    return points_in_poly(np.c_[xx.ravel()+0.5,yy.ravel()+0.5],np.array(POLY[naam],float)).reshape(shape)
def kaart(shape=(64,64)):
    lab=np.zeros(shape,object); lab[:]=''
    for n in POLY:
        m=masker(n,shape)&(lab=='')
        lab[m]=n
    return lab
