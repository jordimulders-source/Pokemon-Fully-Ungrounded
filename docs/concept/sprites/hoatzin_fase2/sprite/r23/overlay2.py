# overlay2.py uit.png: slagpennen-lijnen (lijnen.SCHACHT geel, SCHEID cyaan) over het model en over r21, 20x
import sys; from PIL import ImageDraw
from raster import *; import lijnen as LJ, math
x0,y0,x1,y1,K=30,2,58,30,20
def wit(p):
    s=Image.open(p).convert('RGBA'); w=Image.new('RGB',(64,64),'white'); w.paste(s,(0,0),s); return w
ims=[grid(model_img(K,x0,y0,x1,y1),K,x0,y0), grid(wit('hoatzin.png').crop((x0,y0,x1,y1)).resize(((x1-x0)*K,(y1-y0)*K),Image.NEAREST),K,x0,y0)]
def P(p):
    t=math.radians(p[0]); return ((LJ.C[0]+p[1]*math.cos(t)-x0)*K,(LJ.C[1]+p[1]*math.sin(t)-y0)*K)
for im in ims[:1]:
    d=ImageDraw.Draw(im)
    for pl in LJ.SCHACHT: d.line([P(p) for p in pl],fill=(255,230,0),width=2)
    for pl in LJ.SCHEID: d.line([P(p) for p in pl],fill=(0,255,255),width=2)
ims=[labels(i,K,18,x0,y0,28) for i in ims]
c=Image.new('RGB',(ims[0].width*2+10,ims[0].height),'white'); c.paste(ims[0],(0,0)); c.paste(ims[1],(ims[0].width+10,0)); c.save(sys.argv[1])
