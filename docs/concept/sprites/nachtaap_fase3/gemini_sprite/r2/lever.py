"""Levert r1: muriqui.png (hoofdversie, oog C), oog_A/B/C.png, muriqui_8x.png, normal.pal, vel.png"""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
from tools import *
import subprocess
HOOFD='C'
subprocess.run(['python3','build.py',HOOFD],check=True)
for v in 'ABC': png(load(f'raster_{v}.txt'),f'oog_{v}.png')
a=load('raster.txt'); png(a,'muriqui.png')
r=np.array(rgb(a).convert('RGBA')); r[a==0,3]=0
Image.fromarray(r).resize((512,512),Image.NEAREST).save('muriqui_8x.png')
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%((152,208,160) if k==0 else P[k]) for k in range(16)))
subprocess.run(['python3','vel.py','raster.txt','vel_tmp.png'],check=True)
V=Image.open('vel_tmp.png'); os.remove('vel_tmp.png')
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
H=V.size[1]; W=Image.new('RGB',(V.size[0],H+26*12+60),'white'); W.paste(V,(0,0)); d=ImageDraw.Draw(W)
d.text((10,H+4),'oogvarianten (kop 12x): A 2 rijen plat | B 3 rijen plat | C 3 rijen, platte bovenrand + ronde onderkant (hoofdversie)',font=F,fill='black')
for k,v in enumerate('ABC'):
    im=rgb(load(f'raster_{v}.txt'))
    W.paste(im.crop((1,24,18,48)).resize((17*12,24*12),Image.NEAREST),(10+k*(17*12+16),H+26))
    d.text((14+k*(17*12+16),H+30),v,font=F,fill='red')
W.save('vel.png')
