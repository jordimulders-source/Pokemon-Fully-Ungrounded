# klassenraster (npy) -> geïndexeerde png (index 0 transparant); optioneel palet 'model'
import numpy as np, sys; from PIL import Image; from palet import pal
def maak(o,v='gen3'):
    im=Image.fromarray(o.astype('uint8'),'P'); p=[c for t in pal(v) for c in t]; im.putpalette(p+[0]*(768-len(p))); im.info['transparency']=0; return im
if __name__=='__main__':
    o=np.load(sys.argv[1]); maak(o,sys.argv[3] if len(sys.argv)>3 else 'gen3').save(sys.argv[2],transparency=0)
