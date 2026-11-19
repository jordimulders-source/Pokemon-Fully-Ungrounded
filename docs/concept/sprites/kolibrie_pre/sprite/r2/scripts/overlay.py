# Model (natief raster) op het doelraster: uitsnede x0..x1/y0..y1 in doelpixels, schaal S, met rasterlijnen; naast de sprite
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'..'); from toon import rgba
A=np.load(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); S=int(sys.argv[6]); out=sys.argv[7]
N=Image.open('natief.png').convert('RGBA'); k=16
Nb=N.resize((100*k,100*k),Image.NEAREST)
s=77/40
def nat(tx,ty): return ((11.5+tx*s)*k,(18.5+ty*s)*k)
a=nat(x0,y0); b=nat(x1,y1)
M=Nb.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1]))).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
P=Image.new('RGBA',((x1-x0)*S,(y1-y0)*S),(236,236,226,255)); P.alpha_composite(rgba(A).crop((x0,y0,x1,y1)).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST))
V=Image.new('RGBA',(2*(x1-x0)*S+10,(y1-y0)*S),(255,255,255,255)); V.paste(P,(0,0)); V.paste(M,((x1-x0)*S+10,0))
d=ImageDraw.Draw(V)
for i in range(x1-x0+1):
    for off in (0,(x1-x0)*S+10): d.line([(off+i*S,0),(off+i*S,(y1-y0)*S)],fill=(255,0,0,90) if (x0+i)%5 else (255,0,0,255))
for j in range(y1-y0+1):
    for off in (0,(x1-x0)*S+10): d.line([(off,j*S),(off+(x1-x0)*S,j*S)],fill=(255,0,0,90) if (y0+j)%5 else (255,0,0,255))
V.save(out)
