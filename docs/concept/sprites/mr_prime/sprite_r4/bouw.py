# Bouwt een variant: basis -> ogen/monocle (gezicht.py) -> hoed/haar (hoed.py) -> opschoning (opschoon.py als die er is)
import sys, numpy as np, hoed, gezicht
def bouw(hv='B', ov='E1', log=None, schoon=True):
    log={} if log is None else log
    C=np.load('basis.npy')
    C=gezicht.maak(C,ov,log)
    C=hoed.variant(C,hv,log)
    if schoon:
        try:
            import opschoon; C=opschoon.schoon(C,log)
        except ImportError: pass
        import r3post; C=r3post.post(C,log)
    return C
if __name__=='__main__':
    from toon import rgb; from PIL import Image
    out=sys.argv[1]; z=12
    tiles=[]
    for hv,ov in [('A','O1'),('B','O1'),('B','O2'),('B','O3')]:
        log={}; c=bouw(hv,ov,log); print(hv,ov,log)
        tiles.append(Image.fromarray(rgb(c[0:30,18:64])).resize((46*z,30*z),0))
    W=Image.new('RGB',(46*z*2+10,30*z*2+10),(255,255,255))
    for k,t in enumerate(tiles): W.paste(t,((k%2)*(46*z+10),(k//2)*(30*z+10)))
    W.save(out)
