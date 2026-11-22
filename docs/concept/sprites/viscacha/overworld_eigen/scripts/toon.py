"""Toon een of meer rasters op 8x naast de front (3x) en echte OW-sprites. Gebruik: toon.py uit.png raster1.txt [raster2.txt ...]"""
import sys,os,numpy as np
from PIL import Image
sys.path.insert(0,os.path.dirname(__file__)); from ow_pal import *
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../../..'))
BG=(200,220,200)
out_p=sys.argv[1]; ras=[parse(open(p).read()) for p in sys.argv[2:]]
f,_=front_rgba(R+'/docs/concept/sprites/viscacha/af/viscacha.png',R+'/docs/concept/sprites/viscacha/af/normal.pal')
tiles=[f.resize((192,192),Image.NEAREST)]
for a in ras: tiles.append(rgba(a).resize((256,256),Image.NEAREST))
for a in ras: tiles.append(rgba(a).resize((32,32),Image.NEAREST))
W=sum(t.width for t in tiles)+10*len(tiles); out=Image.new('RGBA',(W,256),BG+(255,))
x=0
for t in tiles: out.alpha_composite(t,(x,0)); x+=t.width+10
out.save(out_p)
