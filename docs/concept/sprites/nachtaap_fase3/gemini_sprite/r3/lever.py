"""Levert r3: muriqui.png (oog C), muriqui_8x.png, normal.pal, vel.png"""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
from tools import *
import subprocess
HOOFD='C'
subprocess.run(['python3','build.py',HOOFD],check=True)
a=load('raster.txt'); png(a,'muriqui.png')
r=np.array(rgb(a).convert('RGBA')); r[a==0,3]=0
Image.fromarray(r).resize((512,512),Image.NEAREST).save('muriqui_8x.png')
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%((152,208,160) if k==0 else P[k]) for k in range(16)))
subprocess.run(['python3','vel.py','raster.txt','vel_tmp.png'],check=True)
import shutil; shutil.move('vel_tmp.png','vel.png')
