# Model (natief) met het spriteraster erover + de huidige sprite ernaast, voor een zone. python3 rooster.py IN.txt i0 i1 j0 j1 UIT.png
import numpy as np; from PIL import Image, ImageDraw; import sys
from reduce_pal import PAL
S=1.6; X0,Y0=17,20; Z=24
o=np.loadtxt(sys.argv[1],dtype=int); i0,i1,j0,j1=map(int,sys.argv[2:6])
nat=Image.open('natief.png').convert('RGB')
big=nat.resize((100*15,100*15),Image.NEAREST)   # 1 natieve px = 15 -> spritecel = 24
cx0=int((X0+i0*S)*15); cy0=int((Y0+j0*S)*15)
w=(i1-i0)*Z; h=(j1-j0)*Z
m=big.crop((cx0,cy0,cx0+w,cy0+h)); d=ImageDraw.Draw(m)
for k in range(i1-i0+1): d.line([(k*Z,0),(k*Z,h)],fill=(255,0,0))
for k in range(j1-j0+1): d.line([(0,k*Z),(w,k*Z)],fill=(255,0,0))
rgb=np.array([(235,235,235)]+PAL[1:])[o[j0:j1,i0:i1]].astype('uint8')
sp=Image.fromarray(rgb).resize((w,h),Image.NEAREST); d2=ImageDraw.Draw(sp)
for k in range(i1-i0+1): d2.line([(k*Z,0),(k*Z,h)],fill=(255,0,0))
for k in range(j1-j0+1): d2.line([(0,k*Z),(w,k*Z)],fill=(255,0,0))
v=Image.new('RGB',(2*w+30,h+20),'white'); v.paste(sp,(0,20)); v.paste(m,(w+30,20)); dv=ImageDraw.Draw(v)
for k in range(i1-i0):
    dv.text((k*Z+6,4),str(i0+k),fill=(0,0,255)); dv.text((w+30+k*Z+6,4),str(i0+k),fill=(0,0,255))
for k in range(j1-j0): dv.text((2*w+2+8,20+k*Z+6),str(j0+k),fill=(0,0,255))
v.save(sys.argv[6])
