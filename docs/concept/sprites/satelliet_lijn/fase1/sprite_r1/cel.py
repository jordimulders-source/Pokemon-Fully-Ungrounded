# cel.py y0 y1 x0 x1 : per spritepixel de modelpixels (klasse-letters) die erin vallen + spritewaarde
import sys,numpy as np
from PIL import Image
a=np.asarray(Image.open('../model/model_gekozen_natief.png').convert('RGB')).astype(int)
lum=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]; sat=a.max(2)-a.min(2)
def L(y,x):
    r,g,b=a[y,x]; l=lum[y,x]
    if min(r,g,b)>=244: return 'W' if 25<x<75 and 25<y<75 else '.'
    if l<45: return '#'
    if g>r+15: return 'T' if l>150 else 't'
    if sat[y,x]>=55: return 'D' if l<75 else ('P' if l<100 else ('p' if l<150 else 'h'))
    return 'w' if l>=222 else ('l' if l>=185 else ('1' if l>=150 else '2'))
f=59/75; X0,Y0,OX,OY=17,16,2,6
o=np.load(sys.argv[5]) if len(sys.argv)>5 else np.load('kaal.npy')
CH=".#DPpWwlmTt"
y0,y1,x0,x1=map(int,sys.argv[1:5])
from collections import defaultdict
c=defaultdict(str)
for y in range(99):
  for x in range(99):
    c[(int(OY+(y-Y0+0.5)*f),int(OX+(x-X0+0.5)*f))]+=L(y,x)
for sy in range(y0,y1):
    print('%2d '%sy+' '.join('%s:%-4s'%(CH[o[sy,sx]],c[(sy,sx)]) for sx in range(x0,x1)))
