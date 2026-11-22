# model op spritegrootte (natief 2x2-gemiddelde, zelfde uitlijning als r1: sprite (r,c) = natief (13+2(r-9)+..., 67+2(c-4))) met raster
import numpy as np; from PIL import Image, ImageDraw
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
S=np.full((64,64,3),255.0)
for r in range(64):
    for c in range(64):
        y=13+2*(r-9); x=67+2*(c-4)
        if 0<=y and y+2<=n.shape[0] and 0<=x and x+2<=n.shape[1]: S[r,c]=n[y:y+2,x:x+2].reshape(-1,3).mean(0)
np.save('model64.npy',S)
def vel(x0,x1,y0,y1,Z,out):
    im=Image.fromarray(S[y0:y1,x0:x1].astype('uint8')).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST); d=ImageDraw.Draw(im)
    for x in range(x0,x1+1):
        d.line([((x-x0)*Z,0),((x-x0)*Z,im.height)],fill=(255,0,0) if x%5==0 else (200,200,200))
        if x%5==0: d.text(((x-x0)*Z+2,2),str(x),fill=(0,0,255))
    for y in range(y0,y1+1):
        d.line([(0,(y-y0)*Z),(im.width,(y-y0)*Z)],fill=(255,0,0) if y%5==0 else (200,200,200))
        if y%5==0: d.text((2,(y-y0)*Z+2),str(y),fill=(0,0,255))
    im.save(out)
vel(0,32,8,48,22,'/tmp/claude-0/mL.png'); vel(30,62,8,48,22,'/tmp/claude-0/mR.png')
