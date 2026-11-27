# Natief raster van gemini/r6.png terughalen: pitch 10,24 (100x100), fase gemeten via randsterkte.
from PIL import Image; import numpy as np
D='docs/concept/sprites/ledian_evo/'
a=np.asarray(Image.open(D+'gemini/r6.png').convert('RGB')).astype(int)
P=10.24; PHX=9.3; PHY=9.2
xs=np.arange(PHX+1+P/2-P,1024,P); xs=xs[xs>=0]
ys=np.arange(PHY+1+P/2-P,1024,P); ys=ys[ys>=0]
out=np.zeros((len(ys),len(xs),3),'uint8'); spread=np.zeros((len(ys),len(xs)))
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(y-2),int(y+3); x0,x1=int(x-2),int(x+3)
        blk=a[max(0,y0):y1,max(0,x0):x1].reshape(-1,3)
        out[j,i]=np.median(blk,axis=0); spread[j,i]=blk.std(axis=0).sum()
out[(out>=0xe0).all(axis=2)]=255
im=Image.fromarray(out); im.save(D+'sprite_r1/natief.png')
g=np.asarray(im.convert('L')); yy,xx=np.where(g<240)
print(len(xs),len(ys),'bbox',xx.min(),xx.max(),yy.min(),yy.max(),'max spread',spread.max().round(1),'mean',spread[g<240].mean().round(1))
