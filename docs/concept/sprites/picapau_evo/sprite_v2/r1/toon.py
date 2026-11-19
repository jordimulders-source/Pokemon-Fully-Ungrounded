# npy -> 8x png met het Gen 3-palet van bouw.py (controle)
import sys; import numpy as np; from PIL import Image
PAL=[(255,255,255),(24,20,16),(226,150,96),(192,110,60),(142,74,42),(250,242,214),(230,210,166),(196,170,124),
     (232,82,74),(204,196,192),(142,132,130),(78,70,70),(252,226,96),(212,170,52),(255,255,255),(98,48,26)]
P=dict(enumerate(PAL))
o=np.load(sys.argv[1]); s=int(sys.argv[3]) if len(sys.argv)>3 else 8
img=np.zeros(o.shape+(3,),'uint8')
for k,c in P.items(): img[o==k]=c
im=Image.fromarray(img).resize((o.shape[1]*s,o.shape[0]*s),0)
from PIL import ImageDraw; d=ImageDraw.Draw(im)
if s>1:
  for x in range(0,o.shape[1]*s,s*8): d.line([(x,0),(x,im.height)],fill=(200,200,255))
  for y in range(0,o.shape[0]*s,s*8): d.line([(0,y),(im.width,y)],fill=(200,200,255))
im.save(sys.argv[2])
