# vel.py txt uit.png : sprite 8x | kale reductie 8x | model op dezelfde schaal, + 1x op licht en donker
import sys,numpy as np; from PIL import Image; from pal import *
g=lees(sys.argv[1]); k=lees(sys.argv[3] if len(sys.argv)>3 else 'kaal.txt'); S=8
def im(t,bg=(255,255,255)): return Image.fromarray(rgb(t,bg))
h,w=g.shape
m=Image.open('../gemini/r1.png').convert('RGB')
# modeluitsnede die overeenkomt met de bbox (natief x18.., y4.. -> model px 9.75+10.24*n)
x0=9.75+10.24*18; y0=9.75+10.24*4; m=m.crop((int(x0),int(y0),int(x0+10.24*2*w),int(y0+10.24*2*h))).resize((w*S,h*S),Image.LANCZOS)
pan=[im(g).resize((w*S,h*S),Image.NEAREST),im(k).resize((w*S,h*S),Image.NEAREST),m]
V=Image.new('RGB',(3*(w*S+16)+16+2*(64*2+16),h*S+32),(255,255,255))
for i,p in enumerate(pan): V.paste(p,(16+i*(w*S+16),16))
# 64x64 1x op licht en donker (2x getoond zodat het zichtbaar is) + echte 1x
s=np.full((64,64),'.'); s[64-h:64,(64-w)//2:(64-w)//2+w]=g
for j,bg in enumerate([(232,232,232),(40,44,56)]):
    t=Image.fromarray(rgb(s,bg)); ox=16+3*(w*S+16)+j*(64*2+16)
    V.paste(t.resize((128,128),Image.NEAREST),(ox,16)); V.paste(t,(ox,16+140))
V.save(sys.argv[2])
