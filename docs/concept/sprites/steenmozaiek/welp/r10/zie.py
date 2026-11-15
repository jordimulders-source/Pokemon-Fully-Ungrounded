# Kop op 12x: sprite (met raster) | model (zelfde raster). gebruik: python3 zie.py a.npy out.png [x0,y0,x1,y1] [z]
import sys,numpy as np
from PIL import Image, ImageDraw
from toon6 import big
F=np.load('FIN10.npy'); SRC='../../referenties/model_welp_gekozen.png'; k=16.896
def raster(c,box,z):
    d=ImageDraw.Draw(c)
    for i in range(box[2]-box[0]+1): d.line([(i*z,0),(i*z,c.height)],fill=(0,160,255,255) if (i+box[0])%5==0 else (120,120,120,70))
    for j in range(box[3]-box[1]+1): d.line([(0,j*z),(c.width,j*z)],fill=(0,160,255,255) if (j+box[1])%5==0 else (120,120,120,70))
    return c
def mod(b,z):
    m=Image.open(SRC).convert('RGBA')
    return m.crop((int(99.3+b[0]*k),int(191.5+b[1]*k),int(99.3+b[2]*k),int(191.5+b[3]*k))).resize(((b[2]-b[0])*z,(b[3]-b[1])*z),Image.LANCZOS)
if __name__=='__main__':
    box=tuple(map(int,sys.argv[3].split(','))) if len(sys.argv)>3 else (0,0,26,26); z=int(sys.argv[4]) if len(sys.argv)>4 else 12
    a=np.load(sys.argv[1])[box[1]:box[3],box[0]:box[2]]
    A=raster(big(a,z,F),box,z); B=raster(mod(box,z),box,z)
    V=Image.new('RGBA',(A.width*2+10,A.height),(255,255,255,255)); V.alpha_composite(A,(0,0)); V.alpha_composite(B,(A.width+10,0)); V.save(sys.argv[2])
