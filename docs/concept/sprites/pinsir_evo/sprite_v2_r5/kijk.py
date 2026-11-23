# Hulp: model (origineel 1024) en sprite op hetzelfde spriteraster, met rasterlijnen en coordinaten.
import numpy as np
from PIL import Image, ImageDraw
S=64/91; OY=9; PITCH=10.24; FASE=9.25
M=Image.open('referenties/model_v2_r4.webp').convert('RGB')
def sprite2model(sx,sy):
    # linkerbovenhoek van spritepixel in modelpixels (natief nx = (sx-0.3)/S+5)
    nx=(sx-0.3)/S+5; ny=(sy-OY-0.3)/S+11
    return 4.5+nx*PITCH-PITCH/2, 4.5+ny*PITCH-PITCH/2
def model_crop(x0,y0,x1,y1,k):
    a=sprite2model(x0,y0); b=sprite2model(x1,y1)
    return M.crop((round(a[0]),round(a[1]),round(b[0]),round(b[1]))).resize(((x1-x0)*k,(y1-y0)*k),Image.LANCZOS)
def sprite_crop(path_or_img,x0,y0,x1,y1,k,bg=(152,208,160)):
    im=path_or_img if isinstance(path_or_img,Image.Image) else Image.open(path_or_img)
    im=im.convert('RGBA'); c=Image.new('RGBA',im.size,bg+(255,)); c.alpha_composite(im)
    return c.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*k,(y1-y0)*k),Image.NEAREST)
def raster(img,x0,y0,k,stap=1,kleur=(255,0,0)):
    d=ImageDraw.Draw(img); w,h=img.size
    for i in range(0,w//k+1):
        c=kleur if (x0+i)%4==0 else (255,190,190)
        if (x0+i)%4==0 or k>=12: d.line([(i*k,0),(i*k,h)],fill=c)
        if (x0+i)%4==0: d.text((i*k+2,2),str(x0+i),fill=(0,0,255))
    for j in range(0,h//k+1):
        c=kleur if (y0+j)%4==0 else (255,190,190)
        if (y0+j)%4==0 or k>=12: d.line([(0,j*k),(w,j*k)],fill=c)
        if (y0+j)%4==0: d.text((2,j*k+2),str(y0+j),fill=(0,0,255))
    return img
def naast(beelden,gap=12,label=None):
    w=sum(b.width for b in beelden)+gap*(len(beelden)-1); h=max(b.height for b in beelden)+(14 if label else 0)
    o=Image.new('RGB',(w,h),(255,255,255)); x=0; d=ImageDraw.Draw(o)
    for i,b in enumerate(beelden):
        o.paste(b,(x,14 if label else 0))
        if label: d.text((x+2,1),label[i],fill=(0,0,0))
        x+=b.width+gap
    return o
def vergelijk(sprites,x0,y0,x1,y1,k,labels,metraster=True):
    bs=[sprite_crop(s,x0,y0,x1,y1,k) for s in sprites]+[model_crop(x0,y0,x1,y1,k)]
    if metraster: bs=[raster(b,x0,y0,k) for b in bs]
    return naast(bs,label=labels)
_A=np.asarray(M).astype(int)
FG=~((_A.min(2)>222)&((_A[...,0]-_A[...,2])<40))
def dekking(sx,sy):
    a=sprite2model(sx,sy); b=sprite2model(sx+1,sy+1)
    return FG[round(a[1]):round(b[1]),round(a[0]):round(b[0])].mean()
def modelmasker(th=0.5):
    return np.array([[dekking(x,y)>=th for x in range(64)] for y in range(64)])
def modelkleur(sx,sy):
    a=sprite2model(sx,sy); b=sprite2model(sx+1,sy+1)
    blk=_A[round(a[1])+2:round(b[1])-2,round(a[0])+2:round(b[0])-2].reshape(-1,3)
    return np.median(blk,0)
