import sys
exec(open('hand.py').read())
base=a.copy()
from PIL import Image
outs={}
for v in 'ABC':
    a[:]=base; ogen(v); outs[v]=a.copy(); save_txt(a,f'raster_{v}.txt')
HOOFD=sys.argv[1] if len(sys.argv)>1 else 'A'
save_txt(outs[HOOFD],'raster.txt')
