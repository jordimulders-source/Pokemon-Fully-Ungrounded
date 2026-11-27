# Model-in-spriteraster: elke spritepixel toont zijn 2x2 natieve modelpixels (128x128), voor vergelijk per pixel.
import numpy as np, sys; from PIL import Image, ImageDraw
sys.path.insert(0,'.'); from kaart import *
N=np.load('../sprite_r3/natief.npy'); P=np.load('../sprite_r3/natief_pal.npy')
B=np.full((128,128,3),255,'uint8')
for Y in range(64):
    for X in range(64):
        x,y=blok(X,Y)
        for a in range(2):
            for b in range(2):
                k=N[y+a,x+b] if y+a<160 and x+b<160 else -1
                if k>=0: B[2*Y+a,2*X+b]=P[k]
if __name__=='__main__':
    x0,y0,x1,y1=map(int,sys.argv[1:5]); s=int(sys.argv[5]); sp=sys.argv[6]
    o=Image.open(sp).convert('RGBA'); bg=Image.new('RGBA',(64,64),(240,240,236,255)); bg.alpha_composite(o)
    A=bg.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
    M=Image.fromarray(B[2*y0:2*y1,2*x0:2*x1]).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
    W=Image.new('RGB',(2*(x1-x0)*s+10,(y1-y0)*s),(255,255,255)); W.paste(A,(0,0)); W.paste(M,((x1-x0)*s+10,0))
    d=ImageDraw.Draw(W)
    for i in range(x1-x0+1):
        for off in (0,(x1-x0)*s+10): d.line([(off+i*s,0),(off+i*s,(y1-y0)*s)],fill=(0,170,255))
    for j in range(y1-y0+1): d.line([(0,j*s),(W.width,j*s)],fill=(0,170,255))
    for i in range(0,x1-x0,2): d.text((i*s+2,2),str(x0+i),fill=(255,0,0))
    for j in range(0,y1-y0,2): d.text((2,j*s+2),str(y0+j),fill=(255,0,0))
    W.save(sys.argv[7])
