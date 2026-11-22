"""Blokraster (regel: 'y aaaaaaaa bbbbbbbb cccccccc dddddddd', 4 blokken van 8 kolommen) -> .txt-raster. Controleert de lengte."""
import sys,os,numpy as np
sys.path.insert(0,os.path.dirname(__file__)); from ow_pal import totext
def lees(p):
    a=np.zeros((32,32),np.uint8)
    for l in open(p):
        if not l.strip() or l.startswith('#'): continue
        y,*b=l.split(); r=''.join(b); assert len(r)==32,(y,len(r))
        for x,c in enumerate(r):
            if c!='.': a[int(y),x]=int(c,16)
    return a
if __name__=='__main__':
    a=lees(sys.argv[1]); open(sys.argv[2],'w').write(totext(a)+'\n')
