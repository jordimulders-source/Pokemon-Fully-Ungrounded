# Plakt elke tros van r10 nog eens, verschoven, achter het origineel (alleen Gemini-pixels).
import sys
from PIL import Image, ImageFilter, ImageChops
import numpy as np
src=Image.open('gemini/r10.png').convert('RGB'); a=np.array(src).astype(int)
r,g,b=a[...,0],a[...,1],a[...,2]
M=lambda m:Image.fromarray(m)
green=(g>r+10)
light=(a.min(2)>200)
def fruitmask(box):
  x0,y0,x1,y1=box
  # achtergrond = licht en vanaf de rand van het vak bereikbaar (flood fill), oogwit zit ingesloten
  L=light[y0:y1,x0:x1].copy(); H,W=L.shape
  bgm=np.zeros_like(L); stack=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
  while stack:
    y,x=stack.pop()
    if 0<=y<H and 0<=x<W and L[y,x] and not bgm[y,x]:
      bgm[y,x]=True; stack+= [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
  m=np.zeros(light.shape,bool); m[y0:y1,x0:x1]=~bgm & ~green[y0:y1,x0:x1]
  return m
boxes=[(120,430,320,700),(380,280,570,540),(695,425,890,690)]
def build(offs):
  out=src.copy()
  for (x0,y0,x1,y1),(dx,dy) in zip(boxes,offs):
    m=fruitmask((x0,y0,x1,y1))
    mi=M((m*255).astype(np.uint8))
    layer=Image.new('RGB',src.size,'white'); layer.paste(src,(dx,dy),mi.transform(src.size,Image.AFFINE,(1,0,0,0,1,0)))
    shifted_mask=Image.new('L',src.size,0); shifted_mask.paste(mi,(dx,dy))
    shifted_img=Image.new('RGB',src.size); shifted_img.paste(src,(dx,dy))
    out.paste(shifted_img,(0,0),shifted_mask)   # kopie
    out.paste(src,(0,0),mi)                      # origineel weer erop
  return out
offs=eval(sys.argv[1]); name=sys.argv[2]
im=build(offs); im.save(f'plak/{name}.png')
bg=Image.new('RGB',im.size,(255,255,255))
d=ImageChops.difference(im,bg).convert('L').point(lambda v:255 if v>30 else 0)
cc=im.crop(d.getbbox()); w,h=cc.size; s=64/max(w,h)
t=cc.resize((round(w*s),round(h*s)),Image.BOX).quantize(16).convert('RGB')
can=Image.new('RGB',(64,64),'white'); can.paste(t,((64-t.width)//2,64-t.height)); can.resize((512,512),Image.NEAREST).save(f'plak/{name}_test64_8x.png')
