# overlay.py uit.png x0 y0 x1 y1 K: model-uitsnede met de afgelezen lijnen (lijnen.py) in rood/geel
import sys; from PIL import ImageDraw
from raster import *; from lijnen import PLUK, VEER
x0,y0,x1,y1,K=map(int,sys.argv[2:7])
im=grid(model_img(K,x0,y0,x1,y1),K,x0,y0); d=ImageDraw.Draw(im)
P=lambda p:((p[0]-x0+.5)*K,(p[1]-y0+.5)*K)
for pl in PLUK.values(): d.line([P(p) for p in pl],fill=(255,230,0),width=2)
for pl in VEER: d.line([P(p) for p in pl],fill=(0,255,255),width=2)
labels(im,K,18,x0,y0,max(x1-x0,y1-y0)).save(sys.argv[1])
