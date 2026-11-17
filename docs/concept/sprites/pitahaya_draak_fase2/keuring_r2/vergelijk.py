from PIL import Image, ImageDraw
import numpy as np
s=Image.open('sprite_r2/pitahaya2_r2.png'); si=np.array(s); srgb=np.array(s.convert('RGB')).astype(int)
n=np.array(Image.open('sprite_r2/natief.png').convert('RGB')).astype(int)
m=Image.open('model/model.png').convert('RGB')
best=None
for ox in range(-3,6):
  for oy in range(-46,-36):
    mm=np.full((64,64,3),255.0)
    for sy in range(64):
      for sx in range(64):
        x0=3*sx+ox; y0=3*sy+oy
        if x0<0 or y0<0 or x0+3>n.shape[1] or y0+3>n.shape[0]: continue
        mm[sy,sx]=n[y0:y0+3,x0:x0+3].reshape(-1,3).mean(0)
    mask=si!=0
    fg=(np.abs(mm-255).sum(2)>60)
    sc=(mask^fg).sum()
    if best is None or sc<best[0]: best=(sc,ox,oy,mm)
print('offset',best[1:3],'silhouet-xor',best[0])
mm=best[3]; np.save('keuring_r2/model64.npy',mm)
Image.fromarray(mm.astype(np.uint8)).save('keuring_r2/model64.png')
mask=si!=0; fg=(np.abs(mm-255).sum(2)>60)
print('alleen sprite',np.argwhere(mask&~fg).tolist())
print('alleen model',np.argwhere(fg&~mask).tolist())
def crop(x0,y0,x1,y1,W,name):
  a=Image.fromarray(srgb[y0:y1,x0:x1].astype(np.uint8)).resize(((x1-x0)*W,(y1-y0)*W),Image.NEAREST)
  b=Image.fromarray(mm[y0:y1,x0:x1].astype(np.uint8)).resize(((x1-x0)*W,(y1-y0)*W),Image.NEAREST)
  ox,oy=best[1],best[2]; mx0=3*x0+ox; my0=3*y0+oy
  nat=n[max(my0,0):3*y1+oy,max(mx0,0):3*x1+ox].astype(np.uint8)
  c=Image.fromarray(nat).resize((a.width,a.height),Image.NEAREST)
  sh=Image.new('RGB',(a.width*3+20,a.height),(128,128,128)); sh.paste(a,(0,0)); sh.paste(b,(a.width+10,0)); sh.paste(c,(2*a.width+20,0))
  d=ImageDraw.Draw(sh)
  for i in range(x1-x0+1):
    d.line([(i*W,0),(i*W,4)],fill=(0,0,0))
  sh.save('keuring_r2/'+name)
crop(2,34,26,60,12,'kop12x.png')
crop(16,28,46,48,12,'rug12x.png')
crop(8,44,62,63,10,'poten10x.png')
