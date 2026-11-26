import sys
from PIL import Image, ImageDraw
import numpy as np
def zoom(src,dst,k=12,box=None,grid=True):
    im=Image.open(src); p=im.getpalette(); a=np.array(im)
    if box: a=a[box[1]:box[3],box[0]:box[2]]
    rgb=np.array(p[:48]).reshape(16,3)[a].astype(np.uint8); rgb[a==0]=(200,230,200)
    big=Image.fromarray(np.kron(rgb,np.ones((k,k,1),np.uint8)))
    if grid:
        d=ImageDraw.Draw(big)
        ox,oy=(box[0],box[1]) if box else (0,0)
        for x in range(a.shape[1]):
            if (x+ox)%8==0: d.line([(x*k,0),(x*k,big.height)],fill=(255,120,120))
            if (x+ox)%8==0: d.text((x*k+1,1),str(x+ox),fill=(200,0,0))
        for y in range(a.shape[0]):
            if (y+oy)%8==0: d.line([(0,y*k),(big.width,y*k)],fill=(255,120,120)); d.text((1,y*k+1),str(y+oy),fill=(200,0,0))
    big.save(dst)
if __name__=='__main__':
    b=tuple(map(int,sys.argv[4].split(','))) if len(sys.argv)>4 else None
    zoom(sys.argv[1],sys.argv[2],int(sys.argv[3]),b)
