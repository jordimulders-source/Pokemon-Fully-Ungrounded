# vgl.py sprite.png uit.png [x0 y0 x1 y1 schaal]
# sprite (8x of 'schaal') | model op exact dezelfde uitsnede en schaal (gedeelde geometrie), met spritepixelraster over beide.
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite'); from reductie_gedeeld import P,X0M,X0S,Y0M,Y0S
MODEL='../r8/gemini_r8.png'
def model_crop(x0,y0,x1,y1,s):
    a=Image.open(MODEL).convert('RGB'); W=Image.new('RGB',(1824,1559),'white'); W.paste(a,(400,400))
    mx0=X0M+(x0-X0S)*P+400; my0=Y0M-(Y0S-y0)*P+400
    return W.transform(((x1-x0)*s,(y1-y0)*s),Image.EXTENT,(mx0,my0,mx0+(x1-x0)*P,my0+(y1-y0)*P),Image.BICUBIC)
def sprite_rgb(p,bg=(152,208,160)):
    im=Image.open(p)
    if im.mode=='RGBA':
        a=np.asarray(im).copy(); a[a[...,3]==0,:3]=bg; return Image.fromarray(a[...,:3])
    o=np.asarray(im).astype(int); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=pal[o].astype('uint8'); img[o==0]=bg; return Image.fromarray(img)
def raster(im,s,col):
    d=ImageDraw.Draw(im)
    if s>=10:
        for i in range(0,im.size[0],s): d.line([(i,0),(i,im.size[1])],fill=col)
        for j in range(0,im.size[1],s): d.line([(0,j),(im.size[0],j)],fill=col)
    return im
if __name__=='__main__':
    sp=sys.argv[1]; uit=sys.argv[2]
    x0,y0,x1,y1,s=(list(map(int,sys.argv[3:8])) if len(sys.argv)>3 else [0,0,64,64,8])
    a=sprite_rgb(sp).crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
    m=model_crop(x0,y0,x1,y1,s)
    a=raster(a,s,(120,120,120)); m=raster(m,s,(200,200,255))
    W=Image.new('RGB',(a.size[0]*2+16,a.size[1]),'white'); W.paste(a,(0,0)); W.paste(m,(a.size[0]+16,0)); W.save(uit)
