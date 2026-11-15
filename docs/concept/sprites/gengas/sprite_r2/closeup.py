# closeup.py naam x0 y0 x1 y1 : sprite | kleurgids op 12x naast elkaar (alleen weergave)
import sys
from PIL import Image
n,x0,y0,x1,y1=sys.argv[1],*map(int,sys.argv[2:6]); S=12
s=Image.open('gengas_r2.png').convert('RGBA'); k=Image.open('../model/kleurgids_64.png').convert('RGBA')
w,h=(x1-x0)*S,(y1-y0)*S
V=Image.new('RGBA',(2*w+12,h),(255,255,255,255))
a=Image.new('RGBA',(64,64),(255,255,255,255)); a.alpha_composite(s)
V.paste(a.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(0,0)); V.paste(k.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(w+12,0))
V.save(n)
