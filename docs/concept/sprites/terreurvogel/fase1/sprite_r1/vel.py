# vel.png: sprite 8x | kale reductie 8x | model met rode spriteomtrek ; daaronder swaps 4x en 1x naast fase 2 v8
import numpy as np, sys, glob; from PIL import Image, ImageDraw
from lib import *; from modelover import modelbeeld, model1x
def rgbaP(pad,k):
    im=Image.open(pad); a=np.array(im); pal=im.getpalette()
    o=np.zeros((64,64,4),'uint8')
    for i in set(a.ravel()):
        if i==0: continue
        o[a==i,:3]=pal[3*i:3*i+3]; o[a==i,3]=255
    return Image.fromarray(o,'RGBA').resize((64*k,64*k),Image.NEAREST)
def omtrek(a,k):
    m=a>0; lay=Image.new('RGBA',(64*k,64*k),(0,0,0,0)); d=ImageDraw.Draw(lay)
    for y in range(64):
        for x in range(64):
            if not m[y,x]: continue
            if y==0 or not m[y-1,x]: d.line([(x*k,y*k),(x*k+k,y*k)],fill=(255,0,0,255),width=2)
            if y==63 or not m[y+1,x]: d.line([(x*k,y*k+k),(x*k+k,y*k+k)],fill=(255,0,0,255),width=2)
            if x==0 or not m[y,x-1]: d.line([(x*k,y*k),(x*k,y*k+k)],fill=(255,0,0,255),width=2)
            if x==63 or not m[y,x+1]: d.line([(x*k+k,y*k),(x*k+k,y*k+k)],fill=(255,0,0,255),width=2)
    return lay
def bouw(hoofd,swaps,uit,k=8):
    BG=(236,236,236,255); W=64*k*3+40; vel=Image.new('RGBA',(W,64*k+40+64*4+60+64+40),BG); d=ImageDraw.Draw(vel)
    a=np.array(Image.open(hoofd))
    vel.alpha_composite(rgbaP(hoofd,k),(10,30)); d.text((10,10),hoofd+' 8x',fill=(0,0,0))
    vel.alpha_composite(rgbaP('kaal.png',k),(20+64*k,30)); d.text((20+64*k,10),'kale reductie 8x',fill=(0,0,0))
    mb=modelbeeld(k).convert('RGBA'); mb.alpha_composite(omtrek(a,k)); vel.alpha_composite(mb,(30+128*k,30)); d.text((30+128*k,10),'model + rode spriteomtrek',fill=(0,0,0))
    y=40+64*k; x=10
    lijst=[(hoofd,'model-kleuren')]+[(s,s.split('_')[-1][:-4]) for s in swaps]+[('../../fase2/swaps_r1/v8.png','fase 2 v8')]
    for pad,nm in lijst:
        vel.alpha_composite(rgbaP(pad,4),(x,y+14)); d.text((x,y),nm,fill=(0,0,0)); x+=64*4+8
    y2=y+14+64*4+10; x=10
    for pad,nm in lijst:
        vel.alpha_composite(rgbaP(pad,1),(x,y2)); x+=72
    x+=20; vel.alpha_composite(model1x().convert('RGBA'),(x,y2)); d.text((x,y2+66),'model 1x',fill=(0,0,0))
    vel.save(uit)
if __name__=='__main__':
    bouw(sys.argv[1],sorted(glob.glob('kuiken_r1_s*.png')),sys.argv[2] if len(sys.argv)>2 else 'vel.png')
