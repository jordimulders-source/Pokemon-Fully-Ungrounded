# npy -> 8x png met modelkleuren (controle)
import sys; import numpy as np; from PIL import Image
P={0:(255,255,255),1:(14,10,8),2:(205,134,91),3:(191,110,63),4:(138,73,46),5:(243,233,201),6:(224,206,171),7:(200,179,141),
 8:(222,87,77),9:(180,168,164),10:(118,106,104),11:(70,60,56),12:(248,221,95),13:(213,186,91),14:(255,255,255),15:(98,50,28)}
o=np.load(sys.argv[1]); s=int(sys.argv[3]) if len(sys.argv)>3 else 8
img=np.zeros(o.shape+(3,),'uint8')
for k,c in P.items(): img[o==k]=c
im=Image.fromarray(img).resize((o.shape[1]*s,o.shape[0]*s),0)
from PIL import ImageDraw; d=ImageDraw.Draw(im)
if s>1:
  for x in range(0,o.shape[1]*s,s*8): d.line([(x,0),(x,im.height)],fill=(200,200,255))
  for y in range(0,o.shape[0]*s,s*8): d.line([(0,y),(im.width,y)],fill=(200,200,255))
im.save(sys.argv[2])
