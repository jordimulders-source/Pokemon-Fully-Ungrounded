# cmp.py a.txt b.txt uit.png [x0 y0 x1 y1 schaal]: twee rasters naast elkaar (a met oud palet uit ../lijf_r2)
import sys,importlib.util
from PIL import Image
def ld(p):
    s=importlib.util.spec_from_file_location('p'+str(hash(p)),p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
P0=ld('../lijf_r2/pal.py'); P1=ld('pal.py')
a,b,o=sys.argv[1:4]; x0,y0,x1,y1,k=(list(map(int,sys.argv[4:9]))+[0,0,64,64,8])[:5] if len(sys.argv)>4 else (0,0,64,64,8)
A=P0.rgb(P0.load(a)).crop((x0,y0,x1,y1)); B=P1.rgb(P1.load(b)).crop((x0,y0,x1,y1))
W,H=(x1-x0)*k,(y1-y0)*k; out=Image.new('RGB',(2*W+8,H),(255,255,255))
out.paste(A.resize((W,H),0),(0,0)); out.paste(B.resize((W,H),0),(W+8,0)); out.save(o)
