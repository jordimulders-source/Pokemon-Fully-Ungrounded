# Ronde 4: zwarte ogen (Jordi: "kudu irl heeft een zwart oog"; a/b/c waren "nog niet goed", uitdrukking: kalm, half gesloten lid).
# Model A3: lid = dikke zwarte lijn op rij 22, x 10-13 (gemeten x 10,3-13,3); daaronder het oog, 1 rij (x 10,4-13,3, pupil x 11-12).
# Elke variant: bronpixels 1-op-1, alleen omgekleurd naar het kudupalet; '-' = bronpixel die niet tot het oog hoort (vacht blijft).
# Lid uit het model = rij 22, x 10-13 -> '0' (bovenlaag, alleen waar genoemd).
import numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def bron(n,bx0,by0,bx1,by1,kaart,dx,dy,tag):
    a=np.asarray(Image.open(R+n+'/anim_front_gba.png')); out=[]
    for y in range(by0,by1+1):
        for x in range(bx0,bx1+1):
            c=kaart.get(int(a[y,x]),'-')
            if c!='-': out.append((x+dx,y+dy,c,'oog %s: %s bronpixel (%d,%d) index %d'%(tag,n,x,y,a[y,x])))
    return out
LID=[(x,22,'0','lid uit het model (dikke zwarte lijn rij 22, x 10-13)') for x in range(10,14)]
VAR={
 # A Kangaskhan: donker oog onder een zwaar lid (lid 82,65,16 -> K; zwart -> 0; wit glans -> W; mauve 148,106,139 -> D)
 'A':('Kangaskhan 1-op-1 (zwaar lid zit in de bron)',lambda: bron('kangaskhan',39,38,42,40,{15:'K',6:'0',1:'W',8:'D'},-29,-16,'A')),
 # B Ponyta: zwart oog (16,16,16 -> 0; donkergrijs 90,90,90 -> K; glans -> W) + lid uit het model
 'B':('Ponyta 1-op-1 + lid uit het model',lambda: bron('ponyta',17,26,19,28,{15:'0',14:'K',1:'W'},-7,-3,'B')+LID),
 # C Flareon (rechteroog): zwart (a) -> 0, rand donkerrood (f) -> K, grijze tweede glans (9) -> 3, glans -> W, lichte rand (c) -> L; + lid uit het model
 'C':('Flareon 1-op-1 + lid uit het model',lambda: bron('flareon',23,29,27,32,{10:'0',15:'K',9:'3',1:'W'},-13,-7,'C')+LID),
 # D Ponyta 1-op-1 met haar eigen lid (rij 25), zonder modellid
 'D':('Ponyta 1-op-1 (eigen lid, zonder modellid)',lambda: bron('ponyta',17,25,19,28,{15:'0',14:'K',1:'W'},-7,-3,'D')),
}
def variant(v): return VAR[v][1]()
