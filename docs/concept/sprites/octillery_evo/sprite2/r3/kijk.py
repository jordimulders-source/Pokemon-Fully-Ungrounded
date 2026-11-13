# r3/kijk.py uit.png : snelle blik: 8x licht | 8x donker, daaronder 1x/2x/4x op licht en donker
import sys; sys.path.insert(0,'r3'); sys.path.insert(0,'.')
import bouw3,cfg
from PIL import Image
a=cfg.read('r3/raster.txt'); BG=(208,208,176,255); DK=(72,80,96,255)
v=Image.new('RGB',(1040,512+270),(255,255,255))
v.paste(cfg.rgba(a,BG).resize((512,512),0),(0,0)); v.paste(cfg.rgba(a,DK).resize((512,512),0),(520,0))
x=0
for bg in (BG,DK):
    for k in (1,2,4):
        v.paste(cfg.rgba(a,bg).resize((64*k,64*k),0),(x,516)); x+=64*k+6
v.save(sys.argv[1])
