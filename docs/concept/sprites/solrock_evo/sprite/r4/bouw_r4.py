# r4: hele plaat zonder breuk (= basis van r1, ../basis.npy) + ogen uit het natieve raster (ogen_natief.py).
import numpy as np, sys; from PIL import Image
sys.path.insert(0,'..'); from ogen_natief import red
from npy2png import save
p,ph=5.12,4.25; S=11.87; X0=138-0.5*S; Y0=107-1.2*S
PAL=[(152,208,160),(16,14,18),(42,40,44),(66,64,66),(104,100,98),(252,228,148),(206,162,88),
     (248,192,96),(210,134,52),(156,92,36),(96,52,20),(228,84,72),(180,36,44)]   # rood naar de modeltinten (154,37,39)/(207,67,61); zalm las als mond
M={'K':1,'R':12,'r':11,'a':7,'b':8,'c':9,'L':10,'g':3}
KEUZE={'L':(62,92,7,6,int(sys.argv[1]) if len(sys.argv)>1 else 0,int(sys.argv[2]) if len(sys.argv)>2 else 0),
       'R':(83,95,9,6,0,1)}
basis=np.load('../basis.npy'); o=basis.copy()
# oude (gereduceerde) ogen eerst weg: rood en het zwart van de oogkas -> plaattint van de buren
OUD={'L':(16,22,32,38),'R':(25,33,33,39)}
log={}
for k,(x0,y0,w,h,fx,fy) in KEUZE.items():
    blok=red(x0+fx,y0+fy,w,h)
    # natieve blokmidden -> modelcoordinaat -> spritecoordinaat; blok gecentreerd daarop
    cxn=x0+fx+w; cyn=y0+fy+h          # natieve index van het blokmidden
    cx=(ph+cxn*p-X0)/S; cy=(ph+cyn*p-Y0)/S
    sx=int(round(cx-w/2)); sy=int(round(cy-h/2))
    rows=[list(r) for r in blok]
    if k=='R':   # opschonen: onderste roodrij afwisselend R/r -> licht (model: lichtere onderhelft)
        for i in range(w):
            if rows[2][i]=='R': rows[2][i]='r'
        # zwarte inkeping uit het model: natieve kolom 90, rij 98-100 (1 natieve px breed, viel weg bij 2x2) -> blokkolom 3, rij 1
        rows[1][3]='K'
    for j,row in enumerate(rows):
        for i,c in enumerate(row):
            o[sy+j,sx+i]=M[c]
    log[k]=(sx,sy,w,h)
np.save('sprite.npy',o); save(o,'sprite.png',PAL+[(0,0,0)]*3)
print(log)
