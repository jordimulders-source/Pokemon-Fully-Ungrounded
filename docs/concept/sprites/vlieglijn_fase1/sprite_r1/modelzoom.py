# alleen het model (natief) met spriteraster en coordinaten, groot. python3 modelzoom.py i0 i1 j0 j1 UIT.png
import numpy as np; from PIL import Image, ImageDraw; import sys
S=1.6; X0,Y0=17,20; Z=40; F=25   # 1 natieve px = 25, spritecel = 40
i0,i1,j0,j1=map(int,sys.argv[1:5])
nat=Image.open('natief.png').convert('RGB').resize((100*F,100*F),Image.NEAREST)
cx0=int((X0+i0*S)*F); cy0=int((Y0+j0*S)*F); w=(i1-i0)*Z; h=(j1-j0)*Z
m=nat.crop((cx0,cy0,cx0+w,cy0+h)); d=ImageDraw.Draw(m)
for k in range(i1-i0+1): d.line([(k*Z,0),(k*Z,h)],fill=(255,0,0))
for k in range(j1-j0+1): d.line([(0,k*Z),(w,k*Z)],fill=(255,0,0))
for k in range(i1-i0):
    for l in range(j1-j0): d.text((k*Z+2,l*Z+2),'%d,%d'%(i0+k,j0+l),fill=(255,0,160))
m.save(sys.argv[5])
