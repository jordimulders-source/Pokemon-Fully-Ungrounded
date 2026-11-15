# Gezichtspixels van Gengar (zelfde selectie als ../model/gezicht.py), verschoven naar plek A (dx -6, dy +5).
# Geeft dict {(x,y): gengar_index} in spritecoordinaten. Alleen meting/controle.
import numpy as np
from PIL import Image
G='../../../../../graphics/pokemon/gengar/anim_front.png'
def face():
    gi=np.array(Image.open(G))[:64]; f={}
    for y in range(24,41):
        for x in range(16,39):
            v=gi[y,x]; nb=gi[max(0,y-1):y+2,max(0,x-1):x+2]
            if v in {1,2,3,4,5,6,7,14,15} or (v==13 and any(n in {1,2,3,4,5,6,7} for n in nb.flatten())):
                f[(x-6,y+5)]=int(v)
    return f
if __name__=='__main__':
    import sys; sys.path.insert(0,'.'); from meet import klas
    f=face(); xs=[p[0] for p in f]; ys=[p[1] for p in f]
    print(min(xs),max(xs),min(ys),max(ys))
    for y in range(min(ys)-1,max(ys)+2):
        print('%3d '%y+''.join(('.123456789abcdef'[f[(x,y)]] if (x,y) in f else klas(x,y).lower()) for x in range(6,36)))
