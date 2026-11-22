# zoom.py sprite.png x0 y0 x1 y1 uit  (spritecoord in 61-raster); links het natieve model (zelfde gebied, via de schrap-index), rechts de sprite, 16x
import sys,numpy as np; from PIL import Image
sp=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); uit=sys.argv[6]
wk,wr=np.load('weg.npy'); keepc=[c for c in range(75) if c not in wk]; keepr=[r for r in range(75) if r not in wr]
n=Image.open('natief.png').convert('RGB').crop((12,16,87,91))
# modelgebied dat bij deze spritekolommen hoort
mx0,mx1=keepc[x0],keepc[x1-1]+1; my0,my1=keepr[y0],keepr[y1-1]+1
m=n.crop((mx0,my0,mx1,my1)); S=16
m=m.resize((m.width*S,m.height*S),Image.NEAREST)
s=Image.open(sp).convert('RGB').crop((x0+1,y0+3,x1+1,y1+3)); s=s.resize((s.width*S,s.height*S),Image.NEAREST)
v=Image.new('RGB',(m.width+s.width+16,max(m.height,s.height)),(255,255,255)); v.paste(m,(0,0)); v.paste(s,(m.width+16,0)); v.save(uit)
