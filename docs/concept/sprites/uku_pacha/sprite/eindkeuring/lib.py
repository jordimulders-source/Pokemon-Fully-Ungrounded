# gedeelde helpers eindkeuring (geen neveneffecten bij import)
import os, sys
from PIL import Image, ImageDraw
import numpy as np
D=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(D,'../r2'))
import geom
ORDE='.KndhsmblpwBDYPW'
PAL={'.':(255,255,255),'K':(16,20,28),'n':(36,50,76),'d':(66,78,102),'h':(130,164,200),'s':(82,102,132),
'm':(108,130,158),'b':(112,150,172),'l':(119,175,186),'p':(156,212,212),'w':(194,235,230),
'B':(75,108,148),'D':(44,73,111),'Y':(226,196,72),'P':(132,96,148),'W':(244,248,248)}
MODEL=Image.open(os.path.join(D,'../../model/r2_natief.png')).convert('RGB')
def lees(f): return [list(l.rstrip('\n')[:64].ljust(64,'.')) for l in open(f)][:64]
def schrijf(R,f): open(f,'w').write('\n'.join(''.join(r) for r in R)+'\n')
def png(R,f,pal=PAL):
    im=Image.new('P',(64,64),0); flat=[]
    for c in ORDE: flat+=list(pal[c])
    im.putpalette(flat+[0]*(768-len(flat)))
    for y,r in enumerate(R):
        for x,c in enumerate(r): im.putpixel((x,y),ORDE.index(c))
    im.save(f,transparency=0)
def rgb(R,bg=(255,255,255),pal=PAL):
    im=Image.new('RGB',(64,64),bg)
    for y,r in enumerate(R):
        for x,c in enumerate(r):
            if c!='.': im.putpixel((x,y),pal[c])
    return im
def model_in_sprite(x0,y0,x1,y1,s):
    "modelregio die overeenkomt met sprite-rechthoek, op schaal s px per spritepixel"
    a=geom.s2n(x0,y0); b=geom.s2n(x1-1,y1-1)
    box=(a[0],a[2],b[1],b[3])
    return MODEL.transform(((x1-x0)*s,(y1-y0)*s),Image.EXTENT,box,Image.BICUBIC)
def grid(im,s,col=(200,200,200)):
    if col==(255,0,0): col=(235,225,225)
    d=ImageDraw.Draw(im)
    for i in range(0,im.width,s): d.line([(i,0),(i,im.height)],fill=col)
    for j in range(0,im.height,s): d.line([(0,j),(im.width,j)],fill=col)
    return im
import math
def dekking():
    "fractie model-niet-achtergrond per spritepixel (64x64)"
    fg=(~geom.BG).astype(float); C=np.zeros((64,64))
    for j in range(64):
        for i in range(64):
            x0,x1,y0,y1=geom.s2n(i,j); a=t=0
            for cy in range(int(math.floor(y0)),int(math.ceil(y1))):
                for cx in range(int(math.floor(x0)),int(math.ceil(x1))):
                    if not(0<=cx<100 and 0<=cy<100): continue
                    w=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy))
                    if w<=0: continue
                    t+=w; a+=w*fg[cy,cx]
            C[j,i]=a/t if t else 0
    return C
def lum_model():
    "gemiddelde modelhelderheid per spritepixel (alleen voorgrondcellen)"
    N=geom.N; fg=~geom.BG; L=np.zeros((64,64))
    for j in range(64):
        for i in range(64):
            x0,x1,y0,y1=geom.s2n(i,j); a=t=0
            for cy in range(int(math.floor(y0)),int(math.ceil(y1))):
                for cx in range(int(math.floor(x0)),int(math.ceil(x1))):
                    if not(0<=cx<100 and 0<=cy<100) or not fg[cy,cx]: continue
                    w=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy))
                    if w<=0: continue
                    t+=w; a+=w*N[cy,cx].mean()
            L[j,i]=a/t if t else -1
    return L
