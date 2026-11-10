# box1x.py raster out [x0 y0 x1 y1 z]: BOX-verkleind model | sprite, op 1x-niveau vergroot
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from PIL import Image
from geo import *
import pal
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB')
m=src.crop((int(OX),int(OY),int(OX+64*S),int(OY+64*S))).resize((64,64),Image.BOX)
s=pal.rgb(pal.load(sys.argv[1]),bg=(255,255,255))
x0,y0,x1,y1,z=list(map(int,sys.argv[3:8])) if len(sys.argv)>3 else [0,0,64,64,6]
o=Image.new('RGB',(2*(x1-x0)*z+8,(y1-y0)*z),'white')
o.paste(m.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),(0,0))
o.paste(s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),((x1-x0)*z+8,0))
o.save(sys.argv[2])
