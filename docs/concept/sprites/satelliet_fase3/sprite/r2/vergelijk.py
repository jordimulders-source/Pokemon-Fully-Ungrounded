import sys
from PIL import Image, ImageDraw
import numpy as np
exec(open('bouw.py').read().split("# ---- 1.")[0])
def rast(path,k):
    rows=[l.rstrip('\n') for l in open(path)]
    B=Image.new('RGB',(OUTW*k,OH*k),(205,225,205)); d=ImageDraw.Draw(B)
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            if ch!='.': d.rectangle([x*k,y*k,x*k+k-1,y*k+k-1],fill=kaal.PAL[int(ch,16)])
    return B
def modelk(k):
    im=Image.open(kaal.M).convert('RGB'); f=k/s
    big=im.resize((int(W*f),int(H*f)),Image.LANCZOS)
    A=Image.new('RGB',(OUTW*k,OH*k),(255,255,255)); A.paste(big,(int(round(-X0*f)),int(round(-Y0*f)))); return A
if __name__=='__main__':
    k=int(sys.argv[3]) if len(sys.argv)>3 else 10
    A=modelk(k); B=rast(sys.argv[1],k)
    for img in (A,B):
        d=ImageDraw.Draw(img)
        for x in range(0,OUTW+1,4): d.line([(x*k,0),(x*k,OH*k)],fill=(255,150,150))
        for y in range(0,OH+1,4): d.line([(0,y*k),(OUTW*k,y*k)],fill=(255,150,150))
    out=Image.new('RGB',(A.width,A.height*2+6),(0,0,0)); out.paste(B,(0,0)); out.paste(A,(0,A.height+6)); out.save(sys.argv[2])
