# Eén oogvrucht uit r10, scherp verkleind: per blok de meest voorkomende paletkleur (geen mengkleuren).
from PIL import Image, ImageDraw
import numpy as np
im=Image.open('gemini/r10.png').convert('RGB')
f=np.array(im.crop((462,378,556,478))).astype(int)
f[(f[...,1]>f[...,0]+10)]=255                    # blad weg
P=np.array([[255,255,255],[20,15,15],[235,235,235],[150,150,155],[230,95,50],[175,45,30],[110,20,15]])  # wit bg, zwart, oogwit, oogschaduw, rood, donkerrood, lijn
idx=((f[...,None,:]-P[None,None])**2).sum(-1).argmin(-1)
def down(w):
  H,W=idx.shape; h=round(H*w/W); out=np.zeros((h,w),int)
  for y in range(h):
    for x in range(w):
      b=idx[y*H//h:(y+1)*H//h, x*W//w:(x+1)*W//w].ravel()
      fg=b[b!=0]
      out[y,x]=0 if len(fg)<len(b)*0.4 else np.bincount(fg).argmax()
  return Image.fromarray(P[out].astype(np.uint8))
tiles=[down(w) for w in (6,9,14)]
S=16; W=sum(t.width*S for t in tiles)+60*3+20; H=max(t.height*S for t in tiles)+40
o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); x=10
for t,lab in zip(tiles,['3 trossen ~6 px','2 trossen (A) ~9 px','1 tros (C) ~14 px']):
  o.paste(t.resize((t.width*S,t.height*S),Image.NEAREST),(x,10)); d.text((x,H-25),lab,fill='black'); x+=t.width*S+60
o.save('plak/vrucht_maten_scherp.png')
