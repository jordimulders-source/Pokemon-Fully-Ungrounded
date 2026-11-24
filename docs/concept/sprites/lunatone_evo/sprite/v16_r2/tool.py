import numpy as np; from PIL import Image
PAL=np.array([(0,0,0),(24,16,16),(60,22,28),(88,32,34),(138,56,50),(182,86,76),(204,108,92),(214,122,102),
              (168,20,24),(222,50,44),(236,128,112)],float)
def save(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((o.shape[1]*sc,o.shape[0]*sc),Image.NEAREST)
  im.save(fn,transparency=0)
def rgba(o,bgc=(230,230,230),sc=1):
  a=PAL[o].astype('uint8'); a[o==0]=bgc; im=Image.fromarray(a)
  return im.resize((o.shape[1]*sc,o.shape[0]*sc),Image.NEAREST) if sc>1 else im
def grid(o,fn,sc=12):
  from PIL import ImageDraw
  im=rgba(o,sc=sc); d=ImageDraw.Draw(im)
  for k in range(0,o.shape[0]+1):
    c=(120,120,255) if k%8==0 else (200,200,200)
    d.line([(k*sc,0),(k*sc,o.shape[0]*sc)],fill=c); d.line([(0,k*sc),(o.shape[1]*sc,k*sc)],fill=c)
  for k in range(0,o.shape[0],4):
    d.text((k*sc+1,1),str(k),fill=(0,0,255)); d.text((1,k*sc+1),str(k),fill=(0,0,255))
  im.save(fn)
def txt(o):
  C=' #234567890RIL'
  return '\n'.join(f'{j:2d} '+''.join(' #2345.7RIL'[v] for v in o[j]) for j in range(o.shape[0]))
