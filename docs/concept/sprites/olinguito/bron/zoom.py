import sys
sys.path.insert(0,'/home/user/projectgrounded/tools/concept/sprites')
import spritelib as L
from PIL import Image, ImageDraw
a,pal=L.load_png(sys.argv[1]); f=int(sys.argv[3]); x0,y0,x1,y1=map(int,sys.argv[4].split(',')); z=int(sys.argv[5]) if len(sys.argv)>5 else 12
fr=a[f*64:(f+1)*64][y0:y1,x0:x1]
im=L.checker_bg(fr.shape[1]*z,fr.shape[0]*z,z); im.alpha_composite(L.scaled(L.rgb_img(fr,pal),z))
d=ImageDraw.Draw(im)
for i in range(fr.shape[1]+1):
    d.line([(i*z,0),(i*z,im.height)],fill=(0,0,0,60) if (x0+i)%8 else (0,0,255,140))
for j in range(fr.shape[0]+1):
    d.line([(0,j*z),(im.width,j*z)],fill=(0,0,0,60) if (y0+j)%8 else (0,0,255,140))
for i in range(0,fr.shape[1],2): d.text((i*z+2,2),str(x0+i),fill=(0,0,255,255))
for j in range(0,fr.shape[0],2): d.text((2,j*z+2),str(y0+j),fill=(0,0,255,255))
im.save(sys.argv[2])
