# Mock: hele Pokémon scherp op 64 px. (1) r10 met dubbele trossen (3 trossen), (2) A: middelste tros weg, linker/rechter 1,5x.
import sys; sys.path.insert(0,'plak')
from PIL import Image, ImageChops, ImageDraw
import numpy as np
exec(open('plak/dubbel.py').read().split('boxes=')[0])   # src, fruitmask, M
boxes=[(120,430,320,700),(380,280,570,540),(695,425,890,690)]
def crisp64(im):
  bg=Image.new('RGB',im.size,(255,255,255))
  d=ImageChops.difference(im,bg).convert('L').point(lambda v:255 if v>30 else 0)
  c=im.crop(d.getbbox()); q=c.quantize(15,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
  pal=np.array(q.getpalette()[:45]).reshape(15,3); idx=np.array(q)
  wb=((pal-255)**2).sum(1).argmin()
  H,W=idx.shape; s=64/max(H,W); h,w=round(H*s),round(W*s); out=np.zeros((h,w),int)
  for y in range(h):
    for x in range(w):
      b=idx[y*H//h:(y+1)*H//h, x*W//w:(x+1)*W//w].ravel(); fg=b[b!=wb]
      out[y,x]=wb if len(fg)<len(b)*0.45 else np.bincount(fg).argmax()
  t=Image.fromarray(pal[out].astype(np.uint8))
  can=Image.new('RGB',(64,64),'white'); can.paste(t,((64-w)//2,64-h)); return can
# variant A
im=src.copy()
mid=fruitmask(boxes[1]); arr=np.array(im); arr[mid]=255; im=Image.fromarray(arr)
for box,anchor in ((boxes[0],'l'),(boxes[2],'r')):
  m=fruitmask(box); x0,y0,x1,y1=box
  ys,xs=np.where(m); bx0,by0,bx1,by1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
  crop=src.crop((bx0,by0,bx1,by1)); mk=M((m[by0:by1,bx0:bx1]*255).astype(np.uint8))
  f=1.5; nw,nh=round(crop.width*f),round(crop.height*f)
  crop=crop.resize((nw,nh),Image.NEAREST); mk=mk.resize((nw,nh),Image.NEAREST)
  cx=(bx0+bx1)//2 + (-25 if anchor=='l' else 25)
  im.paste(crop,(cx-nw//2,by0-10),mk)
im.save('plak/mock_A_groot.png')
a3=Image.open('plak/a.png').convert('RGB')
tiles=[crisp64(a3),crisp64(im)]
o=Image.new('RGB',(512*2+40,560),'white'); d=ImageDraw.Draw(o)
for i,(t,l) in enumerate(zip(tiles,['3 volle trossen','A: 2 trossen, 1,5x'])):
  o.paste(t.resize((512,512),Image.NEAREST),(i*552,0)); d.text((i*552+10,530),l,fill='black')
o.save('plak/mock_vergelijk_64.png')
for t,n in zip(tiles,['3','A']): t.save(f'plak/mock_{n}_64.png')
